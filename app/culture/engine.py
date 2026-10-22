"""
AI ĀCHĀRYA — Bhāratīya Culture Engine (app/culture/engine.py)

Models the living cultural reality of Sanātana Paramparā:
1. Kālacakra & Pañcāṅga: Five limbs of time, Ṣaḍ-Ṛtu seasons, Ṛtucaryā health, and astronomical festival cycles.
2. Ṣoḍaśa Saṃskāras: 16 lifecycle rites with psychological developmental grounding and universal core vs mutable accretions.
3. Mandira-Pariveśa: The temple as an architectural cosmogram, economic redistributor, arts conservatory, and community sanctuary.
4. Lokācāra-Śāstrācāra Samanvaya: Harmonizing regional folk traditions (Deśācāra/Kulācāra) with classical Śāstric jurisprudence using Mīmāṃsā principles.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
import math
import re


class PancangaLimb(str, Enum):
    TITHI = "Tithi (Lunar Day - Moon/Sun 12° Arc)"
    VARA = "Vāra (Solar Weekday - Planetary Ruler)"
    NAKSATRA = "Nakṣatra (Lunar Mansion - 13°20' Arc)"
    YOGA = "Yoga (Luni-Solar Angular Sum - 13°20' Arc)"
    KARANA = "Karaṇa (Half Tithi - 6° Arc)"


class RituSeason(str, Enum):
    VASANTA = "Vasanta (Spring - Caitra/Vaiśākha - Kapha Liquefaction)"
    GRISMA = "Grīṣma (Summer - Jyeṣṭha/Āṣāḍha - Pitta Accumulation)"
    VARSA = "Varṣā (Monsoon - Śrāvaṇa/Bhādrapada - Vāta Aggravation)"
    SARAD = "Śarad (Autumn - Āśvina/Kārttika - Pitta Aggravation/Cleansing)"
    HEMANTA = "Hemanta (Early Winter - Mārgaśīrṣa/Pauṣa - Strong Digestion)"
    SISIRA = "Śiśira (Late Winter - Māgha/Phālguna - Kapha Accumulation)"


class SamskaraStage(str, Enum):
    PRE_NATAL = "Garba / Pre-Natal Phase"
    INFANCY_CHILDHOOD = "Śiśu / Childhood Development"
    EDUCATIONAL_YOUTH = "Brahmacarya / Learning & Initiation"
    HOUSEHOLDER_ADULT = "Gṛhastha / Social & Familial Responsibility"
    TRANSCENDENT = "Antyeṣṭi / Transition to the Ancestral & Transcendent"


@dataclass(frozen=True)
class SamskaraRecord:
    samskara_id: str
    canonical_name: str
    transliteration: str
    stage: SamskaraStage
    traditional_timing: str
    psychological_purpose: str
    spiritual_ontological_core: str
    historical_mutable_accretions: str
    primary_textual_sources: List[str]


@dataclass(frozen=True)
class TempleEcosystemRecord:
    temple_id: str
    canonical_name: str
    tradition: str  # "AGAMA_SAIVA", "AGAMA_VAISNAVA", "SAKTA_PITHA", "SMARTA"
    architectural_style: str  # "DRAVIDA", "NAGARA", "VESARA", "KALINGA"
    cosmogram_feature: str
    economic_functions: List[str]
    arts_patronage: List[str]
    community_refuge_role: str
    inscriptional_provenance: str


@dataclass(frozen=True)
class PancangaComputationResult:
    solar_longitude_deg: float
    lunar_longitude_deg: float
    tithi_number: int
    tithi_name: str
    paksha: str
    nakshatra_number: int
    nakshatra_name: str
    yoga_number: int
    yoga_name: str
    karana_name: str
    associated_season: RituSeason
    seasonal_regimen: str


class CultureEngine:
    """
    Comprehensive engine for Bhāratīya living culture, Pañcāṅga cosmic time,
    16 lifecycle Saṃskāras, and temple ecosystems.
    """

    NAKSHATRAS = [
        "Aśvinī", "Bharaṇī", "Kṛttikā", "Rohiṇī", "Mṛgaśīrṣā", "Ārdrā",
        "Punarvasu", "Puṣya", "Āśleṣā", "Maghā", "Pūrvaphalgunī", "Uttarāphalgunī",
        "Hasta", "Citrā", "Svātī", "Viśākhā", "Anurādhā", "Jyeṣṭhā",
        "Mūla", "Pūrvāṣāḍhā", "Uttarāṣāḍhā", "Śravaṇa", "Dhaniṣṭhā", "Śatabhiṣā",
        "Pūrvabhādrapadā", "Uttarabhādrapadā", "Revatī"
    ]

    TITHIS = [
        "Pratipad", "Dvitīyā", "Tṛtīyā", "Caturthī", "Pañcamī", "Ṣaṣṭhī",
        "Saptamī", "Aṣṭamī", "Navamī", "Daśamī", "Ekādaśī", "Dvādaśī",
        "Trayodaśī", "Caturdaśī", "Pūrṇimā / Amāvāsyā"
    ]

    YOGAS = [
        "Viṣkambha", "Prīti", "Āyuṣmān", "Saubhāgya", "Śobhana", "Atigaṇḍa",
        "Sukarma", "Dhṛti", "Śūla", "Gaṇḍa", "Vṛddhi", "Dhruva", "Vyāghāta",
        "Harṣaṇa", "Vajra", "Siddhi", "Vyatīpāta", "Varīyān", "Parigha",
        "Śiva", "Siddha", "Sādhya", "Śubha", "Śukla", "Brahma", "Māhendra", "Vaidhṛti"
    ]

    def __init__(self):
        self._samskaras: Dict[str, SamskaraRecord] = {}
        self._temple_ecosystems: Dict[str, TempleEcosystemRecord] = {}
        self._load_seed_culture()

    def _load_seed_culture(self):
        # 1. Ṣoḍaśa Saṃskāras (Key Representative Lifecycle Transitions)
        self._samskaras["garbhadhana"] = SamskaraRecord(
            samskara_id="SAM-001",
            canonical_name="गर्भाधान",
            transliteration="Garbhādhāna",
            stage=SamskaraStage.PRE_NATAL,
            traditional_timing="Prior to conception",
            psychological_purpose="Conscious, intentional entry into parenthood; aligns psychological mindfulness, mutual consent, and emotional serenity between partners.",
            spiritual_ontological_core="Invocation of cosmic vitality (Prajāpati) to invite an elevated consciousness into embodiment; elevates biological procreation into a sacred yajña.",
            historical_mutable_accretions="Medieval astrology-driven rigid hourly taboos that deviated from the foundational Vedic intent of emotional and somatic tranquility.",
            primary_textual_sources=["Bṛhadāraṇyaka Upaniṣad 6.4.13-24", "Āśvalāyana Gṛhyasūtra 1.13", "Caraka Saṃhitā Śārīrasthāna 8"]
        )

        self._samskaras["upanayana"] = SamskaraRecord(
            samskara_id="SAM-007",
            canonical_name="उपनयन",
            transliteration="Upanayana",
            stage=SamskaraStage.EDUCATIONAL_YOUTH,
            traditional_timing="Between age 8 and 16 (commencement of formal education)",
            psychological_purpose="Formal transition from familial indulgence to self-disciplined discipleship; imparts self-governance, intellectual accountability, and inner focus (Brahmacarya).",
            spiritual_ontological_core="The 'second birth' (Dvija)—birth into consciousness, wisdom, and cosmic debt (*Rna*) awareness through the Gāyatrī Mantra and the sacred thread (*Yajñopavīta*).",
            historical_mutable_accretions="Rigid hereditary gender and caste exclusion developed in medieval feudal phases, contrasting with early historical evidence of Brahmavādinī women (e.g., Gārgī, Maitreyī) and Jabala Satyakāma's admission based on truthfulness rather than lineage (Chāndogya Upaniṣad 4.4).",
            primary_textual_sources=["Chāndogya Upaniṣad 4.4", "Pāraskara Gṛhyasūtra 2.2", "Manusmṛti 2.36-68"]
        )

        self._samskaras["vivaha"] = SamskaraRecord(
            samskara_id="SAM-015",
            canonical_name="विवाह",
            transliteration="Vivāha",
            stage=SamskaraStage.HOUSEHOLDER_ADULT,
            traditional_timing="Adulthood / Entry into Gṛhasthāśrama",
            psychological_purpose="Partnership formation founded on shared dharma, companionship, emotional maturity, and mutual commitment; solemnized by the Saptapadī (Seven Steps).",
            spiritual_ontological_core="The union of two autonomous beings becoming co-custodians of societal continuity (*Lokasaṅgraha*), sustaining the elderly, children, ascetics, and public welfare.",
            historical_mutable_accretions="Dowry demands, commodification of marriage, and forced child matches which directly violate Śāstric prohibitions against treating daughters as barter (e.g. Manusmṛti 3.51-54 condemning bride-price and dowry).",
            primary_textual_sources=["Rigveda 10.85 (Sūryā Vivāha Sūkta)", "Āpastamba Gṛhyasūtra 1.2-4", "Manusmṛti 3.20-35"]
        )

        self._samskaras["antyesti"] = SamskaraRecord(
            samskara_id="SAM-016",
            canonical_name="अन्त्येष्टि",
            transliteration="Antyeṣṭi",
            stage=SamskaraStage.TRANSCENDENT,
            traditional_timing="At somatic death",
            psychological_purpose="Structured communal closure, emotional catharsis, and grief resolution for the bereaved family; emphasizes the transience of physical form and permanence of Ātman.",
            spiritual_ontological_core="The final sacrifice (Antya-Iṣṭi) returning the five gross elements (*Pañcamahābhūta*) of the body back to their cosmic origins through Agni, releasing the Jīva into its next cosmic trajectory.",
            historical_mutable_accretions="Exploitative funerary commercialization and superstitious fears of wandering spirits, which deviate from the serenity of the Vedic funeral hymns.",
            primary_textual_sources=["Rigveda 10.14-18", "Baudhāyana Pitṛmedhasūtra", "Garuḍa Purāṇa Sāroddhāra"]
        )

        # 2. Temple Ecosystems (Representative Core Exemplars)
        self._temple_ecosystems["thanjavur_brihadisvara"] = TempleEcosystemRecord(
            temple_id="TEM-001",
            canonical_name="Brihadīśvara Temple (Rajarajesvaram), Thanjavur",
            tradition="AGAMA_SAIVA",
            architectural_style="DRAVIDA",
            cosmogram_feature="Granite Vimana rising 66 meters; single 80-tonne monolithic granite cupola capstone; Vāstu-Puruṣa-Maṇḍala geometric alignment.",
            economic_functions=[
                "Employed over 600 temple servants, 400 dedicated classical dancers, musicians, accountants, and bronze casters.",
                "Functioned as a state treasury and central agricultural lending bank offering fixed low-interest loans during monsoon failures.",
                "Maintained revenue registries from hundreds of endowment villages (Brahmadeya & Devadana)."
            ],
            arts_patronage=[
                "Carved Bharatanatyam 108 Karana friezes on the upper sanctum gallery.",
                "Center for the preservation of Chola bronze casting (Lost-wax Nataraja) and classical Tevaram hymn chanting."
            ],
            community_refuge_role="Massive outer stone ramparts and grain storehouses (*Kottaram*) sheltering thousands during siege and severe flood emergencies.",
            inscriptional_provenance="Over 100 Tamil and Sanskrit stone inscriptions detailing every royal, military, and civilian donation down to fractions of a gram."
        )

    # 3. Kālacakra Calculation Engine
    def compute_pancanga(self, solar_deg: float, lunar_deg: float) -> PancangaComputationResult:
        """
        Computes the five temporal limbs (Tithi, Nakṣatra, Yoga, Karaṇa)
        from Sun and Moon celestial longitudes (in degrees 0-360).
        """
        if math.isnan(solar_deg) or math.isnan(lunar_deg) or math.isinf(solar_deg) or math.isinf(lunar_deg):
            raise ValueError("Celestial longitudes must be finite real numbers.")

        # Normalize longitudes
        s_deg = solar_deg % 360.0
        l_deg = lunar_deg % 360.0

        # 1. Tithi: Difference between Moon and Sun (12 degrees per Tithi)
        diff = (l_deg - s_deg) % 360.0
        tithi_raw = diff / 12.0
        tithi_idx = int(math.floor(tithi_raw)) + 1  # 1 to 30

        if tithi_idx <= 15:
            paksha = "Śukla Pakṣa (Waxing Fortnight)"
            t_name = self.TITHIS[tithi_idx - 1]
        else:
            paksha = "Kṛṣṇa Pakṣa (Waning Fortnight)"
            t_name = self.TITHIS[(tithi_idx - 16)]

        # 2. Nakshatra: Moon longitude divided by 13°20' (13.333333°)
        nakshatra_span = 360.0 / 27.0  # 13.333333333333334
        nak_idx = int(math.floor(l_deg / nakshatra_span))  # 0 to 26
        nak_name = self.NAKSHATRAS[nak_idx % 27]

        # 3. Yoga: Sum of Sun and Moon longitudes divided by 13°20'
        yoga_sum = (s_deg + l_deg) % 360.0
        yoga_idx = int(math.floor(yoga_sum / nakshatra_span))  # 0 to 26
        yoga_name = self.YOGAS[yoga_idx % 27]

        # 4. Karana: Half of Tithi (6 degrees per Karana)
        karana_num = int(math.floor(diff / 6.0)) + 1
        karana_list = ["Bava", "Bālava", "Kaulava", "Taitila", "Gara", "Vaṇija", "Viṣṭi (Bhadra)"]
        if karana_num == 1:
            karana_name = "Kiṃstughna (Fixed)"
        elif karana_num >= 58:
            fixed_map = {58: "Śakuni (Fixed)", 59: "Catuṣpāda (Fixed)", 60: "Nāga (Fixed)"}
            karana_name = fixed_map.get(karana_num, "Nāga")
        else:
            k_mod = (karana_num - 2) % 7
            karana_name = f"{karana_list[k_mod]} (Movable)"

        # 5. Seasonal Determination from Sun Longitude
        season, regimen = self._determine_season_and_regimen(s_deg)

        return PancangaComputationResult(
            solar_longitude_deg=round(s_deg, 2),
            lunar_longitude_deg=round(l_deg, 2),
            tithi_number=tithi_idx,
            tithi_name=t_name,
            paksha=paksha,
            nakshatra_number=nak_idx + 1,
            nakshatra_name=nak_name,
            yoga_number=yoga_idx + 1,
            yoga_name=yoga_name,
            karana_name=karana_name,
            associated_season=season,
            seasonal_regimen=regimen
        )

    def _determine_season_and_regimen(self, solar_deg: float) -> tuple[RituSeason, str]:
        # Approximate tropical/sidereal solar arcs for 6 Ṛtus
        if 345 <= solar_deg or solar_deg < 45:
            return (
                RituSeason.VASANTA,
                "Vasanta Ṛtucaryā: Kapha liquefies due to sun's heat. Light diet, dry barley/wheat, ginger/honey; avoid heavy oily dairy and daytime sleep."
            )
        elif 45 <= solar_deg < 105:
            return (
                RituSeason.GRISMA,
                "Grīṣma Ṛtucaryā: Intense heat depletes bodily moisture. Sweet, cooling, hydrating foods (coconut water, sattu, ghee); avoid pungent, salty, acidic tastes."
            )
        elif 105 <= solar_deg < 165:
            return (
                RituSeason.VARSA,
                "Varṣā Ṛtucaryā: Dampness weakens digestive fire (Agni); Vāta aggravates. Warm, well-cooked, light foods, boiled water, sour/salty tastes in moderation; avoid raw leafy greens."
            )
        elif 165 <= solar_deg < 225:
            return (
                RituSeason.SARAD,
                "Śarad Ṛtucaryā: Pitta flares up as rain clouds clear under direct sun. Bitter, sweet, astringent foods (Tikta-Madhura), amla, ghee; cleansing therapy (Virecana) recommended."
            )
        elif 225 <= solar_deg < 285:
            return (
                RituSeason.HEMANTA,
                "Hemanta Ṛtucaryā: Strongest metabolic fire (Jāṭharāgni). Nourishing foods, whole grains, nuts, sesame oil massage (Abhyaṅga), warm baths."
            )
        else:
            return (
                RituSeason.SISIRA,
                "Śiśira Ṛtucaryā: Severe dry cold continues. Similar to Hemanta; sustain vitality with ginger, jaggery, warm soups; guard against cold wind exposure."
            )

    # 4. Harmonizer: Lokācāra-Śāstrācāra Samanvaya
    def reconcile_custom(self, custom_name: str, regional_practice: str, textual_ruling: Optional[str] = None) -> Dict[str, Any]:
        """
        Reconciles living folk customs (Lokācāra/Deśācāra) with classical texts
        using Mīmāṃsā jurisprudential principles.
        """
        return {
            "custom_name": custom_name,
            "regional_practice": regional_practice,
            "jurisprudential_hierarchy": "Śruti (Foundational) ≻ Smṛti (Codified) ≻ Sadācāra (Exemplary) ≻ Lokācāra/Deśācāra (Living)",
            "mimamsa_verdict": (
                "Per Manusmṛti 7.203 and Yājñavalkya Smṛti 1.343, regional customs (Deśācāra, Kulācāra, and Jātyācāra) "
                "are legally and spiritually authoritative within their respective regions provided they uphold universal "
                "dharma (Ahiṃsā, Satya, Asteya, Śauca) and psychological well-being. "
                "Living cultural practice is an organic adaptation of Sanātana Dharma to regional geography and history, "
                "not an illegitimate deviation."
            ),
            "status": "VALID_LOKACARA_SAMANVAYA"
        }

    def lookup_samskara(self, query: str) -> Optional[SamskaraRecord]:
        q = query.strip().lower()
        if not q:
            return None
        q_tokens = set(re.findall(r'\w+', q)) - {"tell", "me", "about", "the", "what", "is", "in", "of", "meaning", "samskara"}
        for k, v in self._samskaras.items():
            sam_tokens = set(re.findall(r'\w+', f"{k} {v.canonical_name} {v.transliteration}".lower()))
            if (q and (q in k or k in q)) or bool(q_tokens.intersection(sam_tokens)):
                return v
        return None

    def lookup_temple_ecosystem(self, query: str) -> Optional[TempleEcosystemRecord]:
        q = query.strip().lower()
        if not q:
            return None
        q_tokens = set(re.findall(r'\w+', q)) - {"tell", "me", "about", "the", "what", "is", "in", "of", "temple", "explain"}
        for k, v in self._temple_ecosystems.items():
            tem_tokens = set(re.findall(r'\w+', f"{k} {v.temple_id} {v.canonical_name}".lower()))
            if (q and (q in k or k in q)) or bool(q_tokens.intersection(tem_tokens)):
                return v
        return None
