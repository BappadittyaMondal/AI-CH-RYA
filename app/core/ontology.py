"""
Knowledge Ontology (§4) - Formal Universe of Coverage
"""

from enum import Enum
from typing import List, Optional, Set
from pydantic import BaseModel, Field


class TextType(str, Enum):
    SRUTI = "ŚRUTI"
    VEDANGA = "VEDĀṄGA"
    KALPA_SUTRA = "KALPA-SŪTRA"
    SMRTI_DHARMA = "SMṚTI/DHARMA"
    ITIHASA = "ITIHĀSA"
    PURANA = "PURĀṆA"
    AGAMA_TANTRA = "ĀGAMA/TANTRA"
    DARSANA = "DARŚANA"
    COMMENTARY = "COMMENTARY"
    NIBANDHA = "NIBANDHA"
    STOTRA_KAVYA = "STOTRA/KĀVYA"
    SAMPRADAYA = "SAMPRADĀYA"
    REGIONAL_TRAD = "REGIONAL_TRAD"
    ORAL_TRADITION = "ORAL_TRADITION"
    HISTORICAL_SRC = "HISTORICAL_SRC"
    MODERN_SCHOLAR = "MODERN_SCHOLAR"
    MODERN_INTERP = "MODERN_INTERP"
    USER_SOURCE = "USER_SOURCE"


# The 13 Mukhya (Principal) Upaniṣads as the primary scholarly core
MUKHYA_UPANISADS: Set[str] = {
    "Īśā",
    "Kena",
    "Kaṭha",
    "Praśna",
    "Muṇḍaka",
    "Māṇḍūkya",
    "Taittirīya",
    "Aitareya",
    "Chāndogya",
    "Bṛhadāraṇyaka",
    "Śvetāśvatara",
    "Kauṣītaki",
    "Maitrāyaṇīya",
}

# The 6 Vedāṅgas
VEDANGAS: List[str] = [
    "Śikṣā (Phonetics/Pronunciation)",
    "Vyākaraṇa (Grammar)",
    "Chandas (Metre/Prosody)",
    "Nirukta (Etymology)",
    "Kalpa (Ritual/Ethics)",
    "Jyotiṣa (Astronomy/Time-keeping)",
]

# The 6 Orthodox Darśanas (Ṣaḍ-darśana)
SAD_DARSANAS: List[str] = [
    "Nyāya",
    "Vaiśeṣika",
    "Sāṃkhya",
    "Yoga",
    "Mīmāṃsā",
    "Vedānta",
]

# The 18 Mahāpurāṇas
MAHAPURANAS: List[str] = [
    "Brahmā",
    "Padma",
    "Viṣṇu",
    "Śiva",
    "Bhāgavata",
    "Nārada",
    "Mārkaṇḍeya",
    "Agni",
    "Bhaviṣya",
    "Brahma Vaivarta",
    "Liṅga",
    "Varāha",
    "Skanda",
    "Vāmana",
    "Kūrma",
    "Matsya",
    "Garuḍa",
    "Brahmāṇḍa",
]


class TextEntity(BaseModel):
    id: str = Field(..., description="Unique text identifier, e.g. BG, ISHA, RV")
    title: str = Field(..., description="Standard title of the text in IAST and Devanagari")
    text_type: TextType = Field(..., description="Ontology classification")
    tradition: Optional[str] = None
    sakha_recension: Optional[str] = None
    is_mukhya: bool = False
    description: Optional[str] = None

    def validate_authority_hierarchy(self) -> int:
        """
        Returns numeric authority rank for retrieval prioritization:
        Śruti (1) > Vedāṅga/Kalpa (2) > Smṛti/Itihāsa/Purāṇa (3) > Darśana/Commentary (4) > Modern (5)
        """
        hierarchy = {
            TextType.SRUTI: 1,
            TextType.VEDANGA: 2,
            TextType.KALPA_SUTRA: 2,
            TextType.SMRTI_DHARMA: 3,
            TextType.ITIHASA: 3,
            TextType.PURANA: 3,
            TextType.AGAMA_TANTRA: 3,
            TextType.DARSANA: 4,
            TextType.COMMENTARY: 4,
            TextType.NIBANDHA: 4,
            TextType.STOTRA_KAVYA: 5,
            TextType.SAMPRADAYA: 5,
            TextType.REGIONAL_TRAD: 6,
            TextType.ORAL_TRADITION: 6,
            TextType.HISTORICAL_SRC: 7,
            TextType.MODERN_SCHOLAR: 8,
            TextType.MODERN_INTERP: 9,
            TextType.USER_SOURCE: 10,
        }
        return hierarchy.get(self.text_type, 99)
