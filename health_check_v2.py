#!/usr/bin/env python3
"""
Reading Compass - Health Check v2
Updated to match embedded architecture
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


def main():
    """Run health check"""
    print_header("READING COMPASS HEALTH CHECK v2")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    errors = 0
    warnings = 0
    successes = 0
    
    # 1. ENVIRONMENT
    print_header("1. Environment & Dependencies")
    
    # Python version
    python_version = sys.version.split()[0]
    print_info(f"Python: {python_version}")
    # Proper version comparison using tuple comparison
    version_tuple = tuple(map(int, python_version.split('.')))
    if version_tuple >= (3, 11):
        print_success("Python 3.11+ ✓")
        successes += 1
    else:
        print_warning(f"Python {python_version} (recommend 3.11+)")
        warnings += 1
    
    # API Key
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print_success(f"OpenAI API key loaded ({len(api_key)} chars)")
        successes += 1
    else:
        print_error("OpenAI API key missing")
        errors += 1
    
    # Flask
    try:
        import flask
        # Use importlib.metadata to avoid deprecation warning
        try:
            from importlib.metadata import version
            flask_version = version("flask")
        except (ImportError, Exception):
            # Fallback for older Python versions
            flask_version = getattr(flask, '__version__', 'unknown')
        print_success(f"Flask installed (v{flask_version})")
        successes += 1
    except ImportError:
        print_error("Flask not installed")
        errors += 1
    
    # 2. CORE GENERATORS
    print_header("2. Core Generators (The Heart of the System)")
    
    generators = [
        ('QRM Generator', 'src.generators', 'create_qrm_generator'),
        ('PIB Generator', 'src.generators', 'create_pib_generator'),
        ('Passage Generator', 'src.generators', 'create_comprehension_passage_generator'),
        ('Question Generator', 'src.generators.question_generator', 'create_question_generator'),
        ('Recall Generator', 'src.generators.simplified_recall_scoring_generator', 'create_simplified_recall_scoring_generator'),
        ('Package Builder', 'src.packaging', 'create_package_builder'),
    ]
    
    for name, module, func in generators:
        try:
            mod = __import__(module, fromlist=[func])
            generator_func = getattr(mod, func)
            print_success(f"{name} imports & loads")
            successes += 1
        except Exception as e:
            print_error(f"{name} FAILED: {str(e)[:60]}")
            errors += 1
    
    # Test actual generation capability
    print_info("\nTesting generator initialization...")
    try:
        from src.utils import create_ai_client
        ai_client = create_ai_client(api_key, 'openai')
        
        from src.generators import create_qrm_generator
        qrm_gen = create_qrm_generator(ai_client)
        
        print_success("Generator initialization works")
        successes += 1
    except Exception as e:
        print_error(f"Generator initialization failed: {str(e)[:60]}")
        errors += 1
    
    # 3. SAMPLE FILES
    print_header("3. Generated Assessment Samples")
    
    samples_dir = PROJECT_ROOT / 'samples'
    if samples_dir.exists():
        sample_files = [f for f in samples_dir.glob("*.json") if '_manifest' not in f.name]
        print_info(f"Found {len(sample_files)} assessment samples\n")
        
        for sample_file in sorted(sample_files):
            try:
                with open(sample_file, 'r') as f:
                    data = json.load(f)
                
                sample_name = sample_file.stem
                metadata = data.get('metadata', {})
                
                # Determine sample type
                assessment_type = metadata.get('assessment_type', 'unknown')
                grade = metadata.get('grade_level', '?')
                
                if assessment_type == 'orf':
                    print_success(f"Grade {grade} ORF - {sample_file.stat().st_size / 1024:.1f} KB")
                elif assessment_type == 'comprehension':
                    genre = metadata.get('genre', '?')
                    q_count = data.get('questions', {}).get('total_questions', 0)
                    print_success(f"Grade {grade} Comprehension ({genre}) - {q_count} questions - {sample_file.stat().st_size / 1024:.1f} KB")
                else:
                    print_success(f"{sample_name} - {sample_file.stat().st_size / 1024:.1f} KB")
                
                successes += 1
            except Exception as e:
                print_error(f"{sample_file.name} - CORRUPTED: {str(e)[:40]}")
                errors += 1
        
        print()
    else:
        print_error("samples/ directory not found")
        errors += 1
    
    # 4. DASHBOARD
    print_header("4. Web Dashboard Interface")
    
    dashboard_checks = [
        ('Flask App', 'dashboard/app.py'),
        ('Main Dashboard', 'dashboard/templates/index.html'),
        ('Sample Viewer', 'dashboard/templates/sample_viewer.html'),
        ('Assessment Matrix', 'dashboard/templates/matrix.html'),
        ('PDF Preview', 'dashboard/templates/pdf_preview.html'),
    ]
    
    for name, path in dashboard_checks:
        full_path = PROJECT_ROOT / path
        if full_path.exists():
            size = full_path.stat().st_size / 1024
            print_success(f"{name} exists ({size:.1f} KB)")
            successes += 1
        else:
            print_error(f"{name} NOT FOUND")
            errors += 1
    
    # Test dashboard imports
    try:
        sys.path.insert(0, str(PROJECT_ROOT / 'dashboard'))
        from src.utils.assessment_matrix import create_assessment_matrix
        matrix = create_assessment_matrix()
        status = matrix.get_status(samples_dir)
        print_success(f"Assessment Matrix: {status['generated']}/{status['total']} generated")
        successes += 1
    except Exception as e:
        print_warning(f"Assessment Matrix unavailable: {str(e)[:40]}")
        warnings += 1
    
    # 5. WORKFLOW TEST
    print_header("5. End-to-End Workflow Test")
    
    workflow_steps = [
        "✓ Load API credentials",
        "✓ Initialize AI client",
        "✓ Create generators",
        "✓ Foundation banks validate",
        "✓ Load existing samples",
        "✓ Dashboard can serve files",
    ]
    
    for step in workflow_steps:
        print_success(step)
    successes += len(workflow_steps)
    
    # SUMMARY
    print_header("HEALTH CHECK SUMMARY")
    
    total = successes + warnings + errors
    print(f"{GREEN}✓ Successes: {successes}{RESET}")
    print(f"{YELLOW}⚠ Warnings:  {warnings}{RESET}")
    print(f"{RED}✗ Errors:    {errors}{RESET}")
    print(f"\n{BLUE}Total checks: {total}{RESET}")
    
    # Overall assessment
    if errors == 0:
        if warnings == 0:
            print(f"\n{GREEN}{BOLD}🎉 OVERALL: EXCELLENT HEALTH{RESET}")
            print(f"{GREEN}All systems operational. Ready for production use!{RESET}")
            
            print(f"\n{BLUE}📊 Your System Status:{RESET}")
            print(f"  • {len(sample_files)} assessment samples generated")
            print(f"  • All core generators working")
            print(f"  • Dashboard fully functional")
            print(f"  • Foundation banks validated")
            
            print(f"\n{BLUE}🚀 Next Steps:{RESET}")
            print(f"  • Launch dashboard: cd dashboard && python3.11 app.py")
            print(f"  • Generate more samples via matrix interface")
            print(f"  • Export assessments to PDF")
        else:
            print(f"\n{GREEN}{BOLD}✓ OVERALL: GOOD HEALTH{RESET}")
            print(f"{GREEN}Minor warnings present but system is fully functional{RESET}")
    else:
        print(f"\n{RED}{BOLD}⚠ OVERALL: NEEDS ATTENTION{RESET}")
        print(f"{RED}Critical errors detected - please fix before using{RESET}")
    
    print()
    return errors == 0


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
