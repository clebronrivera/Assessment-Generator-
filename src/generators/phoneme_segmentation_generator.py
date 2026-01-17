"""
Phoneme Segmentation Fluency Generator (FL-PSF)

Generates word lists for phoneme segmentation (20 words).
"""

from typing import Optional
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.generators.simple_assessment_generator import SimpleAssessmentGenerator
from src.banks import word_banks


def create_phoneme_segmentation_generator(assessment_id: str = "FL-PSF"):
    """Factory function to create Phoneme Segmentation generator
    
    Args:
        assessment_id: Assessment ID (FL-PSF or PA-PHON). Defaults to FL-PSF.
    """
    return PhonemeSegmentationGenerator(assessment_id)


class PhonemeSegmentationGenerator(SimpleAssessmentGenerator):
    """Generator for Phoneme Segmentation assessments (FL-PSF or PA-PHON)"""
    
    def __init__(self, assessment_id: str = "FL-PSF"):
        super().__init__(assessment_id)
    
    def generate_items(self, grade: str, form_number: int, seed: Optional[int] = None, **kwargs):
        """
        Generate 20 words for phoneme segmentation.
        
        Args:
            grade: Grade level
            form_number: Form number (used as seed if seed not provided)
            seed: Random seed for reproducibility
            **kwargs: Additional parameters
            
        Returns:
            List of word items
        """
        # Use form_number as seed if seed not provided
        if seed is None:
            seed = form_number
        
        words = word_banks.get_phoneme_segmentation_words(count=20, seed=seed)
        
        items = []
        for idx, word in enumerate(words, 1):
            items.append({
                "item_number": idx,
                "word": word
            })
        
        return items
