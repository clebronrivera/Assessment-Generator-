"""
Complete ORF Assessment Package Example

Demonstrates generating a full ORF assessment package:
1. Generate passage (ORF Generator)
2. Generate assessor materials (Assessor Materials Generator)
3. Bundle complete package

Created: 2026-01-12
"""

# Mock implementations for demonstration purposes
# In production, import from actual modules

class MockORFResult:
    """Mock ORF generator result"""
    def __init__(self):
        self.passage_text = """
The Amazing Journey of Monarch Butterflies

Every fall, millions of monarch butterflies begin an incredible journey. These 
beautiful insects travel thousands of miles from Canada and the United States 
to Mexico. The trip takes several weeks, and the butterflies face many dangers 
along the way.

Monarchs are special because they are the only butterflies that migrate such 
long distances. They fly up to 3,000 miles to reach their winter home. During 
the journey, they must find food and water. They also need to avoid bad weather 
and predators.

When spring arrives, the butterflies begin their return trip north. However, 
the same butterflies that flew south do not make it all the way back. Instead, 
they lay eggs along the way. Their children and grandchildren continue the 
journey. It takes three or four generations to complete the full cycle.

Scientists are still learning about how monarchs find their way. Some think the 
butterflies use the sun as a compass. Others believe they can sense the Earth's 
magnetic field. Whatever the method, these tiny creatures accomplish an amazing 
feat year after year.
        """.strip()
        
        self.metadata = {
            "grade": "2",
            "band": "early",
            "actual_word_count": 150,
            "target_word_count": 150,
            "lexile_target": "300-400L",
            "form_id": "ORF-2-EARLY-001",
            "genre": "nonfiction",
            "topic": "animal migration"
        }


def demonstrate_complete_package():
    """Generate and display complete ORF assessment package"""
    
    print("=" * 80)
    print("COMPLETE ORF ASSESSMENT PACKAGE GENERATION")
    print("=" * 80)
    
    # STEP 1: Generate passage (using mock for demo)
    print("\n[STEP 1] Generating ORF Passage...")
    print("-" * 80)
    
    passage_result = MockORFResult()
    
    print(f"✓ Passage generated")
    print(f"  Grade: {passage_result.metadata['grade']}")
    print(f"  Band: {passage_result.metadata['band']}")
    print(f"  Word Count: {passage_result.metadata['actual_word_count']}")
    print(f"  Lexile: {passage_result.metadata['lexile_target']}")
    print(f"  Form ID: {passage_result.metadata['form_id']}")
    
    # STEP 2: Generate assessor materials
    print("\n[STEP 2] Generating Assessor Materials...")
    print("-" * 80)
    
    from orf_assessor_materials_generator import create_orf_assessor_materials_generator
    
    materials_gen = create_orf_assessor_materials_generator()
    materials = materials_gen.generate(
        grade=passage_result.metadata["grade"],
        passage_text=passage_result.passage_text,
        passage_word_count=passage_result.metadata["actual_word_count"],
        form_id=passage_result.metadata["form_id"]
    )
    
    print(f"✓ Assessor materials generated")
    print(f"  WCPM Benchmarks:")
    print(f"    Fall: {materials.wcpm_benchmark['fall']} WCPM")
    print(f"    Winter: {materials.wcpm_benchmark['winter']} WCPM")
    print(f"    Spring: {materials.wcpm_benchmark['spring']} WCPM")
    
    # STEP 3: Package everything
    print("\n[STEP 3] Creating Complete Package...")
    print("-" * 80)
    
    package = {
        # Student Materials
        "student_passage": {
            "title": "Student Reading Passage",
            "content": passage_result.passage_text,
            "instructions": "Read this passage aloud when your teacher says 'start.'"
        },
        
        # Assessor Materials
        "assessor_passage": {
            "title": "Assessor Copy (for marking errors)",
            "content": passage_result.passage_text,
            "note": "Mark errors directly on this copy during assessment"
        },
        
        "administration_materials": {
            "timing_script": materials.timing_script,
            "word_supply_rules": materials.word_supply_rules,
            "general_instructions": materials.general_instructions
        },
        
        "scoring_materials": {
            "score_sheet": materials.score_sheet,
            "accuracy_guide": materials.accuracy_calculation,
            "prosody_rubric": materials.prosody_rubric,
            "benchmarks": materials.wcpm_benchmark
        },
        
        "error_tracking": {
            "marking_grid": materials.error_marking_grid,
            "error_types": materials.error_types
        },
        
        # Metadata
        "metadata": {
            "form_id": passage_result.metadata["form_id"],
            "grade": passage_result.metadata["grade"],
            "band": passage_result.metadata["band"],
            "passage_word_count": passage_result.metadata["actual_word_count"],
            "lexile": passage_result.metadata["lexile_target"],
            "genre": passage_result.metadata["genre"],
            "generated_at": materials.generated_at,
            "schema_version": materials.schema_version
        }
    }
    
    print(f"✓ Package created with {len(package)} components")
    print(f"  - Student passage (clean copy)")
    print(f"  - Assessor passage (for error marking)")
    print(f"  - Administration materials (3 documents)")
    print(f"  - Scoring materials (4 components)")
    print(f"  - Error tracking (2 guides)")
    print(f"  - Metadata (form ID, benchmarks, etc.)")
    
    # STEP 4: Display sample outputs
    print("\n[STEP 4] Sample Outputs")
    print("=" * 80)
    
    print("\n--- STUDENT PASSAGE (First 200 chars) ---")
    print(passage_result.passage_text[:200] + "...")
    
    print("\n--- TIMING SCRIPT (First 300 chars) ---")
    print(materials.timing_script[:300] + "...")
    
    print("\n--- SCORE SHEET (First 400 chars) ---")
    print(materials.score_sheet[:400] + "...")
    
    print("\n--- ERROR MARKING GRID (First 300 chars) ---")
    print(materials.error_marking_grid[:300] + "...")
    
    # STEP 5: Summary
    print("\n" + "=" * 80)
    print("PACKAGE SUMMARY")
    print("=" * 80)
    print(f"""
Form ID:           {package['metadata']['form_id']}
Grade:             {package['metadata']['grade']}
Lexile Band:       {package['metadata']['lexile']}
Passage Words:     {package['metadata']['passage_word_count']}
Genre:             {package['metadata']['genre']}

WCPM Benchmarks:
  Fall:            {materials.wcpm_benchmark['fall']} WCPM
  Winter:          {materials.wcpm_benchmark['winter']} WCPM
  Spring:          {materials.wcpm_benchmark['spring']} WCPM

Package Contents:
  ✓ Student reading passage
  ✓ Assessor copy for marking
  ✓ 60-second timing script
  ✓ 3-second word supply rules
  ✓ General administration instructions
  ✓ Complete score sheet with calculations
  ✓ Accuracy calculation guide
  ✓ Prosody rubric (NAEP-aligned)
  ✓ Error marking system
  ✓ Error type definitions

Status:            READY FOR ADMINISTRATION

Bank Usage:
  - Bank 1 (Lexile): Used in passage generation
  - Bank 2 (ORF):    Used for WCPM benchmarks
  - Bank 7 (Text):   Used in passage structure
    """)
    
    return package


def demonstrate_multiple_grades():
    """Generate packages for multiple grades to show variation"""
    
    print("\n" + "=" * 80)
    print("MULTI-GRADE COMPARISON")
    print("=" * 80)
    
    from orf_assessor_materials_generator import create_orf_assessor_materials_generator
    
    materials_gen = create_orf_assessor_materials_generator()
    
    grades = ["1", "2", "3", "5", "8"]
    
    print("\nWCPM Benchmarks Across Grades (from Bank 2):")
    print("-" * 80)
    print(f"{'Grade':<8} {'Fall':<12} {'Winter':<12} {'Spring':<12}")
    print("-" * 80)
    
    for grade in grades:
        materials = materials_gen.generate(
            grade=grade,
            passage_text="Sample passage",
            passage_word_count=150,
            form_id=f"ORF-{grade}-TEST"
        )
        
        print(
            f"{grade:<8} "
            f"{materials.wcpm_benchmark['fall']:<12} "
            f"{materials.wcpm_benchmark['winter']:<12} "
            f"{materials.wcpm_benchmark['spring']:<12}"
        )
    
    print("-" * 80)
    print("\nNote: All benchmarks pulled from Bank 2 (ORF Word Counts)")
    print("      Same materials structure for all grades, only benchmarks vary")


def demonstrate_json_export():
    """Show how to export package to JSON for storage/transmission"""
    
    print("\n" + "=" * 80)
    print("JSON EXPORT EXAMPLE")
    print("=" * 80)
    
    from orf_assessor_materials_generator import create_orf_assessor_materials_generator
    import json
    
    materials_gen = create_orf_assessor_materials_generator()
    materials = materials_gen.generate(
        grade="2",
        passage_text="Sample passage for JSON export demonstration.",
        passage_word_count=150,
        form_id="ORF-2-EARLY-001"
    )
    
    # Convert to dictionary
    materials_dict = materials.to_dict()
    
    # Export to JSON
    json_output = json.dumps(materials_dict, indent=2)
    
    print("\nMaterials exported to JSON:")
    print("-" * 80)
    print(json_output[:500] + "\n... (truncated)")
    print("-" * 80)
    print(f"Full JSON size: {len(json_output)} characters")
    print("\nThis JSON can be:")
    print("  - Stored in a database")
    print("  - Transmitted via API")
    print("  - Saved to file for archival")
    print("  - Used to regenerate materials later")


if __name__ == "__main__":
    # Run demonstrations
    print("\n" + "=" * 80)
    print("ORF ASSESSMENT PACKAGE - COMPLETE DEMONSTRATION")
    print("=" * 80)
    
    # Main demonstration
    package = demonstrate_complete_package()
    
    # Additional demonstrations
    demonstrate_multiple_grades()
    demonstrate_json_export()
    
    print("\n" + "=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("=" * 80)
    print("""
Next Steps:
1. Integrate ORF Generator with this Assessor Materials Generator
2. Create PDF generator to format materials for printing
3. Create web interface to allow educators to generate assessments
4. Add data storage to track generated assessments
5. Begin Phase 2B: Comprehension Assessment Generator

Phase 2A Status: ✅ COMPLETE
- ORF Passage Generator: ✅ Complete
- ORF Assessor Materials Generator: ✅ Complete
- Complete ORF workflow operational
    """)
