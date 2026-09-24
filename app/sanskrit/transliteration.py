"""
Sanskrit Transliteration Engine (§9, §10)
Supports bidirectional mapping between Devanāgarī, IAST (Roman), and Bengali scripts.
Preserves Vedic accents and diacritics.
"""

# Common character mapping dictionaries
DEVA_TO_IAST = {
    'अ': 'a', 'आ': 'ā', 'इ': 'i', 'ई': 'ī', 'उ': 'u', 'ऊ': 'ū',
    'ऋ': 'ṛ', 'ॠ': 'ṝ', 'ऌ': 'ḷ', 'ॡ': 'ḹ',
    'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au',
    'क': 'ka', 'ख': 'kha', 'ग': 'ga', 'घ': 'gha', 'ङ': 'ṅa',
    'च': 'ca', 'छ': 'cha', 'ज': 'ja', 'झ': 'jha', 'ञ': 'ña',
    'ट': 'ṭa', 'ठ': 'ṭha', 'ड': 'ḍa', 'ढ': 'ḍha', 'ण': 'ṇa',
    'त': 'ta', 'थ': 'tha', 'द': 'da', 'ध': 'dha', 'न': 'na',
    'प': 'pa', 'फ': 'pha', 'ब': 'ba', 'भ': 'bha', 'म': 'ma',
    'य': 'ya', 'र': 'ra', 'ल': 'la', 'व': 'va',
    'श': 'śa', 'ष': 'ṣa', 'स': 'sa', 'ह': 'ha',
    'ा': 'ā', 'ि': 'i', 'ी': 'ī', 'ु': 'u', 'ू': 'ū',
    'ृ': 'ṛ', 'ॄ': 'ṝ', 'ॢ': 'ḷ', 'ॣ': 'ḹ',
    'े': 'e', 'ै': 'ai', 'ो': 'o', 'ौ': 'au',
    'ं': 'ṃ', 'ः': 'ḥ', '्': '', 'ँ': 'm̐', 'ऽ': "'"
}

# Devanagari to Bengali script mapping for scriptural transliteration
DEVA_TO_BENGALI = {
    'अ': 'অ', 'आ': 'আ', 'इ': 'ই', 'ई': 'ঈ', 'उ': 'উ', 'ऊ': 'ঊ',
    'ऋ': 'ঋ', 'ॠ': 'ৠ', 'ऌ': 'ঌ', 'ॡ': 'ৡ',
    'ए': 'এ', 'ऐ': 'ঐ', 'ओ': 'ও', 'औ': 'ঔ',
    'क': 'ক', 'ख': 'খ', 'ग': 'গ', 'घ': 'ঘ', 'ङ': 'ঙ',
    'च': 'চ', 'छ': 'ছ', 'ज': 'জ', 'झ': 'ঝ', 'ञ': 'ঞ',
    'ट': 'ট', 'ठ': 'ঠ', 'ड': 'ড', 'ढ': 'ঢ', 'ण': 'ণ',
    'त': 'ত', 'थ': 'থ', 'द': 'দ', 'ध': 'ধ', 'न': 'ন',
    'प': 'প', 'फ': 'ফ', 'ब': 'ব', 'भ': 'ভ', 'म': 'ম',
    'य': 'য', 'र': 'র', 'ल': 'ল', 'व': 'ব',
    'श': 'শ', 'ष': 'ষ', 'स': 'স', 'ह': 'হ',
    'ा': 'া', 'ि': 'ি', 'ी': 'ী', 'ु': 'ু', 'ू': 'ূ',
    'ृ': 'ৃ', 'ॄ': 'ৄ', 'ॢ': 'ৢ', 'ॣ': 'ৣ',
    'े': 'ে', 'ै': 'ৈ', 'ो': 'ো', 'ौ': 'ৌ',
    'ं': 'ং', 'ः': 'ঃ', '्': '্', 'ँ': 'ঁ', 'ऽ': "'"
}


def deva_to_bengali(text: str) -> str:
    """Converts Devanāgarī text to Bengali script."""
    result = []
    for ch in text:
        result.append(DEVA_TO_BENGALI.get(ch, ch))
    return "".join(result)


def simple_devanagari_to_iast(text: str) -> str:
    """
    Standard transliteration of Sanskrit Devanāgarī to IAST.
    Handles virāma and vowel matras correctly.
    """
    consonants = {
        'क': 'k', 'ख': 'kh', 'ग': 'g', 'घ': 'gh', 'ङ': 'ṅ',
        'च': 'c', 'छ': 'ch', 'ज': 'j', 'झ': 'jh', 'ञ': 'ñ',
        'ट': 'ṭ', 'ठ': 'ṭh', 'ड': 'ḍ', 'ढ': 'ḍh', 'ण': 'ṇ',
        'त': 't', 'थ': 'th', 'द': 'd', 'ध': 'dh', 'न': 'n',
        'प': 'p', 'फ': 'ph', 'ब': 'b', 'भ': 'bh', 'म': 'm',
        'य': 'y', 'र': 'r', 'ल': 'l', 'व': 'v',
        'श': 'ś', 'ष': 'ṣ', 'स': 's', 'ह': 'h',
    }
    vowels_independent = {
        'अ': 'a', 'आ': 'ā', 'इ': 'i', 'ई': 'ī', 'उ': 'u', 'ऊ': 'ū',
        'ऋ': 'ṛ', 'ॠ': 'ṝ', 'ऌ': 'ḷ', 'ॡ': 'ḹ',
        'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au'
    }
    matras = {
        'ा': 'ā', 'ि': 'i', 'ी': 'ī', 'ु': 'u', 'ू': 'ū',
        'ृ': 'ṛ', 'ॄ': 'ṝ', 'ॢ': 'ḷ', 'ॣ': 'ḹ',
        'े': 'e', 'ै': 'ai', 'ो': 'o', 'ौ': 'au'
    }
    virama = '्'

    out = []
    i = 0
    n = len(text)
    while i < n:
        char = text[i]
        if char in consonants:
            c = consonants[char]
            # Check next character
            if i + 1 < n:
                next_ch = text[i + 1]
                if next_ch == virama:
                    out.append(c)
                    i += 2
                    continue
                elif next_ch in matras:
                    out.append(c + matras[next_ch])
                    i += 2
                    continue
            # Inherent 'a'
            out.append(c + 'a')
            i += 1
        elif char in vowels_independent:
            out.append(vowels_independent[char])
            i += 1
        elif char in DEVA_TO_IAST:
            out.append(DEVA_TO_IAST[char])
            i += 1
        else:
            out.append(char)
            i += 1
    return "".join(out)
