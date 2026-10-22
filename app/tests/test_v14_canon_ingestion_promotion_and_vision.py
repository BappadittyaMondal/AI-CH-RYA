"""
AI ĀCHĀRYA — Standing Test Suite for Version 14.0 (test_v14_canon_ingestion_promotion_and_vision.py)

Comprehensive verification of:
1. Mūla-Pāṭha Canonical Text Ingestion & Tri-Layer Representation (app/canon/mula_ingestion.py).
2. Pāṇinian Anatomy, Chandas Prosody, and Cryptographic SHA-256 Tamper Detection.
3. Multi-Signature Epistemic Governance & Canonical Isolation Gate (app/intelligence/promotion_governance.py).
4. Multimodal CV Keyframe Pipeline, HSV Clustering & Anti-Hallucination Gate (app/intelligence/cv_pipeline.py).
5. Master Multi-Agent Orchestrator FSM States 17, 18, and 19 (app/orchestration/multi_agent.py).
6. FastAPI v14 REST Endpoints (app/api/main.py).
"""

import pytest
import sqlite3
from fastapi.testclient import TestClient

from app.core.knowledge_states import KnowledgeState
from app.core.db_schema import init_sqlite_memory_db
from app.canon.mula_ingestion import MulaPathaEngine, TriLayerVerse, TextAuthorityType
from app.intelligence.promotion_governance import (
    EpistemicPromotionEngine, ScholarSignatureType, _AUTHORIZED_SCHOLAR_KEYS
)
from app.intelligence.cv_pipeline import CvOpticalPipelineEngine
from app.orchestration.multi_agent import MasterOrchestrator
from app.api.main import app

client = TestClient(app)


def test_mula_patha_ingestion_and_tri_layer():
    """Verifies Tri-Layer representation for BG 2.47, Isha 1, and RV 10.90.14."""
    bg_res = MulaPathaEngine.explore_tri_layer("BG_02_47", include_commentary_overlay=True)
    assert bg_res["canonical_id"] == "BG_02_47"
    assert "कर्मण्येवाधिकारस्ते" in bg_res["layer_1_mula"]["sanskrit_deva"]
    assert "Anuṣṭubh" in bg_res["layer_1_mula"]["meter_chandas"]
    assert bg_res["layer_1_mula"]["knowledge_state"] == "A_CANONICAL"
    assert bg_res["layer_1_mula"]["is_immutable"] is True
    
    # Layer 2: Pāṇinian Anatomy
    l2 = bg_res["layer_2_paninian_anatomy"]
    assert "karmaṇi" in l2["padaccheda"]
    assert "adhikāraḥ" in l2["padaccheda"]
    assert "te karmaṇi eva adhikāraḥ" in l2["anvaya"]
    assert "karmaṇi + eva = karmaṇy eva (Yaṇ-sandhi per Pāṇini 6.1.77)" in l2["sandhi_decompositions"]
    
    # Layer 3: Śabdārtha
    l3 = bg_res["layer_3_sabdartha"]
    assert "duty" in l3["word_glosses"]["karmaṇi"].lower()
    assert "right" in l3["word_glosses"]["adhikāraḥ"].lower()
    
    # Commentary Overlay segregation
    overlays = bg_res["secondary_commentary_overlay"]
    assert len(overlays) == 2
    assert overlays[0]["commentator"] == "Ādi Śaṅkarācārya"
    assert overlays[1]["commentator"] == "Śrī Rāmānujācārya"


def test_mula_patha_tamper_detection_and_integrity_veto():
    """Verifies that altering even a single character trips the cryptographic integrity veto."""
    # 1. Unaltered verification
    is_valid, msg = MulaPathaEngine.verify_verse_integrity(
        "BG_02_47",
        "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन । मा कर्मफलहेतुर्भूर्मा ते सङ्गोऽस्त्वकर्मणि ॥"
    )
    assert is_valid is True
    assert "INTEGRITY VERIFIED" in msg
    
    # 2. Tampered verification (altering one word: changing फलेषु to धनेषु)
    tampered_deva = "कर्मण्येवाधिकारस्ते मा धनेषु कदाचन । मा कर्मफलहेतुर्भूर्मा ते सङ्गोऽस्त्वकर्मणि ॥"
    is_valid_tampered, tamper_msg = MulaPathaEngine.verify_verse_integrity("BG_02_47", tampered_deva)
    assert is_valid_tampered is False
    assert "INTEGRITY BREACH VETO" in tamper_msg


def test_mula_patha_sqlite_database_population():
    """Verifies database population of canonical texts and verses into in-memory SQLite schema."""
    conn = init_sqlite_memory_db()
    inserted_count = MulaPathaEngine.populate_database(conn)
    assert inserted_count >= 3
    
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM verses WHERE state = 'A_CANONICAL'")
    count = cursor.fetchone()[0]
    assert count >= 3
    
    cursor.execute("SELECT commentator FROM commentaries WHERE verse_id = 'BG_02_47'")
    commentators = [row[0] for row in cursor.fetchall()]
    assert "Ādi Śaṅkarācārya" in commentators
    conn.close()


def test_epistemic_promotion_corroboration_score_calculation():
    """Verifies non-compensatory corroboration score calculation formula."""
    # Zero evidence
    assert EpistemicPromotionEngine.calculate_corroboration_score(0, 0, 0) == 0.0
    
    # Insufficient evidence (1 epigraph = 0.40, below 0.80)
    assert EpistemicPromotionEngine.calculate_corroboration_score(1, 0, 0) == 0.40
    
    # Sufficient evidence (2 epigraphs = 0.80)
    assert EpistemicPromotionEngine.calculate_corroboration_score(2, 0, 0) == 0.80
    
    # Multi-source triangulation (1 epigraph 0.40 + 1 manuscript 0.35 + 1 peer study 0.25 = 1.0)
    assert EpistemicPromotionEngine.calculate_corroboration_score(1, 1, 1) == 1.0


def test_epistemic_promotion_canonical_isolation_veto():
    """Verifies that attempting to promote candidate insights to A_CANONICAL trips a security veto."""
    signatures = {
        ScholarSignatureType.PANDIT_SEAL: _AUTHORIZED_SCHOLAR_KEYS[ScholarSignatureType.PANDIT_SEAL],
        ScholarSignatureType.ACHARYA_SEAL: _AUTHORIZED_SCHOLAR_KEYS[ScholarSignatureType.ACHARYA_SEAL],
        ScholarSignatureType.TECH_AUDITOR_SEAL: _AUTHORIZED_SCHOLAR_KEYS[ScholarSignatureType.TECH_AUDITOR_SEAL]
    }
    
    audit = EpistemicPromotionEngine.audit_and_promote_candidate(
        insight_id="INS-TEST-001",
        target_state=KnowledgeState.A_CANONICAL,
        num_epigraphs=3,
        num_manuscripts=3,
        num_peer_reviewed=3,
        signatures=signatures,
        rationale="Attempting direct injection into scripture"
    )
    assert audit.is_promoted is False
    assert "CANONICAL ISOLATION SECURITY VETO" in audit.status_verdict


def test_epistemic_promotion_multi_signature_quorum():
    """Verifies m-of-n quorum requirement for promoting candidate insights to B_CURATED."""
    valid_key_p = _AUTHORIZED_SCHOLAR_KEYS[ScholarSignatureType.PANDIT_SEAL]
    valid_key_a = _AUTHORIZED_SCHOLAR_KEYS[ScholarSignatureType.ACHARYA_SEAL]
    
    # Sub-case A: Single signature (Quorum deficit)
    audit_single = EpistemicPromotionEngine.audit_and_promote_candidate(
        insight_id="INS-TEST-002",
        target_state=KnowledgeState.B_CURATED,
        num_epigraphs=2,
        num_manuscripts=1,
        num_peer_reviewed=1,
        signatures={ScholarSignatureType.PANDIT_SEAL: valid_key_p},
        rationale="Single signer attempt"
    )
    assert audit_single.is_promoted is False
    assert "QUORUM DEFICIT VETO" in audit_single.status_verdict
    
    # Sub-case B: 2 valid signatures (Quorum satisfied)
    audit_quorum = EpistemicPromotionEngine.audit_and_promote_candidate(
        insight_id="INS-TEST-003",
        target_state=KnowledgeState.B_CURATED,
        num_epigraphs=2,
        num_manuscripts=1,
        num_peer_reviewed=1,
        signatures={
            ScholarSignatureType.PANDIT_SEAL: valid_key_p,
            ScholarSignatureType.ACHARYA_SEAL: valid_key_a
        },
        rationale="Dual scholar authenticated promotion"
    )
    assert audit_quorum.is_quorum_satisfied is True
    assert audit_quorum.corroboration_score >= 0.80


def test_cv_optical_anti_hallucination_veto():
    """Verifies that asserting visual observations without CV pixel telemetry triggers an optical veto."""
    # Text making attire and physiological micro-signal claims without pixel stream
    res = CvOpticalPipelineEngine.audit_multimodal_stream(
        text_claims="The speaker kurta colour was saffron and nervous sweating was visible."
    )
    assert res.is_hallucination_vetoed is True
    assert res.optical_score == 0.0
    assert "ANTI-HALLUCINATION OPTICAL VETO" in res.verdict


def test_cv_optical_verified_keyframe_and_chromatic_contradiction():
    """Verifies keyframe HSV clustering and chromatic contradiction detection."""
    # 1. Matching observation
    res_match = CvOpticalPipelineEngine.audit_multimodal_stream(
        text_claims="The speaker delivered the discourse in saffron robes.",
        raw_keyframe_hex="#FF9933",
        pose_symmetry=0.92
    )
    assert res_match.is_hallucination_vetoed is False
    assert res_match.optical_score == 1.0
    assert res_match.color_cluster.nearest_canonical_color == "Saffron"
    
    # 2. Chromatic contradiction: text claims blue suit, but sensor reads saffron (#FF9933)
    res_contradiction = CvOpticalPipelineEngine.audit_multimodal_stream(
        text_claims="The speaker was wearing a blue suit during the address.",
        raw_keyframe_hex="#FF9933"
    )
    assert res_contradiction.is_hallucination_vetoed is True
    assert res_contradiction.optical_score == 0.20
    assert "CHROMATIC CONTRADICTION DETECTED" in res_contradiction.verdict


def test_master_orchestrator_states_17_18_19():
    """Verifies Master Orchestrator FSM transitions for States 17, 18, and 19."""
    orch = MasterOrchestrator()
    
    # State 17: Mūla-Pāṭha Tri-Layer Canon Exploration
    res_17 = orch.process_query("Please explain bg 2.47 padaccheda and anvaya in the original unmodified text")
    assert "BG_02_47" in res_17.direct_answer
    assert "MŪLA-PĀṬHA TRI-LAYER CANONICAL FORENSIC EXPLORATION" in res_17.visual_forensic_card
    assert "karmaṇy evādhikāras te" in res_17.transliteration
    
    # State 18: Epistemic Governance & Promotion
    res_18 = orch.process_query("Perform an epistemic promotion audit with scholar signature and pandit seal")
    assert "Epistemic Promotion Governance Audit" in res_18.direct_answer
    assert "EPISTEMIC PROMOTION MULTI-SIGNATURE GOVERNANCE AUDIT" in res_18.visual_forensic_card
    
    # State 19: Multimodal CV Optical Integrity Audit
    res_19 = orch.process_query("Execute cv keyframe audit on video stream with chromatic contradiction")
    assert "Multimodal Optical & Anti-Hallucination Audit" in res_19.direct_answer
    assert "MULTIMODAL COMPUTER VISION OPTICAL INTEGRITY AUDIT" in res_19.visual_forensic_card





def test_fastapi_v14_endpoints():
    """Verifies FastAPI REST endpoints for v14 engines."""
    # Endpoint 1: Mūla-Pāṭha Explorer
    r1 = client.post("/canon/mula-patha/explore", json={"canonical_id": "BG_02_47", "include_commentaries": True})
    assert r1.status_code == 200
    data1 = r1.json()
    assert data1["canonical_id"] == "BG_02_47"
    assert "karmaṇi" in data1["layer_2_paninian_anatomy"]["padaccheda"]
    
    # Endpoint 2: Epistemic Promotion Audit
    r2 = client.post(
        "/intelligence/epistemic-governance/audit",
        json={
            "insight_id": "INS-TEST-API",
            "target_state": "B_CURATED",
            "num_epigraphs": 2,
            "num_manuscripts": 2,
            "num_peer_reviewed": 1,
            "signatures": {
                "PANDIT_SEAL": "KEY_PANDIT_PANINI_VERIFIED_2026",
                "ACHARYA_SEAL": "KEY_ACHARYA_VEDANTA_VERIFIED_2026"
            },
            "rationale": "API testing verification"
        }
    )
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2["is_quorum_satisfied"] is True
    assert data2["corroboration_score"] >= 0.80
    
    # Endpoint 3: Multimodal CV Optical Audit
    r3 = client.post(
        "/intelligence/cv-optical/audit",
        json={
            "text_claims": "The speaker dress colour was saffron",
            "raw_keyframe_hex": "#FF9933"
        }
    )
    assert r3.status_code == 200
    data3 = r3.json()
    assert data3["is_hallucination_vetoed"] is False
    assert data3["color_cluster"]["nearest_color"] == "Saffron"
