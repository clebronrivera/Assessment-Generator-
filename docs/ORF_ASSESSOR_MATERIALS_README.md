# ORF Assessor Materials Generator

**Purpose:** Generates complete assessor materials package for Oral Reading Fluency assessments  
**Created:** 2026-01-12  
**Schema Version:** 2026.1  
**Phase:** 2A - ORF Generator  

---

## Overview

The ORF Assessor Materials Generator produces all materials needed by an assessor to properly administer, score, and interpret an Oral Reading Fluency assessment. It works in conjunction with the ORF Passage Generator to create a complete assessment package.

**Key Feature:** This generator does NOT use AI. All content is deterministic and template-based, ensuring 100% consistency across all assessments.

---

## What It Generates

### 1. Administration Materials
- **60-Second Timing Script**: Exact script for introducing and timing the assessment
- **3-Second Word Supply Rule**: When and how to supply words to struggling readers
- **General Instructions**: Complete administration protocol

### 2. Scoring Materials
- **Score Sheet**: Complete scoring form with calculations
- **WCPM Benchmarks**: Grade-specific targets from Bank 2 (Fall/Winter/Spring)
- **Accuracy Calculator**: Formula and examples for calculating reading accuracy
- **Prosody Rubric**: NAEP-aligned 4-level fluency scale

### 3. Error Tracking Materials
- **Error Marking Grid**: System for marking errors during reading
- **Error Type Definitions**: Substitutions, omissions, insertions, hesitations, etc.
- **Marking Examples**: Visual guide for real-time error notation

---

## Bank Usage

### Bank 2 (ORF Word Counts) ✅
**Used For:**
- WCPM (Words Correct Per Minute) benchmarks by season
- Fall, Winter, Spring targets for each grade
- Benchmark comparison on score sheet

**Example:**
```python
Bank 2 Grade 2:
- Fall Target: 50 WCPM
- Winter Target: 70 WCPM
- Spring Target: 90 WCPM
```

**No Other Banks Needed:** This generator produces standardized materials. Only WCPM benchmarks vary by grade.

---

## Anti-Drift Compliance

### ✅ Bank-Driven
- All WCPM benchmarks from Bank 2
- No hardcoded grade targets
- Consistent across all generated materials

### ✅ Deterministic Output
- No AI generation = no variability
- Same inputs always produce identical outputs
- Template-based with bank value injection

### ✅ Research-Aligned
- 60-second standard timing (DIBELS, AIMSweb)
- 3-second word supply rule (research-based)
- NAEP prosody rubric (validated)
- Standard error marking system

---

## Usage

### Basic Usage

```python
from orf_assessor_materials_generator import create_orf_assessor_materials_generator

# Create generator
generator = create_orf_assessor_materials_generator()

# Generate materials for a specific passage
materials = generator.generate(
    grade="2",
    passage_text="The cat ran across...",
    passage_word_count=150,
    form_id="ORF-2-EARLY-001"
)

# Access components
print(materials.timing_script)
print(materials.score_sheet)
print(materials.error_marking_grid)
print(materials.prosody_rubric)
```

### Complete Workflow

```python
from orf_generator import create_orf_generator
from orf_assessor_materials_generator import create_orf_assessor_materials_generator
from ai_client import create_ai_client

# Step 1: Generate passage
ai_client = create_ai_client("your_api_key")
passage_gen = create_orf_generator(ai_client)
passage_result = passage_gen.generate(grade="2", band="early")

# Step 2: Generate assessor materials
materials_gen = create_orf_assessor_materials_generator()
materials = materials_gen.generate(
    grade=passage_result.metadata["grade"],
    passage_text=passage_result.passage_text,
    passage_word_count=passage_result.metadata["actual_word_count"],
    form_id=passage_result.metadata["form_id"]
)

# Step 3: Package for distribution
assessment_package = {
    "student_passage": passage_result.passage_text,
    "assessor_copy": passage_result.passage_text,  # Same text, will be marked
    "administration_script": materials.timing_script,
    "word_supply_rules": materials.word_supply_rules,
    "score_sheet": materials.score_sheet,
    "error_marking_guide": materials.error_marking_grid,
    "prosody_rubric": materials.prosody_rubric,
    "benchmarks": materials.wcpm_benchmark
}
```

---

## Output Structure

### ORFAssessorMaterials Dataclass

```python
@dataclass
class ORFAssessorMaterials:
    # Administration
    timing_script: str                    # 60-second protocol
    word_supply_rules: str                # 3-second rule
    general_instructions: str             # Complete admin guide
    
    # Scoring
    score_sheet: str                      # Complete scoring form
    wcpm_benchmark: Dict[str, int]        # Fall/winter/spring targets
    accuracy_calculation: str             # Formula with examples
    prosody_rubric: str                   # 4-level NAEP scale
    
    # Error Marking
    error_marking_grid: str               # Marking system guide
    error_types: Dict[str, str]           # Error type definitions
    
    # Metadata
    grade: str                            # Grade level
    passage_word_count: int               # Total words in passage
    form_id: str                          # Form identifier
    generated_at: str                     # ISO timestamp
    schema_version: str                   # "2026.1"
    bank_usage: Dict[str, str]            # Which banks were used
```

---

## Components Detail

### 1. Timing Script
**Purpose:** Standardized administration for 60-second timing  
**Includes:**
- Setup checklist
- Exact script to say to student
- During-reading protocols
- 60-second stopping procedure
- Post-reading steps

**Research Basis:** DIBELS, AIMSweb, and other CBM protocols use 60-second standard timing

### 2. Word Supply Rules
**Purpose:** Consistent intervention for hesitations  
**Includes:**
- When to supply words (3-second rule)
- How to count 3 seconds
- How to mark supplied words
- Self-correction handling

**Research Basis:** 3-second rule prevents frustration while maintaining assessment integrity

### 3. Score Sheet
**Purpose:** Complete scoring and interpretation form  
**Includes:**
- Student information section
- Step-by-step calculation guide
- WCPM calculation (Words Read - Errors)
- Accuracy calculation
- Benchmark comparison with grade-specific targets from Bank 2
- Prosody rating section
- Performance level indicators
- Notes section

**Auto-Populated:**
- Form ID
- Grade level
- Passage word count
- WCPM benchmarks (Fall/Winter/Spring from Bank 2)

### 4. Accuracy Calculator
**Purpose:** Guide for calculating reading accuracy percentage  
**Includes:**
- Formula: (Words Read - Errors) / Words Read × 100
- Three worked examples with different performance levels
- Accuracy interpretation guidelines (97-100%, 90-96%, <90%)

**Research Basis:** Accuracy matters as much as speed for determining instructional level

### 5. Prosody Rubric
**Purpose:** Evaluate reading fluency beyond speed and accuracy  
**Includes:**
- 4-level scale (NAEP-aligned)
- Phrasing & expression descriptors
- Smoothness indicators
- Pace considerations
- Notes section for observations

**Research Basis:** NAEP Oral Reading Fluency Scale, validated for grades 1-8

### 6. Error Marking Grid
**Purpose:** Real-time error notation system  
**Includes:**
- 7 error/notation types with visual examples
- Substitutions, omissions, insertions, hesitations
- Self-corrections and repetitions (not counted as errors)
- Last-word-read marking (] bracket at 60 seconds)
- Passage-specific example using actual passage text

**Research Basis:** Standard miscue analysis conventions

---

## Quality Standards

### Consistency
- ✅ Same materials for same grade across all generations
- ✅ WCPM benchmarks always from Bank 2
- ✅ Standard 60-second timing protocol
- ✅ Consistent error marking conventions

### Completeness
- ✅ Everything needed to administer assessment
- ✅ Everything needed to score assessment
- ✅ Everything needed to interpret results
- ✅ No additional materials required

### Usability
- ✅ Clear instructions for assessors
- ✅ Step-by-step scoring guidance
- ✅ Visual examples for error marking
- ✅ Professional formatting

### Research Alignment
- ✅ DIBELS/AIMSweb timing protocols
- ✅ NAEP prosody rubric
- ✅ Standard CBM error conventions
- ✅ Evidence-based benchmarks

---

## Integration with ORF Generator

The Assessor Materials Generator is designed to work seamlessly with the ORF Passage Generator:

```python
# ORF Generator produces:
{
    "passage_text": "...",
    "metadata": {
        "grade": "2",
        "actual_word_count": 150,
        "form_id": "ORF-2-EARLY-001",
        ...
    }
}

# Assessor Materials Generator consumes:
materials = generator.generate(
    grade=metadata["grade"],           # From passage metadata
    passage_text=passage_text,         # The actual passage
    passage_word_count=metadata["actual_word_count"],  # Exact count
    form_id=metadata["form_id"]        # Form identifier
)
```

**Result:** Complete assessment package with matching metadata across all components

---

## Error Handling

### Missing Banks
```python
# If banks cannot be imported, falls back to mock data
# Prints warning but continues operation
# Useful for testing without full project setup
```

### Invalid Grade
```python
# If grade not in Bank 2, uses default values
# Logs warning in bank_usage metadata
```

---

## Testing

### Unit Tests
```python
# Test materials generation
materials = generator.generate(
    grade="2",
    passage_text="Sample text",
    passage_word_count=150,
    form_id="TEST-001"
)

assert materials.grade == "2"
assert materials.passage_word_count == 150
assert "Bank 2" in materials.bank_usage
assert materials.wcpm_benchmark["fall"] > 0
assert len(materials.timing_script) > 0
```

### Integration Tests
```python
# Test with actual ORF generator output
passage = orf_generator.generate(grade="2", band="early")
materials = materials_generator.generate(
    grade=passage.metadata["grade"],
    passage_text=passage.passage_text,
    passage_word_count=passage.metadata["actual_word_count"],
    form_id=passage.metadata["form_id"]
)

# Verify metadata alignment
assert materials.grade == passage.metadata["grade"]
assert materials.form_id == passage.metadata["form_id"]
```

---

## Future Enhancements

### Potential Additions
- [ ] Spanish language materials
- [ ] Alternative timing protocols (90 seconds, 120 seconds)
- [ ] Digital scoring worksheet (JSON/CSV export)
- [ ] Progress monitoring templates
- [ ] Parent-friendly results summary

### Not Planned (Out of Scope)
- ❌ AI-generated materials (defeats purpose of deterministic output)
- ❌ Custom scoring rubrics (standardization required)
- ❌ Grade-specific variations beyond benchmarks (consistency required)

---

## Changelog

### 2026-01-12 - Initial Creation
- Complete assessor materials generator
- 7 major components (timing, scoring, error marking, etc.)
- Bank 2 integration for WCPM benchmarks
- NAEP-aligned prosody rubric
- Research-based protocols (60-second timing, 3-second rule)
- Deterministic, template-based generation (no AI)
- Full documentation and examples

---

## Files

**Source:**
- `src/generators/orf_assessor_materials_generator.py` (main generator)

**Dependencies:**
- `src/banks/orf_word_counts.py` (Bank 2 - WCPM benchmarks)
- Python 3.9+ (uses dataclasses, type hints)

**Related:**
- `src/generators/orf_generator.py` (generates passages)
- `src/generators/base_generator.py` (base class, if used)

---

## Support

**Questions?** Check:
1. This README
2. TASK_LIST.md (Phase 2A section)
3. CHANGELOG.md (implementation details)
4. Bank 2 documentation (WCPM benchmarks)

**Issues?** Verify:
1. Bank 2 is available and has data for your grade
2. Grade parameter is valid (1-8)
3. Passage word count is reasonable (>50 words)

---

**Status:** ✅ Production Ready  
**Testing:** ✅ Ready for Unit Tests  
**Integration:** ✅ Ready for ORF Generator Integration  
**Documentation:** ✅ Complete
