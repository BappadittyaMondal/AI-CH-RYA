"""
AI ĀCHĀRYA — Standing Test Suite for Version 9.0 (app/tests/test_v9_microsignals_mimamsa_ledger.py)
Validates:
1. Micro-Signal Forensic Engine (agency inversion, euphemisms, asymmetric burden).
2. Mīmāṃsā Hermeneutic Grayzone Engine (Ṣaḍ-Vidha Liṅga, Arthavāda vs Vidhi, Jaimini 1.3.3).
3. Computer Vision Optical Bridge & Anti-Hallucination Gate (veto vs HSV verification).
4. Candidate Epistemic Learning Ledger (sandboxed C_CANDIDATE staging, B_CURATED promotion, A_CANONICAL isolation).
5. Master Orchestrator FSM v9 routing.
6. FastAPI REST endpoints for v9 intelligence and verification.
"""

import pytest
from fastapi.testclient import TestClient
from app.api.main import app
from app.intelligence.micro_signals import MicroSignalForensicParser, MicroSignalCategory
from app.verification.mimamsa import MimamsaGrayzoneResolver, AuthorityStrata, MimamsaCanon
from app.intelligence.cv_bridge import ComputerVisionOpticalBridge, OpticalEvidenceLevel
from app.intelligence.learning_ledger import CandidateEpistemicLedger, InsightDomain
from app.core.knowledge_states import KnowledgeState
from app.orchestration.multi_agent import MasterOrchestrator


client = TestClient(app)


def test_micro_signal_agency_inversion_and_euphemism():
    """Validates detection of passive voice agent obfuscation and sanitizing euphemisms."""
    text = "Violence broke out after stones were pelted during the yatra. The temple was damaged in a mysterious fire."
    rep = MicroSignalForensicParser.analyze_text(text)

    assert rep.total_signals_detected >= 3
    assert rep.composite_manipulation_score >= 0.50
    assert rep.is_compromised is True
    assert rep.dominant_manipulation_vector in [
        MicroSignalCategory.AGENCY_INVERSION.value,
        MicroSignalCategory.EUPHEMISTIC_NEUTRALIZATION.value
    ]

    categories = [s.category for s in rep.detected_signals]
    assert MicroSignalCategory.AGENCY_INVERSION in categories
    assert MicroSignalCategory.EUPHEMISTIC_NEUTRALIZATION in categories


def test_micro_signal_asymmetric_burden_and_anachronism():
    """Validates detection of asymmetric evidential burdens and anachronistic smears."""
    text = "There is no contemporary written record for this unproven indigenous claim, which represents a bastion of brahmanical hegemony."
    rep = MicroSignalForensicParser.analyze_text(text)

    assert rep.total_signals_detected >= 2
    categories = [s.category for s in rep.detected_signals]
    assert MicroSignalCategory.ASYMMETRIC_BURDEN in categories
    assert MicroSignalCategory.PREJUDICIAL_ANACHRONISM in categories


def test_mimamsa_grayzone_arthavada_vs_vidhi():
    """Validates classification of hyperbole/curses as Arthavāda rather than binding Vidhi."""
    claim = "He who neglects this rite goes to hell and incurs the sin of killing a thousand cows."
    res = MimamsaGrayzoneResolver.resolve_grayzone(claim, declared_source="Manusmriti")

    assert res.is_arthavada_metaphor is True
    assert res.is_vidhi_binding is False
    assert res.primary_stratum == AuthorityStrata.SMRITI
    assert res.overall_coherence_score > 0.0
    assert "ARTHAVĀDA" in res.siddhanta_resolution


def test_mimamsa_sruti_smriti_conflict_resolution():
    """Validates Jaimini 1.3.3: Smṛti contradictory to universal Śruti oneness is invalidated."""
    valid_vidhi = "Satyaṃ vada, dharmaṃ cara, ahimsā paramo dharmaḥ."
    res_valid = MimamsaGrayzoneResolver.resolve_grayzone(valid_vidhi, declared_source="Taittiriya Upanishad")
    assert res_valid.is_vidhi_binding is True
    assert res_valid.is_scripturally_valid is True
    assert res_valid.primary_stratum == AuthorityStrata.SRUTI

    # Invalidate claim preaching innate structural inferiority
    invalid_claim = "Certain classes possess innate inferiority and cannot attain liberation."
    res_invalid = MimamsaGrayzoneResolver.resolve_grayzone(invalid_claim, declared_source="Medieval Digest")
    assert res_invalid.is_scripturally_valid is False
    assert "1.3.3" in res_invalid.siddhanta_resolution


def test_cv_optical_bridge_anti_hallucination_veto():
    """Validates that text-only visual claims are vetoed while CV metrics are verified."""
    text_unverified = "The speaker was wearing a saffron dress color and sweating nervously with pupil dilation."
    rep_veto = ComputerVisionOpticalBridge.audit_visual_assertions(text_claims=text_unverified)

    assert rep_veto.is_hallucination_vetoed is True
    assert rep_veto.optical_integrity_score == 0.0
    assert len(rep_veto.detected_unverified_claims) >= 3
    assert "ANTI-HALLUCINATION OPTICAL VETO" in rep_veto.audit_verdict

    # Verified CV extraction
    rep_cv = ComputerVisionOpticalBridge.audit_visual_assertions(
        text_claims="Analysis of speaker attire",
        evidence_level=OpticalEvidenceLevel.KEYFRAME_DOMINANT_HEX,
        keyframe_dominant_hex="#FF9933",
        pose_symmetry_score=0.92
    )
    assert rep_cv.is_hallucination_vetoed is False
    assert rep_cv.optical_integrity_score == 1.0
    assert rep_cv.verified_visual_metrics["nearest_color_name"] == "Saffron"
    assert "92.0%" in rep_cv.verified_visual_metrics["pose_symmetry"]


def test_candidate_epistemic_learning_ledger_sandboxing():
    """Validates candidate learning staging, query retrieval, and A_CANONICAL isolation."""
    item = CandidateEpistemicLedger.record_candidate_insight(
        topic="Sinauli Antenna Swords",
        domain=InsightDomain.ARCHAEOLOGY_EPIGRAPHY,
        learned_content="Copper antenna swords with distinct hilt bifurcation dated c. 2000 BCE in Doab.",
        evidence_source="ASI Sanjay Manjul 2018 Excavation Report"
    )

    assert item.insight_id.startswith("INS-")
    assert item.knowledge_state == KnowledgeState.C_CANDIDATE
    assert item.is_promoted is False

    # Query ledger
    matches = CandidateEpistemicLedger.query_insights("Sinauli")
    assert len(matches) >= 1
    assert any(m.insight_id == item.insight_id for m in matches)

    # Promote to B_CURATED
    ok, msg = CandidateEpistemicLedger.promote_to_curated(item.insight_id, "ACHARYA_ADMIN_VERIFIED_2026")
    assert ok is True

    # Failed promotion with invalid key
    fail_ok, _ = CandidateEpistemicLedger.promote_to_curated(item.insight_id, "WRONG_KEY")
    assert fail_ok is False

    # Stats verify isolation
    stats = CandidateEpistemicLedger.get_ledger_stats()
    assert stats["canonical_isolation_enforced"] is True
    assert stats["b_curated_promoted"] >= 1


def test_master_orchestrator_v9_routing():
    """Validates MasterOrchestrator FSM dispatching to the 4 new v9 states."""
    mo = MasterOrchestrator()

    # 1. Optical audit routing
    resp_opt = mo.process_query("optical audit check dress colour and pupil dilation")
    assert "ANTI-HALLUCINATION OPTICAL VETO" in resp_opt.direct_answer
    assert resp_opt.visual_forensic_card is not None

    # 2. Micro-signal routing
    resp_ms = mo.process_query("micro-signal analysis of stones were pelted during the procession")
    assert "Forensic Micro-Signal Analysis" in resp_opt.direct_answer or "Micro-Signal" in resp_ms.direct_answer
    assert resp_ms.visual_forensic_card is not None

    # 3. Grayzone routing
    resp_gz = mo.process_query("mimamsa grayzone analysis of arthavada vs vidhi in smriti vs sruti")
    assert "Mīmāṃsā Hermeneutic Resolution" in resp_gz.direct_answer or "Resolution" in resp_gz.direct_answer
    assert resp_gz.visual_forensic_card is not None

    # 4. Learning ledger routing
    resp_ll = mo.process_query("query candidate insight from epistemic ledger")
    assert "Epistemic Candidate Ledger" in resp_ll.direct_answer
    assert resp_ll.visual_forensic_card is not None


def test_fastapi_v9_endpoints():
    """Validates all newly exposed FastAPI endpoints for v9."""
    # 1. Micro-signals
    res_ms = client.post("/intelligence/micro-signals", json={"text_payload": "Clashes erupted and the temple was damaged in a mysterious fire."})
    assert res_ms.status_code == 200
    data_ms = res_ms.json()
    assert data_ms["total_signals_detected"] >= 2
    assert "detected_signals" in data_ms

    # 2. Mīmāṃsā Grayzone
    res_gz = client.post("/verification/mimamsa-grayzone", json={"claim_or_verse": "He who neglects this falls into hell for a thousand years", "declared_source": "Manusmriti"})
    assert res_gz.status_code == 200
    data_gz = res_gz.json()
    assert data_gz["is_arthavada_metaphor"] is True
    assert len(data_gz["canon_evaluations"]) == 6

    # 3. CV Optical Audit
    res_opt = client.post("/intelligence/cv-optical-audit", json={"text_claims": "The leader was nervous, sweating, with dress color red.", "has_cv_keyframe": False})
    assert res_opt.status_code == 200
    data_opt = res_opt.json()
    assert data_opt["is_hallucination_vetoed"] is True

    # 4. Learning Ledger Record & Stats
    res_rec = client.post("/intelligence/learning-ledger/record", json={
        "topic": "Lothal Dock Basin",
        "domain": InsightDomain.ARCHAEOLOGY_EPIGRAPHY.value,
        "learned_content": "Tidal lock gate and trapezoidal burnt-brick basin facilitating Bronze Age maritime trade.",
        "evidence_source": "S.R. Rao ASI Lothal Report"
    })
    assert res_rec.status_code == 200
    data_rec = res_rec.json()
    assert data_rec["status"] == "RECORDED_IN_C_CANDIDATE"

    # Query ledger
    res_q = client.get("/intelligence/learning-ledger/query?keyword=Lothal")
    assert res_q.status_code == 200
    assert len(res_q.json()) >= 1

    # Ledger stats
    res_stats = client.get("/intelligence/learning-ledger/stats")
    assert res_stats.status_code == 200
    assert res_stats.json()["canonical_isolation_enforced"] is True
