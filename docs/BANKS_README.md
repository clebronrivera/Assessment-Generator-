# Reading Assessment Generator - Foundation Banks

## Overview

This module contains the **7 Foundation Banks** that power the entire Reading Assessment Generator system. These banks are:

1. **Lexile Ranges** - Grade-specific Lexile bands (Early/Late)
2. **ORF Word Counts** - Oral Reading Fluency passage length targets
3. **Comprehension Word Counts** - Comprehension passage length specifications
4. **Comprehension Blueprint** - Complete assessment specifications by grade
5. **Form Requirements** - Which forms/genres to produce per grade
6. **Answer Options** - Number of answer choices by grade band
7. **Text Structures** - Available structures for narrative and nonfiction

## Status: ✅ COMPLETE

All 7 banks are:
- ✅ Implemented with immutable dataclasses
- ✅ Fully validated with automated tests
- ✅ Documented with docstrings and examples
- ✅ Exportable to JSON format
- ✅ Ready for use in generators

## Installation & Testing

```bash
# Navigate to project directory
cd reading_assessment_generator

# Run comprehensive test
python test_banks.py

# Expected output: "ALL TESTS PASSED"
```

## Quick Start

```python
from src.banks import (
    get_lexile_range,
    get_orf_target,
    get_blueprint,
    get_assessment_specs
)

# Get Lexile range for Grade 2 Early
lexile = get_lexile_range("2", "early")
print(lexile)  # 2 Early: 245L to 425L

# Get ORF target for Grade 2
orf = get_orf_target("2")
print(orf.target_word_count)  # 140

# Get complete comprehension blueprint for Grade 3
blueprint = get_blueprint("3")
print(blueprint.total_questions)  # 8
print(blueprint.distribution.to_dict())  # {'explicit': 4, 'implicit': 4}

# Get ALL specs for an assessment in one call
specs = get_assessment_specs("3", "comprehension", "early")
print(specs["lexile_range"])  # 480L to 645L
print(specs["word_count"])  # 175
print(specs["total_questions"])  # 8
```

## Architecture

```
src/banks/
├── __init__.py                    # Unified interface & validation
├── lexile_ranges.py              # Bank 1: Lexile bands
├── orf_word_counts.py            # Bank 2: ORF targets
├── comp_word_counts.py           # Bank 3: Comprehension word counts
├── comprehension_blueprint.py    # Bank 4: Assessment specs
├── form_requirements.py          # Bank 5: Form production
├── answer_options.py             # Bank 6: Answer choice counts
└── text_structures.py            # Bank 7: Text structures
```

## Bank Details

### Bank 1: Lexile Ranges
- **Purpose**: Define Lexile targeting for passage generation
- **Coverage**: K through 8+ (grades 9-12)
- **Structure**: Early and Late sub-bands per grade
- **Key Functions**:
  - `get_lexile_range(grade, band)` - Get range object
  - `get_midpoint_lexile(grade, band)` - Calculate midpoint for targeting
  - `validate_lexile_target(grade, band, target)` - Validate a target

### Bank 2: ORF Word Counts
- **Purpose**: Define passage length for timed fluency assessments
- **Coverage**: Grades 1-8
- **Basis**: Hasbrouck & Tindal (2017) Spring 75th percentile + 10
- **Key Functions**:
  - `get_orf_target(grade)` - Get complete ORF specs
  - `validate_word_count(grade, count)` - Check ±2 word compliance

### Bank 3: Comprehension Word Counts
- **Purpose**: Define passage length for comprehension assessments
- **Coverage**: K through 8+
- **Rule**: Average ±10% for narrative variation
- **Key Functions**:
  - `get_comp_word_count(grade)` - Get word count specs
  - `validate_word_count(grade, count)` - Check range compliance

### Bank 4: Comprehension Blueprint
- **Purpose**: Complete assessment specification by grade
- **Includes**:
  - Text access mode (listening vs. independent)
  - Question counts and distribution
  - Support requirements (pictures, text features)
  - Text types and example themes
- **Key Functions**:
  - `get_blueprint(grade)` - Get complete blueprint
  - `requires_picture(grade)` - Check if K-1 picture needed
  - `requires_text_features(grade)` - Check if 6+ features needed

### Bank 5: Form Requirements
- **Purpose**: Define which forms are produced per grade
- **Includes**:
  - Required bands (Early/Late)
  - Genre options per grade
  - Form naming conventions
- **Key Functions**:
  - `get_form_requirements(grade, type)` - Get requirements
  - `generate_form_id(...)` - Create standardized form IDs
  - `calculate_total_forms(...)` - Determine form count

### Bank 6: Answer Options
- **Purpose**: Define number of answer choices by grade
- **Standards**:
  - K-1: 2 options
  - 2-3: 3 options
  - 4-8+: 4 options
- **Key Functions**:
  - `get_num_options(grade)` - Get option count
  - `get_distractor_guidance(grade)` - Get quality requirements

### Bank 7: Text Structures
- **Purpose**: Define available structures per genre
- **Narrative**: chronological, problem_solution, sequence
- **Nonfiction**: descriptive, cause_effect, compare_contrast, problem_solution, sequence
- **Key Functions**:
  - `get_structure_definition(structure, genre)` - Get complete definition
  - `get_structure_names(genre)` - List available structures
  - `get_signal_words(structure, genre)` - Get transition words

## Anti-Drift Safeguards

These banks implement multiple anti-drift measures:

1. **Immutable Dataclasses**: All data structures are frozen
2. **Automatic Validation**: Banks validate on import
3. **Type Enforcement**: Enums prevent invalid values
4. **Lookup-Only Access**: No runtime modifications allowed
5. **Version Tracking**: Bank version embedded in exports

## JSON Export

All banks can be exported to JSON:

```python
from src.banks import export_all_banks_to_json
import json

# Export all banks
data = export_all_banks_to_json()

# Save to file
with open('banks_export.json', 'w') as f:
    json.dump(data, f, indent=2)
```

The export includes:
- Bank version number
- All 7 banks in structured format
- All metadata and documentation

## Testing

Run the test suite:

```bash
python test_banks.py
```

This will:
1. Validate all 7 banks
2. Test individual lookups
3. Test unified specs getter
4. Test form generation scenarios
5. Export to JSON

## Next Steps

With banks complete, the next phase is:

1. **Build Generators** (Week 3-5)
   - ORF Passage Generator
   - Comprehension Passage Generator
   - Question Generator
   - Recall Scoring Generator

2. **Create Validation System** (Week 6)
   - Word count validators
   - Question distribution validators
   - QRM→PIB→Passage alignment checker

3. **Implement API** (Week 7)
   - FastAPI endpoints
   - PDF generation
   - Versioning system

4. **Build Frontend** (Week 8-10)
   - React UI
   - Form wizard
   - Package downloader

## Support

For questions or issues:
1. Check bank validation with `python test_banks.py`
2. Review bank docstrings and examples
3. Examine `banks_export.json` for data structure

## Version

- **Module Version**: 1.0.0
- **Bank Version**: 2026.1
- **Last Updated**: January 12, 2026
