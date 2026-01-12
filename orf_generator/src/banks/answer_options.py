"""
Bank 6: Answer Option Standards by Grade
Defines number of answer options for multiple choice questions by grade band.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class AnswerOptionStandard:
    """
    Answer option specifications for a grade band.
    
    Attributes:
        grade_band: Grade range (e.g., "K-1", "2-3", "4-8+")
        num_options: Number of answer choices
        distractor_quality: Description of distractor requirements
        notes: Additional guidance
    """
    grade_band: str
    num_options: int
    distractor_quality: str
    notes: str = ""
    
    def __str__(self) -> str:
        return f"{self.grade_band}: {self.num_options} options ({self.distractor_quality})"
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON export."""
        return {
            "grade_band": self.grade_band,
            "num_options": self.num_options,
            "distractor_quality": self.distractor_quality,
            "notes": self.notes
        }


# ANSWER OPTION STANDARDS BANK DATA
ANSWER_OPTION_BANK = [
    AnswerOptionStandard(
        grade_band="K-1",
        num_options=2,
        distractor_quality="One clearly correct, one clearly incorrect",
        notes="Can use picture-supported options for K; text only for grade 1"
    ),
    AnswerOptionStandard(
        grade_band="2-3",
        num_options=3,
        distractor_quality="Plausible distractors based on common misunderstandings",
        notes="Distractors should be text-based and plausible but clearly incorrect"
    ),
    AnswerOptionStandard(
        grade_band="4-8+",
        num_options=4,
        distractor_quality="Three plausible distractors, one best answer",
        notes="All options should be plausible; distractors reflect common errors"
    ),
]


def get_num_options(grade: str) -> int:
    """
    Get number of answer options for a specific grade.
    
    Args:
        grade: Grade level (K, 1-8, 8+)
    
    Returns:
        Number of answer options (2, 3, or 4)
    
    Example:
        >>> get_num_options("K")
        2
        >>> get_num_options("5")
        4
    """
    # Map grade to band
    if grade in ["K", "1"]:
        return 2
    elif grade in ["2", "3"]:
        return 3
    else:  # 4, 5, 6, 7, 8, 8+
        return 4


def get_option_standard(grade: str) -> Optional[AnswerOptionStandard]:
    """
    Get full answer option standard for a grade.
    
    Args:
        grade: Grade level (K, 1-8, 8+)
    
    Returns:
        AnswerOptionStandard object or None if grade not found
    """
    if grade in ["K", "1"]:
        return ANSWER_OPTION_BANK[0]
    elif grade in ["2", "3"]:
        return ANSWER_OPTION_BANK[1]
    elif grade in ["4", "5", "6", "7", "8", "8+"]:
        return ANSWER_OPTION_BANK[2]
    return None


def get_distractor_guidance(grade: str) -> str:
    """
    Get distractor quality guidance for a grade.
    
    Args:
        grade: Grade level (K, 1-8, 8+)
    
    Returns:
        Distractor quality description string
    """
    standard = get_option_standard(grade)
    return standard.distractor_quality if standard else ""


def validate_option_count(grade: str, num_provided: int) -> bool:
    """
    Validate that provided number of options matches grade standard.
    
    Args:
        grade: Grade level
        num_provided: Number of options provided in question
    
    Returns:
        True if matches standard, False otherwise
    """
    expected = get_num_options(grade)
    return num_provided == expected


def export_to_json() -> list[dict]:
    """
    Export entire answer option bank to JSON-serializable format.
    
    Returns:
        List of dictionaries representing all answer option standards
    """
    return [standard.to_dict() for standard in ANSWER_OPTION_BANK]


# Validation on module load
def _validate_bank():
    """Internal validation to ensure bank integrity."""
    # Check all grade bands present
    expected_bands = {"K-1", "2-3", "4-8+"}
    found_bands = {standard.grade_band for standard in ANSWER_OPTION_BANK}
    assert found_bands == expected_bands, f"Missing grade bands: {expected_bands - found_bands}"
    
    # Check option counts are increasing
    prev_count = 0
    for standard in ANSWER_OPTION_BANK:
        assert standard.num_options > prev_count, \
            f"Band {standard.grade_band} option count not increasing"
        prev_count = standard.num_options
    
    # Check specific grades
    assert get_num_options("K") == 2, "K should have 2 options"
    assert get_num_options("2") == 3, "Grade 2 should have 3 options"
    assert get_num_options("5") == 4, "Grade 5 should have 4 options"
    assert get_num_options("8+") == 4, "Grade 8+ should have 4 options"
    
    print("✓ Bank 6 (Answer Options) validated successfully")


if __name__ == "__main__":
    # Run validation
    _validate_bank()
    
    # Print all standards
    print("\nAnswer Option Standards:")
    for standard in ANSWER_OPTION_BANK:
        print(f"  {standard}")
    
    # Test lookups
    print("\nSample Lookups:")
    for grade in ["K", "2", "5", "8+"]:
        num = get_num_options(grade)
        guidance = get_distractor_guidance(grade)
        print(f"  Grade {grade}: {num} options")
        print(f"    Distractor guidance: {guidance}")
    
    # Export
    import json
    print("\nJSON Export:")
    print(json.dumps(export_to_json(), indent=2))
