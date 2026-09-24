"""
Evidence Profile (§17)
Enforces: NO FALSE PRECISION. Never states a bare percentage like '93% true' to users.
Calculates internal triage score strictly for engineering triage.
"""

from enum import Enum
from pydantic import BaseModel, Field


class TextualConfidence(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    UNVERIFIABLE = "UNVERIFIABLE"


class QualitativeLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    NONE = "NONE"


class InterpretiveAgreement(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    DISPUTED = "DISPUTED"


class HistoricalCertainty(str, Enum):
    ESTABLISHED = "ESTABLISHED"
    DEBATED = "DEBATED"
    UNCERTAIN = "UNCERTAIN"
    UNKNOWABLE_BY_CURRENT_EVIDENCE = "UNKNOWABLE BY CURRENT EVIDENCE"


class EvidenceProfile(BaseModel):
    textual_confidence: TextualConfidence = TextualConfidence.HIGH
    source_quality: QualitativeLevel = QualitativeLevel.HIGH
    independent_corroboration: QualitativeLevel = QualitativeLevel.HIGH
    interpretive_agreement: InterpretiveAgreement = InterpretiveAgreement.HIGH
    historical_certainty: HistoricalCertainty = HistoricalCertainty.ESTABLISHED

    def calculate_internal_triage_score(
        self,
        extraction_quality: float = 1.0,
        interpretive_consistency: float = 1.0
    ) -> float:
        """
        Internal engineering triage metric only (§17).
        EvidenceScore = 0.30·source_quality + 0.25·textual_verification +
                        0.20·corroboration + 0.15·extraction_quality +
                        0.10·interpretive_consistency
        NEVER surfaced to the user as a probability of metaphysical/historical truth.
        """
        level_map = {
            QualitativeLevel.HIGH: 1.0,
            QualitativeLevel.MEDIUM: 0.6,
            QualitativeLevel.LOW: 0.3,
            QualitativeLevel.NONE: 0.0,
        }
        textual_map = {
            TextualConfidence.HIGH: 1.0,
            TextualConfidence.MEDIUM: 0.6,
            TextualConfidence.LOW: 0.3,
            TextualConfidence.UNVERIFIABLE: 0.0,
        }

        sq = level_map.get(self.source_quality, 0.5)
        tv = textual_map.get(self.textual_confidence, 0.5)
        co = level_map.get(self.independent_corroboration, 0.5)

        score = (0.30 * sq) + (0.25 * tv) + (0.20 * co) + (0.15 * extraction_quality) + (0.10 * interpretive_consistency)
        return round(score, 4)

    def format_user_facing_summary(self) -> str:
        """Surfaces qualitative profile without deceptive numerical certainty percentages."""
        return (
            f"- Textual Confidence: {self.textual_confidence.value}\n"
            f"- Source Quality: {self.source_quality.value}\n"
            f"- Independent Corroboration: {self.independent_corroboration.value}\n"
            f"- Interpretive Agreement: {self.interpretive_agreement.value}\n"
            f"- Historical Certainty: {self.historical_certainty.value}"
        )
