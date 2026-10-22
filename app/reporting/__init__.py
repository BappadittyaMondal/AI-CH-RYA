"""
Reporting & Multi-Modal Export Subsystem (v8.0)
Exposes ExportManager, ThematicDomain, and audio synthesis capabilities.
"""

from app.reporting.themes import ThematicDomain, ThemePalette, detect_thematic_domain, get_theme_palette
from app.reporting.html_dashboard import HTMLDashboardBuilder
from app.reporting.markdown_dossier import MarkdownDossierBuilder
from app.reporting.pdf_report import ExecutivePDFCompiler
from app.reporting.audio_engine import (
    AudioLanguage,
    AudioPacing,
    AudioSynthesizer,
    AudioSynthesisResult,
    SiksaMetricalParser,
    AudioDeckRenderer
)
from app.reporting.export_manager import (
    ExportFormat,
    ExportResult,
    ExportManager
)

__all__ = [
    "ThematicDomain",
    "ThemePalette",
    "detect_thematic_domain",
    "get_theme_palette",
    "HTMLDashboardBuilder",
    "MarkdownDossierBuilder",
    "ExecutivePDFCompiler",
    "AudioLanguage",
    "AudioPacing",
    "AudioSynthesizer",
    "AudioSynthesisResult",
    "SiksaMetricalParser",
    "AudioDeckRenderer",
    "ExportFormat",
    "ExportResult",
    "ExportManager",
]
