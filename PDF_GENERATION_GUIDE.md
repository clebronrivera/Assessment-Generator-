# PDF Generation Guide

## Overview
The system now generates both **Assessor PDFs** and **Student PDFs** for all assessment types, with specialized formatting for different assessment categories.

## Features Implemented

### 1. PDF Generation Library
- Added `weasyprint` to `requirements.txt` for HTML-to-PDF conversion
- Created PDF generation utilities in `src/utils/page_generator.py`
- Added PDF download routes in `dashboard/app.py`

### 2. Spelling Assessments (PH-SPEL)
**Student PDF:**
- Shows numbered items with blanks/underlines for writing
- Each blank corresponds to a letter in the word
- Clean, simple layout for student responses

**Assessor PDF:**
- Shows the actual words to dictate
- Includes space to record student's actual response
- Full answer key with all correct spellings

### 3. Multiple Choice Questions (Comprehension, etc.)
**Student PDF:**
- Shows complete questions with all answer options (A, B, C, D)
- Includes passage text for comprehension assessments
- Clear numbering and formatting

**Assessor PDF:**
- Shows all questions with answer options
- Correct answers clearly marked (✓)
- **Wrong Answer Tracking**: Space to circle which wrong answer the student selected
- Allows recording of specific distractor types selected
- Useful for error analysis (e.g., "student selected B instead of A")

### 4. Audio-Only Assessments (Rhyme Recognition, etc.)
**Student PDF:**
- Shows numbered items with instructions (e.g., "Listen for word pair")
- No visual stimulus shown to student
- Clean, minimal layout

**Assessor PDF:**
- Complete answer key with expected responses
- All items listed with correct answers
- Instructions for administration

### 5. Visual Assessments (Letter Recognition, etc.)
**Student PDF:**
- Shows actual items (letters, words, etc.) in grid or list format
- Clear numbering
- Large, readable fonts

**Assessor PDF:**
- Answer key with all correct responses
- Scoring information
- Response coding instructions

## Usage

### Via Dashboard
1. Navigate to an assessment in the dashboard
2. Click "View Assessor Page" or "View Student Page" to see HTML preview
3. Click "🖨️ Print" button to print from browser, OR
4. Use new PDF download routes:
   - `/pdf/assessor/<sample_name>` - Download assessor PDF
   - `/pdf/student/<sample_name>` - Download student PDF

### Programmatically
```python
from pathlib import Path
from src.utils.page_generator import generate_pdfs_for_assessment

assessment_file = Path("samples/sample_1.json")
templates_dir = Path("templates")
output_dir = Path("output/pdfs")

pdfs = generate_pdfs_for_assessment(assessment_file, templates_dir, output_dir)
# Returns: {'assessor': Path(...), 'student': Path(...)}
```

## Installation

```bash
pip install weasyprint
```

Note: On some systems, you may need to install additional system dependencies for WeasyPrint. See https://doc.courtbouillon.org/weasyprint/stable/first_steps.html

## Technical Details

### Assessment Type Detection
The system automatically detects assessment types based on:
- `assessment_id` field (e.g., "PH-SPEL" for spelling)
- `student_presentation` mode (e.g., "audio_only")
- Presence of `answer_options` in items (multiple choice)
- Presence of `questions.questions` structure (comprehension)

### Template Customization
Templates automatically adapt based on:
- Assessment ID
- Item structure
- Student presentation mode
- Assessor interaction type

### Wrong Answer Recording
For multiple choice questions, the assessor PDF includes:
- All answer options listed
- Correct answer clearly marked
- Checkboxes/circles to mark which wrong answer was selected
- Useful for diagnostic analysis of student errors

## Examples

### Spelling Assessment
**Student sees:**
```
1. _____ _____ _____ _____  (blanks for "word")
2. _____ _____ _____ _____  (blanks for "read")
```

**Assessor sees:**
```
1. word
   Student response: ________________________
2. read
   Student response: ________________________
```

### Multiple Choice (Rhyme Recognition)
**Student sees:**
```
1. Listen for word pair
2. Listen for word pair
```

**Assessor sees:**
```
1. cup / fox → No
2. sun / fun → Yes
```

### Comprehension Questions
**Student sees:**
- Full passage text
- Questions with A, B, C, D options

**Assessor sees:**
- Questions with all options
- Correct answers marked
- Space to record wrong answers selected

## Future Enhancements

- Add QR codes to link PDFs to digital assessment interface
- Support for custom page layouts per assessment type
- Batch PDF generation for multiple assessments
- PDF watermarking for form tracking