"""
AI ĀCHĀRYA — Propaganda Detector & Satya-Pramāṇa Filter (app/verification/propaganda_detector.py)

Mathematical & Epistemological Deconstruction of Ideological Distortion:
1. Four Bias Vectors: Colonial/Eurocentric, Marxist/Reductionist, Theological/Iconoclastic, Pseudoscience/Anachronistic.
2. Attenuated Logistic Evidence-Distortion Tensor (ALEDT) preventing hyper-attenuation while enforcing a sharp collapse on verified propaganda.
3. Grounded Distortion Proof Tuples requiring counter-Pramāṇa textual citations.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
import math
import re


class DistortionVector(str, Enum):
    COLONIAL_EUROCENTRIC = "Colonial & Eurocentric (Racialized, Macaulayite, Stagnant Orient)"
    MARXIST_REDUCTIONIST = "Marxist & Economic-Reductionist (Monolithic Class Conflict)"
    THEOLOGICAL_ICONOCLASTIC = "Theological & Iconoclastic (Missionary, Pagan Demonization)"
    PSEUDOSCIENCE_ANACHRONISM = "Pseudoscience & Anachronism (Supersonic Jets, Quantum Teleportation in Mantras)"


class ForensicStratumLevel(str, Enum):
    TIER_1_PHYSICAL_EMPIRICAL = "TIER_1_PHYSICAL_EMPIRICAL"
    TIER_2_MATERIAL_CAUSALITY = "TIER_2_MATERIAL_CAUSALITY"
    TIER_3_MANUSCRIPT_PROVENANCE = "TIER_3_MANUSCRIPT_PROVENANCE"
    TIER_4_CANONICAL_ASTRONOMICAL_MATH = "TIER_4_CANONICAL_ASTRONOMICAL_MATH"
    TIER_5_GEOPOLITICAL_REALISM = "TIER_5_GEOPOLITICAL_REALISM"


@dataclass(frozen=True)
class StratifiedTierScore:
    tier: ForensicStratumLevel
    factual_reality: float              # 0.0 to 1.0 (did the physical event or historical person exist?)
    propaganda_distortion: float        # 0.0 to 1.0 (is the claim distorted/sensationalized?)
    causal_attribution_valid: bool      # whether the causal/prophetic link is established
    dimension_name: str
    evidence_justification: str


@dataclass(frozen=True)
class StratifiedForensicReport:
    composite_factual_reality: float    # Physical occurrence reality
    prophetic_causal_reality: float     # Causal predictive reality (veto gated)
    composite_distortion: float         # Propaganda / sensationalism level
    gamma_causal_veto: float            # 0.0 or 1.0
    tier_scores: List[StratifiedTierScore]
    summary_verdict: str
    seeker_guidance: str


@dataclass(frozen=True)
class DistortionProofTuple:
    vector: DistortionVector
    target_clause: str
    identified_fallacy: str
    counter_pramana_source: str
    confidence: float = 0.90


@dataclass
class BiasProfile:
    colonial_vector: float = 0.0       # 0.0 to 1.0
    marxist_vector: float = 0.0        # 0.0 to 1.0
    theological_vector: float = 0.0    # 0.0 to 1.0
    pseudoscience_vector: float = 0.0  # 0.0 to 1.0
    proofs: List[DistortionProofTuple] = field(default_factory=list)

    @property
    def max_distortion(self) -> float:
        """L-infinity norm: maximum singular distortion vector."""
        return max(
            self.colonial_vector,
            self.marxist_vector,
            self.theological_vector,
            self.pseudoscience_vector
        )


class PropagandaDetector:
    """
    Evaluates claims and text passages against the 4 distortion vectors,
    extracting textual distortion proofs and computing the ALEDT Satya score.
    """

    # Lexical and contextual markers for the 4 vectors
    _PATTERNS = {
        DistortionVector.COLONIAL_EUROCENTRIC: [
            r"\baryan\s+(?:invaders?|invasion|race|conquest|subjugation)\b",
            r"\bdravidian\s+(?:aborigines?|primitives?|conquered|subjugated)\b",
            r"\bstagnant\s+oriental\s+despotism\b",
            r"\blacked\s+(?:historical\s+consciousness|critical\s+faculty)\b",
            r"\bborrowed\s+all\s+(?:geometry|astronomy|alphabet)\s+from\s+(?:greeks|mesopotamia|persia)\b",
            r"\bwhite\s+aryan\s+civilizers\b"
        ],
        DistortionVector.MARXIST_REDUCTIONIST: [
            r"\bbrahminical\s+conspiracy\s+(?:to\s+extract\s+surplus|against\s+masses)?\b",
            r"\bfeudal\s+mode\s+of\s+production\s+explaining\s+all\b",
            r"\bspiritual\s+texts\s+merely\s+(?:instruments\s+of\s+class\s+rule|ideological\s+weapons?)\b",
            r"\bnegate\s+(?:chetana|atman|consciousness)\s+as\s+bourgeois\s+illusion\b",
            r"\beconomic\s+surplus\s+extraction\s+as\s+sole\s+basis\b"
        ],
        DistortionVector.THEOLOGICAL_ICONOCLASTIC: [
            r"\bpagan\s+heathen\s+(?:idolatry|superstition)\b",
            r"\bdevil\s+worship\s+and\s+false\s+gods\b",
            r"\bgrotesque\s+polytheism\s+requiring\s+salvation\b",
            r"\bprimitive\s+animism\s+lacking\s+true\s+god\b",
            r"\bfilthy\s+idolatry\s+must\s+be\s+cleansed\b"
        ],
        DistortionVector.PSEUDOSCIENCE_ANACHRONISM: [
            r"\b(?:nuclear\s+missiles?|atomic\s+bombs?|radiation\s+weapons?)\b",
            r"\b(?:supersonic\s+aircraft|spacecraft|interplanetary\s+travel|airplanes?\s+in\s+vedas?)\b",
            r"\bquantum\s+(?:computing|mechanics|entanglement)\s+.*?\b(?:rigveda|vedas?|upanishads?)\b",
            r"\b(?:genetic\s+engineering|test\s+tube\s+babies?)\s+.*?\b(?:mahabharata|kauravas?)\b",
            r"\bvedic\s+(?:airplanes?|spacecraft|nuclear)\b",
            r"\b(?:ancient\s+aliens?|extraterrestrials?\s+(?:built|gods?)|ufos?\s+in\s+temples?|gods\s+(?:were|are)\s+aliens?|cargo\s+cult\s+(?:rishis?|gods?))\b"
        ]
    }

    # Evidence weights for ALEDT
    EVIDENCE_WEIGHTS = {
        "epigraphy": 0.35,
        "textual_criticism": 0.25,
        "archaeology": 0.25,
        "astronomy_science": 0.15
    }

    # Refutation and critical context markers to prevent false positives when scholars debunk myths
    _REFUTATION_MARKERS = [
        r"\b(?:myth|fallacy|dogma|fabrication|illusion|misconception)\s+of\b",
        r"\b(?:refuted|debunked|disproved|disproven|falsified|rejected|discarded|overturned)\b",
        r"\bfalse\s+claim\s+that\b",
        r"\bno\s+evidence\s+for\b",
        r"\bunfounded\s+(?:theory|claim|hypothesis)\b",
        r"\bcritique\s+of\b"
    ]

    # Cross-cultural and commercial apocalyptic hoax index
    _HOAX_PATTERNS = [
        (
            r"\b(?:nostradamus\s+.*?\b(?:hitler|hister)|hister\s+was\s+hitler)\b",
            "Nostradamus Hister Fallacy: 'Hister' refers to the Latin geographical name for the Lower Danube River (Ister), not Adolf Hitler.",
            "Century 2 Quatrain 24 Philological Analysis (Latin Ister)"
        ),
        (
            r"\b(?:twin\s+brothers?\s+.*?\bbirds?\s+of\s+iron|nostradamus\s+.*?\b9\/11|iron\s+birds\s+.*?\btwin\s+towers?)\b",
            "Nostradamus 9/11 Hoax: Quatrain was invented in 1997 by Canadian student Neil Marshall as a demonstration of retroactive confirmation bias.",
            "Neil Marshall (1997) Critical Attribution Hoax Investigation"
        ),
        (
            r"\b(?:mayan\s+calendar\s+.*?\b(?:2012|apocalypse|doomsday))\b",
            "Mayan 2012 Apocalypse Trope: Conflates standard Mesoamerican b'ak'tun calendar cycle turnover with supernatural cataclysm.",
            "Mesoamerican Epigraphic & Anthropological Consensus"
        ),
        (
            r"\b(?:kalki\s+(?:avatar\s+)?(?:has\s+already\s+taken\s+birth|born\s+in\s+\d{4}|reveal(?:ed)?\s+in\s+2032))\b",
            "Commercial Avatāra Date-Setting: Fabricates modern birth dates for Kalki to manufacture apocalyptic urgency. Directly violates Bhāgavata 12.2 timeline.",
            "Śrīmad Bhāgavatam Canto 12 Ch. 2; Sūrya Siddhānta"
        ),
        (
            r"\b(?:vajpayee\s+.*?\b(?:13\s+days?|malika)|malika\s+.*?\b(?:vajpayee|pakistan|gandhi))\b",
            "Modern Bazaar Print Interpolation: Modern political figures are post-1970s print chapbook additions entirely absent from academic palm-leaf archives.",
            "Odisha State Museum & Utkal University Pothi Archives"
        ),
        (
            r"\b(?:ancient\s+aliens?\s+built\s+temples?|kailasa\s+.*?\balien\s+lasers?|shiva\s+lingam\s+.*?\balien\s+rocket|gods\s+were\s+extraterrestrials?)\b",
            "Ancient Astronaut Fallacy: Attributing indigenous Indian monolithic stone architecture to extraterrestrial technology without empirical evidence, denigrating historical Sthapati craftsmanship.",
            "Baroda Copper Plate (812 CE), Mānasāra, Mayamata, Vāstu-vidyā treatises"
        )
    ]

    def detect_bias(self, text: str) -> BiasProfile:
        """
        Analyzes a textual claim and extracts the 4-vector distortion scores
        with explicit proof tuples, distinguishing active propaganda from scholarly refutations.
        """
        t_lower = text.lower()
        profile = BiasProfile()
        proofs: List[DistortionProofTuple] = []

        scores = {v: 0.0 for v in DistortionVector}
        is_refuting = any(re.search(rm, t_lower) for rm in self._REFUTATION_MARKERS)

        # 1. Evaluate four standard distortion vectors
        for vector, regexes in self._PATTERNS.items():
            matches = []
            for rx in regexes:
                found = re.findall(rx, t_lower)
                if found:
                    matches.extend(found)

            if matches:
                if is_refuting:
                    scores[vector] = 0.0
                    proofs.append(
                        DistortionProofTuple(
                            vector=vector,
                            target_clause=matches[0],
                            identified_fallacy="Identified ideological marker cited in critical/refutational context (debunking, not propagating)",
                            counter_pramana_source="Valid Scholarly Refutation"
                        )
                    )
                else:
                    intensity = min(1.0, 0.4 + 0.2 * len(matches))
                    scores[vector] = intensity
                    proofs.append(
                        DistortionProofTuple(
                            vector=vector,
                            target_clause=matches[0],
                            identified_fallacy=f"Matched {len(matches)} active ideological distortion marker(s) for {vector.value}",
                            counter_pramana_source="Primary Epigraphy & Critical Edition Corpus"
                        )
                    )

        # 2. Check cross-cultural and apocalyptic hoax index
        for hoax_rx, fallacy_desc, pramana_src in self._HOAX_PATTERNS:
            hoax_match = re.search(hoax_rx, t_lower)
            if hoax_match:
                if not is_refuting:
                    scores[DistortionVector.PSEUDOSCIENCE_ANACHRONISM] = max(
                        scores[DistortionVector.PSEUDOSCIENCE_ANACHRONISM], 0.85
                    )
                    proofs.append(
                        DistortionProofTuple(
                            vector=DistortionVector.PSEUDOSCIENCE_ANACHRONISM,
                            target_clause=hoax_match.group(0),
                            identified_fallacy=fallacy_desc,
                            counter_pramana_source=pramana_src,
                            confidence=0.98
                        )
                    )

        profile.colonial_vector = scores[DistortionVector.COLONIAL_EUROCENTRIC]
        profile.marxist_vector = scores[DistortionVector.MARXIST_REDUCTIONIST]
        profile.theological_vector = scores[DistortionVector.THEOLOGICAL_ICONOCLASTIC]
        profile.pseudoscience_vector = scores[DistortionVector.PSEUDOSCIENCE_ANACHRONISM]
        profile.proofs = proofs

        return profile

    def compute_aledt_score(
        self,
        evidence_scores: Dict[str, float],
        bias: BiasProfile,
        theta: float = 0.50,
        kappa: float = 8.0
    ) -> Tuple[float, str, Dict[str, any]]:
        """
        Computes the Attenuated Logistic Evidence-Distortion Tensor (ALEDT) score:
        S_Satya = (sum w_i * E_i) / (1 + exp(kappa * [max_distortion - theta]))
        """
        # 1. Base Weighted Evidence
        raw_evidence = sum(
            self.EVIDENCE_WEIGHTS.get(k, 0.0) * float(evidence_scores.get(k, 0.0))
            for k in self.EVIDENCE_WEIGHTS
        )

        # 2. Maximum Distortion (L-infinity norm)
        max_dist = bias.max_distortion

        # 3. Logistic Sigmoid Attenuation Factor
        # When max_dist < theta (0.50), logistic penalty is close to 0, denominator ~ 1.0.
        # When max_dist > 0.70, logistic penalty surges, collapsing S_Satya to zero.
        logistic_arg = kappa * (max_dist - theta)
        # Numerical guard against overflow
        logistic_arg = max(-30.0, min(30.0, logistic_arg))
        distortion_attenuation = 1.0 + math.exp(logistic_arg)

        # Non-distorted base denominator is 1 + exp(kappa * (-theta)) ≈ 1.018
        base_denom = 1.0 + math.exp(-kappa * theta)
        normalized_attenuation = distortion_attenuation / base_denom

        final_satya_score = max(0.0, min(1.0, raw_evidence / normalized_attenuation))

        # Categorization
        if final_satya_score >= 0.70 and max_dist < 0.35:
            verdict = "PRAMĀṆA_SIDDHA (Grounded & Epistemically Established)"
        elif final_satya_score >= 0.40 and max_dist < 0.60:
            verdict = "VICĀRAṆĪYA (Scholarly Debate / Corroboration Needed)"
        elif max_dist >= 0.60:
            verdict = "KŪṬA_YUKTI (Identified Ideological Distortion / Propaganda)"
        else:
            verdict = "APRAMĀṆIKA (Inadequate Evidentiary Corroboration)"

        diagnostics = {
            "raw_evidence_score": round(raw_evidence, 4),
            "max_distortion_vector": round(max_dist, 4),
            "attenuation_factor": round(normalized_attenuation, 4),
            "final_satya_score": round(final_satya_score, 4),
            "proof_count": len(bias.proofs)
        }

        return final_satya_score, verdict, diagnostics

    STRATIFIED_WEIGHTS = {
        ForensicStratumLevel.TIER_1_PHYSICAL_EMPIRICAL: 0.25,
        ForensicStratumLevel.TIER_2_MATERIAL_CAUSALITY: 0.20,
        ForensicStratumLevel.TIER_3_MANUSCRIPT_PROVENANCE: 0.25,
        ForensicStratumLevel.TIER_4_CANONICAL_ASTRONOMICAL_MATH: 0.20,
        ForensicStratumLevel.TIER_5_GEOPOLITICAL_REALISM: 0.10,
    }

    def compute_stratified_forensic_matrix(
        self,
        tiers: List[StratifiedTierScore],
        gamma_causal: Optional[float] = None
    ) -> StratifiedForensicReport:
        """
        Computes 5-tier stratified reality and enforces the non-compensatory
        multiplicative causal veto gate:
        S_PropheticReality = gamma_causal * sum(w_i * FactualScore_i)
        Decouples physical occurrence reality from prophetic fraud.
        """
        if not tiers:
            return StratifiedForensicReport(
                composite_factual_reality=0.0,
                prophetic_causal_reality=0.0,
                composite_distortion=0.0,
                gamma_causal_veto=0.0,
                tier_scores=[],
                summary_verdict="NO_TIERS_EVALUATED",
                seeker_guidance="No claim strata submitted for evaluation."
            )

        # Non-compensatory attribution gate
        if gamma_causal is None:
            attribution_valid = all(t.causal_attribution_valid for t in tiers)
            computed_gamma = 1.0 if attribution_valid else 0.0
        else:
            computed_gamma = max(0.0, min(1.0, float(gamma_causal)))

        total_w = sum(self.STRATIFIED_WEIGHTS.get(t.tier, 0.20) for t in tiers)
        raw_factual = sum(self.STRATIFIED_WEIGHTS.get(t.tier, 0.20) * t.factual_reality for t in tiers) / total_w
        raw_distortion = sum(self.STRATIFIED_WEIGHTS.get(t.tier, 0.20) * t.propaganda_distortion for t in tiers) / total_w

        factual_reality_score = round(raw_factual, 4)
        prophetic_causal_reality = round(computed_gamma * raw_factual, 4)
        distortion_score = round(raw_distortion, 4)

        if computed_gamma == 0.0 and factual_reality_score > 0.40:
            summary = "POST_HOC_RATIONALIZATION_DETACHED_FROM_PROPHECY (Physical events occurred, but ancient prophetic causation is 100% ungrounded)"
        elif prophetic_causal_reality >= 0.70 and distortion_score < 0.30:
            summary = "GROUNDED_EPISTEMIC_HISTORICAL_RECORD"
        elif distortion_score >= 0.60:
            summary = "KŪṬA_YUKTI (Sensationalist Commercial Doomsday Fabrication)"
        else:
            summary = "VICĀRAṆĪYA (Mixed Scholarly and Physical Correlation)"

        guidance = (
            "Seeker Guidance: Discern physical occurrences from supernatural manipulation. "
            "Do not succumb to apocalyptic anxiety or commercial fear-mongering. "
            "Sanātana Dharma upholds Puruṣārtha, Abhaya (fearlessness per Gītā 16.1), and steadfast duty."
        )

        return StratifiedForensicReport(
            composite_factual_reality=factual_reality_score,
            prophetic_causal_reality=prophetic_causal_reality,
            composite_distortion=distortion_score,
            gamma_causal_veto=computed_gamma,
            tier_scores=tiers,
            summary_verdict=summary,
            seeker_guidance=guidance
        )

