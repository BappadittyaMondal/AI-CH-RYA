"""
AI ĀCHĀRYA — Advaita Vedānta Prakaraṇa Pedagogy Engine (app/pedagogy/vedanta_prakarana.py)

Models systematic Upaniṣadic and Prakaraṇa pedagogy based on Ādi Śaṅkarācārya's Ātmabodha (68 verses):
1. Adhikārī Qualification (Sādhana-Catuṣṭaya).
2. Adhyāsa Deconstruction (Rajjusarpa & Śuktirajat superimposition).
3. Upādhi & Pañca-kośa Apavāda (Negation of 3 bodies and 5 sheaths).
4. Sākṣī Caitanya Isolation (The Unattached Witness).
5. Mahāvākya Identity via Bhāga-tyāga-lakṣaṇā (Tat Tvam Asi).
6. Jīvanmukti & Saccidānanda Realization (Nirvāṇaṣaṭkam culmination).
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional
import re


class VedantaPedagogyStage(str, Enum):
    STAGE_1_ADHIKARI = "1. Adhikārī Qualification (Sādhana Catuṣṭaya & Mumukṣutva)"
    STAGE_2_ADHYASA = "2. Adhyāsa Discrimination (Superimposition: Rope/Snake & Silver/Shell)"
    STAGE_3_APAVADA = "3. Upādhi & Pañca-Kośa Apavāda (Deconstruction of 3 Bodies & 5 Sheaths)"
    STAGE_4_SAKSHI = "4. Sākṣī Isolation (The Unattached Witness Consciousness)"
    STAGE_5_MAHAVAKYA = "5. Mahāvākya Identity (Tat Tvam Asi via Bhāgatyāga-lakṣaṇā)"
    STAGE_6_JIVANMUKTI = "6. Jīvanmukti & Saccidānanda Realization (Cidānanda-rūpaḥ Śivo'ham)"


@dataclass(frozen=True)
class AtmabodhaPedagogyReport:
    inquiry_text: str
    target_stage: VedantaPedagogyStage
    primary_verse_citation: str
    epistemic_principle: str
    pedagogical_analogy: str
    upadhi_analysis: str
    practical_sadhana: str
    nirvana_satkam_culmination: str


class AtmabodhaPrakaranaEngine:
    """
    Renders step-by-step Vedāntic pedagogy for philosophical inquiries,
    guiding seekers from empirical confusion to direct realization.
    """

    @classmethod
    def analyze_inquiry(cls, inquiry_text: str) -> AtmabodhaPedagogyReport:
        """
        Determines the relevant Vedāntic pedagogical stage and constructs
        a rigorous Prakaraṇa resolution grounded in Ātmabodha.
        """
        q_lower = inquiry_text.lower()

        # Stage 5 / 6: Mahavakya or Jivanmukti
        if any(k in q_lower for k in ["tat tvam asi", "aham brahmasmi", "jivanmukti", "sivoham", "shivo hum", "nirvana satkam", "liberated while alive"]):
            stage = VedantaPedagogyStage.STAGE_6_JIVANMUKTI
            verse = "Ātmabodha 68: 'तीर्थादिकं न चापेक्ष्य स्वात्मन्येव प्रलीयते। स सर्वविद्भवत्येको ह्यमृतोऽसंशयं नरः॥'"
            principle = "Direct Non-Dual Abidance: The Jīvanmukta transcends pilgrimage, ritual, and time, resting in the self-luminous Ātman."
            analogy = "Like a drop merging into the ocean, or the space in a pot merging into infinite space when the pot breaks."
            upadhi = "All Upādhis (gross, subtle, causal) are recognized as transient mental projections, leaving unconditioned Saccidānanda."
            sadhana = "Rest continuously in the witness state without claiming authorship of thoughts or bodily actions (Karma-phala-tyāga)."
            culmination = "चिदानन्दरूपः शिवोऽहम् शिवोऽहम् — I am Pure Consciousness and Bliss, I am Śiva."

        # Stage 4: Sakshi / Witness Consciousness
        elif any(k in q_lower for k in ["witness", "sakshi", "sākṣī", "who am i", "observer", "mind vs consciousness"]):
            stage = VedantaPedagogyStage.STAGE_4_SAKSHI
            verse = "Ātmabodha 19: 'व्यापृतेष्विन्द्रियेष्वात्मा व्यापारीवाविवेकिनाम्। दृश्यतेऽभ्रेषु धावत्सु धावन्निव यथा शशी॥'"
            principle = "The Self is motionless and unaffected; it appears active only due to the movement of the mind and senses."
            analogy = "Like the moon appearing to run across the night sky when clouds rapidly drift over it."
            upadhi = "Separates Sākṣī (Consciousness) from Sākṣya (the objects of awareness: body, thoughts, emotions)."
            sadhana = "Practice Neti-Neti (Not this, not this): Whenever an emotion or pain arises, notice: 'I am the observer of this, not the sensation itself.'"
            culmination = "The witness is ever-free, uncontaminated by mental grief or bodily illness."

        # Stage 3: Panchakosha / Upadhi Deconstruction
        elif any(k in q_lower for k in ["pancha kosha", "pañca-kośa", "5 sheaths", "three bodies", "subtle body", "annamaya", "pranamaya", "gross body"]):
            stage = VedantaPedagogyStage.STAGE_3_APAVADA
            verse = "Ātmabodha 14: 'वपुस्तुषादिभिः कोशैर्युक्तं युक्तं तु कण्डनात्। आत्मानमन्तरं शुद्धं विविच्यात्तण्डुलं यथा॥'"
            principle = "The pure Self inside the 5 sheaths must be discriminated like husked rice from paddy grains through pounding."
            analogy = "Like pounding paddy in a mortar to separate the pure white grain of rice from the outer brown husk."
            upadhi = "Negates identification with Annamaya (food), Prāṇamaya (energy), Manomaya (desire), Vijñānamaya (intellect), and Ānandamaya (dormant bliss)."
            sadhana = "Systematic cognitive peeling: Recognize each sheath as an object perceived in waking, dream, or deep sleep."
            culmination = "Transcendence of the 3 bodies yields the birthless, deathless Ātman."

        # Stage 2: Adhyasa / Superimposition
        elif any(k in q_lower for k in ["adhyasa", "superimposition", "rope snake", "illusion", "maya", "rajjusarpa", "mirage"]):
            stage = VedantaPedagogyStage.STAGE_2_ADHYASA
            verse = "Ātmabodha 7: 'तावत्सत्यं जगद्भाति शुक्तिकारजतं यथा। यावन्न ज्ञायते ब्रह्म सर्वाधिष्ठानमद्वयम्॥'"
            principle = "The empirical universe appears real only so long as the non-dual Brahman, the substratum of all, remains unrealized."
            analogy = "Like the terrifying appearance of a venomous snake in a harmless coiled rope in dim twilight."
            upadhi = "Avidyā projects name and form (Nāma-Rūpa) on pure Consciousness."
            sadhana = "Bring the lamp of knowledge: Once a flashlight reveals the rope, the fear of snakebite vanishes forever without a physical battle."
            culmination = "Ignorance is dispelled by Knowledge alone, never by action (Ātmabodha v. 3)."

        # Default Stage 1: Adhikari & Jñana direct cause
        else:
            stage = VedantaPedagogyStage.STAGE_1_ADHIKARI
            verse = "Ātmabodha 2: 'बोधोऽन्यसाधनेभ्यो हि साक्षात् मोक्षैकसाधनम्। पाकस्य वह्निवत् ज्ञानं विना मोक्षो न सिध्यति॥'"
            principle = "Knowledge (Jñāna) is the direct, indispensable instrument of Liberation, exactly as fire is for cooking."
            analogy = "Like fire to cooking: Spoons, water, and pots are auxiliary, but without fire no cooking occurs."
            upadhi = "Action (Karma) prepares the vessel by purifying the mind (Citta-śuddhi), but only direct inquiry dispels ignorance."
            sadhana = "Cultivate Sādhana-Catuṣṭaya: Viveka (discrimination), Vairāgya (dispassion), Ṣaṭ-sampatti (inner restraint), and Mumukṣutva (longing for truth)."
            culmination = "Knowledge of the Self is not intellectual data collection, but direct awakening (Aparokṣānubhūti)."

        return AtmabodhaPedagogyReport(
            inquiry_text=inquiry_text,
            target_stage=stage,
            primary_verse_citation=verse,
            epistemic_principle=principle,
            pedagogical_analogy=analogy,
            upadhi_analysis=upadhi,
            practical_sadhana=sadhana,
            nirvana_satkam_culmination=culmination
        )
