"""
Bank 4: Comprehensive Comprehension Blueprint (K-8+)
Defines complete comprehension assessment specifications by grade.
"""

from dataclasses import dataclass, field
from typing import Optional, Literal
from enum import Enum


class TextAccessMode(str, Enum):
    """How student accesses the passage."""
    LISTENING = "listening"  # Assessor reads passage aloud
    INDEPENDENT = "independent"  # Student reads passage


class ItemAccessMode(str, Enum):
    """How student accesses the questions."""
    READ_ALOUD = "read_aloud"  # Assessor reads questions aloud
    STUDENT_READS = "student_reads"  # Student reads questions


class TextType(str, Enum):
    """Primary text type for the grade."""
    NARRATIVE = "narrative"
    NARRATIVE_AND_NONFICTION = "narrative_and_nonfiction"
    PRIMARILY_NONFICTION = "primarily_nonfiction"
    NONFICTION_DOMINANT = "nonfiction_dominant"


@dataclass(frozen=True)
class QuestionDistribution:
    """
    Distribution of question types for a grade.
    
    All counts must sum to total_questions.
    """
    explicit: int = 0
    implicit: int = 0
    vocabulary: int = 0
    main_idea: int = 0
    text_structure: int = 0
    inference_advanced: int = 0
    
    @property
    def total(self) -> int:
        """Calculate total questions."""
        return (self.explicit + self.implicit + self.vocabulary + 
                self.main_idea + self.text_structure + self.inference_advanced)
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        result = {}
        if self.explicit > 0: result["explicit"] = self.explicit
        if self.implicit > 0: result["implicit"] = self.implicit
        if self.vocabulary > 0: result["vocabulary"] = self.vocabulary
        if self.main_idea > 0: result["main_idea"] = self.main_idea
        if self.text_structure > 0: result["text_structure"] = self.text_structure
        if self.inference_advanced > 0: result["inference_advanced"] = self.inference_advanced
        return result


@dataclass(frozen=True)
class CognitiveDistribution:
    """Distribution of cognitive demand levels."""
    low: int = 0
    medium: int = 0
    high: int = 0

    @property
    def total(self) -> int:
        return self.low + self.medium + self.high

    def to_dict(self) -> dict:
        return {"low": self.low, "medium": self.medium, "high": self.high}


@dataclass(frozen=True)
class ComprehensionBlueprint:
    """
    Complete comprehension assessment specification for a grade level.
    
    This is the single source of truth for comprehension assessment structure.
    """
    grade: str
    text_access_mode: TextAccessMode
    item_access_mode: ItemAccessMode
    supports_allowed: str  # e.g., "Single picture per passage", "None"
    text_features_required: bool
    text_type: TextType
    example_themes: list[str]
    lexile_range_note: str  # Reference to Bank 1
    total_questions: int
    distribution: QuestionDistribution
    cognitive_demands: CognitiveDistribution
    
    def __post_init__(self):
        """Validate that distributions sum to total questions."""
        if self.distribution.total != self.total_questions:
            raise ValueError(
                f"Grade {self.grade}: Question distribution ({self.distribution.total}) "
                f"does not match total_questions ({self.total_questions})"
            )
        if self.cognitive_demands.total != self.total_questions:
            raise ValueError(
                f"Grade {self.grade}: Cognitive distribution ({self.cognitive_demands.total}) "
                f"does not match total_questions ({self.total_questions})"
            )
    
    def __str__(self) -> str:
        return (f"Grade {self.grade}: {self.total_questions} questions, "
                f"{self.text_access_mode.value}, {self.text_type.value}")
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON export."""
        return {
            "grade": self.grade,
            "text_access_mode": self.text_access_mode.value,
            "item_access_mode": self.item_access_mode.value,
            "supports_allowed": self.supports_allowed,
            "text_features_required": self.text_features_required,
            "text_type": self.text_type.value,
            "example_themes": self.example_themes,
            "lexile_range_note": self.lexile_range_note,
            "total_questions": self.total_questions,
            "question_distribution": self.distribution.to_dict(),
            "cognitive_distribution": self.cognitive_demands.to_dict()
        }


# COMPREHENSION BLUEPRINT BANK DATA
BLUEPRINT_BANK = [
    # Kindergarten
    ComprehensionBlueprint(
        grade="K",
        text_access_mode=TextAccessMode.LISTENING,
        item_access_mode=ItemAccessMode.READ_ALOUD,
        supports_allowed="Single picture per passage",
        text_features_required=False,
        text_type=TextType.NARRATIVE,
        example_themes=["Family", "School", "Animals", "Daily routines"],
        lexile_range_note="BR310L-BR5L",
        total_questions=4,
        distribution=QuestionDistribution(explicit=4),
        cognitive_demands=CognitiveDistribution(low=4)
    ),
    
    # Grade 1
    ComprehensionBlueprint(
        grade="1",
        text_access_mode=TextAccessMode.LISTENING,
        item_access_mode=ItemAccessMode.READ_ALOUD,
        supports_allowed="Single picture per passage",
        text_features_required=False,
        text_type=TextType.NARRATIVE,
        example_themes=["Friends", "Routines", "Nature", "Helping others"],
        lexile_range_note="BR35L-365L",
        total_questions=5,
        distribution=QuestionDistribution(explicit=4, implicit=1),
        cognitive_demands=CognitiveDistribution(low=4, medium=1)
    ),
    
    # Grade 2
    ComprehensionBlueprint(
        grade="2",
        text_access_mode=TextAccessMode.INDEPENDENT,
        item_access_mode=ItemAccessMode.STUDENT_READS,
        supports_allowed="None",
        text_features_required=False,
        text_type=TextType.NARRATIVE,
        example_themes=["Everyday problems", "Helping others", "Friendship", "Community"],
        lexile_range_note="245L-605L",
        total_questions=6,
        distribution=QuestionDistribution(explicit=4, implicit=2),
        cognitive_demands=CognitiveDistribution(low=3, medium=3)
    ),
    
    # Grade 3
    ComprehensionBlueprint(
        grade="3",
        text_access_mode=TextAccessMode.INDEPENDENT,
        item_access_mode=ItemAccessMode.STUDENT_READS,
        supports_allowed="None",
        text_features_required=False,
        text_type=TextType.NARRATIVE_AND_NONFICTION,
        example_themes=["Community", "Simple science topics", "Historical figures", "Problem-solving"],
        lexile_range_note="480L-810L",
        total_questions=8,
        distribution=QuestionDistribution(explicit=4, implicit=4),
        cognitive_demands=CognitiveDistribution(low=3, medium=3, high=2)
    ),
    
    # Grade 4
    ComprehensionBlueprint(
        grade="4",
        text_access_mode=TextAccessMode.INDEPENDENT,
        item_access_mode=ItemAccessMode.STUDENT_READS,
        supports_allowed="None",
        text_features_required=False,
        text_type=TextType.NARRATIVE_AND_NONFICTION,
        example_themes=["History", "Problem solving", "Scientific processes", "Cultural topics"],
        lexile_range_note="700L-1005L",
        total_questions=10,
        distribution=QuestionDistribution(explicit=4, implicit=4, vocabulary=2),
        cognitive_demands=CognitiveDistribution(low=3, medium=4, high=3)
    ),
    
    # Grade 5
    ComprehensionBlueprint(
        grade="5",
        text_access_mode=TextAccessMode.INDEPENDENT,
        item_access_mode=ItemAccessMode.STUDENT_READS,
        supports_allowed="None",
        text_features_required=False,
        text_type=TextType.NARRATIVE_AND_NONFICTION,
        example_themes=["Survival", "Innovation", "Exploration", "Systems and structures"],
        lexile_range_note="795L-1100L",
        total_questions=12,
        distribution=QuestionDistribution(explicit=4, implicit=4, vocabulary=2, main_idea=2),
        cognitive_demands=CognitiveDistribution(low=3, medium=5, high=4)
    ),
    
    # Grade 6
    ComprehensionBlueprint(
        grade="6",
        text_access_mode=TextAccessMode.INDEPENDENT,
        item_access_mode=ItemAccessMode.STUDENT_READS,
        supports_allowed="None",
        text_features_required=True,
        text_type=TextType.PRIMARILY_NONFICTION,
        example_themes=["Science", "Social studies", "Ecosystems", "Historical analysis"],
        lexile_range_note="875L-1180L",
        total_questions=14,
        distribution=QuestionDistribution(
            explicit=4, implicit=4, vocabulary=2, main_idea=2, text_structure=2
        ),
        cognitive_demands=CognitiveDistribution(low=3, medium=6, high=5)
    ),
    
    # Grade 7
    ComprehensionBlueprint(
        grade="7",
        text_access_mode=TextAccessMode.INDEPENDENT,
        item_access_mode=ItemAccessMode.STUDENT_READS,
        supports_allowed="None",
        text_features_required=True,
        text_type=TextType.NONFICTION_DOMINANT,
        example_themes=["Argument", "Systems", "Scientific inquiry", "Economic concepts"],
        lexile_range_note="940L-1250L",
        total_questions=16,
        distribution=QuestionDistribution(
            explicit=4, implicit=4, vocabulary=2, main_idea=2, 
            text_structure=2, inference_advanced=2
        ),
        cognitive_demands=CognitiveDistribution(low=3, medium=7, high=6)
    ),
    
    # Grade 8
    ComprehensionBlueprint(
        grade="8",
        text_access_mode=TextAccessMode.INDEPENDENT,
        item_access_mode=ItemAccessMode.STUDENT_READS,
        supports_allowed="None",
        text_features_required=True,
        text_type=TextType.NONFICTION_DOMINANT,
        example_themes=["Policy", "Ethics", "Analysis", "Complex systems"],
        lexile_range_note="1000L-1310L",
        total_questions=18,
        distribution=QuestionDistribution(
            explicit=4, implicit=4, vocabulary=2, main_idea=2, 
            text_structure=2, inference_advanced=4
        ),
        cognitive_demands=CognitiveDistribution(low=3, medium=8, high=7)
    ),
    
    # Grade 8+ (High School)
    ComprehensionBlueprint(
        grade="8+",
        text_access_mode=TextAccessMode.INDEPENDENT,
        item_access_mode=ItemAccessMode.STUDENT_READS,
        supports_allowed="None",
        text_features_required=True,
        text_type=TextType.NONFICTION_DOMINANT,
        example_themes=["Policy analysis", "Ethical dilemmas", "Historical interpretation", "Scientific research"],
        lexile_range_note="1050L-1450L",
        total_questions=18,
        distribution=QuestionDistribution(
            explicit=4, implicit=4, vocabulary=2, main_idea=2, 
            text_structure=2, inference_advanced=4
        ),
        cognitive_demands=CognitiveDistribution(low=2, medium=8, high=8)
    ),
]


# Create lookup dictionary
_BLUEPRINT_LOOKUP = {bp.grade: bp for bp in BLUEPRINT_BANK}


def get_blueprint(grade: str) -> Optional[ComprehensionBlueprint]:
    """
    Get complete comprehension blueprint for a grade.
    
    Args:
        grade: Grade level (K, 1-8, 8+)
    
    Returns:
        ComprehensionBlueprint object or None if grade not found
    
    Example:
        >>> bp = get_blueprint("3")
        >>> print(bp.total_questions)
        8
    """
    return _BLUEPRINT_LOOKUP.get(grade)


def get_question_distribution(grade: str) -> Optional[QuestionDistribution]:
    """
    Get question distribution for a grade.
    
    Args:
        grade: Grade level (K, 1-8, 8+)
    
    Returns:
        QuestionDistribution object or None if grade not found
    """
    bp = get_blueprint(grade)
    return bp.distribution if bp else None


def requires_picture(grade: str) -> bool:
    """
    Check if grade requires picture support (K-1 only).
    
    Args:
        grade: Grade level
    
    Returns:
        True if picture required, False otherwise
    """
    bp = get_blueprint(grade)
    return bp and "picture" in bp.supports_allowed.lower()


def requires_text_features(grade: str) -> bool:
    """
    Check if grade requires text features (6+ only).
    
    Args:
        grade: Grade level
    
    Returns:
        True if text features required, False otherwise
    """
    bp = get_blueprint(grade)
    return bp.text_features_required if bp else False


def is_listening_comprehension(grade: str) -> bool:
    """
    Check if grade uses listening comprehension (K-1 only).
    
    Args:
        grade: Grade level
    
    Returns:
        True if listening comprehension, False otherwise
    """
    bp = get_blueprint(grade)
    return bp and bp.text_access_mode == TextAccessMode.LISTENING


def get_all_grades() -> list[str]:
    """Get list of all grades with comprehension assessments."""
    return ["K", "1", "2", "3", "4", "5", "6", "7", "8", "8+"]


def export_to_json() -> list[dict]:
    """
    Export entire blueprint bank to JSON-serializable format.
    
    Returns:
        List of dictionaries representing all blueprints
    """
    return [bp.to_dict() for bp in BLUEPRINT_BANK]


# Validation on module load
def _validate_bank():
    """Internal validation to ensure bank integrity."""
    # Check all grades K-8+ present
    expected_grades = {"K", "1", "2", "3", "4", "5", "6", "7", "8", "8+"}
    found_grades = {bp.grade for bp in BLUEPRINT_BANK}
    
    assert found_grades == expected_grades, f"Missing grades: {expected_grades - found_grades}"
    
    # Validate each blueprint
    for bp in BLUEPRINT_BANK:
        # Check distribution sums correctly (already checked in __post_init__)
        assert bp.distribution.total == bp.total_questions
        
        # Check K-1 are listening comprehension
        if bp.grade in ["K", "1"]:
            assert bp.text_access_mode == TextAccessMode.LISTENING, \
                f"Grade {bp.grade} should be listening comprehension"
            assert "picture" in bp.supports_allowed.lower(), \
                f"Grade {bp.grade} should have picture support"
        
        # Check 2+ are independent reading
        if bp.grade not in ["K", "1"]:
            assert bp.text_access_mode == TextAccessMode.INDEPENDENT, \
                f"Grade {bp.grade} should be independent reading"
            assert bp.supports_allowed == "None", \
                f"Grade {bp.grade} should have no supports"
        
        # Check 6+ require text features
        if bp.grade in ["6", "7", "8", "8+"]:
            assert bp.text_features_required, \
                f"Grade {bp.grade} should require text features"
    
    # Check question counts are increasing
    prev_count = 0
    for bp in BLUEPRINT_BANK:
        assert bp.total_questions >= prev_count, \
            f"Grade {bp.grade} question count not increasing or equal"
        prev_count = bp.total_questions
    
    print("✓ Bank 4 (Comprehension Blueprint) validated successfully")


if __name__ == "__main__":
    # Run validation
    _validate_bank()
    
    # Print sample blueprints
    print("\nSample Comprehension Blueprints:")
    for grade in ["K", "2", "5", "8+"]:
        bp = get_blueprint(grade)
        print(f"\n  {bp}")
        print(f"    Text access: {bp.text_access_mode.value}")
        print(f"    Total questions: {bp.total_questions}")
        print(f"    Distribution: {bp.distribution.to_dict()}")
        print(f"    Picture required: {requires_picture(grade)}")
        print(f"    Text features required: {requires_text_features(grade)}")
    
    # Export sample
    import json
    print("\nJSON Export Sample (Grade 3):")
    print(json.dumps(get_blueprint("3").to_dict(), indent=2))
