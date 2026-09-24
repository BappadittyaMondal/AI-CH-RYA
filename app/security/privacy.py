"""
User Memory vs Knowledge Memory Strict Separation (§27, §32)
Strict boundary enforcement ensuring learner progress, notes, and quiz histories
are completely isolated and never leak or pollute the shared canonical knowledge base.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from app.core.knowledge_states import KnowledgeState


class UserMemoryStore(BaseModel):
    user_id: str
    private_notes: Dict[str, str] = Field(default_factory=dict)
    quiz_history: Dict[str, Any] = Field(default_factory=dict)
    preferences: Dict[str, Any] = Field(default_factory=dict)
    allow_tracking: bool = True

    def reset_private_data(self) -> None:
        """Allows learner to completely wipe personal progress data (§32)."""
        self.private_notes.clear()
        self.quiz_history.clear()
        self.preferences.clear()


class MemoryIsolationGate:
    """Guarantees that User Memory cannot be written to Canonical or Curated Knowledge."""

    @staticmethod
    def assert_separation(source_layer: str, target_knowledge_state: KnowledgeState) -> bool:
        """
        Returns False and raises ValueError if user memory attempts
        to be persisted as canonical or curated knowledge.
        """
        if source_layer == "USER_MEMORY":
            if target_knowledge_state in [KnowledgeState.A_CANONICAL, KnowledgeState.B_CURATED, KnowledgeState.C_CANDIDATE]:
                raise PermissionError(
                    "Strict Memory Separation Violation (§27): "
                    "User personal notes/data cannot be merged into shared knowledge bases."
                )
        return True
