"""
Immutable Core Untranslatable Glossary (§10)
Preserves semantic integrity of foundational Sanātana Dharma concepts
across all languages (Sanskrit, Bengali, Hindi, English).
"""

from typing import Dict
from pydantic import BaseModel


class GlossaryEntry(BaseModel):
    sanskrit_iast: str
    devanagari: str
    bengali: str
    hindi: str
    essential_meaning: str
    avoid_simplifications: str


CORE_GLOSSARY: Dict[str, GlossaryEntry] = {
    "Dharma": GlossaryEntry(
        sanskrit_iast="Dharma",
        devanagari="धर्म",
        bengali="ধর্ম",
        hindi="धर्म",
        essential_meaning="Cosmic order, righteousness, intrinsic nature, ethical duty, and that which upholds existence.",
        avoid_simplifications="Never reduce to mere 'religion', 'creed', or 'sectarian faith'."
    ),
    "Karma": GlossaryEntry(
        sanskrit_iast="Karma",
        devanagari="कर्म",
        bengali="কর্ম",
        hindi="कर्म",
        essential_meaning="Intentional action (mental, vocal, physical) and its inexorable causal impression and consequence.",
        avoid_simplifications="Never reduce to fatalistic 'luck', 'destiny', or passive 'fate'."
    ),
    "Ṛta": GlossaryEntry(
        sanskrit_iast="Ṛta",
        devanagari="ऋत",
        bengali="ঋত",
        hindi="ऋत",
        essential_meaning="The primordial cosmic rhythm, natural dynamic order, and truth governing the universe.",
        avoid_simplifications="Never equate to rigid human statutory law."
    ),
    "Ātman": GlossaryEntry(
        sanskrit_iast="Ātman",
        devanagari="आत्मन्",
        bengali="আত্মা",
        hindi="आत्मा",
        essential_meaning="The true immortal Self, witness consciousness (sākṣin), distinct from body, senses, and ego.",
        avoid_simplifications="Never confuse with psychological ego, personality, or mortal soul."
    ),
    "Brahman": GlossaryEntry(
        sanskrit_iast="Brahman",
        devanagari="ब्रह्मन्",
        bengali="ব্রহ্ম",
        hindi="ब्रह्म",
        essential_meaning="The ultimate, infinite, unconditioned reality; foundational substratum of all existence.",
        avoid_simplifications="Never confuse with the creator deity Brahmā (चतुर्मुख ब्रह्मा) or the priest Brāhmaṇa."
    ),
    "Māyā": GlossaryEntry(
        sanskrit_iast="Māyā",
        devanagari="माया",
        bengali="মায়া",
        hindi="माया",
        essential_meaning="The inexplicable creative power that projects names and forms, veiling unconditioned reality.",
        avoid_simplifications="Never reduce to mere non-existent hallucination; it has empirical (vyāvahārika) reality."
    ),
    "Yoga": GlossaryEntry(
        sanskrit_iast="Yoga",
        devanagari="योग",
        bengali="যোগ",
        hindi="योग",
        essential_meaning="Integration of consciousness, spiritual discipline, and experiential union with ultimate reality.",
        avoid_simplifications="Never reduce to merely physical postures (āsanas) or exercise gymnastics."
    ),
    "Yajña": GlossaryEntry(
        sanskrit_iast="Yajña",
        devanagari="यज्ञ",
        bengali="যজ্ঞ",
        hindi="यज्ञ",
        essential_meaning="Sacred offering, selfless reciprocal contribution, and dedication of action to the cosmic whole.",
        avoid_simplifications="Never reduce solely to ritual animal slaughter or primitive fire rites."
    ),
    "Tapas": GlossaryEntry(
        sanskrit_iast="Tapas",
        devanagari="तपस्",
        bengali="তপস্যা",
        hindi="तपस्या",
        essential_meaning="Spiritual ardour, purifying self-discipline, and focused transformative inner heat.",
        avoid_simplifications="Never equate to self-harm or morbid mortification."
    ),
    "Śraddhā": GlossaryEntry(
        sanskrit_iast="Śraddhā",
        devanagari="श्रद्धा",
        bengali="শ্রদ্ধা",
        hindi="श्रद्धा",
        essential_meaning="Earnest intellectual and intuitive trust, reverential openness grounded in discernment.",
        avoid_simplifications="Never equate to blind, unquestioning dogmatic credulity."
    ),
    "Mokṣa": GlossaryEntry(
        sanskrit_iast="Mokṣa",
        devanagari="मोक्ष",
        bengali="মোক্ষ",
        hindi="मोक्ष",
        essential_meaning="Liberation from the cycle of birth and death (saṃsāra), cessation of ignorance, self-realization.",
        avoid_simplifications="Never describe merely as a post-mortem heavenly realm (svarga)."
    )
}


def lookup_glossary_term(term: str) -> GlossaryEntry:
    """Case-insensitive lookup for core terms."""
    normalized = term.strip().capitalize()
    for key, entry in CORE_GLOSSARY.items():
        if key.lower() == normalized.lower():
            return entry
    raise KeyError(f"Term '{term}' not found in core untranslatable glossary.")
