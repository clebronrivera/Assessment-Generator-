"""
Assessment Generators Module

This module provides all generator functions for creating assessment components.

Active Generators:
- ORF Generator: Oral Reading Fluency passages
- ORF Assessor Materials: Timing scripts, scoring sheets, rubrics
- QRM Generator: Question Requirements Matrix
- PIB Generator: Passage Information Bank (blueprint)
- Comprehension Passage Generator: Full reading passages
- Question Generator: Multiple-choice and constructed response questions
- Simplified Recall Scoring: Character + detail recall rubrics

Archived Generators:
- recall_scoring_generator.py - Replaced by simplified version (see archived/)

Version: 2026.1
Last Updated: January 14, 2026
"""

from .orf_generator import create_orf_generator
from .orf_assessor_materials_generator import create_orf_assessor_materials_generator
from .qrm_generator import create_qrm_generator
from .pib_generator import create_pib_generator
from .comprehension_passage_generator import create_comprehension_passage_generator
from .question_generator import create_question_generator

# Use NEW simplified recall generator
from .simplified_recall_scoring_generator import create_simplified_recall_scoring_generator

# Alias for backwards compatibility (if needed)
create_recall_scoring_generator = create_simplified_recall_scoring_generator

__all__ = [
    'create_orf_generator',
    'create_orf_assessor_materials_generator',
    'create_qrm_generator',
    'create_pib_generator',
    'create_comprehension_passage_generator',
    'create_question_generator',
    'create_simplified_recall_scoring_generator',
    'create_recall_scoring_generator',  # Alias to simplified version
]

# Version info
__version__ = '2026.1'
__author__ = 'Reading Assessment System'
__deprecated__ = [
    'archived/recall_scoring_generator.py - Use simplified_recall_scoring_generator instead'
]
