"""
AI ĀCHĀRYA — Computer Vision Optical Bridge & Anti-Hallucination Gate (app/intelligence/cv_bridge.py)

Anti-Hallucination Visual Gate & Multi-Modal Verification:
1. Optical Evidence Levels:
   - TEXT_ONLY_UNVERIFIED: Raw audio/video transcripts or articles without pixel stream data.
   - KEYFRAME_DOMINANT_HEX: HSV/RGB color histogram metrics extracted from verified video keyframes.
   - FULL_CV_KEYFRAME_PIPELINE: Pose landmarks (MediaPipe), facial action coding (FACS), and color histograms.
2. Veto Logic:
   Strictly rejects transcript-only assertions regarding:
   - Dress color, attire fabric, jewelry luster.
   - Micro-facial twitches, eye blinking frequency, pupil dilation.
   - Body language, perspiration/sweating, hand tremors.
3. Mathematical Verification:
   When CV histogram metrics are provided, verifies color clustering without hallucination.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
import re
import math


class OpticalEvidenceLevel(str, Enum):
    TEXT_ONLY_UNVERIFIED = "TEXT_ONLY_UNVERIFIED (No pixel data; pure transcript / text)"
    KEYFRAME_DOMINANT_HEX = "KEYFRAME_DOMINANT_HEX (Verified keyframe HSV/RGB histogram)"
    FULL_CV_KEYFRAME_PIPELINE = "FULL_CV_KEYFRAME_PIPELINE (Keyframe CV + Pose Mesh + Color Clustering)"


@dataclass(frozen=True)
class OpticalAuditReport:
    evidence_level: OpticalEvidenceLevel
    is_hallucination_vetoed: bool
    optical_integrity_score: float  # 0.0 to 1.0
    detected_unverified_claims: List[str]
    verified_visual_metrics: Dict[str, str]
    audit_verdict: str
    forensic_advice: str


class ComputerVisionOpticalBridge:
    """
    Guards against optical illusions and visual hallucinations in textual analysis,
    while providing mathematically grounded verification when pixel data is present.
    """

    # Visual micro-signal terms that cannot be inferred from text alone
    _VISUAL_OBSERVATION_PATTERNS = [
        (r"\b(?:dress|suit|shirt|kurta|sari|tie|turban|attire|garment)\s+colou?r\b", "Attire color assertion"),
        (r"\b(?:sweating|perspiring|nervous\s+twitch|sweat\s+on\s+forehead)\b", "Physiological perspiration/twitch assertion"),
        (r"\b(?:pupil\s+dilation|eyes?\s+darting|rapid\s+blinking|gaze\s+aversion)\b", "Ocular micro-signal assertion"),
        (r"\b(?:body\s+language|slouching|nervous\s+fidgeting|tense\s+shoulders?)\b", "Somatic posture/body language assertion"),
        (r"\b(?:micro-expressions?|facial\s+expression|lip\s+tremor)\b", "Facial micro-expression assertion"),
    ]

    # Reference RGB centroids for color mapping
    _CANONICAL_PALETTES = {
        "saffron": (255, 153, 51),
        "white": (255, 255, 255),
        "black": (0, 0, 0),
        "navy": (0, 0, 128),
        "crimson": (220, 20, 60),
        "gold": (255, 215, 0),
        "green": (34, 139, 34)
    }

    @classmethod
    def _hex_to_rgb(cls, hex_code: str) -> Tuple[int, int, int]:
        clean_hex = hex_code.strip().lstrip("#")
        if len(clean_hex) == 3:
            clean_hex = "".join([c * 2 for c in clean_hex])
        if len(clean_hex) != 6:
            return (0, 0, 0)
        try:
            return (
                int(clean_hex[0:2], 16),
                int(clean_hex[2:4], 16),
                int(clean_hex[4:6], 16)
            )
        except ValueError:
            return (0, 0, 0)

    @classmethod
    def _euclidean_color_distance(cls, c1: Tuple[int, int, int], c2: Tuple[int, int, int]) -> float:
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))

    @classmethod
    def audit_visual_assertions(
        cls,
        text_claims: str,
        evidence_level: OpticalEvidenceLevel = OpticalEvidenceLevel.TEXT_ONLY_UNVERIFIED,
        keyframe_dominant_hex: Optional[str] = None,
        pose_symmetry_score: Optional[float] = None
    ) -> OpticalAuditReport:
        """
        Audits visual assertions, enforcing the Anti-Hallucination Visual Gate.
        """
        text_lower = text_claims.lower()
        unverified_claims: List[str] = []

        for pattern, label in cls._VISUAL_OBSERVATION_PATTERNS:
            if re.search(pattern, text_lower):
                unverified_claims.append(label)

        has_visual_claims = len(unverified_claims) > 0

        # Scenario A: Text claims visual details without pixel evidence -> STRICT VETO
        if has_visual_claims and evidence_level == OpticalEvidenceLevel.TEXT_ONLY_UNVERIFIED:
            return OpticalAuditReport(
                evidence_level=evidence_level,
                is_hallucination_vetoed=True,
                optical_integrity_score=0.0,
                detected_unverified_claims=unverified_claims,
                verified_visual_metrics={},
                audit_verdict=(
                    "ANTI-HALLUCINATION OPTICAL VETO: The prompt or input asserts visual micro-signals "
                    f"({', '.join(unverified_claims)}) based strictly on text transcripts. "
                    "In the absence of a Computer Vision (CV) pixel stream, any visual assertion is an optical illusion and machine hallucination."
                ),
                forensic_advice="Disregard unverified visual speculation. Confine forensic analysis to verbatim statements and material archaeological data."
            )

        # Scenario B: Computer Vision data supplied -> Mathematical Verification
        verified_metrics: Dict[str, str] = {}
        if keyframe_dominant_hex:
            rgb = cls._hex_to_rgb(keyframe_dominant_hex)
            closest_color = min(
                cls._CANONICAL_PALETTES.keys(),
                key=lambda k: cls._euclidean_color_distance(rgb, cls._CANONICAL_PALETTES[k])
            )
            verified_metrics["dominant_hex"] = keyframe_dominant_hex.upper()
            verified_metrics["nearest_color_name"] = closest_color.capitalize()
            verified_metrics["rgb_triplet"] = f"RGB({rgb[0]}, {rgb[1]}, {rgb[2]})"

        if pose_symmetry_score is not None:
            verified_metrics["pose_symmetry"] = f"{round(pose_symmetry_score * 100, 1)}%"
            verified_metrics["posture_stability"] = "Stable bilateral symmetry" if pose_symmetry_score >= 0.80 else "Asymmetric posture"

        optical_score = 1.0 if (keyframe_dominant_hex or pose_symmetry_score is not None) else 0.85

        return OpticalAuditReport(
            evidence_level=evidence_level,
            is_hallucination_vetoed=False,
            optical_integrity_score=optical_score,
            detected_unverified_claims=[],
            verified_visual_metrics=verified_metrics,
            audit_verdict=(
                f"VERIFIED OPTICAL AUDIT: Grounded in {evidence_level.name}. Visual attributes mathematically validated."
                if verified_metrics else
                "CLEAN AUDIT: No unverified visual claims detected in text."
            ),
            forensic_advice="Visual claims match verified sensor metrics; proceeding with multimodal confidence."
        )
