# Integration Challenges - Additional Fixes Required

**Date:** 2026-01-12 13:33  
**Status:** New issues discovered after initial fixes applied  
**Priority:** HIGH - Blocking package builder testing

---

## Summary

Initial fixes applied successfully:
- ✅ ORF generator now uses `complete()` method
- ✅ Test mocks updated to provide 6 questions

New issues discovered:
- ❌ Challenge 1: ORF generator return type mismatch
- ❌ Challenge 2: Mock data doesn't match actual Bank 4 specifications

---

## Challenge 1: ORF Generator Return Type Mismatch

### The Problem

**Error:**
```
AttributeError: 'dict' object has no attribute 'metadata'
```

**Location:** `test_package_builder.py`, line 357

**Root Cause:**
```python
# Package builder expects:
passage.metadata['actual_word_count']  # Object with .metadata attribute

# But ORF generator likely returns:
{
    'metadata': {...},
    'passage_text': '...'
}  # Dict, not object
```

### Investigation Needed

We need to check the actual ORF generator to see what it returns. Based on other generators, it should return a dataclass with attributes, not a dictionary.

**Likely scenarios:**

**Scenario A: ORF returns dict (inconsistent)**
```python
# If ORF generator returns:
return {
    "passage_text": text,
    "metadata": {
        "form_id": form_id,
        "actual_word_count": count
    }
}

# Then access would be:
passage["metadata"]["actual_word_count"]  # Dict notation
```

**Scenario B: ORF returns object (consistent)**
```python
# If ORF generator returns (like other generators):
@dataclass
class ORFPassageResult:
    passage_text: str
    metadata: Dict[str, Any]

# Then access would be:
passage.metadata["actual_word_count"]  # Object.attribute notation
```

### Solution

**Check the actual ORF generator code** to determine:
1. Does it return a dataclass or dict?
2. What is the structure?
3. How do other generators access ORF passage data?

**Then apply appropriate fix:**

**If ORF returns dict:** Update package builder to handle dict access:
```python
# In assessment_package_builder.py
# Current (line ~160):
passage_word_count = passage_result.metadata["actual_word_count"]

# Fix for dict:
if isinstance(passage_result, dict):
    passage_word_count = passage_result["metadata"]["actual_word_count"]
else:
    passage_word_count = passage_result.metadata["actual_word_count"]
```

**If ORF returns object:** No changes needed, test code is correct.

---

## Challenge 2: Mock Data Doesn't Match Bank 4

### The Problem

**Error:**
```
ValueError: Question type 'explicit' count mismatch: got 2, expected 4
```

**Location:** `src/generators/qrm_generator.py`, line 401

**Root Cause:**

Our mock provides:
```python
"type_distribution": {
    "explicit": 2,      # ❌ Wrong
    "implicit": 2,
    "vocabulary": 1,
    "main_idea": 1
}
```

But Bank 4 actually requires (for Grade 2 narrative):
```python
"type_distribution": {
    "explicit": 4,      # ✅ Correct
    "implicit": 1,
    "vocabulary": 1,
    "main_idea": 0      # Or similar distribution
}
```

### Solution: Check Actual Bank 4

**Need to examine:** `src/banks/comprehension_blueprint.py`

**Look for:** Grade 2, narrative genre specifications

**Then update mock to match exactly**

---

## Action Plan

### Step 1: Investigate ORF Return Type

```bash
# Check ORF generator return type
grep -A 20 "def generate" src/generators/orf_generator.py | grep -A 10 "return"

# Check if it returns dataclass or dict
grep "@dataclass" src/generators/orf_generator.py
grep "class.*Result" src/generators/orf_generator.py
```

### Step 2: Check Bank 4 for Grade 2

```bash
# View Bank 4 Grade 2 specifications
# File: src/banks/comprehension_blueprint.py
# Look for Grade 2 narrative distribution
```

**Method A: If you have the file**
```python
from src.banks import get_blueprint
blueprint = get_blueprint("2")
print(blueprint.question_types)  # See actual distribution
```

**Method B: Check the bank file directly**
```bash
grep -A 30 "grade.*2" src/banks/comprehension_blueprint.py
```

### Step 3: Apply Fixes

**Fix 1: Update test_package_builder.py for ORF**

If ORF returns dict:
```python
# Line 357 - Change from:
passage_word_count = passage.metadata['actual_word_count']

# To:
passage_word_count = (
    passage["metadata"]["actual_word_count"] 
    if isinstance(passage, dict) 
    else passage.metadata["actual_word_count"]
)
```

**Fix 2: Update MockAI with correct Bank 4 data**

```python
def _mock_get_blueprint(self, grade: str) -> Dict[str, Any]:
    """Mock Bank 4 data - MUST match actual bank exactly"""
    if grade == "2":
        return {
            "total_questions": 6,
            "question_types": {
                "explicit": 4,      # ✅ Corrected from Bank 4
                "implicit": 1,      # ✅ Corrected
                "vocabulary": 1,    # ✅ Same
                "main_idea": 0      # ✅ Corrected
            },
            "cognitive_demands": {
                "low": 2,
                "medium": 3,
                "high": 1
            }
        }
```

**Then update MockAI._qrm_response() to match:**

```python
def _qrm_response(self):
    import json
    return json.dumps({
        "questions": [
            # Question 1: explicit, low
            {"question_number": 1, "question_type": "explicit", "cognitive_demand": "low", ...},
            # Question 2: explicit, low  
            {"question_number": 2, "question_type": "explicit", "cognitive_demand": "low", ...},
            # Question 3: explicit, medium
            {"question_number": 3, "question_type": "explicit", "cognitive_demand": "medium", ...},
            # Question 4: explicit, medium
            {"question_number": 4, "question_type": "explicit", "cognitive_demand": "medium", ...},
            # Question 5: vocabulary, medium
            {"question_number": 5, "question_type": "vocabulary", "cognitive_demand": "medium", ...},
            # Question 6: implicit, high
            {"question_number": 6, "question_type": "implicit", "cognitive_demand": "high", ...}
        ],
        "total_questions": 6,
        "type_distribution": {
            "explicit": 4,      # ✅ Updated
            "implicit": 1,      # ✅ Updated
            "vocabulary": 1,
            "main_idea": 0      # ✅ Updated
        },
        "cognitive_distribution": {
            "low": 2,
            "medium": 3,
            "high": 1
        },
        # ... rest unchanged
    })
```

### Step 4: Verify Fixes

```bash
# Run tests
python3 test_package_builder.py

# Expected output:
# ✓ ORF package test passed
# ✓ Comprehension package test passed
# ✓ All package builder tests passed!
```

---

## Questions to Answer

### For Challenge 1 (ORF Return Type):

1. **What does `src/generators/orf_generator.py` actually return?**
   - Dict or dataclass?
   - What is the exact structure?

2. **How does `orf_assessor_materials_generator.py` access ORF data?**
   - Does it use dict notation or object attributes?
   - This will show us the expected pattern

3. **Do we need to fix the generator or the test?**
   - If generator returns dict: Fix test to use dict notation
   - If generator returns object: Test is correct, investigate why it's failing

### For Challenge 2 (Bank 4 Distribution):

1. **What is the actual Bank 4 Grade 2 narrative distribution?**
   - How many explicit questions? (We think 4, not 2)
   - How many implicit questions? (We think 1, not 2)
   - How many main_idea questions? (We think 0, not 1)

2. **Are there different distributions for narrative vs. nonfiction?**
   - Should we check both?
   - Should our mock support both?

---

## Recommended Next Steps

**Immediate (to unblock testing):**

1. Check `src/generators/orf_generator.py` return type
2. Check `src/banks/comprehension_blueprint.py` Grade 2 specs
3. Apply both fixes
4. Re-run tests

**If you need my help:**

- I can search for the ORF generator code and check return type
- I can help create the correct Bank 4-compliant mock
- I can update the test file with both fixes

**Please confirm:**

1. Should I investigate and propose specific fixes?
2. Or should I wait for you to check the actual files?
3. Do you want me to create a corrected test_package_builder.py with both fixes?

---

## Status

**Current State:**
- ✅ Initial fixes applied (API standardization, 6 questions)
- ❌ New challenges blocking tests
- 🔍 Investigation needed for both issues

**Next Action Required:**
- Investigate ORF return type
- Check Bank 4 Grade 2 distribution
- Apply corrective fixes
- Verify tests pass

**Priority:** HIGH - This blocks package builder integration completion
