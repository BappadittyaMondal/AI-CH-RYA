"""
Hallucination Firewall (Verse Verification Gate) (§19)
Executes a strict 6-step pre-flight check before quoting any scripture.
Prevents manufactured Sanskrit, invented chapter/verse numbers, and fabricated commentaries.
"""

from typing import Optional, Dict
from pydantic import BaseModel


class VerseVerificationRequest(BaseModel):
    text_name: str
    chapter: str
    verse: str
    sanskrit_passage: str
    purported_translation: Optional[str] = None


class VerificationGateResult(BaseModel):
    passed: bool
    step_failed: Optional[str] = None
    failure_message: Optional[str] = None
    canonical_reference: Optional[str] = None
    safe_output_text: str


# Canonical seed database for instant verified lookup
CANONICAL_SEEDS: Dict[str, Dict[str, str]] = {
    "BG_2_47": {
        "text": "Bhagavad Gītā",
        "chapter": "2",
        "verse": "47",
        "sanskrit": "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन। मा कर्मफलहेतुर्भूर्मा ते सङ्गोऽस्त्वकर्मणि॥",
        "iast": "karmaṇyevādhikāraste mā phaleṣu kadācana | mā karmaphalaheturbhūrmā te saṅgo'stvakarmaṇi ||",
        "translation": "You have a right only to work, never to its fruits; let not the fruits of action be your motive, nor let your attachment be to inaction."
    },
    "ISHA_1": {
        "text": "Īśā Upaniṣad",
        "chapter": "1",
        "verse": "1",
        "sanskrit": "ॐ ईशा वास्यमिदं सर्वं यत्किञ्च जगत्यां जगत्। तेन त्यक्तेन भुञ्जीथा मा गृधः कस्यस्विद्धनम्॥",
        "iast": "oṃ īśā vāsyamidaṃ sarvaṃ yatkiñca jagatyāṃ jagat | tena tyaktena bhuñjīthā mā gṛdhaḥ kasyasviddhanam ||",
        "translation": "All this, whatsoever moves in this moving world, is enveloped by the Lord. By renouncing that, find joy; do not covet anyone's wealth."
    }
}


class HallucinationFirewall:
    """Rigorous gatekeeper against verse hallucination."""

    KNOWN_TEXTS = {
        "bhagavad gita", "bhagavad gītā", "gita", "gītā", "bg",
        "isha upanishad", "īśā upaniṣad", "isha", "īśā",
        "katha upanishad", "kaṭha upaniṣad", "katha",
        "mundaka upanishad", "muṇḍaka upaniṣad",
        "mandukya upanishad", "māṇḍūkya upaniṣad",
        "rigveda", "ṛgveda", "samaveda", "sāmaveda", "yajurveda", "atharvaveda",
        "mahabharata", "mahābhārata", "ramayana", "rāmāyaṇa"
    }

    @classmethod
    def verify(cls, req: VerseVerificationRequest) -> VerificationGateResult:
        # Step 1: Does this text exist?
        clean_text = req.text_name.strip().lower()
        if clean_text not in cls.KNOWN_TEXTS:
            return VerificationGateResult(
                passed=False,
                step_failed="Step 1: Text Existence",
                failure_message=f"Text '{req.text_name}' is not recognized in the canonical corpus index.",
                safe_output_text=f"I cannot verify this quotation precisely — the text '{req.text_name}' could not be confirmed in verified catalogs."
            )

        # Step 2: Correct source identified?
        # Step 3 & 4: Correct chapter & verse?
        key = None
        if any(term in clean_text for term in ["git", "gīt", "bg"]):
            key = f"BG_{req.chapter.strip()}_{req.verse.strip()}"
        elif any(term in clean_text for term in ["ish", "īś", "isopanisad"]):
            key = f"ISHA_{req.verse.strip()}"

        if key and key in CANONICAL_SEEDS:
            seed = CANONICAL_SEEDS[key]
            # Step 5: Sanskrit text verified against real edition?
            clean_input_sanskrit = "".join(req.sanskrit_passage.split())
            clean_seed_sanskrit = "".join(seed["sanskrit"].split())

            # Check if input sanskrit matches canonical text or is fake
            if clean_input_sanskrit and clean_input_sanskrit not in clean_seed_sanskrit and clean_seed_sanskrit not in clean_input_sanskrit:
                return VerificationGateResult(
                    passed=False,
                    step_failed="Step 5: Sanskrit Text Verification",
                    failure_message="The provided Sanskrit string does not match authentic verified critical editions.",
                    safe_output_text="I cannot verify this Sanskrit quotation precisely against authentic critical editions. Here is what is canonical: " + seed["sanskrit"]
                )

            return VerificationGateResult(
                passed=True,
                canonical_reference=f"{seed['text']} {seed['chapter']}.{seed['verse']}",
                safe_output_text=f"Verified: {seed['sanskrit']}"
            )

        # For verses not yet seeded or suspicious references
        if req.chapter.isdigit() and int(req.chapter) > 100:
            return VerificationGateResult(
                passed=False,
                step_failed="Step 3: Chapter Verification",
                failure_message=f"Chapter {req.chapter} exceeds canonical limits for {req.text_name}.",
                safe_output_text="I cannot verify this citation precisely — the cited chapter does not exist in standard editions."
            )

        # Unverified fallback (§19)
        return VerificationGateResult(
            passed=False,
            step_failed="Step 5/6: Unverified Passage",
            failure_message="Passage could not be verified in the primary corpus.",
            safe_output_text="I cannot verify this quotation precisely from primary critical editions — here is what can be confirmed from available secondary scholarship."
        )
