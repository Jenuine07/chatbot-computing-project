# chatbot_project/nlp/cleaner.py

import re
import unicodedata
from typing import List
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# Regex to keep only alphanumeric + dash (for hyphenated words) and numbers
_WORD_RE = re.compile(r"[a-z0-9\-]+", re.IGNORECASE)


class Cleaner:
    def __init__(self, remove_stopwords: bool = False):
        factory = StopWordRemoverFactory()
        self._stopper = factory.create_stop_word_remover()
        self.remove_stopwords = remove_stopwords

    def normalize_text(self, text: str) -> str:
        """Lowercase, strip spaces, normalize unicode, and remove diacritics."""
        if not text:
            return ""

        # Unicode normalization (NFKD) → ensures consistent accents/spacing
        text = unicodedata.normalize("NFKD", text)

        # Strip diacritics (é → e, ú → u, etc.)
        text = "".join([c for c in text if not unicodedata.combining(c)])

        # Lowercase
        text = text.lower()

        # Replace underscore with space
        text = text.replace("_", " ")

        # Collapse multiple spaces
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize into words.
        - Optionally remove stopwords.
        - Keeps numbers and hyphenated words.
        """
        text = self.normalize_text(text)

        if self.remove_stopwords:
            text = self._stopper.remove(text)

        return _WORD_RE.findall(text)


# --- Backward-compatible helper ---
def clean_and_tokenize(text: str, remove_stopwords: bool = False) -> List[str]:
    """Utility function for quick cleaning + tokenization."""
    return Cleaner(remove_stopwords=remove_stopwords).tokenize(text)
