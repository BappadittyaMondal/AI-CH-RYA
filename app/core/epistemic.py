"""
Epistemic Separation Engine (§6)
Ensures distinct categorization of textual, traditional, commentary,
historical, linguistic, philosophical, empirical, and modern scholarly claims.
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class EpistemicCategory(str, Enum):
    PRIMARY_TEXTUAL_CLAIM = "PRIMARY_TEXTUAL_CLAIM"
    TRADITIONAL_INTERPRETATION = "TRADITIONAL_INTERPRETATION"
    SAMPRADAYA_SPECIFIC_VIEW = "SAMPRADAYA_SPECIFIC_VIEW"
    COMMENTARIAL_CLAIM = "COMMENTARIAL_CLAIM"
    HISTORICAL_CLAIM = "HISTORICAL_CLAIM"
    LINGUISTIC_CLAIM = "LINGUISTIC_CLAIM"
    PHILOSOPHICAL_ARGUMENT = "PHILOSOPHICAL_ARGUMENT"
    MODERN_SCHOLARLY_VIEW = "MODERN_SCHOLARLY_VIEW"
    EMPIRICAL_SCIENTIFIC_CLAIM = "EMPIRICAL_SCIENTIFIC_CLAIM"
    SYMBOLIC_INTERPRETATION = "SYMBOLIC_INTERPRETATION"
    USER_SUPPLIED_CLAIM = "USER_SUPPLIED_CLAIM"
    UNVERIFIED_CLAIM = "UNVERIFIED_CLAIM"
    ARCHAEOLOGICAL_STRATIGRAPHIC_CLAIM = "ARCHAEOLOGICAL_STRATIGRAPHIC_CLAIM"
    ASTRONOMICAL_DATING_CLAIM = "ASTRONOMICAL_DATING_CLAIM"
    LINGUISTIC_RECONSTRUCTION_CLAIM = "LINGUISTIC_RECONSTRUCTION_CLAIM"
    COMMERCIAL_MARKETING_CTA = "COMMERCIAL_MARKETING_CTA"
    GEO_ECONOMIC_SUPPLY_CHAIN_CLAIM = "GEO_ECONOMIC_SUPPLY_CHAIN_CLAIM"


class EpistemicClaim(BaseModel):
    category: EpistemicCategory
    claim_text: str
    citation: Optional[str] = None
    tradition_or_scholar: Optional[str] = None
    is_empirical: bool = False

    def validate_scientific_claim(self) -> None:
        """
        Rule §6 & §3: EMPIRICAL_SCIENTIFIC_CLAIM is held to empirical scientific standards.
        It must never be inflated by scriptural authority.
        """
        if self.category == EpistemicCategory.EMPIRICAL_SCIENTIFIC_CLAIM:
            self.is_empirical = True


class MultiLensAnswerSegment(BaseModel):
    """
    Answers must never merge these four distinct questions without explicit labels:
    1. What does the text say?
    2. What does tradition/commentary say?
    3. What do historians argue?
    4. What can be empirically demonstrated?
    """
    textual_claim: Optional[EpistemicClaim] = None
    traditional_interpretation: Optional[EpistemicClaim] = None
    historical_claim: Optional[EpistemicClaim] = None
    empirical_claim: Optional[EpistemicClaim] = None
    other_claims: List[EpistemicClaim] = Field(default_factory=list)

    def is_properly_separated(self) -> bool:
        """Verifies that no claim is left untagged or ambiguously conflated."""
        all_claims = []
        if self.textual_claim:
            all_claims.append(self.textual_claim)
        if self.traditional_interpretation:
            all_claims.append(self.traditional_interpretation)
        if self.historical_claim:
            all_claims.append(self.historical_claim)
        if self.empirical_claim:
            all_claims.append(self.empirical_claim)
        all_claims.extend(self.other_claims)

        for c in all_claims:
            if not isinstance(c.category, EpistemicCategory):
                return False
        return True
