"""
Bank 7: Text Structure Examples by Genre
Defines available text structures and their characteristics for narrative and nonfiction passages.
"""

from dataclasses import dataclass
from typing import Literal, Optional
from enum import Enum


class Genre(str, Enum):
    """Passage genre."""
    NARRATIVE = "narrative"
    NONFICTION = "nonfiction"


class TextStructure(str, Enum):
    """Available text structures."""
    CHRONOLOGICAL = "chronological"
    PROBLEM_SOLUTION = "problem_solution"
    CAUSE_EFFECT = "cause_effect"
    COMPARE_CONTRAST = "compare_contrast"
    DESCRIPTIVE = "descriptive"
    SEQUENCE = "sequence"


@dataclass(frozen=True)
class StructureDefinition:
    """
    Definition and guidance for a specific text structure.
    
    Attributes:
        structure: Structure type
        genre: Which genre uses this structure
        description: What this structure does
        signal_words: Common signal words/phrases
        typical_use: When to use this structure
        example_topics: Sample topics that fit this structure
    """
    structure: TextStructure
    genre: Genre
    description: str
    signal_words: list[str]
    typical_use: str
    example_topics: list[str]
    
    def __str__(self) -> str:
        return f"{self.structure.value} ({self.genre.value}): {self.description}"
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON export."""
        return {
            "structure": self.structure.value,
            "genre": self.genre.value,
            "description": self.description,
            "signal_words": self.signal_words,
            "typical_use": self.typical_use,
            "example_topics": self.example_topics
        }


# TEXT STRUCTURE BANK DATA

# Narrative Structures
NARRATIVE_STRUCTURES = [
    StructureDefinition(
        structure=TextStructure.CHRONOLOGICAL,
        genre=Genre.NARRATIVE,
        description="Events presented in time order from beginning to end",
        signal_words=["first", "then", "next", "after", "finally", "later", "before"],
        typical_use="Stories with clear sequence of events",
        example_topics=[
            "A day at the park",
            "Learning to ride a bike",
            "A family trip",
            "Making a new friend"
        ]
    ),
    StructureDefinition(
        structure=TextStructure.PROBLEM_SOLUTION,
        genre=Genre.NARRATIVE,
        description="Character faces a problem and works to solve it",
        signal_words=["problem", "solution", "challenge", "resolved", "fixed", "decided"],
        typical_use="Stories with clear conflict and resolution",
        example_topics=[
            "Lost pet found",
            "Overcoming fear",
            "Helping a friend",
            "Solving a mystery"
        ]
    ),
    StructureDefinition(
        structure=TextStructure.SEQUENCE,
        genre=Genre.NARRATIVE,
        description="Specific steps or stages in order",
        signal_words=["first", "second", "step", "stage", "process"],
        typical_use="How-to narratives or procedural stories",
        example_topics=[
            "Learning a new skill",
            "Following directions",
            "Completing a project",
            "Growing a garden"
        ]
    ),
]

# Nonfiction Structures
NONFICTION_STRUCTURES = [
    StructureDefinition(
        structure=TextStructure.DESCRIPTIVE,
        genre=Genre.NONFICTION,
        description="Provides details about a topic, person, place, or thing",
        signal_words=["for example", "characteristics", "such as", "including", "like"],
        typical_use="Informational texts introducing a topic",
        example_topics=[
            "Animal habitats",
            "Types of weather",
            "Parts of a plant",
            "Historical landmarks"
        ]
    ),
    StructureDefinition(
        structure=TextStructure.CAUSE_EFFECT,
        genre=Genre.NONFICTION,
        description="Shows how one event or action leads to another",
        signal_words=["because", "therefore", "as a result", "consequently", "due to", "if...then"],
        typical_use="Scientific processes or historical events",
        example_topics=[
            "Water cycle",
            "Erosion",
            "Migration patterns",
            "Climate effects"
        ]
    ),
    StructureDefinition(
        structure=TextStructure.COMPARE_CONTRAST,
        genre=Genre.NONFICTION,
        description="Shows similarities and differences between two or more things",
        signal_words=["similar", "different", "both", "however", "while", "unlike", "in contrast"],
        typical_use="Analyzing relationships between concepts",
        example_topics=[
            "Desert vs. rainforest",
            "Past vs. present",
            "Two historical figures",
            "Different ecosystems"
        ]
    ),
    StructureDefinition(
        structure=TextStructure.PROBLEM_SOLUTION,
        genre=Genre.NONFICTION,
        description="Presents a problem and explains how it was or could be solved",
        signal_words=["problem", "solution", "challenge", "addressed", "resolved", "improved"],
        typical_use="Social issues, scientific challenges, historical problems",
        example_topics=[
            "Conservation efforts",
            "Medical breakthroughs",
            "Engineering solutions",
            "Community improvements"
        ]
    ),
    StructureDefinition(
        structure=TextStructure.SEQUENCE,
        genre=Genre.NONFICTION,
        description="Events or steps in chronological or logical order",
        signal_words=["first", "next", "then", "finally", "stages", "process"],
        typical_use="Historical timelines, scientific processes, how things work",
        example_topics=[
            "Life cycle",
            "Historical timeline",
            "Scientific method",
            "Manufacturing process"
        ]
    ),
]

# Combine all structures
ALL_STRUCTURES = NARRATIVE_STRUCTURES + NONFICTION_STRUCTURES


# Create lookup dictionaries
_NARRATIVE_LOOKUP = {s.structure: s for s in NARRATIVE_STRUCTURES}
_NONFICTION_LOOKUP = {s.structure: s for s in NONFICTION_STRUCTURES}


def get_structure_definition(
    structure: str, 
    genre: str
) -> Optional[StructureDefinition]:
    """
    Get structure definition for a specific structure and genre.
    
    Args:
        structure: Structure type (e.g., "chronological", "cause_effect")
        genre: Genre ("narrative" or "nonfiction")
    
    Returns:
        StructureDefinition object or None if not found
    
    Example:
        >>> defn = get_structure_definition("problem_solution", "narrative")
        >>> print(defn.description)
        Character faces a problem and works to solve it
    """
    try:
        structure_enum = TextStructure(structure)
    except ValueError:
        return None
    
    if genre == "narrative":
        return _NARRATIVE_LOOKUP.get(structure_enum)
    elif genre == "nonfiction":
        return _NONFICTION_LOOKUP.get(structure_enum)
    return None


def get_structures_for_genre(genre: str) -> list[StructureDefinition]:
    """
    Get all available structures for a genre.
    
    Args:
        genre: "narrative" or "nonfiction"
    
    Returns:
        List of StructureDefinition objects for that genre
    """
    if genre == "narrative":
        return NARRATIVE_STRUCTURES
    elif genre == "nonfiction":
        return NONFICTION_STRUCTURES
    return []


def get_structure_names(genre: str) -> list[str]:
    """
    Get list of structure names for a genre.
    
    Args:
        genre: "narrative" or "nonfiction"
    
    Returns:
        List of structure names as strings
    
    Example:
        >>> get_structure_names("nonfiction")
        ['descriptive', 'cause_effect', 'compare_contrast', 'problem_solution', 'sequence']
    """
    structures = get_structures_for_genre(genre)
    return [s.structure.value for s in structures]


def get_signal_words(structure: str, genre: str) -> list[str]:
    """
    Get signal words for a specific structure.
    
    Args:
        structure: Structure type
        genre: Genre
    
    Returns:
        List of signal words/phrases
    """
    defn = get_structure_definition(structure, genre)
    return defn.signal_words if defn else []


def get_example_topics(structure: str, genre: str) -> list[str]:
    """
    Get example topics for a specific structure.
    
    Args:
        structure: Structure type
        genre: Genre
    
    Returns:
        List of example topics
    """
    defn = get_structure_definition(structure, genre)
    return defn.example_topics if defn else []


def is_valid_combination(structure: str, genre: str) -> bool:
    """
    Check if a structure/genre combination is valid.
    
    Args:
        structure: Structure type
        genre: Genre
    
    Returns:
        True if combination is valid, False otherwise
    """
    return get_structure_definition(structure, genre) is not None


def export_to_json() -> dict:
    """
    Export entire text structure bank to JSON-serializable format.
    
    Returns:
        Dictionary with narrative and nonfiction structures
    """
    return {
        "narrative_structures": [s.to_dict() for s in NARRATIVE_STRUCTURES],
        "nonfiction_structures": [s.to_dict() for s in NONFICTION_STRUCTURES]
    }


# Validation on module load
def _validate_bank():
    """Internal validation to ensure bank integrity."""
    # Check narrative structures
    narrative_structure_types = {s.structure for s in NARRATIVE_STRUCTURES}
    assert TextStructure.CHRONOLOGICAL in narrative_structure_types, \
        "Narrative missing chronological structure"
    assert TextStructure.PROBLEM_SOLUTION in narrative_structure_types, \
        "Narrative missing problem_solution structure"
    
    # Check nonfiction structures
    nonfiction_structure_types = {s.structure for s in NONFICTION_STRUCTURES}
    assert TextStructure.DESCRIPTIVE in nonfiction_structure_types, \
        "Nonfiction missing descriptive structure"
    assert TextStructure.CAUSE_EFFECT in nonfiction_structure_types, \
        "Nonfiction missing cause_effect structure"
    
    # Verify all have required fields
    for s in ALL_STRUCTURES:
        assert len(s.signal_words) > 0, f"{s.structure} has no signal words"
        assert len(s.example_topics) > 0, f"{s.structure} has no example topics"
    
    print("✓ Bank 7 (Text Structures) validated successfully")


if __name__ == "__main__":
    # Run validation
    _validate_bank()
    
    # Print all structures
    print("\nNarrative Structures:")
    for s in NARRATIVE_STRUCTURES:
        print(f"  {s.structure.value}:")
        print(f"    {s.description}")
        print(f"    Signal words: {', '.join(s.signal_words[:5])}")
        print(f"    Example: {s.example_topics[0]}")
    
    print("\nNonfiction Structures:")
    for s in NONFICTION_STRUCTURES:
        print(f"  {s.structure.value}:")
        print(f"    {s.description}")
        print(f"    Signal words: {', '.join(s.signal_words[:5])}")
        print(f"    Example: {s.example_topics[0]}")
    
    # Test lookups
    print("\nValid Combinations:")
    print(f"  problem_solution + narrative: {is_valid_combination('problem_solution', 'narrative')}")
    print(f"  cause_effect + nonfiction: {is_valid_combination('cause_effect', 'nonfiction')}")
    print(f"  cause_effect + narrative: {is_valid_combination('cause_effect', 'narrative')}")
    
    # Export sample
    import json
    print("\nJSON Export Sample (Narrative only):")
    print(json.dumps({"narrative_structures": [s.to_dict() for s in NARRATIVE_STRUCTURES]}, indent=2))
