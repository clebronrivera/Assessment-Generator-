#!/usr/bin/env python3.11
"""
Generate all missing assessments for the Reading Compass Dashboard
"""
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

# Define all missing assessments based on the matrix
missing_assessments = [
    # ORF Assessments (Grades K, 1, 3)
    {"type": "orf", "grade": "K", "band": "early"},
    {"type": "orf", "grade": "1", "band": "early"},
    {"type": "orf", "grade": "3", "band": "early"},
    
    # Comprehension - Nonfiction (Grades 2-6)
    {"type": "comp", "grade": "2", "genre": "nonfiction"},
    {"type": "comp", "grade": "3", "genre": "nonfiction"},
    {"type": "comp", "grade": "4", "genre": "nonfiction"},
    {"type": "comp", "grade": "5", "genre": "nonfiction"},
    {"type": "comp", "grade": "6", "genre": "nonfiction"},
    
    # Comprehension - Narrative (Grades 3-6)
    {"type": "comp", "grade": "3", "genre": "narrative"},
    {"type": "comp", "grade": "4", "genre": "narrative"},
    {"type": "comp", "grade": "5", "genre": "narrative"},
    {"type": "comp", "grade": "6", "genre": "narrative"},
]

def generate_assessment(assessment):
    """Generate a single assessment"""
    if assessment["type"] == "orf":
        script = PROJECT_ROOT / "generate_orf_assessment.py"
        cmd = [sys.executable, str(script), "--grade", assessment["grade"], "--band", assessment["band"]]
        desc = f"Grade {assessment['grade']} ORF ({assessment['band']})"
    else:
        script = PROJECT_ROOT / "generate_comprehension_assessment.py"
        cmd = [sys.executable, str(script), "--grade", assessment["grade"], "--genre", assessment["genre"]]
        desc = f"Grade {assessment['grade']} Comprehension ({assessment['genre']})"
    
    print(f"\n{'='*80}")
    print(f"🚀 Generating: {desc}")
    print(f"{'='*80}")
    
    try:
        result = subprocess.run(cmd, cwd=str(PROJECT_ROOT), capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ SUCCESS: {desc}")
            return True
        else:
            print(f"❌ FAILED: {desc}")
            print(f"Error output:\n{result.stderr[-500:]}")  # Last 500 chars
            return False
    except subprocess.TimeoutExpired:
        print(f"⏱️ TIMEOUT: {desc} (exceeded 5 minutes)")
        return False
    except Exception as e:
        print(f"❌ ERROR: {desc} - {e}")
        return False

def main():
    print("\n" + "="*80)
    print("📚 READING COMPASS - BATCH ASSESSMENT GENERATOR")
    print("="*80)
    print(f"\nTotal assessments to generate: {len(missing_assessments)}")
    print("\nStarting generation process...\n")
    
    results = []
    start_time = time.time()
    
    for i, assessment in enumerate(missing_assessments, 1):
        print(f"\n[{i}/{len(missing_assessments)}]", end=" ")
        success = generate_assessment(assessment)
        results.append(success)
        
        # Small delay between generations to avoid rate limits
        if i < len(missing_assessments):
            time.sleep(2)
    
    # Summary
    elapsed = time.time() - start_time
    successful = sum(results)
    failed = len(results) - successful
    
    print("\n" + "="*80)
    print("📊 GENERATION SUMMARY")
    print("="*80)
    print(f"✅ Successful: {successful}/{len(missing_assessments)}")
    print(f"❌ Failed: {failed}/{len(missing_assessments)}")
    print(f"⏱️  Total time: {elapsed/60:.1f} minutes")
    print("="*80 + "\n")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
