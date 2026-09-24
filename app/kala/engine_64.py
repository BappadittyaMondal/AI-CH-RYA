"""
64 Kalā Engine (§18)
Manages classical Indian arts and sciences across variant traditional lists
(Vātsyāyana's Kāmasūtra, Bhāgavata Purāṇa, Śukranīti), providing modern equivalents
and practical exercises without flattening tradition-specific variations.
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class KalaArt(BaseModel):
    number: int
    sanskrit_term: str
    transliteration_iast: str
    source_tradition: str  # e.g. "Kāmasūtra 1.3.15", "Bhāgavata Purāṇa 10.45"
    translation: str
    historical_meaning: str
    traditional_interpretation: str
    modern_equivalent: str
    domain: str  # e.g. "Aesthetics & Performing Arts", "Design & Engineering", "Linguistics & Memory", "Martial/Physical"
    practical_project_exercise: str
    exemplars: List[str] = Field(default_factory=list)


# Foundational sample from classical Vātsyāyana corpus
SAMPLE_KALA_REGISTRY: List[KalaArt] = [
    KalaArt(
        number=1,
        sanskrit_term="गीतम्",
        transliteration_iast="Gītam",
        source_tradition="Kāmasūtra 1.3.15",
        translation="Art of Singing and Vocal Music",
        historical_meaning="Cultivation of svara, rāga, tāla, and devotional singing.",
        traditional_interpretation="Vocal harmony resonating with Nāda-Brahman.",
        modern_equivalent="Vocal performance, acoustic training, sound design.",
        domain="Performing Arts",
        practical_project_exercise="Learn the foundational sapta-svaras and perform a 5-minute vocal scale calibration in Rāga Bhairavī.",
        exemplars=["Tānsen", "Purandara Dāsa", "Tyāgarāja"]
    ),
    KalaArt(
        number=2,
        sanskrit_term="वाद्यम्",
        transliteration_iast="Vādyam",
        source_tradition="Kāmasūtra 1.3.15",
        translation="Art of Instrumental Music",
        historical_meaning="Mastery over the four classes of instruments: tata, suṣira, avanaddha, ghana.",
        traditional_interpretation="Translating inner rhythm and breath into instrumental resonance.",
        modern_equivalent="Multi-instrumental musicianship and audio orchestration.",
        domain="Performing Arts",
        practical_project_exercise="Practice rhythmic subdivisions (tāla exercises) on a percussion or stringed instrument.",
        exemplars=["Ustad Bismillah Khan", "Pandit Ravi Shankar"]
    ),
    KalaArt(
        number=3,
        sanskrit_term="नृत्यम्",
        transliteration_iast="Nṛtyam",
        source_tradition="Kāmasūtra 1.3.15",
        translation="Art of Dance and Expressive Movement",
        historical_meaning="Integration of bhāva, rāga, and tāla using body language and mudrās.",
        traditional_interpretation="Embodied storytelling and spiritual surrender through movement.",
        modern_equivalent="Choreography, kinetic arts, physical theater.",
        domain="Performing Arts",
        practical_project_exercise="Master 5 fundamental asamyuta (single-hand) mudrās from the Abhinaya Darpaṇa.",
        exemplars=["Rukmini Devi Arundale", "Kelucharan Mohapatra"]
    ),
    KalaArt(
        number=4,
        sanskrit_term="आलेख्यम्",
        transliteration_iast="Ālekhyam",
        source_tradition="Kāmasūtra 1.3.15",
        translation="Art of Painting and Visual Composition",
        historical_meaning="Execution of visual art using the six limbs of painting (Ṣaḍaṅga).",
        traditional_interpretation="Manifesting the unseen forms and moods through proportion (pramāṇa) and color (varṇikābhaṅga).",
        modern_equivalent="Visual fine arts, UI/UX design, digital illustration.",
        domain="Design & Fine Arts",
        practical_project_exercise="Create a compositional sketch illustrating the principle of Bhāva (emotion) and Pramāṇa (proportion).",
        exemplars=["Raja Ravi Varma", "Nandalal Bose"]
    ),
    KalaArt(
        number=44,
        sanskrit_term="मानसीकाव्यक्रिया",
        transliteration_iast="Mānasī-kāvya-kriyā",
        source_tradition="Kāmasūtra 1.3.15",
        translation="Art of Mental Poetic Composition & Improvisation",
        historical_meaning="Composing sophisticated verses mentally without pen or paper in real-time.",
        traditional_interpretation="Unobstructed flow of Sarasvatī in the purified intellect (dhī).",
        modern_equivalent="Creative writing, rapid ideation, extemporaneous speech, freestyle composition.",
        domain="Linguistics & Memory",
        practical_project_exercise="Compose a 4-line poem in Anuṣṭubh meter (or English iambic tetrameter) purely in mind before writing it down.",
        exemplars=["Kālidāsa", "Bāṇabhaṭṭa"]
    ),
    KalaArt(
        number=58,
        sanskrit_term="वास्तुविद्या",
        transliteration_iast="Vāstu-vidyā",
        source_tradition="Kāmasūtra 1.3.15 / Mānasāra",
        translation="Art of Architecture, Spatial Design & Construction",
        historical_meaning="Harmonizing built environments with cardinal directions, solar paths, and cosmic mandalas.",
        traditional_interpretation="Architecture as an extension of the cosmic Puruṣa (Vāstupuruṣa Maṇḍala).",
        modern_equivalent="Sustainable architecture, civil engineering, ergonomic spatial planning.",
        domain="Design & Engineering",
        practical_project_exercise="Draft a floor plan for a quiet study space incorporating natural light orientation and ventilation.",
        exemplars=["Maya Dānava", "Viśvakarmā"]
    )
]


class KalaEngine:
    """Provides querying and pedagogical exploration of the 64 Kalās."""

    @classmethod
    def get_by_number(cls, number: int) -> Optional[KalaArt]:
        for art in SAMPLE_KALA_REGISTRY:
            if art.number == number:
                return art
        return None

    @classmethod
    def search_by_domain_or_term(cls, query: str) -> List[KalaArt]:
        q = query.lower()
        results = []
        for art in SAMPLE_KALA_REGISTRY:
            if (
                q in art.sanskrit_term.lower()
                or q in art.transliteration_iast.lower()
                or q in art.translation.lower()
                or q in art.modern_equivalent.lower()
                or q in art.domain.lower()
            ):
                results.append(art)
        return results
