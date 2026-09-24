"""
Age-Appropriate & Wellbeing Layer (§28)
Enforces:
1. No fear-based teaching (karma/punishment taught descriptively, never coercively).
2. Grief and death sensitivity (compassionate presence first, never cold dogma).
3. No spiritual bypassing (immediate supportive response and crisis referral when distress is detected).
"""

import re
from typing import Optional, Tuple
from pydantic import BaseModel


class WellbeingAssessment(BaseModel):
    is_crisis_query: bool
    is_grief_query: bool
    is_minor_safe: bool
    framing_guidance: str
    crisis_response_text: Optional[str] = None


class WellbeingGuard:
    """Safeguards learners from fear-based coercion, emotional distress, and spiritual bypassing."""

    CRISIS_KEYWORDS = [
        r'\bsuicid',
        r'\bkill\s+myself\b',
        r'\bend\s+my\s+life\b',
        r'\bwant\s+to\s+die\b',
        r'\bself[- ]harm\b',
    ]

    GRIEF_KEYWORDS = [
        r'\blost\s+my\s+(?:mother|father|parent|child|son|daughter|brother|sister|friend|spouse|husband|wife)\b',
        r'\bpassed\s+away\b',
        r'\bgrieving\b',
        r'\bmourning\b',
        r'\bdeath\s+of\s+my\b',
    ]

    FEAR_PATTERNS = [
        r'you\s+will\s+rot\s+in\s+hell',
        r'sinners\s+will\s+burn',
        r'divine\s+wrath\s+will\s+punish\s+you',
        r'you\s+will\s+be\s+cursed',
    ]

    @classmethod
    def evaluate_learner_prompt(cls, prompt: str, is_child_mode: bool = False) -> WellbeingAssessment:
        p_lower = prompt.lower()

        # 1. Crisis Check (No Spiritual Bypassing §28)
        for pattern in cls.CRISIS_KEYWORDS:
            if re.search(pattern, p_lower):
                crisis_msg = (
                    "I hear that you are going through immense pain right now, and I want you to know that you are not alone. "
                    "Your life and wellbeing are precious. Please reach out to someone who can help you immediately:\n\n"
                    "- In India: Tele-MANAS (14416 or 1800-891-4416) or Vandrevala Foundation (9999 666 555)\n"
                    "- In the US: Call or text 988 (Suicide & Crisis Lifeline)\n"
                    "- In the UK: Call 111 or Samaritans at 116 123\n"
                    "- International: Find local resources at https://findahelpline.com/\n\n"
                    "Rather than a philosophical lesson right now, please take a moment to speak directly with a caring professional or loved one."
                )
                return WellbeingAssessment(
                    is_crisis_query=True,
                    is_grief_query=False,
                    is_minor_safe=True,
                    framing_guidance="Immediate empathetic crisis redirect. No doctrinal bypassing.",
                    crisis_response_text=crisis_msg
                )

        # 2. Grief Sensitivity Check
        for pattern in cls.GRIEF_KEYWORDS:
            if re.search(pattern, p_lower):
                return WellbeingAssessment(
                    is_crisis_query=False,
                    is_grief_query=True,
                    is_minor_safe=True,
                    framing_guidance="Acknowledge personal loss with compassionate warmth first before introducing philosophical context."
                )

        # 3. Child-safe / Non-fear framing check
        return WellbeingAssessment(
            is_crisis_query=False,
            is_grief_query=False,
            is_minor_safe=True,
            framing_guidance="Standard balanced pedagogical framing." if not is_child_mode else "Gentle narrative framing without fearful imagery."
        )

    @classmethod
    def sanitize_output_against_fear(cls, text: str) -> str:
        """Removes coercive or fear-based doctrinal pronouncements."""
        sanitized = text
        for pat in cls.FEAR_PATTERNS:
            sanitized = re.sub(pat, "[explained descriptively as traditional cosmological concept]", sanitized, flags=re.IGNORECASE)
        return sanitized
