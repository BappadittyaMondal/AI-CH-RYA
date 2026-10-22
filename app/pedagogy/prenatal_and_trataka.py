"""Prenatal Auditory Safety & Trāṭaka Meditation Engines (app/pedagogy/prenatal_and_trataka.py)

Implements:
1. PrenatalAuditorySafetyEngine: Demarcates valid maternal-fetal biology and Ayurvedic
   Garbha Saṃskāra from commercial pseudoscientific 'fetal genius' training claims.
2. TratakaMeditationEngine: Evaluates authentic Haṭha Yoga Trāṭaka (HYP 2.31-32)
   with strict neuro-ophthalmic safety guidelines, phototoxicity prevention, and medical contraindications.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any


# ==============================================================================
# Domain 1: Prenatal Auditory & Maternal Safety
# ==============================================================================

class PrenatalClaimType(str, Enum):
    AUTHENTIC_MATERNAL_CARE = "AUTHENTIC_MATERNAL_CARE (Ayurvedic Garbha Saṃskāra)"
    AUDITORY_HABITUATION = "AUDITORY_HABITUATION (Fetal Sensory Rhythm Recognition)"
    TACTICAL_GENIUS_PSEUDOSCIENCE = "TACTICAL_GENIUS_PSEUDOSCIENCE (Chakravyūha Fetal Military Training)"


@dataclass
class PrenatalAuditResult:
    query: str
    claim_type: PrenatalClaimType
    is_commercial_pseudoscience: bool
    empirical_neurobiology_verdict: str
    ayurvedic_shastric_context: str
    classical_metaphysical_explanation: str
    commercial_scam_warning: str


class PrenatalAuditorySafetyEngine:
    """Engine assessing prenatal fetal learning and maternal Garbha Saṃskāra claims."""

    @classmethod
    def audit_claim(cls, text: str) -> PrenatalAuditResult:
        text_lower = text.lower()

        is_military_or_genius = any(k in text_lower for k in [
            "abhimanyu", "chakravyuh", "chakravyuha", "military tactics in womb",
            "teach engineering to baby", "make genius baby in womb", "fetal high iq"
        ])

        if is_military_or_genius:
            return PrenatalAuditResult(
                query=text,
                claim_type=PrenatalClaimType.TACTICAL_GENIUS_PSEUDOSCIENCE,
                is_commercial_pseudoscience=True,
                empirical_neurobiology_verdict=(
                    "Empirical embryology and audiology confirm that the human fetal auditory system becomes functional "
                    "between 24 and 28 weeks of gestation. Fetuses can perceive low-frequency vowels, maternal voice cadence, "
                    "and rhythm (DeCasper & Spence 1986; Partanen et al. 2013 PNAS). However, symbolic language comprehension, "
                    "spatial geometry, and complex tactical maneuvers (such as a 7-layered Chakravyūha military formation) require "
                    "an operational cerebral cortex and prefrontal executive synthesis, which do not exist in utero."
                ),
                ayurvedic_shastric_context=(
                    "Suśruta Saṃhitā (Śārīrasthāna 3.30) notes that consciousness (Cetanā-dhātu) expresses in the 4th month "
                    "as the fetal heart and limbs differentiate. Caraka Saṃhitā (Śārīrasthāna 4.15) emphasizes the Dauhṛda "
                    "(bi-cardiac) stage, where maternal emotional serenity directly affects fetal vitality. Classical Ayurveda "
                    "prescribes Saumanasya (maternal mental peace, sattvic diet, melodious chanting), not technical schooling."
                ),
                classical_metaphysical_explanation=(
                    "In classical Itihāsa hermeneutics, Abhimanyu's intuitive battlefield capability represents trans-migratory "
                    "Pūrva-Janma Saṃskāras (predispositions accumulated across past lives) manifesting through poetic hyperbole "
                    "(Atiśayokti), not literal in-utero classroom education."
                ),
                commercial_scam_warning=(
                    "Beware commercial 'Garbha Sanskar' packages and apps that promise to create 'instant genius' or 'super-baby' "
                    "graduates for exorbitant fees. These exploit parental anxiety through pseudoscientific marketing."
                )
            )

        # Authentic Ayurvedic Maternal Inquiry
        return PrenatalAuditResult(
            query=text,
            claim_type=PrenatalClaimType.AUTHENTIC_MATERNAL_CARE,
            is_commercial_pseudoscience=False,
            empirical_neurobiology_verdict=(
                "Maternal stress hormones (cortisol) cross the placental barrier and can negatively impact fetal development. "
                "Gentle music, maternal reading, and calm emotional environments promote parasympathetic tone and healthy gestation."
            ),
            ayurvedic_shastric_context=(
                "Caraka and Suśruta emphasize Dauhṛdāvamāna (fulfilling the healthy desires of the pregnant mother) and Sattvavajaya "
                "(mental equilibrium) to ensure optimal progeny health."
            ),
            classical_metaphysical_explanation=(
                "The womb is an environment of gentle nurturance where positive rhythmic vibrations create favorable Saṃskāras."
            ),
            commercial_scam_warning="Standard prenatal care should focus on medical nutrition, obstetric monitoring, and maternal wellbeing."
        )


# ==============================================================================
# Domain 2: Trāṭaka Meditation & Ophthalmic Safety
# ==============================================================================

class TratakaPracticeType(str, Enum):
    BAHIR_TRATAKA = "BAHIR_TRATAKA (External Steady Gazing - Flame / Dot)"
    ANTAR_TRATAKA = "ANTAR_TRATAKA (Internal Visual Concentration - Mental Image)"
    OCCULT_HYPE_PSEUDOSCIENCE = "OCCULT_HYPE_PSEUDOSCIENCE (Instant Third-Eye Telepathy Claims)"


@dataclass
class TratakaAuditResult:
    query: str
    practice_type: TratakaPracticeType
    is_safe: bool
    medical_contraindications: List[str]
    neuro_ophthalmic_mechanism: str
    hatha_yoga_shastric_foundation: str
    safety_guidelines: List[str]
    occult_hype_refutation: str


class TratakaMeditationEngine:
    """Engine auditing Trāṭaka meditation practice with strict ophthalmic safety gates."""

    @classmethod
    def audit_practice(cls, text: str, user_has_eye_condition: bool = False) -> TratakaAuditResult:
        text_lower = text.lower()

        is_occult = any(k in text_lower for k in [
            "third eye open in 21 days", "psychic vision", "x-ray vision tratak",
            "telepathy tratak", "instant superpower tratak"
        ])

        contraindications = [
            "Absolute: Glaucoma (intraocular pressure elevation).",
            "Absolute: Retinal detachment or severe degenerative retinopathy.",
            "Relative: Severe uncorrected myopia / astigmatism (risk of acute eye strain).",
            "Relative: Chronic dry eye syndrome (keratoconjunctivitis sicca).",
            "Psychiatric: Vulnerability to visual hallucinations or psychosis (Troxler fading can induce perceptual distortions)."
        ]

        if is_occult:
            return TratakaAuditResult(
                query=text,
                practice_type=TratakaPracticeType.OCCULT_HYPE_PSEUDOSCIENCE,
                is_safe=False,
                medical_contraindications=contraindications,
                neuro_ophthalmic_mechanism=(
                    "Fixating gaze without blinking suppresses microsaccades and induces Troxler's fading—the peripheral visual field "
                    "temporarily fades from awareness due to retinal adaptation in the visual cortex. This promotes alpha brainwave "
                    "synchronization (8–12 Hz) and focused attention, not supernatural optical powers."
                ),
                hatha_yoga_shastric_foundation=(
                    "Haṭha Yoga Pradīpikā 2.31–32 categorizes Trāṭaka as one of the Ṣaṭkarmas (purificatory actions): "
                    "'Looking intently with an unblinking gaze at a minute point until tears fall'. Its purpose is Śodhana "
                    "(cleansing ocular dullness and sluggishness) preparatory to Dhāraṇā (concentration), not occult voyeurism."
                ),
                safety_guidelines=[
                    "Never practice flame gazing closer than 1 meter (minimum safe distance: 3–4 feet).",
                    "Do not exceed 3 to 5 minutes of flame gazing for beginners (maximum 10 minutes for advanced practitioners).",
                    "Extinguish the candle and gently cup eyes with warm palms (Palming) following practice."
                ],
                occult_hype_refutation=(
                    "Claims of gaining supernatural telepathy or x-ray clairvoyance in 21 days are commercial clickbait. "
                    "Authentic Yoga targets Citta-Śuddhi (mental purity) and focus, not circus performances."
                )
            )

        # Legitimate Practice Evaluation
        return TratakaAuditResult(
            query=text,
            practice_type=TratakaPracticeType.BAHIR_TRATAKA,
            is_safe=not user_has_eye_condition,
            medical_contraindications=contraindications,
            neuro_ophthalmic_mechanism=(
                "Stabilizes optic nerve signaling, reduces visual cognitive noise, and triggers lacrimal gland flushing, "
                "which cleanses the cornea and stimulates parasympathetic relaxation via the facial nerve."
            ),
            hatha_yoga_shastric_foundation=(
                "Haṭha Yoga Pradīpikā 2.31: निरीक्षेन् निश्चलदृशा सूक्ष्मलक्ष्यं समाहितः। अश्रुसम्पातपर्यन्तम् आचार्यैस् त्राटकं स्मृतम्॥ "
                "Trāṭaka is a revered concentration builder that calms mental agitation."
            ),
            safety_guidelines=[
                "Place candle flame exactly at eye level, 3 to 4 feet away, in a draft-free dark room.",
                "Blink naturally if eyes burn; do not forcibly restrain blinking to the point of severe corneal abrasion.",
                "Conclude immediately with cold water splash and 2 minutes of palming."
            ],
            occult_hype_refutation="Trāṭaka is a classical concentration technique; ground your expectations in mental tranquility."
        )
