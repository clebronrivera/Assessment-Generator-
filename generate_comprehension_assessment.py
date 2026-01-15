#!/usr/bin/env python3.11
"""
Comprehension Assessment Generator - Command Line Interface
Generates comprehension assessments for specified grades and genres using the AI generation pipeline
"""

import sys
import os
import argparse
from pathlib import Path
import json

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import generators and utilities
from src.generators import (
    create_qrm_generator,
    create_pib_generator,
    create_comprehension_passage_generator,
    create_question_generator,
    create_recall_scoring_generator
)
from src.packaging import create_package_builder
from src.utils import create_ai_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_comprehension_assessment(grade: str, genre: str, band: str = None):
    """Generate a comprehension assessment for the specified grade and genre"""
    
    # Determine band based on grade if not specified
    if band is None:
        if grade in ['1', '2', '3', '4']:
            band = 'early'
        else:
            band = 'late'
    
    print(f"\n{'='*80}")
    print(f"Generating Comprehension Assessment - Grade {grade} {genre.title()} ({band} band)")
    print(f"{'='*80}\n")
    
    try:
        # Initialize AI client
        provider = os.getenv('AI_PROVIDER', 'openai')
        api_key = None
        
        if provider == 'openai':
            api_key = os.getenv('OPENAI_API_KEY')
        elif provider == 'anthropic':
            api_key = os.getenv('ANTHROPIC_API_KEY')
        elif provider == 'gemini':
            api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
            
        if not api_key and provider != 'mock':
            print(f"❌ Error: API key for {provider} not found in environment variables")
            return False
            
        ai_client = create_ai_client(api_key, provider)
        
        # Initialize generators
        qrm_gen = create_qrm_generator(ai_client)
        pib_gen = create_pib_generator(ai_client)
        passage_gen = create_comprehension_passage_generator(ai_client)
        question_gen = create_question_generator(ai_client)
        recall_gen = create_recall_scoring_generator(ai_client)
        package_builder = create_package_builder()
        
        # 1. Generate QRM
        print(f"Step 1: Generating QRM...")
        qrm = qrm_gen.generate(grade=grade, genre=genre, band=band)
        print(f"   ✓ QRM generated: {qrm.total_questions} questions planned")
        
        # 2. Generate PIB
        print(f"Step 2: Generating PIB...")
        pib = pib_gen.generate(qrm_result=qrm)
        print(f"   ✓ PIB generated: {pib.total_scenes} scenes")
        
        # 3. Generate Passage
        print(f"Step 3: Generating passage...")
        passage = passage_gen.generate(qrm_result=qrm, pib_result=pib)
        print(f"   ✓ Passage generated: {passage.actual_word_count} words")
        
        # 4. Generate Questions
        print(f"Step 4: Generating questions...")
        questions = question_gen.generate(qrm_result=qrm, passage_result=passage)
        print(f"   ✓ Questions generated: {questions.total_questions} questions")
        
        # 5. Generate Recall Scoring
        print(f"Step 5: Generating recall scoring...")
        recall = recall_gen.generate(passage_result=passage)
        print(f"   ✓ Recall scoring: {recall.total_sentences} sentences")
        
        # 6. Build Package
        print(f"Step 6: Building comprehension package...")
        package = package_builder.build_comprehension_package(
            qrm_result=qrm,
            pib_result=pib,
            passage_result=passage,
            questions_result=questions,
            recall_result=recall
        )
        
        # 7. Save to samples directory
        output_dir = PROJECT_ROOT / "samples"
        output_dir.mkdir(exist_ok=True)
        
        filename = f"sample_comp_grade{grade}_{genre}"
        
        output_file = output_dir / f"{filename}.json"
        manifest_file = output_dir / f"{filename}_manifest.json"
        
        # Export JSON
        package_builder.export_to_json(package, filepath=str(output_file))
        
        # Create and save manifest
        manifest = package_builder.create_manifest(package)
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Successfully generated comprehension assessment!")
        print(f"  • Package: {output_file}")
        print(f"  • Manifest: {manifest_file}")
        print(f"  • Word Count: {manifest.get('statistics', {}).get('passage_word_count', 0)}")
        print(f"  • Questions: {manifest.get('statistics', {}).get('total_questions', 0)}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error generating comprehension assessment: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    parser = argparse.ArgumentParser(description='Generate Comprehension Assessment')
    parser.add_argument('--grade', required=True, help='Grade level (1, 2, 3, 4, 5, 6)')
    parser.add_argument('--genre', required=True, choices=['narrative', 'nonfiction'], 
                       help='Genre (narrative or nonfiction)')
    parser.add_argument('--band', choices=['early', 'middle', 'late'], help='Reading band')
    
    args = parser.parse_args()
    
    success = generate_comprehension_assessment(args.grade, args.genre, args.band)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
