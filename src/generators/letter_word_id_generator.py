"""
Letter-Word Identification Generator (PH-LWID)

Generates letter-word mixes by grade band (40 items).
"""

from typing import Optional
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.generators.simple_assessment_generator import SimpleAssessmentGenerator
from src.banks import word_banks


def create_letter_word_id_generator():
    """Factory function to create Letter-Word ID generator"""
    return LetterWordIDGenerator()


class LetterWordIDGenerator(SimpleAssessmentGenerator):
    """Generator for Letter-Word Identification assessments"""
    
    def __init__(self):
        super().__init__("PH-LWID")
    
    def get_grade_band(self, grade: str) -> str:
        """Convert grade to grade band"""
        if grade == "K":
            return "K"
        elif grade == "1":
            return "G1"
        elif grade in ["2", "3"]:
            return "G2_3"
        else:
            return "K"  # Default
    
    def generate_items(self, grade: str, form_number: int, seed: Optional[int] = None, **kwargs):
        """
        Generate 40 items (mix of letters and words) for grade band.
        
        Args:
            grade: Grade level
            form_number: Form number (used as seed if seed not provided)
            seed: Random seed for reproducibility
            **kwargs: Additional parameters
            
        Returns:
            List of letter/word items
        """
        # Use form_number as seed if seed not provided
        if seed is None:
            seed = form_number
        
        grade_band = self.get_grade_band(grade)
        items_list = word_banks.get_letter_word_mix(grade_band, count=40, seed=seed)
        
        items = []
        for idx, item in enumerate(items_list, 1):
            # Determine if it's a letter (single char, all caps or all lower) or word
            is_letter = len(item) == 1 and (item.isupper() or item.islower())
            
            items.append({
                "item_number": idx,
                "content": item,
                "item_type": "letter" if is_letter else "word"
            })
        
        return items
