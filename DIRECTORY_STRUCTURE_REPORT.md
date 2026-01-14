# DIRECTORY STRUCTURE REPORT
**Reading Assessment Generator Project**  
**Generated:** 2026-01-12 14:14:23 EST  
**Mode:** DIAGNOSTIC READ-ONLY - NO CHANGES MADE

---

## EXECUTIVE SUMMARY

- **Total Files:** 123 items found
- **Python Files:** 43 (.py files)
- **Documentation Files:** 20 (.md files)
- **Template Files:** 17 (.j2 files)
- **Data Files:** 2 (.json files)
- **Configuration Files:** 2 (.txt, .env.example)
- **Total Directories:** ~20+ directories

---

## 1. ROOT DIRECTORY STRUCTURE

```
/Users/lebron/Desktop/Bank Creator/
├── .DS_Store (20.0 KB)
├── .env.example (0.2 KB)
├── .git/ (version control)
├── .gitignore (0.6 KB)
├── ADDITIONAL_FIXES_NEEDED.md (8.5 KB)
├── ANTI_DRIFT_PROTOCOL.md (12.4 KB)
├── CHANGELOG.md (60.3 KB) ⭐ LARGEST FILE
├── INTEGRATION_FIXES.md (22.6 KB)
├── LICENSE (1.1 KB)
├── PIB_FIX.md (9.3 KB)
├── README.md (5.5 KB)
├── TASK_LIST.md (10.3 KB)
├── audit_results.json (0.9 KB)
├── audit_workflow.py (14.4 KB)
├── requirements.txt (0.3 KB)
├── test_package_builder.py (20.8 KB)
├── complete_package/ (empty directory)
├── data/
├── docs/
├── orf_generator/
├── src/
├── templates/
├── templates-2/
└── tests/
```

---

## 2. SOURCE CODE STRUCTURE (`src/`)

### 2.1 Overview
```
src/
├── .DS_Store (6.0 KB)
├── api/ (empty)
├── banks/
├── generators/
├── packaging/
├── utils/
└── validation/ (empty)
```

### 2.2 Banks Module (`src/banks/`)
**Purpose:** Content bank definitions and specifications

```
src/banks/
├── .DS_Store (6.0 KB)
├── __init__.py (6.9 KB)
├── __pycache__/ (8 cached files)
├── answer_options.py (5.3 KB)
├── comp_word_counts.py (8.0 KB)
├── comprehension_blueprint.py (15.4 KB)
├── form_requirements.py (14.8 KB)
├── lexile_ranges.py (7.6 KB)
├── orf_word_counts.py (6.3 KB)
└── text_structures.py (11.4 KB)
```

**Files:** 9 Python files (7 modules + 1 __init__ + pycache)

### 2.3 Generators Module (`src/generators/`)
**Purpose:** Core content generation engines

```
src/generators/
├── .DS_Store (6.0 KB)
├── __init__.py (2.0 KB)
├── __pycache__/ (7 cached files)
├── base_generator.py (3.9 KB)
├── comprehension_passage_generator.py (21.6 KB)
├── orf_assessor_materials_generator.py (21.3 KB)
├── orf_generator.py (7.9 KB)
├── pib_generator.py (25.9 KB)
├── qrm_generator.py (18.5 KB)
├── question_generator.py (28.4 KB) ⭐ LARGEST GENERATOR
└── recall_scoring_generator.py (24.4 KB)
```

**Files:** 10 Python files (8 generators + base + __init__)

### 2.4 Packaging Module (`src/packaging/`)
**Purpose:** Assessment package assembly

```
src/packaging/
├── .DS_Store (6.0 KB)
├── __init__.py (0.4 KB)
├── __pycache__/
└── assessment_package_builder.py (16.3 KB)
```

**Files:** 3 Python files

### 2.5 Utils Module (`src/utils/`)
**Purpose:** Shared utilities and helpers

```
src/utils/
├── __init__.py (0.3 KB)
├── __pycache__/ (3 cached files)
├── ai_client.py (6.4 KB)
└── template_loader.py (1.8 KB)
```

**Files:** 4 Python files

---

## 3. ORF GENERATOR STRUCTURE (`orf_generator/`)

### 3.1 Overview
```
orf_generator/
├── .DS_Store (6.0 KB)
├── ORF_GENERATOR_README.md (5.2 KB)
├── example_orf_generator.py (4.9 KB)
├── src/
└── templates/
```

### 3.2 ORF Source (`orf_generator/src/`)
```
orf_generator/src/
├── .DS_Store (6.0 KB)
├── banks/
├── generators/
└── utils/
```

#### Banks Submodule
```
orf_generator/src/banks/
├── __init__.py (6.9 KB)
├── answer_options.py (5.3 KB)
├── comp_word_counts.py (8.0 KB)
├── comprehension_blueprint.py (14.1 KB)
├── form_requirements.py (14.8 KB)
├── lexile_ranges.py (7.4 KB)
├── orf_word_counts.py (6.3 KB)
└── text_structures.py (11.4 KB)
```

**Files:** 8 Python files

#### Generators Submodule
```
orf_generator/src/generators/
├── __init__.py (0.2 KB)
├── base_generator.py (3.9 KB)
└── orf_generator.py (7.9 KB)
```

**Files:** 3 Python files

#### Utils Submodule
```
orf_generator/src/utils/
├── __init__.py (0.2 KB)
└── ai_client.py (6.4 KB)
```

**Files:** 2 Python files

### 3.3 ORF Templates
```
orf_generator/templates/prompts/
└── orf_passage.j2 (3.3 KB)
```

---

## 4. TEMPLATES STRUCTURE

### 4.1 Primary Templates (`templates/`)
```
templates/
├── .DS_Store (6.0 KB)
├── pdf/ (subdirectory)
└── prompts/
```

#### Prompt Templates
```
templates/prompts/
├── README.md (6.5 KB)
├── comp_passage.j2 (5.3 KB)
├── comp_pib.j2 (3.3 KB)
├── comp_qrm.j2 (3.7 KB)
├── orf_passage.j2 (3.3 KB)
├── picture_description.j2 (4.0 KB)
├── questions.j2 (4.8 KB)
├── recall_scoring.j2 (4.4 KB)
└── text_features.j2 (4.7 KB)
```

**Files:** 9 files (8 templates + 1 README)

### 4.2 Secondary Templates (`templates-2/`)
```
templates-2/
├── .DS_Store (8.0 KB)
└── prompts/
```

#### Prompt Templates (Duplicate Set)
```
templates-2/prompts/
├── README.md (6.5 KB)
├── comp_passage.j2 (5.3 KB)
├── comp_pib.j2 (3.3 KB)
├── comp_qrm.j2 (3.7 KB)
├── orf_passage.j2 (3.3 KB)
├── picture_description.j2 (4.0 KB)
├── questions.j2 (4.8 KB)
├── recall_scoring.j2 (4.4 KB)
└── text_features.j2 (4.7 KB)
```

**Files:** 9 files (identical to templates/)

---

## 5. DOCUMENTATION STRUCTURE (`docs/`)

```
docs/
├── BANKS_README.md (6.8 KB)
├── COMPREHENSION_PASSAGE_GENERATOR_README.md (13.9 KB)
├── ORF_ASSESSOR_MATERIALS_README.md (11.7 KB)
├── ORF_GENERATOR_README.md (5.2 KB)
├── PHASE_1_COMPLETE.md (7.2 KB)
├── PIB_GENERATOR_README.md (15.3 KB)
├── QRM_GENERATOR_README.md (13.8 KB)
├── QUESTION_GENERATOR_README.md (9.9 KB)
├── QUICK_REFERENCE.md (6.8 KB)
├── RECALL_SCORING_GENERATOR_README.md (8.6 KB)
├── example_complete_orf_package.py (10.5 KB)
├── example_orf_generator.py (4.9 KB)
├── example_pib_usage.py (17.7 KB)
└── example_qrm_usage.py (16.6 KB)
```

**Files:** 14 files (10 markdown docs + 4 Python examples)

---

## 6. TESTS STRUCTURE (`tests/`)

```
tests/
├── .DS_Store (6.0 KB)
├── integration/ (empty)
├── unit/
└── validation/ (empty)
```

### Unit Tests
```
tests/unit/
└── test_banks.py (5.1 KB)
```

**Files:** 1 Python test file

---

## 7. DATA STRUCTURE (`data/`)

```
data/
└── banks_export.json (25.4 KB)
```

**Files:** 1 JSON file

---

## 8. FILE STATISTICS

### 8.1 Top 5 Largest Files

| Rank | File | Size | Type |
|------|------|------|------|
| 1 | CHANGELOG.md | 60.3 KB | Documentation |
| 2 | question_generator.py | 28.4 KB | Source Code |
| 3 | pib_generator.py | 25.9 KB | Source Code |
| 4 | data/banks_export.json | 25.4 KB | Data |
| 5 | recall_scoring_generator.py | 24.4 KB | Source Code |

### 8.2 File Type Distribution

| Type | Count | Purpose |
|------|-------|---------|
| Python (.py) | 43 | Source code and tests |
| Markdown (.md) | 20 | Documentation |
| Jinja2 (.j2) | 17 | Prompt templates |
| JSON (.json) | 2 | Data files |
| Text (.txt) | 1 | Dependencies |
| Config | 2 | .env.example, .gitignore |
| System | ~15 | .DS_Store, __pycache__ |

### 8.3 Directory Depth Analysis

```
Level 0: /Users/lebron/Desktop/Bank Creator/ (root)
Level 1: src/, docs/, tests/, templates/, data/, orf_generator/
Level 2: src/banks/, src/generators/, src/utils/, src/packaging/
Level 3: orf_generator/src/banks/, orf_generator/src/generators/
Level 4: templates/prompts/, orf_generator/templates/prompts/
```

**Maximum Depth:** 4 levels

---

## 9. COMPONENT SUMMARY

### 9.1 Core Generators (7 total)
1. **base_generator.py** - Abstract base class
2. **comprehension_passage_generator.py** - Passage generation
3. **orf_assessor_materials_generator.py** - ORF materials
4. **orf_generator.py** - ORF passage generation
5. **pib_generator.py** - PIB (Passage Information Blueprint)
6. **qrm_generator.py** - QRM (Question Requirements Matrix)
7. **question_generator.py** - Question generation
8. **recall_scoring_generator.py** - Recall scoring rubrics

### 9.2 Content Banks (7 modules)
1. **answer_options.py** - Answer choice templates
2. **comp_word_counts.py** - Comprehension word count specs
3. **comprehension_blueprint.py** - Comprehension structure
4. **form_requirements.py** - Form specifications
5. **lexile_ranges.py** - Reading level ranges
6. **orf_word_counts.py** - ORF word count specs
7. **text_structures.py** - Text structure templates

### 9.3 Prompt Templates (8 templates)
1. comp_passage.j2
2. comp_pib.j2
3. comp_qrm.j2
4. orf_passage.j2
5. picture_description.j2
6. questions.j2
7. recall_scoring.j2
8. text_features.j2

---

## 10. OBSERVATIONS & NOTES

### 10.1 Duplicate Structures
- **templates/** and **templates-2/** contain identical files
- Both ORF generator and main src/ have similar bank structures

### 10.2 Empty Directories
- `complete_package/` - Empty
- `src/api/` - Empty
- `src/validation/` - Empty
- `tests/integration/` - Empty
- `tests/validation/` - Empty

### 10.3 Active Development Indicators
- Multiple __pycache__ directories (active Python execution)
- Recent test file: test_package_builder.py (20.8 KB) in root
- Audit workflow script in root
- Multiple fix/integration documentation files

### 10.4 Documentation Quality
- Comprehensive README files for each generator
- Example usage scripts provided
- CHANGELOG.md is the largest file (60+ KB)
- Clear separation of concerns in documentation

---

## 11. ARCHITECTURAL NOTES

### 11.1 Module Organization
- **Modular Design:** Clear separation between banks, generators, utils
- **Dual Structure:** Main src/ and separate orf_generator/ package
- **Template Separation:** Jinja2 templates isolated in templates/
- **Test Structure:** Unit tests present, integration tests planned

### 11.2 Code Distribution
- **Generators:** ~155 KB total (largest component)
- **Banks:** ~78 KB total (specification layer)
- **Utils:** ~8 KB total (minimal utilities)
- **Packaging:** ~16 KB (assembly layer)

---

## END OF REPORT

**Report Status:** ✅ COMPLETE  
**Verification:** All files and directories catalogued  
**No modifications made:** READ-ONLY diagnostic completed successfully
