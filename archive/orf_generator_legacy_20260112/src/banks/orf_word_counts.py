"""
Bank 2: ORF (Oral Reading Fluency) Word Count Targets by Grade
Based on Hasbrouck & Tindal (2017) Spring 75th percentile WCPM + 10
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ORFTargets:
    """
    Oral Reading Fluency targets for a specific grade.
    
    Attributes:
        grade: Grade level (1-8)
        spring_wcpm_50th: Spring Words Correct Per Minute at 50th percentile
        spring_wcpm_75th: Spring Words Correct Per Minute at 75th percentile
        target_word_count: Recommended passage word count (prevents ceiling effects)
        basis: Source of WCPM data
    """
    grade: str
    spring_wcpm_50th: int
    spring_wcpm_75th: int
    target_word_count: int
    basis: str = "Hasbrouck & Tindal 2017"
    
    def __str__(self) -> str:
        return (f"Grade {self.grade}: Target {self.target_word_count} words "
                f"(WCPM 50th: {self.spring_wcpm_50th}, 75th: {self.spring_wcpm_75th})")
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON export."""
        return {
            "grade": self.grade,
            "spring_wcpm_50th": self.spring_wcpm_50th,
            "spring_wcpm_75th": self.spring_wcpm_75th,
            "target_word_count": self.target_word_count,
            "basis": self.basis
        }
    
    @property
    def min_word_count(self) -> int:
        """Minimum allowed word count (target - 2)."""
        return self.target_word_count - 2
    
    @property
    def max_word_count(self) -> int:
        """Maximum allowed word count (target + 2)."""
        return self.target_word_count + 2


# ORF WORD COUNT BANK DATA
# Rule: Target = (Spring 75th percentile WCPM + 10), rounded to next multiple of 10
ORF_BANK = [
    # Grade 1: 91 + 10 = 101 → 110
    ORFTargets("1", spring_wcpm_50th=60, spring_wcpm_75th=91, target_word_count=110),
    
    # Grade 2: 124 + 10 = 134 → 140
    ORFTargets("2", spring_wcpm_50th=100, spring_wcpm_75th=124, target_word_count=140),
    
    # Grade 3: 139 + 10 = 149 → 150
    ORFTargets("3", spring_wcpm_50th=112, spring_wcpm_75th=139, target_word_count=150),
    
    # Grade 4: 160 + 10 = 170 → 170
    ORFTargets("4", spring_wcpm_50th=133, spring_wcpm_75th=160, target_word_count=170),
    
    # Grade 5: 169 + 10 = 179 → 180
    ORFTargets("5", spring_wcpm_50th=146, spring_wcpm_75th=169, target_word_count=180),
    
    # Grade 6: 173 + 10 = 183 → 190
    ORFTargets("6", spring_wcpm_50th=146, spring_wcpm_75th=173, target_word_count=190),
    
    # Grade 7: Estimated based on progression → 200
    ORFTargets("7", spring_wcpm_50th=150, spring_wcpm_75th=180, target_word_count=200),
    
    # Grade 8: Estimated based on progression → 210
    ORFTargets("8", spring_wcpm_50th=155, spring_wcpm_75th=185, target_word_count=210),
]


# Create lookup dictionary
_ORF_LOOKUP = {target.grade: target for target in ORF_BANK}


def get_orf_target(grade: str) -> Optional[ORFTargets]:
    """
    Get ORF targets for a specific grade.
    
    Args:
        grade: Grade level (1-8)
    
    Returns:
        ORFTargets object or None if grade not found
    
    Example:
        >>> targets = get_orf_target("2")
        >>> print(targets.target_word_count)
        140
    """
    return _ORF_LOOKUP.get(grade)


def get_target_word_count(grade: str) -> Optional[int]:
    """
    Get target word count for a grade.
    
    Args:
        grade: Grade level (1-8)
    
    Returns:
        Target word count as integer or None if grade not found
    """
    targets = get_orf_target(grade)
    return targets.target_word_count if targets else None


def validate_word_count(grade: str, word_count: int) -> bool:
    """
    Validate that a word count falls within acceptable range (±2 words).
    
    Args:
        grade: Grade level (1-8)
        word_count: Actual word count to validate
    
    Returns:
        True if within acceptable range, False otherwise
    
    Example:
        >>> validate_word_count("2", 141)  # 140 target, ±2 allowed
        True
        >>> validate_word_count("2", 145)  # Outside range
        False
    """
    targets = get_orf_target(grade)
    if not targets:
        return False
    
    return targets.min_word_count <= word_count <= targets.max_word_count


def get_wcpm_benchmarks(grade: str) -> Optional[dict]:
    """
    Get WCPM benchmarks for comparison/scoring.
    
    Args:
        grade: Grade level (1-8)
    
    Returns:
        Dictionary with 50th and 75th percentile WCPM values
    """
    targets = get_orf_target(grade)
    if not targets:
        return None
    
    return {
        "50th_percentile": targets.spring_wcpm_50th,
        "75th_percentile": targets.spring_wcpm_75th,
        "grade": grade
    }


def get_orf_grades() -> list[str]:
    """Get list of all grades with ORF assessments (1-8)."""
    return ["1", "2", "3", "4", "5", "6", "7", "8"]


def export_to_json() -> list[dict]:
    """
    Export entire ORF bank to JSON-serializable format.
    
    Returns:
        List of dictionaries representing all ORF targets
    """
    return [target.to_dict() for target in ORF_BANK]


# Validation on module load
def _validate_bank():
    """Internal validation to ensure bank integrity."""
    # Check all grades 1-8 present
    expected_grades = {"1", "2", "3", "4", "5", "6", "7", "8"}
    found_grades = {target.grade for target in ORF_BANK}
    
    assert found_grades == expected_grades, f"Missing ORF grades: {expected_grades - found_grades}"
    
    # Check word counts are reasonable and increasing
    prev_count = 0
    for target in ORF_BANK:
        assert target.target_word_count > prev_count, \
            f"Grade {target.grade} word count not increasing"
        assert target.target_word_count % 10 == 0, \
            f"Grade {target.grade} word count not multiple of 10"
        prev_count = target.target_word_count
    
    print("✓ Bank 2 (ORF Word Counts) validated successfully")


if __name__ == "__main__":
    # Run validation
    _validate_bank()
    
    # Print sample data
    print("\nSample ORF Targets:")
    for grade in ["1", "2", "3"]:
        targets = get_orf_target(grade)
        print(f"  {targets}")
        print(f"    Acceptable range: {targets.min_word_count}-{targets.max_word_count} words")
    
    # Export sample
    import json
    print("\nJSON Export Sample:")
    print(json.dumps(export_to_json()[:3], indent=2))
