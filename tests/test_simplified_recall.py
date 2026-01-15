#!/usr/bin/env python3
"""
Test Script for Simplified Recall Scoring Generator

Tests the new simplified recall approach with a mock passage.
Validates that:
1. JSON structure is simple and parseable
2. Scoring guide is generated correctly
3. Validation passes
4. Output is practical and usable

Created: 2026-01-14
"""

import sys
from dataclasses import dataclass
from datetime import datetime

# Add src directory to path
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.generators.simplified_recall_scoring_generator import (
    SimplifiedRecallScoringGenerator,
    SimplifiedRecallGuide,
    SimplifiedSentenceScoring
)


@dataclass
class MockPassageResult:
    """Mock passage result for testing"""
    passage_text: str
    passage_title: str
    grade: str
    genre: str
    form_id: str


class MockAIClient:
    """Mock AI client that returns valid simplified recall JSON"""
    
    def complete(self, prompt: str) -> str:
        """Return mock simplified recall JSON"""
        return """{
  "sentences": [
    {
      "sentence_number": 1,
      "sentence_text": "Maya was excited for second grade.",
      "character_name": "Maya",
      "key_detail": "excited for second grade",
      "scoring_note": "2 pts: Maya + second grade | 1 pt: either | 0 pts: neither"
    },
    {
      "sentence_number": 2,
      "sentence_text": "She saw a new boy named Jordan sitting alone.",
      "character_name": "Jordan",
      "key_detail": "sitting alone",
      "scoring_note": "2 pts: Jordan + alone | 1 pt: either | 0 pts: neither"
    },
    {
      "sentence_number": 3,
      "sentence_text": "Maya invited him to play tag.",
      "character_name": "Maya",
      "key_detail": "invited to play tag",
      "scoring_note": "2 pts: Maya inviting + tag | 1 pt: either | 0 pts: neither"
    },
    {
      "sentence_number": 4,
      "sentence_text": "Jordan smiled and joined the game.",
      "character_name": "Jordan",
      "key_detail": "joined the game",
      "scoring_note": "2 pts: Jordan + joined | 1 pt: either | 0 pts: neither"
    },
    {
      "sentence_number": 5,
      "sentence_text": "They became friends and played together every day.",
      "character_name": "They (Maya and Jordan)",
      "key_detail": "became friends",
      "scoring_note": "2 pts: friendship + regular play | 1 pt: either | 0 pts: neither"
    }
  ],
  "general_instructions": "For each sentence, award 2 points if student recalls BOTH the character and key detail, 1 point for either one, 0 points for neither. Allow paraphrasing."
}"""


def test_simplified_recall_generator():
    """Test the simplified recall scoring generator"""
    
    print("\n" + "=" * 80)
    print("TESTING SIMPLIFIED RECALL SCORING GENERATOR")
    print("=" * 80 + "\n")
    
    # Create mock passage
    mock_passage = MockPassageResult(
        passage_text="""Maya was excited for second grade. She saw a new boy named Jordan sitting alone. Maya invited him to play tag. Jordan smiled and joined the game. They became friends and played together every day.""",
        passage_title="Making Friends",
        grade="2",
        genre="narrative",
        form_id="COMP-G2-NARRATIVE-001"
    )
    
    print("Mock Passage:")
    print(f"  Title: {mock_passage.passage_title}")
    print(f"  Grade: {mock_passage.grade}")
    print(f"  Sentences: 5")
    print()
    
    # Create generator with mock AI
    mock_ai = MockAIClient()
    generator = SimplifiedRecallScoringGenerator(ai_client=mock_ai)
    
    # Generate scoring guide
    print("Generating simplified recall scoring guide...")
    try:
        scoring_guide = generator.generate(passage_result=mock_passage)
        print("✓ Generation successful!\n")
        
        # Display results
        print("=" * 80)
        print("GENERATED SCORING GUIDE")
        print("=" * 80 + "\n")
        
        print(f"Total Sentences: {scoring_guide.total_sentences}")
        print(f"Max Total Points: {scoring_guide.max_total_points}")
        print(f"Form ID: {scoring_guide.form_id}")
        print()
        
        print("General Instructions:")
        print(f"  {scoring_guide.general_instructions}")
        print()
        
        print("Sentence-by-Sentence Scoring:")
        print("-" * 80)
        
        for sent in scoring_guide.sentences:
            print(f"\nSentence {sent.sentence_number}: \"{sent.sentence_text}\"")
            print(f"  Character: {sent.character_name}")
            print(f"  Key Detail: {sent.key_detail}")
            print(f"  Max Points: {sent.max_points}")
            print(f"  Scoring: {sent.scoring_note}")
        
        print("\n" + "=" * 80)
        print("VALIDATION CHECKS")
        print("=" * 80 + "\n")
        
        # Validation checks
        checks = []
        
        # Check 1: Sentence count
        if scoring_guide.total_sentences == 5:
            checks.append(("✓", "Sentence count matches (5)"))
        else:
            checks.append(("✗", f"Sentence count mismatch: {scoring_guide.total_sentences} != 5"))
        
        # Check 2: Max points calculation
        if scoring_guide.max_total_points == 10:
            checks.append(("✓", "Max points correct (10 = 5 sentences × 2 points)"))
        else:
            checks.append(("✗", f"Max points incorrect: {scoring_guide.max_total_points} != 10"))
        
        # Check 3: All sentences have scoring
        if len(scoring_guide.sentences) == 5:
            checks.append(("✓", "All sentences have scoring data"))
        else:
            checks.append(("✗", f"Missing scoring for some sentences"))
        
        # Check 4: All sentences have character names
        all_have_characters = all(s.character_name for s in scoring_guide.sentences)
        if all_have_characters:
            checks.append(("✓", "All sentences have character names"))
        else:
            checks.append(("✗", "Some sentences missing character names"))
        
        # Check 5: All sentences have key details
        all_have_details = all(s.key_detail for s in scoring_guide.sentences)
        if all_have_details:
            checks.append(("✓", "All sentences have key details"))
        else:
            checks.append(("✗", "Some sentences missing key details"))
        
        # Check 6: All max_points are 2
        all_2pts = all(s.max_points == 2 for s in scoring_guide.sentences)
        if all_2pts:
            checks.append(("✓", "All sentences worth 2 points"))
        else:
            checks.append(("✗", "Some sentences have incorrect max_points"))
        
        # Display checks
        for symbol, message in checks:
            print(f"{symbol} {message}")
        
        # Overall result
        all_passed = all(symbol == "✓" for symbol, _ in checks)
        
        print("\n" + "=" * 80)
        if all_passed:
            print("✅ ALL TESTS PASSED!")
            print("=" * 80 + "\n")
            print("The simplified recall scoring generator is working correctly.")
            print("\nKey Benefits:")
            print("  • Simple JSON structure (easy for AI to generate)")
            print("  • Clear character + detail approach")
            print("  • Practical for real assessors")
            print("  • Reliable and robust")
            return True
        else:
            print("❌ SOME TESTS FAILED")
            print("=" * 80 + "\n")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_simplified_recall_generator()
    sys.exit(0 if success else 1)
