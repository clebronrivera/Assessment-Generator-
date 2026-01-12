"""
QRM Generator - Complete Examples

Demonstrates:
1. Basic QRM generation
2. QRM validation
3. Content requirement extraction
4. Preview of QRM→PIB→Passage workflow

Created: 2026-01-12
"""

from qrm_generator import create_qrm_generator, QuestionType, CognitiveDemand


class MockAI:
    """Mock AI client for demonstration"""
    
    def complete(self, prompt):
        """Return mock QRM based on grade"""
        
        # Detect grade from prompt
        if "Grade: 2" in prompt or "grade=\"2\"" in prompt:
            return self._grade_2_narrative()
        elif "Grade: 5" in prompt:
            return self._grade_5_nonfiction()
        else:
            return self._grade_2_narrative()
    
    def _grade_2_narrative(self):
        """Grade 2 narrative QRM"""
        return '''
{
  "questions": [
    {
      "question_number": 1,
      "question_type": "explicit",
      "cognitive_demand": "low",
      "evidence_location": "beginning",
      "content_requirement": "Passage must explicitly state the main character's name (Maya) and that she is starting second grade in the first two sentences",
      "distractor_guidance": "Use other character names from story; use similar names (Maria, Mia); use other grade levels"
    },
    {
      "question_number": 2,
      "question_type": "explicit",
      "cognitive_demand": "low",
      "evidence_location": "middle",
      "content_requirement": "Passage must describe a specific activity Maya did during recess: she organized a game of tag with new students",
      "distractor_guidance": "Use other recess activities mentioned; use activities at wrong time of day; use plausible school activities not mentioned"
    },
    {
      "question_number": 3,
      "question_type": "implicit",
      "cognitive_demand": "medium",
      "evidence_location": "throughout",
      "content_requirement": "Maya's actions must demonstrate kindness without explicitly stating she is kind: she invites lonely student to join, shares supplies, helps someone who fell",
      "distractor_guidance": "Use other positive traits that could fit (brave, smart, funny) but aren't as strongly supported by evidence"
    },
    {
      "question_number": 4,
      "question_type": "implicit",
      "cognitive_demand": "medium",
      "evidence_location": "end",
      "content_requirement": "Passage must show cause-effect: Because Maya included others, she made new friends and felt happy about starting school",
      "distractor_guidance": "Use other outcomes mentioned; use logical outcomes not in text; use outcomes with reversed causation"
    },
    {
      "question_number": 5,
      "question_type": "vocabulary",
      "cognitive_demand": "medium",
      "evidence_location": "middle",
      "content_requirement": "Include word 'hesitant' with clear context: 'The new student looked hesitant to join, standing alone and unsure'",
      "distractor_guidance": "Use words with similar prefix (hesitate, resistant); use words describing similar emotion (nervous, shy); use antonyms (confident, eager)"
    },
    {
      "question_number": 6,
      "question_type": "main_idea",
      "cognitive_demand": "high",
      "evidence_location": "throughout",
      "content_requirement": "Central theme: Being welcoming and inclusive helps everyone feel happy and makes school better. Must be supported by Maya's actions, others' responses, and outcome",
      "distractor_guidance": "Use details as main ideas (starting school is hard); use overly specific points (playing tag is fun); use unsupported themes (teachers are helpful)"
    }
  ],
  "required_content_elements": [
    "Character introduction: Maya, starting second grade",
    "School setting with specific locations (classroom, recess area)",
    "New students who need welcoming",
    "Maya's inclusive actions: inviting lonely student, sharing supplies, helping someone",
    "Recess activity: organizing game of tag",
    "Cause-effect: Maya's kindness leads to friendships and happiness",
    "Target vocabulary: 'hesitant' with strong context clues",
    "Clear central theme about kindness/inclusion"
  ],
  "required_vocabulary": ["hesitant"],
  "required_structure_elements": [
    "chronological sequence (beginning of day to end)",
    "cause-effect relationship (kindness → friendship)",
    "problem-solution (lonely students → Maya includes them)"
  ]
}
        '''
    
    def _grade_5_nonfiction(self):
        """Grade 5 nonfiction QRM - more complex"""
        return '''
{
  "questions": [
    {
      "question_number": 1,
      "question_type": "explicit",
      "cognitive_demand": "low",
      "evidence_location": "beginning",
      "content_requirement": "Passage must state that coral reefs cover less than 1% of ocean floor but support 25% of marine species",
      "distractor_guidance": "Use other percentages mentioned; swap the two statistics; use plausible but wrong percentages"
    },
    {
      "question_number": 2,
      "question_type": "vocabulary",
      "cognitive_demand": "medium",
      "evidence_location": "middle",
      "content_requirement": "Include 'symbiotic' with context: coral and algae relationship where both benefit - algae provide food, coral provides shelter",
      "distractor_guidance": "Use other relationship types (parasitic, competitive); use words with similar structure (synthetic, symbolic)"
    },
    {
      "question_number": 3,
      "question_type": "implicit",
      "cognitive_demand": "medium",
      "evidence_location": "middle",
      "content_requirement": "Describe multiple threats to reefs (warming, pollution, overfishing) so reader can infer they are endangered",
      "distractor_guidance": "Use individual threats as the inference; use unmentioned reasons; use effects rather than status"
    },
    {
      "question_number": 4,
      "question_type": "cause_effect",
      "cognitive_demand": "medium",
      "evidence_location": "throughout",
      "content_requirement": "Explain that rising water temperature causes coral bleaching (algae leave, coral turns white, eventually dies)",
      "distractor_guidance": "Reverse cause and effect; use related but different causes; use bleaching effects on other organisms"
    },
    {
      "question_number": 5,
      "question_type": "compare_contrast",
      "cognitive_demand": "high",
      "evidence_location": "middle",
      "content_requirement": "Compare coral polyps (small, numerous, build reef structure) vs. reef fish (mobile, diverse species, depend on reef)",
      "distractor_guidance": "Compare unrelated elements; use characteristics of only one; use similarities as contrasts"
    },
    {
      "question_number": 6,
      "question_type": "authors_purpose",
      "cognitive_demand": "high",
      "evidence_location": "throughout",
      "content_requirement": "Include urgency language about reef threats and mention of conservation efforts to show purpose is to inform and motivate action",
      "distractor_guidance": "Use partial purposes (inform only, entertain, describe); use unsupported purposes"
    }
  ],
  "required_content_elements": [
    "Statistic: coral reefs <1% ocean floor but support 25% marine species",
    "Definition of symbiotic relationship with coral-algae example",
    "Multiple reef threats: warming, pollution, overfishing",
    "Cause-effect: temperature rise → bleaching → coral death",
    "Coral polyp characteristics: small, numerous, build structure",
    "Reef fish characteristics: mobile, diverse, depend on reef",
    "Conservation efforts or calls to action",
    "Urgency language about threats"
  ],
  "required_vocabulary": ["symbiotic"],
  "required_structure_elements": [
    "cause-effect relationships",
    "compare-contrast structure",
    "problem-solution framing",
    "text features: headings for major sections"
  ]
}
        '''


def demonstrate_basic_generation():
    """Demonstrate basic QRM generation"""
    
    print("=" * 80)
    print("EXAMPLE 1: BASIC QRM GENERATION - GRADE 2 NARRATIVE")
    print("=" * 80)
    
    # Create generator with mock AI
    mock_ai = MockAI()
    generator = create_qrm_generator(mock_ai)
    
    # Generate QRM
    qrm = generator.generate(
        grade="2",
        genre="narrative",
        band="early",
        topic="making friends at school"
    )
    
    print(f"\n✓ QRM Generated Successfully")
    print(f"\nMETADATA:")
    print(f"  Form ID: {qrm.form_id}")
    print(f"  Grade: {qrm.grade} | Genre: {qrm.genre} | Band: {qrm.band}")
    print(f"  Total Questions: {qrm.total_questions}")
    print(f"  Generated: {qrm.generated_at}")
    
    print(f"\nDISTRIBUTIONS (from Bank 4):")
    print(f"  Question Types: {qrm.type_distribution}")
    print(f"  Cognitive Levels: {qrm.cognitive_distribution}")
    print(f"  Evidence Locations: {qrm.evidence_distribution}")
    
    print(f"\nREQUIRED CONTENT FOR PASSAGE:")
    for i, element in enumerate(qrm.required_content_elements, 1):
        print(f"  {i}. {element}")
    
    print(f"\nVOCABULARY TARGETS:")
    for word in qrm.required_vocabulary:
        print(f"  - {word}")
    
    print(f"\nSTRUCTURE REQUIREMENTS:")
    for structure in qrm.required_structure_elements:
        print(f"  - {structure}")
    
    return qrm


def demonstrate_question_details(qrm):
    """Show detailed view of each question"""
    
    print("\n" + "=" * 80)
    print("EXAMPLE 2: DETAILED QUESTION SPECIFICATIONS")
    print("=" * 80)
    
    for q in qrm.questions:
        print(f"\n{'─' * 80}")
        print(f"QUESTION {q.question_number}")
        print(f"{'─' * 80}")
        print(f"Type: {q.question_type.value.upper()}")
        print(f"Cognitive Demand: {q.cognitive_demand.value.upper()}")
        print(f"Evidence Location: {q.evidence_location}")
        print(f"\nWhat Passage MUST Contain:")
        print(f"  {q.content_requirement}")
        print(f"\nDistractor Strategy:")
        print(f"  {q.distractor_guidance}")


def demonstrate_validation():
    """Show QRM validation against Bank 4"""
    
    print("\n" + "=" * 80)
    print("EXAMPLE 3: QRM VALIDATION AGAINST BANK 4")
    print("=" * 80)
    
    mock_ai = MockAI()
    generator = create_qrm_generator(mock_ai)
    
    print("\nGenerating QRM for Grade 2...")
    qrm = generator.generate(
        grade="2",
        genre="narrative",
        band="early"
    )
    
    print("\n✓ Validation Passed!")
    print("\nBank 4 Requirements vs. QRM Output:")
    print(f"  Total Questions: 6 required → {qrm.total_questions} generated ✓")
    print(f"  Explicit: 2 required → {qrm.type_distribution.get('explicit', 0)} generated ✓")
    print(f"  Implicit: 2 required → {qrm.type_distribution.get('implicit', 0)} generated ✓")
    print(f"  Vocabulary: 1 required → {qrm.type_distribution.get('vocabulary', 0)} generated ✓")
    print(f"  Main Idea: 1 required → {qrm.type_distribution.get('main_idea', 0)} generated ✓")
    print(f"  Low Demand: 2 required → {qrm.cognitive_distribution.get('low', 0)} generated ✓")
    print(f"  Medium Demand: 3 required → {qrm.cognitive_distribution.get('medium', 0)} generated ✓")
    print(f"  High Demand: 1 required → {qrm.cognitive_distribution.get('high', 0)} generated ✓")


def demonstrate_workflow_preview():
    """Show how QRM feeds into next steps"""
    
    print("\n" + "=" * 80)
    print("EXAMPLE 4: QRM → PIB → PASSAGE WORKFLOW (PREVIEW)")
    print("=" * 80)
    
    mock_ai = MockAI()
    qrm_gen = create_qrm_generator(mock_ai)
    
    # Step 1: Generate QRM
    print("\n[STEP 1: QRM - Question Planning]")
    print("─" * 80)
    qrm = qrm_gen.generate(
        grade="2",
        genre="narrative",
        band="early",
        topic="overcoming challenges"
    )
    print(f"✓ QRM generated with {qrm.total_questions} questions")
    print(f"✓ Required content elements: {len(qrm.required_content_elements)}")
    
    # Step 2: PIB (to be built)
    print("\n[STEP 2: PIB - Passage Content Requirements]")
    print("─" * 80)
    print("(PIB Generator not yet built)")
    print("\nPIB will convert QRM requirements into:")
    print("  - Scene descriptions")
    print("  - Character details")
    print("  - Plot elements")
    print("  - Dialogue examples")
    print("  - Vocabulary placement")
    print("\nExample PIB element from QRM Q3:")
    print(f"  QRM Q3: {qrm.questions[2].content_requirement}")
    print("  PIB conversion:")
    print("    → Scene 1: Maya notices lonely student at recess")
    print("    → Action: Maya approaches and invites student to play")
    print("    → Scene 2: Maya shares pencils with student who forgot supplies")
    print("    → Scene 3: Maya helps student who tripped, stays to comfort them")
    print("    → Result: Show student smiling and joining group")
    
    # Step 3: Passage (to be built)
    print("\n[STEP 3: PASSAGE - Final Text Generation]")
    print("─" * 80)
    print("(Passage Generator not yet built)")
    print("\nPassage will be written using PIB requirements:")
    print("  - Include all scenes from PIB")
    print("  - Use vocabulary words in context")
    print("  - Follow structure requirements")
    print("  - Match Lexile and word count from Banks 1 & 3")
    print("  - Ensure all questions are answerable")
    
    print("\n[RESULT: Complete Assessment]")
    print("─" * 80)
    print("✓ Passage with embedded content for all questions")
    print("✓ Questions that are guaranteed answerable")
    print("✓ Answer key with evidence locations")
    print("✓ No guesswork - everything planned before writing")


def demonstrate_grade_comparison():
    """Compare QRMs across grades"""
    
    print("\n" + "=" * 80)
    print("EXAMPLE 5: GRADE COMPARISON - COMPLEXITY PROGRESSION")
    print("=" * 80)
    
    mock_ai = MockAI()
    generator = create_qrm_generator(mock_ai)
    
    # Grade 2
    print("\nGRADE 2 - Narrative")
    print("─" * 80)
    qrm_2 = generator.generate(grade="2", genre="narrative", band="early")
    print(f"Questions: {qrm_2.total_questions}")
    print(f"Question Types: {list(qrm_2.type_distribution.keys())}")
    print(f"Complexity: {qrm_2.cognitive_distribution}")
    print("Focus: Character identification, simple cause-effect, basic inference")
    
    # Grade 5
    print("\nGRADE 5 - Nonfiction")
    print("─" * 80)
    qrm_5 = generator.generate(grade="5", genre="nonfiction", band="late")
    print(f"Questions: {qrm_5.total_questions}")
    print(f"Question Types: {list(qrm_5.type_distribution.keys())}")
    print(f"Complexity: {qrm_5.cognitive_distribution}")
    print("Focus: Analysis, compare-contrast, author's purpose, multiple causes")
    
    print("\nCOMPLEXITY PROGRESSION:")
    print("  Grade 2: Mostly explicit, simple inference, 1 high-complexity question")
    print("  Grade 5: More analysis, multiple relationships, author evaluation")


def demonstrate_json_export():
    """Show JSON export for storage/transmission"""
    
    print("\n" + "=" * 80)
    print("EXAMPLE 6: JSON EXPORT FOR STORAGE")
    print("=" * 80)
    
    mock_ai = MockAI()
    generator = create_qrm_generator(mock_ai)
    
    qrm = generator.generate(grade="2", genre="narrative", band="early")
    
    import json
    qrm_json = json.dumps(qrm.to_dict(), indent=2)
    
    print("\nQRM exported to JSON:")
    print("─" * 80)
    print(qrm_json[:600] + "\n... (truncated)")
    print("─" * 80)
    print(f"\nFull JSON size: {len(qrm_json)} characters")
    print("\nUse cases:")
    print("  - Store in database for later use")
    print("  - Pass to PIB generator")
    print("  - Track QRM versions")
    print("  - Audit question planning process")


if __name__ == "__main__":
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "QRM GENERATOR - COMPLETE EXAMPLES" + " " * 25 + "║")
    print("╚" + "═" * 78 + "╝")
    
    # Run all demonstrations
    qrm = demonstrate_basic_generation()
    demonstrate_question_details(qrm)
    demonstrate_validation()
    demonstrate_workflow_preview()
    demonstrate_grade_comparison()
    demonstrate_json_export()
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("""
The QRM Generator is the foundation of quality comprehension assessments:

✓ Plans questions BEFORE passage is written
✓ Ensures every question will be answerable
✓ Enforces Bank 4 specifications (distributions, complexity)
✓ Provides detailed content requirements for passage
✓ Feeds directly into PIB Generator (next step)

NEXT STEPS:
1. Build PIB Generator (uses QRM output)
2. Build Comprehension Passage Generator (uses QRM + PIB)
3. Build Question Generator (uses QRM to create actual questions)
4. Test complete workflow end-to-end

Phase 2B Status:
  ✓ QRM Generator - Complete
  ⏳ PIB Generator - Next
  ⏳ Passage Generator - After PIB
    """)
