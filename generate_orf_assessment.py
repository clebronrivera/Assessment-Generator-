#!/usr/bin/env python3.11
"""
ORF Assessment Generator - Command Line Interface
Generates ORF assessments for specified grades using the AI generation pipeline
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
    create_orf_generator,
    create_orf_assessor_materials_generator
)
from src.packaging import create_package_builder
from src.utils import create_ai_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_orf_assessment(grade: str, band: str = None):
    """Generate an ORF assessment for the specified grade"""
    
    # Determine band based on grade if not specified
    if band is None:
        if grade in ['K', '1', '2', '3']:
            band = 'early'
        else:
            band = 'late'
    
    print(f"\n{'='*80}")
    print(f"Generating ORF Assessment - Grade {grade} ({band} band)")
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
        orf_gen = create_orf_generator(ai_client)
        materials_gen = create_orf_assessor_materials_generator()
        package_builder = create_package_builder()
        
        # 1. Generate Passage
        print(f"Step 1: Generating ORF passage for Grade {grade}...")
        passage = orf_gen.generate(grade=grade, band=band)
        
        # Handle different return types (dict vs object)
        if isinstance(passage, dict):
            word_count = passage['metadata']['actual_word_count']
            passage_text = passage['passage_text']
            form_id = passage['metadata'].get('form_id', f'ORF-G{grade}-{band.upper()}-001')
        else:
            word_count = passage.metadata['actual_word_count']
            passage_text = passage.passage_text
            form_id = passage.metadata.get('form_id', f'ORF-G{grade}-{band.upper()}-001')
            
        print(f"   ✓ Passage generated: {word_count} words")
        
        # 2. Generate Materials
        print(f"Step 2: Generating assessor materials...")
        materials = materials_gen.generate(
            grade=grade,
            passage_text=passage_text,
            passage_word_count=word_count,
            form_id=form_id
        )
        print(f"   ✓ Materials generated: {materials.form_id}")
        
        # 3. Build Package
        print(f"Step 3: Building ORF package...")
        package = package_builder.build_orf_package(passage, materials)
        
        # 4. Save to samples directory
        output_dir = PROJECT_ROOT / "samples"
        output_dir.mkdir(exist_ok=True)
        
        filename = f"sample_orf_grade{grade}"
        # Note: We use the base filename without band to match Assessment Matrix expectations
        # if band:
        #    filename += f"_{band}"
        
        output_file = output_dir / f"{filename}.json"
        manifest_file = output_dir / f"{filename}_manifest.json"
        
        # Export JSON
        package_builder.export_to_json(package, filepath=str(output_file))
        
        # Create and save manifest
        manifest = package_builder.create_manifest(package)
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Successfully generated ORF assessment!")
        print(f"  • Package: {output_file}")
        print(f"  • Manifest: {manifest_file}")
        print(f"  • Word Count: {manifest.get('statistics', {}).get('passage_word_count', 0)}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error generating ORF assessment: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    parser = argparse.ArgumentParser(description='Generate ORF Assessment')
    parser.add_argument('--grade', required=True, help='Grade level (K, 1, 2, 3, 4, 5, 6)')
    parser.add_argument('--band', choices=['early', 'middle', 'late'], help='Reading band')
    
    args = parser.parse_args()
    
    success = generate_orf_assessment(args.grade, args.band)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
