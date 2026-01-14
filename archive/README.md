# Archive Directory

## orf_generator_legacy_20260112/
Legacy standalone ORF generator package from early development.

**Why Archived:**
- Functionality now integrated into `src/generators/`
- Uses outdated API (`ai_client.generate()` instead of `ai_client.complete()`)
- Kept for historical reference

**Key Difference:**
The legacy version calls `self.ai_client.generate(prompt)` while the current implementation uses `self.ai_client.complete(prompt)`.

**Safe to Delete:** After 30 days if no issues arise (after February 12, 2026)
