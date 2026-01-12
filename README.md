# Reading Assessment Generator

A bank-driven system for generating K-8 reading assessments with complete anti-drift protocols. Produces ORF (Oral Reading Fluency) and comprehension assessments with all necessary materials for educators.

## 🎯 Overview

This system generates research-aligned reading assessments by:
1. Using **Foundation Banks** as the single source of truth (no hardcoded values)
2. Following a **QRM→PIB→Passage** workflow for comprehension (plan questions before writing)
3. Validating all outputs against bank specifications
4. Producing complete assessment packages ready for classroom use

## ✨ Features

### Current Capabilities (Phase 2B Complete - 100% Verified)

- ✅ **ORF Assessments** (Grades 1-8)
  - Lexile-targeted passages (Bank 1)
  - Word count validation ±2 words (Bank 2)
  - Complete assessor materials (timing scripts, score sheets, rubrics)
  
- ✅ **Comprehension Passages** (Grades K-8+)
  - QRM: Question planning with Bank 4 validation
  - PIB: Scene-by-scene content blueprinting
  - Passage: AI-generated text with validation
  - Word count ±20 words (Bank 3)
  - Vocabulary verification
  - 100% audit-verified workflow

### Coming Soon (Phase 2C - In Progress)

- ⏳ Multiple choice question generation
- ⏳ Recall scoring templates
- ⏳ Complete assessment packages

## 🏗️ Architecture

### Foundation Banks (Phase 1 - Complete)

Seven immutable banks provide all specifications:

1. **Bank 1:** Lexile Ranges (20 ranges, K-8+, Early/Late)
2. **Bank 2:** ORF Word Counts (WCPM benchmarks)
3. **Bank 3:** Comprehension Word Counts
4. **Bank 4:** Comprehension Blueprint (118 question specs)
5. **Bank 5:** Form Requirements
6. **Bank 6:** Answer Options by Grade
7. **Bank 7:** Text Structures (Narrative/Nonfiction)

### Core Generators (Phase 2A & 2B - Complete)

**ORF Workflow:**
```python
passage = orf_generator.generate(grade="2", band="early")
materials = assessor_materials_generator.generate(
    grade="2", 
    passage_text=passage.passage_text,
    passage_word_count=passage.actual_word_count,
    form_id=passage.form_id
)
```

**Comprehension Workflow:**
```python
# Step 1: Plan questions (QRM)
qrm = qrm_generator.generate(grade="2", genre="narrative", band="early")

# Step 2: Blueprint content (PIB)
pib = pib_generator.generate(qrm_result=qrm)

# Step 3: Write passage
passage = passage_generator.generate(qrm_result=qrm, pib_result=pib)
```

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/reading-assessment-generator.git
cd reading-assessment-generator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create `.env` file:

```bash
# Choose your AI provider
OPENAI_API_KEY=your_key_here
# OR
ANTHROPIC_API_KEY=your_key_here
```

### Usage

```python
from src.generators import create_orf_generator
from src.utils import create_ai_client

# Create AI client
ai_client = create_ai_client("your_api_key")

# Generate ORF assessment
orf_gen = create_orf_generator(ai_client)
passage = orf_gen.generate(grade="2", band="early")

print(passage.passage_text)
print(f"Word count: {passage.actual_word_count}")
print(f"Lexile: {passage.metadata['lexile_target']}")
```

See `docs/examples/` for complete workflows.

## 📊 Project Status

**Overall Progress:** ~40% Complete

- ✅ Phase 1: Foundation Banks (100%)
- ✅ Phase 2A: ORF Workflow (100%)
- ✅ Phase 2B: Comprehension Workflow (100% - VERIFIED)
- 🔄 Phase 2C: Question & Recall Generators (In Progress)
- ⏳ Phase 3: User Interface & Workflow
- ⏳ Phase 4: Validation & Quality Checks
- ⏳ Phase 5: Output & Packaging
- ⏳ Phase 6: Testing & Verification

## 🧪 Testing

```bash
# Run bank validation tests
python -m pytest tests/unit/test_banks.py

# Run comprehensive workflow audit
python audit_workflow.py
```

**Latest Audit:** 100% pass rate (12/12 tests) - 2026-01-12

## 📖 Documentation

- **[Banks Documentation](docs/BANKS_README.md)** - Complete bank specifications
- **[Quick Reference](docs/QUICK_REFERENCE.md)** - Bank lookup guide
- **[Anti-Drift Protocol](ANTI_DRIFT_PROTOCOL.md)** - Development guidelines
- **[Task List](TASK_LIST.md)** - Current project status
- **[Changelog](CHANGELOG.md)** - Development history

### Component Documentation

- [ORF Generator](docs/ORF_GENERATOR_README.md)
- [ORF Assessor Materials](docs/ORF_ASSESSOR_MATERIALS_README.md)
- [QRM Generator](docs/QRM_GENERATOR_README.md)
- [PIB Generator](docs/PIB_GENERATOR_README.md)
- [Comprehension Passage Generator](docs/COMPREHENSION_PASSAGE_GENERATOR_README.md)

## 🔒 Anti-Drift Protocol

This project follows strict anti-drift protocols:

- **All data from banks** - No hardcoded specifications
- **Bank usage logged** - Every generation tracks which banks used
- **Validation enforced** - Outputs validated against bank constraints
- **Immutable banks** - Banks are frozen dataclasses
- **Schema versioning** - All outputs include schema version

See [ANTI_DRIFT_PROTOCOL.md](ANTI_DRIFT_PROTOCOL.md) for complete guidelines.

## 🤝 Contributing

This project is currently in active development. Contribution guidelines will be added in Phase 6.

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Research-aligned with DIBELS, AIMSweb, and NAEP standards
- Built with anti-drift protocols for long-term maintainability
- Validated through comprehensive automated testing

---

**Version:** 2026.1  
**Last Updated:** 2026-01-12  
**Status:** Phase 2C In Progress
