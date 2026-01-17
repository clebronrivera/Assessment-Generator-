#!/usr/bin/env python3
"""
Fix Assessment Structure Script

Adds missing fields to ORF and Comprehension assessments to make them
compatible with PDF generation and the assessment system:
- Adds assessment_id, form_id, form_number, assessment_name to metadata
- Adds interface_spec for PDF generation
- Adds scoring information
- Fixes manifest files to include assessment_type, form_number, total_items
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent
SAMPLES_DIR = PROJECT_ROOT / "samples"


def get_orf_interface_spec() -> Dict[str, Any]:
    """Get interface spec for ORF assessments"""
    return {
        "student_presentation": "full_text",
        "student_sees_text": True,
        "items_advance_mode": "n/a",
        "assessor_interaction": "error_marking",
        "click_cycle": None,
        "timing_mode": "timer_down",
        "timer_direction": "down",
        "timer_visible_to_student": False,
        "assessor_script": [
            "SETUP: Prepare assessment materials. Ensure student has clean copy of passage.",
            "SAY TO STUDENT: 'I'm going to ask you to read this passage aloud. Read it as accurately and smoothly as you can. If you come to a word you don't know, I'll tell it to you. Do you have any questions?'",
            "ADMINISTRATION:",
            "  • Start timer when student begins reading",
            "  • Mark errors on assessor copy in real-time",
            "  • Supply words after 3-second hesitation",
            "  • Stop at 60 seconds and mark last word read",
            "  • Calculate WCPM and accuracy",
            "  • Score prosody using rubric"
        ],
        "student_prompt": "Read this passage aloud as accurately and smoothly as you can.",
        "student_action": "Student reads the passage aloud from a clean copy. Student attempts to read as accurately and smoothly as possible within the 60-second time limit.",
        "assessor_grading": "Assessor marks errors in real-time on assessor copy. Calculate WCPM = (Words Read - Errors) and Accuracy = (Words Read - Errors) / Words Read × 100. Score prosody using 1-4 scale.",
        "additional_considerations": ""
    }


def get_comp_interface_spec() -> Dict[str, Any]:
    """Get interface spec for Comprehension assessments"""
    return {
        "student_presentation": "full_text_with_questions",
        "student_sees_text": True,
        "items_advance_mode": "manual_next_button",
        "assessor_interaction": "correct_incorrect",
        "click_cycle": None,
        "timing_mode": "untimed",
        "timer_direction": "none",
        "timer_visible_to_student": False,
        "assessor_script": [
            "SETUP: Prepare assessment materials. Ensure student has access to passage and questions.",
            "SAY TO STUDENT: 'I'm going to ask you to read this passage and then answer some questions about it. You can refer back to the passage while answering questions.'",
            "ADMINISTRATION:",
            "  • Allow student to read passage at their own pace",
            "  • Present questions one at a time",
            "  • Mark each answer as correct or incorrect",
            "  • Record recall scoring if applicable",
            "  • Calculate total score"
        ],
        "student_prompt": "Read this passage and answer the questions that follow.",
        "student_action": "Student reads passage and answers questions. Student can refer back to passage while answering.",
        "assessor_grading": "Assessor marks each question as correct or incorrect. Calculate total score based on questions answered correctly.",
        "additional_considerations": ""
    }


def get_orf_scoring() -> Dict[str, Any]:
    """Get scoring info for ORF assessments"""
    return {
        "primary_metric": "wcpm",
        "secondary_metrics": [
            "accuracy_pct",
            "prosody_score",
            "total_errors"
        ],
        "error_types": [
            "substitution",
            "omission",
            "insertion",
            "hesitation"
        ]
    }


def get_comp_scoring() -> Dict[str, Any]:
    """Get scoring info for Comprehension assessments"""
    return {
        "primary_metric": "total_correct",
        "secondary_metrics": [
            "accuracy_pct",
            "recall_score"
        ],
        "error_types": [
            "incorrect"
        ]
    }


def fix_orf_assessment(json_file: Path) -> bool:
    """Fix an ORF assessment file"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"  ❌ Error reading {json_file.name}: {e}")
        return False
    
    # Extract info from existing metadata
    metadata = data.get("metadata", {})
    grade = metadata.get("grade", "N/A")
    band = metadata.get("band", "early")
    package_id = metadata.get("package_id", "")
    
    # Generate form_id and form_number from package_id or filename
    form_number = 1  # Default
    if package_id:
        # Try to extract form number from package_id
        parts = package_id.split("-")
        if len(parts) >= 2:
            try:
                form_number = int(parts[-1]) if parts[-1].isdigit() else 1
            except:
                pass
    
    # If not found, try filename
    if form_number == 1:
        filename_parts = json_file.stem.split("_")
        for part in filename_parts:
            if part.isdigit():
                form_number = int(part)
                break
    
    form_id = f"ORF-{grade}-{band.upper()}-{form_number:03d}"
    
    # Update metadata
    if "assessment_id" not in metadata:
        metadata["assessment_id"] = "ORF"
    if "form_id" not in metadata:
        metadata["form_id"] = form_id
    if "form_number" not in metadata:
        metadata["form_number"] = form_number
    if "assessment_name" not in metadata:
        metadata["assessment_name"] = f"Oral Reading Fluency - Grade {grade}"
    
    data["metadata"] = metadata
    
    # Add root-level fields
    if "assessment_id" not in data:
        data["assessment_id"] = "ORF"
    if "form_id" not in data:
        data["form_id"] = form_id
    if "form_number" not in data:
        data["form_number"] = form_number
    if "grade" not in data:
        data["grade"] = grade
    
    # Add interface_spec
    if "interface_spec" not in data:
        data["interface_spec"] = get_orf_interface_spec()
    
    # Add scoring
    if "scoring" not in data:
        data["scoring"] = get_orf_scoring()
    
    # Add empty items array for PDF generation compatibility
    if "items" not in data and "questions" not in data:
        data["items"] = []
    
    # Write back
    try:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"  ❌ Error writing {json_file.name}: {e}")
        return False


def fix_comp_assessment(json_file: Path) -> bool:
    """Fix a Comprehension assessment file"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"  ❌ Error reading {json_file.name}: {e}")
        return False
    
    # Extract info from existing metadata
    metadata = data.get("metadata", {})
    grade = metadata.get("grade", "N/A")
    band = metadata.get("band", "early")
    genre = metadata.get("genre", "narrative")
    package_id = metadata.get("package_id", "")
    
    # Generate form_id and form_number
    form_number = 1  # Default
    if package_id:
        parts = package_id.split("-")
        if len(parts) >= 2:
            try:
                form_number = int(parts[-1]) if parts[-1].isdigit() else 1
            except:
                pass
    
    # If not found, try filename
    if form_number == 1:
        filename_parts = json_file.stem.split("_")
        for part in filename_parts:
            if part.isdigit():
                form_number = int(part)
                break
    
    form_id = f"COMP-{grade}-{band.upper()}-{genre.upper()}-{form_number:03d}"
    
    # Update metadata
    if "assessment_id" not in metadata:
        metadata["assessment_id"] = "COMP"
    if "form_id" not in metadata:
        metadata["form_id"] = form_id
    if "form_number" not in metadata:
        metadata["form_number"] = form_number
    if "assessment_name" not in metadata:
        metadata["assessment_name"] = f"Reading Comprehension - Grade {grade} ({genre.title()})"
    
    data["metadata"] = metadata
    
    # Add root-level fields
    if "assessment_id" not in data:
        data["assessment_id"] = "COMP"
    if "form_id" not in data:
        data["form_id"] = form_id
    if "form_number" not in data:
        data["form_number"] = form_number
    if "grade" not in data:
        data["grade"] = grade
    
    # Add interface_spec
    if "interface_spec" not in data:
        data["interface_spec"] = get_comp_interface_spec()
    
    # Add scoring
    if "scoring" not in data:
        data["scoring"] = get_comp_scoring()
    
    # Ensure questions field exists (Comprehension uses questions, not items)
    if "questions" not in data and "items" not in data:
        # Try to get questions from qrm or other sections
        if "qrm" in data and "questions" in data["qrm"]:
            data["questions"] = {"questions": data["qrm"]["questions"]}
        else:
            data["questions"] = {"questions": []}
    
    # Write back
    try:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"  ❌ Error writing {json_file.name}: {e}")
        return False


def fix_orf_manifest(manifest_file: Path) -> bool:
    """Fix an ORF manifest file"""
    try:
        with open(manifest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"  ❌ Error reading {manifest_file.name}: {e}")
        return False
    
    # Add missing fields
    if "assessment_type" not in data:
        data["assessment_type"] = "orf"
    
    if "form_number" not in data:
        # Try to extract from package_id or filename
        form_number = 1
        package_id = data.get("package_id", "")
        if package_id:
            parts = package_id.split("-")
            if len(parts) >= 2:
                try:
                    form_number = int(parts[-1]) if parts[-1].isdigit() else 1
                except:
                    pass
        data["form_number"] = form_number
    
    # Fix statistics
    if "statistics" not in data:
        data["statistics"] = {}
    
    stats = data["statistics"]
    if "total_items" not in stats:
        # For ORF, total_items is passage word count
        stats["total_items"] = stats.get("passage_word_count", 0)
    
    # Write back
    try:
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"  ❌ Error writing {manifest_file.name}: {e}")
        return False


def fix_comp_manifest(manifest_file: Path) -> bool:
    """Fix a Comprehension manifest file"""
    try:
        with open(manifest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"  ❌ Error reading {manifest_file.name}: {e}")
        return False
    
    # Add missing fields
    if "assessment_type" not in data:
        data["assessment_type"] = "comprehension"
    
    if "form_number" not in data:
        # Try to extract from package_id or filename
        form_number = 1
        package_id = data.get("package_id", "")
        if package_id:
            parts = package_id.split("-")
            if len(parts) >= 2:
                try:
                    form_number = int(parts[-1]) if parts[-1].isdigit() else 1
                except:
                    pass
        data["form_number"] = form_number
    
    # Fix statistics
    if "statistics" not in data:
        data["statistics"] = {}
    
    stats = data["statistics"]
    if "total_items" not in stats:
        # For Comprehension, total_items is total questions
        stats["total_items"] = stats.get("total_questions", 0)
    
    # Write back
    try:
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"  ❌ Error writing {manifest_file.name}: {e}")
        return False


def main():
    """Main entry point"""
    print("=" * 80)
    print("FIXING ASSESSMENT STRUCTURE")
    print("=" * 80)
    print()
    
    orf_files = list(SAMPLES_DIR.glob("sample_orf_*.json"))
    orf_files.extend(SAMPLES_DIR.glob("sample_*_orf_*.json"))
    comp_files = list(SAMPLES_DIR.glob("sample_comp_*.json"))
    comp_files.extend(SAMPLES_DIR.glob("sample_*_comp_*.json"))
    
    orf_manifests = list(SAMPLES_DIR.glob("sample_orf_*_manifest.json"))
    orf_manifests.extend(SAMPLES_DIR.glob("sample_*_orf_*_manifest.json"))
    comp_manifests = list(SAMPLES_DIR.glob("sample_comp_*_manifest.json"))
    comp_manifests.extend(SAMPLES_DIR.glob("sample_*_comp_*_manifest.json"))
    
    fixed = 0
    failed = 0
    
    # Fix ORF assessments
    print(f"Fixing {len(orf_files)} ORF assessment(s)...")
    for json_file in sorted(orf_files):
        if fix_orf_assessment(json_file):
            print(f"  ✅ Fixed: {json_file.name}")
            fixed += 1
        else:
            print(f"  ❌ Failed: {json_file.name}")
            failed += 1
    
    print()
    
    # Fix Comprehension assessments
    print(f"Fixing {len(comp_files)} Comprehension assessment(s)...")
    for json_file in sorted(comp_files):
        if fix_comp_assessment(json_file):
            print(f"  ✅ Fixed: {json_file.name}")
            fixed += 1
        else:
            print(f"  ❌ Failed: {json_file.name}")
            failed += 1
    
    print()
    
    # Fix ORF manifests
    print(f"Fixing {len(orf_manifests)} ORF manifest(s)...")
    for manifest_file in sorted(orf_manifests):
        if fix_orf_manifest(manifest_file):
            print(f"  ✅ Fixed: {manifest_file.name}")
            fixed += 1
        else:
            print(f"  ❌ Failed: {manifest_file.name}")
            failed += 1
    
    print()
    
    # Fix Comprehension manifests
    print(f"Fixing {len(comp_manifests)} Comprehension manifest(s)...")
    for manifest_file in sorted(comp_manifests):
        if fix_comp_manifest(manifest_file):
            print(f"  ✅ Fixed: {manifest_file.name}")
            fixed += 1
        else:
            print(f"  ❌ Failed: {manifest_file.name}")
            failed += 1
    
    print()
    print("=" * 80)
    print(f"SUMMARY: {fixed} file(s) fixed, {failed} file(s) failed")
    print("=" * 80)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
