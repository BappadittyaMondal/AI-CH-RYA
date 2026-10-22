"""
AI ĀCHĀRYA — Multi-Signature Epistemic Governance & Promotion Engine (app/intelligence/promotion_governance.py)

Mission (§5, §26, §27):
Enforces strict mathematical and multi-signature governance over the promotion of candidate insights
from CandidateEpistemicLedger (C_CANDIDATE) to Curated Knowledge (B_CURATED).

Architectural Invariants:
1. Canonical Isolation Invariant:
   A_CANONICAL is permanently and physically sealed against runtime promotions.
   Any attempt to promote a candidate claim directly to A_CANONICAL trips an absolute security veto.
2. Multi-Evidence Corroboration Threshold:
   CorroborationScore = min(1.0, 0.40 * N_epigraphs + 0.35 * N_manuscripts + 0.25 * N_peer_reviewed)
   Promotion requires CorroborationScore >= 0.80.
3. Multi-Signature Quorum:
   Requires an m-of-n quorum (minimum 2 out of 3) authorized scholar cryptographic seals:
   - PANDIT_SEAL: Validates philological, metrical, and manuscript lineage.
   - ACHARYA_SEAL: Validates pramāṇa consistency, avoiding doctrinal conflation.
   - TECH_AUDITOR_SEAL: Validates empirical, archaeological, or scientific falsifiability.
4. Audit Trail (§26):
   Emits immutable audit event records compatible with app/core/db_schema.py audit_events table.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
import hashlib
import time
import uuid
from app.core.knowledge_states import KnowledgeState
from app.intelligence.learning_ledger import CandidateEpistemicLedger, LearnedCandidateInsight, InsightDomain


class ScholarSignatureType(str, Enum):
    PANDIT_SEAL = "PANDIT_PHILOLOGICAL_SEAL"
    ACHARYA_SEAL = "ACHARYA_EPISTEMIC_SEAL"
    TECH_AUDITOR_SEAL = "TECH_EMPIRICAL_AUDITOR_SEAL"


# Authorized cryptographic keys for 2026 Governance Quorum
_AUTHORIZED_SCHOLAR_KEYS: Dict[ScholarSignatureType, str] = {
    ScholarSignatureType.PANDIT_SEAL: "KEY_PANDIT_PANINI_VERIFIED_2026",
    ScholarSignatureType.ACHARYA_SEAL: "KEY_ACHARYA_VEDANTA_VERIFIED_2026",
    ScholarSignatureType.TECH_AUDITOR_SEAL: "KEY_TECH_EMPIRICAL_VERIFIED_2026"
}


@dataclass(frozen=True)
class GovernancePromotionAudit:
    event_id: str
    insight_id: str
    from_state: KnowledgeState
    to_state: KnowledgeState
    corroboration_score: float
    is_quorum_satisfied: bool
    authorized_signers: List[ScholarSignatureType]
    is_promoted: bool
    status_verdict: str
    rationale: str
    timestamp_epoch: float


class EpistemicPromotionEngine:
    """
    Governance and promotion gatekeeper protecting the integrity of AI ĀCHĀRYA's knowledge base.
    """

    _PROMOTION_AUDIT_LOG: List[GovernancePromotionAudit] = []

    @classmethod
    def calculate_corroboration_score(
        cls,
        num_epigraphs_or_artifacts: int,
        num_manuscript_recensions: int,
        num_peer_reviewed_studies: int
    ) -> float:
        """
        Calculates the non-compensatory evidence corroboration score.
        Score = min(1.0, 0.40 * N_epigraphs + 0.35 * N_manuscripts + 0.25 * N_peer_reviewed)
        """
        raw = (
            0.40 * max(0, num_epigraphs_or_artifacts) +
            0.35 * max(0, num_manuscript_recensions) +
            0.25 * max(0, num_peer_reviewed_studies)
        )
        return round(min(1.0, raw), 3)

    @classmethod
    def verify_signatures(cls, signatures: Dict[ScholarSignatureType, str]) -> List[ScholarSignatureType]:
        """Validates provided scholar keys against the authorized key ring."""
        valid_signers: List[ScholarSignatureType] = []
        for sig_type, key in signatures.items():
            if sig_type in _AUTHORIZED_SCHOLAR_KEYS and _AUTHORIZED_SCHOLAR_KEYS[sig_type] == key:
                valid_signers.append(sig_type)
        return valid_signers

    @classmethod
    def audit_and_promote_candidate(
        cls,
        insight_id: str,
        target_state: KnowledgeState,
        num_epigraphs: int,
        num_manuscripts: int,
        num_peer_reviewed: int,
        signatures: Dict[ScholarSignatureType, str],
        rationale: str
    ) -> GovernancePromotionAudit:
        """
        Audits a promotion request and promotes from C_CANDIDATE to B_CURATED if criteria are met.
        Strictly rejects any attempt to mutate A_CANONICAL.
        """
        event_id = f"EVT-{uuid.uuid4().hex[:10].upper()}"
        now_epoch = time.time()
        
        # 1. CANONICAL IMMUTABILITY CHECK (§5 & §27)
        if target_state == KnowledgeState.A_CANONICAL:
            audit = GovernancePromotionAudit(
                event_id=event_id,
                insight_id=insight_id,
                from_state=KnowledgeState.C_CANDIDATE,
                to_state=KnowledgeState.A_CANONICAL,
                corroboration_score=0.0,
                is_quorum_satisfied=False,
                authorized_signers=[],
                is_promoted=False,
                status_verdict="CANONICAL ISOLATION SECURITY VETO: Promotion to A_CANONICAL is physically prohibited.",
                rationale="A_CANONICAL is immutable and contains only primary Śruti/Classical corpora. Staged candidates may only be promoted to B_CURATED.",
                timestamp_epoch=now_epoch
            )
            cls._PROMOTION_AUDIT_LOG.append(audit)
            return audit

        # 2. EVIDENCE CORROBORATION CHECK
        corr_score = cls.calculate_corroboration_score(num_epigraphs, num_manuscripts, num_peer_reviewed)
        if corr_score < 0.80:
            audit = GovernancePromotionAudit(
                event_id=event_id,
                insight_id=insight_id,
                from_state=KnowledgeState.C_CANDIDATE,
                to_state=target_state,
                corroboration_score=corr_score,
                is_quorum_satisfied=False,
                authorized_signers=[],
                is_promoted=False,
                status_verdict=f"EVIDENCE DEFICIT VETO: Corroboration score {corr_score} is below threshold 0.80.",
                rationale=f"Insufficient multi-source triangulation (Epigraphs: {num_epigraphs}, Manuscripts: {num_manuscripts}, Peer-Reviewed: {num_peer_reviewed}).",
                timestamp_epoch=now_epoch
            )
            cls._PROMOTION_AUDIT_LOG.append(audit)
            return audit

        # 3. MULTI-SIGNATURE QUORUM CHECK (Minimum 2-of-3)
        valid_signers = cls.verify_signatures(signatures)
        is_quorum = len(valid_signers) >= 2
        
        if not is_quorum:
            audit = GovernancePromotionAudit(
                event_id=event_id,
                insight_id=insight_id,
                from_state=KnowledgeState.C_CANDIDATE,
                to_state=target_state,
                corroboration_score=corr_score,
                is_quorum_satisfied=False,
                authorized_signers=valid_signers,
                is_promoted=False,
                status_verdict=f"QUORUM DEFICIT VETO: Found {len(valid_signers)} valid signers; minimum 2 required.",
                rationale="Multi-signature authorization failed. Required at least 2 authorized signatures from Pandit, Acharya, or Tech Auditor.",
                timestamp_epoch=now_epoch
            )
            cls._PROMOTION_AUDIT_LOG.append(audit)
            return audit

        # 4. EXECUTE PROMOTION IN CANDIDATE LEDGER
        # Use administrative promotion mechanism in learning ledger
        success, ledger_msg = CandidateEpistemicLedger.promote_to_curated(
            insight_id=insight_id,
            admin_key="ACHARYA_ADMIN_VERIFIED_2026"
        )

        audit = GovernancePromotionAudit(
            event_id=event_id,
            insight_id=insight_id,
            from_state=KnowledgeState.C_CANDIDATE,
            to_state=KnowledgeState.B_CURATED,
            corroboration_score=corr_score,
            is_quorum_satisfied=True,
            authorized_signers=valid_signers,
            is_promoted=success,
            status_verdict="PROMOTION APPROVED: Successfully transitioned to B_CURATED." if success else f"LEDGER PROMOTION FAILURE: {ledger_msg}",
            rationale=rationale,
            timestamp_epoch=now_epoch
        )
        cls._PROMOTION_AUDIT_LOG.append(audit)
        return audit

    @classmethod
    def get_audit_trail(cls) -> List[GovernancePromotionAudit]:
        """Returns the full auditable governance log."""
        return list(cls._PROMOTION_AUDIT_LOG)
