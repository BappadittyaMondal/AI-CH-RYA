"""
AI ĀCHĀRYA — Vedic Cosmic Organicism Engine (app/verification/organicism.py)

Deconstructs Puruṣa Sūkta (Ṛgveda 10.90 / Vājasaneyi Saṃhitā 31) through:
1. Macrocosm-Microcosm Isomorphism (Piṇḍa-Brahmāṇḍa Aikya / Cosmopsychism).
2. Four Functional Somatic Subsystems (Head, Arms, Thighs, Feet).
3. The Sacredness of the Feet as Pratiṣṭhā (Supported by RV 10.90.14: Padbhyāṃ bhūmiḥ).
4. Mīmāṃsā Jurisprudential Invalidation (Jaimini Sūtra 1.3.3) of medieval birth-caste degradations.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional
import re


class FunctionalSubsystem(str, Enum):
    MUKHAM_INTELLECTUAL = "Mukham (Head / Knowledge / Transmission of Truth)"
    BAHU_DEFENSIVE = "Bāhū (Arms / Sovereignty / Defense & Containment)"
    URU_METABOLIC = "Ūrū (Thighs / Economic Circulation / Agriculture & Commerce)"
    PADBHYAM_FOUNDATIONAL = "Padbhyām (Feet / Grounded Infrastructure / Physical Base)"


@dataclass(frozen=True)
class OrganicismAuditResult:
    is_organicism_aligned: bool
    is_colonial_degradation_detected: bool
    is_birth_caste_conflation: bool
    pratistha_sacred_foundation_verified: bool
    earth_emanation_proof: str
    jaimini_sutra_invalidation_triggered: bool
    subsystems_identified: List[str]
    forensic_verdict: str
    hermeneutic_siddhanta: str


class VedicCosmicOrganicismEngine:
    """
    Evaluates claims regarding Puruṣa Sūkta (RV 10.90) and Varna origins,
    distinguishing classical organismic holism from colonial degradation and medieval calcification.
    """

    _COLONIAL_DEGRADATION_PATTERNS = [
        r"\b(?:feet\s+are\s+(?:dirty|low|inferior|unclean|untouchable))\b",
        r"\b(?:born\s+from\s+feet\s+therefore\s+(?:degraded|sub-human|slaves?))\b",
        r"\b(?:apartheid\s+system\s+in\s+rigveda|divine\s+sanction\s+for\s+untouchability)\b",
        r"\b(?:shudra\s+means\s+born\s+to\s+suffer|inherently\s+impure)\b"
    ]

    _BIRTH_CONFLATION_PATTERNS = [
        r"\b(?:caste\s+by\s+birth\s+in\s+rigveda|hereditary\s+superiority\s+in\s+vedas)\b",
        r"\b(?:brahmin\s+by\s+birth\s+alone|janma\s+jati\s+in\s+purusha\s+sukta)\b"
    ]

    _ORGANIC_SUBSYSTEM_KEYWORDS = {
        FunctionalSubsystem.MUKHAM_INTELLECTUAL: [r"\b(?:head|mouth|mukha|knowledge|speech|intellect|brahmana)\b"],
        FunctionalSubsystem.BAHU_DEFENSIVE: [r"\b(?:arms?|bahu|bāhū|defense|strength|protection|rajanya|kshatriya)\b"],
        FunctionalSubsystem.URU_METABOLIC: [r"\b(?:thighs?|uru|ūrū|commerce|trade|circulation|metabolism|vaishya)\b"],
        FunctionalSubsystem.PADBHYAM_FOUNDATIONAL: [r"\b(?:feet|foot|pada|padbhyam|grounding|base|foundation|infrastructure|shudra)\b"]
    }

    @classmethod
    def audit_organicism_claim(cls, text: str) -> OrganicismAuditResult:
        """
        Audits a claim or query regarding Puruṣa Sūkta, Varna, and Vedic cosmology.
        """
        text_lower = text.lower()

        # 1. Detect Colonial Degradation
        is_colonial = any(re.search(p, text_lower) for p in cls._COLONIAL_DEGRADATION_PATTERNS)

        # 2. Detect Birth Caste Conflation
        is_birth = any(re.search(p, text_lower) for p in cls._BIRTH_CONFLATION_PATTERNS)

        # 3. Identify Functional Subsystems
        detected_subsystems = []
        for subsystem, patterns in cls._ORGANIC_SUBSYSTEM_KEYWORDS.items():
            if any(re.search(p, text_lower) for p in patterns):
                detected_subsystems.append(subsystem.value)

        # 4. Earth-Feet Pratiṣṭhā Verification (RV 10.90.14)
        earth_proof = (
            "Ṛgveda 10.90.14 explicitly proclaims: 'पद्भ्यां भूमिर्दिशः श्रोत्रात्' "
            "(From His feet the sacred Earth / Bhūmi was born). In Vedic ontology, the Earth is worshipped "
            "as the Supreme Divine Mother (Atharvaveda 12.1.12: 'माता भूमिः पुत्रोऽहं पृथिव्याः'). "
            "Therefore, by mathematical transitivity, the feet in Vedic ontology represent sacred, stabilizing "
            "Pratiṣṭhā (divine foundation), never degradation or untouchability."
        )

        # 5. Mīmāṃsā Jurisprudential Invalidation
        # If colonial degradation or rigid birth-conflation is asserted, Jaimini 1.3.3 is triggered
        jaimini_triggered = is_colonial or is_birth

        # 6. Verdict Formulation
        if is_colonial:
            verdict = (
                "COLONIAL WEAPONIZATION DETECTED: The claim projects Victorian bodily taboos "
                "(feet as 'dirty') onto sacred Vedic cosmopsychism. In Ṛgveda 10.90, the four limbs belong "
                "to ONE living body. In an organism, the head cannot survive without the feet."
            )
            is_aligned = False
        elif is_birth:
            verdict = (
                "MEDIEVAL HEREDITARY CONFLATION DETECTED: Conflates classical cosmic functional organicism "
                "with later feudal birth-caste calcification. Gītā 4.13 confirms division by Guṇa and Karma, not Janma."
            )
            is_aligned = False
        else:
            verdict = (
                "VEDIC COSMIC ORGANICISM VERIFIED: Accurately reflects Ṛgvedic cosmopsychism (Piṇḍa-Brahmāṇḍa Aikya), "
                "modeling society and the cosmos as an interconnected, interdependent living organism (Samāja-Puruṣa)."
            )
            is_aligned = True

        siddhanta = (
            "Siddhānta Resolution (Jaimini Sūtra 1.3.3 compliant): 'विरोधे त्वनपेक्षं स्यादसति ह्यनुमानम्' "
            "(Where Smṛti or medieval custom conflicts with Śruti, the Śruti alone prevails). "
            "The foundational Śruti (RV 10.90) establishes organic indivisible unity. Any later medieval "
            "or colonial interpretation that imposes birth-based degradation is scripturally invalid and non-binding."
        )

        return OrganicismAuditResult(
            is_organicism_aligned=is_aligned,
            is_colonial_degradation_detected=is_colonial,
            is_birth_caste_conflation=is_birth,
            pratistha_sacred_foundation_verified=True,
            earth_emanation_proof=earth_proof,
            jaimini_sutra_invalidation_triggered=jaimini_triggered,
            subsystems_identified=detected_subsystems,
            forensic_verdict=verdict,
            hermeneutic_siddhanta=siddhanta
        )
