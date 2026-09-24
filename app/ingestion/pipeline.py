"""
Self-Learning Ingestion Pipeline (§13)
Governs continuous discovery and ingestion of candidate knowledge.
Enforces the rule: Never silently change previously verified (State A) knowledge based on one new source.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from app.core.knowledge_states import KnowledgeState, KnowledgeItem
from app.ingestion.claims import AtomicClaim, ClaimVerificationStatus
from app.ingestion.web import WebEngine
from app.ingestion.youtube import YouTubeEngine, YouTubeEvidenceLevel
from app.ingestion.contradiction import ContradictionReport


class IngestionBatchReport(BaseModel):
    batch_id: str
    source_type: str  # web, youtube, pdf, user_text
    source_url_or_title: str
    extracted_claims: List[AtomicClaim] = Field(default_factory=list)
    state_assigned: KnowledgeState = KnowledgeState.D_SESSION_ONLY
    contradiction_reports: List[ContradictionReport] = Field(default_factory=list)
    governance_approved: bool = False
    notes: str


class IngestionPipeline:
    """End-to-end ingestion pipeline with strict security, classification, and candidate gating."""

    @classmethod
    def ingest_web(cls, url: str, content: str) -> IngestionBatchReport:
        sanitize_report = WebEngine.sanitize_and_screen(url, content)
        claims = sanitize_report.claims

        # External content is Session Only (State D) until processed for candidate promotion
        return IngestionBatchReport(
            batch_id=f"BATCH-WEB-{hash(url) & 0xffffff}",
            source_type="web",
            source_url_or_title=url,
            extracted_claims=claims,
            state_assigned=KnowledgeState.D_SESSION_ONLY,
            notes="Web extraction complete. Screened for injection. Held in Session Only state."
        )

    @classmethod
    def ingest_youtube(
        cls,
        url: str,
        transcript: Optional[str] = None,
        evidence_level: YouTubeEvidenceLevel = YouTubeEvidenceLevel.METADATA_ONLY
    ) -> IngestionBatchReport:
        yt_report = YouTubeEngine.analyze_source(url, transcript, evidence_level)
        return IngestionBatchReport(
            batch_id=f"BATCH-YT-{hash(url) & 0xffffff}",
            source_type="youtube",
            source_url_or_title=url,
            extracted_claims=yt_report.claims_extracted,
            state_assigned=KnowledgeState.D_SESSION_ONLY,
            notes=yt_report.evidence_disclosure
        )
