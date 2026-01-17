"""
Syllable Segmentation Generator (PA-SYLS)

Generates words with syllable counts for segmentation (20 words).
"""

from typing import Optional
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.generators.simple_assessment_generator import SimpleAssessmentGenerator
from src.banks import word_banks


def create_syllable_segmentation_generator():
    """Factory function to create Syllable Segmentation generator"""
    return SyllableSegmentationGenerator()


class SyllableSegmentationGenerator(SimpleAssessmentGenerator):
    """Generator for Syllable Segmentation assessments"""
    
    def __init__(self):
        super().__init__("PA-SYLS")
    
    def generate_items(self, grade: str, form_number: int, seed: Optional[int] = None, **kwargs):
        """
        Generate 20 words with syllable counts.
        
        Args:
            grade: Grade level
            form_number: Form number (used as seed if seed not provided)
            seed: Random seed for reproducibility
            **kwargs: Additional parameters
            
        Returns:
            List of word items with syllable counts
        """
        # Use form_number as seed if seed not provided
        if seed is None:
            seed = form_number
        
        words = word_banks.get_syllable_words(count=20, seed=seed)
        
        items = []
        for idx, word_data in enumerate(words, 1):
            items.append({
                "item_number": idx,
                "word": word_data["word"],
                "correct_syllable_count": word_data["syllable_count"]
            })
        
        return items
