"""
Rhyme Recognition Generator (PA-RHYM)

Generates word pairs for rhyme recognition (20 pairs, rhyming and non-rhyming).
"""

from typing import Optional
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.generators.simple_assessment_generator import SimpleAssessmentGenerator
from src.banks import word_banks


def create_rhyme_recognition_generator():
    """Factory function to create Rhyme Recognition generator"""
    return RhymeRecognitionGenerator()


class RhymeRecognitionGenerator(SimpleAssessmentGenerator):
    """Generator for Rhyme Recognition assessments"""
    
    def __init__(self):
        super().__init__("PA-RHYM")
    
    def generate_items(self, grade: str, form_number: int, seed: Optional[int] = None, **kwargs):
        """
        Generate 20 word pairs for rhyme recognition.
        
        Args:
            grade: Grade level
            form_number: Form number (used as seed if seed not provided)
            seed: Random seed for reproducibility
            **kwargs: Additional parameters
            
        Returns:
            List of word pair items
        """
        # Use form_number as seed if seed not provided
        if seed is None:
            seed = form_number
        
        pairs = word_banks.get_rhyming_pairs(count=20, seed=seed)
        
        items = []
        for idx, pair in enumerate(pairs, 1):
            items.append({
                "item_number": idx,
                "word1": pair["word1"],
                "word2": pair["word2"],
                "correct_answer": pair["rhymes"],  # True if they rhyme
                "expected_response": "yes" if pair["rhymes"] else "no"
            })
        
        return items
