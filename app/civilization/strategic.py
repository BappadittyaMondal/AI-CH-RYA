"""
AI ĀCHĀRYA — Kauṭilyan Realpolitik & Strategic Statecraft Engine (app/civilization/strategic.py)

Integrates classical Indian statecraft (Arthaśāstra, Maṇḍala Theory, Ṣāḍguṇya, Daṇḍanīti)
with modern strategic doctrines (Two-front deterrence, Quad, Nuclear NFU, Strategic Autonomy)
to systematically evaluate and debunk fantastical apocalyptic geopolitical scenarios.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Any
import re


class MandalaRole(str, Enum):
    VIJIGISU = "VIJIGISU (Sovereign central state pursuing security & Dharma)"
    ARI = "ARI (Immediate contiguous rival / competitor)"
    MITRA = "MITRA (Natural ally balancing the contiguous rival)"
    ARI_MITRA = "ARI_MITRA (Ally of the rival power)"
    MADHYAMA = "MADHYAMA (Intermediate regional balancer)"
    UDASINA = "UDASINA (Detached neutral superpower)"


class SadgunyaMethod(str, Enum):
    SANDHI = "SANDHI (Diplomatic peace / strategic economic accord)"
    VIGRAHA = "VIGRAHA (Active defense / armed hostility)"
    ASANA = "ASANA (Strategic patience / entrenched posture)"
    YANA = "YANA (Force projection / military mobilization)"
    SAMSRAYA = "SAMSRAYA (Strategic partnership / multilateral balancing)"
    DVAIDHIBHAVA = "DVAIDHIBHAVA (Dual policy: peace with one, deterrence against other)"


@dataclass(frozen=True)
class GeopoliticalPlausibilityResult:
    claim_text: str
    plausibility_score: float         # 0.0 to 1.0
    status: str                       # PLAUSIBLE, UNREALISTIC, MYTHOLOGICAL_FANTASY
    kautilyan_critique: str
    modern_orbat_reality: str
    structural_contradictions: List[str] = field(default_factory=list)


class StrategicRealpolitikEngine:
    """
    Evaluates claims of wars, alliances, and geopolitical doom through
    Arthaśāstric realism and modern international relations theory.
    """

    _ABSURD_ALLIANCE_PATTERNS = [
        (
            r"\b(?:us|united\s+states|america)\s+.*?\b(?:ally|allies|joint|coalition|join|alongside)\s+.*?\b(?:china|pakistan)\s+.*?\b(?:invad|attack|destroy)\s+india\b",
            "Structural Indo-Pacific Contradiction: US strategy relies on India as a democratic counterweight to Chinese hegemony (Quad, INDUS-X, iCET). A US-China-Pak invasion coalition violates fundamental balance-of-power realpolitik."
        ),
        (
            r"\b13\s+islamic\s+nations?\s+.*?\b(?:invad|attack|destroy)\s+india\b",
            "Monolithic Islamic Bloc Fallacy: Ignores acute intra-regional divisions (Sunni-Shia divide, Abraham Accords) and deep strategic partnerships (India-UAE CEPA, Saudi Vision 2030, India-Middle East Corridor)."
        ),
        (
            r"\brussia\s+.*?\bconvert(?:s|ed|ing)?\s+to\s+hinduism\b",
            "Sovereign Identity Projection: Russia's strategic culture is rooted in Slavic Eurasian identity and Russian Orthodoxy; assuming an entire foreign nuclear superpower converts to Sanātana Dharma is mythological wish-fulfillment, not statecraft."
        ),
        (
            r"\b(?:ww3|world\s+war\s+(?:3|three))\s+.*?\b(?:2025|2026|2027|2028|2029|2030|2031|2032).*?\b(?:destroy|invad|defeat)\s+india\b",
            "Apocalyptic Deterrence Erasure: Ignores India's Credible Minimum Deterrence nuclear triad, second-strike capability, and fortified Himalayan defensive lines under HQ Integrated Defence Staff (IDS)."
        )
    ]

    def evaluate_claim(self, text: str) -> GeopoliticalPlausibilityResult:
        t_lower = text.lower()
        contradictions: List[str] = []

        for pattern, critique in self._ABSURD_ALLIANCE_PATTERNS:
            if re.search(pattern, t_lower):
                contradictions.append(critique)

        # Baseline plausibility calculation
        if len(contradictions) >= 2:
            score = 0.05
            status = "MYTHOLOGICAL_FANTASY (Completely disconnected from realpolitik and statecraft)"
        elif len(contradictions) == 1:
            score = 0.20
            status = "UNREALISTIC_SCENARIO (Violates structural balance-of-power principles)"
        else:
            # Check if text discusses standard grounded two-front security
            two_front = any(k in t_lower for k in ["two-front", "lac", "loc", "china-pakistan economic corridor", "cpec"])
            if two_front:
                score = 0.85
                status = "GROUNDED_STRATEGIC_REALITY (Standard defense planning parameter)"
            else:
                score = 0.50
                status = "GENERAL_GEOPOLITICAL_STATEMENT"

        kautilya_note = (
            "Kauṭilyan Arthaśāstra Assessment: Statecraft operates strictly on Svatva (sovereignty), "
            "Puruṣārtha (human agency), and Daṇḍanīti (military deterrence). States act according to "
            "national self-interest (Svārtha), never by fulfilling foreign mystical prophecies or acting against "
            "their own survival imperatives."
        )

        modern_orbat = (
            "Modern Strategic Reality: India balances regional security through credible nuclear deterrence (NFU), "
            "the Quad maritime partnership, multi-alignment diplomacy, and self-reliant defense manufacturing (Aatmanirbharta). "
            "Apocalyptic doomsday scenarios ignore actual strategic orders of battle (ORBAT)."
        )

        return GeopoliticalPlausibilityResult(
            claim_text=text,
            plausibility_score=score,
            status=status,
            kautilyan_critique=kautilya_note,
            modern_orbat_reality=modern_orbat,
            structural_contradictions=contradictions
        )
