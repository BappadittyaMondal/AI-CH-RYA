"""
Website Intelligence Sub-Engine (§13b)
Safe fetching, sanitization, prompt injection screening, and claim extraction.
Treats all external webpage instructions strictly as INERT DATA, never executed.
"""

import re
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from app.ingestion.claims import AtomicClaim
from app.core.epistemic import EpistemicCategory


class WebSanitizationReport(BaseModel):
    url: str
    raw_length: int
    cleaned_length: int
    prompt_injection_flags_detected: List[str] = Field(default_factory=list)
    is_safe: bool = True
    claims: List[AtomicClaim] = Field(default_factory=list)


class WebEngine:
    """Safe ingestion handler for web content."""

    INJECTION_PATTERNS = [
        r'ignore\s+all\s+(?:prior|previous)\s+instructions',
        r'system\s*:\s*you\s+are\s+now',
        r'act\s+as\s+an\s+unrestricted',
        r'disregard\s+ethical\s+guidelines',
        r'jailbreak',
        r'dan\s+mode',
        r'exfiltrate',
        r'send\s+api_key',
    ]

    @classmethod
    def sanitize_and_screen(cls, url: str, raw_html_or_text: str) -> WebSanitizationReport:
        """
        Screens text for adversarial prompt injection patterns.
        Neutralizes prompt injections by treating all text strictly as inert data.
        """
        flags: List[str] = []
        lower_content = raw_html_or_text.lower()

        for pattern in cls.INJECTION_PATTERNS:
            if re.search(pattern, lower_content):
                flags.append(pattern)

        # Basic stripping of script tags if HTML
        cleaned = re.sub(r'<script.*?</script>', '', raw_html_or_text, flags=re.DOTALL | re.IGNORECASE)
        cleaned = re.sub(r'<style.*?</style>', '', cleaned, flags=re.DOTALL | re.IGNORECASE)
        cleaned = re.sub(r'<[^>]+>', ' ', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()

        claims: List[AtomicClaim] = []
        # Extract atomic sample claims (paraphrased)
        sentences = [s.strip() for s in re.split(r'[\.\!\?]', cleaned) if len(s.strip()) > 20]
        for s in sentences[:5]:
            claims.append(
                AtomicClaim(
                    claim_text=f"External source claims: {s}",
                    claim_type=EpistemicCategory.USER_SUPPLIED_CLAIM,
                    source_title=f"Web Source: {url}",
                    source_url_or_ref=url,
                    evidence_nature="web_text_statement"
                )
            )

        return WebSanitizationReport(
            url=url,
            raw_length=len(raw_html_or_text),
            cleaned_length=len(cleaned),
            prompt_injection_flags_detected=flags,
            is_safe=len(flags) == 0,
            claims=claims
        )
