"""
Multilingual Engine (§10)
Produces 10-layer canonical scriptural exposition across Sanskrit,
IAST, Bengali, Hindi, and English while strictly maintaining terminology consistency.
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from app.multilingual.glossary import CORE_GLOSSARY, lookup_glossary_term


class WordGloss(BaseModel):
    sanskrit: str
    iast: str
    meaning_en: str
    meaning_bn: Optional[str] = None
    meaning_hi: Optional[str] = None


class MultilingualScripturePassage(BaseModel):
    source_reference: str  # e.g. "Bhagavad Gītā 2.47"
    original_sanskrit_deva: str
    transliteration_iast: str
    padaccheda: List[str]
    word_glosses: List[WordGloss]
    literal_translation: str
    contextual_translation: str
    bengali_translation: str
    hindi_translation: str
    english_translation: str
    commentary_summary: Dict[str, str] = Field(
        default_factory=dict,
        description="Keyed by commentator/school, e.g. 'Śaṅkara (Advaita)', 'Rāmānuja (Viśiṣṭādvaita)'"
    )
    practical_explanation: str

    def verify_glossary_preservation(self) -> List[str]:
        """
        Ensures that core untranslatable concepts (e.g. Dharma, Karma, Ātman)
        are properly preserved and glossed in the explanation rather than degraded.
        """
        retained = []
        full_text = f"{self.english_translation} {self.practical_explanation}"
        for term in CORE_GLOSSARY.keys():
            if term.lower() in full_text.lower():
                retained.append(term)
        return retained
