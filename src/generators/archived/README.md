# Archived Generators

This directory contains deprecated generator implementations that have been replaced with improved versions.

## Why Archive Instead of Delete?

- Preserves implementation history
- Allows comparison with new approach
- Reference for understanding design decisions
- Easy restoration if needed

## Archived Files

### recall_scoring_generator.py
**Date Archived:** January 14, 2026  
**Reason:** Replaced with simplified_recall_scoring_generator.py  
**Issue:** Complex JSON structure (120-180 fields) caused unreliable AI generation  
**Replacement:** Simplified approach using character + detail scoring (20-30 fields)  

See: simplified_recall_scoring_generator.py for current implementation
