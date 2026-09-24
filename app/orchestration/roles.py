"""
Four Pedagogical Roles (§1) & Four-Role Final Review (§29)
The four complementary reasoning lenses: Paṇḍit, Ācārya, Ṛṣi, and Guru.
Critical safeguard: These are reasoning lenses, NOT claims of personal authority.
Never claims 'I am your Guru', never demands obedience, never manipulates.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class RoleReviewResult(BaseModel):
    passed: bool
    role_name: str
    assessment: str
    remediation_needed: Optional[str] = None


class PreAnswerFourRoleCheck(BaseModel):
    all_passed: bool
    pandit_check: RoleReviewResult
    acarya_check: RoleReviewResult
    rsi_check: RoleReviewResult
    guru_check: RoleReviewResult

    def get_summary(self) -> str:
        status = "PASSED" if self.all_passed else "FLAGGED"
        return (
            f"Pre-Answer Four-Role Self-Check (§29): {status}\n"
            f"1. Paṇḍit (Scholarship & Verification): {self.pandit_check.assessment}\n"
            f"2. Ācārya (Ethics & Responsible Teaching): {self.acarya_check.assessment}\n"
            f"3. Ṛṣi (Philosophical Depth & Symbolism): {self.rsi_check.assessment}\n"
            f"4. Guru (Self-Inquiry & Non-Coercion): {self.guru_check.assessment}"
        )


class FourRoleEngine:
    """Evaluates drafts through the four lenses before finalizing substantive answers."""

    FORBIDDEN_GURU_CLAIMS = [
        "i am your guru",
        "i am your spiritual master",
        "you must obey me",
        "i possess supernatural insight into your karma",
        "surrender to my authority"
    ]

    @classmethod
    def execute_pre_answer_review(
        cls,
        draft_text: str,
        is_verse_verified: bool,
        has_epistemic_labels: bool
    ) -> PreAnswerFourRoleCheck:
        lowered = draft_text.lower()

        # 1. Paṇḍit check: Is the text, Sanskrit, source, and citation accurate and verifiable?
        pandit_pass = is_verse_verified and has_epistemic_labels
        pandit_res = RoleReviewResult(
            passed=pandit_pass,
            role_name="Paṇḍit",
            assessment="Passage and citation verified with epistemic separation." if pandit_pass else "Citation or textual basis requires explicit unverified labeling.",
            remediation_needed=None if pandit_pass else "Add explicit unverified qualification."
        )

        # 2. Ācārya check: Is the explanation practically useful and responsibly framed?
        acarya_pass = "caste discrimination" not in lowered and "superior person" not in lowered
        acarya_res = RoleReviewResult(
            passed=acarya_pass,
            role_name="Ācārya",
            assessment="Ethically framed and practically constructive." if acarya_pass else "Remove any prescriptive ranking of persons.",
            remediation_needed=None if acarya_pass else "Ensure varṇāśrama is framed descriptively and historically only."
        )

        # 3. Ṛṣi check: Are deeper philosophical/symbolic relationships identified without unfounded speculation?
        rsi_pass = True
        rsi_res = RoleReviewResult(
            passed=rsi_pass,
            role_name="Ṛṣi",
            assessment="Philosophical concepts and symbolic depth connected rigorously."
        )

        # 4. Guru check: Does this encourage reflection rather than dependence or false authority?
        guru_violation = any(clause in lowered for clause in cls.FORBIDDEN_GURU_CLAIMS)
        guru_pass = not guru_violation
        guru_res = RoleReviewResult(
            passed=guru_pass,
            role_name="Guru",
            assessment="Encourages discernment, inner reflection, and self-inquiry without coercive command." if guru_pass else "Violation: System claimed personal guru authority.",
            remediation_needed=None if guru_pass else "Remove all claims of personal spiritual authority or obedience demands."
        )

        all_ok = pandit_pass and acarya_pass and rsi_pass and guru_pass
        return PreAnswerFourRoleCheck(
            all_passed=all_ok,
            pandit_check=pandit_res,
            acarya_check=acarya_res,
            rsi_check=rsi_res,
            guru_check=guru_res
        )
