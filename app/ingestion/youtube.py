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


import hashlib


class ASRPhoneticNormalizer:
    """Normalizes phonetic drift and ASR speech-to-text distortions for Indic and classical terms."""
    _REPLACEMENTS = [
        (r"\bpanch\s*sakha\b", "Pañcasakhā"),
        (r"\bachutanand\b", "Achyutānanda"),
        (r"\bachyutanand\b", "Achyutānanda"),
        (r"\bneelam\s*chakra\b", "Nīlacakra"),
        (r"\bneelachakra\b", "Nīlacakra"),
        (r"\bmadala\s*panji\b", "Mādaḷā Pāñji"),
        (r"\byug\s*sandhi\b", "Yuga Sandhi"),
        (r"\byugsanthi\b", "Yuga Sandhi"),
        (r"\bsuryasidhanta\b", "Sūrya Siddhānta"),
        (r"\bsurya\s*sidhant\b", "Sūrya Siddhānta"),
        (r"\bhister\b", "Hister (Danube)"),
        (r"\bbhavishya\s*malika\b", "Bhavishya Mālikā"),
    ]

    @classmethod
    def normalize_text(cls, raw_text: str) -> str:
        text = raw_text
        for pattern, replacement in cls._REPLACEMENTS:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        return text


class YouTubeEngine:
    """Processes YouTube links under strict evidence transparency guidelines."""

    _CACHE: Dict[str, YouTubeContributionReport] = {}

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
        cache_key = hashlib.sha256(url.encode()).hexdigest()
        if not provided_transcript and cache_key in cls._CACHE:
            return cls._CACHE[cache_key]

        video_id = cls.extract_video_id(url) or "unknown_video"

        # Explicit disclosure rule (§13a.8)
        disclosure = (
            f"Evidence Level: {available_level.value}. "
            "AI ĀCHĀRYA strictly operates on this verified data fidelity level "
            "and does not extrapolate beyond the accessible text/metadata."
        )

        extracted_claims: List[AtomicClaim] = []
        if provided_transcript:
            normalized_txt = ASRPhoneticNormalizer.normalize_text(provided_transcript)
            lines = [l.strip() for l in normalized_txt.split("\n") if l.strip()]
            for idx, line in enumerate(lines[:15]):
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

        report = YouTubeContributionReport(
            video_id=video_id,
            url=url,
            evidence_level_available=available_level,
            evidence_disclosure=disclosure,
            claims_extracted=extracted_claims
        )
        cls._CACHE[cache_key] = report
        return report
