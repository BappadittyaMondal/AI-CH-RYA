"""
Contradiction Engine (§14)
When sources or traditions disagree, explicitly preserves and presents
divergent perspectives without forcing artificial synthesis or flattening differences.
"""

from typing import List
from pydantic import BaseModel, Field
from app.ingestion.claims import AtomicClaim


class ContradictionReport(BaseModel):
    subject: str
    divergent_claims: List[AtomicClaim] = Field(default_factory=list)
    resolution_type: str = "PRESERVED_DIVERGENCE"  # Do not force reconciliation (§14)
    explanatory_note: str

    @classmethod
    def create_report(cls, subject: str, claims: List[AtomicClaim]) -> "ContradictionReport":
        note = (
            f"Sources present distinct viewpoints regarding '{subject}'. "
            "In accordance with §14 of the Master Specification, these are preserved side-by-side "
            "rather than artificially synthesized into a false consensus."
        )
        return cls(
            subject=subject,
            divergent_claims=claims,
            resolution_type="PRESERVED_DIVERGENCE",
            explanatory_note=note
        )
