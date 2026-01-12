#!/usr/bin/env python3
"""
Test script to validate and demonstrate all foundation banks.
Run this to verify all banks are working correctly.
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from banks import (
    validate_all_banks,
    get_assessment_specs,
    export_all_banks_to_json,
    get_lexile_range,
    get_orf_target,
    get_blueprint,
    get_form_requirements,
    get_num_options,
    get_structure_names
)


def main():
    print("\n" + "="*70)
    print("READING ASSESSMENT GENERATOR - FOUNDATION BANKS TEST")
    print("="*70)
    
    # Step 1: Validate all banks
    print("\n[STEP 1] Validating all banks...")
    if not validate_all_banks():
        print("❌ Validation failed. Exiting.")
        sys.exit(1)
    
    # Step 2: Test individual lookups
    print("\n[STEP 2] Testing individual bank lookups...")
    print("-" * 70)
    
    # Test Lexile lookup
    print("\n📊 Bank 1: Lexile Ranges")
    lexile = get_lexile_range("2", "early")
    print(f"   Grade 2 Early: {lexile}")
    
    # Test ORF lookup
    print("\n📖 Bank 2: ORF Word Counts")
    orf = get_orf_target("2")
    print(f"   Grade 2 ORF: {orf}")
    
    # Test Comprehension Blueprint
    print("\n📝 Bank 4: Comprehension Blueprint")
    blueprint = get_blueprint("3")
    print(f"   Grade 3: {blueprint}")
    print(f"   Questions: {blueprint.distribution.to_dict()}")
    
    # Test Form Requirements
    print("\n📋 Bank 5: Form Requirements")
    form_req = get_form_requirements("3", "comprehension")
    print(f"   Grade 3 Comprehension: {form_req}")
    
    # Test Answer Options
    print("\n🎯 Bank 6: Answer Options")
    print(f"   K: {get_num_options('K')} options")
    print(f"   Grade 2: {get_num_options('2')} options")
    print(f"   Grade 5: {get_num_options('5')} options")
    
    # Test Text Structures
    print("\n📐 Bank 7: Text Structures")
    print(f"   Narrative structures: {', '.join(get_structure_names('narrative'))}")
    print(f"   Nonfiction structures: {', '.join(get_structure_names('nonfiction'))}")
    
    # Step 3: Test unified specs getter
    print("\n[STEP 3] Testing unified specs getter...")
    print("-" * 70)
    
    test_cases = [
        ("K", "comprehension", "early"),
        ("2", "orf", "early"),
        ("3", "comprehension", "late"),
        ("5", "comprehension", "early"),
        ("8+", "comprehension", "late")
    ]
    
    for grade, assessment_type, band in test_cases:
        print(f"\n📌 Grade {grade} {assessment_type.upper()} ({band}):")
        specs = get_assessment_specs(grade, assessment_type, band)
        
        # Print key specs
        print(f"   Lexile: {specs.get('lexile_range', 'N/A')}")
        print(f"   Word count: {specs.get('word_count', 'N/A')} (range: {specs.get('word_count_range', 'N/A')})")
        
        if assessment_type == "comprehension":
            print(f"   Questions: {specs.get('total_questions', 'N/A')}")
            print(f"   Answer options: {specs.get('num_answer_options', 'N/A')}")
            print(f"   Picture required: {specs.get('requires_picture', False)}")
            print(f"   Text features required: {specs.get('requires_text_features', False)}")
    
    # Step 4: Test form generation scenarios
    print("\n[STEP 4] Testing form generation scenarios...")
    print("-" * 70)
    
    from banks.form_requirements import generate_form_id, calculate_total_forms
    
    scenarios = [
        ("2", "comprehension", "narrative"),
        ("3", "comprehension", "both"),
        ("5", "orf", "narrative"),
        ("8+", "comprehension", "nonfiction")
    ]
    
    for grade, assessment_type, genre in scenarios:
        num_forms = calculate_total_forms(grade, assessment_type, genre)
        print(f"\n📦 Grade {grade} {assessment_type} ({genre}): {num_forms} forms")
        
        # Show sample form IDs
        bands = ["early", "late"]
        genres = ["narrative", "nonfiction"] if genre == "both" else [genre]
        
        for band in bands:
            for g in genres:
                form_id = generate_form_id(grade, assessment_type, band, g)
                print(f"   - {form_id}")
    
    # Step 5: Export to JSON
    print("\n[STEP 5] Testing JSON export...")
    print("-" * 70)
    
    export_data = export_all_banks_to_json()
    print(f"✅ Successfully exported all banks")
    print(f"   Banks included: {', '.join(export_data['banks'].keys())}")
    print(f"   Bank version: {export_data['version']}")
    
    # Save to file
    output_file = Path(__file__).parent / "banks_export.json"
    with open(output_file, 'w') as f:
        json.dump(export_data, f, indent=2)
    print(f"   Saved to: {output_file}")
    
    # Final summary
    print("\n" + "="*70)
    print("✅ ALL TESTS PASSED")
    print("="*70)
    print("\nFoundation banks are ready for use in generators!")
    print("\nNext steps:")
    print("  1. Build generator templates (ORF, Comprehension, Questions, Recall)")
    print("  2. Create validation system")
    print("  3. Implement API endpoints")
    print("  4. Build frontend UI")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
