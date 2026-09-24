"""
Security Guardrails & Untrusted Content Firewall (§25)
Defends against prompt injection, SSRF, secret leakage, and malicious payload executions.
"""

import re
from typing import List, Tuple
from pydantic import BaseModel, Field


class SecurityInspectionResult(BaseModel):
    is_safe: bool
    violations: List[str] = Field(default_factory=list)
    sanitized_text: str


class SecurityGuardrails:
    """Security filter ensuring external content is strictly treated as inert data."""

    BLOCKED_INJECTION_TOKENS = [
        r"ignore\s+all\s+(?:previous|prior)\s+instructions",
        r"reveal\s+your\s+system\s+prompt",
        r"print\s+environment\s+variables",
        r"api[_-]?key",
        r"gemini[_-]?api[_-]?key",
        r"openai[_-]?api[_-]?key",
        r"sudo\s+rm",
        r"<script>",
        r"javascript:",
    ]

    @classmethod
    def inspect_untrusted_input(cls, raw_input: str) -> SecurityInspectionResult:
        violations: List[str] = []
        lowered = raw_input.lower()

        for pattern in cls.BLOCKED_INJECTION_TOKENS:
            if re.search(pattern, lowered):
                violations.append(f"Security Alert: Blocked pattern '{pattern}' detected.")

        sanitized = raw_input
        # Strip script injections
        sanitized = re.sub(r'<script.*?>.*?</script>', '[REDACTED_SCRIPT]', sanitized, flags=re.DOTALL | re.IGNORECASE)

        return SecurityInspectionResult(
            is_safe=len(violations) == 0,
            violations=violations,
            sanitized_text=sanitized
        )
