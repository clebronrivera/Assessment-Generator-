# Integration Challenges - Resolution Guide

**Date:** 2026-01-12  
**Status:** Solutions Identified  
**Action Required:** Apply fixes to resolve both challenges

---

## Challenge 1: ORF Generator API Mismatch

### Problem
```python
# ORF Generator (Line 44)
passage_text = self.ai_client.generate(prompt)  # ❌ Different method

# All Other Generators
response = self.ai_client.complete(prompt)      # ✅ Standard method
```

### Solution: Standardize to `complete()`

**File to Modify:** `src/generators/orf_generator.py`

**Change Line 44:**
```python
# OLD (Line 44):
passage_text = self.ai_client.generate(prompt)

# NEW:
passage_text = self.ai_client.complete(prompt)
```

**Why This Works:**
- All other generators use `complete()`
- Mock AI clients implement `complete()`
- Real AI clients (OpenAI, Anthropic) use `complete()` wrapper
- Maintains consistency across codebase

**Impact:**
- ✅ ORF generator works with standard mock clients
- ✅ Consistent API across all generators
- ✅ No changes needed to mock clients
- ✅ No changes needed to real AI clients

---

## Challenge 2: QRM Validation Strictness

### Problem
```python
# Bank 4 Requirement: Grade 2 = 6 questions
# Test Mock: Only provides 2 questions
# Result: ValueError at line 392
```

### Solution: Update Mock to Match Bank 4

**File to Modify:** Test files using QRM generator

**Update Mock Response for Grade 2:**
```python
def _qrm_response(self):
    import json
    return json.dumps({
        "questions": [
            # Need 6 questions, not 2
            {"question_number": 1, "question_type": "explicit", "cognitive_demand": "low", ...},
            {"question_number": 2, "question_type": "explicit", "cognitive_demand": "low", ...},
            {"question_number": 3, "question_type": "implicit", "cognitive_demand": "medium", ...},
            {"question_number": 4, "question_type": "implicit", "cognitive_demand": "medium", ...},
            {"question_number": 5, "question_type": "vocabulary", "cognitive_demand": "medium", ...},
            {"question_number": 6, "question_type": "main_idea", "cognitive_demand": "high", ...}
        ],
        "total_questions": 6,  # Must match Bank 4
        "type_distribution": {
            "explicit": 2,      # Bank 4: Grade 2 requirements
            "implicit": 2,
            "vocabulary": 1,
            "main_idea": 1
        },
        "cognitive_distribution": {
            "low": 2,           # Bank 4: Grade 2 requirements
            "medium": 3,
            "high": 1
        },
        # ... rest of response
    })
```

**Why This Works:**
- Matches Bank 4 specifications exactly
- QRM validation passes
- Realistic test scenario
- Proper question type distribution
- Correct cognitive demand distribution

**Alternative: Lenient Testing Mode (Not Recommended)**
```python
# Could add validation flag, but this defeats anti-drift purpose
def generate(self, ..., strict_validation=True):
    if strict_validation:
        self._validate_qrm(...)  # Enforce Bank 4
    # else: skip validation (NOT RECOMMENDED)
```

**Why We Don't Do This:**
- ❌ Defeats anti-drift protocol
- ❌ Allows test data to diverge from banks
- ❌ Creates "test-only" code paths
- ✅ Better: Make mocks match reality (Bank 4)

---

## Implementation Steps

### Step 1: Fix ORF Generator API

```bash
# Edit src/generators/orf_generator.py
# Change line 44 from:
passage_text = self.ai_client.generate(prompt)
# To:
passage_text = self.ai_client.complete(prompt)
```

### Step 2: Fix QRM Mock in Package Builder Tests

```bash
# Edit test_package_builder.py (or wherever mock is defined)
# Update _qrm_response() to return 6 questions
# Match Bank 4 distributions exactly
```

### Step 3: Verify Fixes

```bash
# Test ORF package building
python test_package_builder.py --test-orf

# Test Comprehension package building  
python test_package_builder.py --test-comp

# Test both
python test_package_builder.py
```

### Step 4: Update Documentation

```bash
# Update CHANGELOG.md with fixes
# Update test documentation
# Mark package builder as "fully integrated"
```

---

## Complete MockAI for Package Builder Tests

Here's a complete mock that works with all generators:

```python
class MockAI:
    """Mock AI client for testing - Bank 4 compliant"""
    
    def complete(self, prompt):
        """Standard method used by all generators"""
        if "Question Requirement Matrix" in prompt or "QRM" in prompt:
            return self._qrm_response()
        elif "Passage Information Bank" in prompt or "PIB" in prompt:
            return self._pib_response()
        elif "ORF" in prompt or "oral reading" in prompt.lower():
            return self._orf_response()
        elif "multiple choice questions" in prompt.lower():
            return self._questions_response()
        elif "recall scoring" in prompt.lower():
            return self._recall_response()
        else:
            return self._passage_response()
    
    def _orf_response(self):
        """ORF passage - 150 words for Grade 2"""
        return """The sun was warm on the playground. Max and his friends played tag during recess. They ran fast and laughed together.
        
Max saw a new girl sitting alone on the bench. Her name was Emma. She looked sad. Max walked over to her.

"Do you want to play with us?" Max asked. Emma smiled and nodded. She joined the game of tag.

Soon Emma was running and laughing with everyone. Max felt happy that he asked her to play. Making new friends was fun."""
    
    def _qrm_response(self):
        """Grade 2 QRM - Bank 4 compliant (6 questions)"""
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
                    "question_type": "implicit",
                    "cognitive_demand": "medium",
                    "evidence_location": "middle",
                    "content_requirement": "Emma felt sad before joining",
                    "distractor_guidance": "Use opposite emotions"
                },
                {
                    "question_number": 4,
                    "question_type": "implicit",
                    "cognitive_demand": "medium",
                    "evidence_location": "end",
                    "content_requirement": "Max felt happy about helping Emma",
                    "distractor_guidance": "Use wrong emotions or outcomes"
                },
                {
                    "question_number": 5,
                    "question_type": "vocabulary",
                    "cognitive_demand": "medium",
                    "evidence_location": "beginning",
                    "content_requirement": "Meaning of 'recess'",
                    "distractor_guidance": "Use similar school-related terms"
                },
                {
                    "question_number": 6,
                    "question_type": "main_idea",
                    "cognitive_demand": "high",
                    "evidence_location": "throughout",
                    "content_requirement": "Theme: Being friendly helps others feel included",
                    "distractor_guidance": "Use details as main ideas"
                }
            ],
            "total_questions": 6,
            "type_distribution": {
                "explicit": 2,
                "implicit": 2,
                "vocabulary": 1,
                "main_idea": 1
            },
            "cognitive_distribution": {
                "low": 2,
                "medium": 3,
                "high": 1
            },
            "evidence_distribution": {
                "beginning": 2,
                "middle": 2,
                "end": 1,
                "throughout": 1
            },
            "required_vocabulary": ["recess"],
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
                    "supports_questions": [1, 5],
                    "vocabulary_placement": ["recess"]
                },
                {
                    "scene_number": 2,
                    "scene_type": "action",
                    "location_in_passage": "middle",
                    "purpose": "Introduce Emma alone",
                    "content_description": "Emma sitting alone looking sad",
                    "required_details": ["Emma's name", "sitting alone", "looked sad"],
                    "supports_questions": [2, 3],
                    "vocabulary_placement": []
                },
                {
                    "scene_number": 3,
                    "scene_type": "action",
                    "location_in_passage": "middle",
                    "purpose": "Max invites Emma",
                    "content_description": "Max walks over and invites Emma to play",
                    "required_details": ["Max asks", "Emma smiles", "Emma joins"],
                    "supports_questions": [3, 4],
                    "vocabulary_placement": []
                },
                {
                    "scene_number": 4,
                    "scene_type": "conclusion",
                    "location_in_passage": "end",
                    "purpose": "Show positive outcome",
                    "content_description": "Emma happy, Max happy, friendship",
                    "required_details": ["Emma running and laughing", "Max happy", "making friends"],
                    "supports_questions": [4, 6],
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
                    "supports_questions": [1, 4, 6]
                },
                {
                    "name": "Emma",
                    "role": "supporting",
                    "key_traits": ["new", "shy at first", "happy after"],
                    "actions_to_show": ["Sits alone", "Joins game", "Laughs"],
                    "supports_questions": [2, 3]
                }
            ],
            "opening_hook": "The sun was warm on the playground",
            "central_conflict_or_topic": "Max helps new student feel included",
            "resolution_or_conclusion": "Emma joins in and makes friends",
            "target_lexile": "245L-425L",
            "target_word_count": 125,
            "vocabulary_targets": ["recess"],
            "vocabulary_contexts": {
                "recess": "Time to play outside at school"
            },
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
        """Question generator response - 6 questions"""
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
                    "question_number": 4,
                    "question_text": "How did Max feel after Emma joined the game?",
                    "question_type": "implicit",
                    "cognitive_demand": "medium",
                    "answer_options": [
                        {"letter": "A", "text": "Happy", "is_correct": True, "distractor_type": None},
                        {"letter": "B", "text": "Sad", "is_correct": False, "distractor_type": "opposite"},
                        {"letter": "C", "text": "Tired", "is_correct": False, "distractor_type": "unrelated"}
                    ],
                    "correct_answer": "A",
                    "evidence_location": "end",
                    "evidence_text": "Max felt happy that he asked her to play.",
                    "points_possible": 1
                },
                {
                    "question_number": 5,
                    "question_text": "What does 'recess' mean in this story?",
                    "question_type": "vocabulary",
                    "cognitive_demand": "medium",
                    "answer_options": [
                        {"letter": "A", "text": "Lunch time", "is_correct": False, "distractor_type": "similar_concept"},
                        {"letter": "B", "text": "Play time", "is_correct": True, "distractor_type": None},
                        {"letter": "C", "text": "Class time", "is_correct": False, "distractor_type": "opposite"}
                    ],
                    "correct_answer": "B",
                    "evidence_location": "beginning",
                    "evidence_text": "Max and his friends played tag during recess.",
                    "points_possible": 1
                },
                {
                    "question_number": 6,
                    "question_text": "What is the main idea of this story?",
                    "question_type": "main_idea",
                    "cognitive_demand": "high",
                    "answer_options": [
                        {"letter": "A", "text": "Being friendly helps others", "is_correct": True, "distractor_type": None},
                        {"letter": "B", "text": "The playground was warm", "is_correct": False, "distractor_type": "detail"},
                        {"letter": "C", "text": "Tag is fun", "is_correct": False, "distractor_type": "too_specific"}
                    ],
                    "correct_answer": "A",
                    "evidence_location": "throughout",
                    "evidence_text": "Making new friends was fun.",
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
                # ... additional sentences
            ],
            "general_instructions": "Score each sentence 0-2 points based on key ideas recalled.",
            "scoring_notes": [
                "Accept paraphrasing",
                "Award partial credit for keywords",
                "Don't penalize extra details"
            ]
        })
```

---

## Testing After Fixes

```python
# test_package_builder.py
from src.packaging import create_package_builder
from src.generators import (
    create_orf_generator,
    create_qrm_generator,
    create_pib_generator,
    create_comprehension_passage_generator,
    create_question_generator,
    create_recall_scoring_generator
)

def test_orf_package():
    """Test ORF package building"""
    mock_ai = MockAI()  # Using complete mock above
    
    # Generate ORF components
    orf_gen = create_orf_generator(mock_ai)
    passage = orf_gen.generate(grade="2", band="early")
    
    materials_gen = create_orf_assessor_materials_generator()
    materials = materials_gen.generate(
        grade="2",
        passage_text=passage.passage_text,
        passage_word_count=passage.metadata["actual_word_count"],
        form_id=passage.metadata["form_id"]
    )
    
    # Build package
    builder = create_package_builder()
    package = builder.build_orf_package(passage, materials)
    
    # Verify
    assert package.metadata.assessment_type == "orf"
    assert package.metadata.grade == "2"
    assert len(package.metadata.component_forms) == 2
    print("✓ ORF package test passed")

def test_comprehension_package():
    """Test comprehension package building"""
    mock_ai = MockAI()  # Using complete mock above
    
    # Generate all components
    qrm = create_qrm_generator(mock_ai).generate(grade="2", genre="narrative", band="early")
    pib = create_pib_generator(mock_ai).generate(qrm_result=qrm)
    passage = create_comprehension_passage_generator(mock_ai).generate(qrm_result=qrm, pib_result=pib)
    questions = create_question_generator(mock_ai).generate(qrm_result=qrm, passage_result=passage)
    recall = create_recall_scoring_generator(mock_ai).generate(passage_result=passage)
    
    # Build package
    builder = create_package_builder()
    package = builder.build_comprehension_package(
        qrm_result=qrm,
        pib_result=pib,
        passage_result=passage,
        questions_result=questions,
        recall_result=recall
    )
    
    # Verify
    assert package.metadata.assessment_type == "comprehension"
    assert package.metadata.grade == "2"
    assert len(package.metadata.component_forms) == 5
    assert package.metadata.stats["total_questions"] == 6
    print("✓ Comprehension package test passed")

if __name__ == "__main__":
    test_orf_package()
    test_comprehension_package()
    print("\n✓ All package builder tests passed!")
```

---

## Summary

**Both challenges have straightforward solutions:**

1. **ORF API Mismatch:** Change `generate()` to `complete()` (1 line fix)
2. **QRM Validation:** Use Bank 4-compliant mocks (6 questions, not 2)

**Why These Solutions Work:**
- ✅ Maintains anti-drift protocol (no validation bypassing)
- ✅ Standardizes API across generators
- ✅ Tests match production behavior
- ✅ Minimal code changes required

**Next Actions:**
1. Apply ORF generator fix (1 line change)
2. Update test mocks to Bank 4 compliance
3. Run tests to verify
4. Update documentation

**Status After Fixes:**
- Assessment Package Builder: Fully Integrated ✅
- All generators: Consistent API ✅
- Tests: Bank 4 compliant ✅
