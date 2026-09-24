"""
Document & Manuscript Intelligence Sub-Engine (§13c)
Handles PDF/Document ingestion with OCR corruption detection and structure preservation.
Keeps original raw text and normalized text strictly separate.
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from app.core.provenance import RightsStatus
from app.sanskrit.engine import SanskritEngine


class DocumentPage(BaseModel):
    page_number: int
    raw_extracted_text: str
    normalized_text: str
    ocr_corruption_detected: bool = False
    chapter_or_section: Optional[str] = None


class DocumentIngestionReport(BaseModel):
    document_title: str
    total_pages: int
    rights_status: str = RightsStatus.USER_SUPPLIED
    pages: List[DocumentPage] = Field(default_factory=list)
    has_corruptions: bool = False


class DocumentEngine:
    """Processes document files preserving structure and separating raw vs normalized states."""

    @classmethod
    def process_text_document(
        cls,
        title: str,
        text_pages: List[str],
        rights: str = RightsStatus.USER_SUPPLIED
    ) -> DocumentIngestionReport:
        pages: List[DocumentPage] = []
        any_corruption = False

        for idx, raw_page in enumerate(text_pages, start=1):
            ocr_res = SanskritEngine.normalize_ocr(raw_page)
            has_corrupt = ocr_res["was_modified"]
            if has_corrupt:
                any_corruption = True

            pages.append(
                DocumentPage(
                    page_number=idx,
                    raw_extracted_text=raw_page,
                    normalized_text=ocr_res["normalized_ocr"],
                    ocr_corruption_detected=has_corrupt
                )
            )

        return DocumentIngestionReport(
            document_title=title,
            total_pages=len(pages),
            rights_status=rights,
            pages=pages,
            has_corruptions=any_corruption
        )
