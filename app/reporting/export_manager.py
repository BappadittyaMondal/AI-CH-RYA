"""
Export Manager & Unified Reporting Facade (v8.0)
Coordinates on-demand generation of HTML Dashboards, Forensic Markdown,
Executive PDF Reports, and Multilingual Audio Streams.
Operates with zero disk persistence (100% in-memory streaming via io.BytesIO).
Dormant by default.
"""

import hashlib
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from app.orchestration.formatter import MasterResponseSchema
from app.reporting.themes import ThematicDomain, detect_thematic_domain
from app.reporting.html_dashboard import HTMLDashboardBuilder
from app.reporting.markdown_dossier import MarkdownDossierBuilder
from app.reporting.pdf_report import ExecutivePDFCompiler
from app.reporting.audio_engine import (
    AudioSynthesizer,
    AudioLanguage,
    AudioPacing,
    AudioSynthesisResult,
    AudioDeckRenderer
)


class ExportFormat(str, Enum):
    HTML = "html"
    MARKDOWN = "markdown"
    PDF = "pdf"
    AUDIO = "audio"
    ALL = "all"


class ExportResult(BaseModel):
    format: ExportFormat
    file_name: str
    mime_type: str
    content_bytes: Optional[bytes] = None
    content_text: Optional[str] = None
    sha256_hash: str
    thematic_domain: ThematicDomain


class ExportManager:
    """
    On-Demand Multi-Modal Export Engine.
    Activated solely when explicitly requested by user or API caller.
    """

    @classmethod
    def generate_single_export(
        cls,
        response: MasterResponseSchema,
        export_format: ExportFormat,
        query: str,
        audio_lang: AudioLanguage = AudioLanguage.ENGLISH,
        audio_pacing: AudioPacing = AudioPacing.STANDARD,
        domain_override: Optional[ThematicDomain] = None
    ) -> ExportResult:
        domain = domain_override or detect_thematic_domain(query, response.source_text)
        slug = (response.source_text or "inquiry").replace(" ", "_").replace(":", "_").lower()

        if export_format == ExportFormat.HTML:
            html_content = HTMLDashboardBuilder.render(response, query, domain)
            sha256 = hashlib.sha256(html_content.encode("utf-8")).hexdigest()
            return ExportResult(
                format=ExportFormat.HTML,
                file_name=f"ai_acharya_{slug}_dashboard.html",
                mime_type="text/html; charset=utf-8",
                content_text=html_content,
                sha256_hash=sha256,
                thematic_domain=domain
            )

        elif export_format == ExportFormat.MARKDOWN:
            md_content = MarkdownDossierBuilder.render(response, query, domain)
            sha256 = hashlib.sha256(md_content.encode("utf-8")).hexdigest()
            return ExportResult(
                format=ExportFormat.MARKDOWN,
                file_name=f"ai_acharya_{slug}_dossier.md",
                mime_type="text/markdown; charset=utf-8",
                content_text=md_content,
                sha256_hash=sha256,
                thematic_domain=domain
            )

        elif export_format == ExportFormat.PDF:
            pdf_bytes = ExecutivePDFCompiler.render_pdf_bytes(response, query, domain)
            sha256 = hashlib.sha256(pdf_bytes).hexdigest()
            return ExportResult(
                format=ExportFormat.PDF,
                file_name=f"ai_acharya_{slug}_executive_report.pdf",
                mime_type="application/pdf",
                content_bytes=pdf_bytes,
                sha256_hash=sha256,
                thematic_domain=domain
            )

        elif export_format == ExportFormat.AUDIO:
            audio_res = AudioSynthesizer.synthesize(response, lang=audio_lang, pacing=audio_pacing)
            return ExportResult(
                format=ExportFormat.AUDIO,
                file_name=f"ai_acharya_{slug}_{audio_lang.value}_recitation.wav",
                mime_type=audio_res.mime_type,
                content_bytes=audio_res.audio_bytes,
                content_text=audio_res.ssml_script,
                sha256_hash=audio_res.sha256_hash,
                thematic_domain=domain
            )

        raise ValueError(f"Unsupported export format: {export_format}")

    @classmethod
    def generate_all_exports(
        cls,
        response: MasterResponseSchema,
        query: str,
        audio_lang: AudioLanguage = AudioLanguage.ENGLISH,
        domain_override: Optional[ThematicDomain] = None
    ) -> Dict[ExportFormat, ExportResult]:
        """Generates all 4 export artifacts synchronously in memory."""
        results = {}
        for fmt in [ExportFormat.HTML, ExportFormat.MARKDOWN, ExportFormat.PDF, ExportFormat.AUDIO]:
            results[fmt] = cls.generate_single_export(
                response=response,
                export_format=fmt,
                query=query,
                audio_lang=audio_lang,
                domain_override=domain_override
            )
        return results

    @classmethod
    def decorate_markdown_with_audio_decks(
        cls,
        markdown_text: str,
        audio_endpoint_url: str = "/export/audio"
    ) -> str:
        """
        Injects the required default-muted audio symbols (🔊 / 🎧)
        at both the very beginning and the end of any rendered markdown text.
        """
        header = AudioDeckRenderer.render_markdown_header(audio_endpoint_url)
        footer = AudioDeckRenderer.render_markdown_footer(audio_endpoint_url)
        return f"{header}\n{markdown_text}\n{footer}"
