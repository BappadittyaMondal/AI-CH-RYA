"""
AI ĀCHĀRYA — Pāṇinian Articulatory Phonetics & Poetic Constraint Engine (app/sanskrit/phonetics_engine.py)

Covers classical Pāṇinian Śikṣā and Kāvya-śāstra formal constraints:
1. Uccāraṇa-Sthāna (Articulatory Places):
   - Kaṇṭhya (Velar/Guttural)
   - Tālavya (Palatal)
   - Mūrdhanya (Retroflex)
   - Dantya (Dental)
   - Oṣṭhya (Labial)
   - Mixed: Kaṇṭha-Tālavya, Kaṇṭhoṣṭhya, Dantoṣṭhya
2. Niroṣṭhya Constraint Validator:
   - Validates compositions composed strictly without labial phonemes (lips never touch).
   - Audits Niroṣṭhya Rāmāyaṇa, Dāśarathi hymns, and lip-free stotras.
3. Citra-Kāvya Formal Constraint Engine:
   - Sarvatobhadra & Akṣara-Palindromes.
   - Ekākṣarī (single consonant verses, e.g., Bhāravi's Kirātārjunīya 15.14).
   - Dvyakṣarī (two consonant verses).
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple
import re


class UccaranaSthana(str, Enum):
    KANTHYA = "Kaṇṭhya (Velar / Throat)"
    TALAVYA = "Tālavya (Palatal)"
    MURDHANYA = "Mūrdhanya (Retroflex / Roof of Mouth)"
    DANTYA = "Dantya (Dental / Teeth)"
    OSTHYA = "Oṣṭhya (Labial / Lips)"
    KANTHA_TALAVYA = "Kaṇṭha-Tālavya (Palato-Guttural)"
    KANTHOSTHYA = "Kaṇṭhoṣṭhya (Labio-Guttural)"
    DANTOSTHYA = "Dantoṣṭhya (Labio-Dental)"
    NASIKA = "Nāsikā (Nasal / Anusvāra)"


@dataclass(frozen=True)
class NiroshthyaAuditResult:
    is_niroshthya: bool
    total_characters: int
    labial_count: int
    detected_labial_symbols: List[str]
    forensic_critique: str
    stylistic_category: str


@dataclass(frozen=True)
class CitraKavyaAuditResult:
    is_palindrome: bool
    distinct_consonants_count: int
    distinct_consonants: List[str]
    is_ekaksari: bool
    is_dvyaksari: bool
    pattern_name: str
    forensic_critique: str


class PaninianPhoneticsEngine:
    """
    Computes Pāṇinian articulatory classification and verifies
    severe formal poetic constraints (Niroṣṭhya, Citra-kāvya).
    """

    # Pure labials: lips must meet or shape
    OSTHYA_VOWELS_DEVA = {'उ', 'ऊ'}
    OSTHYA_MATRAS_DEVA = {'ु', 'ू'}
    OSTHYA_CONSONANTS_DEVA = {'प', 'फ', 'ब', 'भ', 'म'}
    
    # Mixed labials
    KANTHOSTHYA_DEVA = {'ओ', 'औ', 'ो', 'ौ'}
    DANTOSTHYA_DEVA = {'व'}

    # IAST equivalents
    OSTHYA_IAST = {'u', 'ū', 'p', 'ph', 'b', 'bh', 'm'}
    MIXED_LABIAL_IAST = {'o', 'au', 'v'}

    @classmethod
    def audit_niroshthya(cls, text: str, strict_mode: bool = True) -> NiroshthyaAuditResult:
        """
        Audits whether a text is strictly Niroṣṭhya (composed without labial contact).
        In strict mode, mixed labials (o, au, v) are also treated as labial infractions.
        """
        detected_labials: List[str] = []
        clean_text = re.sub(r'[\s।॥\d,\.\'\"\-\?\!]', '', text)
        n = len(clean_text)

        i = 0
        while i < n:
            ch = clean_text[i]
            
            # Check Devanagari labials
            if ch in cls.OSTHYA_VOWELS_DEVA or ch in cls.OSTHYA_MATRAS_DEVA or ch in cls.OSTHYA_CONSONANTS_DEVA:
                detected_labials.append(ch)
            elif strict_mode and (ch in cls.KANTHOSTHYA_DEVA or ch in cls.DANTOSTHYA_DEVA):
                detected_labials.append(ch)
            # Check IAST two-char aspirates (ph, bh)
            elif i + 1 < n and clean_text[i:i+2].lower() in {'ph', 'bh'}:
                detected_labials.append(clean_text[i:i+2])
                i += 1
            # Check IAST two-char labio-guttural diphthong (au)
            elif strict_mode and i + 1 < n and clean_text[i:i+2].lower() == 'au':
                detected_labials.append(clean_text[i:i+2])
                i += 1
            # Check IAST single-char pure labials
            elif ch.lower() in {'u', 'ū', 'p', 'b', 'm'}:
                detected_labials.append(ch)
            # Check IAST single-char mixed labials (o, v)
            elif strict_mode and ch.lower() in {'o', 'v'}:
                detected_labials.append(ch)
            i += 1

        is_pure = (len(detected_labials) == 0)
        labial_count = len(detected_labials)

        if is_pure:
            critique = (
                "PERFECT NIROṢṬHYA COMPOSITION: Zero labial phonemes detected. "
                "The entire text can be recited continuously without the lips ever touching or closing. "
                "Exemplifies classical Pāṇinian articulatory mastery (as found in Niroṣṭhya Rāmāyaṇa)."
            )
            style = "Pure Niroṣṭhya (Lip-Free Classical Constraint)"
        else:
            critique = (
                f"NIROṢṬHYA INFRACTION DETECTED: Found {labial_count} labial instances "
                f"({', '.join(detected_labials[:8])}{'...' if labial_count > 8 else ''}). "
                "Requires bilabial or labiodental articulation."
            )
            style = "Standard Classical (Unconstrained Articulation)"

        return NiroshthyaAuditResult(
            is_niroshthya=is_pure,
            total_characters=n,
            labial_count=labial_count,
            detected_labial_symbols=detected_labials,
            forensic_critique=critique,
            stylistic_category=style
        )

    @classmethod
    def audit_citra_kavya(cls, text: str) -> CitraKavyaAuditResult:
        """
        Audits extreme Citra-kāvya combinatorial and symmetrical constraints:
        - Palindromic (Gatapratiyāgata / Sarvatobhadra)
        - Ekākṣarī (one consonant throughout the verse)
        - Dvyakṣarī (two consonants throughout the verse)
        """
        # Strip punctuation, whitespace, dandas
        clean_text = re.sub(r'[\s।॥\d,\.\'\"\-\?\!]', '', text).lower()
        
        # Devanagari Akṣara-level extraction
        aksharas = re.findall(r'(?:[क-ह]्)*[क-ह][\u093e-\u094c]?[\u0902\u0903]?|[अ-औ][\u0902\u0903]?', text)
        is_akshara_pal = (len(aksharas) >= 3 and aksharas == aksharas[::-1])
        is_char_pal = (len(clean_text) >= 3 and clean_text == clean_text[::-1])
        is_pal = is_akshara_pal or is_char_pal

        # Extract consonants (accommodating aspirated Mahāprāṇa units in IAST)
        deva_consonants = re.findall(r'[क-ह]', text)
        iast_consonants = re.findall(r'kh|gh|ch|jh|ṭh|ḍh|th|dh|ph|bh|[kghṅcjñṭḍṇtdnpbmyrlvśṣsh]', text.lower())
        
        consonants = deva_consonants if len(deva_consonants) >= len(iast_consonants) else iast_consonants
        distinct = sorted(list(set(consonants)))
        count = len(distinct)

        is_eka = (count == 1 and len(consonants) >= 8)
        is_dvya = (count == 2 and len(consonants) >= 8)

        if is_eka:
            p_name = "Ekākṣarī (Single Consonant Tour-de-Force)"
            critique = f"Astounding single-consonant constraint: entire composition constructed exclusively with '{distinct[0]}'."
        elif is_dvya:
            p_name = "Dvyakṣarī (Two-Consonant Symmetry)"
            critique = f"Dual-consonant constraint: entire composition constructed using only '{distinct[0]}' and '{distinct[1]}'."
        elif is_pal:
            p_name = "Gatapratiyāgata (Symmetrical Palindrome)"
            critique = "Perfect bidirectional acoustic symmetry: reads identically forward and backward."
        else:
            p_name = "Standard Metrical Composition"
            critique = f"Natural phonetic variation using {count} distinct consonants."

        return CitraKavyaAuditResult(
            is_palindrome=is_pal,
            distinct_consonants_count=count,
            distinct_consonants=distinct,
            is_ekaksari=is_eka,
            is_dvyaksari=is_dvya,
            pattern_name=p_name,
            forensic_critique=critique
        )
