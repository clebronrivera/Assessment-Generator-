# Recall Scoring Generator Migration

**Date:** January 14, 2026  
**Status:** Complete  

---

## What Changed

The original `recall_scoring_generator.py` has been **archived** and replaced with `simplified_recall_scoring_generator.py`.

---

## Why the Change?

### Original Generator Issues:
- ❌ Complex JSON structure (120-180 fields per passage)
- ❌ AI consistently generated malformed JSON
- ❌ Failed even after 3 retry attempts
- ❌ Blocked completion of comprehension samples

### Simplified Generator Benefits:
- ✅ Simple JSON structure (20-30 fields per passage)
- ✅ Reliable AI generation (succeeds in 1-2 attempts)
- ✅ Practical character + detail scoring approach
- ✅ Matches real teacher scoring practices

---

## What Was Archived

### File Moved:
```
src/generators/recall_scoring_generator.py
→ src/generators/archived/recall_scoring_generator.py
```

### Reason:
Too complex for reliable AI generation.

### Replacement:
`src/generators/simplified_recall_scoring_generator.py`

---

## Migration Path

### For Existing Code:

**Option 1: Use new import (recommended)**
```python
from src.generators import create_simplified_recall_scoring_generator

recall_gen = create_simplified_recall_scoring_generator(ai_client)
```

**Option 2: Use backwards-compatible alias**
```python
from src.generators import create_recall_scoring_generator  # Now points to simplified version

recall_gen = create_recall_scoring_generator(ai_client)
```

Both work! The alias ensures old code doesn't break.

---

## Scoring Approach Comparison

### Old (Complex):
For each sentence:
- 2-4 key ideas with importance weights
- 4-8 partial credit keywords
- Detailed 0/1/2 point rubrics
- 3 example student responses
- **Result:** 12-20 fields per sentence

### New (Simplified):
For each sentence:
- Character name
- Key detail
- Simple scoring note
- **Result:** 3-4 fields per sentence

### Scoring Rule:
- 2 points: Character + detail both recalled
- 1 point: Either character OR detail recalled
- 0 points: Neither recalled

---

## What You Need to Do

### If you have existing code using recall scoring:

1. **No immediate changes required** - The alias ensures compatibility

2. **Recommended update** (at your convenience):
   ```python
   # Old import
   from src.generators import create_recall_scoring_generator
   
   # New import (recommended)
   from src.generators import create_simplified_recall_scoring_generator
   ```

3. **Update variable names** (optional, for clarity):
   ```python
   # Instead of:
   recall_gen = create_recall_scoring_generator(ai_client)
   
   # Use:
   recall_gen = create_simplified_recall_scoring_generator(ai_client)
   ```

### Sample Generation Scripts:

- ✅ `generate_samples_simplified.py` - Already uses new generator
- ⚠️ `generate_samples.py` - Still uses old generator (will fail)

**Recommended:** Use `generate_samples_simplified.py` going forward.

---

## Testing

To verify the new generator works:
```bash
python3.11 tests/test_simplified_recall.py
```

To generate samples with new recall scoring:
```bash
python3.11 generate_samples_simplified.py
```

---

## Rollback Plan (If Needed)

If you need to temporarily restore the old generator:

```bash
# Move back from archive
git mv src/generators/archived/recall_scoring_generator.py src/generators/

# Update __init__.py to import old version
# (restore old import statement)

# Recommit
git add -A
git commit -m "temp: Restore old recall generator"
```

**Note:** This is not recommended as the old generator has known reliability issues.

---

## Files Modified

1. `src/generators/archived/recall_scoring_generator.py` - Moved here
2. `src/generators/simplified_recall_scoring_generator.py` - New implementation
3. `src/generators/__init__.py` - Updated to export new generator
4. `generate_samples_simplified.py` - New sample generation script
5. `tests/test_simplified_recall.py` - Tests for new generator

---

## Success Metrics

After migration:
- ✅ All 3 sample assessments generated successfully
- ✅ Recall scoring succeeds on first or second attempt
- ✅ No JSON parsing errors
- ✅ Practical, teacher-friendly scoring rubrics
- ✅ ~$2-3 API cost (vs $5-6 with old approach due to retries)

---

## Questions?

See implementation guide: `IMPLEMENTATION_GUIDE.md`

---

## Archive Policy

Archived generators are kept for:
- Reference and comparison
- Understanding design decisions
- Historical context
- Emergency restoration if needed

Archived code is:
- Not actively maintained
- Not imported by default
- Documented with deprecation reason
- Preserved for reference only
