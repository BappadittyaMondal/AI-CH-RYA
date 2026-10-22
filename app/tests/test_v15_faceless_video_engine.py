"""
AI ĀCHĀRYA — Comprehensive Test Suite for Version 15.0:
Autonomous 100% Free Faceless Video Generation & Multi-Platform Production Engine (§18, §20)
"""

import os
import wave
import json
import tempfile
import pytest
from PIL import Image
from fastapi.testclient import TestClient

from app.video.storyboard import (
    VideoStoryboardDirector,
    VideoStoryboard,
    VideoFormat,
    CameraMotion
)
from app.video.audio_engine import (
    AudioNarrationEngine,
    ProceduralTanpuraGenerator,
    AudioMixerAndDucker,
    AudioConfig
)
from app.video.asset_generator import ProceduralAssetGenerator
from app.video.subtitles import SubtitleCompiler
from app.video.compositor import VideoCompositor, VideoRenderConfig
from app.video.generate import FacelessVideoProductionPipeline
from app.api.main import app, orchestrator


client = TestClient(app)


def test_storyboard_director_short_and_long_structure():
    """Validates scene beat breakdown, Devanāgarī typography, and SEO metadata."""
    # 1. Test 9:16 Short
    sb_short = VideoStoryboardDirector.create_storyboard(
        topic="BG 2.47",
        video_format=VideoFormat.SHORT_9_16,
        language="en"
    )
    assert sb_short.video_format == VideoFormat.SHORT_9_16
    assert len(sb_short.scenes) == 4
    assert "कर्मण्येवाधिकारस्ते" in sb_short.scenes[0].on_screen_devanagari
    assert "karmaṇy evādhikāras te" in sb_short.scenes[0].on_screen_iast
    assert sb_short.scenes[0].motion_type in CameraMotion
    assert "YouTube Shorts" in sb_short.target_platforms[0]

    # 2. Test 16:9 Long-Form
    sb_long = VideoStoryboardDirector.create_storyboard(
        topic="Purusha Sukta",
        video_format=VideoFormat.LONG_16_9,
        language="en"
    )
    assert sb_long.video_format == VideoFormat.LONG_16_9
    assert len(sb_long.scenes) == 6
    assert sb_long.total_duration_sec >= 450.0
    assert "सहस्रशीर्षा पुरुषः" in sb_long.scenes[0].on_screen_devanagari


def test_procedural_tanpura_synthesis():
    """Validates pure-Python procedural Tanpura drone and temple bell generation."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        out_wav = os.path.join(tmp_dir, "tanpura_test.wav")
        cfg = AudioConfig(sample_rate=44100, fundamental_hz=136.1)
        
        result_path = ProceduralTanpuraGenerator.generate_drone(
            duration_sec=2.0,
            output_path=out_wav,
            config=cfg,
            include_temple_bell=True
        )
        assert os.path.exists(result_path)
        
        with wave.open(result_path, "rb") as wf:
            assert wf.getnchannels() == 2
            assert wf.getsampwidth() == 2
            assert wf.getframerate() == 44100
            n_frames = wf.getnframes()
            # Approx 2 seconds
            assert 80000 <= n_frames <= 95000


def test_audio_narration_and_ducking_engine():
    """Validates neural narration synthesis and automated volume ducking mixer."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        voice_path = os.path.join(tmp_dir, "voice_test.wav")
        tanpura_path = os.path.join(tmp_dir, "tanpura_test.wav")
        mixed_path = os.path.join(tmp_dir, "mixed_test.wav")

        # 1. Synthesize voice
        synth_res = AudioNarrationEngine.synthesize_speech(
            text="Karma yoga teaches freedom from the anxiety of results.",
            output_path=voice_path,
            language="en"
        )
        assert os.path.exists(voice_path)
        assert synth_res["duration_sec"] > 1.0

        # 2. Synthesize ambient drone
        ProceduralTanpuraGenerator.generate_drone(
            duration_sec=synth_res["duration_sec"] + 1.0,
            output_path=tanpura_path,
            include_temple_bell=False
        )

        # 3. Mix and duck
        mixed_out = AudioMixerAndDucker.mix_tracks(
            voiceover_wav_path=voice_path,
            ambient_wav_path=tanpura_path,
            output_wav_path=mixed_path,
            voice_volume=1.0,
            ducked_ambient_vol=0.10,
            un_ducked_ambient_vol=0.25
        )
        assert os.path.exists(mixed_out)
        
        with wave.open(mixed_out, "rb") as wf:
            assert wf.getnchannels() == 2
            assert wf.getframerate() == 44100
            assert wf.getnframes() > 10000


def test_procedural_asset_generator_dimensions_and_palettes():
    """Validates 1080x1920 (9:16) and 1920x1080 (16:9) frame rendering with sacred geometry."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        sb = VideoStoryboardDirector.create_storyboard("BG 2.47", VideoFormat.SHORT_9_16)
        short_frame = os.path.join(tmp_dir, "short_frame.png")
        
        # 1. Render Short Frame (1080x1920)
        ProceduralAssetGenerator.create_scene_frame(
            scene=sb.scenes[0],
            video_format=VideoFormat.SHORT_9_16,
            output_path=short_frame,
            topic_header="BHAGAVAD GITA"
        )
        assert os.path.exists(short_frame)
        with Image.open(short_frame) as img:
            assert img.size == (1080, 1920)

        # 2. Render Long-Form Frame (1920x1080)
        long_frame = os.path.join(tmp_dir, "long_frame.png")
        ProceduralAssetGenerator.create_scene_frame(
            scene=sb.scenes[0],
            video_format=VideoFormat.LONG_16_9,
            output_path=long_frame,
            topic_header="BHAGAVAD GITA"
        )
        assert os.path.exists(long_frame)
        with Image.open(long_frame) as img:
            assert img.size == (1920, 1080)


def test_kinetic_subtitles_srt_and_ass_compilation():
    """Validates SRT and kinetic golden highlighted ASS subtitle generation."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        sb = VideoStoryboardDirector.create_storyboard("BG 2.47", VideoFormat.SHORT_9_16)
        srt_out = os.path.join(tmp_dir, "test.srt")
        ass_out = os.path.join(tmp_dir, "test.ass")

        # 1. Generate SRT
        SubtitleCompiler.generate_srt(sb, srt_out)
        assert os.path.exists(srt_out)
        with open(srt_out, "r", encoding="utf-8") as f:
            srt_content = f.read()
        assert "-->" in srt_content
        assert "00:00:00,000" in srt_content

        # 2. Generate ASS with kinetic gold highlights
        SubtitleCompiler.generate_ass(sb, ass_out)
        assert os.path.exists(ass_out)
        with open(ass_out, "r", encoding="utf-8") as f:
            ass_content = f.read()
        assert "[Script Info]" in ass_content
        assert "PlayResX: 1080" in ass_content
        assert "PlayResY: 1920" in ass_content
        assert r"{\c&H0000D7FF&}" in ass_content


def test_end_to_end_compositor_fast_pipeline():
    """Validates complete autonomous generation pipeline in fast mode."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        out_dir = os.path.join(tmp_dir, "test_production")
        
        prod_meta = FacelessVideoProductionPipeline.generate_video(
            topic="BG 2.47",
            video_format=VideoFormat.SHORT_9_16,
            language="en",
            output_dir=out_dir,
            fast_mode=True
        )

        assert os.path.exists(prod_meta["output_video_path"])
        assert os.path.exists(prod_meta["subtitles_srt"])
        assert os.path.exists(prod_meta["subtitles_ass"])
        assert os.path.exists(prod_meta["metadata_json_path"])
        assert prod_meta["render_stats"]["resolution"] == "1080x1920"
        assert len(prod_meta["chapters"]) == 4
        assert prod_meta["total_duration_sec"] > 0.0


def test_master_orchestrator_state_20_routing():
    """Validates State 20 FSM routing for autonomous faceless video generation queries."""
    res = orchestrator.process_query("generate video for BG 2.47")
    rendered = res.render_markdown()
    assert "Autonomous Faceless Video Storyboard" in rendered
    assert "Karma Yoga" in rendered or "BG 2.47" in rendered
    assert "AUTONOMOUS FACELESS VIDEO PRODUCTION ENGINE" in rendered
    assert "python -m app.video.generate" in rendered


def test_fastapi_v15_video_endpoints():
    """Validates FastAPI /video/storyboard and /video/generate endpoints."""
    # 1. Test Storyboard endpoint
    resp_sb = client.post(
        "/video/storyboard",
        json={"topic": "Rishi Code Katapayadi", "format": "short", "language": "en"}
    )
    assert resp_sb.status_code == 200
    sb_data = resp_sb.json()
    assert sb_data["topic"] == "Rishi Code Katapayadi"
    assert len(sb_data["scenes"]) >= 3
    assert "seo_title" in sb_data

    # 2. Test Video Generation endpoint (fast mode)
    resp_gen = client.post(
        "/video/generate",
        json={"topic": "BG 2.47", "format": "short", "language": "en", "fast_mode": True}
    )
    assert resp_gen.status_code == 200
    gen_data = resp_gen.json()
    assert "output_video_path" in gen_data
    assert "subtitles_srt" in gen_data
    assert gen_data["render_stats"]["status"] == "COMPLETED_PRODUCTION_READY"
