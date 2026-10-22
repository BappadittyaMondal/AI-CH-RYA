"""
AI ĀCHĀRYA — Test Suite for Version 6.0 Cognitive Mastery & Pedagogical Scaffolding
(app/tests/test_v6_cognitive_mastery_pedagogy.py)

Covers:
1. Free Spaced Repetition Scheduler (FSRS) power-law retrievability and stability updates.
2. Sweller Cognitive Load Index (L_cog) and dynamic Anvaya fragmentation gating.
3. 20-Minute Gurukula Focus Protocol generation and vagal modulation grounding.
4. Cognitive Scam Firewall detecting DMIT, midbrain activation, and 10X brain claims.
5. Sandboxed Learner State isolation (§27, §32).
6. MasterOrchestrator FSM routing for cognitive student inquiries.
7. MasterOrchestrator scam refutation and seeker action summary.
8. FastAPI REST endpoints for cognitive scheduling, load calculation, and claim audits.
"""

import pytest
from fastapi.testclient import TestClient

from app.pedagogy.cognitive_mastery import (
    CognitiveMasteryEngine,
    ReviewGrade,
    FSRSSchedule,
    CognitiveLoadResult,
    GurukulaFocusProtocol,
    CognitiveScamReport
)
from app.orchestration.multi_agent import MasterOrchestrator
from app.api.main import app


@pytest.fixture
def cognitive_engine():
    return CognitiveMasteryEngine()


@pytest.fixture
def orchestrator():
    return MasterOrchestrator()


@pytest.fixture
def client():
    return TestClient(app)


# --- 1. FSRS POWER-LAW RETENTION MATHEMATICS ---

def test_fsrs_power_law_retrievability_and_intervals(cognitive_engine):
    # Boundary: at t=0, retrievability must be 1.0 (100%)
    r_0 = cognitive_engine.compute_retrievability(elapsed_days=0.0, stability=10.0)
    assert r_0 == 1.0

    # At t = stability (10 days), R(10, 10) = (1 + 0.19)^(-0.5) ≈ 1.19^(-0.5) ≈ 0.9167
    r_stab = cognitive_engine.compute_retrievability(elapsed_days=10.0, stability=10.0)
    assert 0.90 <= r_stab <= 0.93

    # As time elapses (e.g. 50 days), retrievability must decline monotonically
    r_50 = cognitive_engine.compute_retrievability(elapsed_days=50.0, stability=10.0)
    assert r_50 < r_stab

    # Optimal interval calculation for target R=0.90
    interval_days = cognitive_engine.calculate_optimal_interval(stability=10.0, target_r=0.90)
    assert interval_days > 10.0  # Approx 12.3 days

    # Review with GOOD grade: stability increases
    sched_good = cognitive_engine.update_fsrs_schedule(
        topic_id="GITA_2_47",
        elapsed_days=5.0,
        current_stability=5.0,
        difficulty=5.0,
        grade=ReviewGrade.GOOD
    )
    assert sched_good.stability >= 5.0
    assert sched_good.recommended_interval_days > 5.0

    # Review with AGAIN (lapse): stability collapses
    sched_again = cognitive_engine.update_fsrs_schedule(
        topic_id="GITA_2_47",
        elapsed_days=5.0,
        current_stability=10.0,
        difficulty=5.0,
        grade=ReviewGrade.AGAIN
    )
    assert sched_again.stability < 10.0
    assert sched_again.stability <= 2.5


# --- 2. COGNITIVE LOAD INDEX & ANVAYA FRAGMENTATION ---

def test_cognitive_load_index_and_anvaya_fragmentation(cognitive_engine):
    # Simple short verse without conjuncts under zero fatigue
    simple_res = cognitive_engine.evaluate_cognitive_load(
        concept_or_verse="ईशा वास्यमिदं सर्वम्",
        student_fatigue=0.0
    )
    assert simple_res.cognitive_load_index <= 0.85
    assert not simple_res.fragmentation_required
    assert "STANDARD INTEGRATED PEDAGOGY" in simple_res.scaffolding_instruction

    # Dense philosophical passage with high conjunct density and fatigue
    complex_text = (
        "अथातो ब्रह्मजिज्ञासा जन्माद्यस्य यतः शास्त्रयोनित्वात् तत्तु समन्वयात् "
        "विवर्तवाद परिणामवाद माया अनिर्वचनीय ख्यातिवाद अपरोक्षानुभूतिः।"
    )
    complex_res = cognitive_engine.evaluate_cognitive_load(
        concept_or_verse=complex_text,
        student_fatigue=0.9
    )
    assert complex_res.cognitive_load_index > 0.85
    assert complex_res.fragmentation_required
    assert "DYNAMIC PEDAGOGICAL FRAGMENTATION TRIGGERED" in complex_res.scaffolding_instruction
    assert "Padaccheda" in complex_res.scaffolding_instruction


# --- 3. GURUKULA FOCUS PROTOCOL GENERATION ---

def test_gurukula_focus_protocol_generation(cognitive_engine):
    protocol = cognitive_engine.generate_gurukula_focus_protocol()
    assert protocol.total_minutes == 20
    assert len(protocol.steps) == 5

    phases = [s["phase"] for s in protocol.steps]
    assert any("Somatic Activation" in p for p in phases)
    assert any("Autonomic Coherence" in p for p in phases)
    assert any("Attentional Fixation" in p for p in phases)

    # Check physiological and cultural grounding
    assert "vagal" in protocol.physiological_rationale.lower()
    assert "Thoppukaranam" in protocol.cultural_context
    assert "Abhaya" in protocol.anti_fear_grounding


# --- 4. COGNITIVE SCAM FIREWALL ---

def test_cognitive_scam_firewall_detection(cognitive_engine):
    # 1. DMIT test detection
    rep_dmit = cognitive_engine.evaluate_cognitive_claim(
        "Our academy uses DMIT fingerprint tests to discover your child's genius brain lobe dominance."
    )
    assert rep_dmit.is_pseudoscientific
    assert any("DMIT" in f for f in rep_dmit.detected_fallacies)
    assert any("Indian Psychiatric Society" in f for f in rep_dmit.detected_fallacies)
    assert "psychiatric" in rep_dmit.medical_scientific_verdict.lower()

    # 2. Midbrain activation & blindfold reading detection
    rep_midbrain = cognitive_engine.evaluate_cognitive_claim(
        "Unlock 3rd eye midbrain activation for kids to read books blindfolded in 2 days."
    )
    assert rep_midbrain.is_pseudoscientific
    assert any("Midbrain Activation" in f for f in rep_midbrain.detected_fallacies)

    # 3. 10X brain speed & 90% dormant brain myth
    rep_10x = cognitive_engine.evaluate_cognitive_claim(
        "Do this brain yoga exercise to 10X faster brain speed and activate 90% dormant brain."
    )
    assert rep_10x.is_pseudoscientific
    assert any("10X Brain Power" in f for f in rep_10x.detected_fallacies)

    # 4. Valid scientific/yogic study inquiry
    rep_valid = cognitive_engine.evaluate_cognitive_claim(
        "How does practicing Nadi Shodhana pranayama and active recall improve focus for college exams?"
    )
    assert not rep_valid.is_pseudoscientific
    assert len(rep_valid.detected_fallacies) == 0


# --- 5. SANDBOXED LEARNER STATE ISOLATION (§27, §32) ---

def test_sandboxed_learner_state_isolation(cognitive_engine):
    learner_id = "student_alpha_001"
    sched = cognitive_engine.record_learner_review(
        learner_id=learner_id,
        topic_id="UPANISHAD_ISHA_1",
        grade=ReviewGrade.GOOD,
        elapsed_days=2.0
    )
    assert sched.topic_id == "UPANISHAD_ISHA_1"
    assert sched.stability >= 1.0

    profile = cognitive_engine.get_or_create_learner_profile(learner_id)
    assert profile.completed_sessions == 1
    assert profile.sandboxed_isolated is True
    assert "UPANISHAD_ISHA_1" in profile.stability_deck


# --- 6. MASTER ORCHESTRATOR FSM COGNITIVE ROUTING ---

def test_master_orchestrator_fsm_cognitive_routing(orchestrator):
    resp = orchestrator.process_query("What is the daily student routine and focus protocol for exam study?")
    assert "Gurukula Cognitive Guidance" in resp.direct_answer
    assert "Patañjali Yoga Sūtra" in resp.source_text
    assert "Thoppukaranam" in resp.practical_application
    assert any("20-minute Gurukula Focus Protocol" in k for k in resp.key_takeaways)
    assert resp.seeker_action_summary is not None
    assert resp.visual_forensic_card is not None


# --- 7. MASTER ORCHESTRATOR SCAM REFUTATION ---

def test_master_orchestrator_fsm_scam_refutation(orchestrator):
    resp = orchestrator.process_query("Can DMIT test and midbrain activation 10X my brain power?")
    assert "Epistemic Cognitive Evaluation" in resp.direct_answer
    assert "PSEUDOSCIENCE DETECTED" in resp.english_explanation or "Cognitive Scam Audit" in resp.english_explanation
    assert any("Reject DMIT" in k for k in resp.key_takeaways)
    assert "Do not waste money" in resp.seeker_action_summary


# --- 8. FASTAPI REST ENDPOINTS ---

def test_fastapi_cognitive_mastery_endpoints(client):
    # 1. Schedule endpoint
    res_sched = client.post(
        "/pedagogy/cognitive-schedule",
        json={
            "topic_id": "BG_2_47",
            "elapsed_days": 3.0,
            "current_stability": 4.0,
            "difficulty": 5.0,
            "grade": 3,
            "target_r": 0.90
        }
    )
    assert res_sched.status_code == 200
    data_sched = res_sched.json()
    assert data_sched["topic_id"] == "BG_2_47"
    assert data_sched["retrievability"] > 0.0
    assert data_sched["recommended_interval_days"] > 0.0

    # 2. Cognitive load endpoint
    res_load = client.post(
        "/pedagogy/cognitive-load",
        json={
            "concept_or_verse": "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन",
            "student_fatigue": 0.3,
            "pedagogical_mode": "Student"
        }
    )
    assert res_load.status_code == 200
    data_load = res_load.json()
    assert "cognitive_load_index" in data_load
    assert "scaffolding_instruction" in data_load

    # 3. Student routine endpoint
    res_routine = client.get("/pedagogy/student-routine")
    assert res_routine.status_code == 200
    data_routine = res_routine.json()
    assert data_routine["total_minutes"] == 20
    assert len(data_routine["steps"]) == 5

    # 4. Evaluate cognitive claim endpoint
    res_claim = client.post(
        "/pedagogy/evaluate-cognitive-claim",
        json={"claim_text": "Is midbrain activation for children real or a scam?"}
    )
    assert res_claim.status_code == 200
    data_claim = res_claim.json()
    assert data_claim["is_pseudoscientific"] is True
    assert len(data_claim["detected_fallacies"]) > 0
