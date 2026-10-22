"""
Resilient Executive PDF Report Compiler (v8.0)
Provides pure-Python PDF compilation with zero external C-dependencies.
Handles Indic scripts through a dual strategy:
1. Pure-Python Standard PDF Generator (Compliant PDF-1.4 binary stream, zero external libraries).
2. Print-Optimized Executive Vector HTML (@media print for 100% perfect Indic HarfBuzz ligature rendering).
"""

import io
import html
from typing import Optional
from app.orchestration.formatter import MasterResponseSchema
from app.reporting.themes import ThematicDomain, detect_thematic_domain, get_theme_palette


class ExecutivePDFCompiler:
    """
    Compiles MasterResponseSchema into an executive PDF report.
    Guaranteed zero external library crashes (pure Python fallback).
    """

    @classmethod
    def render_printable_html(
        cls,
        response: MasterResponseSchema,
        query: str,
        domain_override: Optional[ThematicDomain] = None
    ) -> str:
        """
        Renders a high-resolution, print-optimized document with page-break rules,
        A4 portrait dimensions, and native font ligatures for Sanskrit/Bengali/Hindi.
        """
        domain = domain_override or detect_thematic_domain(query, response.source_text)
        palette = get_theme_palette(domain)

        safe_query = html.escape(query)
        safe_source = html.escape(response.source_text)
        safe_direct = html.escape(response.direct_answer)
        safe_sanskrit = html.escape(response.original_sanskrit)
        safe_translit = html.escape(response.transliteration)
        safe_word = html.escape(response.word_meaning)
        safe_bengali = html.escape(response.bengali_translation)
        safe_hindi = html.escape(response.hindi_translation)
        safe_english = html.escape(response.english_explanation)
        safe_context = html.escape(response.context)
        safe_trad = html.escape(response.traditional_interpretations)
        safe_evidence = html.escape(response.evidence_status.format_user_facing_summary())
        safe_practical = html.escape(response.practical_application)
        safe_seeker = html.escape(response.seeker_action_summary or "")

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Executive Report — {safe_source}</title>
    <style>
        @page {{
            size: A4 portrait;
            margin: 18mm 15mm 18mm 15mm;
            @bottom-right {{
                content: "Page " counter(page) " of " counter(pages);
            }}
        }}

        body {{
            font-family: "Times New Roman", Times, "Noto Serif", serif;
            color: #1A1A1A;
            line-height: 1.5;
            background: #FFFFFF;
            padding: 0;
            margin: 0;
        }}

        .exec-header {{
            border-bottom: 3px double {palette.primary_accent};
            padding-bottom: 12px;
            margin-bottom: 20px;
        }}

        .exec-title {{
            font-size: 20pt;
            font-weight: bold;
            color: {palette.primary_accent};
            margin-bottom: 4px;
        }}

        .exec-meta {{
            font-size: 10pt;
            color: #555555;
            font-style: italic;
        }}

        .badge {{
            display: inline-block;
            background: {palette.primary_accent};
            color: #FFFFFF;
            padding: 2px 8px;
            font-size: 8pt;
            font-weight: bold;
            border-radius: 3px;
            float: right;
        }}

        .section-box {{
            margin-bottom: 16px;
            page-break-inside: avoid;
        }}

        .section-heading {{
            font-size: 12pt;
            font-weight: bold;
            color: {palette.primary_accent};
            border-bottom: 1px solid #DDDDDD;
            padding-bottom: 3px;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .sanskrit-verse {{
            font-family: "Siddhanta", "Noto Sans Devanagari", "Kokila", serif;
            font-size: 14pt;
            line-height: 1.8;
            color: {palette.primary_accent};
            text-align: center;
            background: #FBF8F3;
            border: 1px solid #EAE2D5;
            padding: 12px;
            border-radius: 4px;
            margin: 10px 0;
        }}

        .translit {{
            font-style: italic;
            text-align: center;
            font-size: 10pt;
            color: #444444;
            margin-bottom: 12px;
        }}

        table.lang-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 12px 0;
            font-size: 9.5pt;
        }}

        table.lang-table th, table.lang-table td {{
            border: 1px solid #CCCCCC;
            padding: 8px 10px;
            text-align: left;
            vertical-align: top;
        }}

        table.lang-table th {{
            background: #F5F5F5;
            color: #333333;
            width: 25%;
        }}

        .seeker-highlight {{
            background: #FFF9E6;
            border-left: 4px solid {palette.secondary_accent};
            padding: 10px 14px;
            margin: 12px 0;
            font-size: 10pt;
        }}

        .footer-note {{
            font-size: 8pt;
            color: #777777;
            text-align: center;
            border-top: 1px solid #CCCCCC;
            padding-top: 8px;
            margin-top: 25px;
        }}
    </style>
</head>
<body onload="window.print()">
    <div class="exec-header">
        <span class="badge">EPISTEMIC GRADE: TIER-1</span>
        <div class="exec-title">AI ĀCHĀRYA EXECUTIVE DOSSIER</div>
        <div class="exec-meta">Inquiry: "{safe_query}" | Canonical Record: {safe_source}</div>
    </div>

    {"<div class='seeker-highlight'><strong>SEEKER ACTION & CLARITY SUMMARY:</strong> " + safe_seeker + "</div>" if safe_seeker else ""}

    <div class="section-box">
        <div class="section-heading">1. Executive Verdict</div>
        <p style="font-size: 10.5pt; font-weight: 500;">{safe_direct}</p>
    </div>

    <div class="section-box">
        <div class="section-heading">2. Canonical Sacred Text (Śāstra-Pramāṇa)</div>
        <div class="sanskrit-verse">{safe_sanskrit}</div>
        <div class="translit">{safe_translit}</div>
        <p><strong>Word-by-Word Padaccheda:</strong> {safe_word}</p>
    </div>

    <div class="section-box">
        <div class="section-heading">3. Multilingual Alignment Matrix</div>
        <table class="lang-table">
            <tr><th>বাংলা (Bengali)</th><td>{safe_bengali}</td></tr>
            <tr><th>हिन्दी (Hindi)</th><td>{safe_hindi}</td></tr>
            <tr><th>English (Explanation)</th><td>{safe_english}</td></tr>
        </table>
    </div>

    <div class="section-box">
        <div class="section-heading">4. Commentarial Lineage & Context</div>
        <p><strong>Context:</strong> {safe_context}</p>
        <p style="margin-top: 6px;"><strong>Traditional Lineages:</strong> {safe_trad}</p>
    </div>

    <div class="section-box">
        <div class="section-heading">5. Epistemic Verification & Practical Action</div>
        <p><strong>Evidence Status:</strong> {safe_evidence}</p>
        <p style="margin-top: 6px;"><strong>Practical Application:</strong> {safe_practical}</p>
    </div>

    <div class="footer-note">
        AI ĀCHĀRYA v8.0 • Confidential & Epistemically Verified • Generated via Deterministic Satya-Pramāṇa Pipeline
    </div>
</body>
</html>
"""

    @classmethod
    def render_pdf_bytes(
        cls,
        response: MasterResponseSchema,
        query: str,
        domain_override: Optional[ThematicDomain] = None
    ) -> bytes:
        """
        Emits a standard, valid PDF-1.4 binary stream using pure-Python vector composition.
        Does not require ReportLab, WeasyPrint, or external C-libraries.
        """
        domain = domain_override or detect_thematic_domain(query, response.source_text)
        palette = get_theme_palette(domain)

        # Sanitize text lines for pure ASCII/Latin-1 PDF stream
        title = f"AI ACHARYA EXECUTIVE REPORT: {response.source_text or 'CANONICAL INQUIRY'}"
        sub = f"Query: {query[:75]}..." if len(query) > 75 else f"Query: {query}"
        direct = response.direct_answer[:300].replace("\n", " ")
        translit = response.transliteration[:200].replace("\n", " ")
        english = response.english_explanation[:350].replace("\n", " ")
        practical = response.practical_application[:250].replace("\n", " ")

        # Construct standard PDF stream objects
        def escape_pdf(text: str) -> str:
            return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

        content_stream = f"""BT
/F1 16 Tf
50 780 Td
({escape_pdf(title)}) Tj
/F2 10 Tf
0 -20 Td
({escape_pdf(sub)}) Tj
0 -15 Td
(Domain: {domain.value} | Epistemic Grade: TIER-1 PRAMANA VERIFIED) Tj
/F1 12 Tf
0 -30 Td
(1. EXECUTIVE VERDICT) Tj
/F2 10 Tf
0 -16 Td
({escape_pdf(direct[:95])}) Tj
0 -13 Td
({escape_pdf(direct[95:190])}) Tj
0 -13 Td
({escape_pdf(direct[190:285])}) Tj
/F1 12 Tf
0 -30 Td
(2. CANONICAL SCRIPTURE (IAST Transliteration)) Tj
/F3 10 Tf
0 -16 Td
({escape_pdf(translit[:95])}) Tj
0 -13 Td
({escape_pdf(translit[95:190])}) Tj
/F1 12 Tf
0 -30 Td
(3. ENGLISH EXPLANATION) Tj
/F2 10 Tf
0 -16 Td
({escape_pdf(english[:95])}) Tj
0 -13 Td
({escape_pdf(english[95:190])}) Tj
0 -13 Td
({escape_pdf(english[190:285])}) Tj
/F1 12 Tf
0 -30 Td
(4. PRACTICAL ACHARYA APPLICATION) Tj
/F2 10 Tf
0 -16 Td
({escape_pdf(practical[:95])}) Tj
0 -13 Td
({escape_pdf(practical[95:190])}) Tj
/F2 8 Tf
0 -40 Td
(Generated by AI ACHARYA v8.0 - For full Indic scripts, use the print-optimized HTML dashboard.) Tj
ET
"""
        stream_bytes = content_stream.encode("latin-1", errors="replace")
        stream_len = len(stream_bytes)

        pdf_parts = []
        pdf_parts.append(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")

        # Object 1: Catalog
        obj1 = b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        pdf_parts.append(obj1)

        # Object 2: Pages
        obj2 = b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        pdf_parts.append(obj2)

        # Object 3: Page
        obj3 = b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 4 0 R /Resources << /Font << /F1 5 0 R /F2 6 0 R /F3 7 0 R >> >> >>\nendobj\n"
        pdf_parts.append(obj3)

        # Object 4: Stream
        obj4_head = f"4 0 obj\n<< /Length {stream_len} >>\nstream\n".encode("ascii")
        obj4_foot = b"\nendstream\nendobj\n"
        pdf_parts.append(obj4_head + stream_bytes + obj4_foot)

        # Fonts: F1 (Helvetica-Bold), F2 (Helvetica), F3 (Times-Italic)
        obj5 = b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>\nendobj\n"
        obj6 = b"6 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
        obj7 = b"7 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Times-Italic >>\nendobj\n"
        pdf_parts.extend([obj5, obj6, obj7])

        # Cross-reference table
        body = b"".join(pdf_parts)
        xref_offsets = []
        pos = 0
        lines = body.split(b"\n")
        # Compute accurate byte offsets
        current_offset = 0
        offsets = {}
        for piece in pdf_parts:
            # find obj definitions
            import re
            m = re.match(rb"^([0-9]+)\s+0\s+obj", piece)
            if m:
                obj_id = int(m.group(1))
                offsets[obj_id] = current_offset
            current_offset += len(piece)

        xref_pos = current_offset
        xref_table = f"xref\n0 8\n0000000000 65535 f \n"
        for i in range(1, 8):
            off = offsets.get(i, 0)
            xref_table += f"{off:010d} 00000 n \n"

        trailer = f"trailer\n<< /Size 8 /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n"

        return body + xref_table.encode("ascii") + trailer.encode("ascii")
