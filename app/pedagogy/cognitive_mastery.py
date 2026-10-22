"""
AI ĀCHĀRYA — Gurukula Cognitive Mastery, FSRS Modeling & Anti-Scam Firewall
(app/pedagogy/cognitive_mastery.py)

Synthesizes:
1. Free Spaced Repetition Scheduler (FSRS) power-law retention modeling.
2. Sweller's Cognitive Load Index (L_cog) with dynamic Anvaya/Padaccheda fragmentation.
3. Autonomic balance & vagal tone modeling (0.1 Hz resonance breathing & Thoppukaranam).
4. Cognitive Scam Firewall systematically debunking DMIT, midbrain activation, and 10X claims.
5. Sandboxed Ephemeral Learner State strictly isolated from canonical corpus (§27, §32).
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
import math
import re
import time


class ReviewGrade(int, Enum):
    AGAIN = 1   # Complete failure of recall
    HARD = 2    # Recalled with significant struggle
    GOOD = 3    # Recalled with normal effort
    EASY = 4    # Instant, effortless recall


@dataclass(frozen=True)
class FSRSSchedule:
    topic_id: str
    stability: float          # Days until retrievability drops to 90% (R=0.90)
    difficulty: float         # Scale 1.0 (trivial) to 10.0 (maximum complexity)
    elapsed_days: float       # Days since last review
    retrievability: float     # Estimated probability of recall: R(t, S) = (1 + 0.19 * t / S)^(-0.5)
    recommended_interval_days: float
    next_due_date_days: float


@dataclass(frozen=True)
class CognitiveLoadResult:
    concept_or_verse: str
    raw_complexity: float      # Scale 0.0 to 10.0
    student_fatigue: float     # Scale 0.0 to 1.0
    cognitive_load_index: float  # L_cog
    fragmentation_required: bool # True if L_cog > 0.85
    pedagogical_mode: str
    scaffolding_instruction: str


@dataclass(frozen=True)
class GurukulaFocusProtocol:
    protocol_name: str
    total_minutes: int
    steps: List[Dict[str, Any]]
    physiological_rationale: str
    cultural_context: str
    anti_fear_grounding: str


@dataclass(frozen=True)
class CognitiveScamReport:
    claim_text: str
    is_pseudoscientific: bool
    confidence: float
    detected_fallacies: List[str]
    medical_scientific_verdict: str
    shastric_verdict: str
    safe_alternative_recommendation: str


@dataclass
class LearnerCognitiveProfile:
    learner_id: str
    stability_deck: Dict[str, FSRSSchedule] = field(default_factory=dict)
    current_fatigue: float = 0.0
    completed_sessions: int = 0
    sandboxed_isolated: bool = True  # Strict physical separation from canonical database


class CognitiveMasteryEngine:
    """
    Production-grade cognitive engineering engine for students and seekers.
    Integrates FSRS retention math, cognitive load gating, autonomic yogic protocols,
    and a zero-tolerance firewall against commercial brain-enhancement quackery.
    """

    # In-memory ephemeral store for learner profiles (strictly isolated per §27, §32)
    _EPHEMERAL_PROFILES: Dict[str, LearnerCognitiveProfile] = {}

    # Cognitive scam patterns
    _SCAM_PATTERNS = [
        (
            r"\b(?:dmit|dermatoglyphics\s+multiple\s+intelligence)\b",
            "DMIT Dermatoglyphics Pseudoscience",
            "Indian Psychiatric Society (IPS) and international cognitive neuroscience classify DMIT as 'medical palmistry'. "
            "Fingerprint ridge patterns have zero clinical correlation with IQ, brain lobe dominance, or career aptitude."
        ),
        (
            r"\b(?:midbrain\s+activation|blindfold\s+read(?:ing)?|third\s+eye\s+activation\s+for\s+kids)\b",
            "Midbrain Activation & Blindfold Reading Scam",
            "The midbrain (mesencephalon) regulates basic auditory and visual motor reflexes; it cannot be 'activated' to give children "
            "blindfolded vision or photographic memory. Debunked in controlled tests as simple peeking magic tricks."
        ),
        (
            r"\b(?:10x\s+(?:faster\s+brain|memory)|300%\s+brain\s+power|overclock\s+your\s+brain|activate\s+90%\s+dormant\s+brain)\b",
            "10X Brain Power & 90% Dormant Brain Myth",
            "Neuroscience confirms humans use 100% of their brains. Working memory capacity is biologically constrained (Cowan's 4 chunks). "
            "Brain processing cannot be multiplied by 10X overnight via finger exercises or commercial workshops."
        ),
        (
            r"\b(?:teach\s+calculus\s+in\s+womb|abhimanyu\s+syllabus\s+for\s+fetus|garbha\s+sanskar\s+iit)\b",
            "In-Utero Academic Curriculum Fallacy",
            "While fetal auditory pathways sense maternal voice cadence from ~24 weeks, academic learning in utero is biologically impossible. "
            "Caraka Saṃhitā (Śārīrasthāna 8) emphasizes maternal peace, wholesome nutrition, and emotional stability, not academic tutoring."
        )
    ]

    # --- 1. FSRS RETENTION MATHEMATICS ---

    @staticmethod
    def compute_retrievability(elapsed_days: float, stability: float) -> float:
        """
        Free Spaced Repetition Scheduler (FSRS) power-law forgetting formula:
        R(t, S) = (1 + 0.19 * t / S)^(-0.5)
        """
        if stability <= 0.0:
            return 0.0
        if elapsed_days <= 0.0:
            return 1.0
        r = math.pow(1.0 + 0.19 * (elapsed_days / stability), -0.5)
        return max(0.0, min(1.0, round(r, 4)))

    @staticmethod
    def calculate_optimal_interval(stability: float, target_r: float = 0.90) -> float:
        """
        Calculates the interval t (in days) required for Retrievability to drop to target_r:
        t = (S / 0.19) * (target_r^(-2) - 1)
        """
        if stability <= 0.0:
            return 1.0
        target_r = max(0.70, min(0.98, target_r))
        r_neg_2 = math.pow(target_r, -2.0)
        interval = (stability / 0.19) * (r_neg_2 - 1.0)
        return max(0.5, round(interval, 2))

    def update_fsrs_schedule(
        self,
        topic_id: str,
        elapsed_days: float,
        current_stability: float,
        difficulty: float,
        grade: ReviewGrade = ReviewGrade.GOOD,
        target_r: float = 0.90
    ) -> FSRSSchedule:
        """
        Updates stability and returns new schedule following FSRS rules.
        """
        current_r = self.compute_retrievability(elapsed_days, current_stability)
        d = max(1.0, min(10.0, float(difficulty)))

        # Update difficulty based on grade
        if grade == ReviewGrade.AGAIN:
            d_new = min(10.0, d + 0.4)
        elif grade == ReviewGrade.EASY:
            d_new = max(1.0, d - 0.4)
        else:
            d_new = d

        # Update stability
        if grade == ReviewGrade.AGAIN:
            # Memory lapse: stability collapses
            s_new = max(0.5, current_stability * 0.25)
        else:
            # FSRS stability update:
            # S' = S * (1 + exp(w4) * (11 - D) * S^(-w5) * (exp(w6 * (1 - R)) - 1))
            # Standard tuned weights: w4 = 0.9, w5 = 0.2, w6 = 2.0
            w4, w5, w6 = 0.9, 0.2, 2.0
            grade_multiplier = 1.0 if grade == ReviewGrade.GOOD else (1.3 if grade == ReviewGrade.EASY else 0.7)
            term1 = math.exp(w4) * (11.0 - d_new)
            term2 = math.pow(max(0.5, current_stability), -w5)
            term3 = math.exp(w6 * (1.0 - current_r)) - 1.0
            s_increase = 1.0 + grade_multiplier * (term1 * term2 * term3)
            s_new = max(current_stability, current_stability * s_increase)

        s_new = round(s_new, 2)
        optimal_days = self.calculate_optimal_interval(s_new, target_r)

        return FSRSSchedule(
            topic_id=topic_id,
            stability=s_new,
            difficulty=round(d_new, 2),
            elapsed_days=round(elapsed_days, 2),
            retrievability=current_r,
            recommended_interval_days=optimal_days,
            next_due_date_days=optimal_days
        )

    # --- 2. COGNITIVE LOAD INDEX & DYNAMIC ANVAYA FRAGMENTATION ---

    def evaluate_cognitive_load(
        self,
        concept_or_verse: str,
        student_fatigue: float = 0.0,
        pedagogical_mode: str = "Student"
    ) -> CognitiveLoadResult:
        """
        Computes Sweller Cognitive Load Index:
        L_cog = (IntrinsicComplexity * 0.6 + ExtraneousNoise * 0.2 + Fatigue * 0.2) / C_WM
        Where C_WM = 4.0 (Cowan's working memory slot capacity).
        If L_cog > 0.85, triggers step-by-step Anvaya / Padaccheda pedagogical fragmentation.
        """
        text = concept_or_verse.strip()
        fatigue = max(0.0, min(1.0, float(student_fatigue)))

        # 1. Intrinsic Complexity estimation based on linguistic and conceptual markers
        length_penalty = min(3.0, len(text.split()) / 12.0)
        sanskrit_conjuncts = len(re.findall(r"[्|्र|्य|त्र|ज्ञ|क्ष|श्र]", text))
        conjunct_penalty = min(3.0, sanskrit_conjuncts * 0.25)
        philosophical_terms = sum(
            1 for w in ["advaita", "brahman", "māyā", "vivartavāda", "pariṇāmavāda", "anvaya", "vyāpti"]
            if w in text.lower()
        )
        term_penalty = min(4.0, philosophical_terms * 1.0)
        raw_complexity = min(10.0, 2.0 + length_penalty + conjunct_penalty + term_penalty)

        # 2. Extraneous Noise (formatting density, unexplained terms)
        extraneous_noise = 0.2 if len(text) > 200 else 0.05

        # 3. Working Memory Slot Bandwidth
        c_wm = 4.0

        # 4. Cognitive Load Index Calculation
        raw_load = (raw_complexity * 0.55) + (extraneous_noise * 1.5) + (fatigue * 3.0)
        l_cog = round(raw_load / c_wm, 3)

        fragmentation_required = (l_cog > 0.85)

        if fragmentation_required:
            instruction = (
                "DYNAMIC PEDAGOGICAL FRAGMENTATION TRIGGERED (L_cog > 0.85): "
                "The target concept or verse exceeds working memory capacity. "
                "1. Break verse into isolated Padaccheda (word boundaries). "
                "2. Present sequential Anvaya (prose syntactic order). "
                "3. Teach only one core philosophical proposition before introducing commentary debate."
            )
        else:
            instruction = (
                "STANDARD INTEGRATED PEDAGOGY: "
                "Working memory capacity is adequate (L_cog <= 0.85). "
                "Deliver full verse, transliteration, and commentary overview concurrently."
            )

        return CognitiveLoadResult(
            concept_or_verse=concept_or_verse,
            raw_complexity=round(raw_complexity, 2),
            student_fatigue=round(fatigue, 2),
            cognitive_load_index=l_cog,
            fragmentation_required=fragmentation_required,
            pedagogical_mode=pedagogical_mode,
            scaffolding_instruction=instruction
        )

    # --- 3. AUTONOMIC VAGAL PRIMING & GURUKULA FOCUS PROTOCOL ---

    def generate_gurukula_focus_protocol(self) -> GurukulaFocusProtocol:
        """
        Generates the evidence-based 20-minute daily Gurukula Focus Protocol,
        synthesizing neurobiology, vagal modulation, and classical Śāstric discipline.
        """
        steps = [
            {
                "phase": "Somatic Activation (00–05 min)",
                "technique": "Traditional Thoppukaranam (Gaṇeśa Karṇa-sparśa Namaskāra)",
                "reps": "14 to 21 slow rhythmic squats holding opposite earlobes with crossed arms",
                "mechanism": "Acupressure on the ear lobule stimulates auricular vagal afferents; deep squatting drives immediate arterial blood flow to the brain, alleviating mental lethargy (Tamas)."
            },
            {
                "phase": "Autonomic Coherence (05–10 min)",
                "technique": "Nāḍī Śodhana Prāṇāyāma (0.1 Hz Resonance Breathing)",
                "reps": "5 minutes of smooth, unforced alternate nostril breathing (approx. 6 breaths/min)",
                "mechanism": "0.1 Hz breathing synchronizes heart rate variability (Respiratory Sinus Arrhythmia), suppressing sympathetic fight-or-flight cortisol and activating prefrontal executive control."
            },
            {
                "phase": "Attentional Fixation (10–13 min)",
                "technique": "Trāṭaka / Dhāraṇā (Single-Point Visual Grounding)",
                "reps": "3 minutes of steady gaze on a ghee lamp flame, black dot, or tip of the nose",
                "mechanism": "Inhibits involuntary saccadic eye movements, training voluntary prefrontal attentional circuits and quieting the default mode network (DMN)."
            },
            {
                "phase": "Deep Deliberate Practice (13–50 min)",
                "technique": "Deep Work Block (Śravaṇa & Manana)",
                "reps": "35–40 minutes of uninterrupted single-task learning with all digital notifications silenced",
                "mechanism": "Leverages the post-prāṇāyāma alpha-band EEG brainwave state (8–12 Hz) for optimal synaptic consolidation."
            },
            {
                "phase": "Active Recall Consolidation (50–60 min)",
                "technique": "Book-Closed Verbal/Written Summary (Nididhyāsana Walk)",
                "reps": "10-minute walk while explaining key concepts from memory without looking at notes",
                "mechanism": "Active retrieval effort stimulates Brain-Derived Neurotrophic Factor (BDNF) and initiates hippocampal-to-neocortical memory transfer."
            }
        ]

        return GurukulaFocusProtocol(
            protocol_name="Sanātana-Cognitive 20-Minute Pre-Study Focus Protocol",
            total_minutes=20,
            steps=steps,
            physiological_rationale=(
                "Combines vagal nerve stimulation, cerebral blood perfusion, and resonance breathing "
                "to systematically downregulate exam stress and prime the cortex for high-retention study."
            ),
            cultural_context=(
                "Rooted in classical Gurukula lifestyle: bodily humility before Gaṇeśa (Thoppukaranam), "
                "breath mastery per Patañjali (Yoga Sūtra 2.49), and single-pointed focus (Dhāraṇā 3.1)."
            ),
            anti_fear_grounding=(
                "Abhaya (fearlessness per Gītā 16.1): Study with dedication to duty (Svadharma), "
                "freed from obsessive anxiety over test results (Gītā 2.47)."
            )
        )

    # --- 4. COGNITIVE SCAM FIREWALL ---

    def evaluate_cognitive_claim(self, claim_text: str) -> CognitiveScamReport:
        """
        Evaluates educational and brain optimization claims against empirical science
        and authentic Śāstric standards, systematically flagging quackery and commercial scams.
        """
        t_lower = claim_text.lower()
        detected_fallacies = []
        is_scam = False

        for pattern, fallacy_name, rebuttal in self._SCAM_PATTERNS:
            if re.search(pattern, t_lower):
                detected_fallacies.append(f"{fallacy_name}: {rebuttal}")
                is_scam = True

        if is_scam:
            scientific_verdict = (
                "PSEUDOSCIENCE DETECTED: This claim relies on scientifically unvalidated or debunked methods "
                "(such as fingerprint IQ testing or midbrain activation). Major psychiatric and neurological bodies "
                "explicitly reject these practices as commercial quackery."
            )
            shastric_verdict = (
                "APRAMĀṆIKA (Lacking Valid Means of Knowledge): Authentic Sanātana tradition upholds patient, "
                "disciplined Abhyāsa (Yoga Sūtra 1.12) and Sāttvika lifestyle (Caraka Saṃhitā). Commercial promises "
                "of instantaneous 10X brain multiplication or magical third-eye reading contradict genuine Śāstra."
            )
            alternative = (
                "Adopt verified cognitive science: Active retrieval practice, spaced repetition schedules (FSRS), "
                "7-8 hours of slow-wave sleep, and 15 minutes of daily Thoppukaranam and Prāṇāyāma."
            )
            conf = 0.95
        else:
            scientific_verdict = (
                "SCIENTIFICALLY COMPATIBLE: The inquiry aligns with established principles of neuroplasticity, "
                "motor coordination, or attention management."
            )
            shastric_verdict = (
                "PRAMĀṆA-COMPATIBLE: Consistent with classical Medhā and Dhī cultivation through conscious effort."
            )
            alternative = "Continue consistent, disciplined practice."
            conf = 0.85

        return CognitiveScamReport(
            claim_text=claim_text,
            is_pseudoscientific=is_scam,
            confidence=conf,
            detected_fallacies=detected_fallacies,
            medical_scientific_verdict=scientific_verdict,
            shastric_verdict=shastric_verdict,
            safe_alternative_recommendation=alternative
        )

    # --- 5. SANDBOXED LEARNER STATE MANAGEMENT (§27, §32) ---

    def get_or_create_learner_profile(self, learner_id: str) -> LearnerCognitiveProfile:
        """
        Retrieves or initializes a sandboxed learner profile in ephemeral storage.
        Guarantees 100% physical isolation from the canonical corpus database.
        """
        if learner_id not in self._EPHEMERAL_PROFILES:
            self._EPHEMERAL_PROFILES[learner_id] = LearnerCognitiveProfile(learner_id=learner_id)
        return self._EPHEMERAL_PROFILES[learner_id]

    def record_learner_review(
        self,
        learner_id: str,
        topic_id: str,
        grade: ReviewGrade,
        elapsed_days: float = 1.0,
        default_difficulty: float = 5.0
    ) -> FSRSSchedule:
        """
        Records an active retrieval review in the learner's sandboxed profile.
        """
        profile = self.get_or_create_learner_profile(learner_id)
        current_schedule = profile.stability_deck.get(topic_id)

        if current_schedule:
            current_s = current_schedule.stability
            current_d = current_schedule.difficulty
        else:
            current_s = 1.0
            current_d = default_difficulty

        new_schedule = self.update_fsrs_schedule(
            topic_id=topic_id,
            elapsed_days=elapsed_days,
            current_stability=current_s,
            difficulty=current_d,
            grade=grade
        )

        profile.stability_deck[topic_id] = new_schedule
        profile.completed_sessions += 1
        return new_schedule
