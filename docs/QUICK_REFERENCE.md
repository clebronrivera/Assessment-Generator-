# Foundation Banks - Quick Reference Card

## Import Everything You Need

```python
from src.banks import (
    get_assessment_specs,      # Get all specs at once
    get_lexile_range,         # Bank 1: Lexile ranges
    get_orf_target,           # Bank 2: ORF word counts
    get_comp_word_count,      # Bank 3: Comp word counts
    get_blueprint,            # Bank 4: Comp blueprint
    get_form_requirements,    # Bank 5: Form requirements
    get_num_options,          # Bank 6: Answer options
    get_structure_names       # Bank 7: Text structures
)
```

## Common Use Cases

### 1. Get Everything for an Assessment (Easiest)

```python
specs = get_assessment_specs("3", "comprehension", "early")
# Returns dictionary with all specifications
```

### 2. Generate ORF Assessment

```python
# Get specifications
grade = "2"
band = "early"

lexile = get_lexile_range(grade, band)
orf = get_orf_target(grade)

print(f"Lexile: {lexile.lexile_min} to {lexile.lexile_max}")
print(f"Target: {orf.target_word_count} words")
print(f"Range: {orf.min_word_count}-{orf.max_word_count}")
```

### 3. Generate Comprehension Assessment

```python
# Get specifications
grade = "3"
band = "early"

lexile = get_lexile_range(grade, band)
word_count = get_comp_word_count(grade)
blueprint = get_blueprint(grade)

print(f"Lexile: {lexile.lexile_min} to {lexile.lexile_max}")
print(f"Words: {word_count.average} (range: {word_count.min_allowed}-{word_count.max_allowed})")
print(f"Questions: {blueprint.total_questions}")
print(f"Distribution: {blueprint.distribution.to_dict()}")
print(f"Answer options: {get_num_options(grade)}")
```

### 4. Check Requirements

```python
from src.banks import requires_picture, requires_text_features

# K-1 picture requirements
if requires_picture("K"):
    print("Generate picture description")

# 6+ text feature requirements
if requires_text_features("7"):
    print("Include headings and organizational features")
```

### 5. Get Available Structures

```python
from src.banks import get_structure_names, get_structure_definition

# List structures
narrative_structures = get_structure_names("narrative")
nonfiction_structures = get_structure_names("nonfiction")

# Get details
structure = get_structure_definition("problem_solution", "narrative")
print(f"Signal words: {structure.signal_words}")
print(f"Example topics: {structure.example_topics}")
```

### 6. Generate Form IDs

```python
from src.banks.form_requirements import generate_form_id

form_id = generate_form_id("3", "comprehension", "early", "narrative")
# Returns: RC-COMP-G3-EARLY-NARR-A
```

### 7. Validate Word Counts

```python
from src.banks import validate_orf_word_count, validate_comp_word_count

# ORF validation (±2 words)
is_valid = validate_orf_word_count("2", 140)  # True
is_valid = validate_orf_word_count("2", 145)  # False

# Comprehension validation (±10% range)
is_valid = validate_comp_word_count("3", 175)  # True
is_valid = validate_comp_word_count("3", 200)  # False
```

## Grade Ranges

- **ORF**: Grades 1-8
- **Comprehension**: K-8+ (where 8+ = grades 9-12)
- **Bands**: "early" or "late"
- **Genres**: "narrative", "nonfiction", "both"

## Question Types by Grade

| Grade | Explicit | Implicit | Vocabulary | Main Idea | Text Structure | Inference Advanced |
|-------|----------|----------|------------|-----------|----------------|-------------------|
| K     | 4        | -        | -          | -         | -              | -                 |
| 1     | 4        | 1        | -          | -         | -              | -                 |
| 2     | 4        | 2        | -          | -         | -              | -                 |
| 3     | 4        | 4        | -          | -         | -              | -                 |
| 4     | 4        | 4        | 2          | -         | -              | -                 |
| 5     | 4        | 4        | 2          | 2         | -              | -                 |
| 6     | 4        | 4        | 2          | 2         | 2              | -                 |
| 7     | 4        | 4        | 2          | 2         | 2              | 2                 |
| 8+    | 4        | 4        | 2          | 2         | 2              | 4                 |

## Answer Options by Grade

- **K-1**: 2 options
- **2-3**: 3 options
- **4-8+**: 4 options

## Special Requirements

### K-1 (Listening Comprehension)
```python
blueprint = get_blueprint("K")
assert blueprint.text_access_mode.value == "listening"
assert blueprint.item_access_mode.value == "read_aloud"
assert requires_picture("K") == True
```

### Grades 6+ (Text Features)
```python
assert requires_text_features("6") == True
assert requires_text_features("7") == True
assert requires_text_features("8+") == True
```

## Text Structures

### Narrative
- chronological
- problem_solution
- sequence

### Nonfiction
- descriptive
- cause_effect
- compare_contrast
- problem_solution
- sequence

## Testing

```bash
# Run all tests
python test_banks.py

# Expected output: "ALL TESTS PASSED"
```

## Validation Messages

Banks auto-validate on import:
```
✓ Bank 1 (Lexile Ranges) validated successfully
✓ Bank 2 (ORF Word Counts) validated successfully
✓ Bank 3 (Comprehension Word Counts) validated successfully
✓ Bank 4 (Comprehension Blueprint) validated successfully
✓ Bank 5 (Form Requirements) validated successfully
✓ Bank 6 (Answer Options) validated successfully
✓ Bank 7 (Text Structures) validated successfully
```

## Common Errors

**Import Error**: Make sure you're running from the project root
```bash
cd reading_assessment_generator
python -c "from src.banks import get_assessment_specs"
```

**KeyError**: Check grade format
- ✅ "K", "1", "2", "3", "4", "5", "6", "7", "8", "8+"
- ❌ "0", "K5", "9", "12"

**ValueError**: Check band/genre spelling
- ✅ "early", "late"
- ❌ "Early", "LATE", "mid"

## Pro Tips

1. **Use get_assessment_specs()** for most tasks - it's the easiest
2. **Trust the types** - Enums prevent typos
3. **Check requirements first** - Use requires_picture() and requires_text_features()
4. **Validate word counts** - Use validate functions before finalizing
5. **Print blueprints** - They're human-readable for debugging

## Example: Complete Assessment Generation Flow

```python
from src.banks import get_assessment_specs

# 1. Get all specs
specs = get_assessment_specs("3", "comprehension", "early")

# 2. Generate passage
# - Target Lexile: specs["lexile_midpoint"]
# - Target words: specs["word_count"]
# - Structure: Choose from specs["genre_options"]

# 3. Generate questions
# - Total: specs["total_questions"]
# - Distribution: specs["question_distribution"]
# - Options: specs["num_answer_options"]

# 4. Validate
# - Word count in range: specs["word_count_range"]
# - All questions present
# - Answer options correct

# 5. Package
# - Form ID from generate_form_id()
# - Include all materials
```

---

**Version**: 2026.1  
**Last Updated**: January 12, 2026
