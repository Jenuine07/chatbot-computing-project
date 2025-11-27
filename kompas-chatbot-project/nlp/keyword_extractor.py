# chatbot_project/nlp/keyword_extractor.py
import re
import numpy as np
from typing import List, Tuple

from nlp.cleaner import Cleaner
from nlp.embedding import Embedder
from nlp.mapping_filter import get_lexicon, idf_score

_YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")


class KeywordExtractor:
    """
    Pipeline:
    1) Lexicon candidates (phrases + unigrams + years)
    2) Lexical scoring (IDF + length bonus)
    3) Embed TOP_M for rerank
    4) Prefer longer phrases; dedupe substrings
    """

    #(top_k=7, top_m_for_embed=10, alpha_lex=0.1)

    def __init__(self, top_k: int = 7, top_m_for_embed: int = 10, alpha_lex: float = 0.1):
        self.cleaner = Cleaner(remove_stopwords=False)
        self.embedder = Embedder()
        self.top_k = top_k
        self.top_m_for_embed = top_m_for_embed
        self.alpha_lex = alpha_lex

        # Load lexicon
        (
            self.PHRASES,
            self.UNIGRAMS,
            self.IDF,
            self.N_DOCS,
            self.MAX_PH_TOKENS,
        ) = get_lexicon()

    # --- Candidate generation ---
    def _phrase_hits(self, tokens: List[str]) -> List[str]:
        hits = set()
        T = len(tokens)
        for i in range(T):
            for n in range(min(self.MAX_PH_TOKENS, T - i), 1, -1):
                cand = " ".join(tokens[i : i + n])
                if cand in self.PHRASES:
                    hits.add(cand)
                    break
        return sorted(hits, key=lambda s: (-len(s.split()), s))

    def _unigram_hits(self, tokens: List[str]) -> List[str]:
        return sorted({t for t in tokens if t in self.UNIGRAMS})

    def _year_hits(self, text: str) -> List[str]:
        return sorted(set(m.group(0) for m in _YEAR_RE.finditer(text)))

    # --- Scoring ---
    def _lex_score(self, term: str) -> float:
        length_bonus = 0.15 * (len(term.split()) - 1)
        return idf_score(term) + length_bonus + 1.0

    def _blend_scores(
        self,
        items: List[Tuple[str, float]],
        sent_emb: np.ndarray,
    ) -> List[Tuple[str, float]]:
        if not items:
            return []

        lex_vals = np.array([s for _, s in items], dtype=np.float32)
        max_lex = float(lex_vals.max()) if len(lex_vals) else 1.0
        lex_norm = (lex_vals / (max_lex if max_lex > 0 else 1.0)).tolist()

        blended = []
        for (term, lex_s), ln in zip(items, lex_norm):
            term_emb = self.embedder.get_embedding(term)
            sim = self.embedder.similarity(sent_emb, term_emb)
            sim01 = 0.5 * (sim + 1.0)  # [-1,1] -> [0,1]
            score = self.alpha_lex * ln + (1.0 - self.alpha_lex) * sim01
            blended.append((term, float(score)))

        blended.sort(key=lambda x: x[1], reverse=True)
        return blended

    def _dedupe_substrings(self, ranked_terms: List[str]) -> List[str]:
        final = []
        for cand in ranked_terms:
            if any((cand != f and cand in f) for f in final):
                continue
            final.append(cand)
            if len(final) >= self.top_k:
                break
        return final

    # --- Public API ---
    def extract(self, prompt: str) -> List[str]:
        if not prompt:
            return []

        norm_text = self.cleaner.normalize_text(prompt)
        tok_keep = self.cleaner.tokenize(prompt)  # keep stopwords not needed, we unify under one tokenizer

        ph = self._phrase_hits(tok_keep)
        uni = self._unigram_hits(tok_keep)
        yrs = self._year_hits(norm_text)

        # Merge unique candidates
        cands, seen = [], set()
        for s in ph + uni + yrs:
            if s not in seen:
                seen.add(s)
                cands.append(s)

        if not cands:
            return []

        scored = [(t, self._lex_score(t)) for t in cands]
        scored.sort(key=lambda x: x[1], reverse=True)

        top_m = scored[: self.top_m_for_embed]
        sent_emb = self.embedder.get_embedding(norm_text)
        blended = self._blend_scores(top_m, sent_emb)

        if len(scored) > self.top_m_for_embed:
            tail = scored[self.top_m_for_embed :]
            tail = [(t, s / (scored[0][1] if scored[0][1] > 0 else 1.0)) for (t, s) in tail]
            tail.sort(key=lambda x: x[1], reverse=True)
            merged = blended + tail
        else:
            merged = blended

        ranked_terms = [t for (t, _) in merged]
        return self._dedupe_substrings(ranked_terms)
