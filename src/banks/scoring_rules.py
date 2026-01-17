"""
Bank 9: ORF Scoring Rules

Deterministic scoring computation rules for Oral Reading Fluency.
Replaces narrative formulas with structured, machine-actionable specifications.

Created: 2026-01-16
Schema Version: 2026.2
"""

from dataclasses import dataclass, field
from typing import Dict, Any
from ..assessments.enums import MetricEnum, ErrorCodeEnum


@dataclass(frozen=True)
class ORFScoringRules:
    """ORF scoring computation rules"""
    time_limit_seconds: int = 60
    hesitation_threshold_seconds: int = 3
    self_correction_window_seconds: int = 3
    self_correction_counting_policy: str = "not_counted_if_within_window"
    
    # Computed metrics definitions
    computed_metrics: Dict[str, Any] = field(default_factory=lambda: {
        MetricEnum.WORDS_READ.value: {
            "source": "input",
            "description": "Total words read in time limit",
            "formula": None
        },
        MetricEnum.TOTAL_ERRORS.value: {
            "source": "counted_errors",
            "description": "Count of errors where counts_as_error=True",
            "formula": "count(errors where counts_as_error=True)"
        },
        MetricEnum.WCPM.value: {
            "source": "computed",
            "description": "Words Correct Per Minute",
            "formula": "WORDS_READ - TOTAL_ERRORS"
        },
        MetricEnum.ACCURACY_PCT.value: {
            "source": "computed",
            "description": "Accuracy percentage",
            "formula": "(WORDS_READ - TOTAL_ERRORS) / WORDS_READ * 100"
        },
        MetricEnum.PROSODY_SCORE.value: {
            "source": "rubric",
            "description": "Prosody rating (1-4 scale)",
            "formula": None
        }
    })
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON export"""
        return {
            "time_limit_seconds": self.time_limit_seconds,
            "hesitation_threshold_seconds": self.hesitation_threshold_seconds,
            "self_correction_window_seconds": self.self_correction_window_seconds,
            "self_correction_counting_policy": self.self_correction_counting_policy,
            "computed_metrics": self.computed_metrics
        }
    
    def compute_wcpm(self, words_read: int, total_errors: int) -> int:
        """
        Compute Words Correct Per Minute.
        
        Args:
            words_read: Total words read in time limit
            total_errors: Count of errors (counts_as_error=True)
        
        Returns:
            WCPM score
        """
        return max(0, words_read - total_errors)
    
    def compute_accuracy(self, words_read: int, total_errors: int) -> float:
        """
        Compute accuracy percentage.
        
        Args:
            words_read: Total words read in time limit
            total_errors: Count of errors (counts_as_error=True)
        
        Returns:
            Accuracy percentage (0-100)
        """
        if words_read == 0:
            return 0.0
        return ((words_read - total_errors) / words_read) * 100


# Singleton instance
ORF_SCORING_RULES = ORFScoringRules()


def get_scoring_rules() -> ORFScoringRules:
    """Get ORF scoring rules instance"""
    return ORF_SCORING_RULES


# Validation on module load
def _validate_rules():
    """Validate scoring rules integrity"""
    rules = ORF_SCORING_RULES
    
    # Check time limits are positive
    assert rules.time_limit_seconds > 0, "Time limit must be positive"
    assert rules.hesitation_threshold_seconds > 0, "Hesitation threshold must be positive"
    assert rules.self_correction_window_seconds > 0, "Self-correction window must be positive"
    
    # Check all required metrics are defined
    required_metrics = [
        MetricEnum.WORDS_READ.value,
        MetricEnum.TOTAL_ERRORS.value,
        MetricEnum.WCPM.value,
        MetricEnum.ACCURACY_PCT.value
    ]
    
    for metric in required_metrics:
        assert metric in rules.computed_metrics, f"Missing metric: {metric}"
    
    # Test computation functions
    assert rules.compute_wcpm(100, 5) == 95, "WCPM computation failed"
    assert rules.compute_accuracy(100, 5) == 95.0, "Accuracy computation failed"
    assert rules.compute_wcpm(50, 60) == 0, "WCPM should not be negative"
    
    print("✓ Bank 9 (ORF Scoring Rules) validated successfully")


if __name__ == "__main__":
    _validate_rules()
    
    print("\n=== ORF Scoring Rules ===")
    rules = ORF_SCORING_RULES
    
    print(f"\nTiming Parameters:")
    print(f"  Time limit: {rules.time_limit_seconds} seconds")
    print(f"  Hesitation threshold: {rules.hesitation_threshold_seconds} seconds")
    print(f"  Self-correction window: {rules.self_correction_window_seconds} seconds")
    
    print(f"\nSelf-Correction Policy:")
    print(f"  {rules.self_correction_counting_policy}")
    
    print(f"\nComputed Metrics:")
    for metric, spec in rules.computed_metrics.items():
        print(f"  • {metric}")
        print(f"    Source: {spec['source']}")
        print(f"    Description: {spec['description']}")
        if spec['formula']:
            print(f"    Formula: {spec['formula']}")
    
    print(f"\nExample Calculations:")
    print(f"  Words read: 120, Errors: 8")
    print(f"    WCPM: {rules.compute_wcpm(120, 8)}")
    print(f"    Accuracy: {rules.compute_accuracy(120, 8):.1f}%")
