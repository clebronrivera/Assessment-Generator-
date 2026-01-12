# Prompt Templates - Index and Usage Guide

## Overview
These Jinja2 templates control AI generation for all assessment components. They enforce anti-drift by pulling all constraints from Foundation Banks.

## Template Files

### 1. `orf_passage.j2` - ORF Passage Generation
**Purpose:** Generate timed oral reading fluency passages
**Uses Banks:** 1 (Lexile), 2 (ORF Word Counts), 5 (Form Requirements)
**Input Variables:**
- `grade` - Grade level (1-8)
- `lexile_min`, `lexile_max`, `lexile_midpoint` - From Bank 1
- `target_word_count`, `min_word_count`, `max_word_count` - From Bank 2
- `structure` - Text structure (from Bank 7)
- `topic_constraint` - Optional topic
- `prohibited_content` - Optional restrictions

**Output:** Plain text narrative passage, 2-4 paragraphs, ±2 words of target

---

### 2. `comp_qrm.j2` - Question Requirement Matrix
**Purpose:** Define questions BEFORE writing passage (step 1 of QRM→PIB→Passage)
**Uses Banks:** 4 (Comprehension Blueprint)
**Input Variables:**
- `grade` - Grade level
- `total_questions` - From Bank 4
- `question_distribution` - Dict from Bank 4
- `word_count_range` - From Bank 3
- `genre` - narrative or nonfiction
- `text_structure` - From Bank 7
- `requires_picture` - Boolean from Bank 4
- `requires_text_features` - Boolean from Bank 4
- `available_structures` - From Bank 7

**Output:** Numbered list of questions with evidence requirements

---

### 3. `comp_pib.j2` - Passage Information Bank
**Purpose:** Convert QRM to concrete content requirements (step 2 of QRM→PIB→Passage)
**Uses Banks:** 1, 3, 4, 7
**Input Variables:**
- `qrm_content` - Output from comp_qrm.j2
- `grade` - Grade level
- `genre` - narrative or nonfiction
- `text_structure` - From Bank 7
- `word_count_average`, `word_count_min`, `word_count_max` - From Bank 3
- `lexile_min`, `lexile_max`, `lexile_midpoint` - From Bank 1
- `requires_text_features` - From Bank 4

**Output:** Structured content guide with required elements and placement

---

### 4. `comp_passage.j2` - Comprehension Passage
**Purpose:** Generate passage from PIB (step 3 of QRM→PIB→Passage)
**Uses Banks:** 1, 3, 4, 7
**Input Variables:**
- `pib_content` - Output from comp_pib.j2
- `grade` - Grade level
- `lexile_min`, `lexile_max`, `lexile_midpoint` - From Bank 1
- `word_count_average`, `word_count_min`, `word_count_max` - From Bank 3
- `genre` - narrative or nonfiction
- `text_structure` - From Bank 7
- `paragraph_count` - Based on grade
- `requires_picture` - From Bank 4
- `requires_text_features` - From Bank 4
- `total_questions` - From Bank 4

**Output:** Complete passage with optional picture description or text features

---

### 5. `questions.j2` - Question Generation
**Purpose:** Generate multiple choice questions with evidence
**Uses Banks:** 4 (Comprehension Blueprint), 6 (Answer Options)
**Input Variables:**
- `passage_text` - Generated passage
- `qrm_content` - Original QRM for alignment
- `grade` - Grade level
- `total_questions` - From Bank 4
- `num_options` - From Bank 6 (2, 3, or 4)
- `question_distribution` - From Bank 4
- `distractor_guidance` - From Bank 6

**Output:** Formatted questions with options, correct answer, evidence locator, rationale

---

### 6. `recall_scoring.j2` - Recall Scoring Guide
**Purpose:** Create sentence-based recall assessment
**Uses Banks:** None directly (uses passage)
**Input Variables:**
- `passage_text` - Generated passage
- `grade` - Grade level

**Output:** Sentence-by-sentence scoring guide with key ideas, keywords, rubric

---

### 7. `picture_description.j2` - K-1 Picture Description
**Purpose:** Generate illustrator-ready picture for K-1 passages
**Uses Banks:** 4 (K-1 requirements)
**Input Variables:**
- `passage_text` - Generated passage
- `grade` - K or 1

**Output:** Single paragraph picture description with style notes

---

### 8. `text_features.j2` - Grades 6+ Text Features
**Purpose:** Add headings and organizational features to nonfiction
**Uses Banks:** 4 (grades 6+ requirements)
**Input Variables:**
- `passage_text` - Generated passage
- `grade` - 6, 7, 8, or 8+
- `word_count_min`, `word_count_max` - From Bank 3

**Output:** Enhanced passage with headings and one organizational feature

---

## Usage Pattern

### For ORF Assessment:
1. Load template: `orf_passage.j2`
2. Get variables from Banks 1, 2, 5
3. Render template
4. Validate output (word count ±2)

### For Comprehension Assessment:
1. Load template: `comp_qrm.j2`
2. Get variables from Bank 4
3. Render QRM → Get output

4. Load template: `comp_pib.j2`
5. Input QRM output + bank variables
6. Render PIB → Get output

7. Load template: `comp_passage.j2`
8. Input PIB output + bank variables
9. Render passage → Get output

10. *If K-1:* Use `picture_description.j2`
11. *If 6+:* Use `text_features.j2`

12. Load template: `questions.j2`
13. Input passage + QRM + bank variables
14. Render questions → Get output

15. Load template: `recall_scoring.j2`
16. Input passage
17. Render recall guide → Get output

---

## Anti-Drift Features

Every template includes:
- ✅ Explicit bank value references
- ✅ Strict constraints (MUST/MUST NOT)
- ✅ Word count enforcement
- ✅ Grade-level specifications
- ✅ Quality standards
- ✅ Output format requirements
- ✅ Examples for clarity
- ✅ Critical reminders

## Variable Naming Convention

All variables come from banks and follow this pattern:
- `grade` - Always from bank lookup
- `lexile_*` - Always from Bank 1
- `word_count_*` - Always from Bank 2 or 3
- `*_count` - Always from Bank 4
- `num_options` - Always from Bank 6
- `structure`, `text_structure` - Always from Bank 7

**NO hardcoded values in templates - all from banks!**

---

## Testing Templates

Test with these sample inputs:

**Grade 2 ORF:**
```python
from jinja2 import Template
from src.banks import get_lexile_range, get_orf_target

grade = "2"
band = "early"
lexile = get_lexile_range(grade, band)
orf = get_orf_target(grade)

variables = {
    'grade': grade,
    'lexile_min': lexile.lexile_min,
    'lexile_max': lexile.lexile_max,
    'lexile_midpoint': get_midpoint_lexile(grade, band),
    'target_word_count': orf.target_word_count,
    'min_word_count': orf.min_word_count,
    'max_word_count': orf.max_word_count,
    'structure': 'chronological'
}

with open('templates/prompts/orf_passage.j2') as f:
    template = Template(f.read())
    
prompt = template.render(**variables)
print(prompt)
```

---

## Next Steps

With templates complete:
1. Build generator classes that use these templates
2. Implement validation logic
3. Create PDF output templates
4. Build API endpoints

---

**Version:** 1.0
**Created:** 2026-01-12
**Templates:** 8/8 complete
