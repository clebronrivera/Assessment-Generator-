"""
Assessment Registry Module

Complete registry of all assessment types with interface specifications.
"""

from .interfaces import (
    PresentationMode,
    AssessorInteraction,
    TimingMode,
    ClickCyclePattern,
    AssessmentInterface
)
from .registry import ASSESSMENTS, get_assessment, get_assessment_summary

__all__ = [
    'PresentationMode',
    'AssessorInteraction',
    'TimingMode',
    'ClickCyclePattern',
    'AssessmentInterface',
    'ASSESSMENTS',
    'get_assessment',
    'get_assessment_summary'
]
