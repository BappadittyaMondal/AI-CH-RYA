"""
Automated Test Suite for Version 13.0 (app/tests/test_v13_cyber_siddhi_prenatal_trataka.py)

Validates:
1. Cognitive Cybersecurity & Anti-Scam Defense Engine
2. Pātañjala Siddhi Boundary & Anti-Quantum Pseudoscience Engine
3. Prenatal Auditory Learning & Ayurvedic Maternal Safety Boundary Engine
4. Trāṭaka Ophthalmic Safety & Neuro-Meditation Engine
5. Master Orchestrator FSM States 13, 14, 15, and 16
6. FastAPI REST Endpoints for all v13 modules
"""

import pytest
from fastapi.testclient import TestClient

from app.intelligence.cyber_defense import (
    CognitiveCybersecurityEngine,
    CyberScamVector,
    PsychologicalKleSha
)
from app.verification.siddhi_boundary import (
    PatanjaliSiddhiBoundaryEngine,
    SiddhiClaimType
)
from app.pedagogy.prenatal_and_trataka import (
    PrenatalAuditorySafetyEngine,
    PrenatalClaimType,
    TratakaMeditationEngine,
    TratakaPracticeType
)
from app.orchestration.multi_agent import MasterOrchestrator
from app.api.main import app


def test_cognitive_cybersecurity_engine_digital_arrest():
    query = "I received a call from CBI saying a parcel with drugs in my name was seized and I am under digital arrest"
    eval_res = CognitiveCybersecurityEngine.evaluate_threat(query)
    assert eval_res.detected_vector == CyberScamVector.DIGITAL_ARREST_EXTORTION
    assert eval_res.primary_klesha_exploited == PsychologicalKleSha.BHAYA
    assert eval_res.is_malicious_scam is True
    assert eval_res.threat_confidence >= 0.95
    assert "1930" in eval_res.national_helpline_action
    assert "Sākṣī-Bhāva" in eval_res.upanishadic_cognitive_countermeasure


def test_cognitive_cybersecurity_engine_investment_trap():
    query = "Join Telegram group for guaranteed return double money in 7 days with daily 5000 profit"
    eval_res = CognitiveCybersecurityEngine.evaluate_threat(query)
    assert eval_res.detected_vector == CyberScamVector.INVESTMENT_LOBHA_TRAP
    assert eval_res.primary_klesha_exploited == PsychologicalKleSha.LOBHA
    assert eval_res.is_malicious_scam is True
    assert eval_res.threat_confidence >= 0.90
    assert "Vairāgya" in eval_res.upanishadic_cognitive_countermeasure


def test_patanjali_siddhi_boundary_quantum_conflation():
    query = "Did Parashurama use quantum teleportation and quantum tunneling to travel to Kailash at the speed of the mind?"
    res = PatanjaliSiddhiBoundaryEngine.audit_claim(query)
    assert res.claim_type == SiddhiClaimType.QUANTUM_TELEPORTATION_CONFLATION
    assert res.is_quantum_conflation is True
    assert res.quantum_pseudoscience_penalty >= 0.80
    assert any("3.37" in ref for ref in res.patanjali_sutra_references)
    assert "Bennett et al. 1993" in res.physics_quantum_reality
    assert "Manojavā" in res.classical_poetic_idiom_analysis


def test_patanjali_siddhi_boundary_valid_manojavitva():
    query = "What is the meaning of manojavitva in Patanjali Yoga Sutra 3.48?"
    res = PatanjaliSiddhiBoundaryEngine.audit_claim(query)
    assert res.claim_type == SiddhiClaimType.MANOJAVITVA_MOBILITY
    assert res.is_quantum_conflation is False
    assert res.shastric_context_valid is True
    assert res.quantum_pseudoscience_penalty == 0.0


def test_prenatal_auditory_safety_engine_tactical_veto():
    query = "Can we teach tactical engineering or Abhimanyu Chakravyuha combat formation to a baby in the womb?"
    res = PrenatalAuditorySafetyEngine.audit_claim(query)
    assert res.claim_type == PrenatalClaimType.TACTICAL_GENIUS_PSEUDOSCIENCE
    assert res.is_commercial_pseudoscience is True
    assert "Suśruta Saṃhitā" in res.ayurvedic_shastric_context
    assert "24 and 28 weeks" in res.empirical_neurobiology_verdict
    assert "Pūrva-Janma Saṃskāras" in res.classical_metaphysical_explanation


def test_trataka_meditation_engine_safety_and_contraindications():
    # Normal safe inquiry
    safe_res = TratakaMeditationEngine.audit_practice("How to practice candle flame trataka properly", user_has_eye_condition=False)
    assert safe_res.practice_type == TratakaPracticeType.BAHIR_TRATAKA
    assert safe_res.is_safe is True
    assert any("3 to 4 feet" in g for g in safe_res.safety_guidelines)

    # User with eye condition (e.g. glaucoma)
    unsafe_res = TratakaMeditationEngine.audit_practice("How to practice candle flame trataka", user_has_eye_condition=True)
    assert unsafe_res.is_safe is False
    assert any("Glaucoma" in c for c in unsafe_res.medical_contraindications)

    # Occult hype inquiry
    occult_res = TratakaMeditationEngine.audit_practice("How to open third eye open in 21 days with telepathy tratak")
    assert occult_res.practice_type == TratakaPracticeType.OCCULT_HYPE_PSEUDOSCIENCE
    assert occult_res.is_safe is False
    assert "Troxler's fading" in occult_res.neuro_ophthalmic_mechanism


def test_master_orchestrator_states_13_14_15_16():
    orch = MasterOrchestrator()

    # State 13: Cyber defense
    r13 = orch.process_query("I got a digital arrest call from fake cyber police")
    assert "Kauṭilīya Arthaśāstra" in r13.source_text
    assert "1930" in r13.english_explanation
    assert r13.visual_forensic_card is not None

    # State 14: Siddhi boundary
    r14 = orch.process_query("Parashurama speed quantum teleportation to kailash")
    assert "Pātañjala Yoga Sūtras" in r14.source_text
    assert "Bennett et al." in r14.source_text
    assert r14.visual_forensic_card is not None

    # State 15: Prenatal safety
    r15 = orch.process_query("Can we teach baby abhimanyu chakravyuh in womb")
    assert "Suśruta Saṃhitā" in r15.source_text
    assert "Partanen et al." in r15.source_text
    assert r15.visual_forensic_card is not None

    # State 16: Trataka safety
    r16 = orch.process_query("How to do candle tratak meditation safely")
    assert "Haṭha Yoga Pradīpikā" in r16.source_text
    assert "Troxler" in r16.english_explanation
    assert r16.visual_forensic_card is not None


def test_fastapi_v13_endpoints():
    client = TestClient(app)

    # 1. Cyber defense
    c_resp = client.post("/intelligence/cyber-defense/audit", json={"query_text": "CBI officer arrest warrant skype call"})
    assert c_resp.status_code == 200
    assert c_resp.json()["detected_vector"] == "DIGITAL_ARREST_EXTORTION"
    assert c_resp.json()["is_malicious_scam"] is True

    # 2. Siddhi boundary
    s_resp = client.post("/verification/siddhi-boundary/audit", json={"claim_text": "quantum teleportation yoga parashurama"})
    assert s_resp.status_code == 200
    assert s_resp.json()["is_quantum_conflation"] is True
    assert s_resp.json()["quantum_pseudoscience_penalty"] >= 0.80

    # 3. Prenatal safety
    p_resp = client.post("/pedagogy/prenatal-safety/audit", json={"claim_text": "teach military tactics in womb chakravyuha"})
    assert p_resp.status_code == 200
    assert p_resp.json()["is_commercial_pseudoscience"] is True

    # 4. Trataka
    t_resp = client.post("/pedagogy/trataka/audit", json={"practice_text": "third eye open in 21 days tratak"})
    assert t_resp.status_code == 200
    assert t_resp.json()["is_safe"] is False
    assert len(t_resp.json()["medical_contraindications"]) >= 3
