"""
AI ĀCHĀRYA — Comprehensive Test Suite for v4.0 Capabilities
Validates:
1. Bhāratīya Civilization Engine (Kṣetra, Epigraphy, Institutions, Material Science)
2. Bhāratīya Culture Engine (Kālacakra Pañcāṅga, Ṣoḍaśa Saṃskāras, Temple Ecosystem, Lokācāra)
3. Propaganda Detector & ALEDT Tensor (4 Distortion Vectors, Non-linear Collapse)
4. Vivāda-Nirṇaya Epistemic Arbitration Engine (Continuous Kernel, Delta-T Penalty, Strata-Aware, Mahābhārata Dating Benchmark)
5. Multi-Agent Integration & FastAPI Endpoints
"""

import pytest
from fastapi.testclient import TestClient
from app.civilization import CivilizationalEngine, CivilizationalStrata
from app.culture import CultureEngine, RituSeason, SamskaraStage
from app.verification.propaganda_detector import PropagandaDetector, DistortionVector, BiasProfile
from app.verification.vivada_nirnaya import (
    VivadaNirnayaEngine,
    ChronologicalHypothesis,
    TextualStrataLevel,
    ArchaeologicalStratumMatch
)
from app.orchestration.multi_agent import MasterOrchestrator
from app.api.main import app


@pytest.fixture
def civ_engine():
    return CivilizationalEngine()


@pytest.fixture
def cult_engine():
    return CultureEngine()


@pytest.fixture
def prop_detector():
    return PropagandaDetector()


@pytest.fixture
def arbitrator():
    return VivadaNirnayaEngine(sigma_strata=600.0, temperature_beta=3.5)


@pytest.fixture
def client():
    return TestClient(app)


# 1. Bhāratīya Civilization Engine Tests
def test_civilization_ksetra_and_geomorphology(civ_engine):
    """Validates Kṣetra sacred geography, Sarasvatī paleochannel, and maritime hubs."""
    sarasvati = civ_engine.lookup_ksetra("Sarasvati")
    assert sarasvati is not None
    assert sarasvati.category == "RIVER"
    assert "Kalibangan" in sarasvati.archaeological_sites
    assert "isro_paleochannel_radar" in sarasvati.scientific_evidence
    assert any("10.75" in ref for ref in sarasvati.textual_references)

    lothal = civ_engine.lookup_ksetra("Lothal")
    assert lothal is not None
    assert lothal.category == "PORT_MARITIME"
    assert "Dholavira" in lothal.archaeological_sites


def test_civilization_epigraphy_and_numismatics(civ_engine):
    """Validates primary epigraphic pillars: Aihole, Junāgaḍh, and Uttaramerūr."""
    aihole = civ_engine.lookup_epigraph("Aihole")
    assert aihole is not None
    assert aihole.ruler == "Pulakeśin II"
    assert any("3,735 years elapsed" in fact for fact in aihole.key_historical_facts)
    assert aihole.epistemic_confidence >= 0.95

    junagadh = civ_engine.lookup_epigraph("Junagadh")
    assert junagadh is not None
    assert "Candragupta Maurya" in " ".join(junagadh.key_historical_facts)
    assert "Aśoka Maurya" in " ".join(junagadh.key_historical_facts)

    uttaramerur = civ_engine.lookup_epigraph("Uttaramerur")
    assert uttaramerur is not None
    assert "Kudavolai" in " ".join(uttaramerur.key_historical_facts)


def test_civilization_material_science_and_institutions(civ_engine):
    """Validates indigenous technology (Wootz, Zawar, Kallanai) and institutions (Dharampal)."""
    wootz = civ_engine.lookup_material_science("Wootz")
    assert wootz is not None
    assert wootz.domain == "METALLURGY"
    assert any("Kodumanal" in site for site in wootz.primary_sites)

    zawar = civ_engine.lookup_material_science("Zawar")
    assert zawar is not None
    assert "distillation retorts" in zawar.physical_evidence_summary

    kallanai = civ_engine.lookup_material_science("Kallanai")
    assert kallanai is not None
    assert kallanai.domain == "HYDRAULIC_ENGINEERING"

    dharampal = civ_engine.lookup_institution("Dharampal")
    assert dharampal is not None
    assert "The Beautiful Tree" in dharampal.archival_evidence


# 2. Bhāratīya Culture Engine Tests
def test_culture_pancanga_mathematics(cult_engine):
    """Validates mathematical computation of Tithi, Nakṣatra, Yoga, Karaṇa, and Ṣaḍ-Ṛtu."""
    # Sun at 0° (Vernal Equinox / Mesha), Moon at 18° -> Tithi difference = 18° -> Dvitīyā (2nd Tithi)
    res = cult_engine.compute_pancanga(solar_deg=0.0, lunar_deg=18.0)
    assert res.tithi_number == 2
    assert "Dvitīyā" in res.tithi_name
    assert "Śukla Pakṣa" in res.paksha
    assert res.associated_season == RituSeason.VASANTA
    assert "Vasanta Ṛtucaryā" in res.seasonal_regimen

    # Test full Moon (180° separation) -> Pūrṇimā (15th Tithi)
    res_full = cult_engine.compute_pancanga(solar_deg=0.0, lunar_deg=180.0)
    assert res_full.tithi_number == 16 or res_full.tithi_number == 15


def test_culture_sodasa_samskaras(cult_engine):
    """Validates Ṣoḍaśa Saṃskāras lifecycle transitions and spiritual vs historical distinctions."""
    upanayana = cult_engine.lookup_samskara("Upanayana")
    assert upanayana is not None
    assert upanayana.stage == SamskaraStage.EDUCATIONAL_YOUTH
    assert "second birth" in upanayana.spiritual_ontological_core.lower()
    assert "Gārgī" in upanayana.historical_mutable_accretions

    vivaha = cult_engine.lookup_samskara("Vivāha")
    assert vivaha is not None
    assert vivaha.stage == SamskaraStage.HOUSEHOLDER_ADULT

    antyesti = cult_engine.lookup_samskara("Antyeṣṭi")
    assert antyesti is not None
    assert antyesti.stage == SamskaraStage.TRANSCENDENT


def test_culture_temple_ecosystem_and_lokacara(cult_engine):
    """Validates temple socio-economic-artistic ecosystem and Mīmāṃsā Lokācāra harmonization."""
    brihadisvara = cult_engine.lookup_temple_ecosystem("Brihadisvara")
    assert brihadisvara is not None
    assert brihadisvara.architectural_style == "DRAVIDA"
    assert len(brihadisvara.economic_functions) >= 2
    assert len(brihadisvara.arts_patronage) >= 2

    recon = cult_engine.reconcile_custom("Theyyam", "Kerala")
    assert recon["status"] == "VALID_LOKACARA_SAMANVAYA"
    assert "Śruti" in recon["jurisprudential_hierarchy"]


# 3. Propaganda Detector & ALEDT Tensor Tests
def test_propaganda_detector_four_vectors(prop_detector):
    """Validates regex and lexical detection across all 4 ideological distortion vectors."""
    # Vector 1: Colonial
    b1 = prop_detector.detect_bias("The white Aryan invaders conquered the dark primitive dravidian aborigines")
    assert b1.colonial_vector > 0.5
    assert len(b1.proofs) >= 1

    # Vector 2: Marxist
    b2 = prop_detector.detect_bias("A brahminical conspiracy to extract surplus from the working class explains this verse")
    assert b2.marxist_vector > 0.5

    # Vector 3: Theological
    b3 = prop_detector.detect_bias("This is filthy pagan heathen idolatry and devil worship that must be cleansed")
    assert b3.theological_vector > 0.5

    # Vector 4: Pseudoscience
    b4 = prop_detector.detect_bias("Vedic seers launched nuclear missiles and interplanetary spacecraft from Kurukshetra")
    assert b4.pseudoscience_vector > 0.5


def test_aledt_mathematical_tensor(prop_detector):
    """Validates the Attenuated Logistic Evidence-Distortion Tensor (ALEDT)."""
    evidence = {"epigraphy": 0.8, "textual_criticism": 0.8, "archaeology": 0.7, "astronomy_science": 0.7}

    # Case A: Minimal scholarly disagreement (bias = 0.20) -> should NOT collapse
    mild_bias = BiasProfile(colonial_vector=0.20)
    score_a, verdict_a, diag_a = prop_detector.compute_aledt_score(evidence, mild_bias)
    assert score_a >= 0.70
    assert "PRAMĀṆA_SIDDHA" in verdict_a

    # Case B: Verified severe propaganda (bias = 0.85) -> MUST collapse sharply
    severe_bias = BiasProfile(colonial_vector=0.85)
    score_b, verdict_b, diag_b = prop_detector.compute_aledt_score(evidence, severe_bias)
    assert score_b < 0.15
    assert "KŪṬA_YUKTI" in verdict_b


# 4. Vivāda-Nirṇaya Epistemic Arbitration Engine Tests
def test_vivada_nirnaya_continuous_anchor_kernel(arbitrator):
    """Validates that the Gaussian anchor kernel is continuous and has no step-function cliff."""
    strata = [ArchaeologicalStratumMatch("Hastinapur", "PGW", 900.0, 100.0, 0.90)]

    # Exactly matching stratum date
    k_exact, _ = arbitrator.compute_continuous_anchor_kernel(900.0, strata)
    assert k_exact >= 0.85

    # 300 years away
    k_300, _ = arbitrator.compute_continuous_anchor_kernel(1200.0, strata)
    # 600 years away (1 sigma)
    k_600, _ = arbitrator.compute_continuous_anchor_kernel(1500.0, strata)
    # 1200 years away (2 sigma)
    k_1200, _ = arbitrator.compute_continuous_anchor_kernel(2100.0, strata)

    # Must be monotonically decreasing without cliff
    assert k_exact > k_300 > k_600 > k_1200
    assert k_1200 >= 0.15  # Minimum baseline prior


def test_vivada_nirnaya_delta_t_ephemeris_uncertainty(arbitrator):
    """Validates physics-based quadratic Delta-T decay for pre-3100 BCE epochs."""
    p_3000, _ = arbitrator.compute_delta_t_ephemeris_multiplier(3000.0)
    assert p_3000 == 1.0  # Fully calibrated historical envelope

    p_5561, _ = arbitrator.compute_delta_t_ephemeris_multiplier(5561.0)
    assert 0.45 <= p_5561 <= 0.65  # Penalized due to non-linear tidal deceleration

    p_12209, _ = arbitrator.compute_delta_t_ephemeris_multiplier(12209.0)
    assert p_12209 < p_5561


def test_vivada_nirnaya_mahabharata_arbitration_benchmark(arbitrator):
    """
    Validates the exact benchmark test case requested by user:
    Nilesh Oak (5561 BCE) vs Traditional (3102 BCE) vs Late Archaeological (900 BCE).
    Verifies that:
    1. Output probabilities sum to 1.0 (normalized Dirichlet-Multinomial Bayesian posterior).
    2. Strongest pillars and fatal bottlenecks are correctly identified.
    3. Stratified reality assessment is populated without ideological dogmatism.
    """
    hypotheses = [
        ChronologicalHypothesis(
            name="High Antiquity Astronomical Model (5561 BCE)",
            proponent_or_school="Nilesh Nilkanth Oak",
            proposed_date_bce=5561.0,
            target_strata_level=TextualStrataLevel.JAYA_CORE,
            astronomy_raw_score=0.88,
            archaeology_raw_score=0.10,
            epigraphy_raw_score=0.20,
            linguistics_raw_score=0.15,
            hermeneutics_raw_score=0.60,
            cherry_pick_penalty=0.25,
            verified_strata=[
                ArchaeologicalStratumMatch("Mehrgarh", "Pre-Harappan Lithic", 5500.0, 500.0, 0.15)
            ]
        ),
        ChronologicalHypothesis(
            name="Traditional Epigraphic & Archaeo-Astronomy Horizon (3102–3067 BCE)",
            proponent_or_school="Aihole Inscription, Aryabhata, Dr. Narahari Achar",
            proposed_date_bce=3102.0,
            target_strata_level=TextualStrataLevel.JAYA_CORE,
            astronomy_raw_score=0.82,
            archaeology_raw_score=0.55,
            epigraphy_raw_score=0.92,
            linguistics_raw_score=0.60,
            hermeneutics_raw_score=0.85,
            cherry_pick_penalty=0.10,
            verified_strata=[
                ArchaeologicalStratumMatch("Kurukshetra / Kalibangan", "Early Harappan / Pre-PGW", 3000.0, 300.0, 0.65)
            ]
        ),
        ChronologicalHypothesis(
            name="Late Materialist Archaeological Redaction (c. 950–850 BCE)",
            proponent_or_school="B.B. Lal (Hastinapur Excavations), Mainstream Academia",
            proposed_date_bce=900.0,
            target_strata_level=TextualStrataLevel.MAHABHARATA_ENCYCLOPEDIC,
            astronomy_raw_score=0.15,
            archaeology_raw_score=0.95,
            epigraphy_raw_score=0.40,
            linguistics_raw_score=0.80,
            hermeneutics_raw_score=0.40,
            cherry_pick_penalty=0.35,
            verified_strata=[
                ArchaeologicalStratumMatch("Hastinapur", "PGW Flood Layer", 900.0, 100.0, 0.95)
            ]
        )
    ]

    results = arbitrator.arbitrate(hypotheses)
    assert len(results) == 3

    # Bayesian posterior probabilities must sum to 1.0
    total_posterior = sum(r.posterior_probability for r in results)
    assert pytest.approx(total_posterior, 0.01) == 1.0

    # Traditional corridor carries highest triangulated evidence
    assert results[0].hypothesis_name == "Traditional Epigraphic & Archaeo-Astronomy Horizon (3102–3067 BCE)"
    assert results[0].posterior_probability > results[1].posterior_probability
    assert "Epigraphic" in results[0].strongest_pillar

    # Nilesh Oak model is accurately diagnosed with archaeological void bottleneck
    oak_res = [r for r in results if "5561" in r.hypothesis_name][0]
    assert "Archaeological Void" in oak_res.fatal_bottleneck
    assert "astronomical memory" in oak_res.stratified_reality_assessment.lower()


# 5. Multi-Agent Orchestration & FastAPI Endpoints Tests
def test_multi_agent_orchestrator_routing():
    """Validates MasterOrchestrator dispatch to ItihasaVettaAgent and SamskritiGuruAgent."""
    orch = MasterOrchestrator()

    # Civilizational Epigraph dispatch
    res_epi = orch.process_query("tell me about Aihole Inscription")
    assert "Aihole" in res_epi.direct_answer
    assert res_epi.evidence_status.textual_confidence.value == "HIGH"

    # Cultural Samskara dispatch
    res_sam = orch.process_query("what is the meaning of Vivaha?")
    assert "Vivāha" in res_sam.direct_answer
    assert res_sam.evidence_status.textual_confidence.value == "HIGH"


def test_fastapi_endpoints_civilization_culture_arbitration(client):
    """Validates that all new REST API endpoints respond with correct schemas and status codes."""
    # 1. Civilization
    r1 = client.get("/civilization/entity/Sarasvati")
    assert r1.status_code == 200
    assert r1.json()["category"] == "RIVER"

    r2 = client.get("/civilization/epigraph/Aihole")
    assert r2.status_code == 200
    assert "Pulakeśin" in r2.json()["ruler"]

    # 2. Culture Pañcāṅga
    r3 = client.post("/culture/pancanga", json={"solar_deg": 15.0, "lunar_deg": 40.0})
    assert r3.status_code == 200
    assert "tithi" in r3.json()
    assert "season" in r3.json()

    # 3. Propaganda Analysis
    r4 = client.post("/verification/propaganda-analysis", json={"claim_text": "White aryan conquest destroyed dravidians"})
    assert r4.status_code == 200
    assert r4.json()["bias_vectors"]["colonial_eurocentric"] > 0.4
    assert "KŪṬA_YUKTI" in r4.json()["verdict"]

    # 4. Vivāda-Nirṇaya
    payload = [
        {
            "name": "Hypothesis 1",
            "proposed_date_bce": 3102,
            "target_strata_level": "JAYA_CORE",
            "astronomy_raw_score": 0.8,
            "archaeology_raw_score": 0.6,
            "epigraphy_raw_score": 0.9,
            "linguistics_raw_score": 0.6,
            "hermeneutics_raw_score": 0.8
        },
        {
            "name": "Hypothesis 2",
            "proposed_date_bce": 1000,
            "target_strata_level": "MAHABHARATA_ENCYCLOPEDIC",
            "astronomy_raw_score": 0.2,
            "archaeology_raw_score": 0.9,
            "epigraphy_raw_score": 0.3,
            "linguistics_raw_score": 0.8,
            "hermeneutics_raw_score": 0.4
        }
    ]
    r5 = client.post("/verification/vivada-nirnaya", json=payload)
    assert r5.status_code == 200
    data = r5.json()
    assert len(data) == 2
    assert "posterior_probability" in data[0]
