"""
FastAPI Application for AI ĀCHĀRYA
Exposes RESTful endpoints for querying, daily gurukula, verification, ingestion, and 64 Kalā.
"""

from fastapi import FastAPI, HTTPException, Body
from typing import Optional, Dict, Any
from app import __version__, __app_name__
from app.pedagogy.modes import TeachingMode
from app.pedagogy.daily_gurukula import DailyGurukulaService, DailyMicroCurriculum
from app.retrieval.hybrid_rag import HybridRetriever, VerseChunk
from app.orchestration.multi_agent import MasterOrchestrator
from app.verification.firewall import HallucinationFirewall, VerseVerificationRequest, VerificationGateResult
from app.kala.engine_64 import KalaEngine, KalaArt
from app.orchestration.quantum_verdict import QuantumTechnicalVerdict
from app.ingestion.pipeline import IngestionPipeline, IngestionBatchReport
from app.pedagogy.practical_systems import PracticalSystemsEngine, SystemDiscipline, ConsultationMode

app = FastAPI(
    title=__app_name__,
    description="Sanātana Jñāna, Śāstra, Saṃskṛti & Lifelong Learning Engine (v3.0)",
    version=__version__,
)

# Seed the in-memory retriever with canonical primary texts
retriever = HybridRetriever()
retriever.add_verse(
    VerseChunk(
        chunk_id="CHK_BG_2_47",
        text_id="BG",
        chapter="2",
        verse="47",
        canonical_id="BG_2_47",
        sanskrit_deva="कर्मण्येवाधिकारस्ते मा फलेषु कदाचन। मा कर्मफलहेतुर्भूर्मा ते सङ्गोऽस्त्वकर्मणि॥",
        iast="karmaṇyevādhikāraste mā phaleṣu kadācana | mā karmaphalaheturbhūrmā te saṅgo'stvakarmaṇi ||",
        padaccheda=["karmaṇi", "eva", "adhikāraḥ", "te", "mā", "phaleṣu", "kadācana"],
        meaning_summary="You have right only to work, never to its fruits; let not fruits be your motive, nor attachment be to inaction.",
        commentary_pointers=["Advaita (Śaṅkarācārya)", "Viśiṣṭādvaita (Rāmānujācārya)", "Dvaita (Madhvācārya)"]
    )
)
retriever.add_verse(
    VerseChunk(
        chunk_id="CHK_BG_2_48",
        text_id="BG",
        chapter="2",
        verse="48",
        canonical_id="BG_2_48",
        sanskrit_deva="योगस्थः कुरु कर्माणि सङ्गं त्यक्त्वा धनञ्जय। सिद्ध्यसिद्ध्योः समो भूत्वा समत्वं योग उच्यते॥",
        iast="yogasthaḥ kuru karmāṇi saṅgaṃ tyaktvā dhanañjaya | siddhyasiddhyoḥ samo bhūtvā samatvaṃ yoga ucyate ||",
        padaccheda=["yogasthaḥ", "kuru", "karmāṇi", "saṅgam", "tyaktvā", "dhanañjaya"],
        meaning_summary="Perform action being steadfast in Yoga, abandoning attachment, balanced in success and failure. Equanimity is called Yoga.",
        commentary_pointers=["Advaita (Śaṅkarācārya)", "Viśiṣṭādvaita (Rāmānujācārya)"]
    )
)
orchestrator = MasterOrchestrator(retriever=retriever)


@app.get("/health")
def health_check() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "app": __app_name__,
        "version": __version__,
        "canonical_coverage": "Vedas, Upaniṣads, Gītā, Itihāsa, Purāṇas, Darśanas, 64 Kalā"
    }


@app.post("/query")
def process_query(
    query: str = Body(..., embed=True),
    mode: TeachingMode = Body(TeachingMode.STUDENT, embed=True)
) -> Dict[str, Any]:
    """Processes queries through Multi-Agent Orchestration, Fact-Checker, and Four-Role pre-checks."""
    response = orchestrator.process_query(query=query, mode=mode)
    return {
        "query": query,
        "mode": mode.value,
        "structured_response": response.model_dump(),
        "rendered_markdown": response.render_markdown()
    }


@app.get("/daily-gurukula")
def get_daily_gurukula(day: int = 1, mode: TeachingMode = TeachingMode.STUDENT) -> DailyMicroCurriculum:
    """Returns the 7-element daily micro-curriculum (§21)."""
    return DailyGurukulaService.generate_lesson(day=day, mode=mode)


@app.post("/verify-verse")
def verify_verse(req: VerseVerificationRequest) -> VerificationGateResult:
    """Explicit Hallucination Firewall verification endpoint (§19)."""
    return HallucinationFirewall.verify(req)


@app.get("/kala/{number}")
def get_kala(number: int) -> KalaArt:
    """Retrieves 64 Kalā art details (§18)."""
    art = KalaEngine.get_by_number(number)
    if not art:
        raise HTTPException(status_code=404, detail=f"Kalā #{number} not found in classical registry.")
    return art


@app.get("/quantum-verdict")
def get_quantum_verdict() -> QuantumTechnicalVerdict:
    """Standing technical verdict on Quantum Computing and QML (§33)."""
    return QuantumTechnicalVerdict.get_standing_verdict()


@app.post("/practical-consultation")
def practical_consultation(
    discipline: SystemDiscipline = Body(..., embed=True),
    mode: ConsultationMode = Body(..., embed=True),
    inquiry_text: str = Body(..., embed=True)
) -> Dict[str, Any]:
    """Evaluates applied Āyurveda, Yoga, or Jyotiṣa queries with mandatory disclaimers (§22)."""
    eval_res = PracticalSystemsEngine.evaluate_request(
        discipline=discipline,
        mode=mode,
        traditional_text=inquiry_text,
        has_clinical_trials=False
    )
    return eval_res.model_dump()
