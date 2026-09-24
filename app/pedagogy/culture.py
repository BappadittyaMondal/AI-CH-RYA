"""
Culture Explainer (§23)
Explains cultural customs (e.g. touching elders' feet, Tulsi, Om, Namaste)
by strictly demarcating Scriptural, Oral, Historical, Regional, Symbolic, and Modern Scientific layers.
"""

from typing import Optional
from pydantic import BaseModel


class CultureExplanation(BaseModel):
    custom_name: str
    scriptural_basis: str
    traditional_oral_explanation: str
    historical_evidence: Optional[str] = None
    regional_variations: str
    symbolic_interpretation: str
    modern_scientific_discussion: Optional[str] = None

    def format_structured_explanation(self) -> str:
        parts = [
            f"### Cultural Explainer: {self.custom_name}\n",
            f"**1. Scriptural Basis:**\n{self.scriptural_basis}\n",
            f"**2. Traditional & Oral Teaching:**\n{self.traditional_oral_explanation}\n",
        ]
        if self.historical_evidence:
            parts.append(f"**3. Historical & Epigraphic Context:**\n{self.historical_evidence}\n")
        parts.append(f"**4. Regional Variations:**\n{self.regional_variations}\n")
        parts.append(f"**5. Symbolic & Philosophical Interpretation:**\n{self.symbolic_interpretation}\n")
        if self.modern_scientific_discussion:
            parts.append(
                f"**6. Modern Empirical Discussion (Separate Lens):**\n{self.modern_scientific_discussion}\n"
            )
        return "\n".join(parts)


class CultureExplainerService:
    @classmethod
    def explain_touching_feet(cls) -> CultureExplanation:
        return CultureExplanation(
            custom_name="Caraṇa-sparśa (Touching Elders' Feet / Praṇāma)",
            scriptural_basis="Described in Manusmṛti 2.120-121 and Taittirīya Upaniṣad ('mātṛdevo bhava, pitṛdevo bhava') as part of abhivādana (reverential greeting).",
            traditional_oral_explanation="Expresses surrender of ego (ahaṅkāra), humility, and seeking the auspicious blessings (āśīrvāda) of elders and teachers.",
            historical_evidence="Inscriptions and classical literature (e.g. Mahābhārata, Harṣacarita) attest to praṇāma as standard civilizational etiquette.",
            regional_variations="Varies across India: in Bengal and the North, touching feet with both hands crossed; in parts of Maharashtra, touching feet with palms; in the South, often full saṣṭāṅga praṇāma in temple contexts.",
            symbolic_interpretation="The feet symbolize the contact point with the earth; bowing low humbles the highest organ (head/intellect) below the elder's lowest point, dissolving arrogance.",
            modern_scientific_discussion="Psychological and behavioral research highlights the prosocial reinforcement of gratitude, humility, and intergenerational social cohesion."
        )
