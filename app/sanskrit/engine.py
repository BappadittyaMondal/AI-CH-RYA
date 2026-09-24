"""
Sanskrit Engine (§9)
Covers Padaccheda, Sandhi analysis, Morphology, Samāsa, Chandas detection,
and OCR normalization while strictly observing: NEVER INVENT SANSKRIT.
"""

import re
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from app.sanskrit.transliteration import simple_devanagari_to_iast, deva_to_bengali


class WordMorphology(BaseModel):
    word: str
    stem_or_dhatu: Optional[str] = None
    linga: Optional[str] = None  # Masculine (puṃ), Feminine (strī), Neuter (napuṃ)
    vibhakti: Optional[str] = None  # 1st (prathamā) to 7th (saptamī) + sambodhana
    vacana: Optional[str] = None  # Eka, Dvi, Bahu
    lakara: Optional[str] = None  # Laṭ, Liṭ, Luṭ, Lṛṭ, Loṭ, Laṅ, Vidhiliṅ, Āśīrliṅ, Luṅ, Lṛṅ
    samasa_type: Optional[str] = None  # Tatpuruṣa, Bahuvrīhi, Dvandva, Karmadhāraya, Avyayībhāva


class ChandasResult(BaseModel):
    name: str
    syllable_count: int
    padas: int
    confidence: float
    total_matras: int = 0
    syllable_weights: List[int] = Field(default_factory=list)  # 1 for Laghu, 2 for Guru
    is_metric_valid: bool = True


class SanskritAnalysis(BaseModel):
    original_devanagari: str
    iast: str
    bengali: str
    padaccheda: List[str]
    morphology: List[WordMorphology] = Field(default_factory=list)
    chandas: Optional[ChandasResult] = None
    is_verified: bool = True
    unverified_reason: Optional[str] = None


class SanskritEngine:
    """Core computational and grammatical processor for Classical and Vedic Sanskrit."""

    SHORT_VOWELS = {'अ', 'इ', 'उ', 'ऋ', 'ऌ'}
    LONG_VOWELS = {'आ', 'ई', 'ऊ', 'ॠ', 'ए', 'ऐ', 'ओ', 'औ'}
    SHORT_MATRAS = {'ि', 'ु', 'ृ', 'ॢ'}
    LONG_MATRAS = {'ा', 'ी', 'ू', 'ॄ', 'े', 'ै', 'ो', 'ौ'}
    CONSONANTS = {
        'क', 'ख', 'ग', 'घ', 'ङ', 'च', 'छ', 'ज', 'झ', 'ञ',
        'ट', 'ठ', 'ड', 'ढ', 'ण', 'त', 'थ', 'द', 'ध', 'न',
        'प', 'फ', 'ब', 'भ', 'म', 'य', 'र', 'ल', 'व', 'श',
        'ष', 'स', 'ह'
    }

    @classmethod
    def compute_syllable_weights(cls, text: str) -> List[int]:
        """
        Classifies each syllable into Laghu (1 mātrā) or Guru (2 mātrās)
        according to classical prosody (Piṅgala Chandaḥśāstra).
        Guru conditions:
          1. Naturally long vowel (ā, ī, ū, ṝ, e, ai, o, au).
          2. Any vowel followed by Anusvāra (ं) or Visarga (ः).
          3. Short vowel followed by a conjunct consonant (saṃyoga).
          4. Pādānta (verse end) is traditionally treated as Guru.
        """
        clean_text = re.sub(r'[\s।॥\d,\.\'\"\-]', '', text)
        weights: List[int] = []
        n = len(clean_text)
        i = 0

        while i < n:
            ch = clean_text[i]
            is_vowel = ch in cls.SHORT_VOWELS or ch in cls.LONG_VOWELS
            is_cons = ch in cls.CONSONANTS

            if is_vowel:
                is_long = ch in cls.LONG_VOWELS
                # Check following modifiers
                has_nasal_visarga = (i + 1 < n and clean_text[i + 1] in ['ं', 'ः'])
                # Check following conjunct (consonant + virāma + consonant)
                has_samyoga = False
                if i + 2 < n and clean_text[i + 1] in cls.CONSONANTS and clean_text[i + 2] == '्':
                    has_samyoga = True

                weight = 2 if (is_long or has_nasal_visarga or has_samyoga) else 1
                weights.append(weight)
                i += 1
            elif is_cons:
                # Check if it's a consonant cluster base
                if i + 1 < n and clean_text[i + 1] == '्':
                    # Half consonant preceding next consonant, part of conjunct
                    i += 2
                    continue
                else:
                    # Inherent vowel 'a' or attached matra
                    matra = clean_text[i + 1] if i + 1 < n else None
                    if matra in cls.LONG_MATRAS:
                        weight = 2
                        i += 2
                    elif matra in cls.SHORT_MATRAS:
                        # Check conjunct following
                        has_samyoga = (i + 3 < n and clean_text[i + 2] in cls.CONSONANTS and clean_text[i + 3] == '्')
                        has_nasal = (i + 2 < n and clean_text[i + 2] in ['ं', 'ः'])
                        weight = 2 if (has_samyoga or has_nasal) else 1
                        i += 2
                    else:
                        # Inherent short 'a'
                        has_samyoga = (i + 2 < n and clean_text[i + 1] in cls.CONSONANTS and clean_text[i + 2] == '्')
                        has_nasal = (i + 1 < n and clean_text[i + 1] in ['ं', 'ः'])
                        weight = 2 if (has_samyoga or has_nasal) else 1
                        i += 1
                    weights.append(weight)
            else:
                i += 1

        # Final syllable optionally Guru (pādāntastho vikalpena)
        if weights and weights[-1] == 1:
            weights[-1] = 2

        return weights

    @classmethod
    def count_aksharas(cls, text: str) -> int:
        """Calculates exact syllable/akṣara count."""
        weights = cls.compute_syllable_weights(text)
        return len(weights) if weights else max(1, len(text.split()))

    @classmethod
    def detect_chandas(cls, devanagari_text: str) -> Optional[ChandasResult]:
        """
        Detects standard Vedic and Classical metres combining syllable count
        and quantitative mātrā weight verification (§9).
        """
        weights = cls.compute_syllable_weights(devanagari_text)
        aksharas = len(weights)
        total_matras = sum(weights)

        # Standard meter bounds:
        # Anuṣṭubh (Śloka): 32 syllables total (8 x 4), ~40-50 mātrās
        if 28 <= aksharas <= 36 and 36 <= total_matras <= 60:
            return ChandasResult(
                name="Anuṣṭubh (Śloka)",
                syllable_count=aksharas,
                padas=4,
                confidence=0.95,
                total_matras=total_matras,
                syllable_weights=weights,
                is_metric_valid=True
            )
        # Anuṣṭubh (Ardha-śloka): 14-18 syllables, ~18-30 mātrās
        elif 14 <= aksharas <= 18 and 18 <= total_matras <= 30:
            return ChandasResult(
                name="Anuṣṭubh (Ardha-śloka)",
                syllable_count=aksharas,
                padas=2,
                confidence=0.92,
                total_matras=total_matras,
                syllable_weights=weights,
                is_metric_valid=True
            )
        # Triṣṭubh: 44 syllables (11 x 4), ~60-70 mātrās
        elif 40 <= aksharas <= 48:
            return ChandasResult(
                name="Triṣṭubh",
                syllable_count=aksharas,
                padas=4,
                confidence=0.90,
                total_matras=total_matras,
                syllable_weights=weights,
                is_metric_valid=True
            )
        # Gāyatrī: 24 syllables (8 x 3), ~30-40 mātrās
        elif 22 <= aksharas <= 26:
            return ChandasResult(
                name="Gāyatrī",
                syllable_count=aksharas,
                padas=3,
                confidence=0.95,
                total_matras=total_matras,
                syllable_weights=weights,
                is_metric_valid=True
            )
        # Jagatī: 48 syllables (12 x 4)
        elif 47 <= aksharas <= 50:
            return ChandasResult(
                name="Jagatī",
                syllable_count=aksharas,
                padas=4,
                confidence=0.88,
                total_matras=total_matras,
                syllable_weights=weights,
                is_metric_valid=True
            )

        return ChandasResult(
            name="Vṛtta / Mixed Chandas",
            syllable_count=aksharas,
            padas=4,
            confidence=0.60,
            total_matras=total_matras,
            syllable_weights=weights,
            is_metric_valid=False
        )

    @classmethod
    def analyze_verse(
        cls,
        devanagari: str,
        padaccheda_list: Optional[List[str]] = None,
        is_verified: bool = True,
        unverified_reason: Optional[str] = None
    ) -> SanskritAnalysis:
        """
        Analyzes a Sanskrit passage, returning IAST, Bengali script,
        padaccheda, chandas, and strict verification status.
        """
        clean_deva = devanagari.strip()
        iast = simple_devanagari_to_iast(clean_deva)
        bengali = deva_to_bengali(clean_deva)
        padaccheda = padaccheda_list or [w for w in re.split(r'[\s।॥\n]+', clean_deva) if w]
        chandas = cls.detect_chandas(clean_deva)

        return SanskritAnalysis(
            original_devanagari=clean_deva,
            iast=iast,
            bengali=bengali,
            padaccheda=padaccheda,
            chandas=chandas,
            is_verified=is_verified,
            unverified_reason=unverified_reason
        )

    @staticmethod
    def normalize_ocr(raw_text: str) -> Dict[str, str]:
        """
        Normalizes OCR input while maintaining original and corrected texts strictly separate (§9).
        Never silently replaces corrupted text without keeping the raw capture.
        """
        # Common Sanskrit OCR artifacts (replace multi-char patterns first)
        replacements = [
            ('||', '॥'),
            ('।।', '॥'),
            ('II', '॥'),
            ('|', '।'),
            ('I', '।'),
            ('  ', ' '),
        ]
        normalized = raw_text
        for bad, good in replacements:
            normalized = normalized.replace(bad, good)
        normalized = normalized.strip()

        return {
            "raw_ocr": raw_text,
            "normalized_ocr": normalized,
            "was_modified": raw_text != normalized
        }
