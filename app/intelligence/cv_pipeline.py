"""
AI ĀCHĀRYA — Multimodal Computer Vision Pipeline & Anti-Optical-Illusion Bridge (app/intelligence/cv_pipeline.py)

Mission:
Provides deep-tech multimodal video processing, distinguishing photon pixel streams from text tokens.
Enforces the Anti-Hallucination Visual Gate (§13, §14):
1. Prohibits inferring visual reality (clothing color, sweating, pupil dilation, eye darting) from audio transcripts.
2. Ingests verified video keyframe metrics (HSV/RGB color clustering, MediaPipe pose symmetry, blink rate).
3. Detects chromatic contradictions (e.g., text asserting 'blue attire' when keyframe HSV is Saffron #FF9933).
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
import math
from app.intelligence.cv_bridge import ComputerVisionOpticalBridge, OpticalEvidenceLevel, OpticalAuditReport


@dataclass(frozen=True)
class CvColorCluster:
    dominant_hex: str
    nearest_canonical_color: str
    hue_degrees: float
    saturation_ratio: float
    luminance_ratio: float
    cluster_pixel_percentage: float


@dataclass(frozen=True)
class CvBiometricMetrics:
    blink_rate_per_min: float
    gaze_stability_ratio: float  # 0.0 to 1.0
    pose_symmetry_index: float   # 0.0 to 1.0
    micro_movement_energy: float # 0.0 to 1.0


@dataclass(frozen=True)
class CvKeyframeAnalysisResult:
    frame_id: str
    timestamp_sec: float
    evidence_level: OpticalEvidenceLevel
    color_cluster: Optional[CvColorCluster]
    biometrics: Optional[CvBiometricMetrics]
    is_hallucination_vetoed: bool
    optical_score: float
    detected_discrepancies: List[str]
    verdict: str
    forensic_advice: str


class CvOpticalPipelineEngine:
    """
    Multimodal video keyframe stream processor and anti-hallucination gate.
    """

    _CANONICAL_COLOR_HUES = {
        "Saffron": (20.0, 45.0),
        "Gold": (46.0, 65.0),
        "Green": (80.0, 160.0),
        "Navy / Blue": (190.0, 250.0),
        "Crimson / Red": (340.0, 15.0),
    }

    @classmethod
    def analyze_hsv_hex(cls, hex_code: str, pixel_percentage: float = 75.0) -> CvColorCluster:
        """
        Converts hex to RGB and calculates HSV hue degrees and saturation.
        """
        rgb = ComputerVisionOpticalBridge._hex_to_rgb(hex_code)
        r_norm, g_norm, b_norm = rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0
        
        c_max = max(r_norm, g_norm, b_norm)
        c_min = min(r_norm, g_norm, b_norm)
        diff = c_max - c_min
        
        # Calculate Hue
        if diff == 0:
            hue = 0.0
        elif c_max == r_norm:
            hue = (60.0 * ((g_norm - b_norm) / diff) + 360.0) % 360.0
        elif c_max == g_norm:
            hue = (60.0 * ((b_norm - r_norm) / diff) + 120.0) % 360.0
        else:
            hue = (60.0 * ((r_norm - g_norm) / diff) + 240.0) % 360.0
            
        sat = 0.0 if c_max == 0 else diff / c_max
        lum = c_max
        
        # Determine nearest canonical color by Euclidean distance in RGB
        canonical_map = ComputerVisionOpticalBridge._CANONICAL_PALETTES
        nearest_color = min(
            canonical_map.keys(),
            key=lambda k: ComputerVisionOpticalBridge._euclidean_color_distance(rgb, canonical_map[k])
        ).capitalize()
        
        return CvColorCluster(
            dominant_hex=hex_code.upper(),
            nearest_canonical_color=nearest_color,
            hue_degrees=round(hue, 1),
            saturation_ratio=round(sat, 2),
            luminance_ratio=round(lum, 2),
            cluster_pixel_percentage=round(pixel_percentage, 1)
        )

    @classmethod
    def audit_multimodal_stream(
        cls,
        text_claims: str,
        frame_id: Optional[str] = None,
        timestamp_sec: float = 0.0,
        raw_keyframe_hex: Optional[str] = None,
        pose_symmetry: Optional[float] = None,
        blink_rate: Optional[float] = None,
        gaze_stability: Optional[float] = None
    ) -> CvKeyframeAnalysisResult:
        """
        Audits combined text claims and Computer Vision sensor telemetry.
        """
        # Step 1: Base text audit via ComputerVisionOpticalBridge
        has_pixel_data = (raw_keyframe_hex is not None) or (pose_symmetry is not None)
        evidence_level = (
            OpticalEvidenceLevel.FULL_CV_KEYFRAME_PIPELINE if (raw_keyframe_hex and pose_symmetry is not None)
            else OpticalEvidenceLevel.KEYFRAME_DOMINANT_HEX if raw_keyframe_hex
            else OpticalEvidenceLevel.TEXT_ONLY_UNVERIFIED
        )

        base_report: OpticalAuditReport = ComputerVisionOpticalBridge.audit_visual_assertions(
            text_claims=text_claims,
            evidence_level=evidence_level,
            keyframe_dominant_hex=raw_keyframe_hex,
            pose_symmetry_score=pose_symmetry
        )

        # If base audit triggered a strict hallucination veto (e.g. visual claim on text-only input)
        if base_report.is_hallucination_vetoed:
            return CvKeyframeAnalysisResult(
                frame_id=frame_id or "NONE",
                timestamp_sec=timestamp_sec,
                evidence_level=evidence_level,
                color_cluster=None,
                biometrics=None,
                is_hallucination_vetoed=True,
                optical_score=0.0,
                detected_discrepancies=base_report.detected_unverified_claims,
                verdict=base_report.audit_verdict,
                forensic_advice=base_report.forensic_advice
            )

        # Step 2: Build color and biometric profiles if pixel telemetry exists
        color_cluster: Optional[CvColorCluster] = None
        if raw_keyframe_hex:
            color_cluster = cls.analyze_hsv_hex(raw_keyframe_hex)

        biometrics: Optional[CvBiometricMetrics] = None
        if pose_symmetry is not None or blink_rate is not None or gaze_stability is not None:
            biometrics = CvBiometricMetrics(
                blink_rate_per_min=blink_rate if blink_rate is not None else 16.0,
                gaze_stability_ratio=gaze_stability if gaze_stability is not None else 0.85,
                pose_symmetry_index=pose_symmetry if pose_symmetry is not None else 0.90,
                micro_movement_energy=0.15
            )

        # Step 3: Check for Chromatic Contradiction between text and pixel measurements
        discrepancies: List[str] = []
        if color_cluster:
            text_lower = text_claims.lower()
            # If text claims blue/navy but pixels show saffron/gold
            if ("blue" in text_lower or "navy" in text_lower) and color_cluster.nearest_canonical_color in ["Saffron", "Gold", "Crimson"]:
                discrepancies.append(f"Chromatic Contradiction: Text asserts blue/navy attire, but keyframe CV HSV confirms {color_cluster.nearest_canonical_color} ({color_cluster.dominant_hex}).")
            # If text claims white but pixels show black/navy
            elif "white" in text_lower and color_cluster.nearest_canonical_color in ["Black", "Navy"]:
                discrepancies.append(f"Chromatic Contradiction: Text asserts white attire, but keyframe CV HSV confirms {color_cluster.nearest_canonical_color} ({color_cluster.dominant_hex}).")

        is_contradiction = len(discrepancies) > 0
        final_score = 0.20 if is_contradiction else base_report.optical_integrity_score
        verdict = (
            f"CHROMATIC CONTRADICTION DETECTED: {'; '.join(discrepancies)}"
            if is_contradiction else
            base_report.audit_verdict
        )

        return CvKeyframeAnalysisResult(
            frame_id=frame_id or "KF-001",
            timestamp_sec=timestamp_sec,
            evidence_level=evidence_level,
            color_cluster=color_cluster,
            biometrics=biometrics,
            is_hallucination_vetoed=is_contradiction,
            optical_score=final_score,
            detected_discrepancies=discrepancies,
            verdict=verdict,
            forensic_advice=(
                "Reject textual claim in favor of verified keyframe HSV sensor readings."
                if is_contradiction else
                base_report.forensic_advice
            )
        )
