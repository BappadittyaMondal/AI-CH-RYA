"""
Thematic Chromatics & Domain Classification System (v8.0)
Maps inquiry domains to traditional and technical color palettes (Prakṛti-Varṇa System).
Provides CSS custom properties for responsive dark/light rendering.
"""

from enum import Enum
from typing import Dict
from pydantic import BaseModel, Field


class ThematicDomain(str, Enum):
    DHARMA_PHILOSOPHY = "DHARMA_PHILOSOPHY"
    STHAPATYA_ARCHITECTURE = "STHAPATYA_ARCHITECTURE"
    ITIHASA_EPIGRAPHY = "ITIHASA_EPIGRAPHY"
    SCIENCE_AERONAUTICS = "SCIENCE_AERONAUTICS"
    AYURVEDA_NATURE = "AYURVEDA_NATURE"
    FORENSIC_REBUTTAL = "FORENSIC_REBUTTAL"


class ThemePalette(BaseModel):
    domain: ThematicDomain
    display_title: str
    primary_accent: str
    secondary_accent: str
    light_bg: str
    light_surface: str
    light_text: str
    light_border: str
    dark_bg: str
    dark_surface: str
    dark_text: str
    dark_border: str

    def to_css_variables(self) -> str:
        """Generates standard CSS variable declarations for both light and dark themes."""
        return f"""
:root {{
    --primary: {self.primary_accent};
    --secondary: {self.secondary_accent};
    --bg-page: {self.light_bg};
    --bg-surface: {self.light_surface};
    --text-main: {self.light_text};
    --border-color: {self.light_border};
    --accent-glow: {self.primary_accent}22;
}}

[data-theme="dark"] {{
    --primary: {self.primary_accent};
    --secondary: {self.secondary_accent};
    --bg-page: {self.dark_bg};
    --bg-surface: {self.dark_surface};
    --text-main: {self.dark_text};
    --border-color: {self.dark_border};
    --accent-glow: {self.secondary_accent}33;
}}
"""


THEME_REGISTRY: Dict[ThematicDomain, ThemePalette] = {
    ThematicDomain.DHARMA_PHILOSOPHY: ThemePalette(
        domain=ThematicDomain.DHARMA_PHILOSOPHY,
        display_title="Dharma & Upaniṣadic Philosophy",
        primary_accent="#D84315",  # Deep Vedic Saffron
        secondary_accent="#B78103",  # Classical Sūrya Gold
        light_bg="#FDFBF7",
        light_surface="#FFFFFF",
        light_text="#212121",
        light_border="#E0DCD3",
        dark_bg="#121212",
        dark_surface="#1E1E1E",
        dark_text="#EDE7F6",
        dark_border="#332A24",
    ),
    ThematicDomain.STHAPATYA_ARCHITECTURE: ThemePalette(
        domain=ThematicDomain.STHAPATYA_ARCHITECTURE,
        display_title="Sthāpatya & Archaeo-Metallurgy",
        primary_accent="#263238",  # Basalt Stone
        secondary_accent="#C2410C",  # Terracotta Oxide
        light_bg="#F8F9FA",
        light_surface="#FFFFFF",
        light_text="#1A202C",
        light_border="#CFD8DC",
        dark_bg="#0F1416",
        dark_surface="#1A2328",
        dark_text="#ECEFF1",
        dark_border="#37474F",
    ),
    ThematicDomain.ITIHASA_EPIGRAPHY: ThemePalette(
        domain=ThematicDomain.ITIHASA_EPIGRAPHY,
        display_title="Itihāsa, Epigraphy & Chronology",
        primary_accent="#78350F",  # Ancient Ochre
        secondary_accent="#0E7490",  # Patina Copper
        light_bg="#FBF8F1",
        light_surface="#FFFFFF",
        light_text="#27272A",
        light_border="#E4D5B7",
        dark_bg="#181512",
        dark_surface="#25201A",
        dark_text="#F4EFE6",
        dark_border="#3D3227",
    ),
    ThematicDomain.SCIENCE_AERONAUTICS: ThemePalette(
        domain=ThematicDomain.SCIENCE_AERONAUTICS,
        display_title="Aeronautics, Nyāya & Epistemology",
        primary_accent="#1E3A8A",  # Royal Deep Blue
        secondary_accent="#0284C7",  # Cyan Spark
        light_bg="#F1F5F9",
        light_surface="#FFFFFF",
        light_text="#0F172A",
        light_border="#CBD5E1",
        dark_bg="#0A0F1D",
        dark_surface="#131C35",
        dark_text="#E2E8F0",
        dark_border="#1E293B",
    ),
    ThematicDomain.AYURVEDA_NATURE: ThemePalette(
        domain=ThematicDomain.AYURVEDA_NATURE,
        display_title="Āyurveda, Yoga & Life Sciences",
        primary_accent="#14532D",  # Forest Emerald
        secondary_accent="#15803D",  # Herbal Sage
        light_bg="#F0FDF4",
        light_surface="#FFFFFF",
        light_text="#14261C",
        light_border="#BBF7D0",
        dark_bg="#0B150E",
        dark_surface="#142419",
        dark_text="#ECFDF5",
        dark_border="#166534",
    ),
    ThematicDomain.FORENSIC_REBUTTAL: ThemePalette(
        domain=ThematicDomain.FORENSIC_REBUTTAL,
        display_title="Forensic Rebuttal & Cognitive Warfare",
        primary_accent="#991B1B",  # Forensic Crimson
        secondary_accent="#D97706",  # Warning Amber
        light_bg="#FFFBFB",
        light_surface="#FFFFFF",
        light_text="#1C1917",
        light_border="#FECDD3",
        dark_bg="#170A0A",
        dark_surface="#261212",
        dark_text="#FEE2E2",
        dark_border="#571717",
    ),
}


def detect_thematic_domain(query: str, source_text: str = "") -> ThematicDomain:
    """
    Deterministically determines the dominant thematic domain based on token analysis.
    Prevents artificial misclassification.
    """
    text = f"{query} {source_text}".lower()

    if any(k in text for k in ["aeronautics", "vaimanika", "iisc", "mukunda", "aerodynamic", "propulsion", "flight", "mercury engine"]):
        return ThematicDomain.SCIENCE_AERONAUTICS

    if any(k in text for k in ["propaganda", "hoax", "conspiracy", "scam", "rebuttal", "distortion", "disinformation", "dmit", "midbrain", "bias"]):
        return ThematicDomain.FORENSIC_REBUTTAL

    if any(k in text for k in ["kailasa", "ellora", "temple", "brihadisvara", "shikhara", "quarry", "incline", "acoustics", "rock-cut", "basalt"]):
        return ThematicDomain.STHAPATYA_ARCHITECTURE

    if any(k in text for k in ["ayurveda", "dosha", "pitta", "vata", "kapha", "yoga", "pranayama", "samskara", "health", "herbal"]):
        return ThematicDomain.AYURVEDA_NATURE

    if any(k in text for k in ["mahabharata", "ramayana", "dating", "inscription", "epigraphy", "aihole", "copper plate", "archeology", "strata", "chronology"]):
        return ThematicDomain.ITIHASA_EPIGRAPHY

    # Default to Dharma / Philosophy for classical scriptural queries
    return ThematicDomain.DHARMA_PHILOSOPHY


def get_theme_palette(domain: ThematicDomain) -> ThemePalette:
    """Returns the ThemePalette instance for the specified domain."""
    return THEME_REGISTRY.get(domain, THEME_REGISTRY[ThematicDomain.DHARMA_PHILOSOPHY])
