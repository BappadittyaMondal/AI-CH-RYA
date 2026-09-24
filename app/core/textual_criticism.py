"""
Textual Criticism & Recension Awareness (§8)
Ensures variant readings across recensions/śākhās/critical editions
are explicitly preserved and surfaced rather than silently collapsed.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class VariantReading(BaseModel):
    reading_text: str = Field(..., description="Variant Sanskrit or textual reading")
    source_edition_or_ms: str = Field(..., description="e.g. Pune Critical Edition, Kashmir Recension, Vulgate")
    meaning_difference: Optional[str] = Field(None, description="Explanation if variant changes meaning")
    is_critical_consensus: bool = False


class RecensionRecord(BaseModel):
    text_id: str
    base_text: str
    recension_name: str = Field(..., description="e.g. Śaunaka vs Paippalāda, Northern vs Southern Mahābhārata")
    sakha: Optional[str] = None
    manuscript_witnesses: List[str] = Field(default_factory=list)
    edition_type: str = "critical"  # critical, traditional, digital
    variants: List[VariantReading] = Field(default_factory=list)

    def has_material_variance(self) -> bool:
        """Returns True if any variant notes a substantive semantic difference."""
        return any(v.meaning_difference for v in self.variants)
