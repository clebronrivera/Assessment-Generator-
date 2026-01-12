#!/usr/bin/env python3
"""
Example: Using the ORF Generator

This script demonstrates how to use the ORF Generator to create
oral reading fluency passages.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src import banks
from src.generators import create_orf_generator
from src.utils import create_ai_client


def example_1_without_ai():
    """
    Example 1: Get the prompt without calling AI
    Useful for testing templates or using external AI tools
    """
    print("="*70)
    print("EXAMPLE 1: Generate Prompt Only (No AI Call)")
    print("="*70)
    
    # Create generator
    generator = create_orf_generator(banks)
    
    # Generate (without AI client - returns prompt only)
    result = generator.generate(
        grade="2",
        band="early",
        topic_constraint="animals",
        structure="problem_solution"
    )
    
    print("\n[Generated Prompt]")
    print(result["prompt"][:500])  # Show first 500 chars
    print("...\n")
    
    print("[Specifications Used]")
    for key, value in result["specs"].items():
        if key != "bank_usage":
            print(f"  {key}: {value}")
    
    print("\n[Bank Usage]")
    for bank, usage in result["specs"]["bank_usage"].items():
        print(f"  {bank}: {usage}")


def example_2_with_mock_ai():
    """
    Example 2: Generate passage using Mock AI (no API key needed)
    Great for testing without API costs
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Generate Passage with Mock AI")
    print("="*70)
    
    # Create generator
    generator = create_orf_generator(banks)
    
    # Create mock AI client (no API key needed)
    ai_client = create_ai_client("fake_key", provider="mock")
    
    # Generate passage
    result = generator.generate(
        grade="2",
        band="early",
        ai_client=ai_client
    )
    
    print("\n[Generated Passage]")
    print(result["passage_text"])
    
    print("\n[Validation Results]")
    validation = result["validation"]
    print(f"  Valid: {validation['valid']}")
    if validation["errors"]:
        print(f"  Errors: {validation['errors']}")
    if validation["warnings"]:
        print(f"  Warnings: {validation['warnings']}")
    
    print("\n[Metadata]")
    print(f"  Grade: {result['grade']}")
    print(f"  Lexile Range: {result['lexile_range']}")
    print(f"  Target Word Count: {result['target_word_count']}")
    print(f"  Actual Word Count: {len(result['passage_text'].split())}")


def example_3_with_real_ai():
    """
    Example 3: Generate passage with real AI (requires API key)
    Uncomment and add your API key to test
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Generate with Real AI (Commented Out)")
    print("="*70)
    
    print("""
To use with real AI, uncomment this code and add your API key:

# For Anthropic Claude:
ai_client = create_ai_client("your-api-key-here", provider="anthropic")

# For OpenAI:
# ai_client = create_ai_client("your-api-key-here", provider="openai")

generator = create_orf_generator(banks)

result = generator.generate_with_retry(
    grade="3",
    band="late",
    ai_client=ai_client,
    max_retries=3
)

# Save to file
generator.save_output(result, "outputs/orf_grade3_late.json")
""")


def example_4_multiple_grades():
    """
    Example 4: Generate for multiple grades
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Generate for Multiple Grades (Mock AI)")
    print("="*70)
    
    generator = create_orf_generator(banks)
    ai_client = create_ai_client("fake", provider="mock")
    
    grades = ["1", "2", "3"]
    
    for grade in grades:
        print(f"\n--- Grade {grade} ---")
        result = generator.generate(
            grade=grade,
            band="early",
            ai_client=ai_client
        )
        
        word_count = len(result["passage_text"].split())
        print(f"  Word Count: {word_count}")
        print(f"  Valid: {result['validation']['valid']}")
        print(f"  First 100 chars: {result['passage_text'][:100]}...")


def example_5_show_all_specs():
    """
    Example 5: Show available specifications for all grades
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: Available Specifications for All Grades")
    print("="*70)
    
    print("\nORF Specifications by Grade:")
    print("-" * 70)
    
    for grade in ["1", "2", "3", "4", "5", "6", "7", "8"]:
        specs = banks.get_assessment_specs(grade, "orf", "early")
        print(f"\nGrade {grade}:")
        print(f"  Lexile: {specs['lexile_range']}")
        print(f"  Target Words: {specs['word_count']}")
        print(f"  Range: {specs['word_count_range']}")


def main():
    """Run all examples"""
    example_1_without_ai()
    example_2_with_mock_ai()
    example_3_with_real_ai()
    example_4_multiple_grades()
    example_5_show_all_specs()
    
    print("\n" + "="*70)
    print("All examples complete!")
    print("="*70)


if __name__ == "__main__":
    main()
