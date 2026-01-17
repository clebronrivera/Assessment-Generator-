#!/usr/bin/env python3
"""
Comprehensive Assessment Verification Script

Checks all assessments for:
1. Proper JSON structure and required fields
2. Corresponding manifest files
3. PDF generation capability
4. Complete assessment details (interface_spec, metadata, items)
5. Missing components

Reports any issues found and can prompt for fixes.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

SAMPLES_DIR = PROJECT_ROOT / "samples"
TEMPLATES_DIR = PROJECT_ROOT / "templates"

# Required fields in assessment JSON
REQUIRED_ASSESSMENT_FIELDS = {
    "metadata": ["assessment_id", "form_id", "form_number", "grade", "assessment_name", "created_at", "schema_version"],
    "interface_spec": ["student_presentation", "assessor_interaction", "timing_mode"],
    "items": []  # Must exist but can be empty for some assessments
}

# Required fields in manifest JSON
REQUIRED_MANIFEST_FIELDS = ["package_id", "assessment_type", "created_at", "grade", "form_number", "schema_version", "statistics", "ready_for_use"]


class AssessmentChecker:
    """Checks assessments for completeness and correctness"""
    
    def __init__(self):
        self.issues = defaultdict(list)
        self.assessments_checked = 0
        self.manifests_checked = 0
        
    def check_assessment_file(self, json_file: Path) -> Tuple[bool, List[str]]:
        """Check a single assessment JSON file"""
        issues = []
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            return False, [f"Invalid JSON: {e}"]
        except Exception as e:
            return False, [f"Error reading file: {e}"]
        
        # Check metadata
        if "metadata" not in data:
            issues.append("Missing 'metadata' field")
        else:
            metadata = data["metadata"]
            for field in REQUIRED_ASSESSMENT_FIELDS["metadata"]:
                if field not in metadata:
                    issues.append(f"Missing metadata field: {field}")
        
        # Check interface_spec
        if "interface_spec" not in data:
            issues.append("Missing 'interface_spec' field")
        else:
            interface_spec = data["interface_spec"]
            for field in REQUIRED_ASSESSMENT_FIELDS["interface_spec"]:
                if field not in interface_spec:
                    issues.append(f"Missing interface_spec field: {field}")
        
        # Check items (must exist, but can be empty for some assessment types)
        # ORF assessments don't have items (they have passages)
        assessment_id_val = data.get("assessment_id") or metadata.get("assessment_id", "")
        assessment_type = metadata.get("assessment_type", "")
        
        if assessment_id_val != "ORF" and assessment_type != "orf":
            if "items" not in data:
                # Some assessments use "questions" instead (Comprehension)
                if "questions" not in data:
                    issues.append("Missing 'items' or 'questions' field")
        
        # Check assessment_id
        if "assessment_id" not in data and "metadata" in data:
            if "assessment_id" not in data["metadata"]:
                issues.append("Missing 'assessment_id' in root or metadata")
        
        # Check scoring
        if "scoring" not in data:
            issues.append("Missing 'scoring' field")
        
        return len(issues) == 0, issues
    
    def check_manifest_file(self, manifest_file: Path) -> Tuple[bool, List[str]]:
        """Check a single manifest JSON file"""
        issues = []
        
        try:
            with open(manifest_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            return False, [f"Invalid JSON: {e}"]
        except Exception as e:
            return False, [f"Error reading file: {e}"]
        
        for field in REQUIRED_MANIFEST_FIELDS:
            if field not in data:
                issues.append(f"Missing manifest field: {field}")
        
        # Check statistics structure
        if "statistics" in data:
            if not isinstance(data["statistics"], dict):
                issues.append("'statistics' must be a dictionary")
            elif "total_items" not in data["statistics"]:
                issues.append("Missing 'total_items' in statistics")
        
        return len(issues) == 0, issues
    
    def check_pdf_generation(self, json_file: Path) -> Tuple[bool, List[str]]:
        """Check if PDFs can be generated for an assessment"""
        issues = []
        
        try:
            from src.utils.page_generator import (
                generate_pages_for_assessment, 
                PDF_AVAILABLE,
                load_assessment_json
            )
            
            # Check if WeasyPrint is available
            if not PDF_AVAILABLE:
                issues.append("PDF generation not available (WeasyPrint not installed)")
                return False, issues
            
            # Check if templates exist
            assessor_template = TEMPLATES_DIR / "assessor_page.html"
            student_template = TEMPLATES_DIR / "student_page.html"
            
            if not assessor_template.exists():
                issues.append(f"Missing assessor template: {assessor_template}")
            if not student_template.exists():
                issues.append(f"Missing student template: {student_template}")
            
            # Try to load assessment
            assessment_data = load_assessment_json(json_file)
            if not assessment_data:
                issues.append("Could not load assessment data for PDF generation")
            
        except ImportError as e:
            issues.append(f"Import error: {e}")
        except Exception as e:
            issues.append(f"Error checking PDF generation: {e}")
        
        return len(issues) == 0, issues
    
    def find_missing_manifests(self) -> List[Path]:
        """Find assessment JSON files without corresponding manifest files"""
        missing = []
        
        for json_file in SAMPLES_DIR.glob("*.json"):
            if json_file.name.endswith("_manifest.json"):
                continue
            
            manifest_file = json_file.parent / f"{json_file.stem}_manifest.json"
            if not manifest_file.exists():
                missing.append(json_file)
        
        return missing
    
    def find_orphaned_manifests(self) -> List[Path]:
        """Find manifest files without corresponding assessment JSON files"""
        orphaned = []
        
        for manifest_file in SAMPLES_DIR.glob("*_manifest.json"):
            base_name = manifest_file.stem.replace("_manifest", "")
            json_file = manifest_file.parent / f"{base_name}.json"
            if not json_file.exists():
                orphaned.append(manifest_file)
        
        return orphaned
    
    def run_full_check(self) -> Dict[str, Any]:
        """Run complete verification of all assessments"""
        print("=" * 80)
        print("ASSESSMENT VERIFICATION REPORT")
        print("=" * 80)
        print()
        
        results = {
            "assessments_checked": 0,
            "assessments_with_issues": 0,
            "manifests_checked": 0,
            "manifests_with_issues": 0,
            "missing_manifests": [],
            "orphaned_manifests": [],
            "pdf_issues": [],
            "all_issues": defaultdict(list)
        }
        
        # Check all assessment JSON files
        print("Checking assessment JSON files...")
        assessment_files = [f for f in SAMPLES_DIR.glob("*.json") 
                           if not f.name.endswith("_manifest.json")]
        
        for json_file in sorted(assessment_files):
            results["assessments_checked"] += 1
            is_valid, issues = self.check_assessment_file(json_file)
            
            if not is_valid:
                results["assessments_with_issues"] += 1
                results["all_issues"][json_file.name].extend(issues)
                print(f"  ❌ {json_file.name}: {len(issues)} issue(s)")
                for issue in issues:
                    print(f"     - {issue}")
            else:
                print(f"  ✅ {json_file.name}: OK")
        
        print()
        
        # Check all manifest files
        print("Checking manifest JSON files...")
        manifest_files = list(SAMPLES_DIR.glob("*_manifest.json"))
        
        for manifest_file in sorted(manifest_files):
            results["manifests_checked"] += 1
            is_valid, issues = self.check_manifest_file(manifest_file)
            
            if not is_valid:
                results["manifests_with_issues"] += 1
                results["all_issues"][manifest_file.name].extend(issues)
                print(f"  ❌ {manifest_file.name}: {len(issues)} issue(s)")
                for issue in issues:
                    print(f"     - {issue}")
            else:
                print(f"  ✅ {manifest_file.name}: OK")
        
        print()
        
        # Check for missing manifests
        print("Checking for missing manifest files...")
        missing_manifests = self.find_missing_manifests()
        results["missing_manifests"] = missing_manifests
        
        if missing_manifests:
            print(f"  ⚠️  Found {len(missing_manifests)} assessment(s) without manifest files:")
            for json_file in missing_manifests:
                print(f"     - {json_file.name}")
        else:
            print("  ✅ All assessments have manifest files")
        
        print()
        
        # Check for orphaned manifests
        print("Checking for orphaned manifest files...")
        orphaned_manifests = self.find_orphaned_manifests()
        results["orphaned_manifests"] = orphaned_manifests
        
        if orphaned_manifests:
            print(f"  ⚠️  Found {len(orphaned_manifests)} orphaned manifest file(s):")
            for manifest_file in orphaned_manifests:
                print(f"     - {manifest_file.name}")
        else:
            print("  ✅ No orphaned manifest files")
        
        print()
        
        # Check PDF generation capability
        print("Checking PDF generation capability...")
        try:
            from src.utils.page_generator import PDF_AVAILABLE
            if PDF_AVAILABLE:
                print("  ✅ PDF generation available (WeasyPrint installed)")
            else:
                print("  ⚠️  PDF generation not available (WeasyPrint not installed)")
                results["pdf_issues"].append("WeasyPrint not installed")
        except (ImportError, OSError) as e:
            # OSError can occur if WeasyPrint is installed but system libraries are missing
            if "libgobject" in str(e) or "dlopen" in str(e):
                print("  ⚠️  PDF generation code ready but system libraries needed (install via: brew install gobject-introspection)")
                results["pdf_issues"].append("WeasyPrint installed but system libraries missing")
            else:
                print("  ⚠️  Could not check PDF generation capability")
                results["pdf_issues"].append("Could not import page_generator")
        
        # Check templates
        assessor_template = TEMPLATES_DIR / "assessor_page.html"
        student_template = TEMPLATES_DIR / "student_page.html"
        
        if not assessor_template.exists():
            print(f"  ❌ Missing assessor template: {assessor_template}")
            results["pdf_issues"].append(f"Missing assessor template")
        else:
            print(f"  ✅ Assessor template found")
        
        if not student_template.exists():
            print(f"  ❌ Missing student template: {student_template}")
            results["pdf_issues"].append(f"Missing student template")
        else:
            print(f"  ✅ Student template found")
        
        print()
        print("=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"Assessments checked: {results['assessments_checked']}")
        print(f"Assessments with issues: {results['assessments_with_issues']}")
        print(f"Manifests checked: {results['manifests_checked']}")
        print(f"Manifests with issues: {results['manifests_with_issues']}")
        print(f"Missing manifests: {len(results['missing_manifests'])}")
        print(f"Orphaned manifests: {len(results['orphaned_manifests'])}")
        print(f"PDF issues: {len(results['pdf_issues'])}")
        print()
        
        total_issues = (
            results['assessments_with_issues'] + 
            results['manifests_with_issues'] + 
            len(results['missing_manifests']) + 
            len(results['orphaned_manifests']) + 
            len(results['pdf_issues'])
        )
        
        if total_issues == 0:
            print("✅ ALL CHECKS PASSED - No issues found!")
        else:
            print(f"⚠️  FOUND {total_issues} TOTAL ISSUE(S) - Review details above")
        
        print("=" * 80)
        
        return results


def main():
    """Main entry point"""
    checker = AssessmentChecker()
    results = checker.run_full_check()
    
    # Return exit code based on results
    total_issues = (
        results['assessments_with_issues'] + 
        results['manifests_with_issues'] + 
        len(results['missing_manifests']) + 
        len(results['orphaned_manifests']) + 
        len(results['pdf_issues'])
    )
    
    return 0 if total_issues == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
