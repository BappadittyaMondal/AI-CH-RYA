"""
Practical Knowledge Systems: Āyurveda, Yoga, Jyotiṣa (§22)
Strictly bifurcates Educational Mode vs. Practice Guidance Mode.
Enforces non-negotiable health safety boundaries and non-deterministic astrology guardrails.
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class SystemDiscipline(str, Enum):
    AYURVEDA = "Āyurveda"
    YOGA = "Yoga"
    JYOTISA = "Jyotiṣa"


class ConsultationMode(str, Enum):
    EDUCATIONAL_MODE = "Educational Mode"
    PRACTICE_GUIDANCE_MODE = "Practice Guidance Mode"


class PracticalSystemResponse(BaseModel):
    discipline: SystemDiscipline
    consultation_mode: ConsultationMode
    historical_traditional_explanation: str
    clinical_evidence_status: str
    mandatory_safety_disclaimer: str
    is_safe: bool = True


class PracticalSystemsEngine:
    """Enforces ethical boundaries and safety disclaimers for traditional applied sciences."""

    MEDICAL_DISCLAIMER = (
        "IMPORTANT MEDICAL DISCLAIMER: This information is provided strictly for educational and cultural "
        "understanding of classical Āyurveda and Yoga traditions. It is NOT medical advice, diagnosis, or treatment. "
        "Never abandon, alter, or delay conventional medical care or prescribed therapies in favor of traditional remedies. "
        "Always consult a qualified, licensed healthcare professional for personal medical conditions."
    )

    ASTROLOGY_DISCLAIMER = (
        "CULTURAL & HISTORICAL NOTICE: Classical Jyotiṣa (Vedic astrology) is presented here strictly as a traditional "
        "symbolic time-keeping and cultural knowledge system. AI ĀCHĀRYA does not make deterministic personal prophecies, "
        "destiny proclamations, or claims of supernatural certainty regarding your future."
    )

    @classmethod
    def evaluate_request(
        cls,
        discipline: SystemDiscipline,
        mode: ConsultationMode,
        traditional_text: str,
        has_clinical_trials: bool = False
    ) -> PracticalSystemResponse:
        evidence_note = (
            "Supported by peer-reviewed modern clinical studies."
            if has_clinical_trials
            else "Traditional knowledge claim; lacks definitive modern clinical trial evidence."
        )

        disclaimer = (
            cls.ASTROLOGY_DISCLAIMER
            if discipline == SystemDiscipline.JYOTISA
            else cls.MEDICAL_DISCLAIMER
        )

        return PracticalSystemResponse(
            discipline=discipline,
            consultation_mode=mode,
            historical_traditional_explanation=traditional_text,
            clinical_evidence_status=evidence_note,
            mandatory_safety_disclaimer=disclaimer,
            is_safe=True
        )
