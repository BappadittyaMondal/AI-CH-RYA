"""
Knowledge Version Control (§26)
Tracks full lifecycle: Created -> Verified -> Updated -> Superseded -> Deprecated -> Rejected.
Ensures knowledge is never silently overwritten and maintains an auditable provenance chain.
"""

from enum import Enum
from typing import List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class FactLifecycleStatus(str, Enum):
    CREATED = "Created"
    VERIFIED = "Verified"
    UPDATED = "Updated"
    SUPERSEDED = "Superseded"
    DEPRECATED = "Deprecated"
    REJECTED = "Rejected"


class VersionAuditEntry(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: FactLifecycleStatus
    actor: str
    rationale: str
    evidence_reference: Optional[str] = None


class VersionedKnowledgeFact(BaseModel):
    fact_id: str
    canonical_text_id: str
    statement: str
    version_number: int = 1
    status: FactLifecycleStatus = FactLifecycleStatus.CREATED
    superseded_by_fact_id: Optional[str] = None
    audit_history: List[VersionAuditEntry] = Field(default_factory=list)

    def transition_status(
        self,
        new_status: FactLifecycleStatus,
        actor: str,
        rationale: str,
        superseding_id: Optional[str] = None
    ) -> None:
        """Transitions fact through lifecycle with compulsory rationale and actor logging."""
        self.status = new_status
        if superseding_id:
            self.superseded_by_fact_id = superseding_id

        entry = VersionAuditEntry(
            status=new_status,
            actor=actor,
            rationale=rationale,
            evidence_reference=superseding_id
        )
        self.audit_history.append(entry)
