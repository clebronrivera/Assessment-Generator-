#!/usr/bin/env python3
"""
Quick script to add passage_title and word_count fields to ORF sample JSON files.
This script:
1. Finds all ORF sample JSON files (excludes manifests)
2. Extracts the first sentence from passage_text as the title
3. Adds passage_title and word_count fields to the passage object
4. Saves the updated JSON files
"""

import json
import os
from pathlib import Path

def count_words(text):
    """Count words in text."""
    return len(text.split())

def extract_title_from_text(text):
    """Extract first sentence from passage text to use as title."""
    # Get first sentence (up to first period, question mark, or exclamation)
    first_sentence = text.split('.')[0].split('?')[0].split('!')[0].strip()
    # Limit to reasonable title length
    if len(first_sentence) > 80:
        first_sentence = first_sentence[:77] + "..."
    return first_sentence

def process_orf_file(filepath):
    """Add title and word count to an ORF JSON file."""
    print(f"\nProcessing: {filepath.name}")
    
    # Load JSON
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Check if this is an ORF file
    if data.get('package_type') != 'orf':
        print(f"  ⚠️  Skipping - not an ORF package")
        return False
    
    # Check if passage exists
    if 'passage' not in data:
        print(f"  ⚠️  Skipping - no passage found")
        return False
    
    passage = data['passage']
    
    # Check if passage_text exists
    if 'passage_text' not in passage:
        print(f"  ⚠️  Skipping - no passage_text found")
        return False
    
    passage_text = passage['passage_text']
    
    # Count words
    word_count = count_words(passage_text)
    
    # Extract title from first sentence
    title = extract_title_from_text(passage_text)
    
    # Add fields
    passage['passage_title'] = title
    passage['word_count'] = word_count
    
    # Save updated JSON
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"  ✅ Added title: \"{title}\"")
    print(f"  ✅ Added word count: {word_count}")
    
    return True

def main():
    """Main function to process all ORF sample files."""
    samples_dir = Path(__file__).parent / 'samples'
    
    if not samples_dir.exists():
        print(f"❌ Samples directory not found: {samples_dir}")
        return
    
    print(f"📁 Scanning directory: {samples_dir}")
    
    # Find all ORF sample JSON files (exclude manifests)
    orf_files = sorted(samples_dir.glob('sample_orf_*.json'))
    orf_files = [f for f in orf_files if 'manifest' not in f.name]
    
    print(f"📄 Found {len(orf_files)} ORF sample files")
    
    processed = 0
    for filepath in orf_files:
        if process_orf_file(filepath):
            processed += 1
    
    print(f"\n{'='*60}")
    print(f"✅ Successfully processed {processed}/{len(orf_files)} files")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
