"""
System Verification Script
Checks that all components are properly integrated
"""

import os
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))


def verify_structure():
    """Verify all required files exist"""
    
    required_files = {
        "Registry System": [
            "src/assessments/__init__.py",
            "src/assessments/interfaces.py",
            "src/assessments/registry.py"
        ],
        "Word Banks": [
            "src/banks/word_banks.py"
        ],
        "Generators": [
            "src/generators/simple_assessment_generator.py",
            "src/generators/letter_recognition_generator.py",
            "src/generators/word_reading_fluency_generator.py",
            "src/generators/phoneme_segmentation_generator.py",
            "src/generators/rhyme_recognition_generator.py",
            "src/generators/onset_rime_generator.py",
            "src/generators/syllable_segmentation_generator.py",
            "src/generators/consonant_sound_generator.py",
            "src/generators/letter_word_id_generator.py"
        ],
        "Dashboard": [
            "dashboard/app.py",
            "dashboard/templates/matrix.html",
            "dashboard/templates/index.html"
        ],
        "Utils": [
            "src/utils/assessment_matrix.py"
        ],
        "CLI Tools": [
            "generate_simple_assessment.py"
        ]
    }
    
    print("="*70)
    print("SYSTEM VERIFICATION")
    print("="*70)
    
    all_good = True
    
    for category, files in required_files.items():
        print(f"\n{category}:")
        for file_path in files:
            exists = os.path.exists(file_path)
            status = "✓" if exists else "✗"
            print(f"  {status} {file_path}")
            if not exists:
                all_good = False
    
    # Check samples directory
    print("\nSamples Directory:")
    samples_dir = Path("samples")
    if samples_dir.exists():
        json_files = list(samples_dir.glob("*.json"))
        manifest_files = list(samples_dir.glob("*_manifest.json"))
        print(f"  ✓ samples/ ({len(json_files)} JSON files, {len(manifest_files)} manifests)")
    else:
        print(f"  ○ samples/ (will be created on first generation)")
    
    print("\n" + "="*70)
    if all_good:
        print("✓ ALL COMPONENTS VERIFIED")
    else:
        print("✗ SOME COMPONENTS MISSING - Check above")
    print("="*70)
    
    return all_good


def test_imports():
    """Test that all modules can be imported"""
    
    print("\n" + "="*70)
    print("TESTING IMPORTS")
    print("="*70)
    
    test_modules = [
        ("Assessment Registry", "src.assessments.registry", "ASSESSMENTS"),
        ("Assessment Interfaces", "src.assessments.interfaces", "AssessmentInterface"),
        ("Word Banks", "src.banks.word_banks", "get_words_by_grade"),
        ("Simple Generator", "src.generators.simple_assessment_generator", "SimpleAssessmentGenerator"),
        ("Assessment Matrix", "src.utils.assessment_matrix", "AssessmentMatrix"),
        ("Letter Recognition Generator", "src.generators.letter_recognition_generator", "create_letter_recognition_generator"),
        ("Word Reading Generator", "src.generators.word_reading_fluency_generator", "create_word_reading_fluency_generator"),
    ]
    
    all_imports_ok = True
    
    for name, module_path, attribute in test_modules:
        try:
            module = __import__(module_path, fromlist=[attribute])
            obj = getattr(module, attribute)
            print(f"  ✓ {name}")
        except Exception as e:
            print(f"  ✗ {name}: {e}")
            all_imports_ok = False
    
    print("="*70)
    if all_imports_ok:
        print("✓ ALL IMPORTS SUCCESSFUL")
    else:
        print("✗ SOME IMPORTS FAILED")
    print("="*70)
    
    return all_imports_ok


def check_registry():
    """Check registry contents"""
    
    print("\n" + "="*70)
    print("REGISTRY CONTENTS")
    print("="*70)
    
    try:
        from src.assessments.registry import ASSESSMENTS
        
        print(f"\nTotal Assessments: {len(ASSESSMENTS)}")
        
        categories = {}
        for asr_id, asr in ASSESSMENTS.items():
            cat = asr.get('category', 'Unknown')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(asr)
        
        for cat, asrs in sorted(categories.items()):
            print(f"\n{cat} ({len(asrs)}):")
            for asr in asrs:
                print(f"  • {asr['id']}: {asr['name']}")
                print(f"    Grade Range: {asr['grade_range']}")
                print(f"    Items: {asr['content']['total_items']}")
                print(f"    Presentation: {asr['interface'].student_presentation.value}")
                print(f"    Timing: {asr['interface'].timing_mode.value}")
        
        print("\n" + "="*70)
        return True
        
    except Exception as e:
        print(f"✗ Error reading registry: {e}")
        import traceback
        traceback.print_exc()
        print("="*70)
        return False


def check_forms_generated():
    """Check if forms have been generated"""
    
    print("\n" + "="*70)
    print("GENERATED FORMS CHECK")
    print("="*70)
    
    try:
        from src.assessments.registry import ASSESSMENTS
        
        samples_dir = Path("samples")
        
        if not samples_dir.exists():
            print("  ○ No samples directory found yet")
            print("  → Run generation commands to create forms")
            print("="*70)
            return
        
        assessment_ids = list(ASSESSMENTS.keys())
        
        for asr_id in assessment_ids:
            # Look for forms in samples directory
            pattern = f"{asr_id.lower()}_form*_*.json"
            forms = list(samples_dir.glob(pattern))
            
            if forms:
                # Group by grade
                by_grade = {}
                for form in forms:
                    # Extract grade from filename: lr_alph_form1_k.json
                    parts = form.stem.split('_')
                    grade = parts[-1] if len(parts) > 0 else '?'
                    if grade not in by_grade:
                        by_grade[grade] = []
                    by_grade[grade].append(form)
                
                grade_str = ", ".join([f"{g}({len(forms)})" for g, forms in by_grade.items()])
                print(f"  ✓ {asr_id}: {len(forms)} form(s) - Grades: {grade_str}")
            else:
                print(f"  ○ {asr_id}: No forms yet (ready to generate)")
        
        print("="*70)
        
    except Exception as e:
        print(f"✗ Error checking forms: {e}")
        import traceback
        traceback.print_exc()
        print("="*70)


def test_generator():
    """Test that a generator can actually create a form"""
    
    print("\n" + "="*70)
    print("GENERATOR FUNCTIONALITY TEST")
    print("="*70)
    
    try:
        from src.generators.letter_recognition_generator import create_letter_recognition_generator
        from pathlib import Path
        import tempfile
        
        # Create temporary directory
        with tempfile.TemporaryDirectory() as tmpdir:
            gen = create_letter_recognition_generator()
            result = gen.generate('K', 1, Path(tmpdir))
            
            if result and gen.validate(result):
                print(f"  ✓ Letter Recognition generator working")
                print(f"    Generated: {result['form_id']}")
                print(f"    Items: {len(result['items'])}")
                print(f"    Grade: {result['grade']}")
            else:
                print(f"  ✗ Generator validation failed")
                return False
        
        print("="*70)
        return True
        
    except Exception as e:
        print(f"✗ Generator test failed: {e}")
        import traceback
        traceback.print_exc()
        print("="*70)
        return False


if __name__ == "__main__":
    print("\n🔍 BANK CREATOR SYSTEM VERIFICATION\n")
    
    # Run all checks
    structure_ok = verify_structure()
    imports_ok = test_imports()
    registry_ok = check_registry()
    check_forms_generated()
    generator_ok = test_generator()
    
    # Final summary
    print("\n" + "="*70)
    print("FINAL STATUS")
    print("="*70)
    
    if structure_ok and imports_ok and registry_ok and generator_ok:
        print("✅ SYSTEM FULLY OPERATIONAL")
        print("\nNext Steps:")
        print("1. Start dashboard: python dashboard/app.py")
        print("2. Generate forms: python generate_simple_assessment.py --assessment-id LR-ALPH --grade K")
        print("3. View in browser: http://localhost:5001")
    else:
        print("⚠️  SOME ISSUES DETECTED")
        print("Review errors above and fix before proceeding")
    
    print("="*70)
