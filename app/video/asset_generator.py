"""
AI ĀCHĀRYA — Procedural Visual Asset Generator (app/video/asset_generator.py)

Mission:
Generates high-resolution, topic-oriented faceless video frames (1080x1920 Shorts & 1920x1080 Long)
using Pillow and NumPy with:
1. Chiaroscuro Vedic slate, ancient parchment, and cosmic obsidian backgrounds.
2. Procedural sacred geometry watermarks (Śrī Yantra, Dharma Cakra, Mandala).
3. Authentic Devanāgarī typography (using Windows Nirmala UI / NirmalaB) with gold foil styling.
4. Clean IAST transliteration and viral retention visual focal points.
"""

import os
import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from app.video.storyboard import SceneBeat, VideoFormat, VideoStoryboard


# Windows Indic & Latin Font Paths
INDIC_FONT_BOLD = "C:/Windows/Fonts/NirmalaB.ttf"
INDIC_FONT_REGULAR = "C:/Windows/Fonts/Nirmala.ttf"
SERIF_FONT_BOLD = "C:/Windows/Fonts/georgiab.ttf"
SERIF_FONT_REGULAR = "C:/Windows/Fonts/georgia.ttf"
SANS_FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"
SANS_FONT_REGULAR = "C:/Windows/Fonts/arial.ttf"


@dataclass
class VisualThemePalette:
    name: str
    bg_gradient_start: Tuple[int, int, int]
    bg_gradient_end: Tuple[int, int, int]
    accent_gold: Tuple[int, int, int]
    card_border: Tuple[int, int, int]
    card_bg: Tuple[int, int, int, int]
    text_primary: Tuple[int, int, int]
    text_secondary: Tuple[int, int, int]
    vignette_alpha: int


PALETTES: Dict[str, VisualThemePalette] = {
    "VEDIC_SLATE": VisualThemePalette(
        name="VEDIC_SLATE",
        bg_gradient_start=(18, 18, 22),      # Dark Charcoal Slate
        bg_gradient_end=(8, 9, 12),          # Deep Obsidian
        accent_gold=(212, 175, 55),          # Imperial Gold
        card_border=(184, 134, 11),          # Dark Goldenrod
        card_bg=(28, 26, 32, 220),           # Translucent Slate
        text_primary=(250, 248, 240),        # Warm Ivory
        text_secondary=(200, 190, 170),      # Muted Gold
        vignette_alpha=160
    ),
    "ANCIENT_PARCHMENT": VisualThemePalette(
        name="ANCIENT_PARCHMENT",
        bg_gradient_start=(32, 20, 14),      # Aged Terracotta / Umber
        bg_gradient_end=(14, 10, 8),         # Deep Bark
        accent_gold=(225, 180, 70),          # Radiant Antique Gold
        card_border=(190, 120, 40),          # Copper Bronze
        card_bg=(38, 24, 18, 225),
        text_primary=(255, 245, 230),
        text_secondary=(215, 185, 150),
        vignette_alpha=170
    ),
    "CYBER_DHARMA": VisualThemePalette(
        name="CYBER_DHARMA",
        bg_gradient_start=(10, 18, 26),      # Deep Midnight Cyan
        bg_gradient_end=(4, 8, 14),          # Cyber Black
        accent_gold=(0, 210, 255),           # Cyber Electric Cyan
        card_border=(0, 160, 200),
        card_bg=(12, 24, 36, 230),
        text_primary=(240, 250, 255),
        text_secondary=(140, 200, 220),
        vignette_alpha=180
    ),
    "COSMIC_NEBULA": VisualThemePalette(
        name="COSMIC_NEBULA",
        bg_gradient_start=(20, 10, 32),      # Deep Astral Indigo
        bg_gradient_end=(6, 4, 12),          # Void
        accent_gold=(230, 195, 80),          # Star Gold
        card_border=(180, 140, 50),
        card_bg=(24, 14, 38, 225),
        text_primary=(252, 248, 255),
        text_secondary=(195, 175, 215),
        vignette_alpha=175
    )
}


class ProceduralAssetGenerator:
    """
    Renders 1080x1920 (Shorts) and 1920x1080 (Long Form) video keyframes
    with sacred geometry, calligraphy, and typographic cards.
    """

    @classmethod
    def get_dimensions(cls, video_format: VideoFormat) -> Tuple[int, int]:
        if video_format == VideoFormat.SHORT_9_16:
            return 1080, 1920
        return 1920, 1080

    @classmethod
    def _load_font(cls, font_path: str, size: int) -> ImageFont.ImageFont:
        try:
            if os.path.exists(font_path):
                return ImageFont.truetype(font_path, size)
        except Exception:
            pass
        return ImageFont.load_default()

    @classmethod
    def _get_palette(cls, theme_name: str) -> VisualThemePalette:
        th_up = theme_name.upper()
        for key in PALETTES:
            if key in th_up:
                return PALETTES[key]
        if "CYBER" in th_up or "SCAM" in th_up:
            return PALETTES["CYBER_DHARMA"]
        if "COSMIC" in th_up or "PURUSHA" in th_up:
            return PALETTES["COSMIC_NEBULA"]
        if "PARCHMENT" in th_up or "RISHI" in th_up or "CODE" in th_up:
            return PALETTES["ANCIENT_PARCHMENT"]
        return PALETTES["VEDIC_SLATE"]

    @classmethod
    def create_scene_frame(
        cls,
        scene: SceneBeat,
        video_format: VideoFormat,
        output_path: str,
        topic_header: Optional[str] = None
    ) -> str:
        """
        Creates a cinematic visual frame for a single scene beat and saves it as PNG.
        """
        width, height = cls.get_dimensions(video_format)
        palette = cls._get_palette(scene.visual_theme)
        is_short = (video_format == VideoFormat.SHORT_9_16)

        # 1. Base Radial Gradient Background (NumPy)
        y, x = np.ogrid[:height, :width]
        cx, cy = width / 2.0, height / 2.0
        max_dist = math.sqrt(cx**2 + cy**2)
        dist = np.sqrt((x - cx)**2 + (y - cy)**2) / max_dist
        
        # Linear interpolation between start and end gradient
        c_start = np.array(palette.bg_gradient_start, dtype=np.float32)
        c_end = np.array(palette.bg_gradient_end, dtype=np.float32)
        
        # Add subtle noise texture for tactile stone/parchment feel
        rng = np.random.default_rng(seed=scene.scene_number * 101)
        noise = rng.normal(0, 3.5, (height, width, 1))

        bg_array = (c_start[None, None, :] * (1.0 - dist[..., None]) + 
                    c_end[None, None, :] * dist[..., None] + noise)
        bg_array = np.clip(bg_array, 0, 255).astype(np.uint8)

        base_img = Image.fromarray(bg_array, mode="RGB")
        overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # 2. Sacred Geometry Watermark (Center / Upper Center)
        geom_cy = int(height * 0.42) if is_short else int(height * 0.48)
        cls._draw_sacred_geometry(
            draw=draw,
            center=(width // 2, geom_cy),
            max_radius=int(min(width, height) * 0.38),
            gold_color=palette.accent_gold
        )

        # 3. Vignette Shadow Overlay
        cls._draw_vignette(overlay, width, height, palette.vignette_alpha)

        # 4. Composite Overlay onto Base
        frame = Image.alpha_composite(base_img.convert("RGBA"), overlay)
        draw_frame = ImageDraw.Draw(frame)

        # 5. Header Branding / Topic Pill
        header_text = topic_header or "AI ĀCHĀRYA ARCHIVE"
        cls._draw_header_badge(draw_frame, width, height, header_text, palette, is_short)

        # 6. Center Focal Card: Devanāgarī Calligraphy & IAST
        cls._draw_central_calligraphy_card(
            frame=frame,
            draw=draw_frame,
            scene=scene,
            width=width,
            height=height,
            palette=palette,
            is_short=is_short
        )

        # 7. Scene Counter / Platform Safe Margins Indicator
        cls._draw_scene_metadata(draw_frame, scene, width, height, palette, is_short)

        # Save to disk
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        frame.convert("RGB").save(output_path, "PNG", optimize=True)
        return output_path

    @classmethod
    def _draw_sacred_geometry(
        cls,
        draw: ImageDraw.ImageDraw,
        center: Tuple[int, int],
        max_radius: int,
        gold_color: Tuple[int, int, int]
    ):
        """
        Draws subtle concentric dharma circles, interlocking triangles, and 16-ray lotus petals.
        """
        cx, cy = center
        faint_gold = (*gold_color, 28)     # 11% opacity
        line_gold = (*gold_color, 45)      # 18% opacity
        accent_gold = (*gold_color, 75)

        # Concentric circles
        for r_factor in [0.25, 0.45, 0.65, 0.85, 1.0]:
            r = int(max_radius * r_factor)
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=faint_gold, width=2)

        # 16-ray Dharma Chakra spokes
        num_spokes = 16
        inner_r = int(max_radius * 0.25)
        outer_r = int(max_radius * 0.85)
        for i in range(num_spokes):
            angle = i * (2 * math.pi / num_spokes)
            x1 = cx + int(inner_r * math.cos(angle))
            y1 = cy + int(inner_r * math.sin(angle))
            x2 = cx + int(outer_r * math.cos(angle))
            y2 = cy + int(outer_r * math.sin(angle))
            draw.line([(x1, y1), (x2, y2)], fill=faint_gold, width=1)

        # Upward and downward sacred triangles (Śrī Yantra motif)
        tri_r = int(max_radius * 0.60)
        # Upward triangle
        up_pts = [
            (cx, cy - tri_r),
            (cx - int(tri_r * math.cos(math.pi / 6)), cy + int(tri_r * math.sin(math.pi / 6))),
            (cx + int(tri_r * math.cos(math.pi / 6)), cy + int(tri_r * math.sin(math.pi / 6))),
        ]
        draw.polygon(up_pts, outline=line_gold)
        # Downward triangle
        down_pts = [
            (cx, cy + tri_r),
            (cx - int(tri_r * math.cos(math.pi / 6)), cy - int(tri_r * math.sin(math.pi / 6))),
            (cx + int(tri_r * math.cos(math.pi / 6)), cy - int(tri_r * math.sin(math.pi / 6))),
        ]
        draw.polygon(down_pts, outline=line_gold)

        # Central Bindu (cosmic point)
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=accent_gold)

    @classmethod
    def _draw_vignette(cls, overlay: Image.Image, width: int, height: int, alpha_max: int):
        """
        Draws deep corner vignette to keep viewer focus centrally anchored.
        """
        v_img = Image.new("L", (width, height), 0)
        v_draw = ImageDraw.Draw(v_img)
        v_draw.rectangle([0, 0, width, height], fill=0)
        
        # Soft outer edge darkening
        margin_x = int(width * 0.08)
        margin_y = int(height * 0.08)
        v_draw.ellipse([margin_x, margin_y, width - margin_x, height - margin_y], fill=255)
        v_img = v_img.filter(ImageFilter.GaussianBlur(radius=int(min(width, height) * 0.12)))
        
        v_arr = np.array(v_img, dtype=np.float32) / 255.0
        v_dark = ((1.0 - v_arr) * alpha_max).astype(np.uint8)

        dark_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        dark_layer.putalpha(Image.fromarray(v_dark, mode="L"))
        overlay.alpha_composite(dark_layer)

    @classmethod
    def _draw_header_badge(
        cls,
        draw: ImageDraw.ImageDraw,
        width: int,
        height: int,
        header_text: str,
        palette: VisualThemePalette,
        is_short: bool
    ):
        """
        Renders refined brand title badge with gold rule line.
        """
        font_size = 28 if is_short else 24
        font = cls._load_font(SERIF_FONT_BOLD, font_size)
        
        top_y = int(height * 0.08) if is_short else int(height * 0.07)
        badge_text = f"☸  {header_text.upper()}  ☸"
        
        bbox = font.getbbox(badge_text)
        txt_w = bbox[2] - bbox[0]
        txt_h = bbox[3] - bbox[1]
        x = (width - txt_w) // 2

        # Accent Rule Line
        line_w = int(txt_w * 1.3)
        lx1 = (width - line_w) // 2
        lx2 = lx1 + line_w
        ly = top_y + txt_h + 14
        draw.line([(lx1, ly), (lx2, ly)], fill=(*palette.accent_gold, 180), width=2)
        
        # Diamond accents on line ends
        draw.polygon([(lx1, ly - 3), (lx1 - 3, ly), (lx1, ly + 3), (lx1 + 3, ly)], fill=palette.accent_gold)
        draw.polygon([(lx2, ly - 3), (lx2 - 3, ly), (lx2, ly + 3), (lx2 + 3, ly)], fill=palette.accent_gold)

        draw.text((x, top_y), badge_text, font=font, fill=palette.accent_gold)

    @classmethod
    def _draw_central_calligraphy_card(
        cls,
        frame: Image.Image,
        draw: ImageDraw.ImageDraw,
        scene: SceneBeat,
        width: int,
        height: int,
        palette: VisualThemePalette,
        is_short: bool
    ):
        """
        Draws the focal calligraphy card displaying Devanāgarī and IAST.
        """
        devanagari = scene.on_screen_devanagari.strip()
        iast = scene.on_screen_iast.strip()

        # Responsive card sizing
        card_w = int(width * 0.88) if is_short else int(width * 0.65)
        card_h = int(height * 0.42) if is_short else int(height * 0.50)
        card_x1 = (width - card_w) // 2
        card_y1 = int(height * 0.26) if is_short else int(height * 0.22)
        card_x2 = card_x1 + card_w
        card_y2 = card_y1 + card_h

        # Semi-transparent Card Backdrop
        card_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        card_draw = ImageDraw.Draw(card_layer)
        corner_r = 24
        
        card_draw.rounded_rectangle(
            [card_x1, card_y1, card_x2, card_y2],
            radius=corner_r,
            fill=palette.card_bg,
            outline=palette.card_border,
            width=2
        )
        
        # Inner thin gold border
        inner_m = 10
        card_draw.rounded_rectangle(
            [card_x1 + inner_m, card_y1 + inner_m, card_x2 - inner_m, card_y2 - inner_m],
            radius=max(6, corner_r - inner_m),
            outline=(*palette.accent_gold, 90),
            width=1
        )
        frame.alpha_composite(card_layer)

        # Devanāgarī Typography
        dev_size = 56 if is_short else 46
        dev_font = cls._load_font(INDIC_FONT_BOLD, dev_size)
        
        # Split devanagari into lines if long
        dev_lines = cls._wrap_text(devanagari, dev_font, card_w - 60)
        
        curr_y = card_y1 + 40
        for d_line in dev_lines:
            d_box = dev_font.getbbox(d_line)
            d_w = d_box[2] - d_box[0]
            d_x = (width - d_w) // 2
            
            # Subtle drop shadow for calligraphy
            draw.text((d_x + 2, curr_y + 2), d_line, font=dev_font, fill=(10, 10, 10))
            draw.text((d_x, curr_y), d_line, font=dev_font, fill=palette.accent_gold)
            curr_y += (d_box[3] - d_box[1] + 16)

        # Decorative Divider
        curr_y += 10
        div_w = int(card_w * 0.45)
        dx1 = (width - div_w) // 2
        dx2 = dx1 + div_w
        draw.line([(dx1, curr_y), (dx2, curr_y)], fill=(*palette.card_border, 160), width=1)
        curr_y += 24

        # IAST / Translation Typography
        iast_size = 28 if is_short else 24
        iast_font = cls._load_font(SERIF_FONT_REGULAR, iast_size)
        iast_lines = cls._wrap_text(iast, iast_font, card_w - 70)
        
        for i_line in iast_lines:
            i_box = iast_font.getbbox(i_line)
            i_w = i_box[2] - i_box[0]
            i_x = (width - i_w) // 2
            draw.text((i_x, curr_y), i_line, font=iast_font, fill=palette.text_primary)
            curr_y += (i_box[3] - i_box[1] + 12)

    @classmethod
    def _draw_scene_metadata(
        cls,
        draw: ImageDraw.ImageDraw,
        scene: SceneBeat,
        width: int,
        height: int,
        palette: VisualThemePalette,
        is_short: bool
    ):
        """
        Draws scene counter and topic cue at safe margins.
        """
        font = cls._load_font(SANS_FONT_BOLD, 18 if is_short else 16)
        beat_cue = f"ACT {scene.scene_number:02d}  •  {scene.visual_theme.replace('_', ' ')}"
        bbox = font.getbbox(beat_cue)
        w = bbox[2] - bbox[0]
        
        # Positioned above bottom UI overlays (Shorts bottom navigation safe area)
        y = int(height * 0.72) if is_short else int(height * 0.82)
        x = (width - w) // 2
        
        draw.text((x, y), beat_cue, font=font, fill=(*palette.text_secondary, 180))

    @classmethod
    def _wrap_text(cls, text: str, font: ImageFont.ImageFont, max_width: int) -> List[str]:
        """
        Wraps text cleanly within max_width boundaries.
        """
        if not text:
            return []
        words = text.split()
        lines: List[str] = []
        current_line: List[str] = []

        for word in words:
            candidate = " ".join(current_line + [word])
            bbox = font.getbbox(candidate)
            w = bbox[2] - bbox[0]
            if w <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]

        if current_line:
            lines.append(" ".join(current_line))
        return lines

    @classmethod
    def generate_all_storyboard_frames(
        cls,
        storyboard: VideoStoryboard,
        output_dir: str
    ) -> List[str]:
        """
        Generates frames for all scenes in the storyboard.
        Returns list of generated PNG file paths.
        """
        os.makedirs(output_dir, exist_ok=True)
        frame_paths: List[str] = []

        for scene in storyboard.scenes:
            filename = f"scene_{scene.scene_number:03d}.png"
            out_path = os.path.join(output_dir, filename)
            cls.create_scene_frame(
                scene=scene,
                video_format=storyboard.video_format,
                output_path=out_path,
                topic_header=storyboard.topic
            )
            frame_paths.append(out_path)

        return frame_paths
