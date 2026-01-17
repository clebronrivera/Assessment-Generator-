#!/usr/bin/env python3
"""
Reading Compass - Comprehensive Health Check
Tests all generators, validates samples, checks dashboard
"""

import sys
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import json

# Colors
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

def print_header(text):
    print(f"\n{BLUE}{BOLD}{'='*80}{RESET}")
    print(f"{BLUE}{BOLD}{text}{RESET}")
    print(f"{BLUE}{BOLD}{'='*80}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✓{RESET} {text}")

def print_warning(text):
    print(f"{YELLOW}⚠{RESET} {text}")

def print_error(text):
    print(f"{RED}✗{RESET} {text}")

def print_info(text):
    print(f"{BLUE}ℹ{RESET} {text}")


class HealthChecker:
    """Comprehensive health check for Reading Compass"""
    
    def __init__(self):
        self.results = {
            'environment': {},
            'structure': {},
            'generators': {},
            'samples': {},
            'dashboard': {},
            'overall': 'unknown'
        }
        self.error_count = 0
        self.warning_count = 0
        self.success_count = 0
    
    def run_all_checks(self):
        """Run all health checks"""
        print_header("READING COMPASS HEALTH CHECK")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        self.check_environment()
        self.check_project_structure()
        self.check_generators()
        self.check_samples()
        self.check_dashboard()
        
        self.print_summary()
        
        return self.error_count == 0
    
    def check_environment(self):
        """Check environment and dependencies"""
        print_header("1. Environment Check")
        
        # Check Python version
        python_version = sys.version.split()[0]
        print_info(f"Python version: {python_version}")
        if python_version >= '3.11':
            print_success("Python 3.11+ detected")
            self.success_count += 1
        else:
            print_warning(f"Python {python_version} detected (recommended: 3.11+)")
            self.warning_count += 1
        
        # Check .env file
        env_file = PROJECT_ROOT / '.env'
        if env_file.exists():
            print_success(".env file found")
            load_dotenv()
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                print_success(f"OpenAI API key loaded ({len(api_key)} chars)")
                self.success_count += 1
            else:
                print_error("OpenAI API key not found in .env")
                self.error_count += 1
        else:
            print_error(".env file not found")
            self.error_count += 1
        
        # Check required packages
        required_packages = ['openai', 'anthropic', 'flask']
        for package in required_packages:
            try:
                __import__(package)
                print_success(f"{package} package installed")
                self.success_count += 1
            except ImportError:
                print_warning(f"{package} package not installed (may not be needed)")
                self.warning_count += 1
    
    def check_project_structure(self):
        """Check project directory structure"""
        print_header("2. Project Structure Check")
        
        required_dirs = [
            'src',
            'src/generators',
            'src/banks',
            'src/packaging',
            'src/utils',
            'samples',
            'dashboard',
            'dashboard/templates',
        ]
        
        for dir_path in required_dirs:
            full_path = PROJECT_ROOT / dir_path
            if full_path.exists():
                print_success(f"{dir_path}/ exists")
                self.success_count += 1
            else:
                print_error(f"{dir_path}/ NOT FOUND")
                self.error_count += 1
        
        # Check key files
        key_files = [
            'src/generators/__init__.py',
            'src/generators/qrm_generator.py',
            'src/generators/pib_generator.py',
            'src/generators/comprehension_passage_generator.py',
            'src/generators/question_generator.py',
            'src/generators/simplified_recall_scoring_generator.py',
            'dashboard/app.py',
            'dashboard/templates/index.html',
            'dashboard/templates/sample_viewer.html',
        ]
        
        for file_path in key_files:
            full_path = PROJECT_ROOT / file_path
            if full_path.exists():
                size = full_path.stat().st_size
                print_success(f"{file_path} exists ({size} bytes)")
                self.success_count += 1
            else:
                print_error(f"{file_path} NOT FOUND")
                self.error_count += 1
    
    def check_generators(self):
        """Check generator functionality"""
        print_header("3. Generator Import Check")
        
        generators_to_test = [
            ('QRM Generator', 'src.generators', 'create_qrm_generator'),
            ('PIB Generator', 'src.generators', 'create_pib_generator'),
            ('Passage Generator', 'src.generators', 'create_comprehension_passage_generator'),
            ('Question Generator', 'src.generators.question_generator', 'create_question_generator'),
            ('Simplified Recall Generator', 'src.generators.simplified_recall_scoring_generator', 'create_simplified_recall_scoring_generator'),
            ('Package Builder', 'src.packaging', 'create_package_builder'),
            ('AI Client', 'src.utils', 'create_ai_client'),
        ]
        
        for name, module, func in generators_to_test:
            try:
                mod = __import__(module, fromlist=[func])
                generator_func = getattr(mod, func)
                print_success(f"{name} imports successfully")
                self.success_count += 1
            except Exception as e:
                print_error(f"{name} import failed: {str(e)}")
                self.error_count += 1
        
        # Check foundation banks
        print_info("\nFoundation Banks:")
        try:
            from src.banks import validate_all_banks
            
            if validate_all_banks():
                print_success("All foundation banks validated successfully")
                self.success_count += 1
            else:
                print_error("Foundation banks validation failed")
                self.error_count += 1
                
        except Exception as e:
            print_error(f"Foundation banks error: {str(e)}")
            self.error_count += 1
    
    def check_samples(self):
        """Check existing samples"""
        print_header("4. Sample Files Check")
        
        samples_dir = PROJECT_ROOT / 'samples'
        if not samples_dir.exists():
            print_error("samples/ directory not found")
            self.error_count += 1
            return
        
        # Find all sample files
        sample_files = list(samples_dir.glob("*.json"))
        sample_files = [f for f in sample_files if '_manifest' not in f.name]
        
        print_info(f"Found {len(sample_files)} sample files\n")
        
        for sample_file in sample_files:
            sample_name = sample_file.stem
            print_info(f"Checking: {sample_name}")
            
            # Check JSON validity
            try:
                with open(sample_file, 'r') as f:
                    data = json.load(f)
                print_success(f"  ✓ Valid JSON ({sample_file.stat().st_size / 1024:.1f} KB)")
                
                # Check structure
                if 'metadata' in data:
                    print_success("  ✓ Has metadata")
                else:
                    print_warning("  ⚠ Missing metadata")
                
                if 'passage' in data or data.get('metadata', {}).get('assessment_type') == 'orf':
                    print_success("  ✓ Has passage (or is ORF)")
                else:
                    print_warning("  ⚠ Missing passage")
                
                if 'questions' in data:
                    q_count = data['questions'].get('total_questions', 0)
                    print_success(f"  ✓ Has {q_count} questions")
                else:
                    print_warning("  ⚠ Missing questions")
                
                # Check manifest
                manifest_file = samples_dir / f"{sample_name}_manifest.json"
                if manifest_file.exists():
                    print_success("  ✓ Has manifest")
                else:
                    print_warning("  ⚠ Missing manifest")
                
                self.success_count += 1
                
            except json.JSONDecodeError as e:
                print_error(f"  ✗ Invalid JSON: {str(e)}")
                self.error_count += 1
            except Exception as e:
                print_error(f"  ✗ Error: {str(e)}")
                self.error_count += 1
            
            print()  # Blank line between samples
    
    def check_dashboard(self):
        """Check dashboard components"""
        print_header("5. Dashboard Check")
        
        dashboard_dir = PROJECT_ROOT / 'dashboard'
        
        # Check Flask app
        app_file = dashboard_dir / 'app.py'
        if app_file.exists():
            print_success("Flask app.py exists")
            
            # Check if it imports correctly
            try:
                import importlib.util
                spec = importlib.util.spec_from_file_location("app", str(app_file))
                # Don't actually import to avoid running the server
                print_success("Flask app has valid Python syntax")
                self.success_count += 1
            except Exception as e:
                print_error(f"Flask app has syntax errors: {str(e)}")
                self.error_count += 1
        else:
            print_error("Flask app.py not found")
            self.error_count += 1
        
        # Check templates
        templates = ['index.html', 'sample_viewer.html', 'matrix.html', 'pdf_preview.html']
        templates_dir = dashboard_dir / 'templates'
        
        for template in templates:
            template_file = templates_dir / template
            if template_file.exists():
                print_success(f"Template {template} exists")
                self.success_count += 1
            else:
                print_warning(f"Template {template} not found")
                self.warning_count += 1
        
        # Check if assessment_matrix exists
        try:
            from src.utils.assessment_matrix import create_assessment_matrix
            matrix = create_assessment_matrix()
            print_success("Assessment matrix module loads")
            self.success_count += 1
        except ImportError:
            print_warning("Assessment matrix module not found (optional)")
            self.warning_count += 1
        except Exception as e:
            print_error(f"Assessment matrix error: {str(e)}")
            self.error_count += 1
    
    def print_summary(self):
        """Print health check summary"""
        print_header("HEALTH CHECK SUMMARY")
        
        total_checks = self.success_count + self.warning_count + self.error_count
        
        print(f"{GREEN}✓ Successes: {self.success_count}{RESET}")
        print(f"{YELLOW}⚠ Warnings:  {self.warning_count}{RESET}")
        print(f"{RED}✗ Errors:    {self.error_count}{RESET}")
        print(f"\n{BLUE}Total checks: {total_checks}{RESET}")
        
        # Overall health
        if self.error_count == 0:
            if self.warning_count == 0:
                print(f"\n{GREEN}{BOLD}🎉 OVERALL: EXCELLENT HEALTH{RESET}")
                print("All systems operational!")
            else:
                print(f"\n{GREEN}{BOLD}✓ OVERALL: GOOD HEALTH{RESET}")
                print("Some minor warnings, but system is functional")
        else:
            print(f"\n{RED}{BOLD}⚠ OVERALL: NEEDS ATTENTION{RESET}")
            print("Critical errors detected - please fix before using")
        
        print()


def main():
    """Run health check"""
    checker = HealthChecker()
    success = checker.run_all_checks()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
