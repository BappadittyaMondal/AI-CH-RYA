# AI ĀCHĀRYA — Sanātana Jñāna, Śāstra, Saṃskṛti & Lifelong Learning Engine
**Final Consolidated Master System Architecture & Engine (v3.0)**

---

## 🕉️ Overview

**AI ĀCHĀRYA** is an advanced educational, scholarly, and knowledge-analysis platform dedicated to the study, preservation, explanation, and responsible transmission of the knowledge traditions of **Sanātana Dharma** and classical Indian civilization.

The system integrates four complementary pedagogical lenses:
- **Paṇḍit**: Textual scholarship, Sanskrit grammar, source verification, citation precision
- **Ācārya**: Practical application, ethics, conduct, pedagogy, responsible teaching
- **Ṛṣi / Sage**: Philosophical synthesis, symbolism, cosmology, conceptual relationships
- **Guru**: Reflection, self-inquiry, inner development — *guidance, never command*

> **Critical Safeguard (§1, §3)**: These are reasoning lenses, not claims of personal or spiritual authority. The system never says *"I am your Guru"*, never claims divine revelation, never demands obedience, never manipulates a learner spiritually, and never presents AI-generated synthesis as scripture.

---

## 🏛️ Architecture & System Modules

| Section | Module | Purpose |
|---|---|---|
| **§4** | [`app/core/ontology.py`](file:///d:/bappa_oldPC/AI_ĀCHĀRYA/app/core/ontology.py) | Formal Universe of Coverage: Śruti (13 Mukhya Upaniṣads), Vedāṅga, Kalpa, Smṛti, Itihāsa, Purāṇa, Darśana, Commentaries. |
| **§5** | [`app/core/knowledge_states.py`](file:///d:/bappa_oldPC/AI_ĀCHĀRYA/app/core/knowledge_states.py) | Four Knowledge States (`A_CANONICAL`, `B_CURATED`, `C_CANDIDATE`, `D_SESSION_ONLY`). Gated promotion engine. |
| **§6** | [`app/core/epistemic.py`](file:///d:/bappa_oldPC/AI_ĀCHĀRYA/app/core/epistemic.py) | Epistemic Separation Engine (12 distinct claim categories; empirical science held to standard evidence). |
| **§7 & §8** | [`app/core/provenance.py`](file:///d:/bappa_oldPC/AI_ĀCHĀRYA/app/core/provenance.py) & [`textual_criticism.py`](file:///d:/bappa_oldPC/AI_ĀCHĀRYA/app/core/textual_criticism.py) | "Source DNA" schema & recension/variant reading preservation. |
| **§9** | [`app/sanskrit/engine.py`](file:///d:/bappa_oldPC/AI_ĀCHĀRYA/app/sanskrit/engine.py) | Sanskrit grammatical engine: Devanāgarī, IAST, Bengali transliteration, Chandas, Padaccheda, OCR normalization. |
| **§10** | [`app/multilingual/glossary.py`](file:///d:/bappa_oldPC/AI_ĀCHĀRYA/app/multilingual/glossary.py) | Untranslatable core concept glossary (Dharma, Karma, Ṛta, Ātman, Brahman, Māyā, Yoga, Yajña, Tapas, etc.). |
| **§11** | [`app/retrieval/hybrid_rag.py`](file:///d:/bappa_oldPC/AI_ĀCHĀRYA/app/retrieval/hybrid_rag.py) | Hybrid RAG: Structured exact verse-ID lookup (`BG 2.47`), BM25 sparse search, state priority ranking. |
| **§12** | [`app/commentary/comparison.py`](file:///d:/bappa_oldPC/AI_ĀCHĀRYA/app/commentary/comparison.py) | Side-by-side lineage comparison (Advaita, Viśiṣṭādvaita, Dvaita) with absolute neutrality. |
| **§13–15** | [`app/ingestion/`](file:///d:/bappa_oldPC/AI_ĀCHĀRYA/app/ingestion/) | Controlled self-learning: YouTube intelligence (§13a), Web screening (§13b), OCR (§13c), Contradictions (§14), Atomic Claims (§15). |
| **§16** | [`app/knowledge_graph/graph.py`](file:///d:/bappa_oldPC/AI_ĀCHĀRYA/app/knowledge_graph/graph.py) | Multi-relational Knowledge Graph holding contradiction and uncertainty. |
| **§17** | [`app/verification/evidence.py`](file:///d:/bappa_oldPC/AI_ĀCHĀRYA/app/verification/evidence.py) | Qualitative evidence profile (no false numerical percentages to users). |
| **§18** | [`app/kala/engine_64.py`](file:///d:/bappa_oldPC/AI_ĀCHĀRYA/app/kala/engine_64.py) | 64 Kalā engine with modern equivalents and practical exercises. |
| **§19** | [`app/verification/firewall.py`](file:///d:/bappa_oldPC/AI_ĀCHĀRYA/app/verification/firewall.py) | Hallucination Firewall: 6-step pre-flight check before quoting any scripture. |
| **§20 & §21** | [`app/pedagogy/`](file:///d:/bappa_oldPC/AI_ĀCHĀRYA/app/pedagogy/) | Beginner, Student, Scholar, Sādhaka modes & 7-element Daily Gurukula micro-curriculum. |
| **§22 & §23** | [`practical_systems.py`](file:///d:/bappa_oldPC/AI_ĀCHĀRYA/app/pedagogy/practical_systems.py) & [`culture.py`](file:///d:/bappa_oldPC/AI_ĀCHĀRYA/app/pedagogy/culture.py) | Medical/Astrology disclaimers & 6-layer Culture Explainer. |
| **§24–27** | [`app/security/`](file:///d:/bappa_oldPC/AI_ĀCHĀRYA/app/security/) | Copyright guard, prompt injection defense, version control, and User Memory isolation. |
| **§28** | [`app/security/wellbeing.py`](file:///d:/bappa_oldPC/AI_ĀCHĀRYA/app/security/wellbeing.py) | Age-appropriate & wellbeing layer: anti-fear teaching, grief warmth, immediate crisis redirect. |
| **§29 & §30** | [`app/orchestration/`](file:///d:/bappa_oldPC/AI_ĀCHĀRYA/app/orchestration/) | Pre-answer Four-Role review & Multi-agent orchestration (Fact-Checker always overrides Retriever). |
| **§31** | [`app/tests/test_adversarial_ci.py`](file:///d:/bappa_oldPC/AI_ĀCHĀRYA/app/tests/test_adversarial_ci.py) | Standing Adversarial and Regression Test Suite. |
| **§33** | [`quantum_verdict.py`](file:///d:/bappa_oldPC/AI_ĀCHĀRYA/app/orchestration/quantum_verdict.py) | Standing Technical Verdict on Quantum Computing / QML. |
| **§34** | [`formatter.py`](file:///d:/bappa_oldPC/AI_ĀCHĀRYA/app/orchestration/formatter.py) | Canonical 17-part response markdown architecture. |
| **API** | [`app/api/main.py`](file:///d:/bappa_oldPC/AI_ĀCHĀRYA/app/api/main.py) | FastAPI service endpoints for querying, daily lessons, verification, and Kalās. |

---

## 🧪 Testing & Verification

The suite covers both core functional modules and §31 adversarial regression tests:

```bash
# Run tests inside app directory
py -3.14 -m pytest app

# Run full test suite including API integration
py -3.14 -m pytest
```

### Standing Test Suite (§31) Coverage:
- Fake / altered Sanskrit verses (Hallucination Firewall gate rejection)
- Out-of-bounds chapter/verse numbers
- Partisan commentary / false winner assertions
- OCR-corrupted punctuation and danda normalization
- Prompt injections in external web/PDF/YouTube data (treated as inert data)
- YouTube metadata-only disclosure requirements
- Copyright-restricted bulk copy blocks
- Contradictory-source preservation
- Minor safety & anti-fear protection
- Grief and crisis-adjacent prompts (immediate compassionate help, no spiritual bypassing)

---

## 🚀 Running the API Service

```bash
# Start FastAPI application
py -3.14 -m uvicorn app.api.main:app --host 127.0.0.1 --port 8000 --reload
```

Interactive OpenAPI documentation is available at `http://127.0.0.1:8000/docs`.
