# Recall Scoring Generator

**Purpose:** Generates recall assessment scoring templates from comprehension passages.

**Created:** 2026-01-12  
**Schema Version:** 2026.1  
**Status:** ✅ Production Ready

---

## Overview

The Recall Scoring Generator creates detailed scoring guides for oral recall assessments. It analyzes passages sentence-by-sentence and generates:

- Key ideas students should recall (2-4 per sentence)
- Partial credit keywords (4-8 per sentence)
- 0-1-2 point rubric per sentence
- Example student responses for each score level

---

## Bank Usage

### Banks Referenced

- **Bank 4 (Comprehension Blueprint):** Via passage metadata for grade-appropriate expectations

### Bank Functions Called

No direct bank function calls - uses passage metadata from Comprehension Passage Generator.

---

## Usage

### Basic Usage

```python
from src.generators import (
    create_comprehension_passage_generator,
    create_recall_scoring_generator
)
from src.utils import create_ai_client

# Initialize AI client
ai_client = create_ai_client("your_api_key")

# Generate passage (Steps 1-3: QRM → PIB → Passage)
passage_gen = create_comprehension_passage_generator(ai_client)
passage = passage_gen.generate(qrm_result=qrm, pib_result=pib)

# Generate recall scoring template
recall_gen = create_recall_scoring_generator(ai_client)
scoring_guide = recall_gen.generate(passage_result=passage)

# Access scoring guide
print(f"Total Sentences: {scoring_guide.total_sentences}")
print(f"Max Points: {scoring_guide.max_total_points}")

for sent in scoring_guide.sentence_scoring:
    print(f"\nSentence {sent.sentence_number}: {sent.sentence_text}")
    print(f"Key Ideas: {len(sent.key_ideas)}")
    print(f"Keywords: {', '.join(sent.partial_keywords)}")
```

### Output Structure

```python
@dataclass
class RecallScoringGuide:
    # Passage information
    passage_text: str
    passage_title: Optional[str]
    total_sentences: int
    
    # Sentence-by-sentence scoring
    sentence_scoring: List[SentenceScoring]
    
    # Overall scoring
    max_total_points: int
    
    # Scoring guidelines
    general_instructions: str
    scoring_notes: List[str]
    
    # Metadata
    grade: str
    genre: str
    band: str
    form_id: str
    passage_form_id: str
    
    # Generation metadata
    generated_at: str
    schema_version: str
    bank_usage: Dict[str, str]
```

### Sentence Scoring Structure

```python
@dataclass
class SentenceScoring:
    sentence_number: int
    sentence_text: str
    max_points: int  # Typically 2
    
    # Key ideas student should recall
    key_ideas: List[KeyIdea]
    
    # Partial credit keywords (4-8 per sentence)
    partial_keywords: List[str]
    
    # Scoring rubric
    score_0_criteria: str  # No recall or incorrect
    score_1_criteria: str  # Partial recall
    score_2_criteria: str  # Complete recall
    
    # Example student responses
    example_score_0: str
    example_score_1: str
    example_score_2: str
```

---

## Features

### 1. Sentence-by-Sentence Analysis

Automatically splits passage into sentences and creates scoring criteria for each.

### 2. Key Ideas Identification

For each sentence, identifies 2-4 key ideas:
- **Essential:** Must be recalled for full credit (1.0 pts)
- **Important:** Should be recalled (0.5-1.0 pts)
- **Supporting:** Nice to have (0.5 pts)

### 3. Partial Credit Keywords

Identifies 4-8 specific words per sentence that indicate understanding:
- Proper nouns (character names, places)
- Key verbs (actions)
- Important adjectives (descriptors)

### 4. Clear Scoring Rubrics

Each sentence has objective criteria:
- **0 points:** No recall or completely incorrect
- **1 point:** Partial recall (some keywords OR one key idea)
- **2 points:** Complete recall (all essential key ideas)

### 5. Example Responses

Provides realistic student response examples for each score level to guide assessors.

---

## Example Output

```
================================================================================
RECALL SCORING GUIDE
================================================================================

Form ID: COMP-2-EARLY-RECALL-001
Passage: Making New Friends
Total Sentences: 9
Max Total Points: 18 (9 sentences × 2 points)

General Instructions:
  Read student's oral recall. Score each sentence 0-2 points based on key 
  ideas recalled. Award partial credit for keywords even if not exact wording.

Scoring Notes:
  • Accept paraphrasing if key ideas are present
  • Award 1 point if student uses 2+ keywords but misses key ideas
  • Award 2 points if all essential key ideas are present
  • Do not penalize for extra details or slightly different sequence

================================================================================
SAMPLE SENTENCE SCORING
================================================================================

────────────────────────────────────────────────────────────────────────────────
SENTENCE 1 (Max 2 points)
────────────────────────────────────────────────────────────────────────────────
"Maya was excited for second grade."

Key Ideas (2):
  • Maya is the main character (essential, 1.0 pts)
  • She is starting second grade (essential, 1.0 pts)

Partial Keywords (4):
  Maya, second grade, excited, school

Scoring Rubric:
  0 pts: No mention of Maya or second grade
  1 pt:  Mentions Maya OR second grade, but not both
  2 pts: States Maya is starting second grade

Example Responses:
  [0] "A girl went to school."
  [1] "Maya was happy."
  [2] "Maya was excited to start second grade."
```

---

## Complete Comprehension Workflow

```python
# Complete 5-step comprehension assessment workflow

# Step 1: Plan questions (QRM)
qrm = qrm_gen.generate(grade="2", genre="narrative", band="early")

# Step 2: Blueprint content (PIB)
pib = pib_gen.generate(qrm_result=qrm)

# Step 3: Write passage
passage = passage_gen.generate(qrm_result=qrm, pib_result=pib)

# Step 4: Generate questions (optional)
questions = question_gen.generate(qrm_result=qrm, passage_result=passage)

# Step 5: Generate recall scoring template
recall_scoring = recall_gen.generate(passage_result=passage)

# You now have:
# - Complete passage
# - Multiple choice questions with answer key
# - Recall scoring template with detailed rubrics
```

---

## Anti-Drift Compliance

✅ **Bank-Driven:**
- Uses passage metadata from Comprehension Passage Generator
- Inherits grade-level expectations from Bank 4

✅ **Validation:**
- Sentence splitting preserves exact passage text
- Key ideas aligned with passage content

✅ **Immutable:**
- Uses frozen dataclasses
- Tracks bank usage
- Includes schema version

✅ **Traceable:**
- Links to passage form ID
- Unique recall scoring form ID

---

## Testing

Run the built-in test:

```bash
cd /Users/lebron/Desktop/Bank\ Creator
python3.11 src/generators/recall_scoring_generator.py
```

Expected output:
- ✓ Complete passage generation (Steps 1-3)
- ✓ Recall scoring guide with 9 sentences
- ✓ 18 max points (9 × 2)
- ✓ Key ideas, keywords, and rubrics for each sentence
- ✓ Example responses for 0, 1, and 2 points

---

## Integration

The Recall Scoring Generator is integrated into `src/generators/__init__.py`:

```python
from src.generators import (
    RecallScoringGenerator,
    RecallScoringGuide,
    SentenceScoring,
    KeyIdea,
    create_recall_scoring_generator
)
```

---

## Use Cases

### 1. Oral Recall Assessments
Educators read passage to student, then student recalls what they remember. Assessor scores using this template.

### 2. Written Recall Assessments
Student reads passage, then writes what they remember. Assessor scores using this template.

### 3. Comprehension Verification
Alternative to multiple choice - tests deeper comprehension through free recall.

---

## Scoring Philosophy

**Focus on Meaning, Not Exact Wording:**
- Accept paraphrasing if key ideas are present
- Award partial credit for keywords
- Don't penalize for extra details or different sequence
- Objective criteria minimize assessor bias

---

## Files

- **Generator:** `src/generators/recall_scoring_generator.py` (597 lines)
- **Documentation:** `docs/RECALL_SCORING_GENERATOR_README.md` (this file)
- **Template:** `templates/prompts/recall_scoring.j2` (exists, not yet used)

---

**Last Updated:** 2026-01-12  
**Status:** Production Ready  
**Phase:** 2C - Question & Recall Generators (COMPLETE)
