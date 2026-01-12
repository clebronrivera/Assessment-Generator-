"""
Bank 3: Comprehension Passage Word Count by Grade
Defines average word counts and allowed ranges for comprehension assessments.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ComprehensionWordCount:
    """
    Word count specifications for comprehension passages at a specific grade.
    
    Attributes:
        grade: Grade level (K, 1-8, 8+)
        average: Target average word count
        min_allowed: Minimum allowed word count (average - 10%)
        max_allowed: Maximum allowed word count (average + 10%)
        rationale: Brief explanation of word count choice
    """
    grade: str
    average: int
    min_allowed: int
    max_allowed: int
    rationale: str = ""
    
    def __str__(self) -> str:
        return f"Grade {self.grade}: {self.average} words (range: {self.min_allowed}-{self.max_allowed})"
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON export."""
        return {
            "grade": self.grade,
            "average_word_count": self.average,
            "allowed_range": f"{self.min_allowed}-{self.max_allowed}",
            "min_allowed": self.min_allowed,
            "max_allowed": self.max_allowed,
            "rationale": self.rationale
        }
    
    def is_valid(self, word_count: int) -> bool:
        """Check if a word count falls within allowed range."""
        return self.min_allowed <= word_count <= self.max_allowed


# COMPREHENSION WORD COUNT BANK DATA
# Rule: Average ±10% to allow narrative variation while maintaining consistency
COMP_BANK = [
    # Kindergarten: Listening comprehension, very short
    ComprehensionWordCount(
        grade="K",
        average=50,
        min_allowed=40,
        max_allowed=60,
        rationale="Listening comprehension, single picture support, attention span"
    ),
    
    # Grade 1: Listening comprehension, still short
    ComprehensionWordCount(
        grade="1",
        average=75,
        min_allowed=65,
        max_allowed=85,
        rationale="Listening comprehension, developing vocabulary"
    ),
    
    # Grade 2: First independent reading comprehension
    ComprehensionWordCount(
        grade="2",
        average=125,
        min_allowed=110,
        max_allowed=140,
        rationale="First independent comprehension grade"
    ),
    
    # Grade 3: Balanced explicit and implicit questions
    ComprehensionWordCount(
        grade="3",
        average=175,
        min_allowed=155,
        max_allowed=195,
        rationale="Supports balanced explicit and implicit questions"
    ),
    
    # Grade 4: Vocabulary and main idea items introduced
    ComprehensionWordCount(
        grade="4",
        average=225,
        min_allowed=200,
        max_allowed=250,
        rationale="Introduces vocabulary and main idea items"
    ),
    
    # Grade 5: Multi-question comprehension sets
    ComprehensionWordCount(
        grade="5",
        average=275,
        min_allowed=245,
        max_allowed=305,
        rationale="Sustains multi-question comprehension sets"
    ),
    
    # Grade 6: Text features and structure
    ComprehensionWordCount(
        grade="6",
        average=325,
        min_allowed=290,
        max_allowed=360,
        rationale="Supports text features and structure"
    ),
    
    # Grade 7: Inference across paragraphs
    ComprehensionWordCount(
        grade="7",
        average=375,
        min_allowed=335,
        max_allowed=415,
        rationale="Enables inference across paragraphs"
    ),
    
    # Grade 8: Complex reasoning and multiple inferences
    ComprehensionWordCount(
        grade="8",
        average=425,
        min_allowed=380,
        max_allowed=470,
        rationale="Complex reasoning and multiple inference items"
    ),
    
    # Grade 8+ (High School): Secondary-level comprehension
    ComprehensionWordCount(
        grade="8+",
        average=500,
        min_allowed=450,
        max_allowed=550,
        rationale="Secondary-level comprehension and analysis"
    ),
]


# Create lookup dictionary
_COMP_LOOKUP = {wc.grade: wc for wc in COMP_BANK}


def get_comp_word_count(grade: str) -> Optional[ComprehensionWordCount]:
    """
    Get word count specifications for a specific grade.
    
    Args:
        grade: Grade level (K, 1-8, 8+)
    
    Returns:
        ComprehensionWordCount object or None if grade not found
    
    Example:
        >>> specs = get_comp_word_count("3")
        >>> print(specs.average)
        175
    """
    return _COMP_LOOKUP.get(grade)


def get_target_word_count(grade: str) -> Optional[int]:
    """
    Get target (average) word count for a grade.
    
    Args:
        grade: Grade level (K, 1-8, 8+)
    
    Returns:
        Average word count as integer or None if grade not found
    """
    specs = get_comp_word_count(grade)
    return specs.average if specs else None


def get_allowed_range(grade: str) -> Optional[tuple[int, int]]:
    """
    Get allowed word count range for a grade.
    
    Args:
        grade: Grade level (K, 1-8, 8+)
    
    Returns:
        Tuple of (min, max) or None if grade not found
    
    Example:
        >>> get_allowed_range("2")
        (110, 140)
    """
    specs = get_comp_word_count(grade)
    return (specs.min_allowed, specs.max_allowed) if specs else None


def validate_word_count(grade: str, word_count: int) -> bool:
    """
    Validate that a word count falls within acceptable range for the grade.
    
    Args:
        grade: Grade level (K, 1-8, 8+)
        word_count: Actual word count to validate
    
    Returns:
        True if within acceptable range, False otherwise
    
    Example:
        >>> validate_word_count("3", 180)
        True
        >>> validate_word_count("3", 200)  # Outside range
        False
    """
    specs = get_comp_word_count(grade)
    if not specs:
        return False
    
    return specs.is_valid(word_count)


def get_comp_grades() -> list[str]:
    """Get list of all grades with comprehension assessments (K-8+)."""
    return ["K", "1", "2", "3", "4", "5", "6", "7", "8", "8+"]


def export_to_json() -> list[dict]:
    """
    Export entire comprehension word count bank to JSON-serializable format.
    
    Returns:
        List of dictionaries representing all word count specifications
    """
    return [wc.to_dict() for wc in COMP_BANK]


# Validation on module load
def _validate_bank():
    """Internal validation to ensure bank integrity."""
    # Check all grades K-8+ present
    expected_grades = {"K", "1", "2", "3", "4", "5", "6", "7", "8", "8+"}
    found_grades = {wc.grade for wc in COMP_BANK}
    
    assert found_grades == expected_grades, f"Missing grades: {expected_grades - found_grades}"
    
    # Check word counts are increasing (except K and 8+ which are special)
    prev_count = 0
    for wc in COMP_BANK:
        if wc.grade not in ["K", "8+"]:
            assert wc.average > prev_count, \
                f"Grade {wc.grade} word count not increasing"
        prev_count = wc.average
    
    # Check ranges are ±10% of average
    for wc in COMP_BANK:
        expected_min = int(wc.average * 0.9)
        expected_max = int(wc.average * 1.1)
        assert abs(wc.min_allowed - expected_min) <= 5, \
            f"Grade {wc.grade} min not ~10% below average"
        assert abs(wc.max_allowed - expected_max) <= 5, \
            f"Grade {wc.grade} max not ~10% above average"
    
    print("✓ Bank 3 (Comprehension Word Counts) validated successfully")


if __name__ == "__main__":
    # Run validation
    _validate_bank()
    
    # Print sample data
    print("\nSample Comprehension Word Counts:")
    for grade in ["K", "2", "5", "8+"]:
        specs = get_comp_word_count(grade)
        print(f"  {specs}")
    
    # Test validation
    print("\nValidation Tests:")
    print(f"  Grade 2, 125 words (target): {validate_word_count('2', 125)}")
    print(f"  Grade 2, 150 words (too high): {validate_word_count('2', 150)}")
    
    # Export sample
    import json
    print("\nJSON Export Sample:")
    print(json.dumps(export_to_json()[:3], indent=2))
