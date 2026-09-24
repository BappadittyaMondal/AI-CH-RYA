"""
Claim Engine (Atomic Knowledge Units) (§15)
Converts external material into discrete, verifiable atomic claims.
Respects copyright by paraphrasing rather than bulk quoting.
"""

import uuid
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field
from app.core.epistemic import EpistemicCategory


class ClaimVerificationStatus(str, Enum):
    UNVERIFIED = "unverified"
    PARTIALLY_VERIFIED = "partially_verified"
    VERIFIED = "verified"


class AtomicClaim(BaseModel):
    claim_id: str = Field(default_factory=lambda: f"CLM-{uuid.uuid4().hex[:6].upper()}")
    claim_text: str = Field(..., description="Paraphrased atomic proposition, not verbatim bulk copyright copy")
    claim_type: EpistemicCategory = EpistemicCategory.USER_SUPPLIED_CLAIM
    source_title: str
    speaker_or_author: Optional[str] = None
    source_url_or_ref: Optional[str] = None
    timestamp_or_page: Optional[str] = None
    evidence_nature: str = Field("direct_statement", description="direct statement / inference / citation")
    status: ClaimVerificationStatus = ClaimVerificationStatus.UNVERIFIED
    related_canonical_text: Optional[str] = None
    contradictory_claim_ids: List[str] = Field(default_factory=list)
    permanent_knowledge: bool = False  # NO by default — requires governance approval (§15, §30)
