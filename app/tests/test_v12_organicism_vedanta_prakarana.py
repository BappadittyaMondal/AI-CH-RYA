"""
AI ĀCHĀRYA — Standing Test Suite for Version 12.0 (app/tests/test_v12_organicism_vedanta_prakarana.py)
Validates:
1. Vedic Cosmic Organicism Engine (Puruṣa Sūkta RV 10.90, Piṇḍa-Brahmāṇḍa, Somatic Subsystems).
2. Earth-Feet Pratiṣṭhā Sanctity (RV 10.90.14 Padbhyāṃ Bhūmiḥ vs Colonial Taboos).
3. Mīmāṃsā Jurisprudential Invalidation (Jaimini 1.3.3 Veto on Medieval Birth Degradation).
4. Advaita Vedānta Prakaraṇa Pedagogy Engine (Ātmabodha 6-stage realization pipeline).
5. Master Orchestrator FSM States 11 and 12 routing.
6. FastAPI REST endpoints for v12 Organicism and Vedānta Prakaraṇa.
"""

import pytest
from fastapi.testclient import TestClient
from app.api.main import app
from app.verification.organicism import VedicCosmicOrganicismEngine, FunctionalSubsystem
from app.pedagogy.vedanta_prakarana import AtmabodhaPrakaranaEngine, VedantaPedagogyStage
from app.orchestration.multi_agent import MasterOrchestrator


client = TestClient(app)


def test_purusha_sukta_cosmic_organicism_valid_alignment():
    """Validates accurate interpretation of Puruṣa Sūkta as a single living cosmic organism."""
    text = (
        "The universe in Purusha Sukta is an interconnected living cosmic body with head, "
        "arms, thighs, and feet representing functional subsystems of knowledge, defense, commerce, and grounding."
    )
    res = VedicCosmicOrganicismEngine.audit_organicism_claim(text)

    assert res.is_organicism_aligned is True
    assert res.is_colonial_degradation_detected is False
    assert res.is_birth_caste_conflation is False
    assert res.pratistha_sacred_foundation_verified is True
    assert "पद्भ्यां भूमिर्दिशः श्रोत्रात्" in res.earth_emanation_proof
    assert len(res.subsystems_identified) >= 3
    assert "VEDIC COSMIC ORGANICISM VERIFIED" in res.forensic_verdict


def test_purusha_sukta_colonial_degradation_veto():
    """Validates detection and veto of colonial weaponized degradation regarding feet."""
    text = "The shudra was born from feet therefore degraded and feet are dirty in the apartheid system in rigveda."
    res = VedicCosmicOrganicismEngine.audit_organicism_claim(text)

    assert res.is_colonial_degradation_detected is True
    assert res.is_organicism_aligned is False
    assert res.jaimini_sutra_invalidation_triggered is True
    assert "COLONIAL WEAPONIZATION DETECTED" in res.forensic_verdict
    assert "Jaimini Sūtra 1.3.3" in res.hermeneutic_siddhanta


def test_purusha_sukta_birth_caste_conflation():
    """Validates detection and Mīmāṃsā invalidation of hereditary birth-caste claims in the Veda."""
    text = "Purusha Sukta mandates caste by birth alone and hereditary superiority in vedas."
    res = VedicCosmicOrganicismEngine.audit_organicism_claim(text)

    assert res.is_birth_caste_conflation is True
    assert res.is_organicism_aligned is False
    assert res.jaimini_sutra_invalidation_triggered is True
    assert "MEDIEVAL HEREDITARY CONFLATION DETECTED" in res.forensic_verdict


def test_atmabodha_prakarana_pedagogy_stages():
    """Validates the 6-stage Vedāntic realization pipeline modeled from Ātmabodha."""
    # 1. Adhikārī / Jñāna direct means
    q1 = "What is the primary qualification and direct means to liberation in Atmabodha?"
    rep1 = AtmabodhaPrakaranaEngine.analyze_inquiry(q1)
    assert rep1.target_stage == VedantaPedagogyStage.STAGE_1_ADHIKARI
    assert "Ātmabodha 2" in rep1.primary_verse_citation
    assert "Knowledge (Jñāna)" in rep1.epistemic_principle

    # 2. Adhyāsa / Superimposition
    q2 = "Explain adhyasa and the rope snake illusion in Advaita Vedanta"
    rep2 = AtmabodhaPrakaranaEngine.analyze_inquiry(q2)
    assert rep2.target_stage == VedantaPedagogyStage.STAGE_2_ADHYASA
    assert "Ātmabodha 7" in rep2.primary_verse_citation
    assert "snake" in rep2.pedagogical_analogy

    # 3. Upādhi / Pañca-Kośa
    q3 = "How to deconstruct the pancha kosha and three bodies?"
    rep3 = AtmabodhaPrakaranaEngine.analyze_inquiry(q3)
    assert rep3.target_stage == VedantaPedagogyStage.STAGE_3_APAVADA
    assert "Ātmabodha 14" in rep3.primary_verse_citation
    assert "paddy" in rep3.pedagogical_analogy

    # 4. Sākṣī Witness Consciousness
    q4 = "Who am I? How does the witness consciousness sakshi remain unattached?"
    rep4 = AtmabodhaPrakaranaEngine.analyze_inquiry(q4)
    assert rep4.target_stage == VedantaPedagogyStage.STAGE_4_SAKSHI
    assert "Ātmabodha 19" in rep4.primary_verse_citation
    assert "moon" in rep4.pedagogical_analogy

    # 5. Jīvanmukti & Saccidānanda
    q5 = "Explain Tat Tvam Asi, Jivanmukti, and sivoham in Nirvana Satkam"
    rep5 = AtmabodhaPrakaranaEngine.analyze_inquiry(q5)
    assert rep5.target_stage == VedantaPedagogyStage.STAGE_6_JIVANMUKTI
    assert "शिवोऽहम्" in rep5.nirvana_satkam_culmination


def test_master_orchestrator_states_11_and_12():
    """Validates Master Orchestrator FSM States 11 and 12 execution."""
    mo = MasterOrchestrator()

    # State 11: Puruṣa Sūkta Cosmic Organicism
    q_org = "purusha sukta living universe cosmic organism: are feet degraded?"
    resp_org = mo.process_query(q_org)
    assert "Puruṣa Sūkta Cosmic Organicism" in resp_org.direct_answer
    assert resp_org.visual_forensic_card is not None
    assert "PURUṢA SŪKTA COSMIC ORGANICISM" in resp_org.visual_forensic_card
    assert "RV 10.90.14" in resp_org.visual_forensic_card or "Padbhyāṃ Bhūmiḥ" in resp_org.visual_forensic_card

    # State 12: Ātmabodha Prakaraṇa Pedagogy
    q_ved = "atmabodha inquiry: who am i and what is witness consciousness sakshi caitanya?"
    resp_ved = mo.process_query(q_ved)
    assert "Advaita Vedānta Prakaraṇa Resolution" in resp_ved.direct_answer
    assert resp_ved.visual_forensic_card is not None
    assert "ADVAITA VEDĀNTA PRAKARAṆA PEDAGOGICAL PIPELINE" in resp_ved.visual_forensic_card


def test_fastapi_v12_endpoints():
    """Validates FastAPI REST endpoints exposed in Version 12.0."""
    # 1. Cosmic Organicism Audit
    res_org = client.post("/verification/cosmic-organicism/audit", json={
        "claim_text": "The universe in Purusha Sukta is an interconnected living cosmic body with head, arms, thighs, and feet."
    })
    assert res_org.status_code == 200
    data_org = res_org.json()
    assert data_org["is_organicism_aligned"] is True
    assert data_org["pratistha_sacred_foundation_verified"] is True

    # 2. Ātmabodha Pedagogy Analysis
    res_ved = client.post("/pedagogy/vedanta/atmabodha-analysis", json={
        "inquiry_text": "Explain adhyasa and the rope snake illusion in Atmabodha"
    })
    assert res_ved.status_code == 200
    data_ved = res_ved.json()
    assert "Adhyāsa" in data_ved["target_stage"]
    assert "Ātmabodha 7" in data_ved["primary_verse_citation"]
