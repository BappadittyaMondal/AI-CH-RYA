"""
The Four Knowledge States (§5) & Corpus Protection Engine
"""

from enum import Enum
from typing import Optional, List
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class KnowledgeState(str, Enum):
    A_CANONICAL = "A — CANONICAL"
    B_CURATED = "B — CURATED"
    C_CANDIDATE = "C — CANDIDATE"
    D_SESSION_ONLY = "D — SESSION ONLY"


class PromotionAuditRecord(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    from_state: KnowledgeState
    to_state: KnowledgeState
    reviewer_id: str
    rationale: str
    evidence_profile_id: Optional[str] = None


class KnowledgeItem(BaseModel):
    item_id: str
    content: str
    state: KnowledgeState = KnowledgeState.D_SESSION_ONLY
    source_id: str
    audit_trail: List[PromotionAuditRecord] = Field(default_factory=list)

    def can_transition_to(self, target_state: KnowledgeState) -> bool:
        """
        State promotion sequence: D -> C -> B -> A.
        Demotions are allowed for correction.
        Direct jumping D -> A or C -> A without passing governance is forbidden.
        """
        valid_transitions = {
            KnowledgeState.D_SESSION_ONLY: [KnowledgeState.C_CANDIDATE],
            KnowledgeState.C_CANDIDATE: [KnowledgeState.B_CURATED, KnowledgeState.D_SESSION_ONLY],
            KnowledgeState.B_CURATED: [KnowledgeState.A_CANONICAL, KnowledgeState.C_CANDIDATE],
            KnowledgeState.A_CANONICAL: [KnowledgeState.B_CURATED],  # Demotion if dispute arises
        }
        return target_state in valid_transitions.get(self.state, [])

    def request_promotion(
        self,
        target_state: KnowledgeState,
        reviewer_id: str,
        rationale: str,
        evidence_profile_id: Optional[str] = None,
    ) -> bool:
        """
        Promotes an item if the transition is valid and authenticated.
        Automatic promotion is strictly forbidden.
        """
        if not reviewer_id or reviewer_id.strip() == "":
            raise ValueError("Governance violation: Reviewer ID is required for state transition.")

        if not self.can_transition_to(target_state):
            raise ValueError(
                f"Invalid transition from {self.state.value} to {target_state.value}. "
                "Promotion D->C->B->A requires step-by-step governance."
            )

        audit = PromotionAuditRecord(
            from_state=self.state,
            to_state=target_state,
            reviewer_id=reviewer_id,
            rationale=rationale,
            evidence_profile_id=evidence_profile_id,
        )
        self.audit_trail.append(audit)
        self.state = target_state
        return True
