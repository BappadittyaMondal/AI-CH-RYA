"""
AI ĀCHĀRYA — Test Suite for Version 7.0: Sthāpatya-Veda Architectural Engineering,
Indigenous Mechanical Physics & Historical Aeronautics Audit Engine
(app/tests/test_v7_sthapatya_and_aeronautics_audit.py)
"""

import pytest
from fastapi.testclient import TestClient

from app.civilization.sthapatya import (
    SthapatyaArchitectureEngine,
    QuarryingFeasibilityResult,
    InclineKinematicsResult,
    TempleAcousticResult,
    LightningGroundingResult,
    SthapatyaTreatise
)
from app.civilization.aeronautics import (
    HistoricalAeronauticsAuditEngine,
    AerodynamicAuditResult,
    HistoricalAeronauticsReport,
    VimanaHermeneuticLevel
)
from app.civilization import CivilizationalEngine
from app.orchestration.multi_agent import MasterOrchestrator
from app.api.main import app


def test_sthapatya_quarrying_feasibility_kailasa():
    """Validates basalt volumetric rock-cut mechanics, hydraulic wedge cleavage, and workforce logistics."""
    engine = SthapatyaArchitectureEngine()
    res = engine.calculate_quarrying_feasibility(
        site_name="Ellora Cave 16 Kailasa",
        net_volume_m3=85000.0,
        rock_density_kg_m3=2850.0,
        project_years=25.0,
        days_per_year=300.0,
        mason_daily_cut_m3=0.25
    )

    assert isinstance(res, QuarryingFeasibilityResult)
    assert res.net_mass_metric_tons == pytest.approx(242250.0, rel=1e-3)
    assert res.hydraulic_wedge_expansion_stress_mpa == 42.0
    assert res.rock_tensile_strength_mpa == 10.0
    assert res.wedge_cleavage_feasible is True
    assert res.estimated_skilled_masons_required == 46  # 85000 / 7500 / 0.25 = 45.33 -> 46
    assert res.estimated_general_laborers_required == 92
    assert "Baroda Copper Plate" in res.primary_epigraphic_anchor
    assert "No lasers or alien machinery required" in res.engineering_explanation


def test_sthapatya_incline_kinematics_brihadisvara():
    """Validates inclined plane kinematics and draft effort for the 80-ton Thanjavur shikhara."""
    engine = SthapatyaArchitectureEngine()
    res = engine.calculate_incline_kinematics(
        structure_name="Thanjavur Brihadisvara Vimāna Shikhara",
        monolith_mass_kg=80000.0,
        ramp_slope_deg=4.0,
        friction_coeff=0.08
    )

    assert isinstance(res, InclineKinematicsResult)
    assert res.monolith_mass_kg == 80000.0
    assert res.ramp_slope_angle_deg == 4.0
    assert res.friction_coefficient == 0.08
    assert res.tractive_pulling_force_newtons > 100000.0
    assert res.required_draft_oxen_pairs > 90
    assert res.required_human_haulers > 500
    assert res.mechanical_advantage_ratio > 5.0
    assert "Sarukkam village" in res.engineering_explanation


def test_sthapatya_acoustics_and_lightning():
    """Validates Garbhagṛha Helmholtz resonance and Puri Nīlacakra lightning grounding."""
    engine = SthapatyaArchitectureEngine()

    # 1. Acoustics
    acoustics = engine.calculate_garbhagriha_acoustics(
        length_m=4.5,
        width_m=4.5,
        height_m=5.0,
        door_width_m=1.2,
        door_height_m=2.4
    )
    assert isinstance(acoustics, TempleAcousticResult)
    assert acoustics.volume_m3 == pytest.approx(101.25, rel=1e-2)
    assert acoustics.helmholtz_resonant_frequency_hz > 0.0
    assert acoustics.vedic_chant_coupling is True
    assert "HRV" in acoustics.autonomic_effect or "vagal" in acoustics.autonomic_effect

    # 2. Lightning Grounding
    lightning = engine.evaluate_nilachakra_lightning_grounding()
    assert isinstance(lightning, LightningGroundingResult)
    assert lightning.is_lightning_arrestor_functional is True
    assert "Aṣṭadhātu" in lightning.alloy_composition
    assert "misawite" in lightning.corrosion_resistance_basis.lower()


def test_sthapatya_treatise_canon():
    """Validates primary Sthāpatya treatise retrieval and principles."""
    engine = SthapatyaArchitectureEngine()

    treatises = engine.get_canonical_treatises()
    assert "manasara" in treatises
    assert "mayamata" in treatises
    assert "samarangana_sutradhara" in treatises
    assert "kasyapa_silpa" in treatises

    bhoja = engine.lookup_treatise("Samarangana Sutradhara")
    assert bhoja is not None
    assert "Bhoja" in bhoja.author_or_school
    assert any("Yantra-vidyā" in p for p in bhoja.key_principles)


def test_civilization_engine_expanded_epigraphs_and_materials():
    """Verifies that CivilizationalEngine contains the new temple epigraphs and material records."""
    engine = CivilizationalEngine()

    # Epigraphs
    baroda = engine.lookup_epigraph("Baroda Copper Plate")
    assert baroda is not None
    assert baroda.record_id == "EPI-004"
    assert "Kṛṣṇa I" in baroda.key_historical_facts[0]

    thanjavur = engine.lookup_epigraph("Brihadisvara")
    assert thanjavur is not None
    assert thanjavur.record_id == "EPI-005"
    assert "Kunjaramallan" in thanjavur.key_historical_facts[1]

    konark = engine.lookup_epigraph("Konark Sun Temple")
    assert konark is not None
    assert konark.record_id == "EPI-006"
    assert "Bisu Moharana" in konark.key_historical_facts[1]

    # Material Science (ARCHITECTURE_VASTU)
    mat_kailasa = engine.lookup_material_science("Kailasa")
    assert mat_kailasa is not None
    assert mat_kailasa.tech_id == "MAT-005"
    assert mat_kailasa.domain == "ARCHITECTURE_VASTU"

    mat_brihad = engine.lookup_material_science("Brihadisvara")
    assert mat_brihad is not None
    assert mat_brihad.tech_id == "MAT-006"

    mat_nila = engine.lookup_material_science("Nilachakra")
    assert mat_nila is not None
    assert mat_nila.tech_id == "MAT-007"

    mat_konark = engine.lookup_material_science("Konark")
    assert mat_konark is not None
    assert mat_konark.tech_id == "MAT-008"


def test_historical_aeronautics_iisc_1974_report():
    """Validates the 1974 IISc aeronautical audit findings, craft parameters, and Hermeneutic Tripartition."""
    engine = HistoricalAeronauticsAuditEngine()
    report = engine.get_iisc_1974_study_report()

    assert report.publication_year == 1974
    assert any("Mukunda" in inv for inv in report.lead_investigators)
    assert len(report.crafts_evaluated) == 4

    for craft in report.crafts_evaluated:
        assert craft.is_aerodynamically_viable is False
        assert craft.lift_to_drag_ratio <= 0.30
        assert len(craft.thermodynamic_physical_violations) > 0

    rukma = engine.audit_craft("rukma")
    assert rukma is not None
    assert rukma.lift_to_drag_ratio == 0.15

    # Hermeneutic Tripartition
    level_alien = engine.evaluate_hermeneutic_stratum("Did aliens fly vimanas with mercury plasma engines?")
    assert level_alien == VimanaHermeneuticLevel.MODERN_PSEUDOSCIENCE_FORGERY

    level_itihasa = engine.evaluate_hermeneutic_stratum("Ravana abducted Sita in the Pushpaka Vimana moving at the speed of thought")
    assert level_itihasa == VimanaHermeneuticLevel.ADHIDAIVIKA_ITIHASA

    level_yogic = engine.evaluate_hermeneutic_stratum("The body is the chariot and the Atman is the rider per Katha Upanishad")
    assert level_yogic == VimanaHermeneuticLevel.ADHYATMIKA_YOGIC


def test_master_orchestrator_sthapatya_and_aeronautics_routing():
    """Tests deterministic FSM State 4 routing in MasterOrchestrator for temple engineering and aeronautics."""
    orchestrator = MasterOrchestrator()

    # 1. Kailasa / Rock-cut
    res_kailasa = orchestrator.process_query("How was the Kailasa temple carved without alien lasers?")
    assert "Baroda Copper Plate" in res_kailasa.source_text
    assert "hydraulic expanding wooden wedges" in res_kailasa.direct_answer
    assert "KAILASA TEMPLE (ELLORA CAVE 16)" in res_kailasa.visual_forensic_card

    # 2. Aeronautics / Vimāna
    res_vimana = orchestrator.process_query("Were vimanas ancient supersonic spacecraft with mercury engines?")
    assert "1974 IISc Aeronautical Study" in res_vimana.source_text
    assert "lift-to-drag ratio" in res_vimana.direct_answer
    assert "1974 IISC AERONAUTICAL AUDIT" in res_vimana.visual_forensic_card

    # 3. Thanjavur / Incline
    res_thanjavur = orchestrator.process_query("How was the 80 ton stone lifted on Brihadisvara temple shikhara?")
    assert "Brihadīśvara Epigraphic Inscriptions" in res_thanjavur.source_text
    assert "Sarukkam" in res_thanjavur.direct_answer
    assert "THANJAVUR BRIHADISVARA MEGALITH" in res_thanjavur.visual_forensic_card

    # 4. Puri Nīlacakra / Lightning
    res_puri = orchestrator.process_query("What is the technology of the Nilachakra lightning arrestor in Puri?")
    assert "Aṣṭadhātu" in res_puri.direct_answer
    assert "Faraday lightning arrestor" in res_puri.direct_answer
    assert "PURI JAGANNATH NILACAKRA" in res_puri.visual_forensic_card


def test_fastapi_endpoints_sthapatya_and_aeronautics():
    """Tests the new FastAPI REST endpoints for Sthāpatya and Aeronautics audits."""
    client = TestClient(app)

    # 1. Quarrying Feasibility
    res_q = client.post("/civilization/sthapatya/quarrying-feasibility", json={
        "site_name": "Ellora Cave 16 Kailasa",
        "net_volume_m3": 85000.0,
        "rock_density_kg_m3": 2850.0,
        "project_years": 25.0
    })
    assert res_q.status_code == 200
    data_q = res_q.json()
    assert data_q["wedge_cleavage_feasible"] is True
    assert "Baroda Copper Plate" in data_q["primary_epigraphic_anchor"]

    # 2. Incline Kinematics
    res_i = client.post("/civilization/sthapatya/incline-kinematics", json={
        "structure_name": "Thanjavur Brihadisvara Vimāna Shikhara",
        "monolith_mass_kg": 80000.0,
        "ramp_slope_deg": 4.0,
        "friction_coeff": 0.08
    })
    assert res_i.status_code == 200
    data_i = res_i.json()
    assert data_i["mechanical_advantage_ratio"] > 5.0
    assert data_i["required_draft_oxen_pairs"] > 90

    # 3. Aeronautics Audit
    res_a = client.post("/civilization/aeronautics/audit", json={
        "craft_name": "rukma",
        "claim_text": "Ancient aliens flew vimanas with mercury plasma engines"
    })
    assert res_a.status_code == 200
    data_a = res_a.json()
    assert data_a["publication_year"] == 1974
    assert data_a["craft_audit"]["craft_name"] == "Rukma Vimāna"
    assert data_a["craft_audit"]["is_aerodynamically_viable"] is False
    assert "Modern Pseudoscience" in data_a["hermeneutic_stratum"]
