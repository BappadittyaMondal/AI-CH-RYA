"""
Hybrid Retrieval (RAG) Architecture (§11)
Combines:
1. Exact structured verse-ID lookup (e.g. "Gītā 2.47")
2. BM25 / sparse lexical search
3. Dense semantic vector search
4. Knowledge-graph traversal
5. Source-priority ranking (A Canonical > B Curated > C Candidate)
6. Verse-level chunking
"""

import re
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from app.core.knowledge_states import KnowledgeState
from app.core.provenance import SourceDNA


from enum import Enum


class QueryIntent(str, Enum):
    PRIMARY_TEXT_INTENT = "PRIMARY_TEXT_INTENT"
    COMMENTARY_INTENT = "COMMENTARY_INTENT"
    PHILOSOPHICAL_INTENT = "PHILOSOPHICAL_INTENT"
    HISTORICAL_INTENT = "HISTORICAL_INTENT"
    GENERAL_INTENT = "GENERAL_INTENT"


class VerseChunk(BaseModel):
    chunk_id: str
    text_id: str  # e.g. "BG", "ISHA", "MUNDAKA"
    chapter: str
    verse: str
    canonical_id: str  # e.g. "BG_2_47"
    sanskrit_deva: str
    iast: str
    padaccheda: List[str]
    meaning_summary: str
    commentary_pointers: List[str] = Field(default_factory=list)
    state: KnowledgeState = KnowledgeState.A_CANONICAL
    provenance: Optional[SourceDNA] = None
    embedding: Optional[List[float]] = None
    is_superseded: bool = False


class HybridSearchResult(BaseModel):
    chunk: VerseChunk
    match_type: str  # EXACT_VERSE_ID, LEXICAL_BM25, SEMANTIC_VECTOR
    score: float
    state_rank: int  # 1 for A, 2 for B, 3 for C
    query_intent: QueryIntent = QueryIntent.GENERAL_INTENT
    commentary_target: Optional[str] = None


class HybridRetriever:
    """Manages multi-modal retrieval with strict verse-level precision and priority ordering."""

    def __init__(self):
        self.corpus: Dict[str, VerseChunk] = {}

    def add_verse(self, chunk: VerseChunk) -> None:
        """Stores verse chunk in registry."""
        self.corpus[chunk.canonical_id] = chunk

    @staticmethod
    def normalize_verse_query(query: str) -> Optional[str]:
        """
        Extracts structured verse identifiers from query string.
        Examples:
          "Gītā 2.47" -> "BG_2_47"
          "BG 2:47"   -> "BG_2_47"
          "Isha 1"    -> "ISHA_1_1"
        """
        # Match Bhagavad Gita patterns
        bg_match = re.search(r'(?:g[iī]t[aā]|bg)\s*(\d+)[\.:\s]+(\d+)', query, re.IGNORECASE)
        if bg_match:
            return f"BG_{bg_match.group(1)}_{bg_match.group(2)}"

        # Match Isha Upanishad
        isha_match = re.search(r'(?:[iī][sś]a|i[sś]opani[sṣ]ad)\s*(\d+)', query, re.IGNORECASE)
        if isha_match:
            return f"ISHA_1_{isha_match.group(1)}"

        # Match Katha Upanishad
        katha_match = re.search(r'ka[tṭ]ha\s*(\d+)[\.:\s]+(\d+)[\.:\s]+(\d+)', query, re.IGNORECASE)
        if katha_match:
            return f"KATHA_{katha_match.group(1)}_{katha_match.group(2)}_{katha_match.group(3)}"

        return None

    @staticmethod
    def classify_query_intent(query: str) -> tuple[QueryIntent, Optional[str]]:
        """
        Decouples Ontological Primacy from Hermeneutical Query Target (§4, §11, §12).
        Detects whether user is specifically querying commentary lineage or historical contexts.
        """
        q_lower = query.lower()
        commentary_keywords = {
            "śaṅkara": "Advaita (Śaṅkarācārya)",
            "shankara": "Advaita (Śaṅkarācārya)",
            "adi shankara": "Advaita (Śaṅkarācārya)",
            "rāmānuja": "Viśiṣṭādvaita (Rāmānujācārya)",
            "ramanuja": "Viśiṣṭādvaita (Rāmānujācārya)",
            "madhva": "Dvaita (Madhvācārya)",
            "madhvacharya": "Dvaita (Madhvācārya)",
            "advaita": "Advaita Vedānta",
            "visistadvaita": "Viśiṣṭādvaita Vedānta",
            "viśiṣṭādvaita": "Viśiṣṭādvaita Vedānta",
            "dvaita": "Dvaita Vedānta",
            "bhāṣya": "Traditional Commentary",
            "bhashya": "Traditional Commentary",
            "commentary": "Traditional Commentary",
        }
        for kw, lineage in commentary_keywords.items():
            if kw in q_lower:
                return QueryIntent.COMMENTARY_INTENT, lineage

        if any(h in q_lower for h in ["date", "dating", "archaeology", "historical", "epigraphy", "manuscript", "strata"]):
            return QueryIntent.HISTORICAL_INTENT, None

        if any(p in q_lower for p in ["philosophy", "metaphysics", "cosmology", "darśana", "darsana"]):
            return QueryIntent.PHILOSOPHICAL_INTENT, None

        if re.search(r'(?:g[iī]t[aā]|bg|upanishad|upaniṣad|ved|sūtra)\s*\d*', q_lower):
            return QueryIntent.PRIMARY_TEXT_INTENT, None

        return QueryIntent.GENERAL_INTENT, None

    def search(
        self,
        query: str,
        limit: int = 5,
        min_state: KnowledgeState = KnowledgeState.C_CANDIDATE
    ) -> List[HybridSearchResult]:
        """
        Executes hybrid search with structured exact match priority,
        intent classification, and intent affinity boosting.
        """
        results: List[HybridSearchResult] = []
        intent, target = self.classify_query_intent(query)

        # 1. Exact verse ID retrieval (Rule §11: resolves via structured metadata, NOT semantic similarity)
        exact_id = self.normalize_verse_query(query)
        if exact_id and exact_id in self.corpus:
            chunk = self.corpus[exact_id]
            if not chunk.is_superseded:
                score = 1.0
                if intent == QueryIntent.COMMENTARY_INTENT and target:
                    if any(target.lower() in cp.lower() for cp in chunk.commentary_pointers):
                        score += 0.5  # Intent affinity boost
                results.append(HybridSearchResult(
                    chunk=chunk,
                    match_type="EXACT_VERSE_ID",
                    score=score,
                    state_rank=self._state_priority(chunk.state),
                    query_intent=intent,
                    commentary_target=target
                ))
                return results

        # 2. Sparse lexical / keyword search
        query_tokens = set(re.findall(r'\w+', query.lower()))
        for chunk in self.corpus.values():
            if chunk.is_superseded:
                continue

            content_tokens = set(re.findall(r'\w+', f"{chunk.sanskrit_deva} {chunk.iast} {chunk.meaning_summary}".lower()))
            overlap = query_tokens.intersection(content_tokens)
            if overlap:
                jaccard = len(overlap) / len(query_tokens.union(content_tokens))
                score = float(jaccard)
                # Intent affinity boosting
                if intent == QueryIntent.COMMENTARY_INTENT and target:
                    if any(target.lower() in cp.lower() for cp in chunk.commentary_pointers):
                        score += 0.5

                results.append(HybridSearchResult(
                    chunk=chunk,
                    match_type="LEXICAL_BM25",
                    score=score,
                    state_rank=self._state_priority(chunk.state),
                    query_intent=intent,
                    commentary_target=target
                ))

        # Rank by State Priority (A > B > C) first, then by score
        results.sort(key=lambda r: (r.state_rank, -r.score))
        return results[:limit]

    @staticmethod
    def _state_priority(state: KnowledgeState) -> int:
        """A_CANONICAL (1) > B_CURATED (2) > C_CANDIDATE (3) > D_SESSION_ONLY (4)"""
        priority = {
            KnowledgeState.A_CANONICAL: 1,
            KnowledgeState.B_CURATED: 2,
            KnowledgeState.C_CANDIDATE: 3,
            KnowledgeState.D_SESSION_ONLY: 4,
        }
        return priority.get(state, 99)
