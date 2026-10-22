"""
AI ĀCHĀRYA — Vivāda-Nirṇaya Engine (app/verification/vivada_nirnaya.py)

Production-Grade Epistemic Arbitration Engine:
Resolves diametrically opposed historical, chronological, and scientific claims:
1. 5-Dimensional Orthogonal Evidentiary Matrix (Astronomy, Archaeology, Epigraphy, Linguistics, Hermeneutics).
2. Continuous Gaussian Temporal Proximity Kernel (eliminating step-function cliff).
3. Physics-based Delta-T Ephemeris Uncertainty Penalty for pre-3100 BCE astronomical claims.
4. Textual Redaction Strata-Aware separation (Jaya 8,800 vs Bhārata 24,000 vs Mahābhārata 100,000).
5. Dirichlet / Softmax Normalized Bayesian Posterior Probabilities with transparent bottleneck disclosure.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
import math


class TextualStrataLevel(str, Enum):
    JAYA_CORE = "Jaya Core Event Layer (~8,800 verses, primary historical conflict)"
    BHARATA_EXPANSION = "Bhārata Expansion Layer (~24,000 verses, ethical & political dialogues)"
    MAHABHARATA_ENCYCLOPEDIC = "Mahābhārata Final Redaction Layer (~100,000 verses, encyclopedic compilation)"


@dataclass
class ArchaeologicalStratumMatch:
    site_name: str
    stratum_name: str
    median_calibrated_bce: float
    uncertainty_years: float = 200.0
    material_match_quality: float = 0.85  # 0.0 to 1.0


@dataclass
class ChronologicalHypothesis:
    name: str
    proponent_or_school: str
    proposed_date_bce: float
    target_strata_level: TextualStrataLevel
    astronomy_raw_score: float        # 0.0 to 1.0
    archaeology_raw_score: float      # 0.0 to 1.0
    epigraphy_raw_score: float        # 0.0 to 1.0
    linguistics_raw_score: float      # 0.0 to 1.0
    hermeneutics_raw_score: float    # 0.0 to 1.0
    cherry_pick_penalty: float = 0.0  # 0.0 to 1.0
    verified_strata: List[ArchaeologicalStratumMatch] = field(default_factory=list)
    summary_claim: str = ""


@dataclass(frozen=True)
class ArbitrationResult:
    hypothesis_name: str
    proponent_or_school: str
    proposed_date_bce: float
    target_strata_level: str
    posterior_probability: float
    epistemic_status: str
    strongest_pillar: str
    fatal_bottleneck: str
    anchor_decay_multiplier: float
    delta_t_astro_multiplier: float
    stratified_reality_assessment: str


class VivadaNirnayaEngine:
    """
    Arbitrates multi-hypothesis conflicts using continuous kernels,
    orthogonal evidentiary dimensions, and Bayesian likelihoods.
    """

    # Orthogonal dimension weights
    WEIGHTS = {
        "astronomy": 0.25,
        "archaeology": 0.30,
        "epigraphy": 0.20,
        "linguistics": 0.15,
        "hermeneutics": 0.10
    }

    def __init__(self, sigma_strata: float = 600.0, temperature_beta: float = 3.5):
        self.sigma_strata = sigma_strata
        self.temperature_beta = temperature_beta

    def compute_continuous_anchor_kernel(
        self,
        hypothesis_date_bce: float,
        strata_matches: List[ArchaeologicalStratumMatch]
    ) -> Tuple[float, Optional[str]]:
        """
        Computes the continuous Gaussian temporal proximity kernel:
        Omega_Anchor = max_s [ exp( - (T_H - T_s)^2 / (2 * sigma^2) ) * Q(s) ]
        Eliminates the discontinuous step-function cliff.
        """
        if not strata_matches:
            # Baseline background prior for unexcavated / alluvial Ganga conditions
            return 0.15, "No directly matching excavated strata provided (baseline alluvial prior: 0.15)"

        best_kernel = 0.15
        best_stratum_desc = None

        for match in strata_matches:
            delta = abs(hypothesis_date_bce - match.median_calibrated_bce)
            kernel_val = math.exp(-(delta ** 2) / (2.0 * (self.sigma_strata ** 2))) * match.material_match_quality
            if kernel_val > best_kernel:
                best_kernel = kernel_val
                best_stratum_desc = f"{match.site_name} ({match.stratum_name} at ~{int(match.median_calibrated_bce)} BCE, delta={int(delta)} yrs, match={match.material_match_quality})"

        return max(0.15, min(1.0, best_kernel)), best_stratum_desc

    def compute_delta_t_ephemeris_multiplier(self, date_bce: float) -> Tuple[float, str]:
        """
        Calculates ephemeris uncertainty penalty for high antiquity dates.
        Earth's tidal deceleration (Delta-T) uncertainty grows quadratically before 3100 BCE.
        """
        if date_bce <= 3100.0:
            return 1.0, "Ephemeris within calibrated historical Delta-T envelope (<= 3100 BCE)"

        excess_millennia = (date_bce - 3100.0) / 1000.0
        # Quadratic decay: e.g. at 5561 BCE, excess = 2.461 -> 1 / (1 + 0.15 * 6.05) ≈ 0.52
        penalty = 1.0 / (1.0 + 0.15 * (excess_millennia ** 2))
        penalty = max(0.20, min(1.0, penalty))
        return penalty, f"Pre-3100 BCE Delta-T tidal drift penalty ({round(penalty, 3)} for {int(date_bce)} BCE)"

    def arbitrate(self, hypotheses: List[ChronologicalHypothesis]) -> List[ArbitrationResult]:
        """
        Executes multi-hypothesis arbitration across all input hypotheses,
        yielding normalized Bayesian posterior probabilities and diagnostic bottlenecks.
        """
        if not hypotheses:
            return []

        composite_scores: List[float] = []
        diagnostics: List[Dict[str, Any]] = []

        for h in hypotheses:
            # 1. Continuous Anchor
            anchor_mult, anchor_desc = self.compute_continuous_anchor_kernel(
                h.proposed_date_bce,
                h.verified_strata
            )

            # 2. Delta-T Astro Penalty
            delta_t_mult, delta_t_desc = self.compute_delta_t_ephemeris_multiplier(h.proposed_date_bce)

            # 3. Weighted Evidence Dot Product
            raw_evidence = (
                self.WEIGHTS["astronomy"] * (h.astronomy_raw_score * delta_t_mult) +
                self.WEIGHTS["archaeology"] * h.archaeology_raw_score +
                self.WEIGHTS["epigraphy"] * h.epigraphy_raw_score +
                self.WEIGHTS["linguistics"] * h.linguistics_raw_score +
                self.WEIGHTS["hermeneutics"] * h.hermeneutics_raw_score
            )

            # 4. Composite Score with Anchor and Cherry-Pick Penalty
            hermeneutic_fidelity = max(0.0, 1.0 - h.cherry_pick_penalty)
            composite = raw_evidence * anchor_mult * hermeneutic_fidelity
            composite_scores.append(composite)

            # 5. Identify Strongest Pillar and Fatal Bottleneck
            pillar_scores = {
                "Astronomical Modeling": h.astronomy_raw_score * delta_t_mult,
                "Archaeological Stratigraphy": h.archaeology_raw_score,
                "Epigraphic Attestation": h.epigraphy_raw_score,
                "Linguistic Chronology": h.linguistics_raw_score,
                "Hermeneutic Comprehensiveness": h.hermeneutics_raw_score
            }
            strongest = max(pillar_scores, key=pillar_scores.get)

            bottleneck = self._identify_fatal_bottleneck(
                h, anchor_mult, delta_t_mult, pillar_scores
            )

            stratified_assessment = self._generate_stratified_reality(h, anchor_mult)

            diagnostics.append({
                "hypothesis": h,
                "composite": composite,
                "anchor_mult": anchor_mult,
                "delta_t_mult": delta_t_mult,
                "strongest": strongest,
                "bottleneck": bottleneck,
                "stratified_assessment": stratified_assessment
            })

        # 6. Softmax Normalization for True Bayesian Posterior
        exp_vals = [math.exp(self.temperature_beta * s) for s in composite_scores]
        total_exp = sum(exp_vals)
        posteriors = [e / total_exp if total_exp > 0 else 1.0 / len(hypotheses) for e in exp_vals]

        results: List[ArbitrationResult] = []
        for i, diag in enumerate(diagnostics):
            p = posteriors[i]
            h = diag["hypothesis"]
            status = self._classify_posterior_status(p)

            results.append(
                ArbitrationResult(
                    hypothesis_name=h.name,
                    proponent_or_school=h.proponent_or_school,
                    proposed_date_bce=h.proposed_date_bce,
                    target_strata_level=h.target_strata_level.value,
                    posterior_probability=round(p, 4),
                    epistemic_status=status,
                    strongest_pillar=diag["strongest"],
                    fatal_bottleneck=diag["bottleneck"],
                    anchor_decay_multiplier=round(diag["anchor_mult"], 4),
                    delta_t_astro_multiplier=round(diag["delta_t_mult"], 4),
                    stratified_reality_assessment=diag["stratified_assessment"]
                )
            )

        # Sort descending by posterior probability
        results.sort(key=lambda r: r.posterior_probability, reverse=True)
        return results

    def _classify_posterior_status(self, p: float) -> str:
        if p >= 0.50:
            return "PROBABLE_PRIMARY_CORRIDOR (Highest Evidence-Weighted Triangulation)"
        elif p >= 0.20:
            return "VIABLE_SECONDARY_CORRIDOR (Substantial Merit with Specific Gaps)"
        else:
            return "MARGINAL_OR_UNANCHORED_HYPOTHESIS (High Theoretical or Material Disconnect)"

    def _identify_fatal_bottleneck(
        self,
        h: ChronologicalHypothesis,
        anchor_mult: float,
        delta_t_mult: float,
        pillar_scores: Dict[str, float]
    ) -> str:
        if anchor_mult < 0.25:
            return f"Archaeological Void: Zero matching urban/metallurgical strata found within a 1,000-year window of {int(h.proposed_date_bce)} BCE."
        if delta_t_mult < 0.60:
            return f"Delta-T Precession Drift: Celestial simulations at {int(h.proposed_date_bce)} BCE suffer from non-linear Earth tidal deceleration uncertainty."
        if h.cherry_pick_penalty >= 0.40:
            return "Hermeneutic Selectivity: Excludes substantial contradictory verses and cultural descriptions from the same text."
        if pillar_scores["Linguistic Chronology"] < 0.30:
            return "Linguistic Improbability: Extant Sanskrit morphology cannot be sustained across this chronological gap without phonetic evolution."
        if pillar_scores["Epigraphic Attestation"] < 0.25:
            return "Epigraphic Absence: No ancient royal inscriptions, copper plates, or external synchronisms acknowledge this epoch."
        return "Minor evidentiary variations across secondary parameters."

    def _generate_stratified_reality(self, h: ChronologicalHypothesis, anchor_mult: float) -> str:
        if h.proposed_date_bce > 4000.0:
            return (
                f"Represents an ancient astronomical memory or inherited celestial benchmark, "
                f"but cannot describe the physical socio-material conflict of the extant Epic due to an archaeological anchor score of {round(anchor_mult, 3)}."
            )
        elif 2500.0 <= h.proposed_date_bce <= 3200.0:
            return (
                "Accurately maps to the traditional Jaya core war horizon (c. 3102 BCE Kali Yuga epoch), "
                "strongly supported by ancient epigraphy (Aihole Inscription 634 CE) and contiguous civilizational memory."
            )
        else:
            return (
                "Accurately maps to the physical Painted Grey Ware (PGW) material culture and final encyclopedic redaction "
                "of the Mahābhārata (c. 1000–800 BCE) following the Hastinapur flood described in the Purāṇas."
            )

    @staticmethod
    def get_default_mahabharata_benchmarks() -> List[ChronologicalHypothesis]:
        """Returns standard 3-tier benchmark hypotheses for the Mahābhārata War."""
        return [
            ChronologicalHypothesis(
                name="3102 BCE Kali Yuga Epoch",
                proponent_or_school="Aryabhata (499 CE) / Pulakeshin II Aihole (634 CE) / Surya Siddhanta",
                proposed_date_bce=3102.0,
                target_strata_level=TextualStrataLevel.JAYA_CORE,
                astronomy_raw_score=0.75,
                archaeology_raw_score=0.45,
                epigraphy_raw_score=0.95,
                linguistics_raw_score=0.55,
                hermeneutics_raw_score=0.90,
                cherry_pick_penalty=0.10,
                verified_strata=[
                    ArchaeologicalStratumMatch("Aihole Meguti Inscription (634 CE)", "Epigraphic Lithic Anchor", 3102.0, 50.0, 0.95),
                    ArchaeologicalStratumMatch("Sarasvati River Desiccation", "Hydrological Strata Kalibangan", 3000.0, 300.0, 0.70),
                    ArchaeologicalStratumMatch("Submerged Dvaraka Marine Layer", "Late Harappan Underwater Walls", 1520.0, 500.0, 0.65)
                ],
                summary_claim="Anchored in primary royal epigraphy, astronomical Mean Yuga conjunctions, and Sarasvati paleochannel desiccation."
            ),
            ChronologicalHypothesis(
                name="c. 950 BCE PGW Stratigraphic Horizon",
                proponent_or_school="Prof. B.B. Lal / Archaeological Survey of India",
                proposed_date_bce=950.0,
                target_strata_level=TextualStrataLevel.MAHABHARATA_ENCYCLOPEDIC,
                astronomy_raw_score=0.25,
                archaeology_raw_score=0.90,
                epigraphy_raw_score=0.30,
                linguistics_raw_score=0.85,
                hermeneutics_raw_score=0.50,
                cherry_pick_penalty=0.20,
                verified_strata=[
                    ArchaeologicalStratumMatch("Hastinapur Period II Flood", "PGW Stratum", 900.0, 100.0, 0.90),
                    ArchaeologicalStratumMatch("Kurukshetra / Bhagwanpura", "Late Harappan-PGW Overlap", 1000.0, 150.0, 0.85)
                ],
                summary_claim="Anchored in Hastinapur Ganga flood horizon matching King Nicaksu's capital relocation to Kausambi."
            ),
            ChronologicalHypothesis(
                name="5561 BCE High Antiquity Model",
                proponent_or_school="Nilesh Nilkanth Oak (Arundhati-Vasistha / Ephemeris Retrodiction)",
                proposed_date_bce=5561.0,
                target_strata_level=TextualStrataLevel.JAYA_CORE,
                astronomy_raw_score=0.92,
                archaeology_raw_score=0.10,
                epigraphy_raw_score=0.15,
                linguistics_raw_score=0.15,
                hermeneutics_raw_score=0.60,
                cherry_pick_penalty=0.45,
                verified_strata=[],
                summary_claim="Derived from Arundhati walking ahead of Vasistha observation in Bhisma Parva, but lacks urban/metallurgical strata."
            )
        ]

    @staticmethod
    def get_default_ramayana_benchmarks() -> List[ChronologicalHypothesis]:
        """Returns standard 3-tier benchmark hypotheses for the Rāmāyaṇa."""
        return [
            ChronologicalHypothesis(
                name="c. 1500–1200 BCE Bronze/Iron Transition Model",
                proponent_or_school="Archaeological Survey of India / H.D. Sankalia / Material Stratigraphy",
                proposed_date_bce=1400.0,
                target_strata_level=TextualStrataLevel.MAHABHARATA_ENCYCLOPEDIC,
                astronomy_raw_score=0.35,
                archaeology_raw_score=0.80,
                epigraphy_raw_score=0.40,
                linguistics_raw_score=0.75,
                hermeneutics_raw_score=0.60,
                cherry_pick_penalty=0.15,
                verified_strata=[
                    ArchaeologicalStratumMatch("Ayodhya Trench Excavations", "Pre-NBPW Stratum", 1400.0, 200.0, 0.75),
                    ArchaeologicalStratumMatch("Adam's Bridge / Rama Setu Carbonates", "Submerged Shoal Strata", 1500.0, 500.0, 0.65)
                ],
                summary_claim="Matches Ayodhya pre-NBPW occupation, early chariot warfare, copper weaponry, and peninsular-Lankan sea passage."
            ),
            ChronologicalHypothesis(
                name="5075 BCE Planetary Horoscope Model",
                proponent_or_school="Dr. Pushkar Bhatnagar (Planetarium Gold Planetary Configuration)",
                proposed_date_bce=5075.0,
                target_strata_level=TextualStrataLevel.JAYA_CORE,
                astronomy_raw_score=0.82,
                archaeology_raw_score=0.25,
                epigraphy_raw_score=0.20,
                linguistics_raw_score=0.30,
                hermeneutics_raw_score=0.70,
                cherry_pick_penalty=0.30,
                verified_strata=[
                    ArchaeologicalStratumMatch("Mehrgarh Early Pastoral Horizon", "Pre-Harappan Stratum", 5000.0, 500.0, 0.40)
                ],
                summary_claim="Derived from Valmiki Bala Kanda 1.18.8-10 horoscope with 5 exalted planets, but Ayodhya lacks 5000 BCE urban strata."
            ),
            ChronologicalHypothesis(
                name="12209 BCE Ephemeris Model",
                proponent_or_school="Nilesh Nilkanth Oak (Pole Star & Equinox Retrodiction)",
                proposed_date_bce=12209.0,
                target_strata_level=TextualStrataLevel.JAYA_CORE,
                astronomy_raw_score=0.88,
                archaeology_raw_score=0.05,
                epigraphy_raw_score=0.05,
                linguistics_raw_score=0.10,
                hermeneutics_raw_score=0.50,
                cherry_pick_penalty=0.50,
                verified_strata=[],
                summary_claim="Derived from pole star and seasonal equinox retrodictions, but falls into the Late Glacial Maximum Paleolithic hunter-gatherer era."
            )
        ]

    @staticmethod
    def get_default_rigveda_benchmarks() -> List[ChronologicalHypothesis]:
        """Returns standard 3-tier benchmark hypotheses for the Ṛgveda."""
        return [
            ChronologicalHypothesis(
                name="c. 3000–1900 BCE Sarasvatī Hydrological & Mature Harappan Floruit",
                proponent_or_school="Prof. K.S. Valdiya / Dr. B.B. Lal / Michel Danino / Sarasvatī Paleohydrology",
                proposed_date_bce=2600.0,
                target_strata_level=TextualStrataLevel.JAYA_CORE,
                astronomy_raw_score=0.85,
                archaeology_raw_score=0.85,
                epigraphy_raw_score=0.45,
                linguistics_raw_score=0.80,
                hermeneutics_raw_score=0.92,
                cherry_pick_penalty=0.08,
                verified_strata=[
                    ArchaeologicalStratumMatch("Sarasvati River Full Flowing Strata", "Ghaggar-Hakra Paleochannel", 2600.0, 300.0, 0.95),
                    ArchaeologicalStratumMatch("Kalibangan Period II Fire Altars", "Mature Harappan Ritual Pits", 2400.0, 200.0, 0.90),
                    ArchaeologicalStratumMatch("Sinauli Warrior Burials & Chariots", "Copper Hoard / OCP-Late Harappan", 1900.0, 150.0, 0.88)
                ],
                summary_claim="Matches perennial Sarasvati flowing from mountains to sea (RV 7.95), prior to its 1900 BCE desiccation at Vinasana."
            ),
            ChronologicalHypothesis(
                name="c. 1500–1200 BCE Colonial Minimalist Migration Model",
                proponent_or_school="Max Müller (1859) / Colonial Indology / Michael Witzel",
                proposed_date_bce=1300.0,
                target_strata_level=TextualStrataLevel.MAHABHARATA_ENCYCLOPEDIC,
                astronomy_raw_score=0.20,
                archaeology_raw_score=0.35,
                epigraphy_raw_score=0.45,
                linguistics_raw_score=0.65,
                hermeneutics_raw_score=0.30,
                cherry_pick_penalty=0.35,
                verified_strata=[
                    ArchaeologicalStratumMatch("Mitanni Cuneiform Inscription", "Tell el-Amarna / Boghazkoy", 1380.0, 50.0, 0.85)
                ],
                summary_claim="Biblical literalism legacy compressing Indian chronology; cannot explain perennial Sarasvati or 2500 BCE Krittika equinox."
            ),
            ChronologicalHypothesis(
                name="7500 BCE Bhirrana Neolithic Antiquity Model",
                proponent_or_school="Harry Sahota / Radical Revisionist Out-of-India School",
                proposed_date_bce=7500.0,
                target_strata_level=TextualStrataLevel.JAYA_CORE,
                astronomy_raw_score=0.30,
                archaeology_raw_score=0.15,
                epigraphy_raw_score=0.05,
                linguistics_raw_score=0.10,
                hermeneutics_raw_score=0.40,
                cherry_pick_penalty=0.55,
                verified_strata=[
                    ArchaeologicalStratumMatch("Bhirrana Period IA Charcoal Stratum", "Early Neolithic Hakra Pit", 7500.0, 400.0, 0.20)
                ],
                summary_claim="Conflates early Neolithic subterranean dwelling pits with late Bronze Age horse-drawn chariot warfare and Rigvedic poetry."
            )
        ]

    def arbitrate_rigveda_chronology(
        self,
        custom_hypotheses: Optional[List[ChronologicalHypothesis]] = None
    ) -> List[ArbitrationResult]:
        """Arbitrates Rigvedic chronological benchmarks."""
        hyps = custom_hypotheses or self.get_default_rigveda_benchmarks()
        return self.arbitrate(hyps)


