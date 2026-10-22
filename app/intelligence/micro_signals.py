"""
AI ĀCHĀRYA — Micro-Signal Forensic Engine (app/intelligence/micro_signals.py)

Advanced Forensic Linguistic & Cognitive Analysis:
1. Passive-Voice Agency Inversion: Detects grammatical deletion or obfuscation of perpetrators in violence, iconoclasm, or coercion.
2. Euphemistic Neutralization & Distortion: Detects sanitizing targeted assault/vandalism into "spontaneous clashes", "land disputes", or "mysterious fires".
3. Asymmetric Epistemic Burden: Detects unequal evidentiary standards demanding absolute physical lithic proof for indigenous claims while accepting colonial/external hearsay.
4. Prejudicial Framing & Weaponized Anachronism: Detects evaluating ancient historical/Bronze Age societies using anachronistic post-industrial ideological categories.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
import re


class MicroSignalCategory(str, Enum):
    AGENCY_INVERSION = "Passive-Voice Agency Inversion"
    EUPHEMISTIC_NEUTRALIZATION = "Euphemistic Neutralization & Sanitization"
    ASYMMETRIC_BURDEN = "Asymmetric Epistemic Burden"
    PREJUDICIAL_ANACHRONISM = "Prejudicial Framing & Weaponized Anachronism"
    COMMERCIAL_FUNNEL_HOOK = "Commercial Funnel Hook (Ed-Tech / Sales Funnel in Educational Discourse)"
    REGIONAL_STATISTICAL_FABRICATION = "Regional Statistical Fabrication & Exceptionalism"
    GEO_ECONOMIC_SUPPLY_CHAIN_BLINDSPOT = "Geo-Economic Supply Chain Blindspot & Strategic Denial"


@dataclass(frozen=True)
class DetectedMicroSignal:
    category: MicroSignalCategory
    matched_phrase: str
    forensic_critique: str
    epistemic_impact: str
    severity_weight: float  # 0.0 to 1.0


@dataclass(frozen=True)
class MicroSignalForensicReport:
    total_signals_detected: int
    composite_manipulation_score: float  # 0.0 to 1.0
    dominant_manipulation_vector: Optional[str]
    detected_signals: List[DetectedMicroSignal]
    rebuttal_strategy: str
    is_compromised: bool


class MicroSignalForensicParser:
    """
    Forensic engine analyzing textual discourse for covert micro-signals,
    semantic laundering, agency obfuscation, and asymmetric framing.
    """

    # 1. Passive-Voice Agency Inversion Patterns
    _AGENCY_INVERSION_PATTERNS = [
        (
            r"\b(?:stones?\s+(?:were|was)\s+pelted|missiles?\s+(?:were|was)\s+hurled)\b",
            "Agentless projectile clause: obscures the organized mob or actor initiating the assault.",
            0.85
        ),
        (
            r"\b(?:clashes?\s+broke\s+out|violence\s+(?:broke\s+out|erupted|ensued))\b",
            "Spontaneous eruption myth: converts unilateral aggression into symmetric mutual conflict.",
            0.80
        ),
        (
            r"\b(?:temple|shrine|structure|monument)\s+(?:collapsed|caught\s+fire|was\s+damaged)\b",
            "Agentless destruction trope: conceals deliberate vandalism or arson under passive natural decay.",
            0.90
        ),
        (
            r"\bshots?\s+(?:were\s+fired|rang\s+out)\b",
            "Actorless gunfire clause: erases shooter identity and motive.",
            0.75
        ),
        (
            r"\b(?:procession|yatra|gathering)\s+led\s+to\s+(?:tension|unrest|violence)\b",
            "Victim-blaming causality: attributes violence to the peaceful assembly rather than the attacking mob.",
            0.85
        )
    ]

    # 2. Euphemistic Neutralization & Laundering Patterns
    _EUPHEMISMS = [
        (
            r"\bland\s+dispute\b",
            "Sanitizes systemic encroachment, illegal land-grab, or Waqf/statutory overreach as mere boundary litigation.",
            0.75
        ),
        (
            r"\bmysterious\s+(?:fire|incident|blaze)\b",
            "Arson laundering: shields incendiary sabotage from criminal inquiry.",
            0.85
        ),
        (
            r"\bdisputed\s+(?:structure|site|place)\b",
            "Epistemic erasure: neutralizes millennia-old archaeological, epigraphic, and liturgical sanctums.",
            0.80
        ),
        (
            r"\bisolated\s+incident\b",
            "Pattern minimization: fragments systematic ideological assaults into disconnected anomalies.",
            0.70
        ),
        (
            r"\blaw\s+and\s+order\s+situation\b",
            "Bureaucratic sanitization: reduces targeted ideological aggression to administrative routine.",
            0.65
        )
    ]

    # 3. Asymmetric Epistemic Burden Patterns
    _ASYMMETRIC_BURDEN_PATTERNS = [
        (
            r"\bno\s+contemporary\s+written\s+records?\b",
            "Weaponized anachronistic literacy demand: demands 2000 BCE alphabetic written books for oral traditions while excusing absence in other Bronze Age cultures.",
            0.80
        ),
        (
            r"\blacks?\s+(?:scientific|historical|peer-reviewed)\s+proof\b",
            "Asymmetric burden of proof: selectively applies hyper-skepticism to indigenous traditions while accepting colonial travelogues without question.",
            0.75
        ),
        (
            r"\bmerely\s+(?:mythological|mythical|legendary|folkloric)\b",
            "Reductionist dismissal: automatically invalidates verified astronomical, epigraphic, and topological Itihāsa records.",
            0.85
        ),
        (
            r"\bunproven\s+indigenous\s+claims?\b",
            "Paternalistic doubt: presumes indigenous memory is invalid until ratified by foreign institutions.",
            0.80
        )
    ]

    # 4. Prejudicial Framing & Weaponized Anachronism Patterns
    _ANACHRONISM_PATTERNS = [
        (
            r"\b(?:patriarchal|oppressive|regressive)\s+bronze\s+age\b",
            "Anachronistic moralizing: evaluates Bronze Age societies through 21st-century ideological frameworks.",
            0.75
        ),
        (
            r"\bbastion\s+of\s+(?:brahmanical|upper-caste)\s+hegemony\b",
            "Marxist ideological reductionism: projects post-colonial class conflict onto ancient civilizational institutions.",
            0.85
        ),
        (
            r"\bfascist\s+(?:hindutva|nationalist)\s+appropriation\b",
            "Political smear weaponization: equates standard national archaeology and heritage conservation with extremism.",
            0.90
        ),
        (
            r"\bprimitive\s+superstition\b",
            "Eurocentric contempt: degrades empirical psychosomatic sciences (Yoga, Prāṇāyāma, Ayurveda) as irrational.",
            0.85
        )
    ]

    # 5. Commercial Funnel Hook Patterns (Sales Pitches disguised as history/science)
    _COMMERCIAL_FUNNEL_PATTERNS = [
        (
            r"\b(?:batch|course|masterclass|registration\s+form|kalam\s+batch|enroll(?:\s+(?:now|today))?|limited\s+seats?|seats?\s+run\s+out|offline\s+batch)\b",
            "Commercial conversion hook: redirects intellectual or historical inquiry into customer acquisition for commercial batches.",
            0.80
        ),
        (
            r"\b(?:iat\s+prep|nest\s+prep|iiser\s+aptitude|target\s+rank\s+one|exam\s+prep(?:aration)?)\b",
            "Coaching funnel alignment: monetizes aspirational student anxiety under the guise of civilizational science analysis.",
            0.75
        ),
        (
            r"\b(?:links?\s+(?:all\s+of\s+them\s+)?(?:are\s+)?given\s+in\s+the\s+description|link\s+in\s+bio|click\s+(?:the\s+)?link|subscribe\s+to\s+our\s+channel)\b",
            "Algorithmic call-to-action (CTA): prioritizes creator monetization and audience capture over neutral historical scholarship.",
            0.60
        )
    ]

    # 6. Regional Statistical Fabrication Patterns
    _REGIONAL_FABRICATION_PATTERNS = [
        (
            r"\b(?:9\s+out\s+of\s+10|90%\s+of\s+scientists?|every\s+9\s+out\s+of\s+10)\b",
            "Hyperbolic demographic fabrication: manufactures extreme statistical claims without empirical census or institutional citation.",
            0.90
        ),
        (
            r"\b(?:cheat\s+code\s+for\s+all\s+geniuses|unreasonable\s+number\s+of\s+(?:scientific\s+)?legends)\b",
            "Regional chauvinism trope: exoticizes a geographic subculture while marginalizing pan-Indian polycentric contributions.",
            0.75
        ),
        (
            r"\b(?:sole\s+intellectual\s+hub|only\s+place\s+in\s+india\s+that\s+produced)\b",
            "Monopolistic intellectual erasure: erases the scientific achievements of other Indian linguistic and geographic traditions.",
            0.85
        )
    ]

    # 7. Geo-Economic Supply Chain Blindspot Patterns
    _GEO_ECONOMIC_PATTERNS = [
        (
            r"\b(?:quell\s+and\s+subdue\s+china|contain\s+china\s+for\s+dharmic\s+reasons)\b",
            "Strategic rhetoric escalation: substitutes martial or spiritual hyperbole for hard supply-chain and military-industrial deterrence.",
            0.80
        ),
        (
            r"\b(?:adopt\s+the\s+elon\s+musk\s+model|white\s+colonizing\s+mindset\s+which\s+chooses\s+to\s+use\s+every\s+planet)\b",
            "Polemical scapegoating: conflates private space-launch engineering with imperialist ecocide without assessing space-defense parity.",
            0.75
        ),
        (
            r"\b(?:critical\s+mineral(?:\s+shortages?|\s+exports?)?|rare-?earth|semiconductor\s+supply\s+chains?|shipping\s+lane(?:\s+port)?\s+blockades?)\b",
            "Geo-economic supply-chain vulnerability: flags dependencies in raw materials, rare-earths, fabrication, or maritime chokepoints.",
            0.85
        ),
        (
            r"\bgreen\s+innovation\s+significantly\b",
            "Supply-chain omission: calls for rapid green transition while ignoring 80%+ critical mineral and solar processing dependency on adversaries.",
            0.65
        )
    ]

    @classmethod
    def analyze_text(cls, text: str) -> MicroSignalForensicReport:
        """
        Executes exhaustive multi-vector micro-signal analysis on raw text.
        """
        if not text or not text.strip():
            return MicroSignalForensicReport(
                total_signals_detected=0,
                composite_manipulation_score=0.0,
                dominant_manipulation_vector=None,
                detected_signals=[],
                rebuttal_strategy="No text provided for analysis.",
                is_compromised=False
            )

        text_lower = text.lower()
        signals: List[DetectedMicroSignal] = []
        category_weights: Dict[MicroSignalCategory, float] = {
            MicroSignalCategory.AGENCY_INVERSION: 0.0,
            MicroSignalCategory.EUPHEMISTIC_NEUTRALIZATION: 0.0,
            MicroSignalCategory.ASYMMETRIC_BURDEN: 0.0,
            MicroSignalCategory.PREJUDICIAL_ANACHRONISM: 0.0,
            MicroSignalCategory.COMMERCIAL_FUNNEL_HOOK: 0.0,
            MicroSignalCategory.REGIONAL_STATISTICAL_FABRICATION: 0.0,
            MicroSignalCategory.GEO_ECONOMIC_SUPPLY_CHAIN_BLINDSPOT: 0.0
        }

        # 1. Check Agency Inversion
        for pattern, critique, weight in cls._AGENCY_INVERSION_PATTERNS:
            match = re.search(pattern, text_lower)
            if match:
                sig = DetectedMicroSignal(
                    category=MicroSignalCategory.AGENCY_INVERSION,
                    matched_phrase=match.group(0),
                    forensic_critique=critique,
                    epistemic_impact="Obscures initiator agency and manufactures false symmetry between aggressor and victim.",
                    severity_weight=weight
                )
                signals.append(sig)
                category_weights[MicroSignalCategory.AGENCY_INVERSION] += weight

        # 2. Check Euphemisms
        for pattern, critique, weight in cls._EUPHEMISMS:
            match = re.search(pattern, text_lower)
            if match:
                sig = DetectedMicroSignal(
                    category=MicroSignalCategory.EUPHEMISTIC_NEUTRALIZATION,
                    matched_phrase=match.group(0),
                    forensic_critique=critique,
                    epistemic_impact="Sanitizes deliberate hostility and minimizes legal/forensic liability.",
                    severity_weight=weight
                )
                signals.append(sig)
                category_weights[MicroSignalCategory.EUPHEMISTIC_NEUTRALIZATION] += weight

        # 3. Check Asymmetric Burden
        for pattern, critique, weight in cls._ASYMMETRIC_BURDEN_PATTERNS:
            match = re.search(pattern, text_lower)
            if match:
                sig = DetectedMicroSignal(
                    category=MicroSignalCategory.ASYMMETRIC_BURDEN,
                    matched_phrase=match.group(0),
                    forensic_critique=critique,
                    epistemic_impact="Imposes an impossible evidential threshold to invalidate native civilizational memory.",
                    severity_weight=weight
                )
                signals.append(sig)
                category_weights[MicroSignalCategory.ASYMMETRIC_BURDEN] += weight

        # 4. Check Anachronism
        for pattern, critique, weight in cls._ANACHRONISM_PATTERNS:
            match = re.search(pattern, text_lower)
            if match:
                sig = DetectedMicroSignal(
                    category=MicroSignalCategory.PREJUDICIAL_ANACHRONISM,
                    matched_phrase=match.group(0),
                    forensic_critique=critique,
                    epistemic_impact="Applies post-industrial ideological categories to discredit ancient civilizational systems.",
                    severity_weight=weight
                )
                signals.append(sig)
                category_weights[MicroSignalCategory.PREJUDICIAL_ANACHRONISM] += weight

        # 5. Check Commercial Funnel Hooks
        for pattern, critique, weight in cls._COMMERCIAL_FUNNEL_PATTERNS:
            match = re.search(pattern, text_lower)
            if match:
                sig = DetectedMicroSignal(
                    category=MicroSignalCategory.COMMERCIAL_FUNNEL_HOOK,
                    matched_phrase=match.group(0),
                    forensic_critique=critique,
                    epistemic_impact="Leverages patriotic or intellectual content to monetize user attention into commercial sales channels.",
                    severity_weight=weight
                )
                signals.append(sig)
                category_weights[MicroSignalCategory.COMMERCIAL_FUNNEL_HOOK] += weight

        # 6. Check Regional Statistical Fabrications
        for pattern, critique, weight in cls._REGIONAL_FABRICATION_PATTERNS:
            match = re.search(pattern, text_lower)
            if match:
                sig = DetectedMicroSignal(
                    category=MicroSignalCategory.REGIONAL_STATISTICAL_FABRICATION,
                    matched_phrase=match.group(0),
                    forensic_critique=critique,
                    epistemic_impact="Fabricates exaggerated demographic or scientific claims without empirical institutional backing.",
                    severity_weight=weight
                )
                signals.append(sig)
                category_weights[MicroSignalCategory.REGIONAL_STATISTICAL_FABRICATION] += weight

        # 7. Check Geo-Economic Supply Chain Blindspots
        for pattern, critique, weight in cls._GEO_ECONOMIC_PATTERNS:
            match = re.search(pattern, text_lower)
            if match:
                sig = DetectedMicroSignal(
                    category=MicroSignalCategory.GEO_ECONOMIC_SUPPLY_CHAIN_BLINDSPOT,
                    matched_phrase=match.group(0),
                    forensic_critique=critique,
                    epistemic_impact="Evades physical metallurgical, supply-chain, or defense-industrial realities in strategic discourse.",
                    severity_weight=weight
                )
                signals.append(sig)
                category_weights[MicroSignalCategory.GEO_ECONOMIC_SUPPLY_CHAIN_BLINDSPOT] += weight

        total_detected = len(signals)
        if total_detected == 0:
            return MicroSignalForensicReport(
                total_signals_detected=0,
                composite_manipulation_score=0.0,
                dominant_manipulation_vector=None,
                detected_signals=[],
                rebuttal_strategy="Text exhibits neutral lexical construction; no significant covert micro-signals detected.",
                is_compromised=False
            )

        # Non-linear composite score calculation with asymptotic saturation
        raw_sum = sum(s.severity_weight for s in signals)
        composite_score = round(min(1.0, 1.0 - (1.0 / (1.0 + 0.45 * raw_sum))), 3)

        # Dominant category
        dominant_cat = max(category_weights, key=lambda k: category_weights[k])
        dominant_name = dominant_cat.value if category_weights[dominant_cat] > 0 else None

        # Build forensic rebuttal strategy
        strategy_lines = [
            f"FORENSIC DECONSTRUCTION (Manipulation Score: {int(composite_score * 100)}%):",
            f"1. Dominant Vector: {dominant_name}.",
            "2. Counter-Strategy: Re-insert deleted agents explicitly; reject euphemistic sanitization; expose asymmetric evidentiary demands."
        ]
        rebuttal_strategy = "\n".join(strategy_lines)

        return MicroSignalForensicReport(
            total_signals_detected=total_detected,
            composite_manipulation_score=composite_score,
            dominant_manipulation_vector=dominant_name,
            detected_signals=signals,
            rebuttal_strategy=rebuttal_strategy,
            is_compromised=(composite_score >= 0.50)
        )
