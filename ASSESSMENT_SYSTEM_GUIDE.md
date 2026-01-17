# Assessment System - Complete Guide

## 🎯 Overview

This system manages 9 assessment types across 4 categories for reading assessment generation and management.

### Assessment Types

1. **Letter Recognition (LR-ALPH)** - Upper & lowercase letter identification
2. **Word Reading Fluency (FL-WRF)** - Timed word reading (K-3)
3. **Phoneme Segmentation Fluency (FL-PSF)** - Rapid phoneme counting
4. **Rhyme Recognition (PA-RHYM)** - Yes/no rhyme judgment
5. **Onset-Rime Blending (PA-OONS)** - Blend onset + rime
6. **Phoneme Segmentation (PA-PHON)** - Full phoneme segmentation
7. **Syllable Segmentation (PA-SYLS)** - Syllable counting
8. **Consonant Sound Accuracy (PH-CSA)** - Letter-sound correspondence
9. **Letter-Word Identification (PH-LWID)** - Mixed letters + words (K-3)

---

## 🚀 Getting Started

### 1. Start the Dashboard

```bash
cd "/Users/lebron/Desktop/Bank Creator"
python3 dashboard/app.py
```

Open browser: http://localhost:5001

### 2. Generate Your First Assessment Form

**Option A: Via Dashboard**
1. Navigate to http://localhost:5001/matrix
2. Find the assessment type you want to generate
3. Click "Generate" button (for missing assessments)
4. View generated form in the matrix

**Option B: Via Command Line**

```bash
# Generate Letter Recognition (Grade K, Form 1)
python3 generate_simple_assessment.py --assessment-id LR-ALPH --grade K

# Generate Word Reading Fluency Grade 1 (Form 1)
python3 generate_simple_assessment.py --assessment-id FL-WRF --grade 1

# Generate Rhyme Recognition (Form 2)
python3 generate_simple_assessment.py --assessment-id PA-RHYM --grade K --form-number 2
```

### 3. View Generated Forms

**In Dashboard:**
- **Assessment Matrix** (`/matrix`) → Expand row → See interface specifications
- **Warehouse Dashboard** (`/`) → View counts by category
- **Recent Activity** → Track generation history

**In File System:**
```
samples/
├── lr_alph_form1_k.json
├── lr_alph_form1_k_manifest.json
├── fl_wrf_form1_1.json
├── fl_wrf_form1_1_manifest.json
└── ...
```

---

## 🎮 Assessment Interface Specifications

Each assessment has defined interface specs for future Mission Control implementation:

### Letter Recognition (LR-ALPH)
- **Student View:** One letter at a time
- **Timing:** Timer counts UP (not down)
- **Assessor Interaction:** Click cycle (5 states)
  1. Correct (default)
  2. Incorrect (1 click)
  3. Self-correct (2 clicks)
  4. Omission (3-4 clicks)
  5. Reset (5 clicks)

### Word Reading Fluency (FL-WRF)
- **Student View:** One word at a time
- **Timing:** 60-second countdown
- **Assessor Interaction:** Same 5-state click cycle
- **Grades:** K, 1, 2, 3 (separate forms)

### Phonological Awareness (Audio Only)
These assessments are audio-only (assessor speaks):
- **PA-RHYM, PA-OONS, PA-PHON, PA-SYLS:** Untimed
- **FL-PSF:** 60-second timed
- **Assessor Interaction:** 
  - RHYM: Yes/No buttons
  - OONS, PHON: Correct/Incorrect/No Response
  - PSF, SYLS: Count input field

### Phonics Assessments
- **Student View:** One item at a time (visual)
- **Timing:** Untimed
- **Assessor Interaction:** Correct/Incorrect/No Response
- **PH-CSA:** 24 consonants/digraphs
- **PH-LWID:** Mix of letters and words by grade band

---

## 📊 Form Management

### Auto-Increment Form Numbers

The system automatically tracks and increments form numbers:

```bash
# First generation (creates Form 1)
python3 generate_simple_assessment.py --assessment-id LR-ALPH --grade K
# Creates: lr_alph_form1_k.json

# Second generation (creates Form 2)
python3 generate_simple_assessment.py --assessment-id LR-ALPH --grade K
# Creates: lr_alph_form2_k.json
```

### Grade-Specific Forms

Some assessments require grade level:

```bash
# Word Reading Fluency
python3 generate_simple_assessment.py --assessment-id FL-WRF --grade K
python3 generate_simple_assessment.py --assessment-id FL-WRF --grade 1
python3 generate_simple_assessment.py --assessment-id FL-WRF --grade 2
python3 generate_simple_assessment.py --assessment-id FL-WRF --grade 3

# Letter-Word Identification (uses grade bands)
python3 generate_simple_assessment.py --assessment-id PH-LWID --grade K
python3 generate_simple_assessment.py --assessment-id PH-LWID --grade 1  # Uses G1 band
python3 generate_simple_assessment.py --assessment-id PH-LWID --grade 2  # Uses G2_3 band
python3 generate_simple_assessment.py --assessment-id PH-LWID --grade 3  # Uses G2_3 band
```

---

## 🔧 Advanced Usage

### Inspect Assessment Registry

```python
from src.assessments.registry import ASSESSMENTS

# View all assessments
for asr_id, asr in ASSESSMENTS.items():
    print(f"{asr_id}: {asr['name']}")
    print(f"  Items: {asr['content']['total_items']}")
    print(f"  Timing: {asr['interface'].timing_mode.value}")
    print(f"  Presentation: {asr['interface'].student_presentation.value}")
```

### Access Word Banks

```python
from src.banks import word_banks

# Get words by grade
k_words = word_banks.get_words_by_grade('K')
print(f"Grade K words: {len(k_words)}")

# Get rhyming pairs
rhyme_pairs = word_banks.get_rhyming_pairs(count=10)
print(f"Rhyming pairs: {len(rhyme_pairs)}")

# Get onset-rime pairs
onset_rime = word_banks.get_onset_rime_pairs(count=20)
print(f"Onset-rime pairs: {len(onset_rime)}")
```

### Generate Multiple Forms Programmatically

```python
from src.generators.letter_recognition_generator import create_letter_recognition_generator
from src.generators.word_reading_fluency_generator import create_word_reading_fluency_generator
from pathlib import Path

samples_dir = Path("samples")

# Generate 3 letter recognition forms
lr_gen = create_letter_recognition_generator()
for i in range(1, 4):
    form = lr_gen.generate('K', i, samples_dir)
    print(f"Generated: {form['form_id']}")

# Generate word reading for all grades
wr_gen = create_word_reading_fluency_generator()
for grade in ['K', '1', '2', '3']:
    for form_num in [1, 2]:
        form = wr_gen.generate(grade, form_num, samples_dir)
        print(f"Generated: {form['form_id']}")
```

---

## 📈 Dashboard Features

### Matrix View (`/matrix`)

- **Expand/Collapse All:** Button to toggle all item specifications
- **Clickable Rows:** Click any row to expand/collapse specs
- **Filter by Grade/Type/Genre:** Use dropdowns to filter assessments
- **Search:** Search by grade, type, or package ID
- **Interface Specs:** See presentation mode, timing, click cycles when expanded
- **Form Tracking:** View all forms for each assessment type

### Warehouse Dashboard (`/`)

- **Category Counts:** Forms grouped by category (ORF, Comprehension, Simple Assessments)
- **Total Inventory:** Overall form count
- **Recent Activity:** Last 50 generations logged with metadata

### Generation API

```bash
# Generate via API
curl -X POST http://localhost:5001/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "assessment_type": "simple",
    "assessment_id": "LR-ALPH",
    "grade": "K"
  }'
```

---

## 🐛 Troubleshooting

### Forms Not Showing in Matrix

1. Refresh the page (Cmd+R or Ctrl+R)
2. Check `samples/` directory for JSON files
3. Verify file naming matches pattern: `{assessment_id}_form{number}_{grade}.json`
4. Restart the dashboard server

### Generation Fails

```bash
# Check for errors
python3 generate_simple_assessment.py --assessment-id LR-ALPH --grade K

# Verify system
python3 verify_system.py

# Check Python version (requires 3.7+)
python3 --version
```

### Dashboard Won't Start

```bash
# Check port 5001 is available
lsof -i :5001

# Kill existing process if needed
pkill -f "python.*dashboard/app.py"

# Try starting again
python3 dashboard/app.py
```

### Import Errors

If you see import errors:

```bash
# Ensure you're in the project root
cd "/Users/lebron/Desktop/Bank Creator"

# Check Python path
python3 -c "import sys; print(sys.path)"

# Test imports directly
python3 -c "from src.assessments.registry import ASSESSMENTS; print(len(ASSESSMENTS))"
```

---

## 🎯 Next Steps: Mission Control

The current system provides:
- ✅ Assessment registry with complete interface specifications
- ✅ Form generation and management
- ✅ Dashboard for viewing and generating content
- ✅ Auto-incrementing form numbers
- ✅ Grade-specific form generation

**Future Development: Mission Control Interface**
- Dual-screen interface (Assessor view + Student view)
- Real-time response recording with click cycles
- Timer implementation (count up/down)
- State management for click cycles
- Session scoring and data export
- Audio playback for phonological assessments

All interface specifications are already defined in the registry and ready for Mission Control implementation. The registry includes:
- Presentation modes (one-at-a-time, audio-only, etc.)
- Timing specifications (timer up, timer down, untimed)
- Click cycle patterns
- Assessor scripts
- Student prompts

---

## 📚 Reference

### Assessment ID Quick Reference

```
LR-ALPH  = Letter Recognition
FL-WRF   = Word Reading Fluency
FL-PSF   = Phoneme Segmentation Fluency
PA-RHYM  = Rhyme Recognition
PA-OONS  = Onset-Rime Blending
PA-PHON  = Phoneme Segmentation
PA-SYLS  = Syllable Segmentation
PH-CSA   = Consonant Sound Accuracy
PH-LWID  = Letter-Word Identification
```

### File Locations

```
src/assessments/          → Registry & interface definitions
  ├── __init__.py
  ├── interfaces.py
  └── registry.py

src/banks/                → Word banks & item pools
  └── word_banks.py

src/generators/           → Form generators
  ├── simple_assessment_generator.py
  ├── letter_recognition_generator.py
  ├── word_reading_fluency_generator.py
  └── ... (7 more generators)

src/utils/                → Utilities
  └── assessment_matrix.py

samples/                  → Generated assessment forms
  ├── lr_alph_form1_k.json
  ├── lr_alph_form1_k_manifest.json
  └── ...

dashboard/                → Web interface
  ├── app.py
  └── templates/
      ├── index.html
      └── matrix.html

generate_simple_assessment.py  → CLI tool
verify_system.py               → Verification script
```

### Command Line Examples

```bash
# Generate all assessment types (one form each)
for ass_id in LR-ALPH FL-WRF FL-PSF PA-RHYM PA-OONS PA-PHON PA-SYLS PH-CSA PH-LWID; do
    python3 generate_simple_assessment.py --assessment-id $ass_id --grade K
done

# Generate multiple forms for Word Reading Fluency
for grade in K 1 2 3; do
    for form in 1 2; do
        python3 generate_simple_assessment.py --assessment-id FL-WRF --grade $grade --form-number $form
    done
done
```

---

## ✅ Verification

Run the verification script to ensure everything is working:

```bash
python3 verify_system.py
```

This will check:
- All required files exist
- All modules can be imported
- Registry contains all 9 assessments
- Generators can create forms
- Generated forms exist in samples directory

---

**Questions?** Check `verify_system.py` for system health checks, or review the code in `src/assessments/registry.py` for complete assessment specifications.
