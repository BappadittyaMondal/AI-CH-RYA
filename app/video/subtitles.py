"""
AI ĀCHĀRYA — Kinetic Subtitle & Typography Compiler (app/video/subtitles.py)

Mission:
Compiles timed subtitles in both standard SubRip (.srt) and Advanced SubStation Alpha (.ass) formats.
Features:
1. Safe margin calculation: elevated above mobile interface controls for 9:16 Shorts
   and cinematic lower-third for 16:9 long form.
2. Kinetic karaoke-style word highlighting: active words emphasized in Radiant Gold.
3. Clean timing synchronization with actual audio durations.
"""

import os
import math
from typing import List, Optional, Tuple, Dict, Any
from app.video.storyboard import VideoStoryboard, SceneBeat, VideoFormat


class SubtitleCompiler:
    """
    Compiles timed captions and kinetic highlighted subtitle files (.srt and .ass).
    """

    @classmethod
    def format_srt_timestamp(cls, seconds: float) -> str:
        """
        Formats seconds into SRT timestamp format: HH:MM:SS,mmm
        """
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int(round((seconds - int(seconds)) * 1000))
        if millis >= 1000:
            millis = 999
        return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

    @classmethod
    def format_ass_timestamp(cls, seconds: float) -> str:
        """
        Formats seconds into ASS timestamp format: H:MM:SS.cc (centiseconds)
        """
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        centis = int(round((seconds - int(seconds)) * 100))
        if centis >= 100:
            centis = 99
        return f"{hrs:d}:{mins:02d}:{secs:02d}.{centis:02d}"

    @classmethod
    def _chunk_narration(cls, text: str, max_words_per_cue: int = 5) -> List[str]:
        """
        Breaks narration sentences into short, high-impact phrasing chunks (3-5 words)
        optimal for mobile viewers' reading speed.
        """
        words = text.split()
        if not words:
            return []
        
        chunks: List[str] = []
        for i in range(0, len(words), max_words_per_cue):
            chunks.append(" ".join(words[i:i + max_words_per_cue]))
        return chunks

    @classmethod
    def generate_srt(
        cls,
        storyboard: VideoStoryboard,
        output_path: str,
        scene_durations: Optional[List[float]] = None
    ) -> str:
        """
        Generates standard .srt subtitles file for video platforms.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        srt_lines: List[str] = []
        cue_idx = 1
        current_time = 0.0

        for s_idx, scene in enumerate(storyboard.scenes):
            dur = scene_durations[s_idx] if (scene_durations and s_idx < len(scene_durations)) else scene.duration_sec
            chunks = cls._chunk_narration(scene.narration_text, max_words_per_cue=5)
            
            if not chunks:
                current_time += dur
                continue

            chunk_dur = dur / float(len(chunks))
            for chunk in chunks:
                start_t = current_time
                end_t = current_time + chunk_dur
                srt_lines.append(str(cue_idx))
                srt_lines.append(f"{cls.format_srt_timestamp(start_t)} --> {cls.format_srt_timestamp(end_t)}")
                srt_lines.append(chunk)
                srt_lines.append("")
                cue_idx += 1
                current_time = end_t

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(srt_lines))

        return output_path

    @classmethod
    def generate_ass(
        cls,
        storyboard: VideoStoryboard,
        output_path: str,
        scene_durations: Optional[List[float]] = None
    ) -> str:
        """
        Generates Advanced SubStation Alpha (.ass) subtitles with bold kinetic golden highlights
        and platform-safe layout margins.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        is_short = (storyboard.video_format == VideoFormat.SHORT_9_16)
        
        play_res_x = 1080 if is_short else 1920
        play_res_y = 1920 if is_short else 1080

        # Typography styling: ASS color hex format is &HAABBGGRR&
        # Gold RGB(212, 175, 55) -> BGR(55, 175, 212) -> &H0037AFD4&
        # Radiant Gold RGB(255, 215, 0) -> &H0000D7FF&
        # Crisp White/Ivory RGB(250, 248, 240) -> &H00F0F8FA&
        # Dark Charcoal Outline RGB(16, 16, 16) -> &H00101010&
        font_size = 54 if is_short else 38
        margin_v = 440 if is_short else 110  # Elevate for Shorts interface safe area

        ass_header = f"""[Script Info]
Title: AI ĀCHĀRYA Kinetic Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
PlayResX: {play_res_x}
PlayResY: {play_res_y}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,{font_size},&H00F0F8FA,&H0000D7FF,&H00101010,&H80000000,-1,0,0,0,100,100,0,0,1,3.5,1.5,2,40,40,{margin_v},1
Style: Highlight,Arial,{font_size},&H0000D7FF,&H00F0F8FA,&H00101010,&H80000000,-1,0,0,0,105,105,0,0,1,4.0,2.0,2,40,40,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        dialogue_lines: List[str] = []
        current_time = 0.0

        for s_idx, scene in enumerate(storyboard.scenes):
            dur = scene_durations[s_idx] if (scene_durations and s_idx < len(scene_durations)) else scene.duration_sec
            chunks = cls._chunk_narration(scene.narration_text, max_words_per_cue=4)
            
            if not chunks:
                current_time += dur
                continue

            chunk_dur = dur / float(len(chunks))
            for chunk in chunks:
                start_t = current_time
                end_t = current_time + chunk_dur
                
                start_str = cls.format_ass_timestamp(start_t)
                end_str = cls.format_ass_timestamp(end_t)

                # Format kinetic gold highlight on active words
                words = chunk.split()
                if len(words) >= 2:
                    # Highlight the first/key emphasis word in bold gold
                    highlighted_chunk = f"{{\\c&H0000D7FF&}}{words[0]}{{\\c&H00F0F8FA&}} " + " ".join(words[1:])
                else:
                    highlighted_chunk = f"{{\\c&H0000D7FF&}}{chunk}{{\\c&H00F0F8FA&}}"

                line = f"Dialogue: 0,{start_str},{end_str},Default,,0,0,0,,{highlighted_chunk}"
                dialogue_lines.append(line)
                current_time = end_t

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(ass_header + "\n".join(dialogue_lines) + "\n")

        return output_path
