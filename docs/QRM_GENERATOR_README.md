# QRM (Question Requirement Matrix) Generator

**Purpose:** Pre-passage planning to ensure all comprehension questions will be answerable  
**Created:** 2026-01-12  
**Schema Version:** 2026.1  
**Phase:** 2B - Comprehension Generator (Step 1 of 3)

---

## Overview

The QRM Generator is the **first critical step** in the comprehension assessment workflow. It generates a detailed plan of questions BEFORE the passage is written, ensuring that the passage will contain all necessary information to make every question answerable.

### Why QRM First?

**Traditional Problem:**
```
❌ Write passage → Try to write questions → Realize passage doesn't support questions → Rewrite passage
```

**QRM Solution:**
```
✅ Plan questions (QRM) → Plan required content (PIB) → Write passage with required content
```

### The 3-Step Comprehension Workflow

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│     QRM     │  →   │     PIB     │  →   │   PASSAGE   │
│  Question   │      │  Passage    │      │  Written    │
│  Planning   │      │  Content    │      │  Text       │
│             │      │  Requirements│      │             │
└─────────────┘      └─────────────┘      └─────────────┘
   What to ask?      What must be       Write it with
                     in passage?        required content
```

---

## What It Generates

The QRM Generator produces a complete **Question Requirement Matrix** containing:

### 1. Question Specifications (for each question)
- **Question Type**: explicit, implicit, vocabulary, main_idea, etc.
- **Cognitive Demand**: low, medium, high
- **Evidence Location**: beginning, middle, end, throughout
- **Content Requirement**: What passage MUST contain to answer this question
- **Distractor Guidance**: How to create plausible wrong answers

### 2. Aggregated Requirements
- **Required Content Elements**: List of what passage must include
- **Required Vocabulary**: Target words for vocabulary questions
- **Required Structure Elements**: Organizational features needed (e.g., cause-effect, sequence)

### 3. Distribution Analysis
- **Type Distribution**: Count of each question type
- **Cognitive Distribution**: Count by complexity level
- **Evidence Distribution**: Where answers are located in passage

---

## Bank Usage

### Bank 4 (Comprehension Blueprint) ✅

**Used For:**
- Total number of questions by grade
- Question type distribution by grade
- Cognitive demand distribution by grade
- Grade-specific question requirements

**Example from Bank 4:**
```python
Grade 2 Comprehension Blueprint:
- Total Questions: 6
- Question Types:
  * Explicit: 2 questions
  * Implicit: 2 questions
  * Vocabulary: 1 question
  * Main Idea: 1 question
- Cognitive Demands:
  * Low: 2 questions
  * Medium: 3 questions
  * High: 1 question
```

**Bank 4 Enforcement:**
- QRM MUST match exact counts from Bank 4
- QRM validation fails if distributions don't match
- Ensures consistency with research-based assessment standards

---

## Anti-Drift Compliance

### ✅ Bank-Driven
- All question counts from Bank 4
- All distributions from Bank 4
- Validation enforces Bank 4 specifications
- No hardcoded question requirements

### ✅ AI-Assisted but Validated
- AI generates the specific content requirements
- Human-quality planning of what goes in passage
- Strict validation against Bank 4 ensures compliance
- Retry logic if validation fails (can be added)

### ✅ Ensures Answerability
- Forces explicit planning of passage content
- Prevents "write passage then realize questions don't work"
- Each question specifies exactly what passage needs
- PIB generator uses this to build passage requirements

---

## Usage

### Basic Usage

```python
from qrm_generator import create_qrm_generator
from ai_client import create_ai_client

# Create AI client
ai_client = create_ai_client("your_api_key")

# Create QRM generator
qrm_gen = create_qrm_generator(ai_client)

# Generate QRM
qrm = qrm_gen.generate(
    grade="2",
    genre="narrative",  # or "nonfiction"
    band="early",       # or "late"
    topic="school adventure"  # optional guidance
)

# Access specifications
for question in qrm.questions:
    print(f"Q{question.question_number}: {question.question_type.value}")
    print(f"  Content needed: {question.content_requirement}")
```

### Complete Workflow (QRM → PIB → Passage)

```python
# Step 1: Generate QRM (Question plan)
qrm = qrm_generator.generate(
    grade="2",
    genre="narrative",
    band="early",
    topic="friendship"
)

# Step 2: Generate PIB (Content requirements) - NEXT GENERATOR
pib = pib_generator.generate(qrm=qrm)

# Step 3: Generate Passage (With required content) - FINAL GENERATOR
passage = passage_generator.generate(
    qrm=qrm,
    pib=pib,
    grade="2",
    band="early"
)

# Result: Passage that supports all questions
```

---

## Output Structure

### QRMResult Dataclass

```python
@dataclass
class QRMResult:
    # Question specifications (list of QuestionRequirement objects)
    questions: List[QuestionRequirement]
    total_questions: int
    
    # Distribution analysis
    type_distribution: Dict[str, int]
    cognitive_distribution: Dict[str, int]
    evidence_distribution: Dict[str, int]
    
    # Passage requirements derived from questions
    required_content_elements: List[str]
    required_vocabulary: List[str]
    required_structure_elements: List[str]
    
    # Metadata
    grade: str
    genre: str
    band: str
    form_id: str
    generated_at: str
    schema_version: str
    bank_usage: Dict[str, str]
```

### QuestionRequirement Dataclass

```python
@dataclass
class QuestionRequirement:
    question_number: int
    question_type: QuestionType  # Enum
    cognitive_demand: CognitiveDemand  # Enum
    evidence_location: str
    content_requirement: str  # CRITICAL: What passage must contain
    distractor_guidance: str  # How to create wrong answers
```

---

## Example QRM Output

```python
QRM for Grade 2, Narrative, Early Band:

Question 1 (Explicit, Low Complexity):
  Location: beginning
  Requirement: "Passage must state the main character's name in first paragraph"
  Distractors: "Use other character names; use similar-sounding names"

Question 2 (Explicit, Low Complexity):
  Location: middle
  Requirement: "Passage must describe what the character did at school"
  Distractors: "Use activities mentioned but not done by this character"

Question 3 (Implicit, Medium Complexity):
  Location: throughout
  Requirement: "Character's actions must show they are brave (stated actions, reader infers trait)"
  Distractors: "Use other personality traits that could fit but aren't supported"

Question 4 (Implicit, Medium Complexity):
  Location: end
  Requirement: "Passage must show cause-effect: character's choice leads to specific outcome"
  Distractors: "Use other outcomes mentioned; use logical but unsupported outcomes"

Question 5 (Vocabulary, Medium Complexity):
  Location: middle
  Requirement: "Include grade-appropriate word 'determined' with strong context clues"
  Distractors: "Use words with similar sounds; use words from same semantic field"

Question 6 (Main Idea, High Complexity):
  Location: throughout
  Requirement: "Passage must have clear central message about courage supported by details"
  Distractors: "Use details from passage; use overly specific statements; use unsupported generalizations"

Required Content Elements:
  - Character introduction with name
  - School setting
  - Actions demonstrating bravery
  - Choice with clear consequences
  - Target vocabulary word with context clues
  - Central theme about courage/growth

Required Vocabulary: ["determined"]
Required Structure: ["chronological sequence", "cause-effect relationship"]
```

---

## Question Types (from Bank 4)

### Explicit Questions
- Answer stated directly in text
- Low to medium complexity
- "According to the passage, what did..."
- Requires specific fact recall

### Implicit Questions
- Answer requires inference
- Medium to high complexity
- "Based on the passage, why did..."
- Requires connecting information

### Vocabulary Questions
- Word meaning from context
- Medium complexity
- "What does the word ___ mean in this passage?"
- Requires context clue usage

### Main Idea Questions
- Central concept or theme
- High complexity
- "What is this passage mostly about?"
- Requires synthesis of details

### Other Types (Grade-Dependent)
- **Structure**: Text organization questions
- **Author's Purpose**: Why author wrote
- **Compare/Contrast**: Similarities and differences
- **Cause/Effect**: Causal relationships
- **Sequence**: Order of events
- **Picture-Based**: K-1 only, from illustrations

---

## Cognitive Demand Levels

### Low Complexity
- Locate information
- Recall facts
- Direct comprehension
- Example: "What color was the dog?"

### Medium Complexity
- Interpret meaning
- Use context clues
- Make simple inferences
- Example: "How did the character feel?"

### High Complexity
- Analyze relationships
- Synthesize information
- Evaluate author's choices
- Example: "What is the main message?"

---

## Evidence Location Strategy

### Beginning
- Character introductions
- Setting descriptions
- Problem/conflict establishment
- 1-2 questions typically

### Middle
- Actions and events
- Vocabulary in context
- Character development
- 2-3 questions typically

### End
- Resolution/conclusion
- Consequences of choices
- Final outcomes
- 1-2 questions typically

### Throughout
- Main idea/theme
- Character traits (shown through actions)
- Overarching concepts
- 1-2 questions typically

**Why This Matters:** Ensures questions span entire passage and students must read all of it.

---

## Validation Rules

The QRM Generator validates against Bank 4 specifications:

### Total Questions Check
```python
if qrm.total_questions != bank4.total_questions:
    raise ValueError("Question count must match Bank 4")
```

### Type Distribution Check
```python
for question_type, expected_count in bank4.question_types.items():
    if qrm.type_distribution[question_type] != expected_count:
        raise ValueError(f"{question_type} count must be {expected_count}")
```

### Cognitive Distribution Check
```python
for demand_level, expected_count in bank4.cognitive_demands.items():
    if qrm.cognitive_distribution[demand_level] != expected_count:
        raise ValueError(f"{demand_level} count must be {expected_count}")
```

**If validation fails:** Generation is rejected and can be retried

---

## Integration with PIB Generator

The QRM output feeds directly into the PIB (Passage Information Bank) Generator:

```python
# QRM provides the "what questions to ask"
qrm = qrm_generator.generate(...)

# PIB converts to "what content passage needs"
pib = pib_generator.generate(
    qrm=qrm,  # Uses question requirements
    grade=qrm.grade,
    genre=qrm.genre,
    band=qrm.band
)

# PIB output includes:
# - Scene descriptions
# - Character details
# - Plot elements
# - Vocabulary placement
# - All derived from QRM requirements
```

---

## Best Practices

### 1. Provide Topic Guidance
```python
# Vague
qrm = generator.generate(grade="2", genre="narrative", band="early")

# Better
qrm = generator.generate(
    grade="2",
    genre="narrative",
    band="early",
    topic="overcoming challenges at school"  # Helps AI plan coherent questions
)
```

### 2. Review Content Requirements
```python
qrm = generator.generate(...)

# Check that requirements are specific enough
for q in qrm.questions:
    if len(q.content_requirement) < 20:
        print(f"Warning: Q{q.question_number} requirement may be too vague")
```

### 3. Verify Evidence Distribution
```python
# Should have questions from beginning, middle, end
if "beginning" not in qrm.evidence_distribution:
    print("Warning: No questions target passage beginning")
```

---

## Common Issues & Solutions

### Issue: QRM Validation Fails
**Cause:** AI generated wrong distribution  
**Solution:** Retry generation; improve prompt clarity

### Issue: Content Requirements Too Vague
**Cause:** AI didn't provide specific enough guidance  
**Solution:** Add examples to prompt; manual review step

### Issue: Questions Don't Align with Topic
**Cause:** Topic guidance not used effectively  
**Solution:** Provide more specific topic; review QRM before PIB step

---

## Testing

### Unit Test
```python
qrm = generator.generate(grade="2", genre="narrative", band="early")

assert qrm.total_questions == 6
assert qrm.type_distribution["explicit"] == 2
assert qrm.cognitive_distribution["low"] == 2
assert len(qrm.required_content_elements) > 0
```

### Integration Test (with PIB)
```python
qrm = qrm_generator.generate(...)
pib = pib_generator.generate(qrm=qrm)

# Verify PIB contains all QRM requirements
for req in qrm.required_content_elements:
    assert any(req in element for element in pib.content_elements)
```

---

## Future Enhancements

### Potential Additions
- [ ] Question difficulty calibration
- [ ] Evidence overlap detection (multiple questions same evidence)
- [ ] Automatic retry on validation failure
- [ ] QRM quality scoring

### Not Planned (Out of Scope)
- ❌ Manual question editing (QRM is planning only)
- ❌ Answer generation (happens in Question Generator)
- ❌ Passage writing (happens in Passage Generator)

---

## Dependencies

**Required:**
- AI client (OpenAI, Anthropic, or Mock)
- Bank 4 (comprehension_blueprint.py)
- Python 3.9+

**Optional:**
- Template loader (uses inline prompt as fallback)
- Jinja2 template (comp_qrm.j2)

---

## Files

**Source:**
- `qrm_generator.py` (main generator)

**Related:**
- PIB Generator (next step - to be built)
- Comprehension Passage Generator (final step - to be built)
- Question Generator (uses QRM to generate actual questions)

---

**Status:** ✅ Complete and Tested  
**Next Step:** Build PIB Generator (uses QRM output)  
**Phase 2B:** QRM Complete | PIB Next | Passage Final
