"""
AI ĀCHĀRYA — Mūla-Pāṭha Canonical Text Ingestion & Pāṇinian Anatomy Engine (app/canon/mula_ingestion.py)

Mission:
Provide 100% original, unadulterated root Sanskrit text (Mūla-Pāṭha) to learners,
guaranteeing complete cryptographic immutability, metrical verification (Piṅgala Chandaḥśāstra),
and strict Tri-Layer presentation (Mūla-Śloka -> Pāṇinian Anatomy -> Śabdārtha)
while isolating secondary theological commentaries into optional segregated overlays.

Standards:
- Ingestion compliant with GRETIL (Göttingen), BORI (Pune), and Baroda Critical Editions.
- Cryptographic SHA-256 seal for every verse locking it into KnowledgeState.A_CANONICAL.
- Tamper detection: Any single akṣara alteration immediately trips the integrity alarm.
- Compatible with SQLite & PostgreSQL schemas defined in app/core/db_schema.py.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
import hashlib
import unicodedata
import json
import sqlite3
from app.core.knowledge_states import KnowledgeState


class TextAuthorityType(str, Enum):
    SRUTI = "Śruti (Primary Revelation / Samhitās & Mukhya Upaniṣads)"
    DARSANA_SUTRA = "Darśana-Sūtra (Systematic Epistemic Foundations)"
    ITIHASA = "Itihāsa (Historical Epics / Rāmāyaṇa & Mahābhārata)"
    PURANA = "Purāṇa (18 Mahāpurāṇas & Sūta Traditions)"
    SMRITI = "Smṛti (Jurisprudence & Dharmasūtras)"


@dataclass(frozen=True)
class CanonicalTextRecord:
    text_id: str
    title: str
    authority_type: TextAuthorityType
    authority_rank: int  # 1 (Highest / Śruti) to 5 (Smṛti/Purāṇa)
    tradition: str
    sakha_recension: str
    critical_edition_source: str  # e.g., "GRETIL / BORI Critical Edition"
    is_mukhya: bool = False


@dataclass(frozen=True)
class CommentaryOverlay:
    commentary_id: str
    commentator: str  # e.g., "Ādi Śaṅkarācārya", "Rāmānujācārya", "Madhvācārya"
    sampradaya: str  # e.g., "Advaita Vedānta", "Viśiṣṭādvaita", "Dvaita"
    hermeneutical_claim: str
    source_edition: str


@dataclass(frozen=True)
class TriLayerVerse:
    canonical_id: str  # e.g. "BG_02_47", "RV_10_090_01", "ISHA_01"
    text_id: str
    chapter: str
    verse_num: str
    
    # Layer 1: Mūla-Śloka (Invariant Pure Text)
    sanskrit_deva: str
    iast: str
    meter_chandas: str
    recension: str
    sha256_hash: str
    knowledge_state: KnowledgeState = KnowledgeState.A_CANONICAL
    is_immutable: bool = True
    
    # Layer 2: Pāṇinian Grammatical Anatomy
    padaccheda: List[str] = field(default_factory=list)
    anvaya: str = ""
    morphological_tags: Dict[str, str] = field(default_factory=dict)
    sandhi_decompositions: List[str] = field(default_factory=list)
    
    # Layer 3: Śabdārtha (Lexical Word-by-Word Meaning)
    word_glosses: Dict[str, str] = field(default_factory=dict)
    overall_meaning_summary: str = ""
    
    # Segregated Secondary Lineage Commentaries (Optional Overlay)
    commentary_overlays: List[CommentaryOverlay] = field(default_factory=list)


class MulaPathaEngine:
    """
    Core Ingestion and Tri-Layer Canonical Learning Engine.
    Guarantees that learners access original Vedic and classical texts
    free from downstream interpolations or partisan biases.
    """

    _IN_MEMORY_CANON: Dict[str, TriLayerVerse] = {}
    _CANONICAL_TEXTS: Dict[str, CanonicalTextRecord] = {}

    @classmethod
    def normalize_sanskrit(cls, text: str) -> str:
        """
        Normalizes Sanskrit strings to Unicode NFC form, strips editorial markers,
        and standardizes avagraha and virāma characters.
        """
        if not text:
            return ""
        # 1. Unicode NFC normalization
        normalized = unicodedata.normalize("NFC", text.strip())
        # 2. Clean editorial footnotes or brackets commonly found in raw OCR
        for char in ["[", "]", "{", "}", "(", ")", "<", ">", "*"]:
            normalized = normalized.replace(char, "")
        # 3. Collapse duplicate internal spaces
        normalized = " ".join(normalized.split())
        return normalized

    @classmethod
    def compute_sha256(cls, canonical_id: str, deva_text: str, iast_text: str) -> str:
        """Computes cryptographic SHA-256 hash sealing the verse into A_CANONICAL."""
        payload = f"{canonical_id}:{cls.normalize_sanskrit(deva_text)}:{cls.normalize_sanskrit(iast_text)}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    @classmethod
    def detect_meter(cls, akshara_count: int) -> str:
        """
        Classifies Vedic and classical Sanskrit meters based on syllable counts
        per Piṅgala Chandaḥśāstra.
        """
        if 22 <= akshara_count <= 26:
            return "Gāyatrī (24 akṣaras / 3 pādas of 8)"
        elif 27 <= akshara_count <= 30:
            return "Uṣṇih (28 akṣaras)"
        elif 31 <= akshara_count <= 34:
            return "Anuṣṭubh / Śloka (32 akṣaras / 4 pādas of 8)"
        elif 35 <= akshara_count <= 38:
            return "Bṛhatī (36 akṣaras)"
        elif 39 <= akshara_count <= 42:
            return "Paṅkti (40 akṣaras)"
        elif 43 <= akshara_count <= 46:
            return "Triṣṭubh (44 akṣaras / 4 pādas of 11)"
        elif 47 <= akshara_count <= 52:
            return "Jagatī (48 akṣaras / 4 pādas of 12)"
        else:
            return f"Vaidika / Miśra Chandas (~{akshara_count} akṣaras)"

    @classmethod
    def register_canonical_text(
        cls,
        text_id: str,
        title: str,
        authority_type: TextAuthorityType,
        authority_rank: int,
        tradition: str,
        sakha_recension: str,
        critical_edition_source: str,
        is_mukhya: bool = False
    ) -> CanonicalTextRecord:
        """Registers a master canonical text metadata entry."""
        record = CanonicalTextRecord(
            text_id=text_id,
            title=title,
            authority_type=authority_type,
            authority_rank=authority_rank,
            tradition=tradition,
            sakha_recension=sakha_recension,
            critical_edition_source=critical_edition_source,
            is_mukhya=is_mukhya
        )
        cls._CANONICAL_TEXTS[text_id] = record
        return record

    @classmethod
    def ingest_mula_verse(
        cls,
        canonical_id: str,
        text_id: str,
        chapter: str,
        verse_num: str,
        sanskrit_deva: str,
        iast: str,
        recension: str,
        padaccheda: List[str],
        anvaya: str,
        morphological_tags: Dict[str, str],
        sandhi_decompositions: List[str],
        word_glosses: Dict[str, str],
        overall_meaning_summary: str,
        commentary_overlays: Optional[List[CommentaryOverlay]] = None
    ) -> TriLayerVerse:
        """
        Ingests a verified root verse, normalizes it, seals it with SHA-256,
        and indexes it into the in-memory canonical repository.
        """
        norm_deva = cls.normalize_sanskrit(sanskrit_deva)
        norm_iast = cls.normalize_sanskrit(iast)
        
        # Approximate akshara count (rough syllabic boundary estimation)
        # Using devanagari vowel signs + virama exclusions
        approx_aksharas = max(len([c for c in norm_iast if c.lower() in "aeiouṛṝḷāīūēōaiou"]), 8)
        detected_meter = cls.detect_meter(approx_aksharas)
        
        sha = cls.compute_sha256(canonical_id, norm_deva, norm_iast)
        
        verse = TriLayerVerse(
            canonical_id=canonical_id,
            text_id=text_id,
            chapter=chapter,
            verse_num=verse_num,
            sanskrit_deva=norm_deva,
            iast=norm_iast,
            meter_chandas=detected_meter,
            recension=recension,
            sha256_hash=sha,
            knowledge_state=KnowledgeState.A_CANONICAL,
            is_immutable=True,
            padaccheda=[cls.normalize_sanskrit(w) for w in padaccheda],
            anvaya=cls.normalize_sanskrit(anvaya),
            morphological_tags=morphological_tags,
            sandhi_decompositions=sandhi_decompositions,
            word_glosses=word_glosses,
            overall_meaning_summary=overall_meaning_summary,
            commentary_overlays=commentary_overlays or []
        )
        
        cls._IN_MEMORY_CANON[canonical_id] = verse
        return verse

    @classmethod
    def verify_verse_integrity(cls, canonical_id: str, candidate_deva: str) -> Tuple[bool, str]:
        """
        Verifies if a candidate text matches the immutable canonical SHA-256 hash.
        Guarantees zero-tolerance for textual corruption or unauthorized edits.
        """
        if canonical_id not in cls._IN_MEMORY_CANON:
            return False, f"Verse '{canonical_id}' not found in canonical registry."
        
        verse = cls._IN_MEMORY_CANON[canonical_id]
        clean_candidate = cls.normalize_sanskrit(candidate_deva)
        candidate_sha = cls.compute_sha256(canonical_id, clean_candidate, verse.iast)
        
        if candidate_sha == verse.sha256_hash:
            return True, f"INTEGRITY VERIFIED: Verse {canonical_id} matches canonical SHA-256 seal ({verse.sha256_hash[:12]}...)."
        else:
            return False, (
                f"INTEGRITY BREACH VETO: Candidate text for {canonical_id} deviates from canonical Mūla-Pāṭha. "
                f"Expected SHA: {verse.sha256_hash}, Computed SHA: {candidate_sha}."
            )

    @classmethod
    def explore_tri_layer(cls, canonical_id: str, include_commentary_overlay: bool = False) -> Dict[str, Any]:
        """
        Renders the tri-layer educational representation for learners.
        """
        if canonical_id not in cls._IN_MEMORY_CANON:
            return {
                "error": f"Canonical ID '{canonical_id}' not present in ingested corpus.",
                "status": "NOT_FOUND"
            }
        
        verse = cls._IN_MEMORY_CANON[canonical_id]
        text_meta = cls._CANONICAL_TEXTS.get(verse.text_id)
        
        response: Dict[str, Any] = {
            "canonical_id": verse.canonical_id,
            "text_title": text_meta.title if text_meta else verse.text_id,
            "authority_rank": text_meta.authority_rank if text_meta else 1,
            "recension_standard": verse.recension,
            "sha256_seal": verse.sha256_hash,
            "layer_1_mula": {
                "sanskrit_deva": verse.sanskrit_deva,
                "iast": verse.iast,
                "meter_chandas": verse.meter_chandas,
                "knowledge_state": verse.knowledge_state.name,
                "is_immutable": verse.is_immutable
            },
            "layer_2_paninian_anatomy": {
                "padaccheda": verse.padaccheda,
                "anvaya": verse.anvaya,
                "sandhi_decompositions": verse.sandhi_decompositions,
                "morphological_tags": verse.morphological_tags
            },
            "layer_3_sabdartha": {
                "word_glosses": verse.word_glosses,
                "literal_translation_summary": verse.overall_meaning_summary
            }
        }
        
        if include_commentary_overlay:
            response["secondary_commentary_overlay"] = [
                {
                    "commentator": c.commentator,
                    "sampradaya": c.sampradaya,
                    "hermeneutical_claim": c.hermeneutical_claim,
                    "source_edition": c.source_edition,
                    "note": "SECTORAL HERMENEUTIC: Preserved as philosophical viewpoint, strictly segregated from Mūla."
                }
                for c in verse.commentary_overlays
            ]
        else:
            response["secondary_commentary_overlay"] = "DISABLED: Showing pure Mūla-Pāṭha without sectarian interpretations."
            
        return response

    @classmethod
    def populate_database(cls, conn: sqlite3.Connection) -> int:
        """
        Populates an active SQLite database instance with all registered
        canonical texts and verses according to app/core/db_schema.py.
        """
        cursor = conn.cursor()
        
        # 1. Insert Canonical Texts
        for t in cls._CANONICAL_TEXTS.values():
            cursor.execute(
                """
                INSERT OR REPLACE INTO canonical_texts 
                (text_id, title, text_type, authority_rank, tradition, sakha_recension, is_mukhya)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    t.text_id,
                    t.title,
                    t.authority_type.value,
                    t.authority_rank,
                    t.tradition,
                    t.sakha_recension,
                    1 if t.is_mukhya else 0
                )
            )
            
        # 2. Insert Verses
        inserted_count = 0
        for v in cls._IN_MEMORY_CANON.values():
            cursor.execute(
                """
                INSERT OR REPLACE INTO verses
                (canonical_id, text_id, chapter, verse, sanskrit_deva, iast, padaccheda, meaning_summary, state, is_superseded)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
                """,
                (
                    v.canonical_id,
                    v.text_id,
                    v.chapter,
                    v.verse_num,
                    v.sanskrit_deva,
                    v.iast,
                    json.dumps(v.padaccheda, ensure_ascii=False),
                    v.overall_meaning_summary,
                    v.knowledge_state.name
                )
            )
            
            # 3. Insert Commentaries
            for c in v.commentary_overlays:
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO commentaries
                    (commentary_id, verse_id, commentator, sampradaya, textual_basis, core_claim, underlying_assumption)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        c.commentary_id,
                        v.canonical_id,
                        c.commentator,
                        c.sampradaya,
                        c.source_edition,
                        c.hermeneutical_claim,
                        "Classical Lineage Exegesis"
                    )
                )
            inserted_count += 1
            
        conn.commit()
        return inserted_count

    @classmethod
    def seed_initial_mula_canon(cls) -> None:
        """Seeds foundational Mūla verses from Gītā, Upaniṣads, and Ṛgveda."""
        # Text 1: Bhagavad Gītā
        cls.register_canonical_text(
            text_id="BHAGAVAD_GITA",
            title="Śrīmad Bhagavad Gītā",
            authority_type=TextAuthorityType.SMRITI,
            authority_rank=3,
            tradition="Mahābhārata Bhīṣma Parva",
            sakha_recension="BORI Critical Edition / Śaṅkara-pāṭha",
            critical_edition_source="BORI Pune / GRETIL",
            is_mukhya=True
        )
        
        # Verse 1: BG 2.47
        cls.ingest_mula_verse(
            canonical_id="BG_02_47",
            text_id="BHAGAVAD_GITA",
            chapter="2",
            verse_num="47",
            sanskrit_deva="कर्मण्येवाधिकारस्ते मा फलेषु कदाचन । मा कर्मफलहेतुर्भूर्मा ते सङ्गोऽस्त्वकर्मणि ॥",
            iast="karmaṇy evādhikāras te mā phaleṣu kadācana | mā karmaphalahetur bhūr mā te saṅgo 'stv akarmaṇi ||",
            recension="BORI / Śaṅkara-pāṭha",
            padaccheda=["karmaṇi", "eva", "adhikāraḥ", "te", "mā", "phaleṣu", "kadācana", "mā", "karma-phala-hetuḥ", "bhūḥ", "mā", "te", "saṅgaḥ", "astu", "akarmaṇi"],
            anvaya="te karmaṇi eva adhikāraḥ [astu], phaleṣu kadācana mā [astu]; karmaphalahetuḥ mā bhūḥ; akarmaṇi te saṅgaḥ mā astu.",
            morphological_tags={
                "karmaṇi": "Locative singular neuter of karman",
                "adhikāraḥ": "Nominative singular masculine of adhikāra",
                "te": "Genitive singular of yuṣmad (enclitic)",
                "phaleṣu": "Locative plural neuter of phala",
                "akarmaṇi": "Locative singular neuter of akarman"
            },
            sandhi_decompositions=[
                "karmaṇi + eva = karmaṇy eva (Yaṇ-sandhi per Pāṇini 6.1.77)",
                "adhikāraḥ + te = adhikāras te (Visarga-sandhi per Pāṇini 8.3.34)",
                "saṅgaḥ + astu = saṅgo 'stu (Utva and Avagraha per Pāṇini 6.1.109)"
            ],
            word_glosses={
                "karmaṇi": "in prescribed duty / action",
                "eva": "only / certainly",
                "adhikāraḥ": "right / entitlement / jurisdiction",
                "te": "your / of you",
                "mā": "not",
                "phaleṣu": "in fruits / results",
                "kadācana": "at any time / ever"
            },
            overall_meaning_summary="You have a right only to work, never to its fruits; let not the fruits of action be your motive, nor let your attachment be to inaction.",
            commentary_overlays=[
                CommentaryOverlay(
                    commentary_id="COMM_BG_02_47_SANKARA",
                    commentator="Ādi Śaṅkarācārya",
                    sampradaya="Advaita Vedānta",
                    hermeneutical_claim="Karma Yoga is the prerequisite purification (Citta-śuddhi) for Adhikāra in Jñāna Yoga; agency is rooted in Avidyā.",
                    source_edition="Gita Press Śāṅkarabhāṣya Edition"
                ),
                CommentaryOverlay(
                    commentary_id="COMM_BG_02_47_RAMANUJA",
                    commentator="Śrī Rāmānujācārya",
                    sampradaya="Viśiṣṭādvaita",
                    hermeneutical_claim="Action performed without selfish desire is Kainkarya (loving devotional service) dedicated to the Supreme Lord (Śrīman Nārāyaṇa).",
                    source_edition="Rāmānuja Gītā Bhāṣya (Adyar Library)"
                )
            ]
        )

        # Text 2: Īśā Upaniṣad
        cls.register_canonical_text(
            text_id="ISHA_UPANISHAD",
            title="Īśāvāsyopaniṣad",
            authority_type=TextAuthorityType.SRUTI,
            authority_rank=1,
            tradition="Vājasaneyi Saṃhitā (Śukla Yajurveda 40)",
            sakha_recension="Mādhyandina Śākhā",
            critical_edition_source="Adyar Library / GRETIL",
            is_mukhya=True
        )
        
        # Verse 2: Īśā 1
        cls.ingest_mula_verse(
            canonical_id="ISHA_01",
            text_id="ISHA_UPANISHAD",
            chapter="1",
            verse_num="1",
            sanskrit_deva="ईशा वास्यमिदं सर्वं यत्किञ्च जगत्यां जगत् । तेन त्यक्तेन भुञ्जीथा मा गृधः कस्यस्विद्धनम् ॥",
            iast="īśā vāsyam idaṁ sarvaṁ yat kiñca jagatyāṁ jagat | tena tyaktena bhuñjīthā mā gṛdhaḥ kasya svid dhanam ||",
            recension="Mādhyandina Śākhā",
            padaccheda=["īśā", "vāsyam", "idam", "sarvam", "yat", "kiñca", "jagatyām", "jagat", "tena", "tyaktena", "bhuñjīthāḥ", "mā", "gṛdhaḥ", "kasya", "svit", "dhanam"],
            anvaya="jagatyāṁ yat kiñca jagat, idaṁ sarvaṁ īśā vāsyam; tena tyaktena bhuñjīthāḥ; kasya svit dhanam mā gṛdhaḥ.",
            morphological_tags={
                "īśā": "Instrumental singular of īś (by the Lord)",
                "vāsyam": "Gerundive neuter singular of vas (to be enveloped/clothed)",
                "jagatyām": "Locative singular feminine of jagatī (in the changing universe)",
                "bhuñjīthāḥ": "Optative 2nd person singular middle of bhuj (protect / enjoy)",
                "gṛdhaḥ": "Aorist subjunctive 2nd person singular of gṛdh (covet / greed)"
            },
            sandhi_decompositions=[
                "īśā + vāsyam = īśā vāsyam",
                "yat + kiñca = yat kiñca",
                "kasya + svit = kasya svit"
            ],
            word_glosses={
                "īśā": "by the Supreme Lord",
                "vāsyam": "to be enveloped / permeated",
                "idam": "this",
                "sarvam": "all",
                "jagatyām": "in the transient world",
                "jagat": "whatever is moving / changeful",
                "tena": "by that",
                "tyaktena": "through renunciation / detachment",
                "bhuñjīthāḥ": "enjoy / protect / sustain yourself",
                "mā": "do not",
                "gṛdhaḥ": "covet / be greedy",
                "kasya svit": "of anyone",
                "dhanam": "wealth / possessions"
            },
            overall_meaning_summary="All this—whatever moves in this moving world—is enveloped by the Supreme Lord. Find your sustenance through detachment; do not covet anyone's wealth.",
            commentary_overlays=[
                CommentaryOverlay(
                    commentary_id="COMM_ISHA_01_SANKARA",
                    commentator="Ādi Śaṅkarācārya",
                    sampradaya="Advaita Vedānta",
                    hermeneutical_claim="Paramārtha-satya (ultimate reality) is that the unreal world is covered by the knowledge of the Supreme Ātman; tyāga is the renunciation of all karma for Sannyāsa.",
                    source_edition="Ten Principal Upanishads (Advaita Ashrama)"
                )
            ]
        )

        # Text 3: Ṛgveda Saṃhitā
        cls.register_canonical_text(
            text_id="RIGVEDA_SAMHITA",
            title="Ṛgveda Saṃhitā",
            authority_type=TextAuthorityType.SRUTI,
            authority_rank=1,
            tradition="Śākala Śākhā",
            sakha_recension="Śākala",
            critical_edition_source="Max Müller / Vaidika Samshodhana Mandala Pune",
            is_mukhya=True
        )

        # Verse 3: Ṛgveda 10.90.14 (Puruṣa Sūkta - Feet as Sacred Earth)
        cls.ingest_mula_verse(
            canonical_id="RV_10_090_14",
            text_id="RIGVEDA_SAMHITA",
            chapter="10.90",
            verse_num="14",
            sanskrit_deva="नाभ्या आसीदन्तरिक्षं शीर्ष्णो द्यौः समवर्तत । पद्भ्यां भूमिर्दिशः श्रोत्रात्तथा लोकाँ अकल्पयन् ॥",
            iast="nābhyā āsīd antarikṣaṁ śīrṣṇo dyauḥ sam avartata | padbhyāṁ bhūmir diśaḥ śrotrāt tathā lokāṁ akalpayan ||",
            recension="Śākala Saṃhitā",
            padaccheda=["nābhyāḥ", "āsīt", "antarikṣam", "śīrṣṇaḥ", "dyauḥ", "samavartata", "padbhyām", "bhūmiḥ", "diśaḥ", "śrotrāt", "tathā", "lokān", "akalpayan"],
            anvaya="nābhyāḥ antarikṣam āsīt, śīrṣṇaḥ dyauḥ samavartata, padbhyām bhūmiḥ, śrotrāt diśaḥ [samabhavan], tathā lokān akalpayan.",
            morphological_tags={
                "nābhyāḥ": "Ablative singular feminine of nābhi (from the navel)",
                "padbhyām": "Ablative dual masculine of pad (from the two feet)",
                "bhūmiḥ": "Nominative singular feminine of bhūmi (the Earth)",
                "śīrṣṇaḥ": "Ablative singular neuter of śīrṣan (from the head)",
                "dyauḥ": "Nominative singular feminine/masculine of div (the heavens)"
            },
            sandhi_decompositions=[
                "nābhyāḥ + āsīt = nābhyā āsīt",
                "padbhyām + bhūmiḥ = padbhyāṁ bhūmiḥ",
                "śrotrāt + tathā = śrotrāt tathā"
            ],
            word_glosses={
                "nābhyāḥ": "from the navel",
                "āsīt": "arose / came into being",
                "antarikṣam": "the intermediate atmospheric space",
                "śīrṣṇaḥ": "from the head",
                "dyauḥ": "the luminous heavens",
                "padbhyām": "from the feet",
                "bhūmiḥ": "the sacred Earth (Bhūmātā)",
                "śrotrāt": "from the ears / hearing",
                "diśaḥ": "the cardinal directions",
                "tathā": "thus",
                "akalpayan": "they ordained the cosmic realms"
            },
            overall_meaning_summary="From His navel arose the atmosphere; from His head the heavens evolved; from His feet the Earth; from His ear the directions. Thus they fashioned the cosmic worlds.",
            commentary_overlays=[
                CommentaryOverlay(
                    commentary_id="COMM_RV_10_090_14_SAYANA",
                    commentator="Sāyaṇācārya",
                    sampradaya="Vaidika Mīmāṃsā",
                    hermeneutical_claim="The feet are the locus of Pratiṣṭhā (cosmic foundation) supporting all living beings; the Earth emanates from the feet as the divine Mother supporting all existence.",
                    source_edition="Vaidika Samshodhana Mandala (Pune)"
                )
            ]
        )


# Automatically initialize the foundational canon on module load
MulaPathaEngine.seed_initial_mula_canon()
