#!/usr/bin/env python3
"""
PIB Generator Patch - Genre-Aware Key Handling

Fixes the PIB generator to accept both 'scenes' (fiction) and 'sections' (nonfiction).

This patch adds a simple key mapping before JSON parsing to normalize
nonfiction 'sections' to 'scenes' for internal processing.

Usage:
    python3.11 patch_pib_generator.py

This will create a patched version of the PIB generator that handles both keys.

Created: 2026-01-14
"""

import sys
import os
from pathlib import Path

# Colors for output
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_header(text):
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}{text}{RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")


def print_success(text):
    print(f"{GREEN}✓{RESET} {text}")


def print_warning(text):
    print(f"{YELLOW}⚠{RESET} {text}")


def print_error(text):
    print(f"{RED}✗{RESET} {text}")


def patch_pib_generator():
    """Patch the PIB generator to handle both 'scenes' and 'sections'"""
    
    print_header("PIB GENERATOR PATCH - GENRE-AWARE KEY HANDLING")
    
    # Locate the PIB generator file
    project_root = Path("/Users/lebron/Desktop/Bank Creator")
    pib_file = project_root / "src" / "generators" / "pib_generator.py"
    
    if not pib_file.exists():
        print_error(f"PIB generator not found at: {pib_file}")
        return False
    
    print_success(f"Found PIB generator: {pib_file}")
    
    # Read current content
    content = pib_file.read_text()
    
    # Check if already patched
    if "GENRE_AWARE_KEY_MAPPING" in content:
        print_warning("PIB generator already patched!")
        print("No changes needed.")
        return True
    
    # Find the _parse_response method
    if "def _parse_response" not in content:
        print_error("Could not find _parse_response method in PIB generator")
        return False
    
    print_success("Found _parse_response method")
    
    # Create the patch
    patch_code = '''
        # GENRE_AWARE_KEY_MAPPING - Added 2026-01-14
        # Handle both 'scenes' (fiction) and 'sections' (nonfiction)
        if 'sections' in data and 'scenes' not in data:
            # Nonfiction uses 'sections' - map to 'scenes' for consistency
            data['scenes'] = data['sections']
            del data['sections']
'''
    
    # Find the location to insert the patch
    # Look for: data = json.loads(json_str)
    # Insert patch right after it
    
    json_loads_line = "data = json.loads(json_str)"
    
    if json_loads_line not in content:
        print_error("Could not find JSON parsing line to patch")
        return False
    
    # Insert the patch
    patched_content = content.replace(
        json_loads_line,
        json_loads_line + patch_code
    )
    
    # Verify the patch was applied
    if patched_content == content:
        print_error("Patch was not applied (content unchanged)")
        return False
    
    # Create backup
    backup_file = pib_file.with_suffix('.py.backup')
    backup_file.write_text(content)
    print_success(f"Created backup: {backup_file.name}")
    
    # Write patched content
    pib_file.write_text(patched_content)
    print_success("Applied patch to PIB generator")
    
    # Show what was changed
    print_header("PATCH APPLIED")
    print("Added genre-aware key mapping:")
    print(patch_code)
    print("\nThis allows the PIB generator to accept:")
    print("  • 'scenes' key (for fiction/narrative passages)")
    print("  • 'sections' key (for nonfiction passages)")
    print("\nBoth are internally normalized to 'scenes' for consistent processing.")
    
    return True


def main():
    success = patch_pib_generator()
    
    if success:
        print_header("✅ PIB GENERATOR PATCHED SUCCESSFULLY!")
        print("\nNext steps:")
        print("1. Test the fix:")
        print("   python3.11 debug_pib_sample3.py")
        print()
        print("2. If test passes, retry Sample 3:")
        print("   python3.11 retry_sample3_fixed.py")
        print()
        print("3. Commit the fix:")
        print("   git add src/generators/pib_generator.py")
        print('   git commit -m "fix: PIB generator now handles nonfiction sections"')
    else:
        print_header("❌ PATCH FAILED")
        print("\nThe automatic patch could not be applied.")
        print("You may need to manually update the PIB generator.")
        print("\nManual fix:")
        print("1. Open: src/generators/pib_generator.py")
        print("2. Find: data = json.loads(json_str)")
        print("3. Add after it:")
        print('''
        # Handle both 'scenes' (fiction) and 'sections' (nonfiction)
        if 'sections' in data and 'scenes' not in data:
            data['scenes'] = data['sections']
            del data['sections']
        ''')
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
