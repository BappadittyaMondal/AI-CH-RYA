"""
Commentary, Rights & Copyright Engine (§24)
Tags external sources and strictly separates Research Mode vs Knowledge Contribution Mode.
Enforces copyright-safe paraphrasing over bulk reproduction.
"""

from enum import Enum
from pydantic import BaseModel, Field
from app.core.provenance import RightsStatus


class IngestionOperatingMode(str, Enum):
    RESEARCH_MODE = "Research Mode"  # Temporary session-only analysis (State D)
    KNOWLEDGE_CONTRIBUTION_MODE = "Knowledge Contribution Mode"  # Governed permanent queue


class CopyrightAuditResult(BaseModel):
    rights_status: str
    operating_mode: IngestionOperatingMode
    is_bulk_copy: bool
    can_persist_permanently: bool
    notice: str


class CopyrightGuard:
    """Enforces intellectual property and ethical citation standards."""

    MAX_FAIR_USE_QUOTE_CHARS = 350

    @classmethod
    def audit_source_usage(
        cls,
        text_snippet: str,
        rights_status: str,
        mode: IngestionOperatingMode
    ) -> CopyrightAuditResult:
        is_bulk = len(text_snippet) > cls.MAX_FAIR_USE_QUOTE_CHARS

        # In Research Mode, content is strictly ephemeral session data (State D)
        if mode == IngestionOperatingMode.RESEARCH_MODE:
            return CopyrightAuditResult(
                rights_status=rights_status,
                operating_mode=mode,
                is_bulk_copy=is_bulk,
                can_persist_permanently=False,
                notice="Research Mode active: analysis is confined to this session only (State D)."
            )

        # Knowledge Contribution Mode checks
        if rights_status in [RightsStatus.COPYRIGHTED, RightsStatus.RESTRICTED]:
            if is_bulk:
                return CopyrightAuditResult(
                    rights_status=rights_status,
                    operating_mode=mode,
                    is_bulk_copy=True,
                    can_persist_permanently=False,
                    notice="Copyrighted restricted material cannot be ingested in bulk. Paraphrased summary required."
                )

        can_persist = rights_status in [RightsStatus.PUBLIC_DOMAIN, RightsStatus.OPEN_LICENSE]

        return CopyrightAuditResult(
            rights_status=rights_status,
            operating_mode=mode,
            is_bulk_copy=is_bulk,
            can_persist_permanently=can_persist,
            notice="Eligible for Candidate evaluation queue under human governance." if can_persist else "Requires copyright review."
        )
