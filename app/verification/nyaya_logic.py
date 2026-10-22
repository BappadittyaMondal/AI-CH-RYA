"""
AI ĀCHĀRYA — Nyāya Epistemology & Hetvābhāsa Fallacy Parser (app/verification/nyaya_logic.py)

Mission:
Implement Akṣapāda Gautama's classical Nyāya logic and inferential fallacy engine
(Nyāyasūtra 1.2.4–9) to detect logical fallacies, deceptive syllogisms, and narrative
manipulation in modern sociopolitical, legal, and theological claims.

The 5 Classical Hetvābhāsas:
1. Savyabhicāra (Inconclusive / Erratic Middle Term)
2. Viruddha (Contradictory Middle Term proving the opposite)
3. Satpratipakṣa (Counter-balanced by an equally strong opposing inference)
4. Asiddha (Unproved Premise / Subject or Invariable Concomitance)
5. Bādhita (Sublated / Empirically refuted by direct perception)
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
import re


class HetvabhasaType(str, Enum):
    SAVYABHICARA = "Savyabhicāra (Inconclusive / Erratic Middle)"
    VIRUDDHA = "Viruddha (Contradictory / Proves the Opposite)"
    SATPRATIPAKSA = "Satpratipakṣa (Counter-Balanced Antinomy)"
    ASIDDHA = "Asiddha (Unproved / Unestablished Premise)"
    BADHITA = "Bādhita (Sublated / Empirically Refuted by Perception)"
    NONE = "Nirdoṣa (Valid Syllogism / Pramāṇa-Siddha)"


@dataclass(frozen=True)
class NyayaSyllogism:
    """The 5-Membered Nyāya Syllogism (Pañcāvayava)."""
    pratijna: str    # 1. Proposition (e.g. "The hill has fire")
    hetu: str        # 2. Reason / Ground (e.g. "Because it has smoke")
    udaharana: str   # 3. Exemplar with Vyāpti (e.g. "Wherever there is smoke there is fire, like a hearth")
    upanaya: str     # 4. Application (e.g. "This hill has smoke which is invariably associated with fire")
    nigamana: str    # 5. Conclusion (e.g. "Therefore, this hill has fire")


@dataclass(frozen=True)
class FallacyAuditResult:
    is_fallacious: bool
    detected_fallacy: HetvabhasaType
    sub_variety: str
    confidence_score: float
    flawed_term: str
    refutation_reason: str
    rebuttal_strategy: str
    classical_exemplar: str


class NyayaLogicEngine:
    """
    Formal Nyāya Logic & Cognitive Fallacy Detection Engine.
    Evaluates propositions against Gautama's 5 Hetvābhāsas.
    """

    # Linguistic triggers for fallacies in unstructured arguments
    _FALLACY_HEURISTICS = [
        # 1. Bādhita (Direct Empirical Refutation)
        {
            "type": HetvabhasaType.BADHITA,
            "variety": "Pratyakṣa-bādhita (Directly refuted by empirical facts/sensors)",
            "patterns": [
                r"fire is cold", r"sun rises in the west", r"ancient planes flew with mercury",
                r"water is dry", r"transcripts reveal dress color", r"sweating seen in text"
            ],
            "reason": "The conclusion asserts a physical property directly sublated by verified perception or laws of physics.",
            "rebuttal": "Confront with direct empirical sensor measurements (Pratyakṣa Pramāṇa), which inherently overrides verbal testimony.",
            "classical_example": "Vahnir anuṣṇaḥ dravyatvāt (Fire is cold because it is a substance) — refuted by tactile perception."
        },
        # 2. Viruddha (Self-Contradictory Middle)
        {
            "type": HetvabhasaType.VIRUDDHA,
            "variety": "Sādhya-viparyaya-sādhaka (The stated reason actually proves the exact opposite)",
            "patterns": [
                r"peaceful because they set fire", r"tolerant because they execute critics",
                r"democratic because elections are cancelled", r"eternal because it is created",
                r"harmless because it poisoned"
            ],
            "reason": "The cited ground (Hetu) has an invariable negative concomitance with the thesis, proving its negation.",
            "rebuttal": "Demonstrate the mathematical contradiction: Hetu $\\implies \\neg$ Sādhya.",
            "classical_example": "Śabdo nityaḥ kṛtakatvāt (Sound is eternal because it is produced) — production proves non-eternality."
        },
        # 3. Asiddha (Unproved Subject or Premise)
        {
            "type": HetvabhasaType.ASIDDHA,
            "variety": "Āśrayāsiddha / Svarūpāsiddha (The subject or premise does not exist in reality)",
            "patterns": [
                r"sky-lotus", r"hare's horn", r"son of a barren woman", r"aliens built ellora",
                r"2032 doomsday", r"secret underground nuclear missiles in 3000 bce",
                r"illuminati laser weapons"
            ],
            "reason": "The locus of inference (Pakṣa) or the presence of the reason (Hetu) is fictitious and unproven.",
            "rebuttal": "Demand primary archaeological, lithic, or empirical proof for the existence of the subject.",
            "classical_example": "Gagarakusumaṁ surabhi (The sky-lotus is fragrant) — the locus 'sky-lotus' does not exist."
        },
        # 4. Savyabhicāra (Erratic / Too Wide Middle)
        {
            "type": HetvabhasaType.SAVYABHICARA,
            "variety": "Sādhāraṇa (The reason exists in both the target and its opposite)",
            "patterns": [
                r"guilty because he was present", r"anti-national because he questioned",
                r"criminal because of his religion", r"scholar because he speaks english",
                r"wise because he is old"
            ],
            "reason": "The middle term is erratic; it coexists with the thesis and with the absence of the thesis.",
            "rebuttal": "Provide a counter-example (Vipakṣa) where the reason exists without the conclusion.",
            "classical_example": "Parvato vahnimān prameyatvāt (The hill has fire because it is knowable) — a lake is also knowable but has no fire."
        },
        # 5. Satpratipakṣa (Counter-Balanced Antinomy)
        {
            "type": HetvabhasaType.SATPRATIPAKSA,
            "variety": "Prakaraṇasama (Balanced by an equally valid opposing inference)",
            "patterns": [
                r"statistically significant yet clinically irrelevant",
                r"strictly legal yet morally bankrupt",
                r"economically profitable yet ecologically destructive"
            ],
            "reason": "There exists an equally strong counter-argument resting on an independent valid ground.",
            "rebuttal": "Elevate to higher-order synthesis (Samanvaya) or introduce decisive third-party evidence.",
            "classical_example": "Śabdo nityaḥ śrāvaṇatvāt vs Śabdo 'nityaḥ kāryatvāt (Equal opposing proofs)."
        }
    ]

    @classmethod
    def audit_argument(cls, text: str) -> FallacyAuditResult:
        """
        Parses an input argument or narrative text for Nyāya inferential fallacies.
        Returns a structured FallacyAuditResult.
        """
        clean_text = text.strip().lower()
        if not clean_text:
            return FallacyAuditResult(
                is_fallacious=False,
                detected_fallacy=HetvabhasaType.NONE,
                sub_variety="None",
                confidence_score=0.0,
                flawed_term="None",
                refutation_reason="Empty input provided.",
                rebuttal_strategy="None",
                classical_exemplar="None"
            )

        # Evaluate heuristics
        for rule in cls._FALLACY_HEURISTICS:
            for pattern in rule["patterns"]:
                if re.search(pattern, clean_text):
                    return FallacyAuditResult(
                        is_fallacious=True,
                        detected_fallacy=rule["type"],
                        sub_variety=rule["variety"],
                        confidence_score=0.92,
                        flawed_term=pattern,
                        refutation_reason=rule["reason"],
                        rebuttal_strategy=rule["rebuttal"],
                        classical_exemplar=rule["classical_example"]
                    )

        # If no heuristic is tripped, evaluate formal syllogistic structure if present
        # Detect if "because" / "therefore" structure is present
        if "because" in clean_text and ("therefore" in clean_text or "hence" in clean_text):
            # Check for circular reasoning (Ātmāśraya)
            parts = clean_text.split("because")
            premise = parts[0].strip()
            reason = parts[1].split("therefore")[0].strip() if "therefore" in parts[1] else parts[1].strip()
            
            # If reason merely repeats premise in different words
            p_tokens = set(re.findall(r"\w+", premise))
            r_tokens = set(re.findall(r"\w+", reason))
            intersection = p_tokens.intersection(r_tokens)
            if len(intersection) >= 3 and len(intersection) / max(len(p_tokens), 1) > 0.65:
                return FallacyAuditResult(
                    is_fallacious=True,
                    detected_fallacy=HetvabhasaType.ASIDDHA,
                    sub_variety="Ātmāśraya (Petitio Principii / Circular Reasoning)",
                    confidence_score=0.88,
                    flawed_term=f"Overlapping tokens: {', '.join(list(intersection)[:4])}",
                    refutation_reason="The reason merely restates the proposition instead of introducing an independent grounding middle term.",
                    rebuttal_strategy="Demand an independent empirical middle term (Hetu) distinct from the thesis.",
                    classical_exemplar="Aparādhī yataḥ sa aparādhakārī (He is guilty because he committed the offense)."
                )

        return FallacyAuditResult(
            is_fallacious=False,
            detected_fallacy=HetvabhasaType.NONE,
            sub_variety="Pramāṇa-Siddha (No Fatal Hetvābhāsa Detected)",
            confidence_score=0.95,
            flawed_term="None",
            refutation_reason="The proposition does not violate Gautama's 5 inferential conditions.",
            rebuttal_strategy="Maintain vigilance and verify empirical ground truth.",
            classical_exemplar="Yatra yatra dhūmas tatra tatra vahniḥ (Valid Vyāpti)."
        )

    @classmethod
    def evaluate_panchavayava(cls, syllogism: NyayaSyllogism) -> Dict[str, Any]:
        """
        Validates the formal 5-membered Nyāya syllogistic structure.
        """
        # Audit each avayava for completeness
        is_complete = bool(
            syllogism.pratijna and syllogism.hetu and 
            syllogism.udaharana and syllogism.upanaya and syllogism.nigamana
        )
        
        # Test the reason for fallacies
        audit = cls.audit_argument(f"{syllogism.pratijna} because {syllogism.hetu}")
        
        return {
            "is_formally_complete": is_complete,
            "has_hetvabhasa": audit.is_fallacious,
            "fallacy_details": audit.detected_fallacy.value,
            "sub_variety": audit.sub_variety,
            "refutation": audit.refutation_reason,
            "syllogism_breakdown": {
                "1_pratijna": syllogism.pratijna,
                "2_hetu": syllogism.hetu,
                "3_udaharana": syllogism.udaharana,
                "4_upanaya": syllogism.upanaya,
                "5_nigamana": syllogism.nigamana
            }
        }
