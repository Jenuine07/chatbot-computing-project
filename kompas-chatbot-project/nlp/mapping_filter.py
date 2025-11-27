# chatbot_project/nlp/mapping_filter.py
import json
import math
import os
from typing import Dict, Set, Tuple

_BASE = os.path.dirname(os.path.abspath(__file__))
_PROMPTS_PATH = os.path.join(_BASE, "prompts.json")

LEXICON_PHRASES: Set[str] = set()
LEXICON_UNIGRAMS: Set[str] = set()
LEXICON_ALL: Set[str] = set()
IDF: Dict[str, float] = {}
N_DOCS: int = 1
MAX_PHRASE_TOKENS: int = 5

# --- Synonym groups ---
SYN_GROUPS = [
    {"pbb", "pajak bumi dan bangunan"},
    {"pph", "pajak penghasilan"},
    {"pph 21", "pajak penghasilan"},
    {"ppn", "pajak pertambahan nilai"},
    {"ppnbm", "pajak penjualan atas barang mewah"},
    {"imb", "izin mendirikan bangunan"},
    {"e-faktur", "faktur pajak"},
    {"e-filing", "e-filing"},
    {"npwp", "nomor pokok wajib pajak"},
    {"spt tahunan", "surat pemberitahuan tahunan"},
    {"kendaraan listrik", "kendaraan bermotor listrik"},
    {"umkm", "usaha mikro, kecil, dan menengah"},
    {"nop", "nomor objek pajak"},

    {"aturan", "ketentuan"},
    {"peraturan", "ketentuan"},
    {"regulasi", "ketentuan"},
    {"undang-undang", "ketentuan"},

    {"pajak properti", "pajak bumi dan bangunan"},
    {"pajak bumi", "pajak bumi dan bangunan"},
    {"pajak bangunan", "pajak bumi dan bangunan"},
    {"kendaraan", "kendaraan bermotor"},
    {"retribusi kebersihan", "retribusi sampah"},
    {"pedagang online", "e-commerce"},
    {"pekerja lepas", "freelancer"},
    {"pajak cukai rokok", "cukai rokok"},
]

_GROUP_BY_TERM: Dict[str, Set[str]] = {}
for grp in SYN_GROUPS:
    for t in grp:
        _GROUP_BY_TERM[t] = grp


def _token_count(s: str) -> int:
    return len(s.split())


def _load_and_build():
    global N_DOCS, MAX_PHRASE_TOKENS
    if not os.path.exists(_PROMPTS_PATH):
        return

    with open(_PROMPTS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    N_DOCS = max(1, len(data))
    df: Dict[str, int] = {}

    for item in data:
        seen_terms = set()
        for kw in item.get("gold_keywords", []):
            kw = kw.lower().strip()
            if not kw:
                continue
            if " " in kw:
                LEXICON_PHRASES.add(kw)
            else:
                LEXICON_UNIGRAMS.add(kw)
            LEXICON_ALL.add(kw)
            seen_terms.add(kw)
        for term in seen_terms:
            df[term] = df.get(term, 0) + 1

    for term in LEXICON_ALL:
        d = df.get(term, 0)
        IDF[term] = math.log(1.0 + N_DOCS / (1.0 + d))

    if LEXICON_PHRASES:
        lengths = sorted(_token_count(p) for p in LEXICON_PHRASES)
        idx = int(0.95 * (len(lengths) - 1))
        MAX_PHRASE_TOKENS = min(6, max(3, lengths[idx]))
    else:
        MAX_PHRASE_TOKENS = 4


_load_and_build()


def get_lexicon() -> Tuple[Set[str], Set[str], Dict[str, float], int, int]:
    return LEXICON_PHRASES, LEXICON_UNIGRAMS, IDF, N_DOCS, MAX_PHRASE_TOKENS


def idf_score(term: str) -> float:
    return IDF.get(term, math.log(1.0 + N_DOCS))


def expand_mapping_limited_to_gold(term: str) -> Set[str]:
    term = term.lower().strip()
    outs = {term}
    grp = _GROUP_BY_TERM.get(term)
    if grp:
        for t in grp:
            if t in LEXICON_ALL:
                outs.add(t)
    return outs
