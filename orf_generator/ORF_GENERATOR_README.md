# ORF Generator

The **ORF (Oral Reading Fluency) Generator** creates grade-appropriate narrative passages for timed oral reading assessments. All passages strictly adhere to specifications from Foundation Banks with ±2 word tolerance.

## What It Does

Generates passages that:
- Target specific Lexile ranges (Bank 1)
- Hit precise word counts with ±2 word tolerance (Bank 2)
- Use appropriate narrative structures (Bank 7)
- Are optimized for oral reading fluency
- Include validation and retry logic

## Quick Start

### 1. Basic Usage (No AI - Get Prompt Only)

```python
from src import banks
from src.generators import create_orf_generator

# Create generator
generator = create_orf_generator(banks)

# Get the prompt (no AI call)
result = generator.generate(
    grade="2",
    band="early"
)

print(result["prompt"])  # The full AI prompt
print(result["specs"])   # All bank specifications used
```

### 2. Generate with Mock AI (No API Key Needed)

```python
from src.utils import create_ai_client

# Create mock AI (returns sample passages)
ai_client = create_ai_client("fake_key", provider="mock")

# Generate passage
result = generator.generate(
    grade="2",
    band="early",
    ai_client=ai_client
)

print(result["passage_text"])
print(result["validation"])
```

### 3. Generate with Real AI

```python
# For Anthropic Claude
ai_client = create_ai_client("your-api-key", provider="anthropic")

# For OpenAI
# ai_client = create_ai_client("your-api-key", provider="openai")

# Generate with automatic retry on validation failure
result = generator.generate_with_retry(
    grade="3",
    band="late",
    ai_client=ai_client,
    max_retries=3,
    topic_constraint="nature",
    structure="chronological"
)

# Save to file
generator.save_output(result, "outputs/grade3_passage.json")
```

## API Reference

### `ORFGenerator.generate()`

**Parameters:**
- `grade` (str): Grade level (1-8)
- `band` (str): Lexile band ("early" or "late") - default: "early"
- `topic_constraint` (str, optional): Topic guidance (e.g., "animals", "school")
- `prohibited_content` (str, optional): Content to avoid (e.g., "no dialogue")
- `structure` (str): Text structure - default: "chronological"
  - Options: chronological, problem_solution, compare_contrast, cause_effect, description
- `ai_client` (optional): AI client for generation

**Returns:**
```python
{
    "passage_text": "The generated passage...",
    "grade": "2",
    "band": "early",
    "lexile_range": "245L to 425L",
    "target_word_count": 140,
    "structure": "chronological",
    "bank_usage": {
        "Bank 1 (Lexile)": "245L-425L",
        "Bank 2 (ORF Word Counts)": "Target: 140 words",
        "Bank 7 (Text Structure)": "chronological"
    },
    "validation": {
        "valid": True,
        "errors": [],
        "warnings": ["Word count: 140 (target: 140, within ±2)"]
    }
}
```

### `ORFGenerator.generate_with_retry()`

Same as `generate()` but includes automatic retry logic:

**Additional Parameters:**
- `max_retries` (int): Maximum retry attempts - default: 3

**Additional Return Fields:**
- `attempts` (int): Number of attempts made

## Word Count Specifications

All word counts from Bank 2 with ±2 word tolerance:

| Grade | Target | Min | Max | Lexile Range |
|-------|--------|-----|-----|--------------|
| 1 | 110 | 108 | 112 | BR35L to 165L |
| 2 | 140 | 138 | 142 | 245L to 425L |
| 3 | 150 | 148 | 152 | 480L to 645L |
| 4 | 170 | 168 | 172 | 700L to 850L |
| 5 | 180 | 178 | 182 | 795L to 945L |
| 6 | 190 | 188 | 192 | 875L to 1025L |
| 7 | 200 | 198 | 202 | 940L to 1095L |
| 8 | 210 | 208 | 212 | 1000L to 1155L |

## Validation

The generator automatically validates:
- ✅ Word count within ±2 words
- ✅ Passage exists and isn't empty
- ✅ Minimum quality checks
- ⚠️ Warnings for formatting issues

## Examples

Run the complete examples:
```bash
python example_orf_generator.py
```

This demonstrates:
1. Generating prompts without AI
2. Using mock AI for testing
3. Setting up real AI (commented out)
4. Batch generation for multiple grades
5. Viewing all available specifications

## Bank Usage

The ORF Generator uses these foundation banks:
- **Bank 1**: Lexile Ranges (grade/band targeting)
- **Bank 2**: ORF Word Counts (±2 word tolerance)
- **Bank 7**: Text Structures (narrative patterns)

## Files

```
src/
  generators/
    base_generator.py          # Base class for all generators
    orf_generator.py          # ORF-specific generator
  utils/
    ai_client.py              # AI API wrapper (OpenAI, Anthropic, Mock)
templates/
  prompts/
    orf_passage.j2            # Jinja2 template for ORF generation
example_orf_generator.py       # Complete examples
```

## AI Client Setup

### Anthropic Claude
```bash
pip install anthropic
export ANTHROPIC_API_KEY="your-key-here"
```

### OpenAI
```bash
pip install openai
export OPENAI_API_KEY="your-key-here"
```

### Using Environment Variables
```python
import os
from src.utils import create_ai_client

api_key = os.getenv("ANTHROPIC_API_KEY")
ai_client = create_ai_client(api_key, provider="anthropic")
```

## Next Steps

After ORF Generator, the system includes:
- **Comprehension Generator** (6 components)
- **Question Generator**
- **Recall Scoring Generator**
- **Picture Description Generator** (K-1)
- **Text Features Generator** (6-8+)
