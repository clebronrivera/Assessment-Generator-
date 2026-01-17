"""
Bank 11: Prosody Scales

Formal prosody scoring rubrics for oral reading fluency.
Structured representation of NAEP Multidimensional Fluency Scale.

Created: 2026-01-16
Schema Version: 2026.2
"""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ProsodyScaleLevel:
    """Single level of prosody scale"""
    score: int
    label: str
    descriptor: str
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON export"""
        return {
            "score": self.score,
            "label": self.label,
            "descriptor": self.descriptor
        }


@dataclass(frozen=True)
class ProsodyScale:
    """Complete prosody scoring rubric"""
    scale_name: str
    score_range: tuple
    levels: tuple  # Use tuple for immutability
    scoring_type: str = "rubric"
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON export"""
        return {
            "scale_name": self.scale_name,
            "score_range": list(self.score_range),
            "levels": [level.to_dict() for level in self.levels],
            "scoring_type": self.scoring_type
        }
    
    def get_level(self, score: int) -> ProsodyScaleLevel:
        """Get level descriptor for a given score"""
        for level in self.levels:
            if level.score == score:
                return level
        raise ValueError(f"Invalid score: {score}. Must be in range {self.score_range}")


# NAEP Multidimensional Fluency Scale (Prosody)
NAEP_PROSODY_SCALE = ProsodyScale(
    scale_name="NAEP Multidimensional Fluency Scale",
    score_range=(1, 4),
    levels=(
        ProsodyScaleLevel(
            score=1,
            label="Word-by-word",
            descriptor="Reads primarily word-by-word with occasional two-word phrases. "
                       "Lacks expression. Ignores most punctuation. Very choppy reading."
        ),
        ProsodyScaleLevel(
            score=2,
            label="Two-word phrases",
            descriptor="Reads with a mixture of two-word phrases and occasional three-to-four-word phrases. "
                       "Limited expression. Monotone. Frequent hesitations and pauses."
        ),
        ProsodyScaleLevel(
            score=3,
            label="Mixed phrasing",
            descriptor="Reads with a mixture of run-ons, mid-sentence pauses for breath, and some choppiness. "
                       "Reasonable syntax. Expressive interpretation. Generally flows but uneven."
        ),
        ProsodyScaleLevel(
            score=4,
            label="Good phrasing",
            descriptor="Reads with good phrasing; adheres to author's syntax. Uses expression to convey meaning. "
                       "Attention to punctuation. Smooth, conversational pace throughout."
        )
    )
)


def get_prosody_scale() -> ProsodyScale:
    """Get NAEP prosody scale instance"""
    return NAEP_PROSODY_SCALE


def validate_prosody_score(score: int) -> bool:
    """
    Validate that a prosody score is within valid range.
    
    Args:
        score: Prosody score to validate
    
    Returns:
        True if valid, False otherwise
    """
    min_score, max_score = NAEP_PROSODY_SCALE.score_range
    return min_score <= score <= max_score


# Validation on module load
def _validate_scale():
    """Validate prosody scale integrity"""
    scale = NAEP_PROSODY_SCALE
    
    # Check score range is valid
    min_score, max_score = scale.score_range
    assert min_score < max_score, "Invalid score range"
    assert min_score == 1, "Score range should start at 1"
    
    # Check all levels in range are defined
    expected_scores = set(range(min_score, max_score + 1))
    found_scores = {level.score for level in scale.levels}
    
    assert found_scores == expected_scores, \
        f"Missing prosody levels: {expected_scores - found_scores}"
    
    # Check levels are in order
    scores = [level.score for level in scale.levels]
    assert scores == sorted(scores), "Prosody levels not in order"
    
    # Check all levels have descriptors
    for level in scale.levels:
        assert len(level.descriptor) > 0, f"Level {level.score} missing descriptor"
        assert len(level.label) > 0, f"Level {level.score} missing label"
    
    # Test get_level function
    for score in range(min_score, max_score + 1):
        level = scale.get_level(score)
        assert level.score == score, f"get_level({score}) returned wrong level"
    
    print("✓ Bank 11 (Prosody Scales) validated successfully")


if __name__ == "__main__":
    _validate_scale()
    
    print("\n=== Prosody Scale ===")
    scale = NAEP_PROSODY_SCALE
    
    print(f"\nScale Name: {scale.scale_name}")
    print(f"Score Range: {scale.score_range[0]}-{scale.score_range[1]}")
    print(f"Scoring Type: {scale.scoring_type}")
    
    print(f"\nLevels:")
    for level in scale.levels:
        print(f"\n  Score {level.score}: {level.label}")
        print(f"  {level.descriptor}")
    
    print(f"\nValidation Examples:")
    print(f"  Score 1 valid: {validate_prosody_score(1)}")
    print(f"  Score 4 valid: {validate_prosody_score(4)}")
    print(f"  Score 5 valid: {validate_prosody_score(5)}")
