"""
Letter Recognition Generator (LR-ALPH)

Generates forms with all 52 letters (upper + lowercase) in scrambled order.
"""

from typing import Optional
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.generators.simple_assessment_generator import SimpleAssessmentGenerator
from src.banks import word_banks


def create_letter_recognition_generator():
    """Factory function to create Letter Recognition generator"""
    return LetterRecognitionGenerator()


class LetterRecognitionGenerator(SimpleAssessmentGenerator):
    """Generator for Letter Recognition assessments"""
    
    def __init__(self):
        super().__init__("LR-ALPH")
    
    def generate_items(self, grade: str, form_number: int, seed: Optional[int] = None, **kwargs):
        """
        Generate 52 letters in scrambled order.
        
        Args:
            grade: Grade level (not used for letters, but kept for consistency)
            form_number: Form number (used as seed if seed not provided)
            seed: Random seed for reproducibility
            **kwargs: Additional parameters
            
        Returns:
            List of letter items
        """
        # Use form_number as seed if seed not provided for consistency
        if seed is None:
            seed = form_number
        
        letters = word_banks.get_all_letters(scrambled=True, seed=seed)
        
        items = []
        for idx, letter in enumerate(letters, 1):
            items.append({
                "item_number": idx,
                "letter": letter,
                "is_uppercase": letter.isupper()
            })
        
        return items
