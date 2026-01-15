#!/usr/bin/env python3
"""
Debug Script for PIB Generator - Sample 3 (Grade 5 Nonfiction)

This script tests the PIB generator in isolation to diagnose why it's failing
for Grade 5 nonfiction passages.

Usage:
    python3.11 debug_pib_sample3.py

Created: 2026-01-14
"""

import sys
import os
import json
from datetime import datetime

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Add project root to path
PROJECT_ROOT = '/Users/lebron/Desktop/Bank Creator'
sys.path.insert(0, PROJECT_ROOT)

from src.generators import create_qrm_generator, create_pib_generator
from src.utils import create_ai_client


def print_header(text):
    print("\n" + "=" * 80)
    print(text)
    print("=" * 80 + "\n")


def print_success(text):
    print(f"✓ {text}")


def print_error(text):
    print(f"✗ {text}")


def print_step(number, text):
    print(f"\n[{number}] {text}")


def debug_pib_generator():
    """Debug PIB generation for Grade 5 nonfiction"""
    
    print_header("PIB GENERATOR DEBUG - GRADE 5 NONFICTION")
    
    # Get API credentials
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print_error("No OpenAI API key found in .env")
        return False
    
    print_success("API key loaded")
    
    try:
        # Create generators
        ai_client = create_ai_client(api_key, 'openai')
        qrm_gen = create_qrm_generator(ai_client)
        pib_gen = create_pib_generator(ai_client)
        
        print_success("Generators created")
        
        # Step 1: Generate QRM
        print_step(1, "Generating QRM for Grade 5 Nonfiction...")
        qrm = qrm_gen.generate(grade="5", genre="nonfiction", band="late")
        print_success(f"QRM generated: {qrm.total_questions} questions")
        
        # Display QRM details
        print("\nQRM Details:")
        print(f"  Grade: {qrm.grade}")
        print(f"  Genre: {qrm.genre}")
        print(f"  Band: {qrm.band}")
        print(f"  Total Questions: {qrm.total_questions}")
        
        # Step 2: Generate PIB (with detailed error capture)
        print_step(2, "Generating PIB from QRM...")
        print("   This is where Sample 3 failed - watching for errors...")
        
        # Store the raw AI response for inspection
        original_complete = ai_client.complete
        last_response = None
        
        def capture_response(prompt):
            nonlocal last_response
            last_response = original_complete(prompt)
            return last_response
        
        ai_client.complete = capture_response
        
        try:
            pib = pib_gen.generate(qrm_result=qrm)
            print_success(f"PIB generated successfully: {pib.total_scenes} scenes")
            
            # Display PIB details
            print("\nPIB Details:")
            print(f"  Total Scenes: {pib.total_scenes}")
            print(f"  Word Count Target: {pib.target_word_count}")
            for i, scene in enumerate(pib.scenes[:3], 1):
                print(f"  Scene {i}: {scene.scene_type.value} - {scene.purpose}")
            
            print_header("✅ PIB GENERATION SUCCESSFUL!")
            print("The PIB generator worked this time. This suggests:")
            print("1. AI generation is stochastic (varies each run)")
            print("2. The generator itself is working correctly")
            print("3. Sample 3 just got unlucky with AI response")
            print("\nRecommendation: Retry Sample 3 - it should work now")
            
            return True
            
        except Exception as e:
            print_error(f"PIB generation failed: {str(e)}")
            
            # Analyze the error
            print_header("ERROR ANALYSIS")
            
            print("\n1. Error Type:")
            print(f"   {type(e).__name__}: {str(e)}")
            
            print("\n2. Last AI Response:")
            if last_response:
                print("   First 500 characters:")
                print("   " + "-" * 60)
                print("   " + last_response[:500])
                print("   " + "-" * 60)
                
                # Try to parse as JSON
                print("\n3. JSON Parsing Attempt:")
                try:
                    # Clean response
                    json_str = last_response.strip()
                    if "```json" in json_str:
                        json_str = json_str.split("```json")[1].split("```")[0].strip()
                    elif "```" in json_str:
                        json_str = json_str.split("```")[1].split("```")[0].strip()
                    
                    data = json.loads(json_str)
                    print("   ✓ Valid JSON structure")
                    print(f"   Keys present: {list(data.keys())}")
                    
                    # Check for 'scenes' key
                    if 'scenes' in data:
                        print(f"   ✓ 'scenes' key found with {len(data['scenes'])} items")
                    else:
                        print("   ✗ 'scenes' key MISSING")
                        print(f"   Available keys: {list(data.keys())}")
                        
                except json.JSONDecodeError as je:
                    print(f"   ✗ JSON parsing failed: {str(je)}")
                    print(f"   Error at position: {je.pos}")
                    if je.pos < len(json_str):
                        print(f"   Context: ...{json_str[max(0, je.pos-50):je.pos+50]}...")
                        
            else:
                print("   No response captured (error before AI call)")
            
            print_header("DIAGNOSIS")
            
            if 'scenes' in str(e).lower():
                print("Issue: AI response missing 'scenes' key")
                print("\nPossible causes:")
                print("1. AI returned different JSON structure")
                print("2. AI included extra text around JSON")
                print("3. JSON parsing removed 'scenes' key accidentally")
                print("\nSuggested fixes:")
                print("1. Add more explicit prompt instructions")
                print("2. Improve JSON cleaning/extraction")
                print("3. Add fallback to reconstruct 'scenes' key")
                print("4. Increase retry attempts for nonfiction")
            else:
                print(f"Issue: {str(e)}")
                print("\nThis is a different error than expected.")
                print("Review the error details above for clues.")
            
            return False
            
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    success = debug_pib_generator()
    
    if success:
        print("\n" + "=" * 80)
        print("NEXT STEP: Retry Sample 3")
        print("=" * 80)
        print("\nRun:")
        print("  python3.11 -c \"")
        print("  from generate_samples_simplified import generate_comprehension_sample_nonfiction")
        print("  import os")
        print("  from dotenv import load_dotenv")
        print("  load_dotenv()")
        print("  api_key = os.getenv('OPENAI_API_KEY')")
        print("  generate_comprehension_sample_nonfiction(api_key, 'openai')")
        print("  \"")
    else:
        print("\n" + "=" * 80)
        print("NEXT STEP: Fix PIB Generator")
        print("=" * 80)
        print("\nBased on the error analysis above, we need to:")
        print("1. Improve the PIB prompt for nonfiction")
        print("2. Add better JSON extraction/cleaning")
        print("3. Add retry logic with better error feedback")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
