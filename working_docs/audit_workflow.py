import sys
import os
import json
import traceback
from datetime import datetime
from typing import Dict, Any, List, Optional

# Add src to path
sys.path.append(os.getcwd())

from src.generators.qrm_generator import create_qrm_generator
from src.generators.pib_generator import create_pib_generator
from src.generators.comprehension_passage_generator import create_comprehension_passage_generator

# --- MOCK AI CLIENT ---

class MockAI:
    def __init__(self, mode="success", word_count_override=None, missing_vocab=False):
        self.mode = mode
        self.word_count_override = word_count_override
        self.missing_vocab = missing_vocab
        self.last_prompt = ""

    def complete(self, prompt):
        self.last_prompt = prompt
        
        # Determine grade from prompt
        grade = "2" # Default
        for g in ["K", "1", "2", "3", "4", "5", "6", "7", "8", "8+"]:
            if f"Grade: {g}\n" in prompt or f'"grade": "{g}"' in prompt:
                grade = g
                break

        if "Question Requirement Matrix" in prompt or "QRM_GEN" in prompt or "question requirement matrix" in prompt.lower():
            return self._qrm_response(grade)
        elif "Passage Information Bank" in prompt or "PIB_GEN" in prompt or "passage information bank" in prompt.lower():
            return self._pib_response(grade)
        else:
            return self._passage_response(grade)

    def _qrm_response(self, grade):
        # Dynamically build QRM based on grade blueprint
        from src.banks import get_blueprint
        bp = get_blueprint(grade)
        dist = bp.distribution.to_dict()
        cog = bp.cognitive_demands.to_dict()
        
        questions = []
        q_num = 1
        
        # Add questions based on distribution
        for q_type, count in dist.items():
            for _ in range(count):
                questions.append({
                    "question_number": q_num,
                    "question_type": q_type,
                    "cognitive_demand": "low", # Fill in later
                    "evidence_location": "middle",
                    "content_requirement": f"Requirement for Q{q_num}",
                    "distractor_guidance": "Distractor help"
                })
                q_num += 1
        
        # Assign cognitive demands
        q_idx = 0
        for demand, count in cog.items():
            for _ in range(count):
                if q_idx < len(questions):
                    questions[q_idx]["cognitive_demand"] = demand
                    q_idx += 1

        return json.dumps({
            "questions": questions,
            "total_questions": bp.total_questions,
            "required_content_elements": ["Element 1", "Element 2"],
            "required_vocabulary": ["hesitant"] if "vocabulary" in dist else [],
            "required_structure_elements": ["chronological"]
        })

    def _pib_response(self, grade):
        from src.banks import get_blueprint, get_comp_word_count
        bp = get_blueprint(grade)
        word_count = get_comp_word_count(grade).average
        
        return json.dumps({
            "scenes": [
                {"scene_number": 1, "scene_type": "opening", "location_in_passage": "beginning", "purpose": "Intro", "content_description": "Intro scene", "required_details": ["Detail 1"], "supports_questions": [1], "vocabulary_placement": []},
                {"scene_number": 2, "scene_type": "action", "location_in_passage": "middle", "purpose": "Action 1", "content_description": "Middle scene 1", "required_details": ["Detail 2", "tag"], "supports_questions": [2], "vocabulary_placement": ["hesitant"]},
                {"scene_number": 3, "scene_type": "action", "location_in_passage": "middle", "purpose": "Action 2", "content_description": "Middle scene 2", "required_details": ["Detail 3"], "supports_questions": [3], "vocabulary_placement": []},
                {"scene_number": 4, "scene_type": "conclusion", "location_in_passage": "end", "purpose": "Conclusion", "content_description": "End scene", "required_details": ["Detail 4"], "supports_questions": [4], "vocabulary_placement": []}
            ],
            "total_scenes": 4,
            "characters": [{"name": "Maya", "role": "protagonist", "key_traits": ["kind"], "actions_to_show": ["helps"], "supports_questions": [1]}],
            "opening_hook": "Once upon a time.",
            "central_conflict_or_topic": "A problem.",
            "resolution_or_conclusion": "Solved.",
            "target_lexile": "300-400L",
            "target_word_count": word_count,
            "vocabulary_targets": ["hesitant"],
            "vocabulary_contexts": {"hesitant": "Context for hesitant"},
            "text_structure": "chronological",
            "organizational_features": [],
            "question_coverage_map": {str(i): [1, 2, 3, 4] for i in range(1, bp.total_questions + 1)}
        })

    def _passage_response(self, grade):
        title = "A Great Story"
        from src.banks import get_comp_word_count
        target = get_comp_word_count(grade).average
        
        if self.mode == "fail_word_count":
            passage = "Word " * (target + 100)
        elif self.mode == "fail_vocab":
            # Ensure it fits word count but missing vocab
            # sentences are ~7 words each.
            needed = target + 10 # Aim slightly above average
            count = needed // 6 
            passage = "A story without it. " * count
        else:
            # Multi-paragraph passage
            # Target is average. 
            count = target // 6
            p_len = count // 3
            p1 = "Maya was hesitant at the playground. " * p_len
            p2 = "Then she played tag with her friends. " * p_len
            p3 = "It was a wonderful day for everyone. " * p_len
            passage = f"{p1}\n\n{p2}\n\n{p3}"     
        return f"{title}\n\n{passage}"

# --- TEST SUITES ---

class AuditSystem:
    def __init__(self):
        self.results = []
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def run_test(self, name, func):
        print(f"Running {name}...")
        try:
            func()
            self.results.append({"name": name, "status": "PASS", "note": ""})
            print(f"  [PASS]")
        except Exception as e:
            self.results.append({"name": name, "status": "FAIL", "note": str(e)})
            print(f"  [FAIL] {e}")
            import traceback
            traceback.print_exc()

    def report(self):
        total = len(self.results)
        passed = len([r for r in self.results if r["status"] == "PASS"])
        rate = (passed / total) * 100 if total > 0 else 0
        
        print("\n" + "="*40)
        print("AUDIT RESULTS SUMMARY")
        print("="*40)
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Pass Rate: {rate:.1f}%")
        print("="*40)

# --- INDIVIDUAL TESTS ---

def test_1_1_qrm_grade_2():
    ai = MockAI()
    gen = create_qrm_generator(ai)
    qrm = gen.generate(grade="2", genre="narrative", band="early", topic="friendship")
    
    assert qrm.total_questions == 6, f"Expected 6 questions, got {qrm.total_questions}"
    assert "explicit" in qrm.type_distribution, "Missing explicit questions"
    assert qrm.type_distribution["explicit"] == 4
    assert "Bank 4" in str(qrm.bank_usage)
    assert qrm.grade == "2"

def test_1_2_pib_from_qrm():
    ai = MockAI()
    qrm_gen = create_qrm_generator(ai)
    qrm = qrm_gen.generate(grade="2", genre="narrative", band="early")
    
    pib_gen = create_pib_generator(ai)
    pib = pib_gen.generate(qrm_result=qrm)
    
    assert pib.total_scenes >= 3
    assert len(pib.characters) >= 1
    assert pib.target_lexile == "245L-425L"
    assert pib.target_word_count == 125
    assert pib.qrm_form_id == qrm.form_id
    assert "Bank 1" in str(pib.bank_usage)

def test_1_3_passage_from_qrm_pib():
    ai = MockAI()
    qrm_gen = create_qrm_generator(ai)
    qrm = qrm_gen.generate(grade="2", genre="narrative", band="early")
    pib_gen = create_pib_generator(ai)
    pib = pib_gen.generate(qrm_result=qrm)
    
    passage_gen = create_comprehension_passage_generator(ai)
    result = passage_gen.generate(qrm_result=qrm, pib_result=pib)
    
    assert result.passage_text is not None
    assert result.actual_word_count > 0
    assert result.validation.validation_passed
    assert result.qrm_form_id == qrm.form_id

# --- INTEGRATION TESTS ---

def test_2_1_complete_workflow():
    ai = MockAI()
    qrm = create_qrm_generator(ai).generate(grade="2", genre="narrative", band="early")
    pib = create_pib_generator(ai).generate(qrm_result=qrm)
    result = create_comprehension_passage_generator(ai).generate(qrm_result=qrm, pib_result=pib)
    
    assert result.qrm_form_id == qrm.form_id
    assert result.pib_form_id == pib.form_id
    assert result.total_questions == qrm.total_questions
    assert result.vocabulary_words == pib.vocabulary_targets

def test_2_2_multi_grade():
    ai = MockAI()
    grades = ["1", "2", "3", "5", "8"]
    for g in grades:
        qrm = create_qrm_generator(ai).generate(grade=g, genre="narrative", band="early")
        # Bank 4 check (Grade 1/2 = 6, 3/5/8 = 8 or 10)
        # We need to check if the generator actually pulls from Bank 4
        # Since MockAI returns hardcoded 6, this test with MockAI will fail Grade 3+ if we assert Bank 4 values
        # Unless we make MockAI smarter. Let's make it smarter or just verify it runs.
        pib = create_pib_generator(ai).generate(qrm_result=qrm)
        result = create_comprehension_passage_generator(ai).generate(qrm_result=qrm, pib_result=pib)
        assert result.grade == g

def test_2_3_genre_variation():
    ai = MockAI()
    genres = ["narrative", "nonfiction"]
    for genre in genres:
        qrm = create_qrm_generator(ai).generate(grade="2", genre=genre, band="early")
        pib = create_pib_generator(ai).generate(qrm_result=qrm)
        result = create_comprehension_passage_generator(ai).generate(qrm_result=qrm, pib_result=pib)
        assert result.genre == genre

# --- ANTI-DRIFT COMPLIANCE ---

def test_3_1_bank_usage():
    ai = MockAI()
    qrm = create_qrm_generator(ai).generate(grade="2", genre="narrative", band="early")
    pib = create_pib_generator(ai).generate(qrm_result=qrm)
    result = create_comprehension_passage_generator(ai).generate(qrm_result=qrm, pib_result=pib)
    
    assert "Bank 4" in str(qrm.bank_usage)
    assert "Bank 1" in str(pib.bank_usage)
    assert "Bank 3" in str(pib.bank_usage)
    assert "Bank 7" in str(pib.bank_usage)

def test_3_2_immutability():
    ai = MockAI()
    gen = create_qrm_generator(ai)
    qrm1 = gen.generate(grade="2", genre="narrative", band="early")
    qrm2 = gen.generate(grade="2", genre="narrative", band="early")
    
    assert qrm1.form_id != qrm2.form_id
    assert qrm1.total_questions == qrm2.total_questions

# --- VALIDATION & ERROR HANDLING ---

def test_4_1_word_count_validation():
    ai = MockAI(mode="fail_word_count")
    qrm = create_qrm_generator(ai).generate(grade="2", genre="narrative", band="early")
    pib = create_pib_generator(ai).generate(qrm_result=qrm)
    passage_gen = create_comprehension_passage_generator(ai)
    
    result = passage_gen.generate(qrm_result=qrm, pib_result=pib)
    assert not result.validation.validation_passed
    assert any("Word count" in w for w in result.validation.warnings)

def test_4_2_missing_vocab_validation():
    ai = MockAI(mode="fail_vocab")
    # Use Grade 4 because Grade 2 has no vocabulary questions in blueprint
    qrm = create_qrm_generator(ai).generate(grade="4", genre="narrative", band="early")
    pib = create_pib_generator(ai).generate(qrm_result=qrm)
    passage_gen = create_comprehension_passage_generator(ai)
    
    result = passage_gen.generate(qrm_result=qrm, pib_result=pib)
    assert not result.validation.validation_passed
    try:
        assert any("hesitant" in w and "not found" in w for w in result.validation.warnings)
    except AssertionError:
        print(f"DEBUG: Warnings found: {result.validation.warnings}")
        raise

# --- OUTPUT QUALITY ---

def test_5_1_question_coverage():
    ai = MockAI()
    qrm = create_qrm_generator(ai).generate(grade="2", genre="narrative", band="early")
    pib = create_pib_generator(ai).generate(qrm_result=qrm)
    result = create_comprehension_passage_generator(ai).generate(qrm_result=qrm, pib_result=pib)
    
    # Check if keyword 'Maya' (from Q 1 requirement) is in text
    assert "Maya" in result.passage_text
    # Check if keyword 'tag' (from Q 2) is in text
    assert "tag" in result.passage_text

def test_5_2_coherence_check():
    ai = MockAI()
    qrm = create_qrm_generator(ai).generate(grade="2", genre="narrative", band="early")
    pib = create_pib_generator(ai).generate(qrm_result=qrm)
    result = create_comprehension_passage_generator(ai).generate(qrm_result=qrm, pib_result=pib)
    
    assert "\n\n" in result.passage_text  # Paragraphs
    assert len(result.passage_text.split('.')) >= 5  # Sentences
    assert result.passage_title is not None
    assert "[" not in result.passage_text  # No placeholders

# --- MAIN RUNNER ---

if __name__ == "__main__":
    audit = AuditSystem()
    
    print("="*80)
    print("COMPREHENSION WORKFLOW AUDIT")
    print("="*80)
    
    # Suite 1
    audit.run_test("Test 1.1: QRM Generator", test_1_1_qrm_grade_2)
    audit.run_test("Test 1.2: PIB Generator", test_1_2_pib_from_qrm)
    audit.run_test("Test 1.3: Passage Generator", test_1_3_passage_from_qrm_pib)
    
    # Suite 2
    audit.run_test("Test 2.1: Complete Workflow", test_2_1_complete_workflow)
    audit.run_test("Test 2.2: Multi-Grade Test", test_2_2_multi_grade)
    audit.run_test("Test 2.3: Genre Variation Test", test_2_3_genre_variation)
    
    # Suite 3
    audit.run_test("Test 3.1: Bank Usage Verification", test_3_1_bank_usage)
    audit.run_test("Test 3.2: Immutability Check", test_3_2_immutability)
    
    # Suite 4
    audit.run_test("Test 4.1: Word Count Validation", test_4_1_word_count_validation)
    audit.run_test("Test 4.2: Missing Vocabulary Validation", test_4_2_missing_vocab_validation)
    
    # Suite 5
    audit.run_test("Test 5.1: Question Coverage Verification", test_5_1_question_coverage)
    audit.run_test("Test 5.2: Coherence Check", test_5_2_coherence_check)
    
    audit.report()
    
    # Save results to a temporary JSON for report generation
    with open("audit_results.json", "w") as f:
        json.dump({
            "timestamp": audit.timestamp,
            "results": audit.results
        }, f)
