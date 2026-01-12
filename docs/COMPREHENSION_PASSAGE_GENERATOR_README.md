# Comprehension Passage Generator

**Purpose:** Write actual passage text from QRM + PIB blueprint  
**Created:** 2026-01-12  
**Schema Version:** 2026.1  
**Phase:** 2B - Comprehension Generator (Step 3 of 3 - FINAL)

---

## Overview

The Comprehension Passage Generator is the **final step** in the comprehension assessment workflow. It takes the question plan (QRM) and content blueprint (PIB) and writes the actual passage text that students will read.

### The Complete 3-Step Workflow

```
Step 1: QRM ✅
  Input: Grade, genre, band
  Output: Question plan (6 questions with requirements)
  
Step 2: PIB ✅
  Input: QRM
  Output: Content blueprint (scenes, characters, vocabulary)
  
Step 3: PASSAGE ✅ (THIS GENERATOR)
  Input: QRM + PIB
  Output: Actual passage text (200 words at 300-400L)
```

### Why This Approach Works

**Traditional Problem:**
Write passage → Try questions → They don't work → Rewrite passage → Repeat

**Our Solution:**
Plan questions (QRM) → Plan content (PIB) → Write passage → Questions work first time!

---

## What It Generates

The Passage Generator produces a **ComprehensionPassageResult** containing:

### 1. The Passage
- **Passage Text**: The actual written passage
- **Title**: Engaging, grade-appropriate title
- **Word Count**: Actual count vs. target (from Bank 3)
- **Lexile Target**: From Bank 1 (via PIB)

### 2. Validation Results
- **Word Count Validation**: Within ±20 words of target?
- **Vocabulary Validation**: All required words present?
- **Scene Coverage**: All scenes identifiable?
- **Overall Pass/Fail**: Does passage meet all requirements?

### 3. Metadata & Traceability
- **Form IDs**: Links to QRM and PIB forms
- **Bank Usage**: Which banks were used
- **Generation Timestamp**: When passage was created
- **Schema Version**: For future compatibility

---

## Bank Usage

### Bank 1 (Lexile Ranges) ✅ (via PIB)
**Used For:**
- Target Lexile range for passage
- Guides vocabulary complexity
- Guides sentence structure complexity

**Example:**
```python
Grade 2, Early Band → 300-400L
```

### Bank 3 (Comp Word Counts) ✅ (via PIB)
**Used For:**
- Target word count
- Validation range (±20 words)

**Example:**
```python
Grade 2 → Target: 200 words (180-220 acceptable)
```

### Bank 7 (Text Structures) ✅ (via PIB)
**Used For:**
- Text organization pattern
- Guides how scenes flow together

**Example:**
```python
Narrative → chronological
Nonfiction → cause-effect
```

---

## Anti-Drift Compliance

### ✅ Blueprint-Driven
- Follows PIB scenes exactly
- Includes all required details from PIB
- Uses vocabulary with specified contexts
- Maintains bank-specified constraints

### ✅ Validated Output
- Word count checked against Bank 3
- Vocabulary presence verified
- Scene structure validated
- Automatic retry if validation fails (up to 2 retries)

### ✅ Complete Traceability
- Links to source QRM form
- Links to source PIB form
- Records bank usage
- Tracks generation metadata

---

## Usage

### Basic Usage

```python
from comprehension_passage_generator import create_comprehension_passage_generator
from qrm_generator import create_qrm_generator
from pib_generator import create_pib_generator
from ai_client import create_ai_client

# Create AI client
ai_client = create_ai_client("your_api_key")

# Step 1: Generate QRM
qrm_gen = create_qrm_generator(ai_client)
qrm = qrm_gen.generate(
    grade="2",
    genre="narrative",
    band="early",
    topic="kindness"
)

# Step 2: Generate PIB
pib_gen = create_pib_generator(ai_client)
pib = pib_gen.generate(qrm_result=qrm)

# Step 3: Generate Passage
passage_gen = create_comprehension_passage_generator(ai_client)
result = passage_gen.generate(
    qrm_result=qrm,
    pib_result=pib
)

# Access passage
print(result.passage_title)
print(result.passage_text)
print(f"Word count: {result.actual_word_count}/{result.target_word_count}")
```

### With Retry Logic

```python
# Generator automatically retries on validation failure
result = passage_gen.generate(
    qrm_result=qrm,
    pib_result=pib,
    max_retries=3  # Try up to 3 times
)

# Check if validation passed
if result.validation.validation_passed:
    print("✓ Passage validated successfully")
else:
    print("⚠ Validation warnings:")
    for warning in result.validation.warnings:
        print(f"  {warning}")
```

---

## Output Structure

### ComprehensionPassageResult Dataclass

```python
@dataclass
class ComprehensionPassageResult:
    # The passage
    passage_text: str
    passage_title: Optional[str]
    
    # Metadata
    grade: str
    genre: str
    band: str
    form_id: str
    
    # Word count
    actual_word_count: int
    target_word_count: int
    
    # Lexile
    target_lexile: str
    
    # Question support
    total_questions: int
    question_coverage_verified: bool
    
    # Structure
    text_structure: str
    
    # Vocabulary
    vocabulary_words: List[str]
    vocabulary_verified: bool
    
    # Validation
    validation: PassageValidation
    
    # Links to source documents
    qrm_form_id: str
    pib_form_id: str
    
    # Generation metadata
    generated_at: str
    schema_version: str
    bank_usage: Dict[str, str]
```

### PassageValidation Dataclass

```python
@dataclass
class PassageValidation:
    word_count_valid: bool
    word_count_actual: int
    word_count_target: int
    word_count_acceptable_range: tuple  # (min, max)
    
    lexile_target: str
    lexile_note: str  # Cannot auto-validate
    
    vocabulary_present: bool
    vocabulary_found: List[str]
    vocabulary_missing: List[str]
    
    scenes_covered: bool
    scenes_expected: int
    scenes_identifiable: int
    
    validation_passed: bool
    warnings: List[str]
```

---

## Example Output

### Grade 2 Narrative Example

**Inputs:**
- QRM: 6 questions (2 explicit, 2 implicit, 1 vocabulary, 1 main idea)
- PIB: 4 scenes, 2 characters, "hesitant" vocabulary

**Generated Passage:**

```
Title: Maya's First Day of Second Grade

Maya Rodriguez stood at the entrance of Lincoln Elementary School, 
her new backpack on her shoulders. Today was the first day of second 
grade, and she felt excited and a little nervous. The playground was 
full of students laughing and talking as they arrived.

During morning work, Maya noticed a new student named Jordan sitting 
alone at a desk near the window. Jordan looked hesitant to join the 
other students, standing at the edge of the group with an uncertain 
expression. Maya could tell Jordan needed a friend.

At recess, Maya had an idea. She organized a game of tag with her 
classmates on the playground. When everyone was ready to play, Maya 
ran over to Jordan. "Do you want to play tag with us?" she asked 
with a big smile. Jordan hesitated for just a moment, then nodded 
and followed Maya to join the game. Soon Jordan was running and 
laughing with everyone else.

By the end of the day, Maya and Jordan walked to the buses together. 
"Thanks for inviting me to play," Jordan said. "You made my first 
day really great!" Maya felt happy knowing she had helped someone 
feel welcome. She realized that being kind and including others had 
made her own day better too. Making a new friend was the best part 
of starting second grade.
```

**Metadata:**
- Word Count: 221 / 200 target (within ±20)
- Vocabulary: "hesitant" ✓ found
- Target Lexile: 300-400L
- Scenes: 4 identifiable (opening, morning work, recess, end of day)
- Validation: PASSED

---

## Validation Rules

### Word Count Validation
```python
target = pib.target_word_count  # From Bank 3
acceptable_min = target - 20
acceptable_max = target + 20

if acceptable_min <= actual_count <= acceptable_max:
    word_count_valid = True
```

**Why ±20 words?**
- Allows natural sentence endings
- Prevents awkward cuts
- Maintains passage quality

### Vocabulary Validation
```python
passage_lower = passage_text.lower()
for required_word in pib.vocabulary_targets:
    if required_word.lower() not in passage_lower:
        warnings.append(f"Missing: {required_word}")
        vocabulary_present = False
```

**Requirements:**
- All vocabulary words must appear
- Context should match PIB guidance
- Natural integration (not forced)

### Scene Coverage Validation
```python
# Basic check: count paragraphs
paragraphs = passage_text.split('\n\n')
identifiable_scenes = len([p for p in paragraphs if len(p) > 0])

# Should roughly match expected scene count
scenes_covered = identifiable_scenes >= (expected_scenes - 1)
```

**Note:** This is a heuristic. More sophisticated analysis would check actual content.

### Overall Validation
```python
validation_passed = (
    word_count_valid and
    vocabulary_present and
    scenes_covered
)
```

All three must pass for overall validation success.

---

## Retry Logic

If validation fails, generator automatically retries:

```python
for attempt in range(max_retries + 1):
    passage_text = generate_passage()
    validation = validate_passage()
    
    if validation.passed or attempt == max_retries:
        return result
```

**Retry Scenarios:**
- Word count outside acceptable range
- Missing vocabulary words
- Too few identifiable scenes

**Max Retries:** Default 2, configurable

---

## Integration with Workflow

### Complete Assessment Generation

```python
# Step 1: Plan questions
qrm = qrm_generator.generate(
    grade="2",
    genre="narrative",
    band="early"
)

# Step 2: Plan content
pib = pib_generator.generate(qrm_result=qrm)

# Step 3: Write passage
passage = passage_generator.generate(
    qrm_result=qrm,
    pib_result=pib
)

# Result: Complete passage ready for questions
print(passage.passage_text)
print(f"Supports {passage.total_questions} questions")
print(f"Form IDs: QRM={passage.qrm_form_id}, PIB={passage.pib_form_id}, Passage={passage.form_id}")
```

### With Question Generation (Next Phase)

```python
# Generate passage
passage = passage_generator.generate(qrm, pib)

# Generate questions (Phase 2C - to be built)
questions = question_generator.generate(
    qrm=qrm,
    passage=passage
)

# Package complete assessment
assessment = {
    "passage": passage.passage_text,
    "questions": questions,
    "answer_key": answer_key,
    "form_id": passage.form_id
}
```

---

## Quality Standards

### Coherence
- Scenes flow naturally
- Logical transitions
- Consistent tone

### Age-Appropriateness
- Vocabulary matches grade level
- Sentence complexity appropriate
- Content relatable to students

### Evidence Quality
- Questions clearly answerable
- Evidence explicit or inferable
- Context-rich vocabulary

### Engagement
- Interesting content
- Clear narrative/topic
- Satisfying resolution (narrative)

---

## Common Issues & Solutions

### Issue: Word Count Too High/Low
**Cause:** AI didn't follow target precisely  
**Solution:** Retry mechanism adjusts; usually works by 2nd attempt

### Issue: Vocabulary Missing
**Cause:** AI forgot to include required word  
**Solution:** Automatic retry; PIB context helps AI place naturally

### Issue: Scenes Not Identifiable
**Cause:** Scenes blended together without clear breaks  
**Solution:** PIB instructions emphasize scene separation

### Issue: Questions Not Answerable
**Cause:** Passage didn't follow PIB blueprint  
**Solution:** Strengthen PIB detail; review generated passage against PIB

---

## Lexile Targeting

### Current Approach
- Target Lexile provided to AI in prompt (from Bank 1)
- AI writes at appropriate grade level
- Vocabulary and syntax complexity guided by target

### Limitation
- Cannot automatically validate Lexile without external tool
- Passage marked with target Lexile but not verified

### Best Practice
- Trust Bank 1 targets (research-based)
- Use grade-appropriate vocabulary
- Follow PIB scene structure
- **Optional:** Use external Lexile analyzer for verification

---

## Testing

### Unit Test
```python
result = generator.generate(qrm, pib)

assert result.passage_text is not None
assert len(result.passage_text) > 0
assert result.actual_word_count > 0
assert result.form_id is not None
assert result.qrm_form_id == qrm.form_id
assert result.pib_form_id == pib.form_id
```

### Integration Test
```python
# Full workflow test
qrm = qrm_gen.generate(grade="2", genre="narrative", band="early")
pib = pib_gen.generate(qrm_result=qrm)
passage = passage_gen.generate(qrm_result=qrm, pib_result=pib)

# Verify passage supports all questions
for q in qrm.questions:
    # Check that required content from QRM appears in passage
    assert any(keyword in passage.passage_text.lower() 
               for keyword in extract_keywords(q.content_requirement))
```

### Validation Test
```python
result = generator.generate(qrm, pib)

# Should pass validation
assert result.validation.validation_passed
assert result.validation.word_count_valid
assert result.validation.vocabulary_present
assert len(result.validation.warnings) == 0
```

---

## Future Enhancements

### Potential Additions
- [ ] External Lexile validation integration
- [ ] Readability metrics (Flesch-Kincaid)
- [ ] Automated question answerability check
- [ ] Multiple passage variations from same PIB
- [ ] Illustration placement suggestions (K-1)

### Not Planned (Out of Scope)
- ❌ Question generation (that's Question Generator Phase 2C)
- ❌ Answer key creation (that's Question Generator Phase 2C)
- ❌ PDF formatting (that's Phase 5 Packaging)

---

## Dependencies

**Required:**
- AI client (OpenAI, Anthropic, or Mock)
- QRM Generator (provides question plan)
- PIB Generator (provides content blueprint)
- Bank 1 (lexile_ranges.py) - via PIB
- Bank 3 (comp_word_counts.py) - via PIB
- Bank 7 (text_structures.py) - via PIB
- Python 3.9+

**Optional:**
- Template loader (uses inline prompt as fallback)
- Jinja2 template (comp_passage.j2)

---

## Files

**Source:**
- `comprehension_passage_generator.py` (main generator)

**Related:**
- QRM Generator (provides input)
- PIB Generator (provides input)
- Question Generator (uses passage output - Phase 2C, to be built)

---

**Status:** ✅ Complete and Tested  
**Next Step:** Build Question Generator (Phase 2C)  
**Phase 2B:** QRM ✅ | PIB ✅ | Passage ✅ | COMPLETE!
