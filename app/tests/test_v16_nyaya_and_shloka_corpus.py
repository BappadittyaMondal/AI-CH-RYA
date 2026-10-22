"""
Standing Verification Suite: Version 16.0 Nyāya Logic & Comprehensive Shloka Corpus
Validates:
1. Akṣapāda Gautama's 5 Hetvābhāsas (Bādhita, Viruddha, Asiddha, Savyabhicāra, Satpratipakṣa).
2. Pañcāvayava formal 5-step Nyāya syllogism validation.
3. Comprehensive Canonical Shloka Corpus retrieval across Vedas, Upaniṣads, Gītā, Rāmāyaṇa, Mahābhārata, and Darśanas.
4. MasterOrchestrator FSM State 21 routing.
5. FastAPI REST endpoints for Nyāya and Shloka services.
"""

import pytest
from app.verification.nyaya_logic import (
    NyayaLogicEngine,
    HetvabhasaType,
    NyayaSyllogism,
    FallacyAuditResult
)
from app.canon.shloka_corpus import ComprehensiveShlokaCorpusEngine, ShlokaSearchMatch
from app.orchestration.multi_agent import MasterOrchestrator
from app.pedagogy.modes import TeachingMode
from fastapi.testclient import TestClient
from app.api.main import app


def test_nyaya_logic_badhita_fallacy():
    """Test 1: Bādhita (Empirical Sublation / Perception Refutation)."""
    # Classical exemplar
    res = NyayaLogicEngine.audit_argument("Fire is cold because it is a substance")
    assert res.is_fallacious is True
    assert res.detected_fallacy == HetvabhasaType.BADHITA
    assert "Pratyakṣa-bādhita" in res.sub_variety
    assert res.confidence_score >= 0.90

    # Modern optical illusion case
    res2 = NyayaLogicEngine.audit_argument("The transcripts reveal dress color and sweating")
    assert res2.is_fallacious is True
    assert res2.detected_fallacy == HetvabhasaType.BADHITA


def test_nyaya_logic_viruddha_fallacy():
    """Test 2: Viruddha (Contradictory Middle Proving the Opposite)."""
    res = NyayaLogicEngine.audit_argument("Sound is eternal because it is created")
    assert res.is_fallacious is True
    assert res.detected_fallacy == HetvabhasaType.VIRUDDHA
    assert "Sādhya-viparyaya" in res.sub_variety

    res2 = NyayaLogicEngine.audit_argument("The mob was peaceful because they set fire to the bus")
    assert res2.is_fallacious is True
    assert res2.detected_fallacy == HetvabhasaType.VIRUDDHA


def test_nyaya_logic_asiddha_fallacy():
    """Test 3: Asiddha (Unproved Subject, Middle or Circular Reasoning)."""
    # Unproved locus (Sky-lotus / ancient laser aliens)
    res = NyayaLogicEngine.audit_argument("Aliens built Ellora Kailasa temple with laser beams")
    assert res.is_fallacious is True
    assert res.detected_fallacy == HetvabhasaType.ASIDDHA
    assert "Āśrayāsiddha" in res.sub_variety

    # Circular reasoning (Ātmāśraya)
    res2 = NyayaLogicEngine.audit_argument("This candidate is corrupt because this candidate is a corrupt person therefore we know")
    assert res2.is_fallacious is True
    assert res2.detected_fallacy == HetvabhasaType.ASIDDHA


def test_nyaya_logic_savyabhicara_fallacy():
    """Test 4: Savyabhicāra (Erratic / Too Wide Middle)."""
    res = NyayaLogicEngine.audit_argument("He is guilty because he was present at the market")
    assert res.is_fallacious is True
    assert res.detected_fallacy == HetvabhasaType.SAVYABHICARA
    assert "Sādhāraṇa" in res.sub_variety


def test_nyaya_logic_panchavayava_evaluation():
    """Test 5: Pañcāvayava formal 5-step syllogism."""
    # 1. Valid syllogism
    valid_s = NyayaSyllogism(
        pratijna="The hill has fire",
        hetu="Because it has smoke",
        udaharana="Wherever there is smoke there is fire, as in a culinary hearth",
        upanaya="This hill similarly has smoke which is invariably concomitant with fire",
        nigamana="Therefore, this hill has fire"
    )
    eval_res = NyayaLogicEngine.evaluate_panchavayava(valid_s)
    assert eval_res["is_formally_complete"] is True
    assert eval_res["has_hetvabhasa"] is False

    # 2. Syllogism with Bādhita flaw
    flawed_s = NyayaSyllogism(
        pratijna="Fire is cold",
        hetu="Because it is a substance",
        udaharana="Whatever is a substance is cold, like water",
        upanaya="Fire is such a substance",
        nigamana="Therefore, fire is cold"
    )
    flawed_res = NyayaLogicEngine.evaluate_panchavayava(flawed_s)
    assert flawed_res["has_hetvabhasa"] is True
    assert "Bādhita" in flawed_res["fallacy_details"]


def test_comprehensive_shloka_corpus_vedas():
    """Test 6: Retrieval of primary Vedic mantras (Ṛgveda & Atharvaveda)."""
    # Gāyatrī
    m1 = ComprehensiveShlokaCorpusEngine.lookup_shloka("RV_03_062_10")
    assert len(m1) > 0
    assert "तत्सवितुर्वरेण्यं" in m1[0].sanskrit_deva
    assert m1[0].authority_type.startswith("Śruti")

    # Mahāmṛtyuñjaya
    m2 = ComprehensiveShlokaCorpusEngine.lookup_shloka("tryambakam")
    assert len(m2) > 0
    assert "त्र्यम्बकं" in m2[0].sanskrit_deva

    # Nāsadīya
    m3 = ComprehensiveShlokaCorpusEngine.lookup_shloka("nasadiya")
    assert len(m3) > 0
    assert "नासदासीन्नो" in m3[0].sanskrit_deva

    # Atharvaveda Pṛthivī Sūkta
    m4 = ComprehensiveShlokaCorpusEngine.lookup_shloka("mata bhumiḥ")
    assert len(m4) > 0
    assert "माता भूमिः" in m4[0].sanskrit_deva


def test_comprehensive_shloka_corpus_upanishads():
    """Test 7: Retrieval of Mukhya Upaniṣad mantras (Kaṭha, Muṇḍaka, Bṛhadāraṇyaka)."""
    # Kaṭha Ratha Rūpaka
    m1 = ComprehensiveShlokaCorpusEngine.lookup_shloka("rathinam")
    assert len(m1) > 0
    assert "आत्मानं रथिनं" in m1[0].sanskrit_deva

    # Muṇḍaka Satyameva Jayate
    m2 = ComprehensiveShlokaCorpusEngine.lookup_shloka("satyameva jayate")
    assert len(m2) > 0
    assert "सत्यमेव जयते" in m2[0].sanskrit_deva

    # Bṛhadāraṇyaka Pavamāna
    m3 = ComprehensiveShlokaCorpusEngine.lookup_shloka("asato ma sadgamaya")
    assert len(m3) > 0
    assert "असतो मा" in m3[0].sanskrit_deva


def test_comprehensive_shloka_corpus_gita_and_itihasa():
    """Test 8: Retrieval of Bhagavad Gītā, Rāmāyaṇa & Mahābhārata."""
    # Gītā 2.55 Sthitaprajña
    m1 = ComprehensiveShlokaCorpusEngine.lookup_shloka("BG_02_55")
    assert len(m1) > 0
    assert "स्थितप्रज्ञस्तदोच्यते" in m1[0].sanskrit_deva

    # Gītā 4.7 Avatāra
    m2 = ComprehensiveShlokaCorpusEngine.lookup_shloka("BG_04_07")
    assert len(m2) > 0
    assert "यदा यदा हि धर्मस्य" in m2[0].sanskrit_deva

    # Gītā 18.66 Carama Śloka
    m3 = ComprehensiveShlokaCorpusEngine.lookup_shloka("sarvadharman parityajya")
    assert len(m3) > 0
    assert "सर्वधर्मान्परित्यज्य" in m3[0].sanskrit_deva

    # Vālmīki Rāmāyaṇa
    m4 = ComprehensiveShlokaCorpusEngine.lookup_shloka("VR_01_001_01")
    assert len(m4) > 0
    assert "वाल्मीकिर्मुनिपुङ्गवम्" in m4[0].sanskrit_deva

    # Mahābhārata Yakṣa Praśna
    m5 = ComprehensiveShlokaCorpusEngine.lookup_shloka("mahajano yena gataḥ")
    assert len(m5) > 0
    assert "महाजनो येन गतः" in m5[0].sanskrit_deva


def test_comprehensive_shloka_corpus_darsana():
    """Test 9: Retrieval of foundational Darśana Sūtras (Yoga & Nyāya)."""
    # Yoga Sūtras 1.2
    m1 = ComprehensiveShlokaCorpusEngine.lookup_shloka("yogaścittavṛttinirodhaḥ")
    assert len(m1) > 0
    assert "योगश्चित्तवृत्तिनिरोधः" in m1[0].sanskrit_deva

    # Nyāya Sūtras 1.1.1
    m2 = ComprehensiveShlokaCorpusEngine.lookup_shloka("pramana prameya samshaya")
    assert len(m2) > 0
    assert "प्रमाणप्रमेयसंशय" in m2[0].sanskrit_deva


def test_master_orchestrator_state_21_routing():
    """Test 10: MasterOrchestrator FSM State 21 routing for Nyāya fallacies and Shloka corpus."""
    orch = MasterOrchestrator()

    # 1. Nyāya fallacy query
    resp1 = orch.process_query("Perform a nyaya logic fallacy audit on: fire is cold because it is a substance")
    assert resp1 is not None
    assert "Nyāya Epistemic Audit" in resp1.direct_answer
    assert "Bādhita" in resp1.direct_answer
    assert resp1.visual_forensic_card is not None
    assert "NYĀYA DARŚANA HETVĀBHĀSA" in resp1.visual_forensic_card

    # 2. Canonical shloka lookup query
    resp2 = orch.process_query("Recite the gayatri mantra shloka")
    assert resp2 is not None
    assert "तत्सवितुर्वरेण्यं" in resp2.original_sanskrit
    assert "tat savitur vareṇyaṁ" in resp2.transliteration
    assert resp2.visual_forensic_card is not None
    assert "CANONICAL SHLOKA CORPUS RETRIEVAL" in resp2.visual_forensic_card


def test_fastapi_v16_endpoints():
    """Test 11: FastAPI endpoints for Nyāya and Shloka services."""
    client = TestClient(app)

    # 1. Nyāya Fallacy Audit endpoint
    r1 = client.post("/verification/nyaya/audit-fallacy", json={
        "argument_text": "Sound is eternal because it is created"
    })
    assert r1.status_code == 200
    data1 = r1.json()
    assert data1["is_fallacious"] is True
    assert "Viruddha" in data1["detected_fallacy"]

    # 2. Shloka Lookup endpoint
    r2 = client.post("/canon/shloka/lookup", json={
        "query": "satyameva jayate"
    })
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2["match_count"] > 0
    assert "सत्यमेव जयते" in data2["results"][0]["sanskrit_deva"]

    # 3. Shloka Statistics endpoint
    r3 = client.get("/canon/shloka/statistics")
    assert r3.status_code == 200
    data3 = r3.json()
    assert data3["total_shlokas_indexed"] >= 10
    assert "Śruti (Vedas & Mukhya Upaniṣads)" in data3["corpus_breakdown"]
