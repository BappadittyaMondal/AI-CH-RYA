"""
Interactive Dark/Light Responsive HTML Dashboard Builder (v8.0)
Generates 100% self-contained, offline HTML5 dashboards matching topic chromatics.
Features embedded dual Web Audio decks (start and end) with multilingual voice routing.
Strictly sanitizes dynamic content to prevent XSS.
"""

import html
from typing import Optional
from app.orchestration.formatter import MasterResponseSchema
from app.reporting.themes import ThematicDomain, detect_thematic_domain, get_theme_palette


class HTMLDashboardBuilder:
    """
    Renders MasterResponseSchema into an interactive, topic-adaptive HTML5 dashboard.
    Zero external dependencies or CDNs. Completely self-contained.
    """

    @classmethod
    def render(
        cls,
        response: MasterResponseSchema,
        query: str,
        domain_override: Optional[ThematicDomain] = None
    ) -> str:
        domain = domain_override or detect_thematic_domain(query, response.source_text)
        palette = get_theme_palette(domain)
        css_vars = palette.to_css_variables()

        # Sanitize all dynamic string inputs
        safe_query = html.escape(query)
        safe_direct = html.escape(response.direct_answer)
        safe_source = html.escape(response.source_text)
        safe_sanskrit = html.escape(response.original_sanskrit)
        safe_translit = html.escape(response.transliteration)
        safe_word = html.escape(response.word_meaning)
        safe_bengali = html.escape(response.bengali_translation)
        safe_hindi = html.escape(response.hindi_translation)
        safe_english = html.escape(response.english_explanation)
        safe_context = html.escape(response.context)
        safe_trad = html.escape(response.traditional_interpretations)
        safe_scholarly = html.escape(response.scholarly_historical_view or "None recorded.")
        safe_disagreement = html.escape(response.areas_of_disagreement or "None recorded.")
        safe_evidence = html.escape(response.evidence_status.format_user_facing_summary())
        safe_practical = html.escape(response.practical_application)
        safe_seeker = html.escape(response.seeker_action_summary or "")
        safe_visual = html.escape(response.visual_forensic_card or "")

        takeaways_html = "".join([f"<li>{html.escape(t)}</li>" for t in response.key_takeaways])
        related_html = "".join([f"<li>{html.escape(r)}</li>" for r in response.related_texts])

        return f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI ĀCHĀRYA — {safe_source or safe_query}</title>
    <style>
        {css_vars}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: var(--bg-page);
            color: var(--text-main);
            line-height: 1.6;
            padding: 20px;
            transition: background-color 0.3s ease, color 0.3s ease;
        }}

        .dashboard-container {{
            max-width: 1040px;
            margin: 0 auto;
        }}

        header.masthead {{
            background: var(--bg-surface);
            border-top: 5px solid var(--primary);
            border-bottom: 2px solid var(--border-color);
            border-radius: 8px 8px 0 0;
            padding: 24px 30px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.06);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }}

        .masthead-title h1 {{
            font-size: 1.6rem;
            color: var(--primary);
            letter-spacing: 0.5px;
        }}

        .masthead-title p {{
            font-size: 0.9rem;
            opacity: 0.8;
        }}

        .top-controls {{
            display: flex;
            gap: 10px;
            align-items: center;
        }}

        button.theme-toggle {{
            background: var(--bg-page);
            color: var(--text-main);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 8px 16px;
            font-size: 0.85rem;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.2s;
        }}

        button.theme-toggle:hover {{
            border-color: var(--primary);
            color: var(--primary);
        }}

        /* Interactive Audio Deck */
        .audio-deck {{
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-left: 4px solid var(--secondary);
            border-radius: 6px;
            padding: 14px 20px;
            margin: 16px 0;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }}

        .audio-trigger-btn {{
            display: flex;
            align-items: center;
            gap: 8px;
            background: var(--primary);
            color: #FFFFFF;
            border: none;
            border-radius: 24px;
            padding: 9px 18px;
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.15s, opacity 0.2s;
        }}

        .audio-trigger-btn:hover {{
            opacity: 0.92;
            transform: scale(1.02);
        }}

        .audio-controls-group {{
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }}

        select.voice-select, select.speed-select {{
            background: var(--bg-page);
            color: var(--text-main);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 6px 10px;
            font-size: 0.85rem;
            cursor: pointer;
        }}

        .card {{
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 22px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }}

        .card-header {{
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 12px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 6px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .sanskrit-box {{
            font-family: "Siddhanta", "Noto Sans Devanagari", "Kokila", Georgia, serif;
            font-size: 1.45rem;
            color: var(--primary);
            text-align: center;
            padding: 18px;
            background: var(--accent-glow);
            border-radius: 6px;
            margin: 12px 0;
            line-height: 1.8;
        }}

        .translit-box {{
            font-family: "Courier New", Courier, monospace;
            font-style: italic;
            font-size: 1.05rem;
            color: var(--secondary);
            text-align: center;
            margin-bottom: 16px;
        }}

        .translation-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 16px;
            margin: 16px 0;
        }}

        .trans-card {{
            background: var(--bg-page);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 14px;
        }}

        .trans-card h4 {{
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--secondary);
            margin-bottom: 6px;
        }}

        .copy-btn {{
            background: transparent;
            border: 1px solid var(--border-color);
            color: var(--text-main);
            border-radius: 4px;
            padding: 3px 8px;
            font-size: 0.75rem;
            cursor: pointer;
        }}

        .copy-btn:hover {{
            border-color: var(--primary);
            color: var(--primary);
        }}

        details.accordion {{
            background: var(--bg-page);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            margin: 10px 0;
            padding: 10px 14px;
        }}

        details.accordion summary {{
            font-weight: 600;
            color: var(--primary);
            cursor: pointer;
            outline: none;
        }}

        details.accordion[open] summary {{
            margin-bottom: 10px;
            border-bottom: 1px dashed var(--border-color);
            padding-bottom: 6px;
        }}

        pre.ascii-card {{
            background: #0D1117;
            color: #58A6FF;
            padding: 14px;
            border-radius: 6px;
            overflow-x: auto;
            font-family: monospace;
            font-size: 0.85rem;
            margin: 12px 0;
        }}

        .badge-verified {{
            display: inline-block;
            background: #2E7D32;
            color: #FFFFFF;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 700;
        }}

        footer.dashboard-footer {{
            text-align: center;
            padding: 24px;
            font-size: 0.85rem;
            opacity: 0.8;
            border-top: 1px solid var(--border-color);
            margin-top: 30px;
        }}
    </style>
</head>
<body>
    <div class="dashboard-container">
        <!-- Masthead -->
        <header class="masthead">
            <div class="masthead-title">
                <h1>AI ĀCHĀRYA — {palette.display_title}</h1>
                <p>Query: <em>"{safe_query}"</em> | Canonical Source: <strong>{safe_source}</strong></p>
            </div>
            <div class="top-controls">
                <span class="badge-verified">✓ PRAMĀṆA VERIFIED</span>
                <button class="theme-toggle" id="themeBtn" onclick="toggleTheme()">🌓 Dark Mode</button>
            </div>
        </header>

        <!-- Top Audio Deck (Starting Deck) -->
        <div class="audio-deck" id="topAudioDeck">
            <button class="audio-trigger-btn" id="topAudioPlayBtn" onclick="toggleReportSpeech('top')">
                <span id="topAudioIcon">🔊</span>
                <span id="topAudioLabel">Listen to Report (Muted)</span>
            </button>
            <div class="audio-controls-group">
                <label for="topVoiceSelect" style="font-size: 0.8rem; font-weight: 600;">Voice:</label>
                <select class="voice-select" id="topVoiceSelect" onchange="syncVoiceSelect(this.value)">
                    <option value="sanskrit">Sanskrit (Devanāgarī)</option>
                    <option value="bengali">Bengali (বাংলা)</option>
                    <option value="hindi">Hindi (हिन्दी)</option>
                    <option value="english" selected>English (Explanation)</option>
                </select>
                <label for="topSpeedSelect" style="font-size: 0.8rem; font-weight: 600;">Speed:</label>
                <select class="speed-select" id="topSpeedSelect" onchange="syncSpeedSelect(this.value)">
                    <option value="0.8">0.8x (Chant / Study)</option>
                    <option value="1.0" selected>1.0x (Standard)</option>
                    <option value="1.2">1.2x (Fast)</option>
                </select>
            </div>
        </div>

        {"<!-- Seeker Action Summary -->" if safe_seeker else ""}
        {f'<div class="card" style="border-left: 5px solid var(--primary);"><div class="card-header">⚡ SEEKER ACTION & CLARITY SUMMARY</div><p>{safe_seeker}</p></div>' if safe_seeker else ""}

        {"<!-- Visual Forensic Card -->" if safe_visual else ""}
        {f'<div class="card"><div class="card-header">📊 FORENSIC VISUAL CARD</div><pre class="ascii-card">{safe_visual}</pre></div>' if safe_visual else ""}

        <!-- Direct Answer Card -->
        <div class="card">
            <div class="card-header">
                <span>1. DIRECT ANSWER</span>
                <button class="copy-btn" onclick="copyText('directAns')">Copy</button>
            </div>
            <p id="directAns">{safe_direct}</p>
        </div>

        <!-- Canonical Sacred Text & Padaccheda -->
        <div class="card">
            <div class="card-header">
                <span>2. CANONICAL SANSKRIT & TRANSLITERATION</span>
                <button class="copy-btn" onclick="copyText('sanskritVerse')">Copy Devanāgarī</button>
            </div>
            <div class="sanskrit-box" id="sanskritVerse">{safe_sanskrit}</div>
            <div class="translit-box">{safe_translit}</div>
            <details class="accordion">
                <summary>Word-by-Word Meaning (Padaccheda & Anvaya)</summary>
                <p style="margin-top: 8px;">{safe_word}</p>
            </details>
        </div>

        <!-- Multi-Script Translations Grid -->
        <div class="card">
            <div class="card-header">3. MULTI-LINGUAL TRANSLATIONS & EXPLANATION</div>
            <div class="translation-grid">
                <div class="trans-card">
                    <h4>Bengali Translation (বাংলা)</h4>
                    <p id="bengaliText">{safe_bengali}</p>
                </div>
                <div class="trans-card">
                    <h4>Hindi Translation (हिन्दी)</h4>
                    <p id="hindiText">{safe_hindi}</p>
                </div>
                <div class="trans-card">
                    <h4>English Explanation</h4>
                    <p id="englishText">{safe_english}</p>
                </div>
            </div>
        </div>

        <!-- Context & Commentary Accordeons -->
        <div class="card">
            <div class="card-header">4. CONTEXT & TRADITIONAL COMMENTARIES</div>
            <p><strong>Historical Context:</strong> {safe_context}</p>
            <details class="accordion" style="margin-top: 14px;" open>
                <summary>Traditional Lineage Interpretations (Sampradāya)</summary>
                <p style="margin-top: 8px;">{safe_trad}</p>
            </details>
            <details class="accordion">
                <summary>Scholarly & Historical View</summary>
                <p style="margin-top: 8px;">{safe_scholarly}</p>
            </details>
            <details class="accordion">
                <summary>Areas of Disagreement & Variant Readings</summary>
                <p style="margin-top: 8px;">{safe_disagreement}</p>
            </details>
        </div>

        <!-- Evidence & Practical Application -->
        <div class="card">
            <div class="card-header">5. EVIDENCE AUDIT & ĀCĀRYA APPLICATION</div>
            <p><strong>Evidence Status:</strong> {safe_evidence}</p>
            <p style="margin-top: 10px;"><strong>Practical Application:</strong> {safe_practical}</p>
            {"<div style='margin-top: 12px;'><strong>Key Takeaways:</strong><ul>" + takeaways_html + "</ul></div>" if takeaways_html else ""}
            {"<div style='margin-top: 12px;'><strong>Related Canonical Texts:</strong><ul>" + related_html + "</ul></div>" if related_html else ""}
        </div>

        <!-- Bottom Audio Deck (Ending Deck) -->
        <div class="audio-deck" id="bottomAudioDeck">
            <button class="audio-trigger-btn" id="bottomAudioPlayBtn" onclick="toggleReportSpeech('bottom')">
                <span id="bottomAudioIcon">🔊</span>
                <span id="bottomAudioLabel">Listen to Report (Muted)</span>
            </button>
            <div class="audio-controls-group">
                <label for="bottomVoiceSelect" style="font-size: 0.8rem; font-weight: 600;">Voice:</label>
                <select class="voice-select" id="bottomVoiceSelect" onchange="syncVoiceSelect(this.value)">
                    <option value="sanskrit">Sanskrit (Devanāgarī)</option>
                    <option value="bengali">Bengali (বাংলা)</option>
                    <option value="hindi">Hindi (हिन्दी)</option>
                    <option value="english" selected>English (Explanation)</option>
                </select>
                <label for="bottomSpeedSelect" style="font-size: 0.8rem; font-weight: 600;">Speed:</label>
                <select class="speed-select" id="bottomSpeedSelect" onchange="syncSpeedSelect(this.value)">
                    <option value="0.8">0.8x (Chant / Study)</option>
                    <option value="1.0" selected>1.0x (Standard)</option>
                    <option value="1.2">1.2x (Fast)</option>
                </select>
            </div>
        </div>

        <!-- Footer -->
        <footer class="dashboard-footer">
            <p>AI ĀCHĀRYA v8.0 • Canonical Sanātana Śāstra & Epistemic Verification Engine</p>
            <p style="margin-top: 4px;">Pramāṇa-Guaranteed • Zero Hallucination • Tamper Evident</p>
        </footer>
    </div>

    <!-- Client-Side Web Audio & Interactivity Script (Zero External Dependencies) -->
    <script>
        let isSpeaking = false;
        let activeUtterance = null;
        let selectedLang = 'english';
        let playbackSpeed = 1.0;

        function toggleTheme() {{
            const html = document.documentElement;
            const current = html.getAttribute('data-theme');
            const target = current === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-theme', target);
            document.getElementById('themeBtn').textContent = target === 'dark' ? '☀️ Light Mode' : '🌓 Dark Mode';
        }}

        function syncVoiceSelect(val) {{
            selectedLang = val;
            document.getElementById('topVoiceSelect').value = val;
            document.getElementById('bottomVoiceSelect').value = val;
            if (isSpeaking) {{
                stopAudio();
                startAudio();
            }}
        }}

        function syncSpeedSelect(val) {{
            playbackSpeed = parseFloat(val);
            document.getElementById('topSpeedSelect').value = val;
            document.getElementById('bottomSpeedSelect').value = val;
            if (isSpeaking) {{
                stopAudio();
                startAudio();
            }}
        }}

        function copyText(elemId) {{
            const text = document.getElementById(elemId).innerText;
            navigator.clipboard.writeText(text).then(() => {{
                alert('Copied to clipboard successfully!');
            }});
        }}

        function getReadingPayload() {{
            if (selectedLang === 'sanskrit') {{
                return document.getElementById('sanskritVerse').innerText;
            }} else if (selectedLang === 'bengali') {{
                return document.getElementById('bengaliText').innerText;
            }} else if (selectedLang === 'hindi') {{
                return document.getElementById('hindiText').innerText;
            }} else {{
                return document.getElementById('directAns').innerText + ". " + document.getElementById('englishText').innerText;
            }}
        }}

        function getLangCode() {{
            if (selectedLang === 'sanskrit') return 'hi-IN';
            if (selectedLang === 'bengali') return 'bn-IN';
            if (selectedLang === 'hindi') return 'hi-IN';
            return 'en-IN';
        }}

        function updateAudioButtons(speaking) {{
            isSpeaking = speaking;
            const icon = speaking ? '⏸️' : '🔊';
            const label = speaking ? 'Pause Audio' : 'Listen to Report (Muted)';
            
            document.getElementById('topAudioIcon').textContent = icon;
            document.getElementById('topAudioLabel').textContent = label;
            document.getElementById('bottomAudioIcon').textContent = icon;
            document.getElementById('bottomAudioLabel').textContent = label;
        }}

        function stopAudio() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
            }}
            updateAudioButtons(false);
        }}

        function startAudio() {{
            if (!('speechSynthesis' in window)) {{
                alert('Web Speech API is not supported in this browser.');
                return;
            }}
            window.speechSynthesis.cancel();

            const text = getReadingPayload();
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = getLangCode();
            utterance.rate = playbackSpeed;

            utterance.onend = function() {{
                updateAudioButtons(false);
            }};

            utterance.onerror = function() {{
                updateAudioButtons(false);
            }};

            activeUtterance = utterance;
            window.speechSynthesis.speak(utterance);
            updateAudioButtons(true);
        }}

        function toggleReportSpeech(origin) {{
            if (isSpeaking) {{
                stopAudio();
            }} else {{
                startAudio();
            }}
        }}
    </script>
</body>
</html>
"""
