"""
Assessment Enums

Standardized enumerations for assessment types, interactions, metrics, and error codes.
Replaces string literals throughout the system for type safety and consistency.

Created: 2026-01-16
Schema Version: 2026.2
"""

from enum import Enum


class AssessmentTypeEnum(Enum):
    """Assessment type identifiers"""
    ORF = "orf"
    WRF = "wrf"
    LR_ALPH = "lr_alph"
    FL_PSF = "fl_psf"
    FL_WRF = "fl_wrf"
    PA_RHYM = "pa_rhym"
    PA_OONS = "pa_oons"
    PA_PHON = "pa_phon"
    PA_SYLS = "pa_syls"
    PH_CSA = "ph_csa"
    PH_CVC = "ph_cvc"
    PH_LWID = "ph_lwid"
    PH_MPHY = "ph_mphy"
    PH_PSWD = "ph_pswd"
    PH_SPEL = "ph_spel"
    PH_WPAT = "ph_wpat"
    VO_EPVT = "vo_epvt"
    VO_MORP = "vo_morp"
    VO_RPVT = "vo_rpvt"
    VO_VOCA = "vo_voca"


class AssessorInteractionEnum(Enum):
    """How assessor marks responses"""
    CLICK_CYCLE = "click_cycle"
    PASSAGE_ERROR_MARKING = "passage_error_marking"  # NEW for ORF
    RUBRIC_SCORE = "rubric_score"  # NEW for prosody and other rubrics
    YES_NO_BUTTONS = "yes_no_buttons"
    CORRECT_INCORRECT = "correct_incorrect"
    COUNT_INPUT = "count_input"


class ResponseCaptureModeEnum(Enum):
    """Response capture granularity"""
    NONE = "none"
    ITEM_LEVEL = "item_level"
    PASSAGE_WORD_LEVEL = "passage_word_level"  # NEW for ORF


class ResponseStateEnum(Enum):
    """Response state for individual items/words"""
    CORRECT = "correct"
    ERROR = "error"
    SELF_CORRECTED = "self_corrected"
    SUPPLIED = "supplied"
    SKIPPED = "skipped"
    NOT_REACHED = "not_reached"
    UNKNOWN = "unknown"


class ErrorCodeEnum(Enum):
    """Universal error codes across assessments"""
    SUBSTITUTION = "substitution"
    OMISSION = "omission"
    INSERTION = "insertion"
    HESITATION_SUPPLY = "hesitation_supply"
    SELF_CORRECTION = "self_correction"
    REPETITION = "repetition"


class MetricEnum(Enum):
    """Measurement metrics"""
    WCPM = "wcpm"
    ACCURACY_PCT = "accuracy_pct"
    TOTAL_ERRORS = "total_errors"
    PROSODY_SCORE = "prosody_score"
    WORDS_READ = "words_read"
    TOTAL_CORRECT = "total_correct"
    TOTAL_TIME_SECONDS = "total_time_seconds"


class TimingModeEnum(Enum):
    """Timing behavior"""
    TIMER_DOWN_FIXED = "timer_down_fixed"  # Fixed countdown (e.g., 60 seconds)
    TIMER_UP = "timer_up"  # Count up, stop manually
    UNTIMED = "untimed"  # No timer


# Validation on module load
def _validate_enums():
    """Validate enum integrity"""
    # Check for duplicate values
    for enum_class in [AssessmentTypeEnum, AssessorInteractionEnum, 
                       ResponseCaptureModeEnum, ResponseStateEnum,
                       ErrorCodeEnum, MetricEnum, TimingModeEnum]:
        values = [e.value for e in enum_class]
        if len(values) != len(set(values)):
            raise ValueError(f"{enum_class.__name__} has duplicate values")
    
    print("✓ Assessment enums validated successfully")


if __name__ == "__main__":
    _validate_enums()
    
    print("\n=== Assessment Enums ===")
    print(f"\nAssessment Types ({len(AssessmentTypeEnum)}):")
    for e in AssessmentTypeEnum:
        print(f"  {e.name}: {e.value}")
    
    print(f"\nAssessor Interactions ({len(AssessorInteractionEnum)}):")
    for e in AssessorInteractionEnum:
        print(f"  {e.name}: {e.value}")
    
    print(f"\nResponse Capture Modes ({len(ResponseCaptureModeEnum)}):")
    for e in ResponseCaptureModeEnum:
        print(f"  {e.name}: {e.value}")
    
    print(f"\nError Codes ({len(ErrorCodeEnum)}):")
    for e in ErrorCodeEnum:
        print(f"  {e.name}: {e.value}")
    
    print(f"\nMetrics ({len(MetricEnum)}):")
    for e in MetricEnum:
        print(f"  {e.name}: {e.value}")
    
    print(f"\nTiming Modes ({len(TimingModeEnum)}):")
    for e in TimingModeEnum:
        print(f"  {e.name}: {e.value}")
