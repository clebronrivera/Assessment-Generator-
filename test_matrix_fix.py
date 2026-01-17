#!/usr/bin/env python3
"""Test script to verify matrix filtering works correctly"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.assessment_matrix import create_assessment_matrix

def test_matrix_filtering():
    """Verify RC-* assessments don't show as missing"""
    print("=" * 80)
    print("TESTING MATRIX FILTERING")
    print("=" * 80)
    
    matrix = create_assessment_matrix()
    samples_dir = PROJECT_ROOT / "samples"
    status = matrix.get_status(samples_dir)
    
    # Check for RC-* assessments in results
    rc_assessments = [
        a for a in status['assessments']
        if a['spec'].assessment_id and a['spec'].assessment_id.startswith('RC-')
    ]
    
    print(f"\n1. RC-* Assessment Check:")
    if rc_assessments:
        print(f"   ❌ FOUND {len(rc_assessments)} RC-* assessments (should be 0):")
        for a in rc_assessments:
            print(f"      - {a['spec'].assessment_id} (Grade {a['spec'].grade})")
        return False
    else:
        print(f"   ✅ No RC-* assessments found (correct!)")
    
    # Check working assessments still appear
    working_ids = ['LR-ALPH', 'FL-WRF', 'PA-RHYM']
    working_found = []
    for a in status['assessments']:
        if a['spec'].assessment_id in working_ids:
            working_found.append(a['spec'].assessment_id)
    
    print(f"\n2. Working Assessments Check:")
    print(f"   Found: {sorted(set(working_found))}")
    if len(working_found) >= 3:
        print(f"   ✅ Working assessments still appear correctly")
    else:
        print(f"   ⚠️  Some working assessments missing")
        return False
    
    # Check generated comprehension still appears
    comp_assessments = [
        a for a in status['assessments']
        if a['spec'].assessment_type == 'comprehension'
    ]
    
    print(f"\n3. Generated Comprehension Check:")
    if comp_assessments:
        comp_with_files = [a for a in comp_assessments if a['exists']]
        print(f"   Found {len(comp_with_files)} generated comprehension assessments")
        if comp_with_files:
            print(f"   ✅ Generated comprehension assessments still appear")
        else:
            print(f"   ⚠️  No generated comprehension found (check your files)")
    else:
        print(f"   ℹ️  No comprehension assessments in matrix (may be normal)")
    
    # Summary
    print(f"\n4. Matrix Summary:")
    print(f"   Total assessments shown: {status['total']}")
    print(f"   Generated: {status['generated']}")
    print(f"   Missing: {status['missing']}")
    
    print(f"\n{'=' * 80}")
    if len(rc_assessments) == 0 and len(working_found) >= 3:
        print("✅ ALL TESTS PASSED")
        return True
    else:
        print("❌ TESTS FAILED - Review output above")
        return False

if __name__ == '__main__':
    success = test_matrix_filtering()
    sys.exit(0 if success else 1)
