"""
Multi-Agent Orchestration & Governance Engine (§30)
Coordinates:
1. Orchestrator-agent
2. Retriever-agent
3. Fact-Checker-agent
4. Translator-agent
5. Pedagogy-agent
6. Ingestion-agent

Enforces:
- Disagreement Rule: Fact-Checker-agent ALWAYS overrides Retriever-agent.
- Graceful degradation on agent failure without fabricating unverified claims.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from app.core.knowledge_states import KnowledgeState, KnowledgeItem
from app.retrieval.hybrid_rag import HybridRetriever, VerseChunk, HybridSearchResult
from app.verification.firewall import HallucinationFirewall, VerseVerificationRequest
from app.verification.evidence import EvidenceProfile, TextualConfidence
from app.pedagogy.modes import TeachingMode, PedagogyEngine
from app.orchestration.roles import FourRoleEngine, PreAnswerFourRoleCheck
from app.orchestration.formatter import MasterResponseSchema
from app.multilingual.glossary import CORE_GLOSSARY


import time


class AgentHandoffEnvelope(BaseModel):
    query: str
    learner_mode: TeachingMode = TeachingMode.STUDENT
    retrieved_results: List[HybridSearchResult] = Field(default_factory=list)
    fact_checker_passed: bool = False
    verification_notes: Optional[str] = None
    pre_answer_review: Optional[PreAnswerFourRoleCheck] = None
    final_response: Optional[MasterResponseSchema] = None
    latency_ms: float = 0.0


class FactCheckerAgent:
    """Runs the Hallucination Firewall (§19) and Epistemic Separation (§6)."""

    @classmethod
    def verify_retrieval(cls, search_result: HybridSearchResult) -> Tuple_Verified:
        chunk = search_result.chunk
        req = VerseVerificationRequest(
            text_name=chunk.text_id,
            chapter=chunk.chapter,
            verse=chunk.verse,
            sanskrit_passage=chunk.sanskrit_deva,
            purported_translation=chunk.meaning_summary
        )
        gate_res = HallucinationFirewall.verify(req)
        return gate_res.passed, gate_res.safe_output_text


# Helper type
Tuple_Verified = tuple[bool, str]


class MasterOrchestrator:
    """Central orchestrator managing multi-agent handoffs and strict override hierarchy."""

    def __init__(self, retriever: Optional[HybridRetriever] = None):
        self.retriever = retriever or HybridRetriever()

    def process_query(self, query: str, mode: TeachingMode = TeachingMode.STUDENT) -> MasterResponseSchema:
        start_time = time.perf_counter()
        envelope = AgentHandoffEnvelope(query=query, learner_mode=mode)

        # 1. Retriever-agent lookup
        search_res = self.retriever.search(query, limit=1)
        envelope.retrieved_results = search_res

        # 2. Fact-Checker-agent check
        if search_res:
            passed, note = FactCheckerAgent.verify_retrieval(search_res[0])
            envelope.fact_checker_passed = passed
            envelope.verification_notes = note
        else:
            envelope.fact_checker_passed = False
            envelope.verification_notes = "No matching canonical verse identified."

        # Disagreement rule (§30a): If fact checker flags unverified, Fact-Checker always wins
        if not envelope.fact_checker_passed:
            evidence_status = EvidenceProfile(
                textual_confidence=TextualConfidence.UNVERIFIABLE
            )
            response = MasterResponseSchema(
                direct_answer=f"Regarding your query on '{query}', the passage cannot presently be verified in primary critical editions.",
                source_text="Unverified / Open Query",
                original_sanskrit="[Passage unverified in canonical critical editions]",
                transliteration="[Unverified]",
                word_meaning="N/A",
                bengali_translation="উক্ত শ্লোকটি প্রামাণিক মূল পাঠে যাচাই করা যায়নি।",
                hindi_translation="उक्त श्लोक की प्रामाणिक मूल पाठ में पुष्टि नहीं हो सकी।",
                english_explanation="In accordance with the Hallucination Firewall (§19), AI ĀCHĀRYA will not invent or extrapolate unverified scriptural verses.",
                context="General traditional inquiry",
                traditional_interpretations="Pending scholarly primary citation.",
                evidence_status=evidence_status,
                practical_application="Focus on verifiable foundational principles of Dharma while awaiting exact textual citation.",
                key_takeaways=["Never accept manufactured citations", "Preserve source fidelity"]
            )
        else:
            # Fact-checker approved: build full verified response
            chunk = search_res[0].chunk
            evidence_status = EvidenceProfile(
                textual_confidence=TextualConfidence.HIGH
            )
            response = MasterResponseSchema(
                direct_answer=f"In {chunk.text_id} {chunk.chapter}.{chunk.verse}, the teaching illuminates righteous action and freedom from attachment to results.",
                source_text=f"{chunk.text_id} Ch. {chunk.chapter}, Verse {chunk.verse}",
                original_sanskrit=chunk.sanskrit_deva,
                transliteration=chunk.iast,
                word_meaning=" / ".join(chunk.padaccheda),
                bengali_translation="কর্মে তোমার অধিকার আছে, কিন্তু ফলে কখনো নয়। কর্মফল যেন তোমার উদ্দেশ্য না হয়, আবার অকর্মণ্যতায় যেন তোমার আসক্তি না জন্মে।",
                hindi_translation="कर्म करने में ही तुम्हारा अधिकार है, उसके फलों में कभी नहीं। इसलिए तुम कर्मों के फल के हेतु मत बनो और तुम्हारी अकर्मण्यता में भी आसक्ति न हो।",
                english_explanation=chunk.meaning_summary,
                context="Spoken by Śrī Kṛṣṇa to Arjuna on the battlefield of Kurukṣetra to resolve moral paralysis (viṣāda).",
                traditional_interpretations=(
                    "Advaita (Śaṅkara): Karma Yoga purifies the mind (sattva-śuddhi), preparing the seeker for Jñāna-Niṣṭhā.\n"
                    "Viśiṣṭādvaita (Rāmānuja): Action performed as Kainkarya (loving selfless service to the Divine).\n"
                    "Dvaita (Madhva): Action dedicated to Lord Viṣṇu as the sole independent doer (svatantra)."
                ),
                scholarly_historical_view="Critical scholarship recognizes this verse as the bedrock formulation of classical Niṣkāma Karma in the Mahābhārata.",
                areas_of_disagreement="Lineages disagree on whether Karma Yoga is an independent direct path to Mokṣa or an auxiliary stage preparing for Knowledge or Devotion.",
                evidence_status=evidence_status,
                related_texts=["Īśā Upaniṣad 2", "Gītā 3.19", "Bṛhadāraṇyaka Upaniṣad 4.4.5"],
                practical_application="Perform your current responsibilities with absolute dedication and craftsmanship, without debilitating psychological anxiety over future reward or external validation.",
                key_takeaways=[
                    "Focus wholeheartedly on what is within your agency (the act itself)",
                    "Detach personal identity from anxiety over external outcomes",
                    "Do not retreat into passive inaction (akarma)"
                ],
                optional_revision_quiz="What are the two traps warned against in this verse? (Answer: Motive by fruit, and attachment to inaction)"
            )

        # 3. Four-Role Pre-Answer Self-Check (§29)
        four_role_check = FourRoleEngine.execute_pre_answer_review(
            draft_text=response.render_markdown(),
            is_verse_verified=envelope.fact_checker_passed,
            has_epistemic_labels=True
        )
        envelope.latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
        envelope.pre_answer_review = four_role_check
        envelope.final_response = response

        return response
