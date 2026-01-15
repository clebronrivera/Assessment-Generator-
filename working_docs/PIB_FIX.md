# Fix PIB KeyError: 'scenes' Issue

**Date:** 2026-01-12  
**Issue:** Comprehension package test fails with `KeyError: 'scenes'`  
**Root Cause:** MockAI._pib_response() missing or incorrectly formatted  
**Priority:** HIGH - Blocking comprehension package testing

---

## Problem Analysis

### Error
```
KeyError: 'scenes'
```

### Location
PIB generator at line 429:
```python
for s_data in data["scenes"]:  # Expects 'scenes' key
```

### Root Cause
The MockAI in `test_package_builder.py` either:
1. Missing `_pib_response()` method
2. Has `_pib_response()` but returns wrong structure
3. Returns text instead of JSON
4. Has a typo in the response structure

---

## Solution: Complete MockAI Implementation

Replace or add the `_pib_response()` method in the MockAI class in `test_package_builder.py`:

```python
def _pib_response(self):
    """
    PIB (Passage Information Bank) response for Grade 2 narrative.
    MUST include 'scenes' key with proper structure.
    """
    import json
    return json.dumps({
        "scenes": [
            {
                "scene_number": 1,
                "scene_type": "opening",
                "location_in_passage": "beginning",
                "purpose": "Introduce main character and setting",
                "content_description": "Maya arrives at school on first day of second grade",
                "required_details": ["Maya's name", "second grade", "school entrance", "red backpack"],
                "supports_questions": [1],
                "vocabulary_placement": []
            },
            {
                "scene_number": 2,
                "scene_type": "action",
                "location_in_passage": "middle",
                "purpose": "Introduce conflict/problem",
                "content_description": "Maya sees new boy Jordan sitting alone, looking hesitant",
                "required_details": ["Jordan's name", "sitting alone", "hesitant", "recess"],
                "supports_questions": [2, 3, 5],
                "vocabulary_placement": ["hesitant"]
            },
            {
                "scene_number": 3,
                "scene_type": "action",
                "location_in_passage": "middle",
                "purpose": "Show main character's action",
                "content_description": "Maya invites Jordan to play tag",
                "required_details": ["Maya asks Jordan", "invitation to play", "tag game"],
                "supports_questions": [2, 4],
                "vocabulary_placement": []
            },
            {
                "scene_number": 4,
                "scene_type": "conclusion",
                "location_in_passage": "end",
                "purpose": "Show resolution and outcome",
                "content_description": "Jordan joins game, both kids happy, friendship formed",
                "required_details": ["Jordan joined", "laughing together", "Max happy", "making friends"],
                "supports_questions": [4, 6],
                "vocabulary_placement": []
            }
        ],
        "total_scenes": 4,
        "characters": [
            {
                "name": "Maya",
                "role": "main",
                "key_traits": ["friendly", "kind", "confident"],
                "actions_to_show": ["Invites Jordan to play", "Smiles", "Makes friend feel welcome"],
                "supports_questions": [1, 3, 4, 6]
            },
            {
                "name": "Jordan",
                "role": "supporting",
                "key_traits": ["new", "hesitant at first", "happy after"],
                "actions_to_show": ["Sits alone", "Looks hesitant", "Joins game", "Laughs"],
                "supports_questions": [2, 3, 4]
            }
        ],
        "opening_hook": "Maya was excited for second grade",
        "central_conflict_or_topic": "New student feels left out, main character helps include them",
        "resolution_or_conclusion": "Jordan joins in, makes friends, both kids happy",
        "target_lexile": "245L-425L",
        "target_word_count": 125,
        "vocabulary_targets": ["hesitant"],
        "vocabulary_contexts": {
            "hesitant": "He looked hesitant to join the other kids playing tag"
        },
        "text_structure": "chronological",
        "organizational_features": [],
        "question_coverage_map": {
            "1": [1],
            "2": [2, 3],
            "3": [2],
            "4": [3, 4],
            "5": [2],
            "6": [4]
        }
    })
```

---

## Verification

After adding the fix, the comprehension test should progress through:

```
[1] Generating QRM...
✓ QRM: 6 questions planned

[2] Generating PIB...
✓ PIB: 4 scenes blueprinted  # ← Should succeed now

[3] Generating Passage...
✓ Passage: ~125 words written

[4] Generating Questions...
✓ Questions: 6 questions with answer key

[5] Generating Recall Scoring...
✓ Recall: 9 sentences, 18 points

[6] Building Package...
✓ Package built: COMP-PKG-2-...
```

---

## Complete MockAI Class Structure

Ensure your MockAI in `test_package_builder.py` has all these methods:

```python
class MockAI:
    """Mock AI client for testing - Bank 4 compliant"""
    
    def complete(self, prompt):
        """Router method - calls appropriate response based on prompt"""
        if "Question Requirement Matrix" in prompt or "QRM" in prompt:
            return self._qrm_response()
        elif "Passage Information Bank" in prompt or "PIB" in prompt:
            return self._pib_response()
        elif "ORF" in prompt or "oral reading" in prompt.lower():
            return self._orf_response()
        elif "multiple choice questions" in prompt.lower():
            return self._questions_response()
        elif "recall scoring" in prompt.lower():
            return self._recall_response()
        else:
            return self._passage_response()
    
    def _qrm_response(self):
        """Grade 2 QRM - 6 questions, Bank 4 compliant"""
        # ... (your existing QRM response with cognitive: low=3, medium=3, high=0)
    
    def _pib_response(self):
        """Grade 2 PIB - 4 scenes"""
        # ... (use the complete implementation above)
    
    def _passage_response(self):
        """Comprehension passage text"""
        # ... (your existing passage)
    
    def _questions_response(self):
        """6 questions with answer options"""
        # ... (your existing questions)
    
    def _recall_response(self):
        """Recall scoring guide"""
        # ... (your existing recall)
    
    def _orf_response(self):
        """ORF passage text"""
        # ... (your existing ORF passage)
```

---

## Key Points

### 1. **'scenes' is Required**
PIB generator MUST receive a response with `"scenes"` key containing an array

### 2. **Proper Structure**
Each scene must have all required fields:
- `scene_number` (int)
- `scene_type` (string: "opening", "action", "dialogue", "description", "conclusion")
- `location_in_passage` (string: "beginning", "middle", "end")
- `purpose` (string)
- `content_description` (string)
- `required_details` (array of strings)
- `supports_questions` (array of ints)
- `vocabulary_placement` (array of strings, can be empty)

### 3. **Complete Response**
PIB response must also include:
- `total_scenes` (int)
- `characters` (array)
- `opening_hook` (string)
- `central_conflict_or_topic` (string)
- `resolution_or_conclusion` (string)
- `target_lexile` (string)
- `target_word_count` (int)
- `vocabulary_targets` (array)
- `vocabulary_contexts` (object)
- `text_structure` (string)
- `organizational_features` (array)
- `question_coverage_map` (object with string keys)

---

## Testing After Fix

```bash
cd "/Users/lebron/Desktop/Bank Creator"
python3 test_package_builder.py
```

**Expected Output:**
```
================================================================================
TESTING COMPREHENSION PACKAGE BUILDER
================================================================================
[1] Generating QRM...
✓ QRM: 6 questions planned
[2] Generating PIB...
✓ PIB: 4 scenes blueprinted
[3] Generating Passage...
✓ Passage: 125 words
[4] Generating Questions...
✓ Questions: 6 questions generated
[5] Generating Recall Scoring...
✓ Recall: Scoring guide created
[6] Building Package...
✓ Package built: COMP-PKG-2-...
[7] Exporting to JSON...
✓ JSON exported
[8] Creating manifest...
✓ Manifest created

================================================================================
COMPREHENSION PACKAGE TEST: PASSED ✓
================================================================================
```

---

## Common Issues

### Issue 1: Wrong scene_type values
**Error:** `ValueError: 'intro' is not a valid SceneType`  
**Fix:** Use only: "opening", "action", "dialogue", "description", "transition", "conclusion"

### Issue 2: Missing vocabulary_placement
**Error:** `KeyError: 'vocabulary_placement'`  
**Fix:** Add empty array `"vocabulary_placement": []` to each scene

### Issue 3: String keys in question_coverage_map
**Note:** Keys should be strings ("1", "2", "3") not integers  
PIB parser converts them to int internally

---

## Summary

**Problem:** Missing or malformed `_pib_response()` in MockAI  
**Solution:** Add complete PIB response with proper structure  
**Result:** Comprehension package test will pass  

**After this fix, both test suites should pass:**
- ✅ ORF Package Test
- ✅ Comprehension Package Test

**Final Status:** 6/6 challenges + PIB fix = Complete package builder integration
