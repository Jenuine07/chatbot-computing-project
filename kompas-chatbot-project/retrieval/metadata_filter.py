# retrieval/metadata_filter.py

"""
Metadata Filter module
Normalizes and maps structured metadata (province, year, category) 
into Qdrant filters.
"""

from typing import Optional, Dict, Any
from qdrant_client.http import models as rest
from nlp.cleaner import Cleaner
from nlp.mapping_filter import expand_mapping_limited_to_gold, SYN_GROUPS
from config.constants import PROVINCES, PROVINCE_ALIASES, CATEGORY_MAP

cleaner = Cleaner()

def normalize_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize values and map synonyms for category."""
    norm = {}

    # Province
    if metadata.get("province"):
        norm["province"] = cleaner.normalize_text(metadata["province"])

    # Year
    if metadata.get("year"):
        try:
            norm["year"] = int(metadata["year"])
        except ValueError:
            pass

    # Category
    if metadata.get("category"):
        cat = cleaner.normalize_text(metadata["category"])
        synonyms = expand_mapping_limited_to_gold(cat)
        norm["category"] = list(synonyms)[0] if synonyms else cat

    return norm


def build_filter(metadata: Dict[str, Any]) -> Optional[rest.Filter]:
    """
    Build a Qdrant filter from normalized metadata dict.
    Example:
        {"province": "papua", "year": 2022, "category": "perdagangan internasional"}
    """
    must_conditions = []

    if metadata.get("province"):
        must_conditions.append(
            rest.FieldCondition(
                key="province",
                match=rest.MatchValue(value=metadata["province"])
            )
        )

    if metadata.get("year"):
        must_conditions.append(
            rest.FieldCondition(
                key="year",
                match=rest.MatchValue(value=int(metadata["year"]))
            )
        )

    if metadata.get("category"):
        must_conditions.append(
            rest.FieldCondition(
                key="category",
                match=rest.MatchValue(value=metadata["category"])
            )
        )

    if not must_conditions:
        return None

    return rest.Filter(must=must_conditions)

def keywords_to_metadata(keywords):
    ks = [k.lower().strip() for k in keywords]

    # Province (alias → canonical)
    prov = None
    for k in ks:
        if k in PROVINCE_ALIASES:
            prov = PROVINCE_ALIASES[k]
            break
        if k in PROVINCES:
            prov = k
            break

    # Year (4-digit number)
    year = next((int(k) for k in ks if k.isdigit() and len(k) == 4), None)

    cat = None
    # for k in ks:
    #     # Direct map
    #     if k in CATEGORY_MAP:
    #         cat = CATEGORY_MAP[k]
    #         break

    #     # Synonym groups (list of sets)
    #     for group in SYN_GROUPS:
    #         if k in group:
    #             cat = list(group)[0]   # pick any representative from the set
    #             break
    #     if cat:
    #         break

    return {"province": prov, "year": year, "category": cat}
