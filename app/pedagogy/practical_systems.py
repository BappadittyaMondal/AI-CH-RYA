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
    emergency_referral_active: bool = False
    emergency_referral_details: Optional[str] = None


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

    ACUTE_EMERGENCY_SYMPTOMS = [
        "chest pain", "heart attack", "angina", "cardiac arrest", "crushing chest",
        "shortness of breath", "cannot breathe", "severe asthma", "cyanosis",
        "stroke", "facial drooping", "slurred speech", "sudden paralysis",
        "seizure", "convulsions", "unconscious", "unresponsive", "diabetic ketoacidosis", "hypoglycemic shock",
        "suicide", "kill myself", "end my life", "self-harm",
        "stiff neck with fever", "meningitis", "severe acute bleeding", "massive bleeding", "haemorrhage",
        "anaphylaxis", "anaphylactic", "poisoning", "toxic ingestion", "overdose", "severe allergic reaction",
        "sudden blindness"
    ]

    ADVERSARIAL_CLINICAL_PATTERNS = [
        r"\b(?:ignore|override|bypass)\b.*\b(?:medical|disclaimer|safety|doctor|protocols?)\b",
        r"\b(?:prescribe|dispense)\b.*\b(?:exact\s+dosage|grams?|mg|dose|prescription)\b",
        r"\b(?:diagnose\s+me|diagnose\s+my|what\s+disease\s+do\s+i\s+have)\b",
        r"\b(?:act\s+as\s+(?:a|an)?\s*(?:unconstrained|jailbroken|unlicensed)?\s*(?:doctor|physician|vaidya))\b"
    ]

    EMERGENCY_REDIRECT_NOTICE = (
        "CRITICAL EMERGENCY RED-FLAG DETECTED: Immediately seek emergency clinical care at an emergency room "
        "or call emergency services (National Emergency: 112, Ambulance: 108, Tele-MANAS: 14416 / 1800-891-4416, "
        "Crisis Lifeline: 988). Classical herbal or home remedies must never be substituted for emergency medicine."
    )

    ADVERSARIAL_REFUSAL_NOTICE = (
        "NON-NEGOTIABLE SAFETY GATE (§22): AI ĀCHĀRYA is not a Software as a Medical Device (SaMD) and is "
        "strictly prohibited from issuing clinical diagnoses, prescribing dosages, or overriding healthcare safety "
        "protocols. Please consult a qualified licensed medical physician or registered Ayurvedic doctor (BAMS/MD)."
    )

    @classmethod
    def check_acute_emergency(cls, text: str) -> Optional[str]:
        """Scans inquiry text for acute, life-threatening symptoms requiring emergency clinical triage."""
        text_lower = text.lower()
        for symptom in cls.ACUTE_EMERGENCY_SYMPTOMS:
            if symptom in text_lower:
                return symptom
        return None

    @classmethod
    def check_adversarial_clinical(cls, text: str) -> Optional[str]:
        """Scans inquiry text for adversarial prompt injection attempting to coerce medical diagnosis or prescription."""
        import re
        text_lower = text.lower()
        for pattern in cls.ADVERSARIAL_CLINICAL_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return pattern
        return None

    @classmethod
    def evaluate_request(
        cls,
        discipline: SystemDiscipline,
        mode: ConsultationMode,
        traditional_text: str,
        has_clinical_trials: bool = False
    ) -> PracticalSystemResponse:
        # 1. Emergency Red-Flag Screening (Patient Safety Gate)
        emergency_trigger = cls.check_acute_emergency(traditional_text)
        if emergency_trigger and discipline in [SystemDiscipline.AYURVEDA, SystemDiscipline.YOGA]:
            return PracticalSystemResponse(
                discipline=discipline,
                consultation_mode=mode,
                historical_traditional_explanation=(
                    f"EMERGENCY CLINICAL TRIAGE TRIGGERED for suspected acute symptom: '{emergency_trigger}'. "
                    "Traditional educational consultation is terminated to prevent medical delay."
                ),
                clinical_evidence_status="UNSAFE_FOR_TRADITIONAL_CONSULTATION: Emergency Medical Evaluation Required Immediately.",
                mandatory_safety_disclaimer=cls.MEDICAL_DISCLAIMER,
                is_safe=False,
                emergency_referral_active=True,
                emergency_referral_details=cls.EMERGENCY_REDIRECT_NOTICE
            )

        # 2. Adversarial Clinical Jailbreak Screening (§22 Gate)
        jailbreak_match = cls.check_adversarial_clinical(traditional_text)
        if jailbreak_match and discipline in [SystemDiscipline.AYURVEDA, SystemDiscipline.YOGA]:
            return PracticalSystemResponse(
                discipline=discipline,
                consultation_mode=mode,
                historical_traditional_explanation=(
                    "ADVERSARIAL CLINICAL ATTEMPT BLOCKED: Request to diagnose or prescribe pharmaceutical/herbal "
                    "treatment violates clinical safety protocols (§22)."
                ),
                clinical_evidence_status="REFUSED: Clinical diagnostic and prescriptive authority withheld by safety firewall.",
                mandatory_safety_disclaimer=cls.MEDICAL_DISCLAIMER,
                is_safe=False,
                emergency_referral_active=False,
                emergency_referral_details=cls.ADVERSARIAL_REFUSAL_NOTICE
            )

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
            is_safe=True,
            emergency_referral_active=False,
            emergency_referral_details=None
        )
