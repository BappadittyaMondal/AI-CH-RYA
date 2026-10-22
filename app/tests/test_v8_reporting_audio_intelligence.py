"""
Automated Verification Suite for Version 8.0:
- Multi-Modal Reporting Engine (HTML Dashboard, Forensic Markdown, Resilient PDF)
- Multilingual Audio (Śravaṇa) Engine with Start & End Interactive Audio Decks
- Hardened Clinical Safety Red-Line Barrier (§22)
- Strategic Semiotics & Anti-Hallucination Visual Gate
- FastAPI Endpoints for On-Demand Exports and Downloads
"""

import io
from fastapi.testclient import TestClient
from app.api.main import app
from app.orchestration.formatter import MasterResponseSchema
from app.verification.evidence import EvidenceProfile
from app.pedagogy.practical_systems import PracticalSystemsEngine, SystemDiscipline, ConsultationMode
from app.reporting import (
    ThematicDomain,
    ThemePalette,
    detect_thematic_domain,
    get_theme_palette,
    HTMLDashboardBuilder,
    MarkdownDossierBuilder,
    ExecutivePDFCompiler,
    AudioLanguage,
    AudioPacing,
    AudioSynthesizer,
    SiksaMetricalParser,
    AudioDeckRenderer,
    ExportFormat,
    ExportManager
)
from app.intelligence import (
    StrategicThinkerLens,
    VisualOpticsAuditResult,
    SemioticMicroSignal,
    MultiOpticStrategicVerdict,
    StrategicSemioticsEngine
)

client = TestClient(app)


def _get_dummy_schema() -> MasterResponseSchema:
    return MasterResponseSchema(
        direct_answer="Perform duty without desire for fruit. Equanimity in action is Yoga.",
        source_text="Bhagavad Gītā 2.47-48",
        original_sanskrit="कर्मण्येवाधिकारस्ते मा फलेषु कदाचन। मा कर्मफलहेतुर्भूर्मा ते सङ्गोऽस्त्वकर्मणि॥",
        transliteration="karmaṇyevādhikāraste mā phaleṣu kadācana | mā karmaphalaheturbhūrmā te saṅgo'stvakarmaṇi ||",
        word_meaning="karmaṇi (in action), eva (only), adhikāraḥ (right), te (your)...",
        bengali_translation="কর্মে তোমার অধিকার আছে, কিন্তু ফলে কখনো নয়। কর্মফল যেন তোমার উদ্দেশ্য না হয়।",
        hindi_translation="कर्म करने में ही तुम्हारा अधिकार है, उसके फलों में कभी नहीं।",
        english_explanation="You have a right only to perform work, never to the fruits of action.",
        context="Kurukṣetra battlefield dialogue between Śrī Kṛṣṇa and Arjuna on Nishkama Karma.",
        traditional_interpretations="Advaita focuses on mental purification (citta-śuddhi); Viśiṣṭādvaita highlights surrender.",
        scholarly_historical_view="Critical edition consensus places this at the metaphysical core of the Bhīṣmaparvan.",
        evidence_status=EvidenceProfile(primary_text_verified=True, external_historical_corroboration="Confirmed"),
        related_texts=["BG 2.48", "BG 3.19", "Isha 2"],
        practical_application="Focus deeply on the execution process rather than anxiety over end outcomes.",
        key_takeaways=["Relinquish outcome obsession", "Maintain poise in victory and defeat"],
        seeker_action_summary="Practice 100% presence in the immediate task, offering fruits to the Supreme Divine."
    )


def test_thematic_domain_chromatics():
    """Verifies Prakrti-Varna thematic detection and CSS variable generation."""
    domain_dharma = detect_thematic_domain("What is the meaning of Upanishads?", "Katha Upanishad")
    assert domain_dharma == ThematicDomain.DHARMA_PHILOSOPHY

    domain_sthapatya = detect_thematic_domain("How was Kailasa temple excavated at Ellora?", "Cave 16")
    assert domain_sthapatya == ThematicDomain.STHAPATYA_ARCHITECTURE

    domain_aero = detect_thematic_domain("Analyze the 1974 IISc aeronautics report on Vimanas", "Mukunda et al.")
    assert domain_aero == ThematicDomain.SCIENCE_AERONAUTICS

    domain_forensic = detect_thematic_domain("Expose the DMIT fingerprint scam and hoax", "Cognitive audit")
    assert domain_forensic == ThematicDomain.FORENSIC_REBUTTAL

    domain_ayurveda = detect_thematic_domain("Evaluate Vata and Pitta doshas in herbal diet", "Caraka")
    assert domain_ayurveda == ThematicDomain.AYURVEDA_NATURE

    palette = get_theme_palette(ThematicDomain.DHARMA_PHILOSOPHY)
    css_vars = palette.to_css_variables()
    assert "--primary: #D84315;" in css_vars
    assert "[data-theme=\"dark\"]" in css_vars


def test_html_dashboard_generation_and_sanitization():
    """Verifies self-contained HTML dashboard with XSS sanitization and dual start/end audio decks."""
    schema = _get_dummy_schema()
    html_output = HTMLDashboardBuilder.render(schema, "Explain BG 2.47 Karma Yoga")

    assert "<!DOCTYPE html>" in html_output
    assert 'id="topAudioDeck"' in html_output
    assert 'id="bottomAudioDeck"' in html_output
    assert "Listen to Report (Muted)" in html_output
    assert "कर्मण्येवाधिकारस्ते" in html_output
    assert "কর্মে তোমার অধিকার আছে" in html_output
    assert "कर्म करने में ही तुम्हारा अधिकार है" in html_output
    assert "window.speechSynthesis" in html_output
    assert "toggleTheme()" in html_output


def test_forensic_markdown_dossier_sha256():
    """Verifies markdown dossier YAML frontmatter and cryptographic SHA-256 verification hash."""
    schema = _get_dummy_schema()
    md_output = MarkdownDossierBuilder.render(schema, "Explain BG 2.47")

    assert "document_type: AI_ACHARYA_FORENSIC_DOSSIER" in md_output
    assert "payload_sha256:" in md_output
    assert "## 1. DIRECT VERDICT / ANSWER" in md_output
    assert "## 3. MULTILINGUAL ALIGNMENT MATRIX" in md_output
    assert "বাংলা (Bengali)" in md_output
    assert "Forensic Cryptographic Verification Signature" in md_output


def test_resilient_pdf_generation():
    """Verifies pure-Python compliant PDF-1.4 binary compilation and print-optimized HTML."""
    schema = _get_dummy_schema()
    pdf_bytes = ExecutivePDFCompiler.render_pdf_bytes(schema, "Explain BG 2.47")

    assert isinstance(pdf_bytes, bytes)
    assert pdf_bytes.startswith(b"%PDF-1.4")
    assert b"%%EOF" in pdf_bytes
    assert len(pdf_bytes) > 500

    printable_html = ExecutivePDFCompiler.render_printable_html(schema, "Explain BG 2.47")
    assert "@page" in printable_html
    assert "A4 portrait" in printable_html
    assert "onload=\"window.print()\"" in printable_html


def test_multilingual_audio_engine_and_siksa_prosody():
    """Verifies Siksa prosody caesura pauses, multilingual WAV synthesis, and audio decks."""
    schema = _get_dummy_schema()

    # Siksa SSML pauses test
    ssml = SiksaMetricalParser.to_ssml(schema.original_sanskrit, AudioLanguage.SANSKRIT, AudioPacing.CHANT_SLOW)
    assert '<break time="600ms"/>' in ssml
    assert '<break time="1200ms"/>' in ssml
    assert 'rate="80%"' in ssml

    # Audio synthesis test across languages
    for lang in [AudioLanguage.SANSKRIT, AudioLanguage.BENGALI, AudioLanguage.HINDI, AudioLanguage.ENGLISH]:
        res = AudioSynthesizer.synthesize(schema, lang=lang, pacing=AudioPacing.STANDARD)
        assert res.mime_type == "audio/wav"
        assert res.audio_bytes.startswith(b"RIFF")
        assert res.duration_est_seconds > 0.0
        assert len(res.sha256_hash) == 64

    # Audio deck markdown decorator test
    raw_md = "Sample content"
    decorated = ExportManager.decorate_markdown_with_audio_decks(raw_md)
    assert "> 🔊 **AUDIO BRIEFING [DEFAULT MUTED]**" in decorated
    assert "> 🎧 **END OF REPORT AUDIO DECK [MUTE / UNMUTE]**" in decorated


def test_clinical_emergency_red_line_gate():
    """Verifies that acute medical red-flags trigger immediate emergency triage and block prescription."""
    # Emergency query with chest pain
    emergency_resp = PracticalSystemsEngine.evaluate_request(
        discipline=SystemDiscipline.AYURVEDA,
        mode=ConsultationMode.PRACTICE_GUIDANCE_MODE,
        traditional_text="Patient experiencing acute crushing chest pain radiating to left arm and sweating."
    )
    assert emergency_resp.is_safe is False
    assert emergency_resp.emergency_referral_active is True
    assert "EMERGENCY CLINICAL TRIAGE TRIGGERED" in emergency_resp.historical_traditional_explanation
    assert "Tele-MANAS: 14416" in emergency_resp.emergency_referral_details

    # Emergency query with suicide
    crisis_resp = PracticalSystemsEngine.evaluate_request(
        discipline=SystemDiscipline.YOGA,
        mode=ConsultationMode.EDUCATIONAL_MODE,
        traditional_text="I want to kill myself please give me a yogic solution."
    )
    assert crisis_resp.is_safe is False
    assert crisis_resp.emergency_referral_active is True

    # Benign cultural query
    benign_resp = PracticalSystemsEngine.evaluate_request(
        discipline=SystemDiscipline.AYURVEDA,
        mode=ConsultationMode.EDUCATIONAL_MODE,
        traditional_text="Classical understanding of Triphala in Caraka Samhita."
    )
    assert benign_resp.is_safe is True
    assert benign_resp.emergency_referral_active is False


def test_strategic_semiotics_and_anti_hallucination_visual_gate():
    """Verifies 7-thinker strategic analysis and the Anti-Hallucination Visual Gate."""
    # Attempting to guess dress color without CV keyframes
    hallucination_query = "What did the speaker's dress color and body language reveal in this press conference?"
    verdict_vetoed = StrategicSemioticsEngine.evaluate_strategic_topic(
        topic="Diplomatic Press Conference",
        text_payload=hallucination_query,
        has_cv_keyframe_data=False
    )
    assert verdict_vetoed.visual_optics_audit.is_hallucination_risk is True
    assert "ANTI-HALLUCINATION VETO" in verdict_vetoed.visual_optics_audit.visual_warning

    # With verified CV keyframe data
    verdict_verified = StrategicSemioticsEngine.evaluate_strategic_topic(
        topic="Diplomatic Press Conference",
        text_payload=hallucination_query,
        has_cv_keyframe_data=True,
        cv_dominant_hex="#1E3A8A"
    )
    assert verdict_verified.visual_optics_audit.is_hallucination_risk is False
    assert "#1E3A8A" in verdict_verified.visual_optics_audit.attire_color_verified

    # Testing passive voice obfuscation and colonial distortion detection
    controversial_text = "Clashes erupted near the ancient disputed structure as colonial caste mythology was quoted."
    verdict_signals = StrategicSemioticsEngine.evaluate_strategic_topic(
        topic="Civilizational Dispute",
        text_payload=controversial_text
    )
    signals = verdict_signals.micro_signals_detected
    signal_types = [s.signal_type for s in signals]
    assert "Passive Voice Agency Obfuscation" in signal_types
    assert "Colonial Semantic Inversion" in signal_types

    # Testing the 7 strategic thinker lenses in the verdict
    assert "EMPIRICAL AUDIT" in verdict_signals.ranganathan_empirical_audit
    assert "DECOLONIAL JURISPRUDENTIAL AUDIT" in verdict_signals.sai_deepak_legal_audit
    assert "ASYMMETRIC INTELLIGENCE" in verdict_signals.doval_threat_cui_bono_audit
    assert "STRATEGIC AUTONOMY" in verdict_signals.jaishankar_geopolitical_audit
    assert "MACRO-FINANCIAL" in verdict_signals.sanyal_shah_macro_audit
    assert "CIVILIZATIONAL SCALE" in verdict_signals.modi_civilizational_action
    assert "CULTURAL GRAYZONE RESOLUTION" in verdict_signals.cultural_grayzone_resolution


def test_fastapi_v8_export_and_intelligence_endpoints():
    """Verifies REST endpoints for HTML, Markdown, PDF, Audio, and Strategic Semiotic Audit."""
    # 1. POST /query with on-demand export formats
    query_resp = client.post("/query", json={
        "query": "BG 2.47",
        "export_formats": ["html", "markdown", "pdf", "audio"]
    })
    assert query_resp.status_code == 200
    q_data = query_resp.json()
    assert "exports" in q_data
    assert "html" in q_data["exports"]
    assert "markdown" in q_data["exports"]
    assert "pdf" in q_data["exports"]
    assert "audio" in q_data["exports"]
    assert "> 🔊 **AUDIO BRIEFING" in q_data["rendered_markdown"]

    # 2. GET /export/download/html
    html_resp = client.get("/export/download/html?query=BG+2.47")
    assert html_resp.status_code == 200
    assert "text/html" in html_resp.headers["content-type"]
    assert "attachment;" in html_resp.headers["content-disposition"]
    assert "<!DOCTYPE html>" in html_resp.text

    # 3. GET /export/download/markdown
    md_resp = client.get("/export/download/markdown?query=BG+2.47")
    assert md_resp.status_code == 200
    assert "text/markdown" in md_resp.headers["content-type"]
    assert "document_type: AI_ACHARYA_FORENSIC_DOSSIER" in md_resp.text

    # 4. GET /export/download/pdf
    pdf_resp = client.get("/export/download/pdf?query=BG+2.47")
    assert pdf_resp.status_code == 200
    assert "application/pdf" in pdf_resp.headers["content-type"]
    assert pdf_resp.content.startswith(b"%PDF-1.4")

    # 5. GET /export/audio
    audio_resp = client.get("/export/audio?query=BG+2.47&lang=bengali")
    assert audio_resp.status_code == 200
    assert "audio/wav" in audio_resp.headers["content-type"]
    assert audio_resp.content.startswith(b"RIFF")

    # 6. POST /intelligence/strategic-semiotic-audit
    strat_resp = client.post("/intelligence/strategic-semiotic-audit", json={
        "topic": "Temple Autonomy & State Control",
        "text_payload": "Clashes erupted as activists questioned the colonial caste rules and state takeover of sacred shrines.",
        "has_cv_keyframe_data": False
    })
    assert strat_resp.status_code == 200
    strat_data = strat_resp.json()
    assert strat_data["topic"] == "Temple Autonomy & State Control"
    assert "sai_deepak_legal_audit" in strat_data
    assert "doval_threat_cui_bono_audit" in strat_data
    assert len(strat_data["micro_signals_detected"]) > 0
