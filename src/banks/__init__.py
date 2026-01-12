"""
Reading Assessment Generator - Foundation Banks Module

This module provides the foundational data banks that drive all assessment generation.
All banks are immutable and validated on import to prevent drift.

Available Banks:
- Bank 1: Lexile Ranges (lexile_ranges.py)
- Bank 2: ORF Word Counts (orf_word_counts.py)
- Bank 3: Comprehension Word Counts (comp_word_counts.py)
- Bank 4: Comprehension Blueprint (comprehension_blueprint.py)
- Bank 5: Form Requirements (form_requirements.py)
- Bank 6: Answer Options (answer_options.py)
- Bank 7: Text Structures (text_structures.py)
"""

# Import all banks
from . import lexile_ranges
from . import orf_word_counts
from . import comp_word_counts
from . import comprehension_blueprint
from . import form_requirements
from . import answer_options
from . import text_structures

# Export key classes and enums for easy access
from .lexile_ranges import LexileRange, get_lexile_range, get_midpoint_lexile
from .orf_word_counts import ORFTargets, get_orf_target, validate_word_count as validate_orf_word_count
from .comp_word_counts import ComprehensionWordCount, get_comp_word_count, validate_word_count as validate_comp_word_count
from .comprehension_blueprint import (
    ComprehensionBlueprint, 
    QuestionDistribution,
    get_blueprint,
    requires_picture,
    requires_text_features,
    is_listening_comprehension
)
from .form_requirements import (
    FormRequirement,
    get_form_requirements,
    get_genre_options,
    generate_form_id
)
from .answer_options import get_num_options, get_distractor_guidance
from .text_structures import (
    get_structure_definition,
    get_structures_for_genre,
    get_structure_names
)


# Version info
__version__ = "1.0.0"
__bank_version__ = "2026.1"  # Year.Revision format


# Unified validation function
def validate_all_banks() -> bool:
    """
    Run validation on all banks and report results.
    
    Returns:
        True if all banks pass validation, False otherwise
    """
    print("="*60)
    print("VALIDATING ALL FOUNDATION BANKS")
    print("="*60)
    
    try:
        lexile_ranges._validate_bank()
        orf_word_counts._validate_bank()
        comp_word_counts._validate_bank()
        comprehension_blueprint._validate_bank()
        form_requirements._validate_bank()
        answer_options._validate_bank()
        text_structures._validate_bank()
        
        print("="*60)
        print("✓ ALL BANKS VALIDATED SUCCESSFULLY")
        print(f"Bank Version: {__bank_version__}")
        print("="*60)
        return True
        
    except AssertionError as e:
        print("="*60)
        print(f"✗ VALIDATION FAILED: {e}")
        print("="*60)
        return False


# Unified export function
def export_all_banks_to_json() -> dict:
    """
    Export all banks to a single JSON structure.
    
    Returns:
        Dictionary containing all bank data
    """
    return {
        "version": __bank_version__,
        "banks": {
            "lexile_ranges": lexile_ranges.export_to_json(),
            "orf_word_counts": orf_word_counts.export_to_json(),
            "comp_word_counts": comp_word_counts.export_to_json(),
            "comprehension_blueprint": comprehension_blueprint.export_to_json(),
            "form_requirements": form_requirements.export_to_json(),
            "answer_options": answer_options.export_to_json(),
            "text_structures": text_structures.export_to_json()
        }
    }


# Quick access helpers
def get_assessment_specs(grade: str, assessment_type: str, band: str = "early") -> dict:
    """
    Get all relevant specifications for an assessment in one call.
    
    Args:
        grade: Grade level (K, 1-8, 8+)
        assessment_type: "orf" or "comprehension"
        band: "early" or "late"
    
    Returns:
        Dictionary with all relevant specs
    
    Example:
        >>> specs = get_assessment_specs("2", "orf", "early")
        >>> print(specs["lexile_range"])
        >>> print(specs["word_count"])
    """
    result = {
        "grade": grade,
        "assessment_type": assessment_type,
        "band": band
    }
    
    # Lexile range
    lexile = get_lexile_range(grade, band)
    if lexile:
        result["lexile_range"] = f"{lexile.lexile_min} to {lexile.lexile_max}"
        result["lexile_midpoint"] = get_midpoint_lexile(grade, band)
    
    # Word count
    if assessment_type == "orf":
        orf = get_orf_target(grade)
        if orf:
            result["word_count"] = orf.target_word_count
            result["word_count_range"] = f"{orf.min_word_count}-{orf.max_word_count}"
    else:  # comprehension
        comp = get_comp_word_count(grade)
        if comp:
            result["word_count"] = comp.average
            result["word_count_range"] = f"{comp.min_allowed}-{comp.max_allowed}"
    
    # Comprehension-specific
    if assessment_type == "comprehension":
        blueprint = get_blueprint(grade)
        if blueprint:
            result["total_questions"] = blueprint.total_questions
            result["question_distribution"] = blueprint.distribution.to_dict()
            result["text_access_mode"] = blueprint.text_access_mode.value
            result["requires_picture"] = requires_picture(grade)
            result["requires_text_features"] = requires_text_features(grade)
    
    # Form requirements
    form_req = get_form_requirements(grade, assessment_type)
    if form_req:
        result["genre_options"] = form_req.genre_options
        result["default_genre"] = form_req.default_genre
    
    # Answer options (comprehension only)
    if assessment_type == "comprehension":
        result["num_answer_options"] = get_num_options(grade)
        result["distractor_guidance"] = get_distractor_guidance(grade)
    
    return result


# Run validation on import
if __name__ != "__main__":
    # Auto-validate when imported (but not when run directly as script)
    validate_all_banks()


if __name__ == "__main__":
    # When run as script, perform comprehensive checks
    print("\n" + "="*60)
    print("READING ASSESSMENT GENERATOR - FOUNDATION BANKS")
    print("="*60)
    
    # Validate
    validate_all_banks()
    
    # Show sample specs
    print("\nSample Assessment Specifications:")
    print("-" * 60)
    
    for grade in ["K", "2", "5", "8"]:
        for assessment_type in ["orf", "comprehension"]:
            if assessment_type == "orf" and grade == "K":
                continue  # Skip K ORF
            
            specs = get_assessment_specs(grade, assessment_type, "early")
            print(f"\nGrade {grade} {assessment_type.upper()} (Early):")
            for key, value in specs.items():
                if key not in ["grade", "assessment_type", "band"]:
                    print(f"  {key}: {value}")
    
    # Export option
    print("\n" + "="*60)
    print("To export all banks to JSON, run:")
    print("  python -c 'from banks import export_all_banks_to_json; import json; print(json.dumps(export_all_banks_to_json(), indent=2))' > banks_export.json")
    print("="*60)
