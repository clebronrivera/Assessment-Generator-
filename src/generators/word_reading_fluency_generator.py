"""
Word Reading Fluency Generator (FL-WRF)

Generates word lists by grade (K-3) with 50 words each.
"""

from typing import Optional
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.generators.simple_assessment_generator import SimpleAssessmentGenerator
from src.banks import word_banks


def create_word_reading_fluency_generator():
    """Factory function to create Word Reading Fluency generator"""
    return WordReadingFluencyGenerator()


class WordReadingFluencyGenerator(SimpleAssessmentGenerator):
    """Generator for Word Reading Fluency assessments"""
    
    def __init__(self):
        super().__init__("FL-WRF")
    
    def generate_items(self, grade: str, form_number: int, seed: Optional[int] = None, **kwargs):
        """
        Generate 50 words for the specified grade.
        
        Args:
            grade: Grade level (K, 1, 2, or 3)
            form_number: Form number (used as seed if seed not provided)
            seed: Random seed for reproducibility
            **kwargs: Additional parameters
            
        Returns:
            List of word items
        """
        # Use form_number as seed if seed not provided
        if seed is None:
            seed = form_number
        
        # Get Dolch sight words for this grade (FL-WRF uses Dolch words, not CVC)
        words = word_banks.get_dolch_words_by_grade(grade)
        
        # If we need 50 but have less, repeat the list
        while len(words) < 50:
            words.extend(word_banks.get_dolch_words_by_grade(grade))
        
        # Shuffle with seed for consistency
        import random
        random.seed(seed)
        shuffled = words.copy()
        random.shuffle(shuffled)
        
        items = []
        for idx, word in enumerate(shuffled[:50], 1):
            items.append({
                "item_number": idx,
                "word": word
            })
        
        return items
