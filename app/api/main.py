"""
FastAPI Application for AI ĀCHĀRYA
Exposes RESTful endpoints for querying, daily gurukula, verification, ingestion, and 64 Kalā.
"""

from fastapi import FastAPI, HTTPException, Body, Response
from typing import Optional, Dict, Any, List
from app import __version__, __app_name__
from app.reporting import ExportFormat, ExportManager, AudioLanguage, AudioPacing
from app.intelligence import StrategicSemioticsEngine, MultiOpticStrategicVerdict
from app.pedagogy.modes import TeachingMode
from app.pedagogy.daily_gurukula import DailyGurukulaService, DailyMicroCurriculum
from app.retrieval.hybrid_rag import HybridRetriever, VerseChunk
from app.orchestration.multi_agent import MasterOrchestrator
from app.verification.firewall import HallucinationFirewall, VerseVerificationRequest, VerificationGateResult
from app.kala.engine_64 import KalaEngine, KalaArt
from app.orchestration.quantum_verdict import QuantumTechnicalVerdict
from app.ingestion.pipeline import IngestionPipeline, IngestionBatchReport
from app.pedagogy.practical_systems import PracticalSystemsEngine, SystemDiscipline, ConsultationMode
from app.civilization import (
    CivilizationalEngine,
    SthapatyaArchitectureEngine,
    HistoricalAeronauticsAuditEngine
)
from app.culture import CultureEngine
from app.verification.propaganda_detector import (
    PropagandaDetector,
    DistortionVector,
    ForensicStratumLevel,
    StratifiedTierScore
)
from app.verification.vivada_nirnaya import VivadaNirnayaEngine, ChronologicalHypothesis, TextualStrataLevel, ArchaeologicalStratumMatch
from app.pedagogy.cognitive_mastery import CognitiveMasteryEngine, ReviewGrade
from app.intelligence.micro_signals import MicroSignalForensicParser
from app.verification.mimamsa import MimamsaGrayzoneResolver
from app.intelligence.cv_bridge import ComputerVisionOpticalBridge, OpticalEvidenceLevel
from app.intelligence.learning_ledger import CandidateEpistemicLedger, InsightDomain
from app.sanskrit.phonetics_engine import PaninianPhoneticsEngine
from app.verification.organicism import VedicCosmicOrganicismEngine
from app.pedagogy.vedanta_prakarana import AtmabodhaPrakaranaEngine
from app.intelligence.cyber_defense import CognitiveCybersecurityEngine
from app.verification.siddhi_boundary import PatanjaliSiddhiBoundaryEngine
from app.pedagogy.prenatal_and_trataka import PrenatalAuditorySafetyEngine, TratakaMeditationEngine
from app.canon.mula_ingestion import MulaPathaEngine, TriLayerVerse
from app.intelligence.promotion_governance import EpistemicPromotionEngine, ScholarSignatureType
from app.intelligence.cv_pipeline import CvOpticalPipelineEngine
from app.core.knowledge_states import KnowledgeState
from app.video.storyboard import VideoStoryboardDirector, VideoFormat
from app.video.generate import FacelessVideoProductionPipeline


civ_engine = CivilizationalEngine()
culture_engine = CultureEngine()
propaganda_detector = PropagandaDetector()
arbitration_engine = VivadaNirnayaEngine()
cognitive_engine = CognitiveMasteryEngine()
sthapatya_engine = SthapatyaArchitectureEngine()
aeronautics_engine = HistoricalAeronauticsAuditEngine()

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
orchestrator = MasterOrchestrator(
    retriever=retriever,
    civilization_engine=civ_engine,
    culture_engine=culture_engine,
    vivada_engine=arbitration_engine,
    propaganda_detector=propaganda_detector,
    cognitive_engine=cognitive_engine,
    sthapatya_engine=sthapatya_engine,
    aeronautics_engine=aeronautics_engine
)


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
    mode: TeachingMode = Body(TeachingMode.STUDENT, embed=True),
    export_formats: Optional[List[ExportFormat]] = Body(None, embed=True),
    audio_lang: AudioLanguage = Body(AudioLanguage.ENGLISH, embed=True)
) -> Dict[str, Any]:
    """Processes queries through Multi-Agent Orchestration, Fact-Checker, and Four-Role pre-checks."""
    response = orchestrator.process_query(query=query, mode=mode)
    raw_markdown = response.render_markdown()
    decorated_markdown = ExportManager.decorate_markdown_with_audio_decks(raw_markdown)

    result_payload: Dict[str, Any] = {
        "query": query,
        "mode": mode.value,
        "structured_response": response.model_dump(),
        "rendered_markdown": decorated_markdown,
    }

    if export_formats:
        exports_data: Dict[str, Any] = {}
        for fmt in export_formats:
            if fmt == ExportFormat.ALL:
                all_res = ExportManager.generate_all_exports(response, query=query, audio_lang=audio_lang)
                for k, v in all_res.items():
                    exports_data[k.value] = {
                        "file_name": v.file_name,
                        "mime_type": v.mime_type,
                        "sha256": v.sha256_hash,
                        "content_text": v.content_text,
                        "has_bytes": v.content_bytes is not None
                    }
            else:
                res = ExportManager.generate_single_export(response, export_format=fmt, query=query, audio_lang=audio_lang)
                exports_data[fmt.value] = {
                    "file_name": res.file_name,
                    "mime_type": res.mime_type,
                    "sha256": res.sha256_hash,
                    "content_text": res.content_text,
                    "has_bytes": res.content_bytes is not None
                }
        result_payload["exports"] = exports_data

    return result_payload


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


@app.get("/civilization/entity/{name}")
def get_civilizational_entity(name: str) -> Dict[str, Any]:
    """Retrieves verified civilizational geography / Kṣetra records."""
    entity = civ_engine.lookup_ksetra(name)
    if not entity:
        raise HTTPException(status_code=404, detail=f"Civilizational entity '{name}' not found.")
    return {
        "entity_id": entity.entity_id,
        "name": entity.name,
        "category": entity.category,
        "ancient_names": entity.ancient_names,
        "coordinates": entity.coordinates,
        "historical_strata": [s.value for s in entity.historical_strata],
        "description": entity.description,
        "archaeological_sites": entity.archaeological_sites,
        "textual_references": entity.textual_references,
        "scientific_evidence": entity.scientific_evidence
    }


@app.get("/civilization/epigraph/{name}")
def get_epigraphic_record(name: str) -> Dict[str, Any]:
    """Retrieves verified lithic or copper-plate epigraphic records."""
    epi = civ_engine.lookup_epigraph(name)
    if not epi:
        raise HTTPException(status_code=404, detail=f"Epigraph '{name}' not found.")
    return {
        "record_id": epi.record_id,
        "title": epi.title,
        "ruler": epi.ruler,
        "dynasty": epi.dynasty,
        "approx_date": epi.approx_date,
        "findspot": epi.findspot,
        "script": epi.script,
        "language": epi.language,
        "key_historical_facts": epi.key_historical_facts,
        "epistemic_confidence": epi.epistemic_confidence,
        "source_citation": epi.source_citation
    }


@app.get("/civilization/material-science/{name}")
def get_material_science_record(name: str) -> Dict[str, Any]:
    """Retrieves verified indigenous material science & metallurgical innovations."""
    mat = civ_engine.lookup_material_science(name)
    if not mat:
        raise HTTPException(status_code=404, detail=f"Material science record '{name}' not found.")
    return {
        "tech_id": mat.tech_id,
        "domain": mat.domain,
        "innovation_name": mat.innovation_name,
        "approximate_origin_era": mat.approximate_origin_era,
        "primary_sites": mat.primary_sites,
        "physical_evidence_summary": mat.physical_evidence_summary,
        "global_significance": mat.global_significance,
        "primary_textual_sources": mat.primary_textual_sources
    }


from pydantic import BaseModel, Field


class StratumPayload(BaseModel):
    site_name: str
    stratum_name: str
    median_calibrated_bce: float
    uncertainty_years: float = 200.0
    material_match_quality: float = 0.8


class HypothesisPayload(BaseModel):
    name: str
    proponent_or_school: str = "Independent Scholar"
    proposed_date_bce: float
    target_strata_level: str = "JAYA_CORE"
    astronomy_raw_score: float = 0.5
    archaeology_raw_score: float = 0.5
    epigraphy_raw_score: float = 0.5
    linguistics_raw_score: float = 0.5
    hermeneutics_raw_score: float = 0.5
    cherry_pick_penalty: float = 0.0
    verified_strata: list[StratumPayload] = Field(default_factory=list)
    summary_claim: str = ""


class PropagandaAnalysisRequest(BaseModel):
    claim_text: str
    evidence_scores: dict[str, float] = Field(default_factory=dict)


class PancangaRequest(BaseModel):
    solar_deg: float
    lunar_deg: float


@app.post("/culture/pancanga")
def compute_pancanga(req: PancangaRequest) -> Dict[str, Any]:
    """Computes the 5 temporal limbs of Pañcāṅga and seasonal health regimen from solar/lunar longitudes."""
    res = culture_engine.compute_pancanga(solar_deg=req.solar_deg, lunar_deg=req.lunar_deg)
    return {
        "solar_longitude_deg": res.solar_longitude_deg,
        "lunar_longitude_deg": res.lunar_longitude_deg,
        "tithi": f"{res.tithi_name} ({res.paksha}, #{res.tithi_number})",
        "nakshatra": f"{res.nakshatra_name} (#{res.nakshatra_number})",
        "yoga": f"{res.yoga_name} (#{res.yoga_number})",
        "karana": res.karana_name,
        "season": res.associated_season.value,
        "seasonal_regimen": res.seasonal_regimen
    }


@app.get("/culture/samskara/{name}")
def get_samskara(name: str) -> Dict[str, Any]:
    """Retrieves developmental, psychological, and spiritual records for Ṣoḍaśa Saṃskāras."""
    sam = culture_engine.lookup_samskara(name)
    if not sam:
        raise HTTPException(status_code=404, detail=f"Saṃskāra '{name}' not found.")
    return {
        "samskara_id": sam.samskara_id,
        "canonical_name": sam.canonical_name,
        "transliteration": sam.transliteration,
        "stage": sam.stage.value,
        "traditional_timing": sam.traditional_timing,
        "psychological_purpose": sam.psychological_purpose,
        "spiritual_ontological_core": sam.spiritual_ontological_core,
        "historical_mutable_accretions": sam.historical_mutable_accretions,
        "primary_textual_sources": sam.primary_textual_sources
    }


@app.post("/verification/propaganda-analysis")
def analyze_propaganda(req: PropagandaAnalysisRequest) -> Dict[str, Any]:
    """Analyzes text for 4 ideological distortion vectors and runs the ALEDT tensor."""
    bias = propaganda_detector.detect_bias(req.claim_text)
    scores = req.evidence_scores or {"epigraphy": 0.5, "textual_criticism": 0.5, "archaeology": 0.5, "astronomy_science": 0.5}
    satya_score, verdict, diagnostics = propaganda_detector.compute_aledt_score(scores, bias)
    return {
        "claim_text": req.claim_text,
        "bias_vectors": {
            "colonial_eurocentric": bias.colonial_vector,
            "marxist_reductionist": bias.marxist_vector,
            "theological_iconoclastic": bias.theological_vector,
            "pseudoscience_anachronism": bias.pseudoscience_vector
        },
        "max_distortion": bias.max_distortion,
        "satya_score": satya_score,
        "verdict": verdict,
        "diagnostics": diagnostics,
        "distortion_proofs": [
            {
                "vector": p.vector.value,
                "target_clause": p.target_clause,
                "identified_fallacy": p.identified_fallacy,
                "counter_pramana_source": p.counter_pramana_source
            }
            for p in bias.proofs
        ]
    }


class TierScorePayload(BaseModel):
    tier: str
    factual_reality: float
    propaganda_distortion: float
    causal_attribution_valid: bool
    dimension_name: str
    evidence_justification: str


class StratifiedForensicRequest(BaseModel):
    tiers: list[TierScorePayload]
    gamma_causal: Optional[float] = None


@app.post("/verification/stratified-forensic-matrix")
def analyze_stratified_forensic_matrix(req: StratifiedForensicRequest) -> Dict[str, Any]:
    """Computes 5-tier stratified reality and non-compensatory multiplicative causal veto gate."""
    converted_tiers = [
        StratifiedTierScore(
            tier=ForensicStratumLevel[t.tier],
            factual_reality=t.factual_reality,
            propaganda_distortion=t.propaganda_distortion,
            causal_attribution_valid=t.causal_attribution_valid,
            dimension_name=t.dimension_name,
            evidence_justification=t.evidence_justification
        )
        for t in req.tiers
    ]
    rep = propaganda_detector.compute_stratified_forensic_matrix(converted_tiers, gamma_causal=req.gamma_causal)
    return {
        "composite_factual_reality": rep.composite_factual_reality,
        "prophetic_causal_reality": rep.prophetic_causal_reality,
        "composite_distortion": rep.composite_distortion,
        "gamma_causal_veto": rep.gamma_causal_veto,
        "summary_verdict": rep.summary_verdict,
        "seeker_guidance": rep.seeker_guidance
    }


class ArbitrationResultModel(BaseModel):
    hypothesis_name: str
    proponent_or_school: str
    proposed_date_bce: float
    target_strata_level: str
    posterior_probability: float
    epistemic_status: str
    strongest_pillar: str
    fatal_bottleneck: str
    anchor_decay_multiplier: float
    delta_t_astro_multiplier: float
    stratified_reality_assessment: str


@app.post("/verification/vivada-nirnaya")
def execute_vivada_nirnaya(hypotheses_payload: list[HypothesisPayload]) -> list[ArbitrationResultModel]:
    """Runs 5D orthogonal epistemic arbitration on competing historical/chronological hypotheses."""
    hyp_list = []
    for h in hypotheses_payload:
        strata = []
        for s in h.verified_strata:
            strata.append(
                ArchaeologicalStratumMatch(
                    site_name=s.site_name,
                    stratum_name=s.stratum_name,
                    median_calibrated_bce=s.median_calibrated_bce,
                    uncertainty_years=s.uncertainty_years,
                    material_match_quality=s.material_match_quality
                )
            )
        hyp_list.append(
            ChronologicalHypothesis(
                name=h.name,
                proponent_or_school=h.proponent_or_school,
                proposed_date_bce=h.proposed_date_bce,
                target_strata_level=TextualStrataLevel[h.target_strata_level],
                astronomy_raw_score=h.astronomy_raw_score,
                archaeology_raw_score=h.archaeology_raw_score,
                epigraphy_raw_score=h.epigraphy_raw_score,
                linguistics_raw_score=h.linguistics_raw_score,
                hermeneutics_raw_score=h.hermeneutics_raw_score,
                cherry_pick_penalty=h.cherry_pick_penalty,
                verified_strata=strata,
                summary_claim=h.summary_claim
            )
        )
    results = arbitration_engine.arbitrate(hyp_list)
    return [
        ArbitrationResultModel(
            hypothesis_name=r.hypothesis_name,
            proponent_or_school=r.proponent_or_school,
            proposed_date_bce=r.proposed_date_bce,
            target_strata_level=r.target_strata_level,
            posterior_probability=r.posterior_probability,
            epistemic_status=r.epistemic_status,
            strongest_pillar=r.strongest_pillar,
            fatal_bottleneck=r.fatal_bottleneck,
            anchor_decay_multiplier=r.anchor_decay_multiplier,
            delta_t_astro_multiplier=r.delta_t_astro_multiplier,
            stratified_reality_assessment=r.stratified_reality_assessment
        )
        for r in results
    ]


class FSRSScheduleRequest(BaseModel):
    topic_id: str
    elapsed_days: float
    current_stability: float
    difficulty: float
    grade: Optional[int] = 3
    target_r: float = 0.90


class CognitiveLoadRequest(BaseModel):
    concept_or_verse: str
    student_fatigue: float = 0.0
    pedagogical_mode: str = "Student"


class CognitiveClaimRequest(BaseModel):
    claim_text: str


@app.post("/pedagogy/cognitive-schedule")
def compute_cognitive_schedule(req: FSRSScheduleRequest) -> Dict[str, Any]:
    """Computes FSRS retrievability, new memory stability, and recommended interval in days."""
    try:
        grade = ReviewGrade(req.grade) if req.grade else ReviewGrade.GOOD
    except ValueError:
        grade = ReviewGrade.GOOD
    sched = cognitive_engine.update_fsrs_schedule(
        topic_id=req.topic_id,
        elapsed_days=req.elapsed_days,
        current_stability=req.current_stability,
        difficulty=req.difficulty,
        grade=grade,
        target_r=req.target_r
    )
    return {
        "topic_id": sched.topic_id,
        "new_stability_days": sched.stability,
        "difficulty": sched.difficulty,
        "retrievability": sched.retrievability,
        "recommended_interval_days": sched.recommended_interval_days,
        "next_due_date_days": sched.next_due_date_days
    }


@app.post("/pedagogy/cognitive-load")
def evaluate_cognitive_load(req: CognitiveLoadRequest) -> Dict[str, Any]:
    """Computes Sweller's Cognitive Load Index (L_cog) and prescribes dynamic Anvaya scaffolding."""
    res = cognitive_engine.evaluate_cognitive_load(
        concept_or_verse=req.concept_or_verse,
        student_fatigue=req.student_fatigue,
        pedagogical_mode=req.pedagogical_mode
    )
    return {
        "concept_or_verse": res.concept_or_verse,
        "raw_complexity": res.raw_complexity,
        "student_fatigue": res.student_fatigue,
        "cognitive_load_index": res.cognitive_load_index,
        "fragmentation_required": res.fragmentation_required,
        "pedagogical_mode": res.pedagogical_mode,
        "scaffolding_instruction": res.scaffolding_instruction
    }


@app.get("/pedagogy/student-routine")
def get_student_focus_protocol() -> Dict[str, Any]:
    """Returns the evidence-based 20-minute daily Gurukula Focus Protocol."""
    protocol = cognitive_engine.generate_gurukula_focus_protocol()
    return {
        "protocol_name": protocol.protocol_name,
        "total_minutes": protocol.total_minutes,
        "steps": protocol.steps,
        "physiological_rationale": protocol.physiological_rationale,
        "cultural_context": protocol.cultural_context,
        "anti_fear_grounding": protocol.anti_fear_grounding
    }


@app.post("/pedagogy/evaluate-cognitive-claim")
def evaluate_cognitive_claim(req: CognitiveClaimRequest) -> Dict[str, Any]:
    """Evaluates educational or brain-optimization claims against empirical neuroscience and Śāstra."""
    report = cognitive_engine.evaluate_cognitive_claim(req.claim_text)
    return {
        "claim_text": report.claim_text,
        "is_pseudoscientific": report.is_pseudoscientific,
        "confidence": report.confidence,
        "detected_fallacies": report.detected_fallacies,
        "medical_scientific_verdict": report.medical_scientific_verdict,
        "shastric_verdict": report.shastric_verdict,
        "safe_alternative_recommendation": report.safe_alternative_recommendation
    }


class QuarryingRequest(BaseModel):
    site_name: str = "Ellora Cave 16 Kailasa"
    net_volume_m3: float = 85000.0
    rock_density_kg_m3: float = 2850.0
    project_years: float = 25.0
    days_per_year: float = 300.0
    mason_daily_cut_m3: float = 0.25


class InclineRequest(BaseModel):
    structure_name: str = "Thanjavur Brihadisvara Vimāna Shikhara"
    monolith_mass_kg: float = 80000.0
    ramp_slope_deg: float = 4.0
    friction_coeff: float = 0.08


class AeronauticsAuditRequest(BaseModel):
    craft_name: Optional[str] = None
    claim_text: Optional[str] = None


@app.post("/civilization/sthapatya/quarrying-feasibility")
def get_quarrying_feasibility(req: QuarryingRequest) -> Dict[str, Any]:
    """Calculates basalt volumetric rock-cut kinematics and labor logistics for monolithic temples."""
    res = sthapatya_engine.calculate_quarrying_feasibility(
        site_name=req.site_name,
        net_volume_m3=req.net_volume_m3,
        rock_density_kg_m3=req.rock_density_kg_m3,
        project_years=req.project_years,
        days_per_year=req.days_per_year,
        mason_daily_cut_m3=req.mason_daily_cut_m3
    )
    return {
        "site_name": res.site_name,
        "net_volume_m3": res.net_volume_m3,
        "net_mass_metric_tons": res.net_mass_metric_tons,
        "hydraulic_wedge_expansion_stress_mpa": res.hydraulic_wedge_expansion_stress_mpa,
        "rock_tensile_strength_mpa": res.rock_tensile_strength_mpa,
        "wedge_cleavage_feasible": res.wedge_cleavage_feasible,
        "daily_quarrying_rate_tons_per_day": res.daily_quarrying_rate_tons_per_day,
        "estimated_skilled_masons_required": res.estimated_skilled_masons_required,
        "estimated_general_laborers_required": res.estimated_general_laborers_required,
        "total_project_years": res.total_project_years,
        "primary_epigraphic_anchor": res.primary_epigraphic_anchor,
        "engineering_explanation": res.engineering_explanation
    }


@app.post("/civilization/sthapatya/incline-kinematics")
def get_incline_kinematics(req: InclineRequest) -> Dict[str, Any]:
    """Calculates inclined plane mechanics, rolling friction, and tractive force for megalith transport."""
    res = sthapatya_engine.calculate_incline_kinematics(
        structure_name=req.structure_name,
        monolith_mass_kg=req.monolith_mass_kg,
        ramp_slope_deg=req.ramp_slope_deg,
        friction_coeff=req.friction_coeff
    )
    return {
        "structure_name": res.structure_name,
        "monolith_mass_kg": res.monolith_mass_kg,
        "ramp_slope_angle_deg": res.ramp_slope_angle_deg,
        "friction_coefficient": res.friction_coefficient,
        "tractive_pulling_force_newtons": res.tractive_pulling_force_newtons,
        "required_draft_oxen_pairs": res.required_draft_oxen_pairs,
        "required_human_haulers": res.required_human_haulers,
        "mechanical_advantage_ratio": res.mechanical_advantage_ratio,
        "engineering_explanation": res.engineering_explanation
    }


@app.post("/civilization/aeronautics/audit")
def audit_historical_aeronautics(req: AeronauticsAuditRequest) -> Dict[str, Any]:
    """Audits aeronautical and Vimāna claims against the 1974 IISc study and Hermeneutic Tripartition."""
    report = aeronautics_engine.get_iisc_1974_study_report()
    craft_res = None
    if req.craft_name:
        craft_res = aeronautics_engine.audit_craft(req.craft_name)
    stratum_res = None
    if req.claim_text:
        stratum_res = aeronautics_engine.evaluate_hermeneutic_stratum(req.claim_text).value

    craft_dict = None
    if craft_res:
        craft_dict = {
            "craft_name": craft_res.craft_name,
            "textual_source": craft_res.textual_source,
            "historical_provenance_date": craft_res.historical_provenance_date,
            "author_or_medium": craft_res.author_or_medium,
            "lift_to_drag_ratio": craft_res.lift_to_drag_ratio,
            "is_aerodynamically_viable": craft_res.is_aerodynamically_viable,
            "thermodynamic_physical_violations": craft_res.thermodynamic_physical_violations,
            "iisc_1974_verdict": craft_res.iisc_1974_verdict
        }

    return {
        "study_title": report.study_title,
        "research_institution": report.research_institution,
        "publication_year": report.publication_year,
        "manuscript_investigation_findings": report.manuscript_investigation_findings,
        "craft_audit": craft_dict,
        "hermeneutic_stratum": stratum_res,
        "hermeneutic_separation_verdict": report.hermeneutic_separation_verdict,
        "seeker_guidance": report.seeker_guidance
    }


@app.get("/export/download/html")
def download_html(query: str = "BG 2.47") -> Response:
    """Streams an on-demand, self-contained interactive HTML dashboard attachment."""
    resp = orchestrator.process_query(query=query)
    export_res = ExportManager.generate_single_export(resp, ExportFormat.HTML, query=query)
    return Response(
        content=export_res.content_text,
        media_type=export_res.mime_type,
        headers={"Content-Disposition": f'attachment; filename="{export_res.file_name}"'}
    )


@app.get("/export/download/markdown")
def download_markdown(query: str = "BG 2.47") -> Response:
    """Streams an on-demand forensic markdown dossier with SHA-256 integrity hash."""
    resp = orchestrator.process_query(query=query)
    export_res = ExportManager.generate_single_export(resp, ExportFormat.MARKDOWN, query=query)
    return Response(
        content=export_res.content_text,
        media_type=export_res.mime_type,
        headers={"Content-Disposition": f'attachment; filename="{export_res.file_name}"'}
    )


@app.get("/export/download/pdf")
def download_pdf(query: str = "BG 2.47") -> Response:
    """Streams an on-demand executive PDF report binary."""
    resp = orchestrator.process_query(query=query)
    export_res = ExportManager.generate_single_export(resp, ExportFormat.PDF, query=query)
    return Response(
        content=export_res.content_bytes,
        media_type=export_res.mime_type,
        headers={"Content-Disposition": f'attachment; filename="{export_res.file_name}"'}
    )


@app.get("/export/audio")
def stream_audio(
    query: str = "BG 2.47",
    lang: AudioLanguage = AudioLanguage.ENGLISH,
    pacing: AudioPacing = AudioPacing.STANDARD
) -> Response:
    """Streams an on-demand synthesized audio wave file for Sanskrit/Bengali/Hindi/English."""
    resp = orchestrator.process_query(query=query)
    export_res = ExportManager.generate_single_export(
        resp, ExportFormat.AUDIO, query=query, audio_lang=lang, audio_pacing=pacing
    )
    return Response(
        content=export_res.content_bytes,
        media_type=export_res.mime_type,
        headers={"Content-Disposition": f'inline; filename="{export_res.file_name}"'}
    )


@app.post("/intelligence/strategic-semiotic-audit")
def strategic_semiotic_audit(
    topic: str = Body(..., embed=True),
    text_payload: str = Body(..., embed=True),
    has_cv_keyframe_data: bool = Body(False, embed=True),
    cv_dominant_hex: Optional[str] = Body(None, embed=True)
) -> Dict[str, Any]:
    """Audits events across 7 strategic thinker lenses with the Anti-Hallucination Visual Gate."""
    verdict = StrategicSemioticsEngine.evaluate_strategic_topic(
        topic=topic,
        text_payload=text_payload,
        has_cv_keyframe_data=has_cv_keyframe_data,
        cv_dominant_hex=cv_dominant_hex
    )
    return verdict.model_dump()


@app.post("/intelligence/micro-signals")
def analyze_micro_signals(text_payload: str = Body(..., embed=True)) -> Dict[str, Any]:
    """Forensically analyzes covert linguistic bias, agency inversion, and asymmetric evidentiary demands."""
    report = MicroSignalForensicParser.analyze_text(text_payload)
    return {
        "total_signals_detected": report.total_signals_detected,
        "composite_manipulation_score": report.composite_manipulation_score,
        "dominant_manipulation_vector": report.dominant_manipulation_vector,
        "detected_signals": [
            {
                "category": s.category.value,
                "matched_phrase": s.matched_phrase,
                "forensic_critique": s.forensic_critique,
                "epistemic_impact": s.epistemic_impact,
                "severity_weight": s.severity_weight
            }
            for s in report.detected_signals
        ],
        "rebuttal_strategy": report.rebuttal_strategy,
        "is_compromised": report.is_compromised
    }


@app.post("/verification/mimamsa-grayzone")
def resolve_mimamsa_grayzone(
    claim_or_verse: str = Body(..., embed=True),
    declared_source: Optional[str] = Body(None, embed=True)
) -> Dict[str, Any]:
    """Arbitrates scriptural and cultural grayzones using 6 Mīmāṃsā canons and authority strata."""
    res = MimamsaGrayzoneResolver.resolve_grayzone(claim_or_verse=claim_or_verse, declared_source=declared_source)
    return {
        "disputed_topic": res.disputed_topic,
        "primary_stratum": res.primary_stratum.value,
        "stratum_authority_weight": res.stratum_authority_weight,
        "is_vidhi_binding": res.is_vidhi_binding,
        "is_arthavada_metaphor": res.is_arthavada_metaphor,
        "canon_evaluations": [
            {
                "canon": c.canon.value,
                "is_satisfied": c.is_satisfied,
                "confidence": c.confidence,
                "analysis": c.analysis
            }
            for c in res.canon_evaluations
        ],
        "overall_coherence_score": res.overall_coherence_score,
        "siddhanta_resolution": res.siddhanta_resolution,
        "is_scripturally_valid": res.is_scripturally_valid
    }


@app.post("/intelligence/cv-optical-audit")
def audit_cv_optical_assertions(
    text_claims: str = Body(..., embed=True),
    has_cv_keyframe: bool = Body(False, embed=True),
    keyframe_dominant_hex: Optional[str] = Body(None, embed=True),
    pose_symmetry_score: Optional[float] = Body(None, embed=True)
) -> Dict[str, Any]:
    """Audits visual claims, enforcing the Anti-Hallucination Visual Gate with optional CV verification."""
    level = OpticalEvidenceLevel.KEYFRAME_DOMINANT_HEX if has_cv_keyframe else OpticalEvidenceLevel.TEXT_ONLY_UNVERIFIED
    report = ComputerVisionOpticalBridge.audit_visual_assertions(
        text_claims=text_claims,
        evidence_level=level,
        keyframe_dominant_hex=keyframe_dominant_hex,
        pose_symmetry_score=pose_symmetry_score
    )
    return {
        "evidence_level": report.evidence_level.value,
        "is_hallucination_vetoed": report.is_hallucination_vetoed,
        "optical_integrity_score": report.optical_integrity_score,
        "detected_unverified_claims": report.detected_unverified_claims,
        "verified_visual_metrics": report.verified_visual_metrics,
        "audit_verdict": report.audit_verdict,
        "forensic_advice": report.forensic_advice
    }


@app.post("/intelligence/learning-ledger/record")
def record_learning_insight(
    topic: str = Body(..., embed=True),
    domain: InsightDomain = Body(InsightDomain.ARCHAEOLOGY_EPIGRAPHY, embed=True),
    learned_content: str = Body(..., embed=True),
    evidence_source: str = Body(..., embed=True)
) -> Dict[str, Any]:
    """Records a newly verified insight into the sandboxed candidate learning ledger."""
    item = CandidateEpistemicLedger.record_candidate_insight(
        topic=topic,
        domain=domain,
        learned_content=learned_content,
        evidence_source=evidence_source
    )
    return {
        "insight_id": item.insight_id,
        "topic": item.topic,
        "domain": item.domain.value,
        "knowledge_state": item.knowledge_state.name,
        "sha256_hash": item.sha256_hash,
        "status": "RECORDED_IN_C_CANDIDATE"
    }


@app.get("/intelligence/learning-ledger/query")
def query_learning_ledger(keyword: str = "Sinauli") -> List[Dict[str, Any]]:
    """Queries candidate insights from the sandboxed self-learning ledger."""
    results = CandidateEpistemicLedger.query_insights(keyword)
    return [
        {
            "insight_id": r.insight_id,
            "topic": r.topic,
            "domain": r.domain.value,
            "learned_content": r.learned_content,
            "evidence_source": r.evidence_source,
            "knowledge_state": r.knowledge_state.name,
            "is_promoted": r.is_promoted
        }
        for r in results
    ]


@app.get("/intelligence/learning-ledger/stats")
def get_learning_ledger_stats() -> Dict[str, Any]:
    """Returns statistics on active candidates and canonical isolation enforcement."""
    return CandidateEpistemicLedger.get_ledger_stats()


@app.post("/verification/chronology/rigveda-arbitration")
def execute_rigveda_chronology_arbitration(
    custom_hypotheses: Optional[list[HypothesisPayload]] = None
) -> list[ArbitrationResultModel]:
    """
    Runs multi-pillar Bayesian chronological arbitration across Ṛgvedic historical hypotheses.
    Defaults to the canonical 3-tier benchmarks: Sarasvatī Hydrological, Colonial Minimalist, and Bhirrana Antiquity.
    """
    if custom_hypotheses and len(custom_hypotheses) > 0:
        hyp_list = []
        for h in custom_hypotheses:
            strata = [
                ArchaeologicalStratumMatch(
                    site_name=s.site_name,
                    stratum_name=s.stratum_name,
                    median_calibrated_bce=s.median_calibrated_bce,
                    uncertainty_years=s.uncertainty_years,
                    material_match_quality=s.material_match_quality
                )
                for s in h.verified_strata
            ]
            hyp_list.append(
                ChronologicalHypothesis(
                    name=h.name,
                    proponent_or_school=h.proponent_or_school,
                    proposed_date_bce=h.proposed_date_bce,
                    target_strata_level=TextualStrataLevel[h.target_strata_level],
                    astronomy_raw_score=h.astronomy_raw_score,
                    archaeology_raw_score=h.archaeology_raw_score,
                    epigraphy_raw_score=h.epigraphy_raw_score,
                    linguistics_raw_score=h.linguistics_raw_score,
                    hermeneutics_raw_score=h.hermeneutics_raw_score,
                    cherry_pick_penalty=h.cherry_pick_penalty,
                    verified_strata=strata,
                    summary_claim=h.summary_claim
                )
            )
        results = arbitration_engine.arbitrate(hyp_list)
    else:
        results = arbitration_engine.arbitrate_rigveda_chronology()

    return [
        ArbitrationResultModel(
            hypothesis_name=r.hypothesis_name,
            proponent_or_school=r.proponent_or_school,
            proposed_date_bce=r.proposed_date_bce,
            target_strata_level=r.target_strata_level,
            posterior_probability=r.posterior_probability,
            epistemic_status=r.epistemic_status,
            strongest_pillar=r.strongest_pillar,
            fatal_bottleneck=r.fatal_bottleneck,
            anchor_decay_multiplier=r.anchor_decay_multiplier,
            delta_t_astro_multiplier=r.delta_t_astro_multiplier,
            stratified_reality_assessment=r.stratified_reality_assessment
        )
        for r in results
    ]


@app.post("/sanskrit/phonetics/niroshthya-audit")
def audit_niroshthya(
    text: str = Body(..., embed=True),
    strict_mode: bool = Body(True, embed=True)
) -> Dict[str, Any]:
    """
    Audits classical verse for the Niroṣṭhya constraint (composed without lip-contact / labials).
    Evaluates both Devanagari and IAST articulatory loci.
    """
    res = PaninianPhoneticsEngine.audit_niroshthya(text=text, strict_mode=strict_mode)
    return {
        "is_niroshthya": res.is_niroshthya,
        "total_characters": res.total_characters,
        "labial_count": res.labial_count,
        "detected_labial_symbols": res.detected_labial_symbols,
        "forensic_critique": res.forensic_critique,
        "stylistic_category": res.stylistic_category
    }


@app.post("/sanskrit/phonetics/citra-kavya-audit")
def audit_citra_kavya(
    text: str = Body(..., embed=True)
) -> Dict[str, Any]:
    """
    Audits Sanskrit verse for extreme Citra-kāvya constraints:
    Palindromic symmetry (Gatapratiyāgata), Ekākṣarī (single consonant), and Dvyakṣarī (two consonants).
    """
    res = PaninianPhoneticsEngine.audit_citra_kavya(text=text)
    return {
        "is_palindrome": res.is_palindrome,
        "distinct_consonants_count": res.distinct_consonants_count,
        "distinct_consonants": res.distinct_consonants,
        "is_ekaksari": res.is_ekaksari,
        "is_dvyaksari": res.is_dvyaksari,
        "pattern_name": res.pattern_name,
        "forensic_critique": res.forensic_critique
    }


@app.post("/verification/cosmic-organicism/audit")
def audit_cosmic_organicism(
    claim_text: str = Body(..., embed=True)
) -> Dict[str, Any]:
    """
    Audits claims regarding Puruṣa Sūkta (RV 10.90), Varna origins, and Vedic cosmic organicism.
    Evaluates functional somatic subsystems, Earth-feet Pratiṣṭhā sanctity, and Jaimini 1.3.3 invalidation.
    """
    res = VedicCosmicOrganicismEngine.audit_organicism_claim(claim_text)
    return {
        "is_organicism_aligned": res.is_organicism_aligned,
        "is_colonial_degradation_detected": res.is_colonial_degradation_detected,
        "is_birth_caste_conflation": res.is_birth_caste_conflation,
        "pratistha_sacred_foundation_verified": res.pratistha_sacred_foundation_verified,
        "earth_emanation_proof": res.earth_emanation_proof,
        "jaimini_sutra_invalidation_triggered": res.jaimini_sutra_invalidation_triggered,
        "subsystems_identified": res.subsystems_identified,
        "forensic_verdict": res.forensic_verdict,
        "hermeneutic_siddhanta": res.hermeneutic_siddhanta
    }


@app.post("/pedagogy/vedanta/atmabodha-analysis")
def analyze_atmabodha_pedagogy(
    inquiry_text: str = Body(..., embed=True)
) -> Dict[str, Any]:
    """
    Renders systematic Advaita Vedānta Prakaraṇa pedagogy based on Ādi Śaṅkarācārya's Ātmabodha.
    Guides inquiries through the 6-stage realization pipeline (Adhikārī, Adhyāsa, Apavāda, Sākṣī, Mahāvākya, Jīvanmukti).
    """
    res = AtmabodhaPrakaranaEngine.analyze_inquiry(inquiry_text)
    return {
        "inquiry_text": res.inquiry_text,
        "target_stage": res.target_stage.value,
        "primary_verse_citation": res.primary_verse_citation,
        "epistemic_principle": res.epistemic_principle,
        "pedagogical_analogy": res.pedagogical_analogy,
        "upadhi_analysis": res.upadhi_analysis,
        "practical_sadhana": res.practical_sadhana,
        "nirvana_satkam_culmination": res.nirvana_satkam_culmination
    }


@app.post("/intelligence/cyber-defense/audit")
def audit_cyber_defense(
    query_text: str = Body(..., embed=True)
) -> Dict[str, Any]:
    """
    Audits query for cyber scam patterns, social engineering, and psychological manipulation (Lobha, Bhaya).
    Maps to Kauṭilīya Arthaśāstra deception classes and Kaṭha Upaniṣad cognitive firewalls.
    """
    res = CognitiveCybersecurityEngine.evaluate_threat(query_text)
    return {
        "query": res.query,
        "detected_vector": res.detected_vector.value,
        "primary_klesha_exploited": res.primary_klesha_exploited.value,
        "threat_confidence": res.threat_confidence,
        "is_malicious_scam": res.is_malicious_scam,
        "kautilya_deception_class": res.kautilya_deception_class,
        "upanishadic_cognitive_countermeasure": res.upanishadic_cognitive_countermeasure,
        "immediate_operational_steps": res.immediate_operational_steps,
        "national_helpline_action": res.national_helpline_action,
        "forensic_critique": res.forensic_critique
    }


@app.post("/verification/siddhi-boundary/audit")
def audit_siddhi_boundary(
    claim_text: str = Body(..., embed=True)
) -> Dict[str, Any]:
    """
    Audits claims of yogic mobility and psychic powers against Pātañjala Yoga Sūtras (YS 3.37, 3.48)
    and quantum physics, separating poetic idioms (Manojavā) from pseudo-quantum conflations.
    """
    res = PatanjaliSiddhiBoundaryEngine.audit_claim(claim_text)
    return {
        "query": res.query,
        "claim_type": res.claim_type.value,
        "is_quantum_conflation": res.is_quantum_conflation,
        "quantum_pseudoscience_penalty": res.quantum_pseudoscience_penalty,
        "shastric_context_valid": res.shastric_context_valid,
        "patanjali_sutra_references": res.patanjali_sutra_references,
        "classical_poetic_idiom_analysis": res.classical_poetic_idiom_analysis,
        "physics_quantum_reality": res.physics_quantum_reality,
        "philosophical_siddhanta": res.philosophical_siddhanta
    }


@app.post("/pedagogy/prenatal-safety/audit")
def audit_prenatal_safety(
    claim_text: str = Body(..., embed=True)
) -> Dict[str, Any]:
    """
    Audits prenatal fetal learning claims against Suśruta Saṃhitā 3.30, Caraka Saṃhitā 4.15,
    and modern developmental audiology (gestational weeks 24–28). Vetoes commercial fetal genius scams.
    """
    res = PrenatalAuditorySafetyEngine.audit_claim(claim_text)
    return {
        "query": res.query,
        "claim_type": res.claim_type.value,
        "is_commercial_pseudoscience": res.is_commercial_pseudoscience,
        "empirical_neurobiology_verdict": res.empirical_neurobiology_verdict,
        "ayurvedic_shastric_context": res.ayurvedic_shastric_context,
        "classical_metaphysical_explanation": res.classical_metaphysical_explanation,
        "commercial_scam_warning": res.commercial_scam_warning
    }


@app.post("/pedagogy/trataka/audit")
def audit_trataka_practice(
    practice_text: str = Body(..., embed=True),
    has_eye_condition: bool = Body(False, embed=True)
) -> Dict[str, Any]:
    """
    Audits Haṭha Yoga Trāṭaka (HYP 2.31–32) for neuro-ophthalmic safety, Troxler adaptation,
    photokeratitis prevention, and medical contraindications (glaucoma, severe myopia, retinopathy).
    """
    res = TratakaMeditationEngine.audit_practice(practice_text, user_has_eye_condition=has_eye_condition)
    return {
        "query": res.query,
        "practice_type": res.practice_type.value,
        "is_safe": res.is_safe,
        "medical_contraindications": res.medical_contraindications,
        "neuro_ophthalmic_mechanism": res.neuro_ophthalmic_mechanism,
        "hatha_yoga_shastric_foundation": res.hatha_yoga_shastric_foundation,
        "safety_guidelines": res.safety_guidelines,
        "occult_hype_refutation": res.occult_hype_refutation
    }


@app.post("/canon/mula-patha/explore")
def explore_mula_patha(
    canonical_id: str = Body(..., embed=True),
    include_commentaries: bool = Body(False, embed=True)
) -> Dict[str, Any]:
    """
    Renders 100% original unmodified Sanskrit root text (Mūla-Pāṭha) in three discrete layers:
    1. Mūla-Śloka (Invariant text with SHA-256 seal & Piṅgala prosody)
    2. Pāṇinian Anatomy (Padaccheda, Anvaya, Sandhi, Morphology)
    3. Śabdārtha (Root dictionary glosses)
    Optional downstream commentary overlays strictly segregated.
    """
    return MulaPathaEngine.explore_tri_layer(canonical_id, include_commentary_overlay=include_commentaries)


@app.post("/intelligence/epistemic-governance/audit")
def audit_epistemic_promotion(
    insight_id: str = Body(..., embed=True),
    target_state: str = Body("B_CURATED", embed=True),
    num_epigraphs: int = Body(0, embed=True),
    num_manuscripts: int = Body(0, embed=True),
    num_peer_reviewed: int = Body(0, embed=True),
    signatures: Dict[str, str] = Body(default_factory=dict, embed=True),
    rationale: str = Body("Administrative promotion audit", embed=True)
) -> Dict[str, Any]:
    """
    Enforces multi-signature governance and non-compensatory corroboration score threshold (>= 0.80)
    for promoting candidate insights to B_CURATED.
    Strictly vetoes any attempt to mutate A_CANONICAL.
    """
    # Parse target state
    t_state = KnowledgeState[target_state] if target_state in KnowledgeState.__members__ else KnowledgeState.B_CURATED
    
    # Parse signatures
    parsed_sigs: Dict[ScholarSignatureType, str] = {}
    for k, v in signatures.items():
        for s_type in ScholarSignatureType:
            if s_type.name == k or s_type.value == k:
                parsed_sigs[s_type] = v
                break

    res = EpistemicPromotionEngine.audit_and_promote_candidate(
        insight_id=insight_id,
        target_state=t_state,
        num_epigraphs=num_epigraphs,
        num_manuscripts=num_manuscripts,
        num_peer_reviewed=num_peer_reviewed,
        signatures=parsed_sigs,
        rationale=rationale
    )
    return {
        "event_id": res.event_id,
        "insight_id": res.insight_id,
        "from_state": res.from_state.name,
        "to_state": res.to_state.name,
        "corroboration_score": res.corroboration_score,
        "is_quorum_satisfied": res.is_quorum_satisfied,
        "authorized_signers": [s.name for s in res.authorized_signers],
        "is_promoted": res.is_promoted,
        "status_verdict": res.status_verdict,
        "rationale": res.rationale
    }


@app.post("/intelligence/cv-optical/audit")
def audit_cv_optical(
    text_claims: str = Body(..., embed=True),
    raw_keyframe_hex: Optional[str] = Body(None, embed=True),
    pose_symmetry: Optional[float] = Body(None, embed=True),
    blink_rate: Optional[float] = Body(None, embed=True)
) -> Dict[str, Any]:
    """
    Audits visual micro-signals against physical sensor telemetry.
    Vetoes optical illusions (inferring dress color, sweating, tremors from text alone).
    Verifies HSV color clustering when raw keyframes are provided.
    """
    res = CvOpticalPipelineEngine.audit_multimodal_stream(
        text_claims=text_claims,
        raw_keyframe_hex=raw_keyframe_hex,
        pose_symmetry=pose_symmetry,
        blink_rate=blink_rate
    )
    return {
        "frame_id": res.frame_id,
        "evidence_level": res.evidence_level.value,
        "is_hallucination_vetoed": res.is_hallucination_vetoed,
        "optical_score": res.optical_score,
        "verdict": res.verdict,
        "forensic_advice": res.forensic_advice,
        "color_cluster": {
            "dominant_hex": res.color_cluster.dominant_hex,
            "nearest_color": res.color_cluster.nearest_canonical_color,
            "hue_degrees": res.color_cluster.hue_degrees,
            "saturation": res.color_cluster.saturation_ratio
        } if res.color_cluster else None,
        "detected_discrepancies": res.detected_discrepancies
    }


class VideoStoryboardRequest(BaseModel):
    topic: str = "BG 2.47"
    format: str = "short"  # "short" (9:16) or "long" (16:9)
    language: str = "en"


class VideoGenerateRequest(BaseModel):
    topic: str = "BG 2.47"
    format: str = "short"
    language: str = "en"
    fast_mode: bool = False


@app.post("/video/storyboard")
def generate_video_storyboard(req: VideoStoryboardRequest) -> Dict[str, Any]:
    """
    Generates a production-grade scene-by-scene storyboard manifest
    for faceless video creation across YouTube Shorts/Reels (9:16) or Long Form (16:9).
    """
    v_format = VideoFormat.SHORT_9_16 if req.format.lower() == "short" else VideoFormat.LONG_16_9
    storyboard = VideoStoryboardDirector.create_storyboard(
        topic=req.topic,
        video_format=v_format,
        language=req.language
    )
    return {
        "project_id": storyboard.project_id,
        "topic": storyboard.topic,
        "format": storyboard.video_format.value,
        "language": storyboard.language,
        "total_duration_sec": storyboard.total_duration_sec,
        "target_platforms": storyboard.target_platforms,
        "seo_title": storyboard.seo_title,
        "seo_description": storyboard.seo_description,
        "seo_tags": storyboard.seo_tags,
        "scenes": [
            {
                "scene_number": s.scene_number,
                "start_sec": s.start_sec,
                "end_sec": s.end_sec,
                "duration_sec": s.duration_sec,
                "narration_text": s.narration_text,
                "visual_theme": s.visual_theme,
                "on_screen_devanagari": s.on_screen_devanagari,
                "on_screen_iast": s.on_screen_iast,
                "motion_type": s.motion_type.value
            }
            for s in storyboard.scenes
        ]
    }


@app.post("/video/generate")
def generate_production_video(req: VideoGenerateRequest) -> Dict[str, Any]:
    """
    Executes the autonomous faceless video production pipeline:
    Storyboarding -> Procedural Frames -> Neural TTS -> Tanpura Bed -> Ducking -> Subtitles -> MP4 Rendering.
    """
    v_format = VideoFormat.SHORT_9_16 if req.format.lower() == "short" else VideoFormat.LONG_16_9
    result = FacelessVideoProductionPipeline.generate_video(
        topic=req.topic,
        video_format=v_format,
        language=req.language,
        fast_mode=req.fast_mode
    )
    return result


class NyayaAuditRequest(BaseModel):
    argument_text: str = Field(..., description="Argument or statement to audit for Hetvābhāsas")


class ShlokaLookupRequest(BaseModel):
    query: str = Field(..., description="Canonical ID, keyword, or text reference (e.g. 'RV_03_062_10' or 'Gayatri')")


@app.post("/verification/nyaya/audit-fallacy")
def audit_nyaya_fallacy(req: NyayaAuditRequest) -> Dict[str, Any]:
    """
    Audits an input proposition against Akṣapāda Gautama's 5 inferential fallacies (Hetvābhāsas).
    """
    from app.verification.nyaya_logic import NyayaLogicEngine
    audit = NyayaLogicEngine.audit_argument(req.argument_text)
    return {
        "argument_text": req.argument_text,
        "is_fallacious": audit.is_fallacious,
        "detected_fallacy": audit.detected_fallacy.value,
        "sub_variety": audit.sub_variety,
        "confidence_score": audit.confidence_score,
        "flawed_term": audit.flawed_term,
        "refutation_reason": audit.refutation_reason,
        "rebuttal_strategy": audit.rebuttal_strategy,
        "classical_exemplar": audit.classical_exemplar
    }


@app.post("/canon/shloka/lookup")
def lookup_canonical_shloka(req: ShlokaLookupRequest) -> Dict[str, Any]:
    """
    Looks up authentic canonical shlokas across Vedas, Upaniṣads, Gītā, Rāmāyaṇa, Mahābhārata, and Darśanas.
    """
    from app.canon.shloka_corpus import ComprehensiveShlokaCorpusEngine
    matches = ComprehensiveShlokaCorpusEngine.lookup_shloka(req.query)
    return {
        "query": req.query,
        "match_count": len(matches),
        "results": [
            {
                "canonical_id": m.canonical_id,
                "text_title": m.text_title,
                "authority_type": m.authority_type,
                "chapter_verse": m.chapter_verse,
                "sanskrit_deva": m.sanskrit_deva,
                "iast": m.iast,
                "meaning_summary": m.meaning_summary,
                "match_score": m.match_score
            }
            for m in matches
        ]
    }


@app.get("/canon/shloka/statistics")
def get_shloka_corpus_statistics() -> Dict[str, Any]:
    """
    Returns corpus breakdown and statistics across all indexed Hindu scriptures.
    """
    from app.canon.shloka_corpus import ComprehensiveShlokaCorpusEngine
    return ComprehensiveShlokaCorpusEngine.get_corpus_statistics()









