"""
Bank 5: Content Form Production Requirements
Defines which assessment forms are produced per grade band and genre options.
"""

from dataclasses import dataclass
from typing import Optional, Literal
from enum import Enum


class AssessmentType(str, Enum):
    """Type of assessment."""
    ORF = "orf"  # Oral Reading Fluency
    COMPREHENSION = "comprehension"


class Genre(str, Enum):
    """Genre options for passages."""
    NARRATIVE = "narrative"
    NONFICTION = "nonfiction"
    BOTH = "both"  # Generates both narrative and nonfiction


@dataclass(frozen=True)
class FormRequirement:
    """
    Defines form production requirements for a grade.
    
    Attributes:
        grade: Grade level
        assessment_type: ORF or Comprehension
        required_bands: List of bands to produce (typically ["early", "late"])
        genre_options: Available genre options for this grade
        default_genre: Default genre if not specified
        notes: Additional notes about form production
    """
    grade: str
    assessment_type: AssessmentType
    required_bands: list[str]
    genre_options: list[str]
    default_genre: str
    notes: str = ""
    
    def __str__(self) -> str:
        return (f"Grade {self.grade} {self.assessment_type.value}: "
                f"{len(self.required_bands)} bands, genres: {', '.join(self.genre_options)}")
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON export."""
        return {
            "grade": self.grade,
            "assessment_type": self.assessment_type.value,
            "required_bands": self.required_bands,
            "genre_options": self.genre_options,
            "default_genre": self.default_genre,
            "notes": self.notes
        }
    
    def supports_genre(self, genre: str) -> bool:
        """Check if this grade supports a specific genre."""
        return genre in self.genre_options


# FORM REQUIREMENT BANK DATA

# ORF Form Requirements (Grades 1-8)
ORF_REQUIREMENTS = [
    FormRequirement(
        grade="1",
        assessment_type=AssessmentType.ORF,
        required_bands=["early", "late"],
        genre_options=["narrative"],  # ORF is typically narrative
        default_genre="narrative",
        notes="ORF passages are narrative-focused for natural oral reading flow"
    ),
    FormRequirement(
        grade="2",
        assessment_type=AssessmentType.ORF,
        required_bands=["early", "late"],
        genre_options=["narrative"],
        default_genre="narrative",
        notes="ORF passages are narrative-focused for natural oral reading flow"
    ),
    FormRequirement(
        grade="3",
        assessment_type=AssessmentType.ORF,
        required_bands=["early", "late"],
        genre_options=["narrative"],
        default_genre="narrative",
        notes="ORF passages are narrative-focused for natural oral reading flow"
    ),
    FormRequirement(
        grade="4",
        assessment_type=AssessmentType.ORF,
        required_bands=["early", "late"],
        genre_options=["narrative"],
        default_genre="narrative",
        notes="ORF passages are narrative-focused for natural oral reading flow"
    ),
    FormRequirement(
        grade="5",
        assessment_type=AssessmentType.ORF,
        required_bands=["early", "late"],
        genre_options=["narrative"],
        default_genre="narrative",
        notes="ORF passages are narrative-focused for natural oral reading flow"
    ),
    FormRequirement(
        grade="6",
        assessment_type=AssessmentType.ORF,
        required_bands=["early", "late"],
        genre_options=["narrative"],
        default_genre="narrative",
        notes="ORF passages are narrative-focused for natural oral reading flow"
    ),
    FormRequirement(
        grade="7",
        assessment_type=AssessmentType.ORF,
        required_bands=["early", "late"],
        genre_options=["narrative"],
        default_genre="narrative",
        notes="ORF passages are narrative-focused for natural oral reading flow"
    ),
    FormRequirement(
        grade="8",
        assessment_type=AssessmentType.ORF,
        required_bands=["early", "late"],
        genre_options=["narrative"],
        default_genre="narrative",
        notes="ORF passages are narrative-focused for natural oral reading flow"
    ),
]

# Comprehension Form Requirements (K-8+)
COMPREHENSION_REQUIREMENTS = [
    FormRequirement(
        grade="K",
        assessment_type=AssessmentType.COMPREHENSION,
        required_bands=["early", "late"],
        genre_options=["narrative"],
        default_genre="narrative",
        notes="Listening comprehension only, single picture support"
    ),
    FormRequirement(
        grade="1",
        assessment_type=AssessmentType.COMPREHENSION,
        required_bands=["early", "late"],
        genre_options=["narrative"],
        default_genre="narrative",
        notes="Listening comprehension only, single picture support"
    ),
    FormRequirement(
        grade="2",
        assessment_type=AssessmentType.COMPREHENSION,
        required_bands=["early", "late"],
        genre_options=["narrative"],
        default_genre="narrative",
        notes="First independent reading comprehension grade"
    ),
    FormRequirement(
        grade="3",
        assessment_type=AssessmentType.COMPREHENSION,
        required_bands=["early", "late"],
        genre_options=["narrative", "nonfiction", "both"],
        default_genre="narrative",
        notes="Both narrative and nonfiction available; each band can have both genres"
    ),
    FormRequirement(
        grade="4",
        assessment_type=AssessmentType.COMPREHENSION,
        required_bands=["early", "late"],
        genre_options=["narrative", "nonfiction", "both"],
        default_genre="narrative",
        notes="Both narrative and nonfiction available; each band can have both genres"
    ),
    FormRequirement(
        grade="5",
        assessment_type=AssessmentType.COMPREHENSION,
        required_bands=["early", "late"],
        genre_options=["narrative", "nonfiction", "both"],
        default_genre="narrative",
        notes="Both narrative and nonfiction available; each band can have both genres"
    ),
    FormRequirement(
        grade="6",
        assessment_type=AssessmentType.COMPREHENSION,
        required_bands=["early", "late"],
        genre_options=["narrative", "nonfiction", "both"],
        default_genre="nonfiction",
        notes="Primarily nonfiction; text features required"
    ),
    FormRequirement(
        grade="7",
        assessment_type=AssessmentType.COMPREHENSION,
        required_bands=["early", "late"],
        genre_options=["narrative", "nonfiction", "both"],
        default_genre="nonfiction",
        notes="Nonfiction dominant; text features required"
    ),
    FormRequirement(
        grade="8",
        assessment_type=AssessmentType.COMPREHENSION,
        required_bands=["early", "late"],
        genre_options=["narrative", "nonfiction", "both"],
        default_genre="nonfiction",
        notes="Nonfiction dominant; text features required"
    ),
    FormRequirement(
        grade="8+",
        assessment_type=AssessmentType.COMPREHENSION,
        required_bands=["early", "late"],
        genre_options=["nonfiction"],
        default_genre="nonfiction",
        notes="High school: nonfiction only, historical or science topics, multi-paragraph"
    ),
]

# Combine all requirements
ALL_REQUIREMENTS = ORF_REQUIREMENTS + COMPREHENSION_REQUIREMENTS


# Create lookup dictionaries
_ORF_LOOKUP = {req.grade: req for req in ORF_REQUIREMENTS}
_COMP_LOOKUP = {req.grade: req for req in COMPREHENSION_REQUIREMENTS}


def get_form_requirements(
    grade: str, 
    assessment_type: Literal["orf", "comprehension"]
) -> Optional[FormRequirement]:
    """
    Get form production requirements for a grade and assessment type.
    
    Args:
        grade: Grade level (K, 1-8, 8+)
        assessment_type: "orf" or "comprehension"
    
    Returns:
        FormRequirement object or None if not found
    
    Example:
        >>> req = get_form_requirements("3", "comprehension")
        >>> print(req.genre_options)
        ['narrative', 'nonfiction', 'both']
    """
    if assessment_type == "orf":
        return _ORF_LOOKUP.get(grade)
    else:
        return _COMP_LOOKUP.get(grade)


def get_required_bands(grade: str, assessment_type: str) -> list[str]:
    """
    Get required bands for a grade (typically ["early", "late"]).
    
    Args:
        grade: Grade level
        assessment_type: "orf" or "comprehension"
    
    Returns:
        List of band names (typically ["early", "late"])
    """
    req = get_form_requirements(grade, assessment_type)
    return req.required_bands if req else []


def get_genre_options(grade: str, assessment_type: str) -> list[str]:
    """
    Get available genre options for a grade.
    
    Args:
        grade: Grade level
        assessment_type: "orf" or "comprehension"
    
    Returns:
        List of genre options (e.g., ["narrative"], ["narrative", "nonfiction", "both"])
    """
    req = get_form_requirements(grade, assessment_type)
    return req.genre_options if req else []


def supports_both_genres(grade: str, assessment_type: str = "comprehension") -> bool:
    """
    Check if grade supports both narrative and nonfiction.
    
    Args:
        grade: Grade level
        assessment_type: "orf" or "comprehension"
    
    Returns:
        True if "both" is an option, False otherwise
    """
    options = get_genre_options(grade, assessment_type)
    return "both" in options


def calculate_total_forms(grade: str, assessment_type: str, genre: str) -> int:
    """
    Calculate total number of forms to generate based on selection.
    
    Args:
        grade: Grade level
        assessment_type: "orf" or "comprehension"
        genre: Selected genre ("narrative", "nonfiction", or "both")
    
    Returns:
        Total number of forms to generate
    
    Example:
        >>> calculate_total_forms("3", "comprehension", "both")
        4  # 2 bands × 2 genres = 4 forms
    """
    req = get_form_requirements(grade, assessment_type)
    if not req:
        return 0
    
    num_bands = len(req.required_bands)
    
    if genre == "both":
        return num_bands * 2  # Early narrative, early nonfiction, late narrative, late nonfiction
    else:
        return num_bands  # Just early and late for selected genre


def generate_form_id(
    grade: str,
    assessment_type: str,
    band: str,
    genre: str,
    form_letter: str = "A"
) -> str:
    """
    Generate standardized form ID.
    
    Args:
        grade: Grade level
        assessment_type: "orf" or "comprehension"
        band: "early" or "late"
        genre: "narrative" or "nonfiction"
        form_letter: Optional form letter (A, B, C, etc.)
    
    Returns:
        Standardized form ID
    
    Example:
        >>> generate_form_id("3", "comprehension", "early", "narrative")
        'RC-COMP-G3-EARLY-NARR-A'
    """
    prefix = "RC-ORF" if assessment_type == "orf" else "RC-COMP"
    grade_str = f"G{grade.replace('+', 'PLUS')}"
    band_str = band.upper()
    genre_str = genre[:4].upper()  # NARR or NONF
    
    return f"{prefix}-{grade_str}-{band_str}-{genre_str}-{form_letter}"


def get_orf_grades() -> list[str]:
    """Get list of grades with ORF assessments."""
    return ["1", "2", "3", "4", "5", "6", "7", "8"]


def get_comprehension_grades() -> list[str]:
    """Get list of grades with comprehension assessments."""
    return ["K", "1", "2", "3", "4", "5", "6", "7", "8", "8+"]


def export_to_json() -> dict:
    """
    Export entire form requirements bank to JSON-serializable format.
    
    Returns:
        Dictionary with ORF and comprehension requirements
    """
    return {
        "orf_requirements": [req.to_dict() for req in ORF_REQUIREMENTS],
        "comprehension_requirements": [req.to_dict() for req in COMPREHENSION_REQUIREMENTS]
    }


# Validation on module load
def _validate_bank():
    """Internal validation to ensure bank integrity."""
    # Check ORF grades 1-8
    expected_orf_grades = {"1", "2", "3", "4", "5", "6", "7", "8"}
    found_orf_grades = {req.grade for req in ORF_REQUIREMENTS}
    assert found_orf_grades == expected_orf_grades, \
        f"Missing ORF grades: {expected_orf_grades - found_orf_grades}"
    
    # Check comprehension grades K-8+
    expected_comp_grades = {"K", "1", "2", "3", "4", "5", "6", "7", "8", "8+"}
    found_comp_grades = {req.grade for req in COMPREHENSION_REQUIREMENTS}
    assert found_comp_grades == expected_comp_grades, \
        f"Missing comprehension grades: {expected_comp_grades - found_comp_grades}"
    
    # Check all have early and late bands
    for req in ALL_REQUIREMENTS:
        assert req.required_bands == ["early", "late"], \
            f"Grade {req.grade} missing early/late bands"
    
    # Check K-2 comprehension only have narrative
    for grade in ["K", "1", "2"]:
        req = get_form_requirements(grade, "comprehension")
        assert req.genre_options == ["narrative"], \
            f"Grade {grade} should only have narrative option"
    
    # Check 3-8 comprehension have both options
    for grade in ["3", "4", "5", "6", "7", "8"]:
        req = get_form_requirements(grade, "comprehension")
        assert "both" in req.genre_options, \
            f"Grade {grade} should have 'both' option"
    
    # Check 8+ comprehension only has nonfiction
    req = get_form_requirements("8+", "comprehension")
    assert req.genre_options == ["nonfiction"], \
        "Grade 8+ should only have nonfiction option"
    
    print("✓ Bank 5 (Form Requirements) validated successfully")


if __name__ == "__main__":
    # Run validation
    _validate_bank()
    
    # Print sample requirements
    print("\nSample Form Requirements:")
    for grade in ["1", "3", "8+"]:
        print(f"\n  Grade {grade}:")
        
        # ORF (if available)
        orf_req = get_form_requirements(grade, "orf")
        if orf_req:
            print(f"    ORF: {orf_req}")
        
        # Comprehension
        comp_req = get_form_requirements(grade, "comprehension")
        if comp_req:
            print(f"    Comprehension: {comp_req}")
            print(f"    Supports both genres: {supports_both_genres(grade)}")
    
    # Test form ID generation
    print("\nSample Form IDs:")
    print(f"  {generate_form_id('3', 'comprehension', 'early', 'narrative')}")
    print(f"  {generate_form_id('3', 'comprehension', 'late', 'nonfiction')}")
    print(f"  {generate_form_id('2', 'orf', 'early', 'narrative')}")
    
    # Test form count calculation
    print("\nForm Count Examples:")
    print(f"  Grade 2 comprehension (narrative): {calculate_total_forms('2', 'comprehension', 'narrative')} forms")
    print(f"  Grade 3 comprehension (both): {calculate_total_forms('3', 'comprehension', 'both')} forms")
    
    # Export sample
    import json
    print("\nJSON Export Sample (ORF only):")
    print(json.dumps({"orf_requirements": [req.to_dict() for req in ORF_REQUIREMENTS[:2]]}, indent=2))
