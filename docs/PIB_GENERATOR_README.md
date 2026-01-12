# PIB (Passage Information Bank) Generator

**Purpose:** Convert QRM into detailed passage content blueprint  
**Created:** 2026-01-12  
**Schema Version:** 2026.1  
**Phase:** 2B - Comprehension Generator (Step 2 of 3)

---

## Overview

The PIB Generator is the **critical bridge** between question planning (QRM) and passage writing. It converts abstract question requirements into concrete scenes, characters, and content specifications.

### The 3-Step Workflow

```
Step 1: QRM ✅
  ↓ "What questions to ask?"
  ↓ Output: Question specifications
  
Step 2: PIB ✅ (THIS GENERATOR)
  ↓ "What content passage needs?"
  ↓ Output: Scene-by-scene blueprint
  
Step 3: Passage (Next)
  ↓ "Write the actual text"
  ↓ Output: Complete passage
```

### Why PIB is Essential

**Without PIB:**
QRM says "Show character is kind" → Passage writer guesses how → Questions may not work

**With PIB:**
QRM says "Show character is kind" → PIB says "Scene 2: Character invites lonely student. Scene 3: Character shares supplies. Scene 4: Character helps someone who fell" → Passage writer knows exactly what to write → Questions work perfectly

---

## What It Generates

The PIB Generator produces a complete **Passage Information Bank** containing:

### 1. Scene Structure (4-8 scenes typically)
For each scene:
- **Scene Number**: Sequence position
- **Scene Type**: opening, action, dialogue, description, conclusion
- **Location in Passage**: beginning/middle/end
- **Purpose**: What this scene accomplishes
- **Content Description**: What happens
- **Required Details**: Specific facts/elements to include
- **Supports Questions**: Which questions this scene answers
- **Vocabulary Placement**: Target words to use here

### 2. Character Specifications (Narrative)
For each character:
- **Name**: Character's name
- **Role**: main/supporting/minor
- **Key Traits**: Personality characteristics
- **Actions to Show**: Specific behaviors that demonstrate traits
- **Supports Questions**: Which questions this character helps answer

### 3. Content Organization
- **Opening Hook**: How to start the passage
- **Central Conflict/Topic**: Main focus
- **Resolution/Conclusion**: How to end
- **Text Structure**: From Bank 7 (chronological, cause-effect, etc.)
- **Organizational Features**: Headings, bullets (nonfiction only)

### 4. Vocabulary Integration
- **Vocabulary Targets**: Words to include (from QRM)
- **Vocabulary Contexts**: Detailed description of how to use each word

### 5. Question Coverage Map
- Maps each question number to scene numbers that support it
- Ensures every question is covered

### 6. Passage Constraints (from Banks)
- **Target Lexile**: From Bank 1
- **Target Word Count**: From Bank 3
- **Text Structure**: From Bank 7

---

## Bank Usage

### Bank 1 (Lexile Ranges) ✅
**Used For:**
- Target Lexile range for passage
- Ensures passage difficulty matches grade/band

**Example:**
```python
Grade 2, Early Band → 300-400L
```

### Bank 3 (Comp Word Counts) ✅
**Used For:**
- Target word count for passage
- Helps PIB determine how many scenes are feasible

**Example:**
```python
Grade 2 → Target: 200 words (±20 acceptable)
```

### Bank 7 (Text Structures) ✅
**Used For:**
- Available text structures by genre
- Guides how scenes are organized

**Example:**
```python
Narrative → chronological, flashback, problem-solution
Nonfiction → description, compare-contrast, cause-effect, sequence
```

---

## Anti-Drift Compliance

### ✅ QRM-Driven
- All content requirements come from QRM
- Every question must be covered by scenes
- Vocabulary placement matches QRM specifications
- No content invented beyond QRM requirements

### ✅ Bank-Driven Constraints
- Lexile from Bank 1
- Word count from Bank 3
- Structure from Bank 7
- No hardcoded targets

### ✅ Validation
- Checks all questions covered
- Checks vocabulary addressed
- Warns if scene count seems off
- Links back to QRM form ID

---

## Usage

### Basic Usage

```python
from pib_generator import create_pib_generator
from qrm_generator import create_qrm_generator
from ai_client import create_ai_client

# Create AI client
ai_client = create_ai_client("your_api_key")

# Step 1: Generate QRM
qrm_gen = create_qrm_generator(ai_client)
qrm = qrm_gen.generate(
    grade="2",
    genre="narrative",
    band="early",
    topic="friendship"
)

# Step 2: Generate PIB from QRM
pib_gen = create_pib_generator(ai_client)
pib = pib_gen.generate(qrm_result=qrm)

# Access PIB components
for scene in pib.scenes:
    print(f"Scene {scene.scene_number}: {scene.content_description}")

for char in pib.characters:
    print(f"{char.name}: {char.key_traits}")
```

### Complete Workflow (QRM → PIB → Passage)

```python
# Step 1: QRM
qrm = qrm_generator.generate(grade="2", genre="narrative", band="early")
# Output: 6 questions with requirements

# Step 2: PIB (using QRM)
pib = pib_generator.generate(qrm_result=qrm)
# Output: 5 scenes, 2 characters, complete blueprint

# Step 3: Passage (using PIB + QRM)
passage = passage_generator.generate(qrm=qrm, pib=pib)
# Output: 200-word passage that supports all 6 questions
```

---

## Output Structure

### PIBResult Dataclass

```python
@dataclass
class PIBResult:
    # Scene structure
    scenes: List[SceneElement]
    total_scenes: int
    
    # Character specifications (if narrative)
    characters: List[CharacterSpec]
    
    # Content organization
    opening_hook: str
    central_conflict_or_topic: str
    resolution_or_conclusion: str
    
    # Vocabulary integration
    vocabulary_targets: List[str]
    vocabulary_contexts: Dict[str, str]
    
    # Structure requirements
    text_structure: str
    organizational_features: List[str]
    
    # Question alignment
    question_coverage_map: Dict[int, List[int]]
    
    # Passage constraints from banks
    target_lexile: str
    target_word_count: int
    actual_grade: str
    genre: str
    band: str
    
    # Metadata
    form_id: str
    qrm_form_id: str  # Links back to QRM
    generated_at: str
    schema_version: str
    bank_usage: Dict[str, str]
```

### SceneElement Dataclass

```python
@dataclass
class SceneElement:
    scene_number: int
    scene_type: SceneType  # Enum
    location_in_passage: str
    purpose: str
    content_description: str
    required_details: List[str]
    supports_questions: List[int]
    vocabulary_placement: List[str]
```

### CharacterSpec Dataclass

```python
@dataclass
class CharacterSpec:
    name: str
    role: str  # main/supporting/minor
    key_traits: List[str]
    actions_to_show: List[str]
    supports_questions: List[int]
```

---

## Example PIB Output

### Grade 2 Narrative Example

**QRM Input:**
- 6 questions (2 explicit, 2 implicit, 1 vocabulary, 1 main idea)
- Required: Show character kindness, use word "hesitant"

**PIB Output:**

```
SCENES (5 total):

Scene 1 - OPENING (beginning)
  Purpose: Introduce Maya and school setting
  Content: Maya arrives for first day of second grade
  Required Details: 
    - State Maya's name
    - Mention second grade
    - Describe school
  Supports Questions: [1]

Scene 2 - ACTION (middle)
  Purpose: Show Maya noticing lonely student
  Content: Maya sees new student standing alone, looking hesitant
  Required Details:
    - New student described
    - Word "hesitant" used with context
  Supports Questions: [3, 5]
  Vocabulary: hesitant

Scene 3 - ACTION (middle)
  Purpose: Show Maya's kindness at recess
  Content: Maya organizes tag game and invites new student
  Required Details:
    - Tag game organized
    - Maya invites student
    - Student joins
  Supports Questions: [2, 3]

Scene 4 - ACTION (middle)
  Purpose: Continue showing kindness
  Content: Maya shares pencils with student who forgot
  Required Details:
    - Student forgot supplies
    - Maya shares
    - Student grateful
  Supports Questions: [3]

Scene 5 - CONCLUSION (end)
  Purpose: Show positive outcome
  Content: End of day, Maya has new friends and feels happy
  Required Details:
    - Friendships formed
    - Maya happy
    - Cause-effect clear
  Supports Questions: [4, 6]

CHARACTERS (2 total):

Maya (main)
  Traits: kind, inclusive, friendly
  Actions to Show:
    - Invites lonely student
    - Shares supplies
    - Organizes inclusive game
  Supports Questions: [1, 2, 3, 4, 6]

Jordan (supporting)
  Traits: new, shy
  Actions to Show:
    - Stands alone hesitantly
    - Joins game
    - Becomes friend
  Supports Questions: [3, 4, 5]

STRUCTURE:
  Opening Hook: "Maya stood at school entrance, excited for second grade"
  Central Topic: Maya makes new students feel welcome
  Resolution: Maya's kindness leads to new friendships
  Text Structure: chronological
  Target Lexile: 300-400L
  Target Words: 200

VOCABULARY CONTEXTS:
  hesitant: "Jordan looked hesitant to join, standing alone with uncertain expression"

QUESTION COVERAGE:
  Q1 → Scene 1
  Q2 → Scene 3
  Q3 → Scenes 2, 3, 4 (shown through multiple actions)
  Q4 → Scene 5
  Q5 → Scene 2
  Q6 → Scene 5
```

---

## Scene Types

### OPENING
- Introduces setting, characters, situation
- Typically 1 scene at beginning
- Sets tone and context

### ACTION
- Events, activities, behaviors
- Typically 2-4 scenes in middle
- Shows character traits through actions

### DIALOGUE
- Character conversations
- Reveals personality, advances plot
- Can be mixed into other scenes

### DESCRIPTION
- Detailed depictions
- More common in nonfiction
- Provides necessary information

### TRANSITION
- Moves between settings/times
- Brief connecting scenes
- "Later that day..." "At recess..."

### CONCLUSION
- Wraps up story/topic
- Shows resolution/outcome
- Typically 1 scene at end

---

## Integration with QRM

The PIB directly extends every QRM requirement:

### QRM Requirement → PIB Scene

**QRM Q3:**
"Character's actions must show kindness without stating 'kind'"

**PIB Conversion:**
```
Scene 2: Maya invites lonely student
  - Detail: Student standing alone
  - Detail: Maya approaches
  - Detail: Maya asks student to join

Scene 3: Maya shares supplies
  - Detail: Student forgot pencils
  - Detail: Maya gives extra pencil
  - Detail: Student says thank you

Scene 4: Maya helps fallen student
  - Detail: Student trips
  - Detail: Maya stops to help
  - Detail: Maya stays until student feels better
```

### QRM Vocabulary → PIB Context

**QRM:**
"Include word 'hesitant' with context clues"

**PIB:**
```
Scene 2, Vocabulary Placement: ["hesitant"]
Context: "Jordan looked hesitant to join the game, 
standing alone at the edge of the playground with 
an uncertain expression, glancing at the other 
students but not moving closer"
```

---

## Validation Rules

The PIB Generator validates:

### Question Coverage
```python
all_questions = {1, 2, 3, 4, 5, 6}
covered_questions = set(pib.question_coverage_map.keys())

if covered_questions != all_questions:
    print(f"Warning: Missing coverage for {all_questions - covered_questions}")
```

### Vocabulary Addressed
```python
for vocab_word in qrm.required_vocabulary:
    if vocab_word not in pib.vocabulary_contexts:
        print(f"Warning: No context provided for '{vocab_word}'")
```

### Scene Count
```python
if pib.total_scenes < 3:
    print("Warning: Too few scenes for question coverage")
elif pib.total_scenes > 8:
    print("Warning: May exceed word count with this many scenes")
```

---

## Narrative vs. Nonfiction Differences

### Narrative PIB

**Focus:**
- Character-driven scenes
- Chronological or problem-solution structure
- Actions that demonstrate traits
- Dialogue and description

**Example Scenes:**
1. Opening: Character introduced in setting
2. Action: Character faces challenge
3. Action: Character attempts solution
4. Climax: Key decision or event
5. Conclusion: Resolution and reflection

### Nonfiction PIB

**Focus:**
- Topic-driven sections
- Logical organization (description, compare-contrast, cause-effect)
- Facts, examples, explanations
- Text features (headings, bullets, diagrams)

**Example Sections:**
1. Introduction: Topic overview with hook
2. Description: Main characteristics or aspects
3. Examples: Specific instances or cases
4. Relationships: Causes, effects, comparisons
5. Conclusion: Summary and implications

---

## Best Practices

### 1. Ensure Even Question Distribution
```python
# Check that no scene supports too many questions
for scene in pib.scenes:
    if len(scene.supports_questions) > 3:
        print(f"Warning: Scene {scene.scene_number} supports {len(scene.supports_questions)} questions")
```

### 2. Verify Vocabulary Placement Natural
```python
# Vocabulary should appear in scenes with relevant context
for vocab_word in pib.vocabulary_targets:
    scenes_with_vocab = [s for s in pib.scenes if vocab_word in s.vocabulary_placement]
    if not scenes_with_vocab:
        print(f"Warning: '{vocab_word}' not placed in any scene")
```

### 3. Check Scene Flow
```python
# Scenes should have logical progression
locations = [s.location_in_passage for s in pib.scenes]
if locations != sorted(locations, key=lambda x: ['beginning', 'middle', 'end'].index(x)):
    print("Warning: Scene order may not flow logically")
```

---

## Common Issues & Solutions

### Issue: Not All Questions Covered
**Cause:** PIB didn't create scenes for all question requirements  
**Solution:** Review QRM, ensure each requirement gets a scene

### Issue: Too Many Scenes
**Cause:** Over-planning, will exceed word count  
**Solution:** Combine related scenes, aim for 4-6 scenes

### Issue: Vocabulary Feels Forced
**Cause:** PIB didn't create natural context for vocab word  
**Solution:** Improve vocabulary context description in PIB

### Issue: Character Actions Don't Match Traits
**Cause:** Character spec disconnected from scenes  
**Solution:** Verify character actions appear in scene descriptions

---

## Testing

### Unit Test
```python
pib = generator.generate(qrm_result=qrm)

assert pib.total_scenes >= 3
assert pib.total_scenes <= 8
assert len(pib.characters) >= 1  # For narrative
assert len(pib.question_coverage_map) == qrm.total_questions
assert pib.qrm_form_id == qrm.form_id
```

### Integration Test (with Passage Generator)
```python
qrm = qrm_generator.generate(...)
pib = pib_generator.generate(qrm_result=qrm)
passage = passage_generator.generate(qrm=qrm, pib=pib)

# Verify passage includes PIB elements
for scene in pib.scenes:
    assert any(detail in passage.text for detail in scene.required_details)

for vocab_word in pib.vocabulary_targets:
    assert vocab_word in passage.text
```

---

## Future Enhancements

### Potential Additions
- [ ] Scene length estimation (words per scene)
- [ ] Dialogue vs. narrative balance calculation
- [ ] Character interaction matrix
- [ ] Scene dependency analysis

### Not Planned (Out of Scope)
- ❌ Actual passage writing (that's Passage Generator's job)
- ❌ Question generation (that's Question Generator's job)
- ❌ Manual scene editing (PIB is AI-generated blueprint)

---

## Dependencies

**Required:**
- AI client (OpenAI, Anthropic, or Mock)
- QRM Generator (provides input)
- Bank 1 (lexile_ranges.py)
- Bank 3 (comp_word_counts.py)
- Bank 7 (text_structures.py)
- Python 3.9+

**Optional:**
- Template loader (uses inline prompt as fallback)
- Jinja2 template (comp_pib.j2)

---

## Files

**Source:**
- `pib_generator.py` (main generator)

**Related:**
- QRM Generator (provides input)
- Comprehension Passage Generator (uses PIB output - to be built)

---

**Status:** ✅ Complete and Tested  
**Next Step:** Build Comprehension Passage Generator (uses QRM + PIB)  
**Phase 2B:** QRM ✅ | PIB ✅ | Passage Next
