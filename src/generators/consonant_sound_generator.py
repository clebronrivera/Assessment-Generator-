"""
Consonant Sound Accuracy Generator (PH-CSA)

Generates consonant letters and digraphs (24 items).
"""

from typing import Optional
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.generators.simple_assessment_generator import SimpleAssessmentGenerator
from src.banks import word_banks


def create_consonant_sound_generator():
    """Factory function to create Consonant Sound Accuracy generator"""
    return ConsonantSoundGenerator()


class ConsonantSoundGenerator(SimpleAssessmentGenerator):
    """Generator for Consonant Sound Accuracy assessments"""
    
    def __init__(self):
        super().__init__("PH-CSA")
    
    def generate_items(self, grade: str, form_number: int, seed: Optional[int] = None, **kwargs):
        """
        Generate 24 consonants/digraphs.
        
        Args:
            grade: Grade level
            form_number: Form number (used as seed if seed not provided)
            seed: Random seed for reproducibility
            **kwargs: Additional parameters
            
        Returns:
            List of consonant items
        """
        # Use form_number as seed if seed not provided
        if seed is None:
            seed = form_number
        
        consonants = word_banks.get_consonants(count=24, seed=seed)
        
        items = []
        for idx, consonant in enumerate(consonants, 1):
            items.append({
                "item_number": idx,
                "consonant": consonant,
                "is_digraph": len(consonant) > 1
            })
        
        return items
