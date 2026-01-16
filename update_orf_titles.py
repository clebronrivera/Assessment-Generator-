#!/usr/bin/env python3
"""
Update ORF passage titles to be short, descriptive, and focused on the main theme.
"""

import json
from pathlib import Path

# Define better titles based on the main theme of each passage
TITLE_UPDATES = {
    'sample_orf_gradeK_early.json': 'Sam Chases a Bug',
    'sample_orf_gradeK.json': 'Sam Plays with a Ball',
    'sample_orf_grade1.json': 'Ben Finds His Lost Ball',
    'sample_orf_grade2.json': 'Bella Helps a Bird',
    'sample_orf_grade3.json': 'Lucy and the Butterfly',
    'sample_orf_grade4.json': 'Lily Explores the Mountains',
    'sample_orf_grade5.json': 'Liam Rescues a Sparrow',
    'sample_orf_grade6.json': 'Luna the Fox Finds a Friend',
    'sample_orf_grade7.json': 'Sarah\'s Forest Adventure',
    'sample_orf_grade8.json': 'Lily\'s Bookstore Discovery',
}

def update_passage_title(filepath, new_title):
    """Update the passage_title in an ORF JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Update the title
    old_title = data['passage'].get('passage_title', 'No title')
    data['passage']['passage_title'] = new_title
    
    # Save the updated JSON
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return old_title, new_title

def main():
    """Update all ORF passage titles."""
    samples_dir = Path(__file__).parent / 'samples'
    
    print('📝 Updating ORF Passage Titles')
    print('=' * 80)
    
    updated_count = 0
    
    for filename, new_title in TITLE_UPDATES.items():
        filepath = samples_dir / filename
        
        if not filepath.exists():
            print(f'\n⚠️  File not found: {filename}')
            continue
        
        old_title, updated_title = update_passage_title(filepath, new_title)
        
        print(f'\n{filename}')
        print(f'  Old: {old_title}')
        print(f'  New: {updated_title}')
        
        updated_count += 1
    
    print(f'\n{"=" * 80}')
    print(f'✅ Updated {updated_count}/{len(TITLE_UPDATES)} titles')
    print(f'{"=" * 80}')

if __name__ == '__main__':
    main()
