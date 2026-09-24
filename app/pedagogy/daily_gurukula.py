"""
Daily Gurukula Engine (§21)
Generates an opt-in personalized daily micro-curriculum containing 7 balanced elements.
"""

from typing import Optional, List
from pydantic import BaseModel, Field
from app.pedagogy.modes import TeachingMode


class DailyMicroCurriculum(BaseModel):
    day_number: int
    mode: TeachingMode = TeachingMode.STUDENT
    one_shloka: str
    one_sanskrit_word: str
    sanskrit_word_meaning: str
    one_historical_insight: str
    one_cultural_explainer: str
    one_dharma_reflection: str
    one_quiz_question: str
    quiz_options: List[str]
    quiz_correct_index: int
    one_revision_item: str


class DailyGurukulaService:
    """Delivers structured daily Gurukula lessons."""

    @classmethod
    def generate_lesson(cls, day: int = 1, mode: TeachingMode = TeachingMode.STUDENT) -> DailyMicroCurriculum:
        return DailyMicroCurriculum(
            day_number=day,
            mode=mode,
            one_shloka="कर्मण्येवाधिकारस्ते मा फलेषु कदाचन। (Gītā 2.47a)",
            one_sanskrit_word="ऋत (Ṛta)",
            sanskrit_word_meaning="The primordial cosmic and moral harmony that orders the universe.",
            one_historical_insight="Archaeological and astronomical references suggest the antiquity of Vedic constellations (Nakṣatra system).",
            one_cultural_explainer="Lighting a dīpa (oil lamp) represents the removal of ignorance (tamas) by the light of knowledge (jñāna).",
            one_dharma_reflection="In your daily duties today, practice focusing entirely on sincere execution without mental anxiety over praise or blame.",
            one_quiz_question="What does the term 'Adhikāra' in Gītā 2.47 strictly designate?",
            quiz_options=[
                "Entitlement to personal fruits",
                "Rightful jurisdiction and duty of action",
                "Passive abandonment of effort",
                "Fatalistic destiny"
            ],
            quiz_correct_index=1,
            one_revision_item="Recall: How does Śraddhā differ from blind credulity?"
        )
