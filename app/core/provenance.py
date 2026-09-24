"""
Source Provenance Schema ("Source DNA") (§7)
Ensures Answer -> Claim -> Source -> exact chapter/verse/page is reconstructable.
"""

from typing import Optional, List
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from app.core.ontology import TextType


class RightsStatus(str):
    PUBLIC_DOMAIN = "PUBLIC_DOMAIN"
    OPEN_LICENSE = "OPEN_LICENSE"
    SCHOLARLY_USE_RESTRICTED = "SCHOLARLY_USE_RESTRICTED"
    COPYRIGHTED = "COPYRIGHTED"
    USER_SUPPLIED = "USER_SUPPLIED"
    LICENSED_CORPUS = "LICENSED_CORPUS"
    RESTRICTED = "RESTRICTED"
    UNKNOWN = "UNKNOWN"


class SourceDNA(BaseModel):
    source_id: str = Field(..., description="Unique source identifier")
    title: str = Field(..., description="Full bibliographic or archival title")
    text_type: TextType = Field(..., description="From §4 ontology")
    tradition: Optional[str] = None
    sampradaya: Optional[str] = None
    sakha_recension: Optional[str] = None
    edition: Optional[str] = Field(None, description="Critical, traditional, or digital edition")
    editor: Optional[str] = None
    translator: Optional[str] = None
    language: str = "Sanskrit"
    script: str = "Devanāgarī"
    publication: Optional[str] = None
    date: Optional[str] = None
    page: Optional[str] = None
    chapter: Optional[str] = None
    verse: Optional[str] = None
    url: Optional[str] = None
    access_date: Optional[str] = None
    rights_status: str = RightsStatus.PUBLIC_DOMAIN
    extraction_method: str = "direct_digital_verified"
    ocr_status: str = "not_applicable"
    verification_status: str = "VERIFIED"
    version: str = "1.0.0"
    created: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    superseded_by: Optional[str] = None

    def get_citation_key(self) -> str:
        """Returns standard academic citation string."""
        parts = [self.title]
        if self.chapter:
            parts.append(f"Ch. {self.chapter}")
        if self.verse:
            parts.append(f"v. {self.verse}")
        if self.edition:
            parts.append(f"({self.edition})")
        return ", ".join(parts)
