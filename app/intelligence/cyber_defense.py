"""Cognitive Cybersecurity & Scam Defense Engine (app/intelligence/cyber_defense.py)

Synthesizes classical Indic statecraft (Pañcatantra Kākolūkīya, Kauṭilīya Arthaśāstra)
and Upaniṣadic psychology (Kaṭha Upaniṣad Ratha Rūpaka) with modern cybersecurity threat
modeling, social engineering counter-measures, and national reporting escalation.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any
import re


class CyberScamVector(str, Enum):
    DIGITAL_ARREST_EXTORTION = "DIGITAL_ARREST_EXTORTION"
    INVESTMENT_LOBHA_TRAP = "INVESTMENT_LOBHA_TRAP"
    PHISHING_IDENTITY_THEFT = "PHISHING_IDENTITY_THEFT"
    FEAR_AUTHORITY_IMPERSONATION = "FEAR_AUTHORITY_IMPERSONATION"
    ROMANCE_HONEYTRAP = "ROMANCE_HONEYTRAP"
    LOTTERY_PRIZE_DECEPTION = "LOTTERY_PRIZE_DECEPTION"
    MALWARE_APK_DOWNLOAD = "MALWARE_APK_DOWNLOAD"
    UNKNOWN_TACTIC = "UNKNOWN_TACTIC"


class PsychologicalKleSha(str, Enum):
    LOBHA = "LOBHA (Greed for unearned returns / free wealth)"
    BHAYA = "BHAYA (Panic from fabricated legal / police arrest)"
    MOHA = "MOHA (Delusional attachment to virtual illusions)"
    KAMA = "KĀMA (Lust / sensory impulse exploitation)"
    ASMITA = "ASMITĀ (Ego inflation / vanity manipulation)"


@dataclass
class CyberThreatEvaluation:
    query: str
    detected_vector: CyberScamVector
    primary_klesha_exploited: PsychologicalKleSha
    threat_confidence: float
    is_malicious_scam: bool
    kautilya_deception_class: str
    upanishadic_cognitive_countermeasure: str
    immediate_operational_steps: List[str]
    national_helpline_action: str
    forensic_critique: str


class CognitiveCybersecurityEngine:
    """Engine mapping ancient threat models and Upaniṣadic psychology to cyber defense."""

    HELPLINE_CYBERCRIME: str = "1930 (National Cyber Crime Reporting Helpline)"
    PORTAL_CYBERCRIME: str = "https://cybercrime.gov.in"

    @classmethod
    def evaluate_threat(cls, text: str) -> CyberThreatEvaluation:
        text_lower = text.lower()
        
        # 1. Digital Arrest / Law Enforcement Impersonation
        if any(k in text_lower for k in [
            "digital arrest", "cbi officer", "customs parcel", "police verification video call",
            "arrest warrant skype", "narcotics parcel", "ed raid warrant", "cyber police call"
        ]):
            return CyberThreatEvaluation(
                query=text,
                detected_vector=CyberScamVector.DIGITAL_ARREST_EXTORTION,
                primary_klesha_exploited=PsychologicalKleSha.BHAYA,
                threat_confidence=0.98,
                is_malicious_scam=True,
                kautilya_deception_class="Bhaya-Kūṭa (Fabricated Coercive Intimidation per Arthaśāstra 1.14)",
                upanishadic_cognitive_countermeasure=(
                    "Sākṣī-Bhāva (Detached Witnessing): Recognize that panic is an artificial emotional perturbation. "
                    "Law enforcement agencies never conduct arrests or demand money over Skype, WhatsApp, or video calls."
                ),
                immediate_operational_steps=[
                    "Disconnect the video/audio call immediately; do not engage or plead.",
                    "Never transfer funds to any 'verification account' or 'RBI safe custody account'.",
                    "Block the offending numbers and preserve screenshots of call logs and profile pictures.",
                    "Report immediately to the National Cyber Crime portal or your local police station."
                ],
                national_helpline_action=f"Dial {cls.HELPLINE_CYBERCRIME} instantly or log in to {cls.PORTAL_CYBERCRIME}.",
                forensic_critique=(
                    "Classic coercive intimidation utilizing fabricated official insignia to trigger acute cortisol spikes, "
                    "bypassing prefrontal cognitive evaluation to compel urgent wire transfers."
                )
            )

        # 2. Investment / Easy Return Scam
        if any(k in text_lower for k in [
            "guaranteed return", "double money", "crypto investment telegram", "part time job like youtube",
            "daily 5000 profit", "insider stock tip telegram", "free trading signals"
        ]):
            return CyberThreatEvaluation(
                query=text,
                detected_vector=CyberScamVector.INVESTMENT_LOBHA_TRAP,
                primary_klesha_exploited=PsychologicalKleSha.LOBHA,
                threat_confidence=0.95,
                is_malicious_scam=True,
                kautilya_deception_class="Lobha-Prapañca (Enticement through Greed per Pañcatantra Mitra-Bheda)",
                upanishadic_cognitive_countermeasure=(
                    "Vairāgya (Dispassion) & Kaṭha Upaniṣad 1.2.2: Discriminate between Preyas (fleeting deceptive pleasure) "
                    "and Śreyas (durable truth). Extraordinary unearned returns are mathematically impossible in authentic markets."
                ),
                immediate_operational_steps=[
                    "Cease all communications on Telegram, WhatsApp, or unverified investment applications.",
                    "Refuse demands to pay 'processing fees' or 'tax clearance fees' to withdraw funds.",
                    "Verify SEBI registration numbers on official sebi.gov.in registries.",
                    "File a formal transaction freeze request with your bank."
                ],
                national_helpline_action=f"Call {cls.HELPLINE_CYBERCRIME} and freeze transaction reference numbers.",
                forensic_critique=(
                    "Pig-butchering (Sha Zhu Pan) architecture: building false trust with small initial payouts, "
                    "then demanding exponential capital injections before terminating access."
                )
            )

        # 3. Phishing / Malware APK Download
        if any(k in text_lower for k in [
            "install this apk", "electricity bill unpaid disconnect", "apk download link",
            "update bank pan card link", "lottery winner link", "gift card claim"
        ]):
            return CyberThreatEvaluation(
                query=text,
                detected_vector=CyberScamVector.MALWARE_APK_DOWNLOAD,
                primary_klesha_exploited=PsychologicalKleSha.MOHA,
                threat_confidence=0.92,
                is_malicious_scam=True,
                kautilya_deception_class="Channa-Kūṭa (Concealed Trojan Weaponry per Arthaśāstra 12.5)",
                upanishadic_cognitive_countermeasure=(
                    "Pramāda-Varjana (Avoidance of Carelessness): Do not click unverified links in urgency. "
                    "The senses must be held in reins like steady horses (Kaṭha Upaniṣad 1.3.3)."
                ),
                immediate_operational_steps=[
                    "Never download or install APK files from SMS, WhatsApp, or third-party web links.",
                    "Never enter netbanking credentials, OTPs, or UPI PINs on external forms.",
                    "If already installed, place the device in Airplane Mode and execute a full factory reset.",
                    "Inform your bank immediately to block netbanking and debit/credit cards."
                ],
                national_helpline_action=f"Report malicious URL/APK to {cls.PORTAL_CYBERCRIME} or call {cls.HELPLINE_CYBERCRIME}.",
                forensic_critique=(
                    "Remote access trojan (RAT) or SMS-forwarding malware engineered to capture banking two-factor OTPs "
                    "and execute unauthorized account drain."
                )
            )

        # Default: General Cyber Inquiry / Non-Malicious
        return CyberThreatEvaluation(
            query=text,
            detected_vector=CyberScamVector.UNKNOWN_TACTIC,
            primary_klesha_exploited=PsychologicalKleSha.ASMITA,
            threat_confidence=0.10,
            is_malicious_scam=False,
            kautilya_deception_class="Sāmānya-Rakṣā (General Operational Hygiene)",
            upanishadic_cognitive_countermeasure=(
                "Ratha-Rūpaka (Kaṭha Upaniṣad 1.3.3–4): Master the mind through discriminative intellect (Buddhi), "
                "observing digital phenomena without reactive panic or greed."
            ),
            immediate_operational_steps=[
                "Maintain robust unique passwords and hardware multi-factor authentication (MFA).",
                "Practice Zero-Trust principles: 'Never Trust, Always Verify' (Pañcatantra Kākolūkīya).",
                "Keep device operating systems and firmware updated."
            ],
            national_helpline_action="Preserve vigilance. In case of suspected fraud, report to 1930.",
            forensic_critique="General cybersecurity inquiry. No active high-confidence social engineering attack detected."
        )
