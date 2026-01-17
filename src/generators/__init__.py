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
- Picture Description Generator: Illustrator-ready descriptions for K-1 passages
- Text Feature Injector: Adds headings and organizational features for grades 6+

Archived Generators:
- recall_scoring_generator.py - Replaced by simplified version (see archived/)

Version: 2026.1
Last Updated: January 15, 2026
"""

from .orf_generator import create_orf_generator
from .orf_assessor_materials_generator import create_orf_assessor_materials_generator
from .qrm_generator import create_qrm_generator
from .pib_generator import create_pib_generator
from .comprehension_passage_generator import create_comprehension_passage_generator
from .question_generator import create_question_generator

# Use NEW simplified recall generator
from .simplified_recall_scoring_generator import create_simplified_recall_scoring_generator

# Phase 2B Optional Generators
from .picture_description_generator import create_picture_description_generator
from .text_feature_injector import create_text_feature_injector

# Alias for backwards compatibility (if needed)
create_recall_scoring_generator = create_simplified_recall_scoring_generator

# Phase 2B Optional Generators
from .picture_description_generator import create_picture_description_generator
from .text_feature_injector import create_text_feature_injector

# Simple Assessment Generators (non-AI)
from .letter_recognition_generator import create_letter_recognition_generator
from .word_reading_fluency_generator import create_word_reading_fluency_generator
from .phoneme_segmentation_generator import create_phoneme_segmentation_generator
from .rhyme_recognition_generator import create_rhyme_recognition_generator
from .onset_rime_generator import create_onset_rime_generator
from .syllable_segmentation_generator import create_syllable_segmentation_generator
from .consonant_sound_generator import create_consonant_sound_generator
from .letter_word_id_generator import create_letter_word_id_generator
from .cvc_blending_generator import create_cvc_blending_generator

__all__ = [
    'create_orf_generator',
    'create_orf_assessor_materials_generator',
    'create_qrm_generator',
    'create_pib_generator',
    'create_comprehension_passage_generator',
    'create_question_generator',
    'create_simplified_recall_scoring_generator',
    'create_recall_scoring_generator',  # Alias to simplified version
    # Phase 2B Optional Generators
    'create_picture_description_generator',
    'create_text_feature_injector',
    # Simple assessment generators
    'create_letter_recognition_generator',
    'create_word_reading_fluency_generator',
    'create_phoneme_segmentation_generator',
    'create_rhyme_recognition_generator',
    'create_onset_rime_generator',
    'create_syllable_segmentation_generator',
    'create_consonant_sound_generator',
    'create_letter_word_id_generator',
    'create_cvc_blending_generator',
]

# Version info
__version__ = '2026.1'
__author__ = 'Reading Assessment System'
__deprecated__ = [
    'archived/recall_scoring_generator.py - Use simplified_recall_scoring_generator instead'
]
