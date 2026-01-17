"""
Assessment Interface Specifications

Data classes and enums for defining assessment interface behaviors.
"""

from typing import List, Optional
from dataclasses import dataclass
from enum import Enum


class PresentationMode(Enum):
    """How content is shown to student"""
    ONE_AT_A_TIME = "one_at_a_time"  # Single letter/word/item
    FULL_GRID = "full_grid"           # All items visible (letter grid)
    FULL_LIST = "full_list"           # All items in list
    AUDIO_ONLY = "audio_only"         # No visual, assessor speaks


class AssessorInteraction(Enum):
    """How assessor marks responses"""
    CLICK_CYCLE = "click_cycle"              # Click to cycle through states
    YES_NO_BUTTONS = "yes_no_buttons"        # Simple binary
    CORRECT_INCORRECT = "correct_incorrect"   # Binary with no-response
    COUNT_INPUT = "count_input"              # Enter a number (syllables/phonemes)


class TimingMode(Enum):
    """Timing behavior"""
    TIMER_UP = "timer_up"           # Count up, stop manually
    TIMER_DOWN_60 = "timer_down_60" # 60-second countdown
    UNTIMED = "untimed"             # No timer


@dataclass
class ClickCyclePattern:
    """Click state cycle pattern"""
    states: List[str]  # e.g., ["correct", "incorrect", "self_correct", "omission", "omission", "reset"]
    
    def get_next_state(self, current: str) -> str:
        """Get next state in cycle"""
        try:
            idx = self.states.index(current)
            return self.states[(idx + 1) % len(self.states)]
        except ValueError:
            return self.states[0]
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {"states": self.states}


@dataclass
class AssessmentInterface:
    """Complete UI/UX specification for an assessment"""
    
    # Student View
    student_presentation: PresentationMode
    student_sees_text: bool
    items_advance_mode: str  # "auto_after_click", "manual_next_button", "n/a"
    
    # Assessor View
    assessor_interaction: AssessorInteraction
    click_cycle: Optional[ClickCyclePattern]
    
    # Timing
    timing_mode: TimingMode
    timer_direction: str  # "up", "down", "none"
    timer_visible_to_student: bool
    
    # Instructions
    assessor_script: List[str]
    student_prompt: str
    
    # NEW: ORF-specific extensions (schema v2026.2)
    passage_marking_enabled: bool = False
    rubric_scoring_enabled: bool = False
    time_limit_seconds: Optional[int] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        result = {
            "student_presentation": self.student_presentation.value,
            "student_sees_text": self.student_sees_text,
            "items_advance_mode": self.items_advance_mode,
            "assessor_interaction": self.assessor_interaction.value,
            "click_cycle": self.click_cycle.to_dict() if self.click_cycle else None,
            "timing_mode": self.timing_mode.value,
            "timer_direction": self.timer_direction,
            "timer_visible_to_student": self.timer_visible_to_student,
            "assessor_script": self.assessor_script,
            "student_prompt": self.student_prompt
        }
        
        # Include new fields if set
        if self.passage_marking_enabled:
            result["passage_marking_enabled"] = self.passage_marking_enabled
        if self.rubric_scoring_enabled:
            result["rubric_scoring_enabled"] = self.rubric_scoring_enabled
        if self.time_limit_seconds is not None:
            result["time_limit_seconds"] = self.time_limit_seconds
        
        return result

