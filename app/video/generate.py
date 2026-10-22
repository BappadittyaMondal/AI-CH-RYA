"""
AI ĀCHĀRYA — Autonomous Faceless Video Generation Pipeline (app/video/generate.py)

Single CLI & Programmatic Command:
python -m app.video.generate --topic "BG 2.47" --format short
python -m app.video.generate --topic "Purusha Sukta" --format long --language en

Produces:
1. Production-ready MP4 (1080x1920 Shorts / 1920x1080 Long).
2. Clean SRT and kinetic ASS golden subtitles.
3. YouTube / Facebook / TikTok viral metadata manifest (JSON).
"""

import os
import sys
import json
import time
import argparse
from typing import Dict, List, Optional, Any

# Ensure Windows console handles UTF-8 gracefully
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from app.video.storyboard import (
    VideoStoryboardDirector,
    VideoStoryboard,
    VideoFormat,
    SceneBeat
)
from app.video.asset_generator import ProceduralAssetGenerator
from app.video.audio_engine import (
    AudioNarrationEngine,
    ProceduralTanpuraGenerator,
    AudioMixerAndDucker,
    AudioConfig
)
from app.video.subtitles import SubtitleCompiler
from app.video.compositor import VideoCompositor, VideoRenderConfig


class FacelessVideoProductionPipeline:
    """
    End-to-end autonomous pipeline orchestrator for faceless video generation.
    """

    @classmethod
    def generate_video(
        cls,
        topic: str,
        video_format: VideoFormat = VideoFormat.SHORT_9_16,
        language: str = "en",
        output_dir: Optional[str] = None,
        voice: Optional[str] = None,
        fast_mode: bool = False
    ) -> Dict[str, Any]:
        """
        Executes the 8-phase autonomous production pipeline.
        """
        start_time = time.time()
        is_short = (video_format == VideoFormat.SHORT_9_16)
        
        # 1. Output directory structure
        fmt_slug = "shorts" if is_short else "long_form"
        safe_topic_slug = "".join(c if c.isalnum() else "_" for c in topic.strip())[:32]
        base_dir = output_dir or os.path.join("output", "videos", fmt_slug, safe_topic_slug)
        assets_dir = os.path.join(base_dir, "assets")
        audio_dir = os.path.join(base_dir, "audio")
        os.makedirs(assets_dir, exist_ok=True)
        os.makedirs(audio_dir, exist_ok=True)

        # 2. Phase I: Director & Storyboard
        storyboard = VideoStoryboardDirector.create_storyboard(
            topic=topic,
            video_format=video_format,
            language=language
        )

        # 3. Phase II: Procedural Frame Asset Generation
        frame_paths = ProceduralAssetGenerator.generate_all_storyboard_frames(
            storyboard=storyboard,
            output_dir=assets_dir
        )

        # 4. Phase III: Voiceover Audio Synthesis
        # Combine all scene narration texts with natural pauses for cohesive pacing
        full_script = " ... ".join([s.narration_text for s in storyboard.scenes])
        voiceover_raw_path = os.path.join(audio_dir, "voiceover_raw.wav")
        
        synth_result = AudioNarrationEngine.synthesize_speech(
            text=full_script,
            output_path=voiceover_raw_path,
            voice=voice,
            language=language
        )
        total_audio_dur = synth_result["duration_sec"]
        
        # Distribute actual audio duration proportionally across scene beats
        script_total_words = max(1, len(full_script.split()))
        scene_durations: List[float] = []
        for s in storyboard.scenes:
            w_count = len(s.narration_text.split())
            ratio = float(w_count) / float(script_total_words)
            s_dur = max(2.5, total_audio_dur * ratio)
            scene_durations.append(round(s_dur, 2))
        
        # Adjust sum to match audio duration
        dur_sum = sum(scene_durations)
        if dur_sum > 0:
            scale_fac = total_audio_dur / dur_sum
            scene_durations = [round(d * scale_fac, 2) for d in scene_durations]

        # 5. Phase IV: Procedural Tanpura Drone & Temple Bell Soundbed
        ambient_path = os.path.join(audio_dir, "tanpura_soundbed.wav")
        ProceduralTanpuraGenerator.generate_drone(
            duration_sec=total_audio_dur + 2.0,
            output_path=ambient_path,
            include_temple_bell=True
        )

        # 6. Phase V: Automated Audio Ducking & Master Mix
        mixed_audio_path = os.path.join(audio_dir, "master_mixed_soundtrack.wav")
        AudioMixerAndDucker.mix_tracks(
            voiceover_wav_path=voiceover_raw_path,
            ambient_wav_path=ambient_path,
            output_wav_path=mixed_audio_path,
            voice_volume=1.0,
            ducked_ambient_vol=0.12,
            un_ducked_ambient_vol=0.28
        )

        # 7. Phase VI: Kinetic Subtitles Compilation
        srt_path = os.path.join(base_dir, "subtitles.srt")
        ass_path = os.path.join(base_dir, "subtitles.ass")
        SubtitleCompiler.generate_srt(storyboard, srt_path, scene_durations)
        SubtitleCompiler.generate_ass(storyboard, ass_path, scene_durations)

        # 8. Phase VII: FFmpeg Video Compositing & Subtitle Burn
        final_mp4_path = os.path.join(base_dir, "final_production.mp4")
        render_cfg = VideoRenderConfig(
            fast_mode=fast_mode,
            burn_subtitles=True
        )
        render_stats = VideoCompositor.render_full_storyboard(
            storyboard=storyboard,
            frame_paths=frame_paths,
            audio_mixed_path=mixed_audio_path,
            subtitle_ass_path=ass_path,
            output_mp4_path=final_mp4_path,
            scene_durations=scene_durations,
            config=render_cfg
        )

        # 9. Phase VIII: Multi-Platform SEO & Metadata Packaging
        chapters: List[Dict[str, Any]] = []
        cur_t = 0.0
        for s_idx, scene in enumerate(storyboard.scenes):
            m = int(cur_t // 60)
            sec = int(cur_t % 60)
            chapters.append({
                "timestamp": f"{m:02d}:{sec:02d}",
                "title": f"Act {scene.scene_number}: {scene.visual_theme}"
            })
            cur_t += scene_durations[s_idx]

        metadata = {
            "project_id": storyboard.project_id,
            "topic": storyboard.topic,
            "video_format": storyboard.video_format.value,
            "language": language,
            "seo_title": storyboard.seo_title,
            "seo_description": storyboard.seo_description,
            "seo_tags": storyboard.seo_tags,
            "total_duration_sec": round(total_audio_dur, 2),
            "chapters": chapters,
            "output_video_path": final_mp4_path,
            "subtitles_srt": srt_path,
            "subtitles_ass": ass_path,
            "render_stats": render_stats,
            "production_time_sec": round(time.time() - start_time, 2)
        }

        meta_path = os.path.join(base_dir, "production_metadata.json")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        metadata["metadata_json_path"] = meta_path
        return metadata


def main():
    parser = argparse.ArgumentParser(description="AI ĀCHĀRYA Autonomous Faceless Video Generator")
    parser.add_argument("--topic", type=str, default="BG 2.47", help="Topic, verse, or inquiry")
    parser.add_argument("--format", type=str, choices=["short", "long"], default="short", help="Video format (short=9:16, long=16:9)")
    parser.add_argument("--language", type=str, choices=["en", "hi", "bn", "sa"], default="en", help="Language code")
    parser.add_argument("--voice", type=str, default=None, help="Specific neural voice override")
    parser.add_argument("--output", type=str, default=None, help="Output directory path")
    parser.add_argument("--fast", action="store_true", help="Fast preview rendering mode")

    args = parser.parse_args()

    v_format = VideoFormat.SHORT_9_16 if args.format == "short" else VideoFormat.LONG_16_9

    print("======================================================================")
    print("[*] AI ACHARYA - Autonomous Faceless Video Production Engine")
    print(f"[*] Topic:    {args.topic}")
    print(f"[*] Format:   {v_format.value}")
    print(f"[*] Language: {args.language}")
    print(f"[*] Fast:     {args.fast}")
    print("======================================================================\n")

    result = FacelessVideoProductionPipeline.generate_video(
        topic=args.topic,
        video_format=v_format,
        language=args.language,
        output_dir=args.output,
        voice=args.voice,
        fast_mode=args.fast
    )

    print("\n[SUCCESS] VIDEO PRODUCTION COMPLETE!")
    print(f"[*] Final Video:     {result['output_video_path']}")
    print(f"[*] File Size:       {result['render_stats']['file_size_mb']} MB")
    print(f"[*] Duration:        {result['total_duration_sec']} seconds")
    print(f"[*] Subtitles (SRT): {result['subtitles_srt']}")
    print(f"[*] Metadata:        {result['metadata_json_path']}")
    print(f"[*] Production Time: {result['production_time_sec']} seconds")
    print("======================================================================")


if __name__ == "__main__":
    main()
