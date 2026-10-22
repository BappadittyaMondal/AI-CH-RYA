"""Pātañjala Siddhi Boundary & Anti-Pseudoscience Engine (app/verification/siddhi_boundary.py)

Deconstructs yogic siddhi claims, separating authentic consciousness psychology
from pseudoscientific 'quantum mechanics' conflations, anchored in Pātañjala Yoga Sūtras,
classical Sanskrit poetic idioms, and rigorous quantum information physics.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any


class SiddhiClaimType(str, Enum):
    MANOJAVITVA_MOBILITY = "MANOJAVITVA_MOBILITY (Speed of the Mind)"
    AKASHA_GAMANA_LEVITATION = "AKASHA_GAMANA_LEVITATION (Space Travel / Levitation)"
    QUANTUM_TELEPORTATION_CONFLATION = "QUANTUM_TELEPORTATION_CONFLATION (Pseudo-Quantum Macro Body)"
    AUTHENTIC_SAMADHI_INQUIRY = "AUTHENTIC_SAMADHI_INQUIRY (Classical Yogic Inquiry)"


@dataclass
class SiddhiAuditResult:
    query: str
    claim_type: SiddhiClaimType
    is_quantum_conflation: bool
    quantum_pseudoscience_penalty: float
    shastric_context_valid: bool
    patanjali_sutra_references: List[str]
    classical_poetic_idiom_analysis: str
    physics_quantum_reality: str
    philosophical_siddhanta: str


class PatanjaliSiddhiBoundaryEngine:
    """Engine auditing yogic siddhi claims against Patañjali Yoga Sūtras and physics."""

    @classmethod
    def audit_claim(cls, text: str) -> SiddhiAuditResult:
        text_lower = text.lower()

        # Check for Quantum Teleportation / Tunneling conflation with yogic body
        is_quantum_mix = any(k in text_lower for k in [
            "quantum teleportation", "quantum physics yoga", "quantum tunneling parashuram",
            "teleporting body", "quantum entangle body", "quantum siddhi"
        ])

        is_parashurama_or_speed = any(k in text_lower for k in [
            "parashurama", "parshuram", "speed of the mind", "manojav", "manojavitva",
            "kailash speed", "insane speed", "reach kailash"
        ])

        if is_quantum_mix or (is_parashurama_or_speed and "quantum" in text_lower):
            return SiddhiAuditResult(
                query=text,
                claim_type=SiddhiClaimType.QUANTUM_TELEPORTATION_CONFLATION,
                is_quantum_conflation=True,
                quantum_pseudoscience_penalty=0.85,
                shastric_context_valid=False,
                patanjali_sutra_references=[
                    "Yoga Sūtra 3.37: ते समाधावुपसर्गा व्युत्थाने सिद्धयः (Siddhis are obstacles to Samādhi)",
                    "Yoga Sūtra 3.48: ततो मनोजवित्वं विकरणभावः प्रधानजयश्च (Mastery of matter and cognitive speed)",
                    "Yoga Sūtra 3.42: कायाकाशयोः सम्बन्धसंयमाल्लघुतूलसमापत्तेश्चाकाशगमनम् (Contemplation on space lightness)"
                ],
                classical_poetic_idiom_analysis=(
                    "In classical Sanskrit and Vedic literature, 'speed of the mind' (Manojavā) is a standard poetic idiom "
                    "(Upamāna), not a mechanical particle velocity. Mind is swiftest because thought crosses the universe instantly "
                    "(Ṛgveda 6.9.5: 'Mano javiṣṭhaṃ patayatsvantaḥ'; Īśā Upaniṣad 4). In Brahmāṇḍa Purāṇa 41, Paraśurāma's swiftness "
                    "signifies intense spiritual focus, while his walking on foot upon Jamadagni's martyrdom illustrates that Avatāras "
                    "honor earthly causality and biological grief within Dharma-Kṣetra."
                ),
                physics_quantum_reality=(
                    "Quantum teleportation (Bennett et al. 1993) transfers the quantum state of microscopic qubits via entangled Bell pairs "
                    "and a classical sub-lightspeed communication channel. A macroscopic human body contains ~10^28 atoms. Teleporting a "
                    "macroscopic biological entity would require 10^28 entangled pairs and dissipates colossal thermodynamic entropy "
                    "(Landauer's Principle: ΔQ ≥ kT ln 2). Claiming that ancient sages performed macroscopic quantum teleportation is an "
                    "anachronistic category error that distorts both physics and Śāstra."
                ),
                philosophical_siddhanta=(
                    "Yoga is Citta-Vṛtti-Nirodha (dissolution of mental fluctuations for Kaivalya), not the pursuit of macroscopic occult "
                    "powers. Seeking superpowers through quantum jargon is a manifestation of Vyutthāna (worldly distraction)."
                )
            )

        if is_parashurama_or_speed:
            return SiddhiAuditResult(
                query=text,
                claim_type=SiddhiClaimType.MANOJAVITVA_MOBILITY,
                is_quantum_conflation=False,
                quantum_pseudoscience_penalty=0.0,
                shastric_context_valid=True,
                patanjali_sutra_references=[
                    "Yoga Sūtra 3.48: ततो मनोजवित्वं विकरणभावः प्रधानजयश्च",
                    "Yoga Sūtra 3.37: ते समाधावुपसर्गा व्युत्थाने सिद्धयः"
                ],
                classical_poetic_idiom_analysis=(
                    "Manojavitva in Patañjali Yoga Sūtra 3.48 refers to the mind-like freedom of consciousness operating without physical "
                    "sensory friction (Vikaraṇa-bhāva) through Pradhāna-jaya (mastery over Prakṛti). It describes the subjective inner state "
                    "of the accomplished Yogī, not an external transportation vehicle."
                ),
                physics_quantum_reality=(
                    "No macroscopic physical violation involved when understood within its proper psychological and metaphysical context."
                ),
                philosophical_siddhanta=(
                    "Siddhis described in Vibhūti Pāda are secondary side-effects and explicit hindrances (Upasargas) to Kaivalya."
                )
            )

        # Default: Classical Yogic Inquiry
        return SiddhiAuditResult(
            query=text,
            claim_type=SiddhiClaimType.AUTHENTIC_SAMADHI_INQUIRY,
            is_quantum_conflation=False,
            quantum_pseudoscience_penalty=0.0,
            shastric_context_valid=True,
            patanjali_sutra_references=[
                "Yoga Sūtra 1.2: योगश्चित्तवृत्तिनिरोधः",
                "Yoga Sūtra 3.37: ते समाधावुपसर्गा व्युत्थाने सिद्धयः"
            ],
            classical_poetic_idiom_analysis="Standard Pātañjala inquiry centered on mental stillness and meditative realization.",
            physics_quantum_reality="Operates within epistemological and psychological domains.",
            philosophical_siddhanta="True achievement in Yoga is detachment (Vairāgya) and Self-knowledge (Puruṣa-Khyāti)."
        )
