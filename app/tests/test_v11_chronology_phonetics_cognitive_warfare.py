"""
AI ĀCHĀRYA — Standing Test Suite for Version 11.0 (app/tests/test_v11_chronology_phonetics_cognitive_warfare.py)
Validates:
1. Rigvedic Chronological Arbitration (3-tier Bayesian benchmarks, Sarasvatī hydrology, Bhirrana Neolithic anchor decay).
2. Pāṇinian Articulatory Phonetics & Niroṣṭhya Audit (lip-free poetry vs labial infractions in Devanagari and IAST).
3. Citra-Kāvya Constraint Engine (Ekākṣarī single-consonant, Dvyakṣarī dual-consonant, Gatapratiyāgata palindromes).
4. Cognitive Warfare Extended Micro-Signals (commercial funnel hooks, regional statistical fabrications, geo-economic blindspots).
5. Master Orchestrator FSM States 9 and 10 routing.
6. FastAPI REST endpoints for v11 chronology and phonetics.
"""

import pytest
from fastapi.testclient import TestClient
from app.api.main import app
from app.verification.vivada_nirnaya import VivadaNirnayaEngine
from app.sanskrit.phonetics_engine import PaninianPhoneticsEngine
from app.intelligence.micro_signals import MicroSignalForensicParser, MicroSignalCategory
from app.orchestration.multi_agent import MasterOrchestrator


client = TestClient(app)


def test_rigveda_3tier_bayesian_chronology_arbitration():
    """Validates multi-pillar Bayesian chronological arbitration for Rigveda hypotheses."""
    engine = VivadaNirnayaEngine()
    benchmarks = engine.get_default_rigveda_benchmarks()
    assert len(benchmarks) == 3

    results = engine.arbitrate_rigveda_chronology()
    assert len(results) == 3

    # Primary hypothesis must be Sarasvatī Hydrological Floruit
    top = results[0]
    assert "Sarasvatī Hydrological" in top.hypothesis_name
    assert top.posterior_probability >= 0.50
    assert "PROBABLE_PRIMARY_CORRIDOR" in top.epistemic_status
    assert top.anchor_decay_multiplier >= 0.80

    # 7500 BCE Bhirrana must suffer severe anchor decay penalty (< 0.25)
    bhirrana_res = next(r for r in results if "Bhirrana" in r.hypothesis_name)
    assert bhirrana_res.proposed_date_bce == 7500.0
    assert bhirrana_res.anchor_decay_multiplier <= 0.25
    assert "Archaeological Void" in bhirrana_res.fatal_bottleneck or "Stratigraphic" in bhirrana_res.fatal_bottleneck or "BCE" in bhirrana_res.fatal_bottleneck
    assert bhirrana_res.posterior_probability < 0.15

    # Colonial Minimalist model (1300 BCE)
    colonial_res = next(r for r in results if "Colonial" in r.hypothesis_name)
    assert colonial_res.posterior_probability < 0.20


def test_paninian_niroshthya_audit_pure_vs_infraction():
    """Validates Niroṣṭhya constraint validation: lip-free verses vs labial infractions."""
    # 1. Pure Devanagari Niroṣṭhya text (Ka, Kha, Ga, Ta, Tha, Da, Na, Cha, Ja, Ra, Sa, etc. - no lips)
    pure_deva = "कनक कान्त कार्तिकेय कीर्ति कान्ति काश"
    res_pure = PaninianPhoneticsEngine.audit_niroshthya(pure_deva)
    assert res_pure.is_niroshthya is True
    assert res_pure.labial_count == 0
    assert "PERFECT NIROṢṬHYA COMPOSITION" in res_pure.forensic_critique

    # 2. Devanagari with labials (pa, pha, ba, bha, ma, u, oo)
    labial_deva = "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन"
    res_impure = PaninianPhoneticsEngine.audit_niroshthya(labial_deva)
    assert res_impure.is_niroshthya is False
    assert res_impure.labial_count >= 2
    assert any(sym in res_impure.detected_labial_symbols for sym in ['म', 'फ'])

    # 3. IAST Niroṣṭhya audit
    pure_iast = "kanaka kānta kārtikeya kīrti"
    res_iast_pure = PaninianPhoneticsEngine.audit_niroshthya(pure_iast)
    assert res_iast_pure.is_niroshthya is True

    # 4. IAST with labials (p, m, b, u, au)
    impure_iast = "puruṣa mātā pitā bandhu gauro"
    res_iast_impure = PaninianPhoneticsEngine.audit_niroshthya(impure_iast, strict_mode=True)
    assert res_iast_impure.is_niroshthya is False
    assert res_iast_impure.labial_count >= 5
    assert "au" in res_iast_impure.detected_labial_symbols


def test_citra_kavya_constraints():
    """Validates extreme Citra-kāvya poetic constraints (Ekākṣarī, Dvyakṣarī, Palindromes)."""
    # 1. Ekākṣarī (Single consonant - all 'na' like Bharavi's Kiratarjuniya 15.14)
    ekaksari_verse = "नाना नना ननु नून नन नन नून नानानना"
    res_eka = PaninianPhoneticsEngine.audit_citra_kavya(ekaksari_verse)
    assert res_eka.is_ekaksari is True
    assert res_eka.distinct_consonants_count == 1
    assert "न" in res_eka.distinct_consonants
    assert "Ekākṣarī" in res_eka.pattern_name

    # 2. Dvyakṣarī (Two consonants - all 'ta' and 'da')
    dvyaksari_verse = "तात तात तात ताद दात दाद दात तात"
    res_dvya = PaninianPhoneticsEngine.audit_citra_kavya(dvyaksari_verse)
    assert res_dvya.is_dvyaksari is True
    assert res_dvya.distinct_consonants_count == 2
    assert "Dvyakṣarī" in res_dvya.pattern_name

    # 3. Palindrome (Gatapratiyāgata / bidirectional symmetry)
    palindrome_verse = "तं न सा कुरुते तारं रं ता ते रु कु सा न तं"
    res_pal = PaninianPhoneticsEngine.audit_citra_kavya(palindrome_verse)
    assert res_pal.is_palindrome is True
    assert "Gatapratiyāgata" in res_pal.pattern_name or "Palindrome" in res_pal.pattern_name


def test_cognitive_warfare_extended_microsignals():
    """Validates new micro-signal detectors: commercial funnels, statistical fabrications, supply chain blindspots."""
    # 1. Commercial Funnel Hook
    text_funnel = "Click the link in bio right now to join our exclusive masterclass before seats run out and enroll today!"
    rep_funnel = MicroSignalForensicParser.analyze_text(text_funnel)
    categories_funnel = [s.category for s in rep_funnel.detected_signals]
    assert MicroSignalCategory.COMMERCIAL_FUNNEL_HOOK in categories_funnel

    # 2. Regional Statistical Fabrication
    text_stats = "Recent survey reveals that 9 out of 10 people in this region hate foreigners and nearly 85 percent confirmed it."
    rep_stats = MicroSignalForensicParser.analyze_text(text_stats)
    categories_stats = [s.category for s in rep_stats.detected_signals]
    assert MicroSignalCategory.REGIONAL_STATISTICAL_FABRICATION in categories_stats

    # 3. Geo-Economic Supply Chain Blindspot
    text_supply = "The geopolitical crisis will cause critical mineral shortages, disrupt semiconductor supply chains, and trigger shipping lane port blockades."
    rep_supply = MicroSignalForensicParser.analyze_text(text_supply)
    categories_supply = [s.category for s in rep_supply.detected_signals]
    assert MicroSignalCategory.GEO_ECONOMIC_SUPPLY_CHAIN_BLINDSPOT in categories_supply


def test_master_orchestrator_states_9_and_10():
    """Validates Master Orchestrator FSM State 9 (Rigveda Chronology) and State 10 (Pāṇinian Phonetics)."""
    mo = MasterOrchestrator()

    # State 9: Rigveda Chronological Arbitration
    query_rig = "rigveda dating: is it 9500 year old rigveda or 3000 bce sarasvati?"
    resp_rig = mo.process_query(query_rig)
    assert "Ṛgveda Chronological Arbitration" in resp_rig.direct_answer or "Sarasvatī" in resp_rig.direct_answer
    assert resp_rig.visual_forensic_card is not None
    assert "3000–1900 BCE" in resp_rig.visual_forensic_card

    # State 10: Pāṇinian Phonetics & Niroṣṭhya Audit
    query_phon = "niroshthya audit of sanskrit verse without lips: कनक कान्त कार्तिकेय"
    resp_phon = mo.process_query(query_phon)
    assert "Pāṇinian Phonetic & Constraint Audit" in resp_phon.direct_answer
    assert resp_phon.visual_forensic_card is not None
    assert "PĀṆINIAN ARTICULATORY PHONETICS" in resp_phon.visual_forensic_card


def test_fastapi_v11_endpoints():
    """Validates FastAPI REST endpoints exposed in Version 11.0."""
    # 1. Rigveda Chronology Arbitration
    res_chron = client.post("/verification/chronology/rigveda-arbitration", json=None)
    assert res_chron.status_code == 200
    data_chron = res_chron.json()
    assert len(data_chron) == 3
    assert "Sarasvatī" in data_chron[0]["hypothesis_name"]
    assert data_chron[0]["posterior_probability"] >= 0.50

    # 2. Niroṣṭhya Audit (pure verse)
    res_niro = client.post("/sanskrit/phonetics/niroshthya-audit", json={"text": "कनक कान्त कार्तिकेय", "strict_mode": True})
    assert res_niro.status_code == 200
    data_niro = res_niro.json()
    assert data_niro["is_niroshthya"] is True
    assert data_niro["labial_count"] == 0

    # 3. Niroṣṭhya Audit (infraction verse)
    res_niro_bad = client.post("/sanskrit/phonetics/niroshthya-audit", json={"text": "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन", "strict_mode": True})
    assert res_niro_bad.status_code == 200
    data_niro_bad = res_niro_bad.json()
    assert data_niro_bad["is_niroshthya"] is False
    assert data_niro_bad["labial_count"] >= 2

    # 4. Citra-Kāvya Audit (Ekākṣarī)
    res_citra = client.post("/sanskrit/phonetics/citra-kavya-audit", json={"text": "नाना नना ननु नून नन नन नून नानानना"})
    assert res_citra.status_code == 200
    data_citra = res_citra.json()
    assert data_citra["is_ekaksari"] is True
    assert data_citra["distinct_consonants_count"] == 1
