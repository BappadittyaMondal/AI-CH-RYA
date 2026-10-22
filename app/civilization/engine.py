"""
AI ĀCHĀRYA — Bhāratīya Civilization Engine (app/civilization/engine.py)

Models the civilizational continuum of Bhāratavarṣa:
1. Kṣetra-Bhūmi (Sacred & Physical Geography, River Basins, Mahājanapadas, Maritime Thalassocracy)
2. Kāla-Gaṇanā (Epigraphy, Inscriptions, Numismatics & Archaeological Stratigraphy)
3. Rājadharma & Arthavyavasthā (Institutions, Śreṇī Guilds, Sabhā/Samiti, Indigenous Education)
4. Vijñāna & Dhātuvidyā (Material Sciences, Wootz Steel, Zinc Smelting, Hydraulic Engineering, Mathematics)
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
import re


class CivilizationalStrata(str, Enum):
    PRE_HARAPPAN = "Pre-Harappan (c. 7000–3300 BCE)"
    SARASVATI_SINDHU_MATURE = "Sarasvatī-Sindhu Mature Phase (c. 3300–1900 BCE)"
    VEDIC_SAMHITA = "Vedic Saṃhitā Strata"
    MAHAJANAPADA_ERA = "Ṣoḍaśa Mahājanapada Era (c. 600–321 BCE)"
    MAURYA_SUNGA = "Mauryan & Śuṅga Epoch (c. 321–185 BCE)"
    CLASSICAL_GUPTA = "Gupta-Vākāṭaka Classical Era (c. 320–550 CE)"
    MEDIEVAL_CHOLA_RASHTRAKUTA = "Chola, Rashtrakuta & Pratihāra Florescence (c. 600–1200 CE)"
    VIJAYANAGARA_MARATHA = "Vijayanagara, Maratha & Regional Resistance (c. 1336–1818 CE)"
    COLONIAL_RESISTANCE_MODERN = "Indigenous Preservation, Swadeshi & Modern Continuity (1820s–Present)"


@dataclass(frozen=True)
class KsetraEntity:
    entity_id: str
    name: str
    category: str  # "RIVER", "MAHAJANAPADA", "PORT_MARITIME", "PILGRIMAGE_TIRTHA"
    ancient_names: List[str]
    coordinates: Optional[tuple[float, float]]
    historical_strata: List[CivilizationalStrata]
    description: str
    archaeological_sites: List[str]
    textual_references: List[str]
    scientific_evidence: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EpigraphicRecord:
    record_id: str
    title: str
    ruler: str
    dynasty: str
    approx_date: str
    findspot: str
    script: str
    language: str
    key_historical_facts: List[str]
    epistemic_confidence: float = 0.95
    source_citation: str = ""


@dataclass(frozen=True)
class InstitutionRecord:
    institution_id: str
    name: str
    category: str  # "GUILD_SRENI", "POLITICAL_GOVERNANCE", "EDUCATION_GURUKULA", "JURISPRUDENCE"
    governing_principles: List[str]
    historical_examples: List[str]
    archival_evidence: str
    primary_texts: List[str]


@dataclass(frozen=True)
class MaterialScienceRecord:
    tech_id: str
    domain: str  # "METALLURGY", "HYDRAULIC_ENGINEERING", "MATHEMATICS_ASTRONOMY", "ARCHITECTURE_VASTU"
    innovation_name: str
    approximate_origin_era: str
    primary_sites: List[str]
    physical_evidence_summary: str
    global_significance: str
    primary_textual_sources: List[str]


class CivilizationalEngine:
    """
    Core engine managing the geographic, epigraphic, institutional,
    and material science continuum of Bhāratavarṣa.
    """

    def __init__(self):
        self._ksetras: Dict[str, KsetraEntity] = {}
        self._epigraphs: Dict[str, EpigraphicRecord] = {}
        self._institutions: Dict[str, InstitutionRecord] = {}
        self._material_sciences: Dict[str, MaterialScienceRecord] = {}
        self._load_seed_data()

    def _load_seed_data(self):
        # 1. Kṣetra Topography (Seed Data)
        self._ksetras["sarasvati_basin"] = KsetraEntity(
            entity_id="KSETRA-001",
            name="Sarasvatī River Basin",
            category="RIVER",
            ancient_names=["Sarasvatī", "Ambitame", "Nadītame", "Devītame"],
            coordinates=(29.5, 74.5),
            historical_strata=[CivilizationalStrata.VEDIC_SAMHITA, CivilizationalStrata.SARASVATI_SINDHU_MATURE],
            description="Perennial Himalayan glacier-fed river celebrated in Rigveda (10.75 Nadīstūti). Over 60% of Harappan/Sarasvati sites reside along its dry paleochannel (Ghaggar-Hakra).",
            archaeological_sites=["Kalibangan", "Rakhigarhi", "Banawali", "Kunal", "Bhirrana"],
            textual_references=["Rigveda 2.41.16", "Rigveda 7.95.2", "Rigveda 10.75.5", "Mahābhārata Śalyaparva"],
            scientific_evidence={
                "isro_paleochannel_radar": "Multi-spectral IRS satellite imaging mapped 4-8 km wide continuous channel from Shivalik foothills to Rann of Kutch.",
                "isotopic_dating": "Sedimentary zircon and strontium isotope studies corroborate perennial glacial origin prior to tectonic desiccation c. 2000 BCE."
            }
        )

        self._ksetras["kuru_panchala"] = KsetraEntity(
            entity_id="KSETRA-002",
            name="Kuru-Pañcāla Realm",
            category="MAHAJANAPADA",
            ancient_names=["Kurukṣetra", "Hastināpura", "Ahicchatra", "Kāmpilya"],
            coordinates=(29.96, 76.87),
            historical_strata=[CivilizationalStrata.VEDIC_SAMHITA, CivilizationalStrata.MAHAJANAPADA_ERA],
            description="Heartland of Vedic rituals, Itihāsa transmission, and Northern Black Polished / Painted Grey Ware material horizons.",
            archaeological_sites=["Hastinapur", "Kurukshetra", "Ahichchhatra", "Indraprastha (Purana Qila)"],
            textual_references=["Śatapatha Brāhmaṇa", "Mahābhārata", "Aṣṭādhyāyī 4.1.176"]
        )

        self._ksetras["lothal_maritime"] = KsetraEntity(
            entity_id="KSETRA-003",
            name="Lothal Maritime Hub & Dvīpāntara Arc",
            category="PORT_MARITIME",
            ancient_names=["Lothal", "Surparaka", "Bhrigukaccha"],
            coordinates=(22.52, 72.24),
            historical_strata=[CivilizationalStrata.SARASVATI_SINDHU_MATURE, CivilizationalStrata.MAHAJANAPADA_ERA],
            description="Tidal dockyard engineering with spillways, basin locks, and carnelian bead factories connecting Indus-Sarasvati trade to Mesopotamia and Persian Gulf.",
            archaeological_sites=["Lothal", "Bet Dwarka", "Dholavira"],
            textual_references=["Baudhāyana Dharmasūtra (Samudrasaṃyāna)", "Periplus of the Erythraean Sea"]
        )

        # 2. Epigraphic Records (Seed Data)
        self._epigraphs["aihole_pulakeshin"] = EpigraphicRecord(
            record_id="EPI-001",
            title="Aihole Meguti Temple Inscription of Pulakeśin II",
            ruler="Pulakeśin II",
            dynasty="Bādāmi Cālukya",
            approx_date="634 CE (Saka 556)",
            findspot="Aihole, Bagalkot district, Karnataka",
            script="Southern / Early Telugu-Kannada script",
            language="Classical Sanskrit (composed by Ravikīrti)",
            key_historical_facts=[
                "Explicitly synchronizes the elapsed time since the Bhārata War: 3,735 years elapsed by Śaka 556 (yielding 3102 BCE for the Bhārata War / Kaliyuga epoch).",
                "Records Pulakeśin II's defeat of Emperor Harṣavardhana on the banks of the Narmadā.",
                "Mentions celebrated poets Kālidāsa and Bhāravi, confirming their high antiquity prior to 634 CE."
            ],
            epistemic_confidence=0.98,
            source_citation="Epigraphia Indica, Vol. VI, pp. 1-12"
        )

        self._epigraphs["junagadh_rudradaman"] = EpigraphicRecord(
            record_id="EPI-002",
            title="Junāgaḍh Rock Inscription of Rudradāman I",
            ruler="Mahākṣatrapa Rudradāman I",
            dynasty="Western Kṣatrapas",
            approx_date="150 CE",
            findspot="Junagadh, Gujarat",
            script="Brāhmī",
            language="Chaste Classical Sanskrit (Earliest long Sanskrit public epigraph)",
            key_historical_facts=[
                "Documents the construction and repairs of the massive Sudarśana reservoir lake.",
                "Attributes original dam construction to Rāṣṭriya Puṣyagupta under Candragupta Maurya (c. 300 BCE).",
                "Attributes canal expansions to Yavanarāja Tuṣāspha under Emperor Aśoka Maurya (c. 250 BCE).",
                "Celebrates Rudradāman's adherence to royal restraint: rebuilding the dam with his own treasury without levying oppressive taxes (kara/viṣṭi) on the populace."
            ],
            epistemic_confidence=0.99,
            source_citation="Epigraphia Indica, Vol. VIII, pp. 36-49"
        )

        self._epigraphs["uttaramerur_chola"] = EpigraphicRecord(
            record_id="EPI-003",
            title="Uttaramerūr Temple Inscription of Parāntaka I",
            ruler="Parāntaka Chola I",
            dynasty="Imperial Chola",
            approx_date="920 CE",
            findspot="Vaikuntha Perumal Temple, Uttaramerur, Tamil Nadu",
            script="Tamil & Grantha",
            language="Tamil and Sanskrit",
            key_historical_facts=[
                "Codifies village democratic self-governance via the Kudavolai (pot ballot) electoral system.",
                "Establishes strict eligibility qualifications for committee members: ownership of tax-paying land, Vedic knowledge, ethical integrity, and clean financial records.",
                "Enforces disqualification for corruption, embezzlement of village funds, or nepotism (covering 5 degrees of kinship)."
            ],
            epistemic_confidence=0.99,
            source_citation="Archaeological Survey of India (ASI) Memoir No. 34"
        )

        self._epigraphs["baroda_copper_karka"] = EpigraphicRecord(
            record_id="EPI-004",
            title="Baroda Copper Plate Inscription of Karka II (Kailasa Cave 16 Record)",
            ruler="Karka II (commemorating King Kṛṣṇa I)",
            dynasty="Rāṣṭrakūṭa",
            approx_date="812 CE (Saka 734)",
            findspot="Baroda (Vadodara), Gujarat",
            script="Early Devanāgarī / Western Indian script",
            language="Classical Sanskrit",
            key_historical_facts=[
                "Explicitly documents the construction of the Kailasa Monolithic Temple (Cave 16) at Elāpura (Ellora) by Rāṣṭrakūṭa King Kṛṣṇa I (reigned c. 756–774 CE).",
                "Records the astonishment of the master architect (Sthapati) upon seeing the completed rock-cut masterpiece: 'katham aho mayedaṁ kṛtam' ('How wonderful! How could I have fashioned this without divine grace?').",
                "Falsifies all modern claims that Kailasa temple has no historical human record or was built by aliens with lasers."
            ],
            epistemic_confidence=0.99,
            source_citation="Indian Antiquary, Vol. XII, pp. 156-165; Epigraphia Indica"
        )

        self._epigraphs["thanjavur_brihadisvara"] = EpigraphicRecord(
            record_id="EPI-005",
            title="Brihadīśvara Temple Epigraphic Inscriptions of Rājarāja Chola I",
            ruler="Rājarāja Chola I",
            dynasty="Imperial Chola",
            approx_date="1010 CE (25th regnal year)",
            findspot="Brihadisvara Temple sanctum plinth walls, Thanjavur, Tamil Nadu",
            script="Tamil and Grantha",
            language="Tamil and Sanskrit",
            key_historical_facts=[
                "Records the exact engineering and financial inventory of the temple, including donations of gold, jewels, silver vessels, and bronze murti weights.",
                "Explicitly names the chief royal architect (Karu-Taccan): Kunjaramallan Rajaraja Peruntaccan, honoring the human Sthapati lineage.",
                "Details the consecration of the copper stūpī (Kumbham) atop the 216-foot vimāna, documenting the human transport of the 80-ton granite dome via an inclined earthen ramp (Sarukkam)."
            ],
            epistemic_confidence=0.99,
            source_citation="South Indian Inscriptions (SII), Vol. II, Archaeological Survey of India"
        )

        self._epigraphs["konark_sun_temple"] = EpigraphicRecord(
            record_id="EPI-006",
            title="Konark Sun Temple Palm-Leaf Chronicles (Bāya Cakaḍā & Madala Panji)",
            ruler="Narasimhadeva I",
            dynasty="Eastern Gaṅga",
            approx_date="c. 1245–1256 CE",
            findspot="Konark, Puri district, Odisha",
            script="Odia & Proto-Bengali-Odia script",
            language="Classical Sanskrit and Old Odia",
            key_historical_facts=[
                "Preserves daily administrative logs (Bāya Cakaḍā) of stone transport, barge logistics on the Candrabhāgā river, and worker food rations over 12 years.",
                "Names the chief master architect: Bisu Moharana (Biśvānanda Moharāna) and a guild of 1,200 master craftsmen.",
                "Details the placement of the structural magnetic iron beams (Loha-kīlaka) balancing the upper corbelled masonry tiers against coastal seismic forces."
            ],
            epistemic_confidence=0.96,
            source_citation="Alice Boner, S.R. Sarma, R.P. Das: 'New Light on the Sun Temple of Konarka' (Varanasi, 1972)"
        )

        # 3. Institutions & Governance (Seed Data)
        self._institutions["sreni_guilds"] = InstitutionRecord(
            institution_id="INST-001",
            name="Śreṇī & Nigama (Artisan & Merchant Guilds)",
            category="GUILD_SRENI",
            governing_principles=[
                "Autonomy of Śreṇī-dharma (guild law recognized and enforced by the royal court per Yājñavalkya 2.192).",
                "Functioned as autonomous banks accepting perpetual endowments (Akṣayanīvī) and paying interest for public welfare and temple charities.",
                "Maintained strict quality apprenticeships, occupational ethics, and mutual welfare safety nets for artisan families."
            ],
            historical_examples=[
                "Silk weavers' guild (Paṭṭavāya Śreṇī) of Mandasor (Dashapura Inscription, 473 CE) constructing a magnificent Sun Temple.",
                "Ayyavole 500 (Five Hundred Lords of Aivalli) maritime merchant guild operating trans-continental trade across South and Southeast Asia."
            ],
            archival_evidence="Corroborated by over 120 inscriptions across Junnar, Nasik, Mandasor, and Nagarjunakonda.",
            primary_texts=["Arthaśāstra 2.4", "Yājñavalkya Smṛti 2.187-192", "Nārada Smṛti 10.1-7"]
        )

        self._institutions["dharampal_education"] = InstitutionRecord(
            institution_id="INST-002",
            name="Indigenous Universal Education Ecosystem (The Beautiful Tree)",
            category="EDUCATION_GURUKULA",
            governing_principles=[
                "Decentralized community-funded elementary schooling (Pāṭhaśālā / Tinnai) operating in nearly every village.",
                "Broad cross-caste enrollment: 1820s British colonial surveys document that the majority of scholars in Tamil, Telugu, and Bengali village schools were from non-Brahmin and lower-varna backgrounds.",
                "Curriculum emphasized mental mathematics, accounting, ethical storytelling, and local languages."
            ],
            historical_examples=[
                "Sir Thomas Munro's 1822–1826 survey of the Madras Presidency.",
                "William Adam's 1835–1838 reports on vernacular education in Bengal and Bihar.",
                "Dr. G.W. Leitner's 1882 survey of indigenous education in the Punjab."
            ],
            archival_evidence="Dharampal's archival compilation: 'The Beautiful Tree: Indigenous Indian Education in the Eighteenth Century' (Biblia Impex, 1983).",
            primary_texts=["Board of Revenue Records, Madras Presidency (1822-1826)", "William Adam's Reports (1835)"]
        )

        # 4. Indigenous Material Science (Seed Data)
        self._material_sciences["wootz_steel"] = MaterialScienceRecord(
            tech_id="MAT-001",
            domain="METALLURGY",
            innovation_name="Wootz Crucible Steel (Ukku / Hinduwani)",
            approximate_origin_era="c. 6th–3rd Century BCE to 18th Century CE",
            primary_sites=["Kodumanal (Tamil Nadu)", "Telangana / Golconda regions", "Mel-siruvalur"],
            physical_evidence_summary="Crucible process melting high-carbon wrought iron with organic carbon sources, producing ultra-high carbon steel (1.2–1.8% C) with carbon nanotube and cementite carbide band structures.",
            global_significance="Exported to Damascus to forge the legendary Damascus swords; praised by Alexander's historians and Arab polymath Al-Kindi.",
            primary_textual_sources=["Rasaratnasamuccaya", "Periplus of the Erythraean Sea", "Al-Kindi's On Swords"]
        )

        self._material_sciences["zawar_zinc"] = MaterialScienceRecord(
            tech_id="MAT-002",
            domain="METALLURGY",
            innovation_name="Zawar Zinc Smelting Retorts (High-Temp Distillation)",
            approximate_origin_era="c. 4th Century BCE (early traces); 12th–16th Century CE (industrial scale)",
            primary_sites=["Zawar, Udaipur district, Rajasthan"],
            physical_evidence_summary="Downward condensation distillation retorts operating at >1000°C. Pure zinc vaporizes at 907°C and oxidizes easily in air; Indian metallurgists condensed it into sealed collection vessels below the furnace.",
            global_significance="First industrial production of metallic zinc in human history, 300 years before William Champion patented it in Bristol (1738) after studying Indian retorts.",
            primary_textual_sources=["Rasārṇava (c. 12th century)", "Rasaratnasamuccaya 5.149-169"]
        )

        self._material_sciences["kallanai_grand_anicut"] = MaterialScienceRecord(
            tech_id="MAT-003",
            domain="HYDRAULIC_ENGINEERING",
            innovation_name="Kallanai (Grand Anicut) on the Kāverī",
            approximate_origin_era="c. 2nd Century CE",
            primary_sites=["Thanjavur district, Tamil Nadu"],
            physical_evidence_summary="Unhewn stone barrage (329 meters long, 20 meters wide) engineered across the sandy, shifting riverbed of the Kaveri to divert surplus floodwaters into the Kollidam (Coleroon) canal system.",
            global_significance="One of the world's oldest functional water-diversion dams in continuous use for almost two millennia, creating the fertile rice bowl of South India.",
            primary_textual_sources=["Pattinappalai", "Silappadikaram", "Chola Inscriptions"]
        )

        self._material_sciences["kerala_mathematics"] = MaterialScienceRecord(
            tech_id="MAT-004",
            domain="MATHEMATICS_ASTRONOMY",
            innovation_name="Infinite Series Calculus (Mādhava-Leibniz & Gregory Series)",
            approximate_origin_era="c. 14th–16th Century CE",
            primary_sites=["Sangamagrama (Irinjalakuda, Kerala)"],
            physical_evidence_summary="Discovered infinite series expansions for pi, sine, cosine, and arctangent 250 years before Isaac Newton and Gottfried Wilhelm Leibniz.",
            global_significance="Anticipated modern mathematical analysis, differential corrections, and power series approximations without the infinitesimal limit paradox.",
            primary_textual_sources=["Yuktibhāṣā of Jyeṣṭhadeva (1530 CE)", "Tantrasaṅgraha of Nīlakaṇṭha Somayājī", "Karaṇapaddhati"]
        )

        self._material_sciences["kailasa_rock_cut"] = MaterialScienceRecord(
            tech_id="MAT-005",
            domain="ARCHITECTURE_VASTU",
            innovation_name="Monolithic Top-Down Basalt Quarrying & Excavation (Kailasa Cave 16)",
            approximate_origin_era="c. 756–774 CE (Rāṣṭrakūṭa King Kṛṣṇa I)",
            primary_sites=["Ellora (Verul), Chhatrapati Sambhajinagar district, Maharashtra"],
            physical_evidence_summary="Vertical top-down cliff trenching removing ~85,000 m³ (~240,000 metric tons) of Deccan basalt without scaffolding. Leveraged natural columnar basalt jointing with water-soaked expanding wooden wedges exerting >40 MPa tensile cleavage stress alongside Wootz steel chisels.",
            global_significance="The largest monolithic rock-cut excavated monument on Earth, demonstrating supreme stereotomy, geometry, and stone carving coordination.",
            primary_textual_sources=["Baroda Copper Plate (812 CE)", "Mānasāra", "Mayamata", "Samarāṅgaṇa Sūtradhāra"]
        )

        self._material_sciences["brihadisvara_interlocking_granite"] = MaterialScienceRecord(
            tech_id="MAT-006",
            domain="ARCHITECTURE_VASTU",
            innovation_name="Interlocking Dry-Ashlar Granite Structural Mechanics (Brihadīśvara Vimāna)",
            approximate_origin_era="c. 1003–1010 CE (Rājarāja Chola I)",
            primary_sites=["Thanjavur, Tamil Nadu"],
            physical_evidence_summary="216-foot hollow pyramidal vimāna constructed entirely of interlocking dry-ashlar crystalline granite blocks without binding mortar. Crowned with an 80-metric-ton granite monolith capstone raised via a 4-mile inclined earthen ramp (Sarukkam) with lubricated timber rollers.",
            global_significance="Pioneered gravity-stabilized seismic damping in tall stone structures, enduring regional earthquakes and delta soil settlement for over 1,000 years.",
            primary_textual_sources=["Mayamata Vāstuśāstra", "Kāśyapa Śilpa", "Thanjavur Temple Epigraphs"]
        )

        self._material_sciences["nilachakra_lightning_grounding"] = MaterialScienceRecord(
            tech_id="MAT-007",
            domain="ARCHITECTURE_VASTU",
            innovation_name="Aṣṭadhātu Corrosion-Passivation & Atmospheric Lightning Dissipation (Puri Nīlacakra)",
            approximate_origin_era="c. 12th Century CE (Anantavarman Coḍagaṅga)",
            primary_sites=["Puri, Odisha"],
            physical_evidence_summary="2.2-ton finial forged from Aṣṭadhātu (8-metal alloy) atop the 214-foot sikhara. Acts as a passive Faraday lightning arrestor with low electrical impedance, dissipating Bay of Bengal cyclonic lightning strikes safely into deep ground aquifers while forming a rust-resistant misawite phosphate film.",
            global_significance="Sophisticated synthesis of sacred metallurgy, atmospheric physics, and structural protection centuries before Benjamin Franklin's 1752 lightning rod.",
            primary_textual_sources=["Mādala Pāñji", "Rasaratnasamuccaya", "Pāñcarātra Saṃhitās"]
        )

        self._material_sciences["konark_magnetic_beams"] = MaterialScienceRecord(
            tech_id="MAT-008",
            domain="ARCHITECTURE_VASTU",
            innovation_name="High-Phosphorus Wrought Iron Clamps & Coastal Foundation Mechanics (Konark)",
            approximate_origin_era="c. 1245–1256 CE (Narasimhadeva I)",
            primary_sites=["Konark, Puri district, Odisha"],
            physical_evidence_summary="Massive forged wrought-iron beams (up to 10 meters long and 9 metric tons) with high phosphorus (0.1–0.25%) and low sulfur content. Placed as structural tie-bars across stone lintels to withstand lateral coastal wind sheer and sand foundation shifting.",
            global_significance="Pre-industrial heavy metallurgical forging matching 19th-century European steam hammer capacities; demonstrates advanced passive atmospheric corrosion resistance.",
            primary_textual_sources=["Bāya Cakaḍā (Palm-Leaf Account Books)", "Alice Boner Konark Manuscripts"]
        )

    # Retrieval and Query Methods
    def lookup_ksetra(self, query: str) -> Optional[KsetraEntity]:
        q = query.strip().lower()
        if not q:
            return None
        q_tokens = set(re.findall(r'\w+', q)) - {"tell", "me", "about", "the", "what", "is", "in", "of", "river", "explain"}
        best_match = None
        best_score = 0
        for k, v in self._ksetras.items():
            if q and (q in k or k in q):
                return v
            name_tokens = set(re.findall(r'\w+', f"{k} {v.name} {' '.join(v.ancient_names)}".lower()))
            common = q_tokens.intersection(name_tokens)
            if len(common) > best_score:
                best_score = len(common)
                best_match = v
        return best_match

    def lookup_epigraph(self, query: str) -> Optional[EpigraphicRecord]:
        q = query.strip().lower()
        if not q:
            return None
        q_tokens = set(re.findall(r'\w+', q)) - {"tell", "me", "about", "the", "what", "is", "in", "of", "inscription", "temple", "plate", "explain"}
        best_match = None
        best_score = 0
        for k, v in self._epigraphs.items():
            if q and (q in k or k in q):
                return v
            epi_tokens = set(re.findall(r'\w+', f"{k} {v.record_id} {v.title} {v.ruler}".lower()))
            common = q_tokens.intersection(epi_tokens)
            if len(common) > best_score:
                best_score = len(common)
                best_match = v
        return best_match

    def lookup_institution(self, query: str) -> Optional[InstitutionRecord]:
        q = query.strip().lower()
        if not q:
            return None
        q_tokens = set(re.findall(r'\w+', q)) - {"tell", "me", "about", "the", "what", "is", "in", "of", "explain"}
        best_match = None
        best_score = 0
        for k, v in self._institutions.items():
            if q and (q in k or k in q):
                return v
            inst_tokens = set(re.findall(r'\w+', f"{k} {v.institution_id} {v.name}".lower()))
            common = q_tokens.intersection(inst_tokens)
            if len(common) > best_score:
                best_score = len(common)
                best_match = v
        return best_match

    def lookup_material_science(self, query: str) -> Optional[MaterialScienceRecord]:
        q = query.strip().lower()
        if not q:
            return None
        q_tokens = set(re.findall(r'\w+', q)) - {"tell", "me", "about", "the", "what", "is", "in", "of", "explain"}
        best_match = None
        best_score = 0
        for k, v in self._material_sciences.items():
            if q and (q in k or k in q):
                return v
            mat_tokens = set(re.findall(r'\w+', f"{k} {v.tech_id} {v.innovation_name} {v.domain}".lower()))
            common = q_tokens.intersection(mat_tokens)
            if len(common) > best_score:
                best_score = len(common)
                best_match = v
        return best_match

    def list_all_entities_summary(self) -> Dict[str, Any]:
        return {
            "total_ksetras": len(self._ksetras),
            "total_epigraphs": len(self._epigraphs),
            "total_institutions": len(self._institutions),
            "total_material_science": len(self._material_sciences),
            "ksetras": [v.name for v in self._ksetras.values()],
            "epigraphs": [f"{v.record_id}: {v.title} ({v.approx_date})" for v in self._epigraphs.values()],
            "institutions": [v.name for v in self._institutions.values()],
            "material_science": [v.innovation_name for v in self._material_sciences.values()]
        }
