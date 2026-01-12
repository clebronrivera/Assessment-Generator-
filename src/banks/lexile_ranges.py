"""
Bank 1: Lexile Readability Grade Band Bank
Defines Lexile ranges for passage targeting with Early/Late sub-bands per grade.
"""

from dataclasses import dataclass
from typing import Literal, Optional
from enum import Enum


class GradeLevel(str, Enum):
    """Valid grade levels for the system."""
    K = "K"
    GRADE_1 = "1"
    GRADE_2 = "2"
    GRADE_3 = "3"
    GRADE_4 = "4"
    GRADE_5 = "5"
    GRADE_6 = "6"
    GRADE_7 = "7"
    GRADE_8 = "8"
    GRADE_8_PLUS = "8+"


class LexileBand(str, Enum):
    """Valid Lexile bands (Early or Late)."""
    EARLY = "early"
    LATE = "late"


@dataclass(frozen=True)
class LexileRange:
    """
    Represents a Lexile range for a specific grade and band.
    
    Attributes:
        grade: Grade level (K, 1-8, 8+)
        band: Sub-band (early or late)
        lexile_min: Minimum Lexile value (e.g., "BR310L", "245L")
        lexile_max: Maximum Lexile value (e.g., "BR160L", "605L")
        basis: Source of range (e.g., "Spring IQR")
    """
    grade: str
    band: str
    lexile_min: str
    lexile_max: str
    basis: str = "Spring 25th-75th percentile"
    
    def __str__(self) -> str:
        return f"{self.grade} {self.band.title()}: {self.lexile_min} to {self.lexile_max}"
    
    @property
    def display(self) -> str:
        """Formatted string for display (e.g., '245L-425L')."""
        return f"{self.lexile_min}-{self.lexile_max}"
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON export."""
        return {
            "grade": self.grade,
            "band": self.band,
            "lexile_min": self.lexile_min,
            "lexile_max": self.lexile_max,
            "display": self.display,
            "basis": self.basis
        }


# LEXILE RANGE BANK DATA
# Source: Spring 25th-75th percentile ranges split into Early/Late bands
LEXILE_BANK = [
    # Kindergarten
    LexileRange("K", "early", "BR310L", "BR160L"),
    LexileRange("K", "late", "BR155L", "BR5L"),
    
    # Grade 1
    LexileRange("1", "early", "BR35L", "165L"),
    LexileRange("1", "late", "170L", "365L"),
    
    # Grade 2
    LexileRange("2", "early", "245L", "425L"),
    LexileRange("2", "late", "430L", "605L"),
    
    # Grade 3
    LexileRange("3", "early", "480L", "645L"),
    LexileRange("3", "late", "650L", "810L"),
    
    # Grade 4
    LexileRange("4", "early", "700L", "850L"),
    LexileRange("4", "late", "855L", "1005L"),
    
    # Grade 5
    LexileRange("5", "early", "795L", "945L"),
    LexileRange("5", "late", "950L", "1100L"),
    
    # Grade 6
    LexileRange("6", "early", "875L", "1025L"),
    LexileRange("6", "late", "1030L", "1180L"),
    
    # Grade 7
    LexileRange("7", "early", "940L", "1095L"),
    LexileRange("7", "late", "1100L", "1250L"),
    
    # Grade 8
    LexileRange("8", "early", "1000L", "1155L"),
    LexileRange("8", "late", "1160L", "1310L"),
    
    # Grade 8+ (High School: Grades 9-12)
    LexileRange("8+", "early", "1050L", "1250L"),
    LexileRange("8+", "late", "1255L", "1450L"),
]


# Create lookup dictionary for fast access
_LEXILE_LOOKUP = {
    (lr.grade, lr.band): lr for lr in LEXILE_BANK
}


def get_lexile_range(grade: str, band: str) -> Optional[LexileRange]:
    """
    Get Lexile range for a specific grade and band.
    
    Args:
        grade: Grade level (K, 1-8, 8+)
        band: Lexile band ("early" or "late")
    
    Returns:
        LexileRange object or None if not found
    
    Example:
        >>> range_obj = get_lexile_range("2", "early")
        >>> print(range_obj)
        2 Early: 245L to 605L
    """
    return _LEXILE_LOOKUP.get((grade, band))


def get_all_ranges_for_grade(grade: str) -> list[LexileRange]:
    """
    Get all Lexile ranges (early and late) for a grade.
    
    Args:
        grade: Grade level (K, 1-8, 8+)
    
    Returns:
        List of LexileRange objects (typically 2: early and late)
    """
    return [lr for lr in LEXILE_BANK if lr.grade == grade]


def validate_lexile_target(grade: str, band: str, target_lexile: str) -> bool:
    """
    Validate that a target Lexile falls within the specified range.
    
    Args:
        grade: Grade level
        band: Lexile band
        target_lexile: Target Lexile value to validate
    
    Returns:
        True if target is within range, False otherwise
    
    Note:
        This does NOT compute actual Lexile scores. It only validates
        that a proposed target falls within the grade band range.
    """
    lexile_range = get_lexile_range(grade, band)
    if not lexile_range:
        return False
    
    # Convert Lexile strings to comparable integers
    # BR (Below Reader) levels are negative
    def lexile_to_int(lexile_str: str) -> int:
        if lexile_str.startswith("BR"):
            return -int(lexile_str[2:-1])  # Remove "BR" and "L"
        return int(lexile_str[:-1])  # Remove "L"
    
    min_val = lexile_to_int(lexile_range.lexile_min)
    max_val = lexile_to_int(lexile_range.lexile_max)
    target_val = lexile_to_int(target_lexile)
    
    return min_val <= target_val <= max_val


def get_midpoint_lexile(grade: str, band: str) -> Optional[str]:
    """
    Calculate the midpoint Lexile for a grade and band.
    Useful for targeting passage generation.
    
    Args:
        grade: Grade level
        band: Lexile band
    
    Returns:
        Midpoint Lexile as string (e.g., "335L") or None if range not found
    """
    lexile_range = get_lexile_range(grade, band)
    if not lexile_range:
        return None
    
    def lexile_to_int(lexile_str: str) -> int:
        if lexile_str.startswith("BR"):
            return -int(lexile_str[2:-1])
        return int(lexile_str[:-1])
    
    def int_to_lexile(val: int) -> str:
        if val < 0:
            return f"BR{abs(val)}L"
        return f"{val}L"
    
    min_val = lexile_to_int(lexile_range.lexile_min)
    max_val = lexile_to_int(lexile_range.lexile_max)
    midpoint = (min_val + max_val) // 2
    
    return int_to_lexile(midpoint)


def get_all_grades() -> list[str]:
    """Get list of all valid grades in the system."""
    return ["K", "1", "2", "3", "4", "5", "6", "7", "8", "8+"]


def get_all_bands() -> list[str]:
    """Get list of all valid bands in the system."""
    return ["early", "late"]


def export_to_json() -> list[dict]:
    """
    Export entire Lexile bank to JSON-serializable format.
    
    Returns:
        List of dictionaries representing all Lexile ranges
    """
    return [lr.to_dict() for lr in LEXILE_BANK]


# Validation on module load
def _validate_bank():
    """Internal validation to ensure bank integrity."""
    grades_found = set()
    for lr in LEXILE_BANK:
        # Check each grade has exactly 2 bands
        grades_found.add(lr.grade)
        
    # Verify all expected grades present
    expected_grades = {"K", "1", "2", "3", "4", "5", "6", "7", "8", "8+"}
    assert grades_found == expected_grades, f"Missing grades: {expected_grades - grades_found}"
    
    # Verify each grade has early and late
    for grade in expected_grades:
        assert get_lexile_range(grade, "early"), f"Missing early band for grade {grade}"
        assert get_lexile_range(grade, "late"), f"Missing late band for grade {grade}"
    
    print("✓ Bank 1 (Lexile Ranges) validated successfully")


if __name__ == "__main__":
    # Run validation
    _validate_bank()
    
    # Print sample lookups
    print("\nSample Lexile Ranges:")
    print(f"  Grade 2 Early: {get_lexile_range('2', 'early')}")
    print(f"  Grade 2 Late: {get_lexile_range('2', 'late')}")
    print(f"  Grade 2 Early Midpoint: {get_midpoint_lexile('2', 'early')}")
    
    # Export sample
    import json
    print("\nJSON Export Sample (first 3 entries):")
    print(json.dumps(export_to_json()[:3], indent=2))
