"""
PIB Generator - Complete Workflow Examples

Demonstrates:
1. QRM → PIB conversion
2. Scene-by-scene breakdown
3. Question coverage verification
4. Character specification
5. Ready-for-passage-writing blueprint

Created: 2026-01-12
"""

from pib_generator import create_pib_generator
from qrm_generator import create_qrm_generator


class MockAI:
    """Mock AI for consistent demonstrations"""
    
    def complete(self, prompt):
        if "Question Requirement Matrix" in prompt:
            return self._qrm_response()
        else:
            return self._pib_response()
    
    def _qrm_response(self):
        return '''
{
  "questions": [
    {"question_number": 1, "question_type": "explicit", "cognitive_demand": "low", "evidence_location": "beginning", "content_requirement": "Passage must state Maya's name and that she is starting second grade", "distractor_guidance": "Use other names or grades"},
    {"question_number": 2, "question_type": "explicit", "cognitive_demand": "low", "evidence_location": "middle", "content_requirement": "Passage must describe specific activity at recess: tag game", "distractor_guidance": "Use other activities"},
    {"question_number": 3, "question_type": "implicit", "cognitive_demand": "medium", "evidence_location": "throughout", "content_requirement": "Maya's actions show kindness without saying 'kind'", "distractor_guidance": "Use other traits"},
    {"question_number": 4, "question_type": "implicit", "cognitive_demand": "medium", "evidence_location": "end", "content_requirement": "Show cause-effect: kindness leads to friendship and happiness", "distractor_guidance": "Use wrong outcomes"},
    {"question_number": 5, "question_type": "vocabulary", "cognitive_demand": "medium", "evidence_location": "middle", "content_requirement": "Use 'hesitant' with strong context clues", "distractor_guidance": "Use similar words"},
    {"question_number": 6, "question_type": "main_idea", "cognitive_demand": "high", "evidence_location": "throughout", "content_requirement": "Central theme: being welcoming makes everyone happy", "distractor_guidance": "Use details as main ideas"}
  ],
  "required_content_elements": ["Maya intro", "School setting", "Kind actions", "New friendships"],
  "required_vocabulary": ["hesitant"],
  "required_structure_elements": ["chronological", "cause-effect"]
}
        '''
    
    def _pib_response(self):
        return '''
{
  "scenes": [
    {
      "scene_number": 1,
      "scene_type": "opening",
      "location_in_passage": "beginning",
      "purpose": "Introduce Maya and establish school setting",
      "content_description": "Maya Rodriguez arrives at Lincoln Elementary on the first day of second grade. She carries her new backpack and feels a mix of excitement and nervousness. The school playground is visible with other students arriving.",
      "required_details": [
        "State Maya's full name clearly",
        "Specify she is starting second grade",
        "Describe school building and playground",
        "Show her emotional state (excited/nervous mix)"
      ],
      "supports_questions": [1],
      "vocabulary_placement": []
    },
    {
      "scene_number": 2,
      "scene_type": "action",
      "location_in_passage": "middle",
      "purpose": "Introduce Jordan and use target vocabulary",
      "content_description": "In the classroom during morning work, Maya notices a new student, Jordan, sitting alone. Jordan looks hesitant to join others, standing at the edge of a group with an uncertain expression, glancing at the other students but not moving closer.",
      "required_details": [
        "Introduce Jordan as new student",
        "Use word 'hesitant' with visual and behavioral context",
        "Describe Jordan's body language: standing at edge, uncertain expression",
        "Show Jordan observing but not joining"
      ],
      "supports_questions": [3, 5],
      "vocabulary_placement": ["hesitant"]
    },
    {
      "scene_number": 3,
      "scene_type": "action",
      "location_in_passage": "middle",
      "purpose": "Show first kind action - recess inclusion",
      "content_description": "At recess, Maya organizes a game of tag with her friends. She notices Jordan sitting alone on a bench. Maya runs over to Jordan and invites them to join the game. Jordan hesitates briefly, then smiles and follows Maya to the group.",
      "required_details": [
        "Specify the game is tag (for Q2)",
        "Show Maya actively organizing the game",
        "Show Maya noticing Jordan alone",
        "Show Maya's invitation action",
        "Show Jordan's response: accepts and joins"
      ],
      "supports_questions": [2, 3],
      "vocabulary_placement": []
    },
    {
      "scene_number": 4,
      "scene_type": "action",
      "location_in_passage": "middle",
      "purpose": "Show second kind action - sharing supplies",
      "content_description": "Back in the classroom for afternoon art project, Jordan realizes they forgot their colored pencils. Before Jordan has to ask, Maya quietly places her extra set of colored pencils on Jordan's desk with a friendly smile.",
      "required_details": [
        "Show Jordan's problem: forgot supplies",
        "Show Maya noticing without being asked",
        "Show Maya's generosity: gives her extra pencils",
        "Show it's done kindly (smile, not making Jordan feel bad)"
      ],
      "supports_questions": [3],
      "vocabulary_placement": []
    },
    {
      "scene_number": 5,
      "scene_type": "action",
      "location_in_passage": "middle",
      "purpose": "Show third kind action - helping someone in need",
      "content_description": "While walking to the buses, a younger student trips and drops their books. Maya stops immediately to help. She picks up the scattered books, checks if the student is okay, and waits with them until they feel better.",
      "required_details": [
        "Show someone needing help (tripped student)",
        "Show Maya's immediate response",
        "Show multiple helpful actions: picks up books, checks on student, stays with them",
        "Demonstrate caring behavior"
      ],
      "supports_questions": [3],
      "vocabulary_placement": []
    },
    {
      "scene_number": 6,
      "scene_type": "conclusion",
      "location_in_passage": "end",
      "purpose": "Show positive outcomes of Maya's kindness",
      "content_description": "At the end of the day, Maya and Jordan walk to the buses together, talking and laughing. Jordan thanks Maya for making the first day so great. Maya feels happy knowing she helped someone feel welcome. She realizes that including others made her own day better too.",
      "required_details": [
        "Show new friendship formed between Maya and Jordan",
        "Show Jordan's gratitude explicitly",
        "Show Maya's happiness as result of her actions",
        "Make cause-effect clear: her kindness led to friendship and joy",
        "Show mutual benefit: Jordan felt welcome, Maya felt fulfilled"
      ],
      "supports_questions": [4, 6],
      "vocabulary_placement": []
    }
  ],
  "characters": [
    {
      "name": "Maya Rodriguez",
      "role": "main",
      "key_traits": ["kind", "observant", "inclusive", "proactive"],
      "actions_to_show": [
        "Organizes inclusive tag game",
        "Invites Jordan to join without hesitation",
        "Shares colored pencils without being asked",
        "Helps younger student who tripped",
        "Makes Jordan feel welcome throughout day"
      ],
      "supports_questions": [1, 2, 3, 4, 6]
    },
    {
      "name": "Jordan",
      "role": "supporting",
      "key_traits": ["new", "shy initially", "grateful", "friendly once welcomed"],
      "actions_to_show": [
        "Stands hesitantly at first (visual for vocabulary)",
        "Accepts Maya's invitation to play",
        "Receives help graciously",
        "Thanks Maya explicitly at end",
        "Becomes friend by end of day"
      ],
      "supports_questions": [3, 4, 5, 6]
    },
    {
      "name": "Younger student",
      "role": "minor",
      "key_traits": ["needs help"],
      "actions_to_show": ["Trips and drops books", "Accepts Maya's help"],
      "supports_questions": [3]
    }
  ],
  "opening_hook": "Maya Rodriguez stood at the entrance of Lincoln Elementary, her brand-new second-grade backpack on her shoulders",
  "central_conflict_or_topic": "Maya navigates her first day of second grade by noticing students who need a friend and actively including them",
  "resolution_or_conclusion": "By the end of the day, Maya has made a new friend and learned that being kind and welcoming makes everyone happier, including herself",
  "vocabulary_contexts": {
    "hesitant": "Use in Scene 2 when describing Jordan. Full context: Jordan looks hesitant to join the other students - standing at the edge of the group with an uncertain expression, glancing at them but not moving closer. This provides both visual (standing at edge, uncertain expression) and behavioral (glancing but not joining) context clues."
  },
  "text_structure": "chronological",
  "organizational_features": [],
  "question_coverage_map": {
    "1": [1],
    "2": [3],
    "3": [2, 3, 4, 5],
    "4": [6],
    "5": [2],
    "6": [6]
  }
}
        '''


def demonstrate_qrm_to_pib():
    """Show complete QRM to PIB conversion"""
    
    print("=" * 80)
    print("EXAMPLE 1: QRM → PIB CONVERSION")
    print("=" * 80)
    
    mock_ai = MockAI()
    qrm_gen = create_qrm_generator(mock_ai)
    pib_gen = create_pib_generator(mock_ai)
    
    # Step 1: Generate QRM
    print("\n[STEP 1: QRM - Question Planning]")
    print("─" * 80)
    qrm = qrm_gen.generate(grade="2", genre="narrative", band="early", topic="kindness")
    print(f"✓ QRM Generated: {qrm.total_questions} questions")
    print(f"  Question Types: {list(qrm.type_distribution.keys())}")
    print(f"  Required Vocabulary: {qrm.required_vocabulary}")
    print(f"  Required Content: {len(qrm.required_content_elements)} elements")
    
    # Step 2: Generate PIB from QRM
    print("\n[STEP 2: PIB - Passage Blueprint]")
    print("─" * 80)
    pib = pib_gen.generate(qrm_result=qrm)
    print(f"✓ PIB Generated: {pib.total_scenes} scenes")
    print(f"  Characters: {len(pib.characters)}")
    print(f"  Target Lexile: {pib.target_lexile}")
    print(f"  Target Words: {pib.target_word_count}")
    print(f"  Structure: {pib.text_structure}")
    
    # Show the conversion
    print("\n[CONVERSION EXAMPLE]")
    print("─" * 80)
    print("\nQRM Question 3 (Implicit):")
    q3 = qrm.questions[2]
    print(f"  Requirement: {q3.content_requirement}")
    print(f"  Location: {q3.evidence_location}")
    
    print("\nPIB Scenes Supporting Q3:")
    for scene in pib.scenes:
        if 3 in scene.supports_questions:
            print(f"\n  Scene {scene.scene_number} ({scene.scene_type.value}):")
            print(f"    Purpose: {scene.purpose}")
            print(f"    Content: {scene.content_description[:100]}...")
    
    return qrm, pib


def demonstrate_scene_breakdown(pib):
    """Show detailed scene-by-scene breakdown"""
    
    print("\n" + "=" * 80)
    print("EXAMPLE 2: COMPLETE SCENE BREAKDOWN")
    print("=" * 80)
    
    for scene in pib.scenes:
        print(f"\n{'━' * 80}")
        print(f"SCENE {scene.scene_number}: {scene.scene_type.value.upper()}")
        print(f"{'━' * 80}")
        print(f"Location: {scene.location_in_passage}")
        print(f"Purpose: {scene.purpose}")
        print(f"\nContent Description:")
        print(f"  {scene.content_description}")
        print(f"\nRequired Details ({len(scene.required_details)}):")
        for detail in scene.required_details:
            print(f"  • {detail}")
        print(f"\nSupports Questions: {scene.supports_questions}")
        if scene.vocabulary_placement:
            print(f"Vocabulary: {', '.join(scene.vocabulary_placement)}")


def demonstrate_question_coverage(qrm, pib):
    """Show how every question is covered"""
    
    print("\n" + "=" * 80)
    print("EXAMPLE 3: QUESTION COVERAGE VERIFICATION")
    print("=" * 80)
    
    for q in qrm.questions:
        scenes = pib.question_coverage_map.get(q.question_number, [])
        print(f"\n{'─' * 80}")
        print(f"QUESTION {q.question_number} ({q.question_type.value}, {q.cognitive_demand.value})")
        print(f"{'─' * 80}")
        print(f"QRM Requirement:")
        print(f"  {q.content_requirement}")
        print(f"\nPIB Coverage: Scenes {scenes}")
        for scene_num in scenes:
            scene = pib.scenes[scene_num - 1]
            print(f"\n  Scene {scene_num}:")
            print(f"    {scene.content_description[:80]}...")


def demonstrate_character_specs(pib):
    """Show character specifications"""
    
    print("\n" + "=" * 80)
    print("EXAMPLE 4: CHARACTER SPECIFICATIONS")
    print("=" * 80)
    
    for char in pib.characters:
        print(f"\n{'━' * 80}")
        print(f"{char.name.upper()} ({char.role})")
        print(f"{'━' * 80}")
        print(f"Key Traits: {', '.join(char.key_traits)}")
        print(f"\nActions to Show (demonstrating traits):")
        for i, action in enumerate(char.actions_to_show, 1):
            print(f"  {i}. {action}")
        print(f"\nSupports Questions: {char.supports_questions}")


def demonstrate_vocabulary_integration(pib):
    """Show vocabulary placement and context"""
    
    print("\n" + "=" * 80)
    print("EXAMPLE 5: VOCABULARY INTEGRATION")
    print("=" * 80)
    
    for vocab_word in pib.vocabulary_targets:
        print(f"\n{'─' * 80}")
        print(f"VOCABULARY: {vocab_word.upper()}")
        print(f"{'─' * 80}")
        
        # Find scene with this vocabulary
        for scene in pib.scenes:
            if vocab_word in scene.vocabulary_placement:
                print(f"Placement: Scene {scene.scene_number}")
                print(f"Scene Content:")
                print(f"  {scene.content_description}")
        
        # Show detailed context
        if vocab_word in pib.vocabulary_contexts:
            print(f"\nDetailed Context Guidance:")
            print(f"  {pib.vocabulary_contexts[vocab_word]}")


def demonstrate_ready_for_passage():
    """Show what passage writer receives"""
    
    print("\n" + "=" * 80)
    print("EXAMPLE 6: READY FOR PASSAGE WRITING")
    print("=" * 80)
    
    mock_ai = MockAI()
    qrm_gen = create_qrm_generator(mock_ai)
    pib_gen = create_pib_generator(mock_ai)
    
    qrm = qrm_gen.generate(grade="2", genre="narrative", band="early")
    pib = pib_gen.generate(qrm_result=qrm)
    
    print("\nPASSAGE WRITER'S INSTRUCTIONS:")
    print("─" * 80)
    print(f"Write a {pib.target_word_count}-word passage at {pib.target_lexile} Lexile")
    print(f"Genre: {pib.genre} | Structure: {pib.text_structure}")
    
    print(f"\nOPENING:")
    print(f"  {pib.opening_hook}")
    
    print(f"\nCENTRAL FOCUS:")
    print(f"  {pib.central_conflict_or_topic}")
    
    print(f"\nSCENE-BY-SCENE REQUIREMENTS:")
    for scene in pib.scenes:
        print(f"\n  Scene {scene.scene_number} (~{pib.target_word_count // pib.total_scenes} words):")
        print(f"    {scene.content_description[:60]}...")
        print(f"    Must include: {scene.required_details[0]}")
        if scene.vocabulary_placement:
            print(f"    Use vocabulary: {scene.vocabulary_placement[0]}")
    
    print(f"\nCONCLUSION:")
    print(f"  {pib.resolution_or_conclusion}")
    
    print(f"\nVALIDATION CHECKLIST:")
    print(f"  □ {pib.total_scenes} scenes present")
    print(f"  □ {len(pib.characters)} characters appear")
    print(f"  □ {len(pib.vocabulary_targets)} vocabulary words used")
    print(f"  □ All {qrm.total_questions} questions answerable")
    print(f"  □ Word count: {pib.target_word_count} ± 20")
    print(f"  □ Lexile: {pib.target_lexile}")


def demonstrate_json_export(pib):
    """Show JSON export for passage generator"""
    
    print("\n" + "=" * 80)
    print("EXAMPLE 7: JSON EXPORT FOR PASSAGE GENERATOR")
    print("=" * 80)
    
    import json
    pib_json = json.dumps(pib.to_dict(), indent=2)
    
    print("\nPIB exported to JSON for passage generator:")
    print("─" * 80)
    print(pib_json[:800] + "\n... (truncated)")
    print("─" * 80)
    print(f"\nFull JSON size: {len(pib_json)} characters")
    print("\nThis JSON contains everything needed to write the passage:")
    print("  • Complete scene descriptions")
    print("  • Character specifications")
    print("  • Vocabulary contexts")
    print("  • Question coverage map")
    print("  • Bank constraints (Lexile, word count)")


if __name__ == "__main__":
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "PIB GENERATOR - COMPLETE EXAMPLES" + " " * 25 + "║")
    print("╚" + "═" * 78 + "╝")
    
    # Run demonstrations
    qrm, pib = demonstrate_qrm_to_pib()
    demonstrate_scene_breakdown(pib)
    demonstrate_question_coverage(qrm, pib)
    demonstrate_character_specs(pib)
    demonstrate_vocabulary_integration(pib)
    demonstrate_ready_for_passage()
    demonstrate_json_export(pib)
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("""
The PIB Generator transforms abstract question requirements into concrete passage plans:

✓ Converts QRM into 4-8 detailed scenes
✓ Specifies character names, traits, and actions
✓ Plans vocabulary placement with context
✓ Maps every question to supporting scenes
✓ Provides constraints from Banks 1, 3, 7
✓ Creates complete blueprint for passage writer

THE WORKFLOW:
1. QRM: "We need questions about character kindness"
2. PIB: "Write 6 scenes showing these 5 kind actions by Maya"
3. Passage: "Here's a 200-word story with all those elements"

NEXT STEP:
Build Comprehension Passage Generator that uses QRM + PIB to write actual passage text

Phase 2B Status:
  ✓ QRM Generator - Complete
  ✓ PIB Generator - Complete
  ⏳ Passage Generator - Next (final step)
    """)
