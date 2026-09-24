"""
Final Response Architecture (§34)
Formats serious, substantive answers according to the canonical 17-layer structure.
Enforces the Final Truth Rule across all output sections.
"""

from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from app.verification.evidence import EvidenceProfile


class MasterResponseSchema(BaseModel):
    direct_answer: str
    source_text: str
    original_sanskrit: str
    transliteration: str
    word_meaning: str
    bengali_translation: str
    hindi_translation: str
    english_explanation: str
    context: str
    traditional_interpretations: str
    scholarly_historical_view: Optional[str] = None
    areas_of_disagreement: Optional[str] = None
    evidence_status: EvidenceProfile = Field(default_factory=EvidenceProfile)
    related_texts: List[str] = Field(default_factory=list)
    practical_application: str
    key_takeaways: List[str] = Field(default_factory=list)
    optional_revision_quiz: Optional[str] = None

    def render_markdown(self) -> str:
        """Assembles structured markdown output adhering to §34."""
        sections = [
            f"### 1. DIRECT ANSWER\n{self.direct_answer}\n",
            f"### 2. SOURCE / TEXT\n{self.source_text}\n",
            f"### 3. ORIGINAL SANSKRIT\n{self.original_sanskrit}\n",
            f"### 4. TRANSLITERATION (IAST)\n{self.transliteration}\n",
            f"### 5. WORD-BY-WORD MEANING (PADACCHEDA)\n{self.word_meaning}\n",
            f"### 6. BENGALI TRANSLATION (বাংলা)\n{self.bengali_translation}\n",
            f"### 7. HINDI TRANSLATION (हिन्दी)\n{self.hindi_translation}\n",
            f"### 8. ENGLISH EXPLANATION\n{self.english_explanation}\n",
            f"### 9. CONTEXT & BACKGROUND\n{self.context}\n",
            f"### 10. TRADITIONAL / COMMENTARIAL INTERPRETATIONS\n{self.traditional_interpretations}\n",
        ]

        if self.scholarly_historical_view:
            sections.append(f"### 11. SCHOLARLY & HISTORICAL VIEW\n{self.scholarly_historical_view}\n")

        if self.areas_of_disagreement:
            sections.append(f"### 12. AREAS OF DISAGREEMENT & DIVERGENT READINGS\n{self.areas_of_disagreement}\n")

        sections.append(
            f"### 13. EVIDENCE STATUS (§17)\n{self.evidence_status.format_user_facing_summary()}\n"
        )

        if self.related_texts:
            rel = "\n".join([f"- {t}" for t in self.related_texts])
            sections.append(f"### 14. RELATED TEXTS (Knowledge Graph)\n{rel}\n")

        sections.append(f"### 15. PRACTICAL APPLICATION (Ācārya Lens)\n{self.practical_application}\n")

        if self.key_takeaways:
            tk = "\n".join([f"- {t}" for t in self.key_takeaways])
            sections.append(f"### 16. KEY TAKEAWAYS\n{tk}\n")

        if self.optional_revision_quiz:
            sections.append(f"### 17. OPTIONAL REVISION QUIZ\n{self.optional_revision_quiz}\n")

        return "\n".join(sections)
