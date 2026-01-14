"""
Test Assessment Package Builder with Bank 4-compliant mocks
FIXED: ORF dict access + correct Bank 4 Grade 2 distribution
"""

# Mock AI client - Bank 4 compliant (CORRECTED)
class MockAI:
    """Mock AI client for testing - Bank 4 compliant"""
    
    def complete(self, prompt):
        """Simple but robust prompt routing"""
        
        # Convert to lowercase for case-insensitive matching
        p = prompt.lower()
        
        # Check in priority order (most specific first)
        # Use very specific patterns to avoid cross-contamination
        
        # 1. PIB - "Passage Information Bank" or "PIB"
        if ("passage information bank" in p or 
            (" pib " in p or p.startswith("pib ") or " pib" in p[-5:])):
            return self._pib_response()
        
        # 2. QRM - Only match if it's the main subject, not just mentioned
        if "question requirement matrix" in p or \
           (p.startswith("generate a qrm") or p.startswith("generate qrm")):
            return self._qrm_response()
        
        # 3. Questions - Must have "multiple choice"
        if "multiple choice" in p:
            return self._questions_response()
        
        # 4. Recall - "recall" + "scor"
        if "recall" in p and "scor" in p:
            return self._recall_response()
        
        # 5. ORF - "orf" or "fluency" or "oral reading"
        if "orf" in p or "fluency" in p or "oral reading" in p:
            return self._orf_response()
        
        # 6. Passage - Default
        return self._passage_response()
    
    def _orf_response(self):
        """ORF passage - 150 words for Grade 2"""
        return """The sun was warm on the playground. Max and his friends played tag during recess. They ran fast and laughed together.
        
Max saw a new girl sitting alone on the bench. Her name was Emma. She looked sad. Max walked over to her.

"Do you want to play with us?" Max asked. Emma smiled and nodded. She joined the game of tag.

Soon Emma was running and laughing with everyone. Max felt happy that he asked her to play. Making new friends was fun."""
    
    def _qrm_response(self):
        """Grade 2 QRM - Bank 4 compliant: explicit=4, implicit=2"""
        import json
        return json.dumps({
            "questions": [
                {
                    "question_number": 1,
                    "question_type": "explicit",
                    "cognitive_demand": "low",
                    "evidence_location": "beginning",
                    "content_requirement": "Main character's name (Max)",
                    "distractor_guidance": "Use other common names"
                },
                {
                    "question_number": 2,
                    "question_type": "explicit",
                    "cognitive_demand": "low",
                    "evidence_location": "middle",
                    "content_requirement": "New girl's name (Emma)",
                    "distractor_guidance": "Use other girl names"
                },
                {
                    "question_number": 3,
                    "question_type": "explicit",
                    "cognitive_demand": "low",
                    "evidence_location": "middle",
                    "content_requirement": "What Max asked Emma",
                    "distractor_guidance": "Use other questions"
                },
                {
                    "question_number": 4,
                    "question_type": "explicit",
                    "cognitive_demand": "medium",
                    "evidence_location": "beginning",
                    "content_requirement": "What game they played",
                    "distractor_guidance": "Use other games"
                },
                {
                    "question_number": 5,
                    "question_type": "implicit",
                    "cognitive_demand": "medium",
                    "evidence_location": "middle",
                    "content_requirement": "How Emma felt before Max invited her",
                    "distractor_guidance": "Use opposite emotions"
                },
                {
                    "question_number": 6,
                    "question_type": "implicit",
                    "cognitive_demand": "medium",
                    "evidence_location": "end",
                    "content_requirement": "Why Max felt happy",
                    "distractor_guidance": "Use wrong reasons"
                }
            ],
            "total_questions": 6,
            "type_distribution": {
                "explicit": 4,
                "implicit": 2
            },
            "cognitive_distribution": {
                "low": 3,
                "medium": 3,
                "high": 0
            },
            "evidence_distribution": {
                "beginning": 2,
                "middle": 3,
                "end": 1
            },
            "required_vocabulary": [],
            "required_content_elements": [
                "Max as main character",
                "Emma as new student",
                "Tag game at recess",
                "Max invites Emma",
                "Emma joins and is happy"
            ],
            "required_structure_elements": ["chronological"]
        })
    
    def _pib_response(self):
        """PIB response"""
        import json
        return json.dumps({
            "scenes": [
                {
                    "scene_number": 1,
                    "scene_type": "opening",
                    "location_in_passage": "beginning",
                    "purpose": "Set scene at recess",
                    "content_description": "Playground during recess, Max playing tag",
                    "required_details": ["playground", "recess", "tag game"],
                    "supports_questions": [1, 4],
                    "vocabulary_placement": []
                },
                {
                    "scene_number": 2,
                    "scene_type": "action",
                    "location_in_passage": "middle",
                    "purpose": "Introduce Emma alone",
                    "content_description": "Emma sitting alone looking sad",
                    "required_details": ["Emma's name", "sitting alone", "looked sad"],
                    "supports_questions": [2, 5],
                    "vocabulary_placement": []
                },
                {
                    "scene_number": 3,
                    "scene_type": "action",
                    "location_in_passage": "middle",
                    "purpose": "Max invites Emma",
                    "content_description": "Max walks over and invites Emma to play",
                    "required_details": ["Max asks", "Emma smiles", "Emma joins"],
                    "supports_questions": [3, 5],
                    "vocabulary_placement": []
                },
                {
                    "scene_number": 4,
                    "scene_type": "conclusion",
                    "location_in_passage": "end",
                    "purpose": "Show positive outcome",
                    "content_description": "Emma happy, Max happy, friendship",
                    "required_details": ["Emma running and laughing", "Max happy", "making friends"],
                    "supports_questions": [6],
                    "vocabulary_placement": []
                }
            ],
            "total_scenes": 4,
            "characters": [
                {
                    "name": "Max",
                    "role": "main",
                    "key_traits": ["friendly", "kind"],
                    "actions_to_show": ["Invites Emma", "Feels happy"],
                    "supports_questions": [1, 6]
                },
                {
                    "name": "Emma",
                    "role": "supporting",
                    "key_traits": ["new", "shy at first", "happy after"],
                    "actions_to_show": ["Sits alone", "Joins game", "Laughs"],
                    "supports_questions": [2, 5]
                }
            ],
            "opening_hook": "The sun was warm on the playground",
            "central_conflict_or_topic": "Max helps new student feel included",
            "resolution_or_conclusion": "Emma joins in and makes friends",
            "target_lexile": "245L-605L",
            "target_word_count": 125,
            "vocabulary_targets": [],
            "vocabulary_contexts": {},
            "text_structure": "chronological",
            "organizational_features": [],
            "question_coverage_map": {
                "1": [1],
                "2": [2],
                "3": [2, 3],
                "4": [3, 4],
                "5": [1],
                "6": [4]
            }
        })
    
    def _passage_response(self):
        """Comprehension passage"""
        return """Making Friends at Recess

The sun was warm on the playground. Max and his friends played tag during recess. They ran fast and laughed together.

Max saw a new girl sitting alone on the bench. Her name was Emma. She looked sad. Max walked over to her.

"Do you want to play with us?" Max asked. Emma smiled and nodded. She joined the game of tag.

Soon Emma was running and laughing with everyone. Max felt happy that he asked her to play. Making new friends was fun."""
    
    def _questions_response(self):
        """Question generator response - 6 questions (4 explicit, 2 implicit)"""
        import json
        return json.dumps({
            "questions": [
                {
                    "question_number": 1,
                    "question_text": "Who is the main character in this story?",
                    "question_type": "explicit",
                    "cognitive_demand": "low",
                    "answer_options": [
                        {"letter": "A", "text": "Max", "is_correct": True, "distractor_type": None},
                        {"letter": "B", "text": "Emma", "is_correct": False, "distractor_type": "other_character"},
                        {"letter": "C", "text": "Sam", "is_correct": False, "distractor_type": "not_in_story"}
                    ],
                    "correct_answer": "A",
                    "evidence_location": "beginning",
                    "evidence_text": "Max and his friends played tag during recess.",
                    "points_possible": 1
                },
                {
                    "question_number": 2,
                    "question_text": "What is the new girl's name?",
                    "question_type": "explicit",
                    "cognitive_demand": "low",
                    "answer_options": [
                        {"letter": "A", "text": "Sarah", "is_correct": False, "distractor_type": "similar_name"},
                        {"letter": "B", "text": "Emma", "is_correct": True, "distractor_type": None},
                        {"letter": "C", "text": "Anna", "is_correct": False, "distractor_type": "similar_name"}
                    ],
                    "correct_answer": "B",
                    "evidence_location": "middle",
                    "evidence_text": "Her name was Emma.",
                    "points_possible": 1
                },
                {
                    "question_number": 3,
                    "question_text": "What did Max ask Emma?",
                    "question_type": "explicit",
                    "cognitive_demand": "low",
                    "answer_options": [
                        {"letter": "A", "text": "Do you want to play?", "is_correct": True, "distractor_type": None},
                        {"letter": "B", "text": "What is your name?", "is_correct": False, "distractor_type": "different_question"},
                        {"letter": "C", "text": "Are you sad?", "is_correct": False, "distractor_type": "different_question"}
                    ],
                    "correct_answer": "A",
                    "evidence_location": "middle",
                    "evidence_text": "Do you want to play with us?",
                    "points_possible": 1
                },
                {
                    "question_number": 4,
                    "question_text": "What game were the children playing?",
                    "question_type": "explicit",
                    "cognitive_demand": "medium",
                    "answer_options": [
                        {"letter": "A", "text": "Hide and seek", "is_correct": False, "distractor_type": "other_game"},
                        {"letter": "B", "text": "Tag", "is_correct": True, "distractor_type": None},
                        {"letter": "C", "text": "Soccer", "is_correct": False, "distractor_type": "other_game"}
                    ],
                    "correct_answer": "B",
                    "evidence_location": "beginning",
                    "evidence_text": "Max and his friends played tag during recess.",
                    "points_possible": 1
                },
                {
                    "question_number": 5,
                    "question_text": "How did Emma feel before Max invited her?",
                    "question_type": "implicit",
                    "cognitive_demand": "medium",
                    "answer_options": [
                        {"letter": "A", "text": "Happy", "is_correct": False, "distractor_type": "opposite"},
                        {"letter": "B", "text": "Sad", "is_correct": True, "distractor_type": None},
                        {"letter": "C", "text": "Angry", "is_correct": False, "distractor_type": "wrong_emotion"}
                    ],
                    "correct_answer": "B",
                    "evidence_location": "middle",
                    "evidence_text": "She looked sad.",
                    "points_possible": 1
                },
                {
                    "question_number": 6,
                    "question_text": "Why did Max feel happy at the end?",
                    "question_type": "implicit",
                    "cognitive_demand": "medium",
                    "answer_options": [
                        {"letter": "A", "text": "He helped Emma feel included", "is_correct": True, "distractor_type": None},
                        {"letter": "B", "text": "He won the game", "is_correct": False, "distractor_type": "wrong_reason"},
                        {"letter": "C", "text": "It was sunny", "is_correct": False, "distractor_type": "detail"}
                    ],
                    "correct_answer": "A",
                    "evidence_location": "end",
                    "evidence_text": "Max felt happy that he asked her to play.",
                    "points_possible": 1
                }
            ]
        })
    
    def _recall_response(self):
        """Recall scoring response"""
        import json
        return json.dumps({
            "sentence_scoring": [
                {
                    "sentence_number": 1,
                    "sentence_text": "The sun was warm on the playground.",
                    "max_points": 2,
                    "key_ideas": [
                        {"idea_text": "Setting is playground", "importance": "important", "points_if_recalled": 1.0},
                        {"idea_text": "Weather was warm/sunny", "importance": "supporting", "points_if_recalled": 1.0}
                    ],
                    "partial_keywords": ["sun", "warm", "playground"],
                    "score_0_criteria": "No mention of location or weather",
                    "score_1_criteria": "Mentions playground OR warm",
                    "score_2_criteria": "Mentions both playground and warm sun",
                    "example_score_0": "It was a day.",
                    "example_score_1": "They were at the playground.",
                    "example_score_2": "The sun was warm on the playground."
                }
            ],
            "general_instructions": "Score each sentence 0-2 points based on key ideas recalled.",
            "scoring_notes": [
                "Accept paraphrasing",
                "Award partial credit for keywords",
                "Don't penalize extra details"
            ]
        })


# Test ORF Package
print("=" * 80)
print("TESTING ORF PACKAGE BUILDER")
print("=" * 80)

try:
    from src.generators import create_orf_generator, create_orf_assessor_materials_generator
    from src.packaging import create_package_builder
    
    mock_ai = MockAI()
    
    # Generate ORF components
    print("\n[1] Generating ORF passage...")
    orf_gen = create_orf_generator(mock_ai)
    passage = orf_gen.generate(grade="2", band="early")
    
    # FIX: ORF returns dict, not object
    print(f"✓ Passage generated: {passage['metadata']['actual_word_count']} words")
    
    print("\n[2] Generating assessor materials...")
    materials_gen = create_orf_assessor_materials_generator()
    materials = materials_gen.generate(
        grade="2",
        passage_text=passage["passage_text"],
        passage_word_count=passage["metadata"]["actual_word_count"],
        form_id=passage["metadata"].get("form_id", "ORF-2-EARLY-001")
    )
    print(f"✓ Materials generated: {materials.form_id}")
    
    print("\n[3] Building ORF package...")
    builder = create_package_builder()
    orf_package = builder.build_orf_package(
        passage_result=passage,
        materials_result=materials
    )
    print(f"✓ Package built: {orf_package.metadata.package_id}")
    print(f"  - Components: {list(orf_package.metadata.component_forms.keys())}")
    print(f"  - Banks used: {orf_package.metadata.banks_used}")
    
    print("\n[4] Exporting to JSON...")
    json_str = builder.export_to_json(orf_package, filepath=None, pretty=False)
    print(f"✓ JSON exported: {len(json_str)} bytes")
    
    print("\n[5] Creating manifest...")
    manifest = builder.create_manifest(orf_package)
    print(f"✓ Manifest created:")
    print(f"  - Package ID: {manifest['package_id']}")
    print(f"  - Components: {manifest['components']}")
    print(f"  - Ready: {manifest['ready_for_use']}")
    
    print("\n" + "=" * 80)
    print("ORF PACKAGE TEST: PASSED ✓")
    print("=" * 80)
    
except Exception as e:
    print(f"\n✗ ORF PACKAGE TEST FAILED")
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Test Comprehension Package
print("\n\n" + "=" * 80)
print("TESTING COMPREHENSION PACKAGE BUILDER")
print("=" * 80)

try:
    from src.generators import (
        create_qrm_generator,
        create_pib_generator,
        create_comprehension_passage_generator,
        create_question_generator,
        create_recall_scoring_generator
    )
    from src.packaging import create_package_builder
    
    mock_ai = MockAI()
    
    # Generate all comprehension components
    print("\n[1] Generating QRM...")
    qrm_gen = create_qrm_generator(mock_ai)
    qrm = qrm_gen.generate(grade="2", genre="narrative", band="early")
    print(f"✓ QRM: {qrm.total_questions} questions")
    
    print("\n[2] Generating PIB...")
    pib_gen = create_pib_generator(mock_ai)
    pib = pib_gen.generate(qrm_result=qrm)
    print(f"✓ PIB: {pib.total_scenes} scenes")
    
    print("\n[3] Generating passage...")
    passage_gen = create_comprehension_passage_generator(mock_ai)
    passage = passage_gen.generate(qrm_result=qrm, pib_result=pib)
    print(f"✓ Passage: {passage.actual_word_count} words")
    
    print("\n[4] Generating questions...")
    question_gen = create_question_generator(mock_ai)
    questions = question_gen.generate(qrm_result=qrm, passage_result=passage)
    print(f"✓ Questions: {questions.total_questions} questions")
    
    print("\n[5] Generating recall scoring...")
    recall_gen = create_recall_scoring_generator(mock_ai)
    recall = recall_gen.generate(passage_result=passage)
    print(f"✓ Recall: {recall.total_sentences} sentences")
    
    print("\n[6] Building comprehension package...")
    builder = create_package_builder()
    comp_package = builder.build_comprehension_package(
        qrm_result=qrm,
        pib_result=pib,
        passage_result=passage,
        questions_result=questions,
        recall_result=recall
    )
    print(f"✓ Package built: {comp_package.metadata.package_id}")
    print(f"  - Components: {list(comp_package.metadata.component_forms.keys())}")
    print(f"  - Banks used: {comp_package.metadata.banks_used}")
    
    print("\n[7] Exporting to JSON...")
    json_str = builder.export_to_json(comp_package, filepath=None, pretty=False)
    print(f"✓ JSON exported: {len(json_str)} bytes")
    
    print("\n[8] Creating manifest...")
    manifest = builder.create_manifest(comp_package)
    print(f"✓ Manifest created:")
    print(f"  - Package ID: {manifest['package_id']}")
    print(f"  - Components: {manifest['components']}")
    print(f"  - Stats: {manifest['statistics']}")
    
    print("\n" + "=" * 80)
    print("COMPREHENSION PACKAGE TEST: PASSED ✓")
    print("=" * 80)
    
except Exception as e:
    print(f"\n✗ COMPREHENSION PACKAGE TEST FAILED")
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("\n\n" + "=" * 80)
print("PACKAGE BUILDER INTEGRATION TEST COMPLETE")
print("=" * 80)
