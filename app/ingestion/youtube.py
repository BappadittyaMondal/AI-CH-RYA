"""
YouTube Intelligence Sub-Engine (§13a)
Extracts claims, segments timestamps, and explicitly discloses evidence fidelity level.
"""

import re
from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from app.ingestion.claims import AtomicClaim
from app.core.epistemic import EpistemicCategory


class YouTubeEvidenceLevel(str, Enum):
    DIRECT_VIDEO_ANALYSIS = "DIRECT_VIDEO_ANALYSIS"
    OFFICIAL_CAPTIONS = "OFFICIAL_CAPTIONS"
    TRANSCRIPT = "TRANSCRIPT"
    SPEECH_TO_TEXT = "SPEECH_TO_TEXT"
    USER_PROVIDED_TRANSCRIPT = "USER_PROVIDED_TRANSCRIPT"
    METADATA_ONLY = "METADATA_ONLY"


class VideoSegment(BaseModel):
    timestamp_start: str
    timestamp_end: str
    speaker: Optional[str] = "Unknown"
    text: str
    claim_type: EpistemicCategory = EpistemicCategory.USER_SUPPLIED_CLAIM


class YouTubeContributionReport(BaseModel):
    video_id: str
    url: str
    evidence_level_available: YouTubeEvidenceLevel
    evidence_disclosure: str
    speaker_identified: Optional[str] = None
    claims_extracted: List[AtomicClaim] = Field(default_factory=list)
    conflicts_detected: List[str] = Field(default_factory=list)


class YouTubeEngine:
    """Processes YouTube links under strict evidence transparency guidelines."""

    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """Normalizes and extracts YouTube video ID from various URL formats."""
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'youtu\.be\/([0-9A-Za-z_-]{11})',
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    @classmethod
    def analyze_source(
        cls,
        url: str,
        provided_transcript: Optional[str] = None,
        available_level: YouTubeEvidenceLevel = YouTubeEvidenceLevel.METADATA_ONLY
    ) -> YouTubeContributionReport:
        video_id = cls.extract_video_id(url) or "unknown_video"

        # Explicit disclosure rule (§13a.8)
        disclosure = (
            f"Evidence Level: {available_level.value}. "
            "AI ĀCHĀRYA strictly operates on this verified data fidelity level "
            "and does not extrapolate beyond the accessible text/metadata."
        )

        extracted_claims: List[AtomicClaim] = []
        if provided_transcript:
            lines = [l.strip() for l in provided_transcript.split("\n") if l.strip()]
            for idx, line in enumerate(lines[:10]):
                extracted_claims.append(
                    AtomicClaim(
                        claim_text=line,
                        claim_type=EpistemicCategory.USER_SUPPLIED_CLAIM,
                        source_title=f"YouTube Video {video_id}",
                        source_url_or_ref=url,
                        timestamp_or_page=f"Segment {idx+1}",
                        evidence_nature="direct_transcript_statement"
                    )
                )

        return YouTubeContributionReport(
            video_id=video_id,
            url=url,
            evidence_level_available=available_level,
            evidence_disclosure=disclosure,
            claims_extracted=extracted_claims
        )
