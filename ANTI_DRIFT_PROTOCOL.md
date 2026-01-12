# Anti-Drift Protocol for Reading Assessment Generator

**Version:** 1.0  
**Effective Date:** 2026-01-12  
**Applies To:** All development work on this project

---

## Purpose

This protocol prevents scope creep, data invention, and architectural drift by enforcing strict task grounding and bank-driven development.

---

## Core Principles

1. **Task Grounding:** All work must reference an existing task in TASK_LIST.md
2. **Bank-Driven:** All data must come from Banks 1-7, never invented
3. **Documentation First:** Update TASK_LIST.md and CHANGELOG.md for every change
4. **Validation Always:** Check anti-drift criteria before and after work
5. **Transparency:** Document all decisions, alternatives, and rationale

---

## Mandatory Pre-Work Validation

### BEFORE starting ANY task, complete this checklist:

#### 1. Task Grounding
- [ ] Task exists in TASK_LIST.md
- [ ] Task is not marked [✅] already
- [ ] All prerequisite tasks marked [✅]
- [ ] Task scope is clear and specific
- [ ] User has confirmed if scope is ambiguous

#### 2. Data Grounding
- [ ] Identified which banks (1-7) will be used
- [ ] Confirmed no new data values being created
- [ ] If new data needed, determined if it belongs in existing bank or requires new bank
- [ ] Verified bank functions exist for needed data

#### 3. Pattern Grounding
- [ ] Reviewed similar code from Phase 1
- [ ] Will use same patterns (dataclasses, Enums, validation)
- [ ] Will follow same file structure conventions
- [ ] Will use same naming conventions

#### 4. Scope Grounding
- [ ] Task directly solves stated requirement
- [ ] Not building features not requested
- [ ] Not over-engineering the solution
- [ ] Identified minimum viable implementation

#### 5. Integration Grounding
- [ ] Identified files that will be created
- [ ] Identified files that will be modified
- [ ] Checked for breaking changes to existing code
- [ ] Verified no new dependencies unless necessary

### If ANY checkbox is unchecked or uncertain:
→ **STOP**  
→ Document the concern  
→ Ask user for clarification  
→ **DO NOT proceed until confirmed**

---

## Mandatory Post-Work Documentation

### AFTER completing ANY task, update these files:

### 1. TASK_LIST.md Updates

**Mark task complete:**
```markdown
- [✅] Task description (Completed: YYYY-MM-DD HH:MM)
```

**Add newly identified tasks:**
```markdown
- [NEW] New task description
  **Why Needed:** Explanation
  **Relates To:** Existing task
  **Phase:** Which phase
  **Priority:** High/Medium/Low
  **Depends On:** Prerequisites
  **Identified:** Date and context
```

**Update blockers:**
```markdown
- [⚠️] Task description
  **Status:** BLOCKED - Reason
  **Resolution:** Options for unblocking
```

### 2. CHANGELOG.md Entry

**Required sections for EVERY entry:**

```markdown
## [YYYY-MM-DD HH:MM] - Task: [Task Name from TASK_LIST.md]

### Task Reference
**From:** Phase [X] - [Phase Name]
**Task:** [Exact task description]
**Status:** ✅ Complete / ⚠️ Partial / 🔄 In Progress
**Related Tasks:** [Dependencies]

### Changes Made
**Files Created:**
- `path/to/file.py` - Purpose - Bank usage

**Files Modified:**
- `path/to/file.py` - Changes - Impact

**Files Deleted:**
- `path/to/file.py` - Reason

### Key Decisions
1. **Decision:** What was decided
   **Rationale:** Why
   **Impact:** Effect on current and future tasks
   **Bank Usage:** Which banks used and how
   **Alternative Considered:** If any
   **Anti-Drift Check:** ✅ or ❌ with explanation

### Anti-Drift Validation
- ✅/❌ Task exists in TASK_LIST.md
- ✅/❌ All data pulled from existing banks
- ✅/❌ No hardcoded values introduced
- ✅/❌ Follows established patterns
- ✅/❌ Dependencies verified complete
- ⚠️ [Any concerns or deviations - explain why necessary]

### Bank Usage Report
**Banks Referenced:**
- Bank X: How used

**Bank Functions Called:**
- `function_name()` - Why

**New Bank Needs Identified:**
- [None] OR [Description]

### Code Changes Summary
```language
// Key code snippets
// Show bank usage
// Show validation logic
```

### Testing & Validation
- What was tested
- Results
- Issues found and resolved

### New Tasks Identified
1. Task - Why - Phase - Priority

### Next Steps
- Immediate next task
- Prerequisites
- Blockers

### Technical Debt / Future Considerations
- Shortcuts taken
- Refactoring needed
- Performance/security notes

### Notes & Warnings
- Important notes
- Gotchas
- Integration points
```

---

## Bank Usage Rules

### The Seven Banks (Source of Truth)

1. **Bank 1:** Lexile Readability Grade Band Bank
   - File: `src/banks/lexile_ranges.py`
   - Use: `get_lexile_range(grade, band)`

2. **Bank 2:** ORF Word Count Targets
   - File: `src/banks/orf_word_counts.py`
   - Use: `get_orf_target(grade)`

3. **Bank 3:** Comprehension Passage Word Counts
   - File: `src/banks/comp_word_counts.py`
   - Use: `get_comp_word_count(grade)`

4. **Bank 4:** Comprehension Blueprint
   - File: `src/banks/comprehension_blueprint.py`
   - Use: `get_blueprint(grade)`

5. **Bank 5:** Form Production Requirements
   - File: `src/banks/form_requirements.py`
   - Use: `get_form_requirements(grade, type)`

6. **Bank 6:** Answer Option Standards
   - File: `src/banks/answer_options.py`
   - Use: `get_num_options(grade)`

7. **Bank 7:** Text Structure Examples
   - File: `src/banks/text_structures.py`
   - Use: `get_structure_names(genre)`

### Absolute Rules

✅ **ALWAYS:**
- Pull data from banks using provided functions
- Log which banks and functions were used
- Validate outputs against bank constraints
- Use bank data in prompt templates

❌ **NEVER:**
- Hardcode Lexile ranges, word counts, or question counts
- Invent new grade levels or bands
- Create data that should be in a bank
- Modify bank data at runtime
- Access bank data directly (use functions)

### When New Data is Needed

If you discover data that should exist but doesn't:

1. **STOP** - Don't invent it
2. **Document** - Describe what's needed and why
3. **Propose** - Should it be in existing bank or new bank?
4. **Ask** - Get user approval before adding
5. **Update** - Add to bank, not to generator code
6. **Test** - Validate new bank data

---

## File Organization Rules

### Directory Structure (Enforced)

```
/Users/lebron/Desktop/Bank Creator/
├── TASK_LIST.md                    ← Update for every task
├── CHANGELOG.md                    ← Update for every task
├── ANTI_DRIFT_PROTOCOL.md          ← This file
├── src/
│   ├── banks/                      ← Source of truth (immutable)
│   ├── generators/                 ← Phase 2 work
│   ├── validation/                 ← Phase 4 work
│   ├── packaging/                  ← Phase 5 work
│   ├── api/                        ← Phase 7 work
│   └── utils/                      ← Shared utilities
├── templates/
│   ├── prompts/                    ← Jinja2 templates
│   └── pdf/                        ← PDF templates
├── tests/
│   ├── unit/
│   ├── integration/
│   └── validation/
└── data/                           ← Generated forms storage
```

### Naming Conventions

**Python Files:**
- `snake_case.py`
- Descriptive names: `orf_generator.py` not `gen.py`

**Classes:**
- `PascalCase`
- Descriptive: `ORFPassageGenerator` not `OPG`

**Functions:**
- `snake_case()`
- Verb-noun: `get_lexile_range()` not `lexile()`

**Constants:**
- `UPPER_SNAKE_CASE`
- Descriptive: `MAX_RETRIES` not `MR`

**Templates:**
- `snake_case.j2`
- Purpose-clear: `orf_passage.j2` not `template1.j2`

---

## Code Quality Standards

### Required for All Code

1. **Type Hints:**
   ```python
   def get_lexile_range(grade: str, band: LexileBand) -> LexileRange:
   ```

2. **Docstrings:**
   ```python
   """
   Brief description.
   
   Args:
       grade: Grade level (K, 1-8, 8+)
       band: Early or Late
   
   Returns:
       LexileRange with min, max, midpoint
   
   Raises:
       ValueError: If grade/band invalid
   
   Bank Usage:
       Uses Bank 1 (Lexile Ranges)
   """
   ```

3. **Validation:**
   ```python
   if grade not in VALID_GRADES:
       raise ValueError(f"Invalid grade: {grade}")
   ```

4. **Bank Logging:**
   ```python
   logger.info(f"Using Bank 1: {grade} {band} → {result}")
   ```

5. **Error Handling:**
   ```python
   try:
       result = generator.generate()
   except ValidationError as e:
       logger.error(f"Validation failed: {e}")
       # Handle gracefully
   ```

---

## Workflow Example

### User Request: "Build the ORF generator"

### Step 1: Pre-Work Validation

**AI Response:**
```
Checking TASK_LIST.md...

Task Found:
- Phase 2A: Build ORF Passage Generator (Grades 1-8)
- Status: [ ] Not started
- Prerequisites: Banks 1, 2, 5 ✅ (Phase 1 complete)

I will:
1. Create src/generators/orf_generator.py
2. Create templates/prompts/orf_passage.j2
3. Use Bank 1 (Lexile ranges)
4. Use Bank 2 (ORF word counts)
5. Use Bank 5 (Form requirements)

Anti-Drift Check:
✅ Task exists in TASK_LIST.md
✅ Will use existing banks only
✅ No new data being created
✅ Follows Phase 1 patterns (dataclasses, validation)

Proceeding? [WAIT FOR CONFIRMATION]
```

### Step 2: Implementation

- Write code using bank functions
- Create Jinja2 template with bank variables
- Add validation using bank constraints
- Log bank usage

### Step 3: Post-Work Documentation

**Update TASK_LIST.md:**
```markdown
- [✅] Build ORF Passage Generator (Completed: 2026-01-12 14:30)
```

**Add CHANGELOG.md entry:**
```markdown
## [2026-01-12 14:30] - Task: Build ORF Passage Generator

### Task Reference
**From:** Phase 2A - ORF Generator
**Task:** Build ORF Passage Generator (Grades 1-8)
**Status:** ✅ Complete

### Changes Made
**Files Created:**
- `src/generators/orf_generator.py` - Generates ORF passages using Banks 1, 2, 5
- `templates/prompts/orf_passage.j2` - Jinja2 template with bank variables

[... full changelog entry ...]
```

### Step 4: Report Completion

**AI Response:**
```
✅ ORF Passage Generator Complete

Created:
- src/generators/orf_generator.py (250 lines)
- templates/prompts/orf_passage.j2 (50 lines)

Bank Usage:
- Bank 1: Lexile targeting
- Bank 2: Word count validation (±2 words)
- Bank 5: Form ID generation

Tests: 15/15 passing

Updated:
- TASK_LIST.md (marked complete)
- CHANGELOG.md (full entry added)

Next Task: Build ORF Assessor Materials Generator
```

---

## Red Flags (Stop Immediately If You See These)

🚨 **Hardcoded Values:**
```python
# ❌ WRONG
if grade == "3":
    lexile_min = 480
    lexile_max = 645

# ✅ CORRECT
lexile_range = get_lexile_range("3", LexileBand.EARLY)
lexile_min = lexile_range.lexile_min
```

🚨 **Invented Data:**
```python
# ❌ WRONG
question_types = ["recall", "inference", "analysis"]  # Not from bank

# ✅ CORRECT
blueprint = get_blueprint("3")
question_types = blueprint.question_distribution.keys()
```

🚨 **Undocumented Tasks:**
```python
# ❌ WRONG
# Just start coding a new feature

# ✅ CORRECT
# 1. Add task to TASK_LIST.md
# 2. Get user approval
# 3. Then implement
```

🚨 **Missing Validation:**
```python
# ❌ WRONG
def generate(grade):
    # No validation
    return passage

# ✅ CORRECT
def generate(grade: str) -> ORFPassage:
    if grade not in VALID_GRADES:
        raise ValueError(f"Invalid grade: {grade}")
    # ... generate ...
    if not validator.validate(passage):
        raise ValidationError("Passage failed validation")
    return passage
```

---

## Enforcement

### Developer Responsibilities

- Read this protocol before starting work
- Follow checklist for every task
- Update documentation for every change
- Ask when uncertain

### Code Review Checklist

- [ ] Task exists in TASK_LIST.md
- [ ] TASK_LIST.md updated (marked complete, new tasks added)
- [ ] CHANGELOG.md entry complete
- [ ] All data from banks (no hardcoded values)
- [ ] Follows established patterns
- [ ] Tests included
- [ ] Documentation updated

### Violations

If anti-drift protocol is violated:
1. Identify the violation
2. Document what went wrong
3. Revert problematic changes
4. Re-implement correctly
5. Update protocol if needed

---

## Summary

**Three Golden Rules:**

1. **Check TASK_LIST.md before starting**
2. **Use banks, never invent data**
3. **Update both files after completing**

**Remember:**
- Task grounding prevents scope creep
- Bank grounding prevents data drift
- Documentation ensures maintainability
- Validation catches errors early

---

**This protocol is mandatory for all development work.**  
**Violations compromise the integrity of the entire system.**
