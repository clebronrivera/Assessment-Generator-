"""
CVC Blending Generator (PH-CVC)

Generates CVC (Consonant-Vowel-Consonant) word lists for phonics blending assessment.
20 items with 4 words each for A, E, I, O, U medial vowels.
Optionally includes 5 nonsense words for pure decoding assessment.
"""

from typing import Optional, List, Dict
from pathlib import Path
import sys
import random

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.generators.simple_assessment_generator import SimpleAssessmentGenerator
from src.banks import word_banks

# CVC words organized by medial vowel
CVC_BY_VOWEL = {
    'a': ['cat', 'bat', 'hat', 'sat', 'mat', 'rat', 'pat', 'fat', 'can', 'man', 'pan', 'van', 'tan', 'ran', 'fan', 'ban'],
    'e': ['bed', 'red', 'led', 'wed', 'get', 'let', 'pet', 'met', 'net', 'set', 'bet', 'wet', 'hen', 'pen', 'ten', 'men'],
    'i': ['sit', 'bit', 'fit', 'hit', 'pit', 'wit', 'big', 'pig', 'wig', 'dig', 'fig', 'rig', 'pin', 'tin', 'win', 'fin'],
    'o': ['hot', 'pot', 'lot', 'dot', 'got', 'not', 'top', 'mop', 'hop', 'pop', 'cop', 'fox', 'box', 'fox', 'log', 'dog'],
    'u': ['cup', 'pup', 'bus', 'us', 'run', 'fun', 'sun', 'bun', 'gun', 'nut', 'cut', 'hut', 'mud', 'bud', 'cub', 'tub']
}

# Consonants for generating nonsense words
CONSONANTS = list('bcdfghjklmnpqrstvwxyz')
VOWELS = list('aeiou')


def create_cvc_blending_generator():
    """Factory function to create CVC Blending generator"""
    return CVCBlendingGenerator()


def generate_nonsense_cvc_word(exclude_words: List[str] = None, seed: Optional[int] = None) -> str:
    """Generate a nonsense CVC word for pure decoding assessment"""
    if exclude_words is None:
        # Build list of all real CVC words
        exclude_words = []
        for vowel_words in CVC_BY_VOWEL.values():
            exclude_words.extend(vowel_words)
    
    max_attempts = 50
    for attempt in range(max_attempts):
        # Use attempt number to vary the seed
        if seed is not None:
            random.seed(seed + attempt * 1000)
        else:
            random.seed(attempt * 1000)
        
        # Pick random consonant, vowel, consonant
        c1 = random.choice(CONSONANTS)
        v = random.choice(VOWELS)
        c2 = random.choice(CONSONANTS)
        
        word = c1 + v + c2
        
        # Make sure it's not a real word
        if word.lower() not in [w.lower() for w in exclude_words]:
            return word
    
    # Fallback: return a word with 'x' which is less common in real CVC words
    return f"x{random.choice(VOWELS)}x"


class CVCBlendingGenerator(SimpleAssessmentGenerator):
    """Generator for CVC Blending assessments"""
    
    def __init__(self):
        super().__init__("PH-CVC")
    
    def generate_items(self, grade: str, form_number: int, seed: Optional[int] = None, include_nonsense: bool = True, **kwargs):
        """
        Generate 20 CVC words (4 each for A, E, I, O, U) plus optionally 5 nonsense words.
        
        Args:
            grade: Grade level (typically K or 1)
            form_number: Form number (used as seed if seed not provided)
            seed: Random seed for reproducibility
            include_nonsense: Whether to include 5 nonsense words (default: True)
            **kwargs: Additional parameters
            
        Returns:
            List of CVC word items
        """
        # Use form_number as seed if seed not provided
        if seed is None:
            seed = form_number
        
        random.seed(seed)
        items = []
        item_number = 1
        
        # Generate 4 words for each vowel (A, E, I, O, U) = 20 words
        for vowel in ['a', 'e', 'i', 'o', 'u']:
            vowel_words = CVC_BY_VOWEL[vowel].copy()
            random.shuffle(vowel_words)
            
            # Take 4 words for this vowel
            for word in vowel_words[:4]:
                items.append({
                    "item_number": item_number,
                    "word": word,
                    "medial_vowel": vowel
                })
                item_number += 1
        
        # Optionally add 5 nonsense words
        if include_nonsense:
            # Build list of real words to exclude
            all_real_words = []
            for vowel_words in CVC_BY_VOWEL.values():
                all_real_words.extend(vowel_words)
            
            for i in range(5):
                nonsense_word = generate_nonsense_cvc_word(
                    exclude_words=all_real_words,
                    seed=seed + 1000 + i
                )
                items.append({
                    "item_number": item_number,
                    "word": nonsense_word,
                    "is_nonsense": True
                })
                item_number += 1
        
        return items
