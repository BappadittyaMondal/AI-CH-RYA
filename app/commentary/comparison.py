"""
Commentary Comparison Engine (§12)
Presents established lineages (Advaita, Viśiṣṭādvaita, Dvaita, Bhedābheda, Śaiva/Śākta) side-by-side.
Never manufactures a false consensus; never picks a 'winner'.
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class LineageReading(BaseModel):
    sampradaya: str  # e.g. "Advaita Vedānta", "Viśiṣṭādvaita Vedānta", "Dvaita Vedānta"
    commentator: str  # e.g. "Ādi Śaṅkarācārya", "Śrī Rāmānujācārya", "Śrī Madhvācārya"
    textual_basis: str  # specific sutra, karika, or commentary section
    core_claim: str
    underlying_assumption: str  # e.g. Kevalādvaita (non-duality of Brahman & Atman), Seśvara Parināma


class CommentaryComparison(BaseModel):
    verse_id: str
    readings: List[LineageReading] = Field(default_factory=list)
    shared_ground: str
    points_of_difference: List[str] = Field(default_factory=list)
    philosophical_tension: str

    def assert_no_winner_picked(self) -> bool:
        """
        Validates that the comparison maintains neutrality and scholarly integrity
        without declaring one lineage victorious or absolute.
        """
        forbidden_phrases = [
            "the correct interpretation is",
            "the true meaning is only",
            "proves that other schools are wrong",
            "wins the debate decisively",
            "the superior school is"
        ]
        comparison_text = f"{self.shared_ground} {' '.join(self.points_of_difference)} {self.philosophical_tension}".lower()
        for phrase in forbidden_phrases:
            if phrase in comparison_text:
                return False
        return True
