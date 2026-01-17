"""
Onset-Rime Blending Generator (PA-OONS)

Generates onset-rime pairs for blending (20 pairs).
"""

from typing import Optional
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.generators.simple_assessment_generator import SimpleAssessmentGenerator
from src.banks import word_banks


def create_onset_rime_generator():
    """Factory function to create Onset-Rime generator"""
    return OnsetRimeGenerator()


class OnsetRimeGenerator(SimpleAssessmentGenerator):
    """Generator for Onset-Rime Blending assessments"""
    
    def __init__(self):
        super().__init__("PA-OONS")
    
    def generate_items(self, grade: str, form_number: int, seed: Optional[int] = None, **kwargs):
        """
        Generate 20 onset-rime pairs.
        
        Args:
            grade: Grade level
            form_number: Form number (used as seed if seed not provided)
            seed: Random seed for reproducibility
            **kwargs: Additional parameters
            
        Returns:
            List of onset-rime items
        """
        # Use form_number as seed if seed not provided
        if seed is None:
            seed = form_number
        
        pairs = word_banks.get_onset_rime_pairs(count=20, seed=seed)
        
        items = []
        for idx, pair in enumerate(pairs, 1):
            items.append({
                "item_number": idx,
                "onset": pair["onset"],
                "rime": pair["rime"],
                "correct_word": pair["word"]
            })
        
        return items
