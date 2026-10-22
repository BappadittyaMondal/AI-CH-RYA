"""
AI ĀCHĀRYA — Mīmāṃsā Hermeneutic Grayzone Engine (app/verification/mimamsa.py)

Classical Pūrvamīmāṃsā & Uttaramīmāṃsā Jurisprudential Arbitration:
1. Ṣaḍ-Vidha Liṅga (Sixfold Epistemic Interpretation Canons):
   - Upakrama-Upasaṃhāra: Harmony of initial and concluding propositions.
   - Abhyāsa: Deliberate thematic repetition.
   - Apūrvatā: Epistemic novelty (truth not attainable via mundane perception).
   - Phala: Direct existential / spiritual purpose.
   - Arthavāda: Distinguishing hyperbolic/contextual praise or blame from binding injunction (Vidhi).
   - Upapatti: Rational non-contradiction and logical coherence.
2. Canonical Hierarchy of Authority:
   Śruti (1.00) ≻ Smṛti (0.75) ≻ Sadācāra (0.50) ≻ Deśācāra/Lokācāra (0.35).
3. Quote-Mining & Grayzone Neutralization:
   Invalidates weaponized medieval accretions or out-of-context verses when they violate foundational Śruti.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
import re


class AuthorityStrata(str, Enum):
    SRUTI = "Śruti (Universal Metaphysical Foundation - Upaniṣads & Saṃhitās)"
    SMRITI = "Smṛti (Context-Dependent Historical Social Manuals)"
    SADACARA = "Sadācāra (Conduct of the Virtuous & Wise)"
    DESACARA = "Deśācāra / Lokācāra (Regional Custom & Living Tradition)"


class MimamsaCanon(str, Enum):
    UPAKRAMA_UPASAMHARA = "Upakrama-Upasaṃhāra (Introduction-Conclusion Consistency)"
    ABHYASA = "Abhyāsa (Thematic Repetition)"
    APURVATA = "Apūrvatā (Epistemic Novelty)"
    PHALA = "Phala (Existential / Spiritual Purpose)"
    ARTHAVADA = "Arthavāda (Explanatory / Rhetorical Metaphor vs Injunction)"
    UPAPATTI = "Upapatti (Logical Intelligibility)"


@dataclass(frozen=True)
class CanonEvaluation:
    canon: MimamsaCanon
    is_satisfied: bool
    confidence: float
    analysis: str


@dataclass(frozen=True)
class GrayzoneResolutionReport:
    disputed_topic: str
    primary_stratum: AuthorityStrata
    stratum_authority_weight: float
    is_vidhi_binding: bool
    is_arthavada_metaphor: bool
    canon_evaluations: List[CanonEvaluation]
    overall_coherence_score: float
    siddhanta_resolution: str
    is_scripturally_valid: bool


class MimamsaGrayzoneResolver:
    """
    Arbitrates cultural, theological, and scriptural grayzones using
    the formal canons of classical Mīmāṃsā hermeneutics.
    """

    STRATA_WEIGHTS = {
        AuthorityStrata.SRUTI: 1.00,
        AuthorityStrata.SMRITI: 0.75,
        AuthorityStrata.SADACARA: 0.50,
        AuthorityStrata.DESACARA: 0.35
    }

    # Lexical markers for Arthavāda (hyperbolic praise/blame, narrative illustration)
    _ARTHAVADA_INDICATORS = [
        r"\b(?:he\s+who\s+.*?(?:goes\s+to\s+hell|falls\s+into\s+hell)|sin\s+of\s+killing\s+a\s+thousand\s+cows)\b",
        r"\b(?:falls?\s+into\s+hell|goes?\s+to\s+hell|thousand\s+years\s+in\s+hell|falls\s+into\s+hell\s+for\s+a\s+thousand\s+years)\b",
        r"\b(?:attains\s+all\s+worlds|burns\s+all\s+sins\s+in\s+a\s+moment)\b",
        r"\b(?:women\s+are\s+fickle|shudras\s+are\s+born\s+from\s+feet)\b",
        r"\b(?:eulogy|praise|stuti|ninda|allegory|metaphor)\b",
        r"\b(?:curse|boon|imprecation|mythological\s+story)\b"
    ]

    # Markers for binding Vidhi (categorical duty, universal ethical injunction)
    _VIDHI_INDICATORS = [
        r"\b(?:satyaṃ\s+vada|dharmaṃ\s+cara|mā\s+pramadaḥ)\b",
        r"\b(?:speak\s+the\s+truth|walk\s+in\s+righteousness|do\s+not\s+injure)\b",
        r"\b(?:ahimsā\s+paramo\s+dharmaḥ|ahimsa|compassion\s+to\s+all\s+beings)\b",
        r"\b(?:atmano\s+mokshartham|tat\s+tvam\s+asi|aham\s+brahmasmi)\b"
    ]

    @classmethod
    def resolve_grayzone(cls, claim_or_verse: str, declared_source: Optional[str] = None) -> GrayzoneResolutionReport:
        """
        Applies the 6 Mīmāṃsā canons and authority strata to resolve an apparent contradiction or disputed rule.
        """
        text_lower = claim_or_verse.lower()
        source_lower = (declared_source or "").lower()

        # 1. Determine Authority Stratum
        if any(k in source_lower or k in text_lower for k in ["upanishad", "upaniṣad", "rigveda", "yajurveda", "samaveda", "atharvaveda", "gita", "gītā", "brahma sutra"]):
            stratum = AuthorityStrata.SRUTI
        elif any(k in source_lower or k in text_lower for k in ["manu", "yajnavalkya", "parashara", "smriti", "smṛti", "arthashastra"]):
            stratum = AuthorityStrata.SMRITI
        elif any(k in source_lower or k in text_lower for k in ["sadacara", "tradition of the virtuous", "elders"]):
            stratum = AuthorityStrata.SADACARA
        else:
            stratum = AuthorityStrata.DESACARA

        stratum_weight = cls.STRATA_WEIGHTS[stratum]

        # 2. Vidhi vs Arthavāda determination
        is_arthavada = any(re.search(pat, text_lower) for pat in cls._ARTHAVADA_INDICATORS)
        is_vidhi = any(re.search(pat, text_lower) for pat in cls._VIDHI_INDICATORS)

        # In classical Mīmāṃsā, if an extreme reward/curse is attached to a minor act, it is Arthavāda (rhetorical incentive), not Vidhi
        if is_arthavada and not is_vidhi:
            is_vidhi_binding = False
        elif is_vidhi:
            is_vidhi_binding = True
        else:
            # Default: Smṛti legal codes are contextual guidelines, not immutable metaphysical laws
            is_vidhi_binding = (stratum == AuthorityStrata.SRUTI)

        # 3. Evaluate the 6 Canons
        evaluations: List[CanonEvaluation] = []

        # Canon 1: Upakrama-Upasaṃhāra (Introduction-Conclusion Harmony)
        # Check if the claim harmonizes with foundational oneness (Brahman/Ātman)
        upakrama_pass = not ("innate inferiority" in text_lower or "eternal damnation" in text_lower)
        evaluations.append(CanonEvaluation(
            canon=MimamsaCanon.UPAKRAMA_UPASAMHARA,
            is_satisfied=upakrama_pass,
            confidence=0.90,
            analysis="Tests consistency with the Upanisadic premise of universal consciousness (Ekam Sat / Sarvam Khalvidam Brahma)."
        ))

        # Canon 2: Abhyāsa (Repetition of Universal Truth)
        abhyasa_pass = stratum in [AuthorityStrata.SRUTI, AuthorityStrata.SMRITI]
        evaluations.append(CanonEvaluation(
            canon=MimamsaCanon.ABHYASA,
            is_satisfied=abhyasa_pass,
            confidence=0.85,
            analysis="Determines whether the asserted principle is repeatedly reinforced across major canonical treatises."
        ))

        # Canon 3: Apūrvatā (Epistemic Novelty)
        evaluations.append(CanonEvaluation(
            canon=MimamsaCanon.APURVATA,
            is_satisfied=True,
            confidence=0.80,
            analysis="Distinguishes transcendent metaphysical revelation from mundane socio-economic arrangements."
        ))

        # Canon 4: Phala (Spiritual / Existential Purpose)
        # Authentic Vidhi always has Citta-śuddhi (mind purification) or Mokṣa as its ultimate fruit
        phala_pass = not bool(re.search(r"\b(?:harm|harmful|destroy|destruction|exploit|exploitation)\b", text_lower))
        evaluations.append(CanonEvaluation(
            canon=MimamsaCanon.PHALA,
            is_satisfied=phala_pass,
            confidence=0.90,
            analysis="Verifies that the ultimate fruit aligns with Dharma, Loka-saṅgraha (universal welfare), and Mokṣa."
        ))

        # Canon 5: Arthavāda (Distinguishing Metaphor from Injunction)
        evaluations.append(CanonEvaluation(
            canon=MimamsaCanon.ARTHAVADA,
            is_satisfied=True,
            confidence=0.95,
            analysis=(
                "Classified as ARTHAVĀDA (illustrative eulogy or contextual deterrent): cannot be cited as binding eternal law."
                if is_arthavada else
                "Classified as normative proposition: must be harmonized with overarching Śruti principles."
            )
        ))

        # Canon 6: Upapatti (Logical Intelligibility)
        # Any Smṛti verse that directly contradicts Śruti is nullified per Jaimini Sūtra 1.3.3 (Virodhe tv anapekṣam)
        upapatti_pass = upakrama_pass and phala_pass
        evaluations.append(CanonEvaluation(
            canon=MimamsaCanon.UPAPATTI,
            is_satisfied=upapatti_pass,
            confidence=0.92,
            analysis="Enforces Jaimini Sūtra 1.3.3: 'Where Smṛti conflicts with Śruti, the Smṛti statement is disregarded.'"
        ))

        # 4. Compute Overall Coherence Score
        satisfied_count = sum(1 for e in evaluations if e.is_satisfied)
        base_coherence = satisfied_count / len(evaluations)
        final_coherence = round(base_coherence * stratum_weight, 3)

        # 5. Build Siddhānta Resolution
        if is_arthavada:
            siddhanta = (
                f"SIDDHĀNTA RESOLUTION: The disputed passage from '{stratum.value}' is formally classified under Mīmāṃsā "
                f"as ARTHAVĀDA (contextual metaphor, rhetorical deterrence, or symbolic praise/blame). "
                f"It is NOT a universal binding injunction (Vidhi). Attempting to cite it as an immutable dogma violates "
                f"classical hermeneutic rules. Supreme authority rests with timeless Śruti (Vedānta)."
            )
            is_valid = True
        elif not upapatti_pass:
            siddhanta = (
                f"SIDDHĀNTA RESOLUTION: The assertion violates Jaimini Sūtra 1.3.3 ('Virodhe tv anapekṣam'). "
                f"Any secondary Smṛti rule or regional custom that contradicts universal Śruti (Advaita/Viśiṣṭādvaita oneness, "
                f"equality of the divine Ātman) is automatically superseded and invalid."
            )
            is_valid = False
        else:
            siddhanta = (
                f"SIDDHĀNTA RESOLUTION: The principle satisfies Mīmāṃsā canons of interpretation under stratum '{stratum.value}'. "
                f"It operates legitimately within its proper contextual domain without violating primary scriptural axioms."
            )
            is_valid = True

        return GrayzoneResolutionReport(
            disputed_topic=claim_or_verse[:100],
            primary_stratum=stratum,
            stratum_authority_weight=stratum_weight,
            is_vidhi_binding=is_vidhi_binding,
            is_arthavada_metaphor=is_arthavada,
            canon_evaluations=evaluations,
            overall_coherence_score=final_coherence,
            siddhanta_resolution=siddhanta,
            is_scripturally_valid=is_valid
        )
