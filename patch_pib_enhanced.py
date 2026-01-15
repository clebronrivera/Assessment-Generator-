#!/usr/bin/env python3
"""
Enhanced PIB Generator Patch - Deep Genre-Aware Key Mapping

Fixes the PIB generator to handle both 'scenes' (fiction) and 'sections' (nonfiction)
at ALL levels - top-level key AND nested fields within each item.

Maps:
- sections → scenes (top level)
- section_number → scene_number (nested)
- section_type → scene_type (nested)
- section_* → scene_* (any section field)

Usage:
    python3.11 patch_pib_enhanced.py

Created: 2026-01-14
"""

import sys
import os
from pathlib import Path

# Colors
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


def patch_pib_generator_enhanced():
    """Apply enhanced PIB patch with deep field mapping"""
    
    print_header("ENHANCED PIB GENERATOR PATCH - DEEP FIELD MAPPING")
    
    # Locate the PIB generator file
    project_root = Path("/Users/lebron/Desktop/Bank Creator")
    pib_file = project_root / "src" / "generators" / "pib_generator.py"
    
    if not pib_file.exists():
        print_error(f"PIB generator not found at: {pib_file}")
        return False
    
    print_success(f"Found PIB generator: {pib_file}")
    
    # Read current content
    content = pib_file.read_text()
    
    # Check if already has enhanced patch
    if "DEEP_FIELD_MAPPING" in content:
        print_warning("PIB generator already has enhanced patch!")
        print("No changes needed.")
        return True
    
    # Find the location to patch
    json_loads_line = "data = json.loads(json_str)"
    
    if json_loads_line not in content:
        print_error("Could not find JSON parsing line to patch")
        return False
    
    print_success("Found JSON parsing line")
    
    # Create the enhanced patch
    enhanced_patch = '''
        # GENRE_AWARE_KEY_MAPPING with DEEP_FIELD_MAPPING - Added 2026-01-14
        # Handle both 'scenes' (fiction) and 'sections' (nonfiction)
        # Maps top-level key AND nested fields within each item
        if 'sections' in data and 'scenes' not in data:
            # Nonfiction uses 'sections' - map to 'scenes' for consistency
            sections = data['sections']
            
            # Map nested fields: section_* → scene_*
            scenes = []
            for section in sections:
                scene = {}
                for key, value in section.items():
                    # Replace 'section_' prefix with 'scene_'
                    new_key = key.replace('section_', 'scene_') if key.startswith('section_') else key
                    scene[new_key] = value
                scenes.append(scene)
            
            data['scenes'] = scenes
            del data['sections']
'''
    
    # Apply the patch
    patched_content = content.replace(
        json_loads_line,
        json_loads_line + enhanced_patch
    )
    
    # Verify the patch was applied
    if patched_content == content:
        print_error("Patch was not applied (content unchanged)")
        return False
    
    # Create backup (with timestamp if backup already exists)
    backup_file = pib_file.with_suffix('.py.backup')
    if backup_file.exists():
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = pib_file.parent / f"{pib_file.stem}.py.backup.{timestamp}"
    
    backup_file.write_text(content)
    print_success(f"Created backup: {backup_file.name}")
    
    # Write patched content
    pib_file.write_text(patched_content)
    print_success("Applied enhanced patch to PIB generator")
    
    # Show what was changed
    print_header("ENHANCED PATCH APPLIED")
    print("Added deep genre-aware field mapping:")
    print(enhanced_patch)
    print("\nThis maps BOTH:")
    print("  1. Top-level key: 'sections' → 'scenes'")
    print("  2. Nested fields: 'section_number' → 'scene_number'")
    print("                    'section_type' → 'scene_type'")
    print("                    'section_*' → 'scene_*' (any field)")
    print("\nGenre handling:")
    print("  • Fiction/Narrative: Uses 'scenes' with 'scene_*' fields (unchanged)")
    print("  • Nonfiction: Uses 'sections' with 'section_*' fields (auto-mapped)")
    
    return True


def main():
    success = patch_pib_generator_enhanced()
    
    if success:
        print_header("✅ ENHANCED PIB PATCH APPLIED SUCCESSFULLY!")
        print("\nNext steps:")
        print("1. Test the fix:")
        print("   python3.11 debug_pib_sample3.py")
        print()
        print("2. If test passes, generate Sample 3:")
        print("   python3.11 generate_samples_simplified.py")
        print("   (It will skip Samples 1 & 2 since they exist)")
        print()
        print("3. Commit the fix:")
        print("   git add src/generators/pib_generator.py")
        print('   git commit -m "fix: Deep field mapping for nonfiction sections"')
    else:
        print_header("❌ PATCH FAILED")
        print("\nThe automatic patch could not be applied.")
        print("\nManual fix:")
        print("1. Open: src/generators/pib_generator.py")
        print("2. Find: data = json.loads(json_str)")
        print("3. Add the enhanced patch from above")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
