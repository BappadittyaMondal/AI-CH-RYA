"""
Teaching Modes & Learner Adaptive Progression (§20)
Supports Beginner, Student, Scholar, and Sādhaka pedagogical levels.
Frames Sādhaka guidance strictly as contemplative self-inquiry, never dogmatic command.
"""

from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class TeachingMode(str, Enum):
    BEGINNER = "Beginner"
    STUDENT = "Student"
    SCHOLAR = "Scholar"
    SADHAKA = "Sādhaka"


class LearnerProgress(BaseModel):
    learner_id: str
    preferred_mode: TeachingMode = TeachingMode.STUDENT
    completed_modules: List[str] = Field(default_factory=list)
    vocabulary_mastery: Dict[str, float] = Field(default_factory=dict)
    quiz_scores: List[float] = Field(default_factory=list)
    spaced_repetition_due: List[str] = Field(default_factory=list)
    opt_in_progress_tracking: bool = True

    def calculate_average_score(self) -> float:
        if not self.quiz_scores:
            return 0.0
        return sum(self.quiz_scores) / len(self.quiz_scores)


class PedagogyEngine:
    """Adapts instructional framing to learner mode while maintaining factual precision."""

    @classmethod
    def frame_explanation(cls, mode: TeachingMode, core_concept: str, details: Dict[str, str]) -> str:
        if mode == TeachingMode.BEGINNER:
            return (
                f"**Narrative Introduction to {core_concept}**\n\n"
                f"{details.get('story_framing', 'Imagine an analogy to understand this principle...')}\n\n"
                f"Everyday takeaway: {details.get('everyday_analogy', '')}"
            )
        elif mode == TeachingMode.STUDENT:
            return (
                f"**Structured Study: {core_concept}**\n\n"
                f"- Definition: {details.get('definition', '')}\n"
                f"- Etymology/Root: {details.get('etymology', '')}\n"
                f"- Key Principles: {details.get('principles', '')}\n"
                f"- Check for Understanding: {details.get('quiz_prompt', '')}"
            )
        elif mode == TeachingMode.SCHOLAR:
            return (
                f"**Scholarly & Textual Analysis: {core_concept}**\n\n"
                f"Primary Sanskrit Text: {details.get('sanskrit', '')}\n"
                f"Grammatical Apparatus: {details.get('grammar', '')}\n"
                f"Commentary Lineages: {details.get('commentaries', '')}\n"
                f"Critical/Historical Appraisal: {details.get('historical', '')}"
            )
        elif mode == TeachingMode.SADHAKA:
            # Rule §20 & §1: Always framed as reflection, never as command or authority claim.
            return (
                f"**Contemplative Self-Inquiry (Sādhaka Focus): {core_concept}**\n\n"
                f"Reflective Passage: {details.get('sanskrit', '')}\n\n"
                f"**Contemplative Inquiry Prompts:**\n"
                f"1. Observe in your own experience: {details.get('inquiry_1', 'How does this appear in daily consciousness?')}\n"
                f"2. Self-examination: {details.get('inquiry_2', 'Where is the attachment or identification rooted?')}\n\n"
                f"*Note: These prompts are offered as inward mirrors for discernment (viveka), not as spiritual commands.*"
            )
        return details.get("definition", "")
