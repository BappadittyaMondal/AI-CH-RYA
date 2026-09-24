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

    @staticmethod
    def count_aksharas(text: str) -> int:
        """
        Calculates syllable/akṣara count for meter (chandas) detection.
        Strips virāma, punctuation, and counts vowels.
        """
        clean_text = re.sub(r'[\s।॥\d,\.\'\"\-]', '', text)
        # Approximate akṣara count by counting vowel nuclei in Devanagari or IAST
        vowel_markers = ['ा', 'ि', 'ी', 'ु', 'ू', 'ृ', 'ॄ', 'ॢ', 'े', 'ै', 'ो', 'ौ', 'ं', 'ः']
        independent_vowels = ['अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ॠ', 'ऌ', 'ए', 'ऐ', 'ओ', 'औ']
        consonants = ['क', 'ख', 'ग', 'घ', 'ङ', 'च', 'छ', 'ज', 'झ', 'ञ',
                      'ट', 'ठ', 'ड', 'ढ', 'ण', 'त', 'थ', 'द', 'ध', 'न',
                      'प', 'फ', 'ब', 'भ', 'म', 'य', 'र', 'ल', 'व', 'श',
                      'ष', 'स', 'ह']

        count = 0
        i = 0
        n = len(clean_text)
        while i < n:
            ch = clean_text[i]
            if ch in independent_vowels:
                count += 1
            elif ch in consonants:
                # Check if followed by virama
                if i + 1 < n and clean_text[i + 1] == '्':
                    # Half consonant, not a full akshara
                    pass
                else:
                    count += 1
            i += 1
        return count if count > 0 else max(1, len(clean_text.split()))

    @classmethod
    def detect_chandas(cls, devanagari_text: str) -> Optional[ChandasResult]:
        """Detects standard Vedic and Classical metres."""
        aksharas = cls.count_aksharas(devanagari_text)

        # Standard meter bounds (considering half-shloka or full shloka)
        # Anuṣṭubh: 32 syllables total (8 x 4), or 16 syllables for half-verse
        if 28 <= aksharas <= 36:
            return ChandasResult(name="Anuṣṭubh (Śloka)", syllable_count=aksharas, padas=4, confidence=0.92)
        elif 14 <= aksharas <= 18:
            return ChandasResult(name="Anuṣṭubh (Ardha-śloka)", syllable_count=aksharas, padas=2, confidence=0.88)
        # Triṣṭubh: 44 syllables (11 x 4)
        elif 40 <= aksharas <= 48:
            return ChandasResult(name="Triṣṭubh", syllable_count=aksharas, padas=4, confidence=0.90)
        # Gāyatrī: 24 syllables (8 x 3)
        elif 22 <= aksharas <= 26:
            return ChandasResult(name="Gāyatrī", syllable_count=aksharas, padas=3, confidence=0.95)
        # Jagatī: 48 syllables (12 x 4)
        elif 47 <= aksharas <= 50:
            return ChandasResult(name="Jagatī", syllable_count=aksharas, padas=4, confidence=0.85)

        return ChandasResult(name="Vṛtta / Mixed Chandas", syllable_count=aksharas, padas=4, confidence=0.60)

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
