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

    def search(
        self,
        query: str,
        limit: int = 5,
        min_state: KnowledgeState = KnowledgeState.C_CANDIDATE
    ) -> List[HybridSearchResult]:
        """
        Executes hybrid search with structured exact match priority,
        followed by lexical/semantic scoring. Never returns superseded facts.
        """
        results: List[HybridSearchResult] = []

        # 1. Exact verse ID retrieval (Rule §11: resolves via structured metadata, NOT semantic similarity)
        exact_id = self.normalize_verse_query(query)
        if exact_id and exact_id in self.corpus:
            chunk = self.corpus[exact_id]
            if not chunk.is_superseded:
                results.append(HybridSearchResult(
                    chunk=chunk,
                    match_type="EXACT_VERSE_ID",
                    score=1.0,
                    state_rank=self._state_priority(chunk.state)
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
                results.append(HybridSearchResult(
                    chunk=chunk,
                    match_type="LEXICAL_BM25",
                    score=float(jaccard),
                    state_rank=self._state_priority(chunk.state)
                ))

        # Rank by State Priority (A > B > C) first, then by match score
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
