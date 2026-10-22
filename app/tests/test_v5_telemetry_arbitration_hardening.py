"""
AI ĀCHĀRYA — Test Suite for v5.0 Telemetry, Causal Stratification, Strategic Realpolitik & FSM Orchestration
(app/tests/test_v5_telemetry_arbitration_hardening.py)
"""

import pytest
from app.verification.propaganda_detector import (
    PropagandaDetector,
    DistortionVector,
    ForensicStratumLevel,
    StratifiedTierScore,
    StratifiedForensicReport
)
from app.civilization.strategic import StrategicRealpolitikEngine
from app.ingestion.youtube import YouTubeEngine, ASRPhoneticNormalizer, YouTubeEvidenceLevel
from app.orchestration.multi_agent import MasterOrchestrator
from app.orchestration.formatter import MasterResponseSchema


def test_propaganda_detector_hoax_index_patterns():
    """Verifies that borrowed Western apocalyptic hoaxes and commercial interpolations are flagged."""
    detector = PropagandaDetector()

    # 1. Nostradamus 9/11 iron birds hoax (Neil Marshall 1997)
    prof_911 = detector.detect_bias("Nostradamus predicted two twin brothers will be destroyed by birds of iron in 9/11")
    assert prof_911.pseudoscience_vector >= 0.80
    assert any("Neil Marshall" in p.identified_fallacy for p in prof_911.proofs)

    # 2. Nostradamus Hister mistranslation
    prof_hister = detector.detect_bias("Centuries ago Nostradamus saw that Hister was Hitler coming to conquer Europe")
    assert any("Lower Danube River" in p.identified_fallacy for p in prof_hister.proofs)

    # 3. Modern political print chapbook interpolation
    prof_pol = detector.detect_bias("Ancient Malika palm leaves predicted Vajpayee would rule for 13 days and Pakistan partition")
    assert any("Modern political figures are post-1970s print chapbook additions" in p.identified_fallacy for p in prof_pol.proofs)

    # 4. Ancient alien temple laser hoax
    prof_alien = detector.detect_bias("Ancient aliens built temples with alien lasers and Shiva Lingam was an alien rocket")
    assert prof_alien.pseudoscience_vector >= 0.80
    assert any("Ancient Astronaut Fallacy" in p.identified_fallacy for p in prof_alien.proofs)


def test_propaganda_detector_multiplicative_causal_veto():
    """
    Verifies that the non-compensatory multiplicative causal veto gate (gamma_causal)
    strictly collapses prophetic validity to 0.0 even if physical events occurred at 90%.
    """
    detector = PropagandaDetector()

    tier1 = StratifiedTierScore(
        tier=ForensicStratumLevel.TIER_1_PHYSICAL_EMPIRICAL,
        factual_reality=0.95,
        propaganda_distortion=0.05,
        causal_attribution_valid=False,  # Storm occurred physically, but prophecy link is ungrounded
        dimension_name="Meteorological Cyclone",
        evidence_justification="Severe Category 4 Cyclone occurred physically."
    )
    tier4 = StratifiedTierScore(
        tier=ForensicStratumLevel.TIER_4_CANONICAL_ASTRONOMICAL_MATH,
        factual_reality=0.0,
        propaganda_distortion=1.0,
        causal_attribution_valid=False,
        dimension_name="Surya Siddhanta Astronomical Timeline",
        evidence_justification="432,000-year cycle has over 426,000 years remaining; 2032 claim is false."
    )

    # When causal attribution is invalid, gamma_causal is 0.0
    report = detector.compute_stratified_forensic_matrix([tier1, tier4], gamma_causal=0.0)

    # Composite factual reality shows that physical events happened
    assert report.composite_factual_reality > 0.40
    # But prophetic causal reality strictly collapses to 0.0 (non-compensatory veto)
    assert report.prophetic_causal_reality == 0.0
    assert report.gamma_causal_veto == 0.0
    assert "POST_HOC_RATIONALIZATION" in report.summary_verdict


def test_strategic_realpolitik_engine():
    """Verifies Kautilyan statecraft and modern ORBAT evaluation of geopolitical claims."""
    engine = StrategicRealpolitikEngine()

    # 1. Absurd multi-nation coalition against India
    res_absurd = engine.evaluate_claim("The US will join China, Pakistan, and 13 Islamic nations to destroy India in WW3 while Russia converts to Hinduism")
    assert res_absurd.plausibility_score <= 0.10
    assert "MYTHOLOGICAL_FANTASY" in res_absurd.status
    assert len(res_absurd.structural_contradictions) >= 2

    # 2. Grounded two-front deterrence
    res_grounded = engine.evaluate_claim("India maintains active two-front defense planning along the LAC and LoC under HQ IDS")
    assert res_grounded.plausibility_score >= 0.80
    assert "GROUNDED_STRATEGIC_REALITY" in res_grounded.status


def test_youtube_asr_phonetic_normalizer_and_caching():
    """Verifies phonetic correction of Indic terms and deterministic caching."""
    raw_noisy_asr = "The panch sakha saint achutanand spoke of neelam chakra and madala panji regarding yug sandhi"
    clean_txt = ASRPhoneticNormalizer.normalize_text(raw_noisy_asr)

    assert "Pañcasakhā" in clean_txt
    assert "Achyutānanda" in clean_txt
    assert "Nīlacakra" in clean_txt
    assert "Mādaḷā Pāñji" in clean_txt
    assert "Yuga Sandhi" in clean_txt

    # Test deterministic caching in YouTubeEngine
    test_url = "https://www.youtube.com/watch?v=NrAwVI8ut_M"
    report1 = YouTubeEngine.analyze_source(test_url, provided_transcript="Test segment line 1\nTest segment line 2")
    assert len(report1.claims_extracted) >= 2

    # Second call without transcript should return from cache
    report2 = YouTubeEngine.analyze_source(test_url)
    assert report2.video_id == report1.video_id
    assert len(report2.claims_extracted) == len(report1.claims_extracted)


def test_master_orchestrator_fsm_media_routing():
    """Verifies that MasterOrchestrator routes media/apocalyptic queries through the FSM."""
    orch = MasterOrchestrator()
    query = "https://www.youtube.com/watch?v=NrAwVI8ut_M do you agree with this video? reality vs propaganda%"
    res = orch.process_query(query)

    assert "Epistemic Analysis" in res.direct_answer
    assert "Prophetic Causal Reality: 0.0%" in res.direct_answer
    assert res.seeker_action_summary is not None
    assert "NOT ending in 2032" in res.seeker_action_summary
    assert res.visual_forensic_card is not None
    assert "STRATIFIED REALITY EVALUATION" in res.render_markdown()
    assert "SEEKER ACTION & CLARITY SUMMARY" in res.render_markdown()


def test_master_orchestrator_fsm_arbitration_routing():
    """Verifies that MasterOrchestrator routes dating arbitration queries through Vivāda-Nirṇaya."""
    orch = MasterOrchestrator()
    query = "Which date of Mahabharata war is closer to reality: Nilesh Oak 5561 BCE or Traditional 3102 BCE?"
    res = orch.process_query(query)

    assert "Vivāda-Nirṇaya 5D Epistemic Arbitration" in res.direct_answer
    assert "Posterior:" in res.direct_answer
    assert "Aihole Inscription" in res.direct_answer
    assert res.evidence_status.textual_confidence.value == "HIGH"


def test_response_schema_visual_and_seeker_formatting():
    """Verifies MasterResponseSchema markdown assembly with seeker summary and visual cards."""
    schema = MasterResponseSchema(
        direct_answer="Direct answer text",
        source_text="Source Text",
        original_sanskrit="सत्यम्",
        transliteration="Satyam",
        word_meaning="Truth",
        bengali_translation="সত্য",
        hindi_translation="सत्य",
        english_explanation="Explanation",
        context="Context",
        traditional_interpretations="Interpretations",
        practical_application="Application",
        seeker_action_summary="Stay fearless and fulfill your Dharma.",
        visual_forensic_card="[VISUAL FORENSIC CARD]"
    )
    rendered = schema.render_markdown()
    assert "SEEKER ACTION & CLARITY SUMMARY" in rendered
    assert "Stay fearless and fulfill your Dharma" in rendered
    assert "[VISUAL FORENSIC CARD]" in rendered
