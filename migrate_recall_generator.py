#!/usr/bin/env python3
"""
Recall Generator Migration Script

Automates the process of:
1. Creating archive structure
2. Moving old recall_scoring_generator.py to archive
3. Updating __init__.py imports
4. Creating migration documentation
5. Validating the migration

Run this script to cleanly retire the old recall generator.

Usage:
    python3.11 migrate_recall_generator.py

Created: January 14, 2026
"""

import os
import sys
import shutil
from pathlib import Path

# Colors for terminal output
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

def print_step(number, text):
    print(f"\n{BLUE}[{number}]{RESET} {text}")


class RecallGeneratorMigration:
    """Handles migration from old to new recall generator"""
    
    def __init__(self, project_root="/Users/lebron/Desktop/Bank Creator"):
        self.project_root = Path(project_root)
        self.generators_dir = self.project_root / "src" / "generators"
        self.archive_dir = self.generators_dir / "archived"
        self.old_generator = self.generators_dir / "recall_scoring_generator.py"
        self.new_generator = self.generators_dir / "simplified_recall_scoring_generator.py"
        
    def validate_project_structure(self):
        """Ensure we're in the right project"""
        print_step(1, "Validating project structure...")
        
        if not self.project_root.exists():
            print_error(f"Project root not found: {self.project_root}")
            return False
            
        if not self.generators_dir.exists():
            print_error(f"Generators directory not found: {self.generators_dir}")
            return False
            
        print_success(f"Project root: {self.project_root}")
        print_success(f"Generators dir: {self.generators_dir}")
        return True
    
    def check_old_generator_exists(self):
        """Check if old generator exists"""
        print_step(2, "Checking for old recall generator...")
        
        if not self.old_generator.exists():
            print_warning("Old recall_scoring_generator.py not found - may already be archived")
            return False
            
        print_success(f"Found: {self.old_generator.name}")
        size_kb = self.old_generator.stat().st_size / 1024
        print(f"   Size: {size_kb:.1f} KB")
        return True
    
    def check_new_generator_exists(self):
        """Check if new generator exists"""
        print_step(3, "Checking for new simplified generator...")
        
        if not self.new_generator.exists():
            print_error("New simplified_recall_scoring_generator.py not found!")
            print("   Please copy it to src/generators/ first")
            return False
            
        print_success(f"Found: {self.new_generator.name}")
        size_kb = self.new_generator.stat().st_size / 1024
        print(f"   Size: {size_kb:.1f} KB")
        return True
    
    def create_archive_structure(self):
        """Create archive directory and README"""
        print_step(4, "Creating archive structure...")
        
        # Create directory
        self.archive_dir.mkdir(exist_ok=True)
        print_success(f"Archive directory: {self.archive_dir}")
        
        # Create README
        readme_content = """# Archived Generators

This directory contains deprecated generator implementations that have been replaced with improved versions.

## Why Archive Instead of Delete?

- Preserves implementation history
- Allows comparison with new approach
- Reference for understanding design decisions
- Easy restoration if needed

## Archived Files

### recall_scoring_generator.py
**Date Archived:** January 14, 2026  
**Reason:** Replaced with simplified_recall_scoring_generator.py  
**Issue:** Complex JSON structure (120-180 fields) caused unreliable AI generation  
**Replacement:** Simplified approach using character + detail scoring (20-30 fields)  

See: simplified_recall_scoring_generator.py for current implementation
"""
        
        readme_path = self.archive_dir / "README.md"
        readme_path.write_text(readme_content)
        print_success(f"Created: {readme_path.name}")
        
        return True
    
    def archive_old_generator(self):
        """Move old generator to archive"""
        print_step(5, "Archiving old recall generator...")
        
        if not self.old_generator.exists():
            print_warning("File already archived or doesn't exist")
            return True
            
        destination = self.archive_dir / self.old_generator.name
        
        # Use shutil.move to preserve metadata
        shutil.move(str(self.old_generator), str(destination))
        
        print_success(f"Moved: {self.old_generator.name}")
        print(f"   → {destination}")
        
        return True
    
    def update_init_file(self):
        """Update __init__.py to import new generator"""
        print_step(6, "Updating __init__.py...")
        
        init_file = self.generators_dir / "__init__.py"
        
        if not init_file.exists():
            print_error("__init__.py not found!")
            return False
        
        # Read current content
        current_content = init_file.read_text()
        
        # Check if already updated
        if 'simplified_recall_scoring_generator' in current_content:
            print_success("__init__.py already updated")
            return True
        
        # Update content
        new_content = current_content
        
        # Replace old import with new one
        old_import = "from .recall_scoring_generator import create_recall_scoring_generator"
        new_import = "from .simplified_recall_scoring_generator import create_simplified_recall_scoring_generator\n\n# Alias for backwards compatibility\ncreate_recall_scoring_generator = create_simplified_recall_scoring_generator"
        
        if old_import in new_content:
            new_content = new_content.replace(old_import, new_import)
            print_success("Replaced old import with new import + alias")
        else:
            # Add new import at the end of imports
            import_section_end = new_content.rfind('from .')
            if import_section_end != -1:
                # Find end of that line
                line_end = new_content.find('\n', import_section_end)
                new_content = new_content[:line_end+1] + new_import + '\n' + new_content[line_end+1:]
                print_success("Added new import to __init__.py")
        
        # Write updated content
        init_file.write_text(new_content)
        print_success("Updated: __init__.py")
        
        return True
    
    def create_migration_notes(self):
        """Create migration documentation"""
        print_step(7, "Creating migration documentation...")
        
        notes_content = """# Recall Scoring Generator Migration

**Date:** January 14, 2026  
**Status:** Complete  

## What Changed

The original `recall_scoring_generator.py` has been **archived** and replaced with `simplified_recall_scoring_generator.py`.

## Files Modified

1. `src/generators/archived/recall_scoring_generator.py` - Moved here
2. `src/generators/simplified_recall_scoring_generator.py` - New implementation
3. `src/generators/__init__.py` - Updated imports
4. `generate_samples_simplified.py` - Uses new generator

## Usage

Old import (still works via alias):
```python
from src.generators import create_recall_scoring_generator
```

New import (recommended):
```python
from src.generators import create_simplified_recall_scoring_generator
```

## Benefits

- ✅ 6x simpler JSON structure
- ✅ Reliable AI generation
- ✅ Practical scoring approach
- ✅ Teacher-friendly rubrics

See IMPLEMENTATION_GUIDE.md for details.
"""
        
        notes_path = self.project_root / "RECALL_MIGRATION.md"
        notes_path.write_text(notes_content)
        print_success(f"Created: {notes_path.name}")
        
        return True
    
    def validate_migration(self):
        """Validate migration was successful"""
        print_step(8, "Validating migration...")
        
        checks = []
        
        # Check 1: Old generator archived
        archived_file = self.archive_dir / "recall_scoring_generator.py"
        if archived_file.exists():
            checks.append((True, "Old generator in archive"))
        else:
            checks.append((False, "Old generator NOT in archive"))
        
        # Check 2: New generator in place
        if self.new_generator.exists():
            checks.append((True, "New generator in place"))
        else:
            checks.append((False, "New generator NOT found"))
        
        # Check 3: Archive README exists
        if (self.archive_dir / "README.md").exists():
            checks.append((True, "Archive README created"))
        else:
            checks.append((False, "Archive README missing"))
        
        # Check 4: __init__.py updated
        init_content = (self.generators_dir / "__init__.py").read_text()
        if 'simplified_recall_scoring_generator' in init_content:
            checks.append((True, "__init__.py updated"))
        else:
            checks.append((False, "__init__.py NOT updated"))
        
        # Check 5: Migration notes created
        if (self.project_root / "RECALL_MIGRATION.md").exists():
            checks.append((True, "Migration notes created"))
        else:
            checks.append((False, "Migration notes missing"))
        
        # Display results
        print()
        all_passed = True
        for passed, message in checks:
            if passed:
                print_success(message)
            else:
                print_error(message)
                all_passed = False
        
        return all_passed
    
    def run_migration(self):
        """Run full migration process"""
        print_header("RECALL GENERATOR MIGRATION")
        
        try:
            # Validation
            if not self.validate_project_structure():
                return False
            
            old_exists = self.check_old_generator_exists()
            
            if not self.check_new_generator_exists():
                return False
            
            # Migration steps
            if not self.create_archive_structure():
                return False
            
            if old_exists:
                if not self.archive_old_generator():
                    return False
            
            if not self.update_init_file():
                return False
            
            if not self.create_migration_notes():
                return False
            
            # Validation
            if not self.validate_migration():
                return False
            
            # Success!
            print_header("✅ MIGRATION COMPLETE!")
            print("\nNext steps:")
            print("1. Review changes: git status")
            print("2. Test new generator: python3.11 tests/test_simplified_recall.py")
            print("3. Generate samples: python3.11 generate_samples_simplified.py")
            print("4. Commit changes: git add -A && git commit -m 'feat: Archive old recall generator'")
            print()
            
            return True
            
        except Exception as e:
            print_error(f"Migration failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Main entry point"""
    migration = RecallGeneratorMigration()
    success = migration.run_migration()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
