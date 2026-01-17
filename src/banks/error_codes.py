"""
Bank 8: Universal Error Code Definitions

Structured error code bank with formal definitions for all error types
across reading assessments. Supports deterministic error counting and
pattern analysis.

Created: 2026-01-16
Schema Version: 2026.2
"""

from dataclasses import dataclass
from typing import List, Optional
from ..assessments.enums import ErrorCodeEnum, AssessmentTypeEnum


@dataclass(frozen=True)
class ErrorCodeDefinition:
    """Structured error code definition"""
    code: ErrorCodeEnum
    label: str
    counts_as_error: bool
    capture_fields_required: List[str]
    allowed_assessment_types: List[AssessmentTypeEnum]
    description: str
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON export"""
        return {
            "code": self.code.value,
            "label": self.label,
            "counts_as_error": self.counts_as_error,
            "capture_fields_required": self.capture_fields_required,
            "allowed_assessment_types": [t.value for t in self.allowed_assessment_types],
            "description": self.description
        }


# Universal Error Code Bank
ERROR_CODE_BANK = [
    ErrorCodeDefinition(
        code=ErrorCodeEnum.SUBSTITUTION,
        label="Substitution",
        counts_as_error=True,
        capture_fields_required=["printed_word", "student_said"],
        allowed_assessment_types=[AssessmentTypeEnum.ORF, AssessmentTypeEnum.WRF],
        description="Student says a different word than what is printed"
    ),
    ErrorCodeDefinition(
        code=ErrorCodeEnum.OMISSION,
        label="Omission",
        counts_as_error=True,
        capture_fields_required=["printed_word"],
        allowed_assessment_types=[AssessmentTypeEnum.ORF, AssessmentTypeEnum.WRF],
        description="Student skips a word entirely"
    ),
    ErrorCodeDefinition(
        code=ErrorCodeEnum.INSERTION,
        label="Insertion",
        counts_as_error=True,
        capture_fields_required=["student_said"],
        allowed_assessment_types=[AssessmentTypeEnum.ORF, AssessmentTypeEnum.WRF],
        description="Student adds a word that is not in the text"
    ),
    ErrorCodeDefinition(
        code=ErrorCodeEnum.HESITATION_SUPPLY,
        label="Hesitation (Word Supplied)",
        counts_as_error=True,
        capture_fields_required=["printed_word", "hesitation_seconds"],
        allowed_assessment_types=[AssessmentTypeEnum.ORF, AssessmentTypeEnum.WRF],
        description="Student pauses 3+ seconds, assessor supplies word"
    ),
    ErrorCodeDefinition(
        code=ErrorCodeEnum.SELF_CORRECTION,
        label="Self-Correction",
        counts_as_error=False,
        capture_fields_required=["printed_word", "initial_error", "corrected_within_window"],
        allowed_assessment_types=[AssessmentTypeEnum.ORF, AssessmentTypeEnum.WRF],
        description="Student corrects own error immediately (not counted as error if within window)"
    ),
    ErrorCodeDefinition(
        code=ErrorCodeEnum.REPETITION,
        label="Repetition",
        counts_as_error=False,
        capture_fields_required=["repeated_text"],
        allowed_assessment_types=[AssessmentTypeEnum.ORF, AssessmentTypeEnum.WRF],
        description="Student repeats word or phrase (not counted as error)"
    )
]


# Create lookup dictionary
_ERROR_CODE_LOOKUP = {ec.code: ec for ec in ERROR_CODE_BANK}


def get_error_code(code: ErrorCodeEnum) -> Optional[ErrorCodeDefinition]:
    """
    Get error code definition by enum.
    
    Args:
        code: ErrorCodeEnum value
    
    Returns:
        ErrorCodeDefinition or None if not found
    """
    return _ERROR_CODE_LOOKUP.get(code)


def get_error_codes_for_assessment(assessment_type: AssessmentTypeEnum) -> List[ErrorCodeDefinition]:
    """
    Get all error codes allowed for a specific assessment type.
    
    Args:
        assessment_type: AssessmentTypeEnum value
    
    Returns:
        List of ErrorCodeDefinition objects
    """
    return [ec for ec in ERROR_CODE_BANK if assessment_type in ec.allowed_assessment_types]


def get_counted_error_codes() -> List[ErrorCodeDefinition]:
    """Get all error codes that count as errors (counts_as_error=True)"""
    return [ec for ec in ERROR_CODE_BANK if ec.counts_as_error]


def export_to_json() -> List[dict]:
    """Export entire error code bank to JSON-serializable format"""
    return [ec.to_dict() for ec in ERROR_CODE_BANK]


# Validation on module load
def _validate_bank():
    """Internal validation to ensure bank integrity"""
    # Check all ErrorCodeEnum values are in bank
    expected_codes = set(ErrorCodeEnum)
    found_codes = {ec.code for ec in ERROR_CODE_BANK}
    
    assert found_codes == expected_codes, \
        f"Missing error codes: {expected_codes - found_codes}"
    
    # Check no duplicate codes
    assert len(ERROR_CODE_BANK) == len(_ERROR_CODE_LOOKUP), \
        "Duplicate error codes found"
    
    # Check all counted errors have required fields
    for ec in ERROR_CODE_BANK:
        if ec.counts_as_error:
            assert len(ec.capture_fields_required) > 0, \
                f"{ec.code.value} counts as error but has no required fields"
    
    print("✓ Bank 8 (Error Codes) validated successfully")


if __name__ == "__main__":
    _validate_bank()
    
    print("\n=== Error Code Bank ===")
    print(f"\nTotal Error Codes: {len(ERROR_CODE_BANK)}")
    
    print("\nCounted Errors:")
    for ec in get_counted_error_codes():
        print(f"  • {ec.label} ({ec.code.value})")
        print(f"    Required fields: {', '.join(ec.capture_fields_required)}")
    
    print("\nNon-Counted Errors:")
    for ec in ERROR_CODE_BANK:
        if not ec.counts_as_error:
            print(f"  • {ec.label} ({ec.code.value})")
    
    print("\nORF Error Codes:")
    orf_codes = get_error_codes_for_assessment(AssessmentTypeEnum.ORF)
    for ec in orf_codes:
        print(f"  • {ec.label}")
