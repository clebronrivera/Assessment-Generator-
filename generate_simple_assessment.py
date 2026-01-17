#!/usr/bin/env python3
"""
Generate Simple Assessment Forms

Generates forms for simple assessment types (Letter Recognition, Word Reading Fluency, etc.)
without requiring AI.

Usage:
    python generate_simple_assessment.py --assessment-id LR-ALPH --grade K
    python generate_simple_assessment.py --assessment-id FL-WRF --grade 1 --form-number 2
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.assessments.registry import get_assessment, ASSESSMENTS
from src.generators import (
    create_letter_recognition_generator,
    create_word_reading_fluency_generator,
    create_phoneme_segmentation_generator,
    create_rhyme_recognition_generator,
    create_onset_rime_generator,
    create_syllable_segmentation_generator,
    create_consonant_sound_generator,
    create_letter_word_id_generator,
    create_cvc_blending_generator
)


# Mapping of assessment IDs to generator factories
GENERATOR_MAP = {
    "LR-ALPH": create_letter_recognition_generator,
    "FL-WRF": create_word_reading_fluency_generator,
    "FL-PSF": create_phoneme_segmentation_generator,
    "PA-RHYM": create_rhyme_recognition_generator,
    "PA-OONS": create_onset_rime_generator,
    "PA-PHON": create_phoneme_segmentation_generator,  # Reuse PSF generator
    "PA-SYLS": create_syllable_segmentation_generator,
    "PH-CSA": create_consonant_sound_generator,
    "PH-LWID": create_letter_word_id_generator,
    "PH-CVC": create_cvc_blending_generator
}


def generate_simple_assessment(assessment_id: str, grade: str, form_number: int = None, 
                                samples_dir: Path = None):
    """
    Generate a simple assessment form.
    
    Args:
        assessment_id: Assessment ID from registry (e.g., "LR-ALPH")
        grade: Grade level (e.g., "K", "1", "2")
        form_number: Optional form number (auto-increments if not provided)
        samples_dir: Directory to save samples (defaults to PROJECT_ROOT/samples)
    """
    if samples_dir is None:
        samples_dir = PROJECT_ROOT / "samples"
    
    # Normalize assessment_id (uppercase, strip whitespace)
    if not assessment_id:
        print(f"❌ Error: Assessment ID is required")
        return False
        
    assessment_id_normalized = assessment_id.upper().strip()
    
    # Validate assessment exists
    assessment = get_assessment(assessment_id_normalized)
    if not assessment:
        print(f"❌ Error: Assessment '{assessment_id}' (normalized: '{assessment_id_normalized}') not found in registry")
        print(f"   Available assessments: {', '.join(ASSESSMENTS.keys())}")
        return False
    
    # Get generator factory - use normalized ID
    generator_factory = GENERATOR_MAP.get(assessment_id_normalized)
    if not generator_factory:
        print(f"❌ Error: No generator available for assessment '{assessment_id_normalized}'")
        print(f"   Available generators: {', '.join(GENERATOR_MAP.keys())}")
        return False
    
    print(f"\n{'='*80}")
    print(f"📋 Generating: {assessment['name']} (Grade {grade})")
    print(f"{'='*80}\n")
    
    try:
        # Create generator - pass assessment_id if factory accepts it
        if assessment_id_normalized in ["FL-PSF", "PA-PHON"]:
            # Phoneme segmentation generator accepts assessment_id
            generator = generator_factory(assessment_id_normalized)
        else:
            generator = generator_factory()
        
        # Generate form - use normalized ID for consistency
        output = generator.generate(
            grade=grade,
            form_number=form_number,
            samples_dir=samples_dir
        )
        
        # Validate
        if not generator.validate(output):
            print(f"❌ Validation failed for generated form")
            return False
        
        print(f"✅ Successfully generated Form {output['form_number']}")
        print(f"   Form ID: {output['form_id']}")
        print(f"   Items: {len(output['items'])}")
        print(f"   Saved to: {samples_dir / (output['metadata']['assessment_id'].lower() + '_form' + str(output['form_number']) + '_' + grade + '.json')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating assessment: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate simple assessment forms",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate Letter Recognition for Kindergarten (auto-form-number)
  python generate_simple_assessment.py --assessment-id LR-ALPH --grade K
  
  # Generate Word Reading Fluency Grade 1, Form 2
  python generate_simple_assessment.py --assessment-id FL-WRF --grade 1 --form-number 2
  
Available Assessment IDs:
  LR-ALPH  - Letter Recognition
  FL-WRF   - Word Reading Fluency
  FL-PSF   - Phoneme Segmentation Fluency
  PA-RHYM  - Rhyme Recognition
  PA-OONS  - Onset-Rime Blending
  PA-PHON  - Phoneme Segmentation
  PA-SYLS  - Syllable Segmentation
  PH-CSA   - Consonant Sound Accuracy
  PH-CVC   - CVC Blending
  PH-LWID  - Letter-Word Identification
        """
    )
    
    parser.add_argument(
        '--assessment-id',
        required=True,
        help='Assessment ID from registry (e.g., LR-ALPH, FL-WRF)'
    )
    
    parser.add_argument(
        '--grade',
        required=True,
        help='Grade level (K, 1, 2, 3, etc.)'
    )
    
    parser.add_argument(
        '--form-number',
        type=int,
        default=None,
        help='Form number (auto-increments if not specified)'
    )
    
    parser.add_argument(
        '--samples-dir',
        type=Path,
        default=None,
        help='Directory to save samples (defaults to PROJECT_ROOT/samples)'
    )
    
    args = parser.parse_args()
    
    # Convert samples_dir
    samples_dir = args.samples_dir if args.samples_dir else None
    
    success = generate_simple_assessment(
        assessment_id=args.assessment_id.upper(),
        grade=args.grade,
        form_number=args.form_number,
        samples_dir=samples_dir
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
