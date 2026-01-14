# Question Generator

**Purpose:** Generates multiple choice questions from QRM specifications and passage text.

**Created:** 2026-01-12  
**Schema Version:** 2026.1  
**Status:** ✅ Production Ready

---

## Overview

The Question Generator is **Step 4** in the comprehension assessment workflow:

1. **QRM Generator** → Plans questions
2. **PIB Generator** → Blueprints content
3. **Passage Generator** → Writes passage
4. **Question Generator** → Creates actual questions ← **YOU ARE HERE**

This generator takes the QRM specifications and the generated passage, then produces:
- Multiple choice questions with plausible distractors
- Complete answer key with evidence locations
- Grade-appropriate number of answer options (from Bank 6)

---

## Bank Usage

### Banks Referenced

- **Bank 4 (Comprehension Blueprint):** Via QRM for question specifications
- **Bank 6 (Answer Options):** Number of answer choices by grade
  - K-2: 3 options (A, B, C)
  - 3+: 4 options (A, B, C, D)

### Bank Functions Called

```python
from src.banks import get_num_options

num_options = get_num_options(grade)  # Returns 3 or 4
```

---

## Usage

### Basic Usage

```python
from src.generators import (
    create_qrm_generator,
    create_pib_generator,
    create_comprehension_passage_generator,
    create_question_generator
)
from src.utils import create_ai_client

# Initialize AI client
ai_client = create_ai_client("your_api_key")

# Step 1: Generate QRM
qrm_gen = create_qrm_generator(ai_client)
qrm = qrm_gen.generate(grade="2", genre="narrative", band="early")

# Step 2: Generate PIB
pib_gen = create_pib_generator(ai_client)
pib = pib_gen.generate(qrm_result=qrm)

# Step 3: Generate Passage
passage_gen = create_comprehension_passage_generator(ai_client)
passage = passage_gen.generate(qrm_result=qrm, pib_result=pib)

# Step 4: Generate Questions
question_gen = create_question_generator(ai_client)
result = question_gen.generate(qrm_result=qrm, passage_result=passage)

# Access questions
for q in result.questions:
    print(f"Q{q.question_number}: {q.question_text}")
    for opt in q.answer_options:
        marker = "✓" if opt.is_correct else " "
        print(f"  [{marker}] {opt.letter}. {opt.text}")
```

### Output Structure

```python
@dataclass
class QuestionGeneratorResult:
    questions: List[Question]           # All questions
    total_questions: int                # Count
    answer_key: AnswerKey              # Complete answer key
    
    # Metadata
    grade: str
    genre: str
    band: str
    form_id: str
    
    # Distributions (for validation)
    type_distribution: Dict[str, int]
    cognitive_distribution: Dict[str, int]
    
    # Links to source documents
    qrm_form_id: str
    passage_form_id: str
    
    # Bank constraints
    num_answer_options: int  # From Bank 6
    
    # Generation metadata
    generated_at: str
    schema_version: str
    bank_usage: Dict[str, str]
```

### Question Structure

```python
@dataclass
class Question:
    question_number: int
    question_text: str
    question_type: QuestionType  # explicit, implicit, vocabulary, etc.
    cognitive_demand: str        # low, medium, high
    answer_options: List[AnswerOption]
    correct_answer: str          # Letter (A, B, C, D)
    evidence_location: str       # Where answer is found
    evidence_text: str           # Actual text from passage
    points_possible: int = 1
```

---

## Features

### 1. QRM-Driven Question Generation

Questions are generated to match QRM specifications exactly:
- Question types (explicit, implicit, vocabulary, main_idea, etc.)
- Cognitive demands (low, medium, high)
- Evidence locations (beginning, middle, end, throughout)
- Content requirements

### 2. Plausible Distractor Generation

Uses QRM distractor guidance to create wrong answers that:
- Are plausible but clearly incorrect
- Test comprehension (not trick questions)
- Follow specific distractor types:
  - `character_confusion` - Wrong character name
  - `similar_name` - Name that sounds similar
  - `opposite` - Opposite of correct answer
  - `wrong_emotion` - Incorrect feeling/emotion
  - `detail_not_main` - Detail instead of main idea
  - `too_general` - Too broad/vague

### 3. Evidence Tracking

Each question includes:
- **Evidence Location:** Where in passage the answer is found
- **Evidence Text:** Exact quote from passage supporting the answer

### 4. Grade-Appropriate Answer Options

Automatically uses Bank 6 to determine number of options:
- **K-2:** 3 options (A, B, C)
- **3+:** 4 options (A, B, C, D)

### 5. Complete Answer Key

Generates answer key with:
- Question number → Correct letter mapping
- Total points possible
- Full question details for reference

---

## Validation

The generator validates:

1. **Question Count:** Matches QRM total
2. **Question Types:** Distribution matches QRM
3. **Cognitive Demands:** Distribution matches QRM
4. **Answer Options:** Correct number per grade (Bank 6)

Warnings are printed if any mismatch is detected.

---

## Example Output

```
================================================================================
QUESTIONS GENERATED SUCCESSFULLY
================================================================================

Form ID: COMP-2-EARLY-QUESTIONS-001
Total Questions: 6
Answer Options: 3 (Grade 2 from Bank 6)
Total Points: 6

Type Distribution:
  explicit: 2
  implicit: 2
  vocabulary: 1
  main_idea: 1

Cognitive Distribution:
  low: 2
  medium: 3
  high: 1

Bank Usage:
  - Bank 4 (Comprehension Blueprint): Via QRM for question specifications
  - Bank 6 (Answer Options): Grade 2 → 3 answer options

================================================================================
SAMPLE QUESTIONS
================================================================================

────────────────────────────────────────────────────────────────────────────────
Question 1 (explicit, low)
────────────────────────────────────────────────────────────────────────────────
What is the main character's name?

  [✓] A. Maya
  [ ] B. Jordan
  [ ] C. Maria

Correct Answer: A
Evidence: "Maya was excited for second grade."

================================================================================
ANSWER KEY
================================================================================
  Question 1: A
  Question 2: B
  Question 3: B
  Question 4: A
  Question 5: B
  Question 6: A
```

---

## Complete Workflow

```python
# Complete 4-step comprehension workflow
qrm = qrm_gen.generate(grade="2", genre="narrative", band="early")
pib = pib_gen.generate(qrm_result=qrm)
passage = passage_gen.generate(qrm_result=qrm, pib_result=pib)
questions = question_gen.generate(qrm_result=qrm, passage_result=passage)

# You now have:
# - QRM: Question specifications
# - PIB: Content blueprint
# - Passage: Actual text
# - Questions: Multiple choice questions with answer key

# Ready for: Packaging into complete assessment document
```

---

## Anti-Drift Compliance

✅ **Bank-Driven:**
- Number of answer options from Bank 6
- Question specifications from Bank 4 (via QRM)

✅ **Validation:**
- Validates question count matches QRM
- Validates type distribution matches QRM
- Validates cognitive distribution matches QRM

✅ **Immutable:**
- Uses frozen dataclasses
- Tracks bank usage
- Includes schema version

✅ **Traceable:**
- Links to QRM form ID
- Links to passage form ID
- Unique question form ID

---

## Testing

Run the built-in test:

```bash
cd /Users/lebron/Desktop/Bank\ Creator
python3.11 src/generators/question_generator.py
```

Expected output:
- ✓ 6 questions generated
- ✓ 3 answer options per question (Grade 2)
- ✓ Complete answer key
- ✓ Evidence tracking
- ✓ Bank usage logged

---

## Integration

The Question Generator is integrated into `src/generators/__init__.py`:

```python
from src.generators import (
    QuestionGenerator,
    QuestionGeneratorResult,
    Question,
    AnswerOption,
    AnswerKey,
    create_question_generator
)
```

---

## Next Steps

After generating questions, you can:

1. **Package Assessment:** Combine passage + questions into PDF
2. **Generate Recall Scoring:** Create recall rubric (Phase 2C next)
3. **Create Complete Package:** Bundle all materials for educators

---

## Technical Details

### Question Types Supported

```python
class QuestionType(Enum):
    EXPLICIT = "explicit"              # Stated directly in text
    IMPLICIT = "implicit"              # Requires inference
    VOCABULARY = "vocabulary"          # Word meaning
    MAIN_IDEA = "main_idea"           # Central concept
    INFERENCE = "inference"            # Draw conclusions
    CAUSE_EFFECT = "cause_effect"     # Causal relationships
    COMPARE_CONTRAST = "compare_contrast"  # Similarities/differences
    AUTHOR_PURPOSE = "author_purpose"  # Why author wrote
    TEXT_STRUCTURE = "text_structure"  # Organization
    POINT_OF_VIEW = "point_of_view"   # Perspective
    THEME = "theme"                    # Underlying message
```

### Distractor Types

- `character_confusion` - Wrong character
- `similar_name` - Name that sounds similar
- `opposite` - Opposite of correct answer
- `wrong_emotion` - Incorrect feeling
- `detail_not_main` - Detail instead of main idea
- `too_general` - Too broad
- `other_game` - Different game/activity
- `wrong_outcome` - Incorrect result
- `partial_wrong` - Partially correct but incomplete

---

## Files

- **Generator:** `src/generators/question_generator.py` (715 lines)
- **Documentation:** `docs/QUESTION_GENERATOR_README.md` (this file)
- **Template:** `templates/prompts/questions.j2` (exists, not yet used)

---

**Last Updated:** 2026-01-12  
**Status:** Production Ready  
**Phase:** 2C - Question & Recall Generators
