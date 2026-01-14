"""
Question Generator

Generates multiple choice questions from QRM and passage.
Uses QRM specifications to create questions with plausible distractors.

Bank Usage:
- Bank 4 (Comprehension Blueprint): Via QRM for question specifications
- Bank 6 (Answer Options): Number of answer choices by grade

Dependencies:
- qrm_generator.py: Provides question specifications
- comprehension_passage_generator.py: Provides passage text

Purpose:
- Final step in comprehension assessment creation
- Generates actual questions from QRM requirements
- Creates plausible distractors using QRM guidance
- Includes answer key with evidence locations

Created: 2026-01-12
Schema Version: 2026.1
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum


class QuestionType(Enum):
    """Types of comprehension questions"""
    EXPLICIT = "explicit"
    IMPLICIT = "implicit"
    VOCABULARY = "vocabulary"
    MAIN_IDEA = "main_idea"
    INFERENCE = "inference"
    CAUSE_EFFECT = "cause_effect"
    COMPARE_CONTRAST = "compare_contrast"
    AUTHOR_PURPOSE = "author_purpose"
    TEXT_STRUCTURE = "text_structure"
    POINT_OF_VIEW = "point_of_view"
    THEME = "theme"


@dataclass
class AnswerOption:
    """Individual answer option"""
    letter: str  # A, B, C, D, etc.
    text: str
    is_correct: bool
    distractor_type: Optional[str] = None  # e.g., "plausible_wrong", "opposite", "detail"


@dataclass
class Question:
    """Individual question with answer options"""
    question_number: int
    question_text: str
    question_type: QuestionType
    cognitive_demand: str  # low, medium, high
    answer_options: List[AnswerOption]
    correct_answer: str  # Letter of correct answer
    evidence_location: str  # Where answer is found in passage
    evidence_text: str  # Actual text from passage supporting answer
    points_possible: int = 1


@dataclass
class AnswerKey:
    """Complete answer key for assessment"""
    questions: List[Question]
    total_questions: int
    total_points: int
    answer_key_summary: Dict[int, str]  # Question # -> Correct letter


@dataclass
class QuestionGeneratorResult:
    """Complete question set with answer key"""
    
    # Questions
    questions: List[Question]
    total_questions: int
    
    # Answer key
    answer_key: AnswerKey
    
    # Metadata
    grade: str
    genre: str
    band: str
    form_id: str
    
    # Question distribution (for validation)
    type_distribution: Dict[str, int]
    cognitive_distribution: Dict[str, int]
    
    # Links to source documents
    qrm_form_id: str
    passage_form_id: str
    
    # Bank constraints
    num_answer_options: int  # From Bank 6
    
    # Generation metadata
    generated_at: str
    schema_version: str
    bank_usage: Dict[str, str]
    
    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        # Convert enums
        for q in result['questions']:
            q['question_type'] = q['question_type'].value if hasattr(q['question_type'], 'value') else q['question_type']
        return result


class QuestionGenerator:
    """
    Generates multiple choice questions from QRM and passage.
    
    Uses QRM specifications to ensure questions match requirements,
    and uses Bank 6 to determine number of answer options by grade.
    """
    
    def __init__(self, ai_client):
        """Initialize with AI client and bank access"""
        self.ai_client = ai_client
        self.schema_version = "2026.1"
        self._load_banks()
        self._load_template()
    
    def _load_banks(self):
        """Load required banks"""
        try:
            from src.banks import get_num_options
            self.get_num_options = get_num_options
        except ImportError:
            print("Warning: Could not import banks, using mock data")
            self.get_num_options = self._mock_get_num_options
    
    def _mock_get_num_options(self, grade: str) -> int:
        """Mock Bank 6 data"""
        # K-2: 3 options, 3-5: 4 options, 6+: 4 options
        if grade in ["K", "1", "2"]:
            return 3
        else:
            return 4
    
    def _load_template(self):
        """Load Jinja2 template for question prompt"""
        try:
            from src.utils import load_template
            self.template = load_template("questions.j2")
        except ImportError:
            self.template = None
            print("Warning: Template loader not available, using inline prompt")
    
    def generate(
        self,
        qrm_result,  # From QRM Generator
        passage_result,  # From Comprehension Passage Generator
        form_id: Optional[str] = None
    ) -> QuestionGeneratorResult:
        """
        Generate multiple choice questions from QRM and passage.
        
        Args:
            qrm_result: QRMResult from QRM Generator
            passage_result: ComprehensionPassageResult from Passage Generator
            form_id: Optional form identifier
        
        Returns:
            QuestionGeneratorResult with questions and answer key
        """
        
        # Get number of answer options from Bank 6
        num_options = self.get_num_options(qrm_result.grade)
        
        # Generate form ID if not provided
        if not form_id:
            form_id = f"COMP-{qrm_result.grade.upper()}-{qrm_result.band.upper()}-QUESTIONS-001"
        
        # Build prompt
        if self.template:
            prompt = self._build_prompt_from_template(
                qrm_result, passage_result, num_options
            )
        else:
            prompt = self._build_inline_prompt(
                qrm_result, passage_result, num_options
            )
        
        # Call AI to generate questions
        response = self.ai_client.complete(prompt)
        
        # Parse response into structured questions
        questions = self._parse_response(response, qrm_result, num_options)
        
        # Create answer key
        answer_key = self._create_answer_key(questions)
        
        # Validate questions match QRM
        self._validate_questions(questions, qrm_result)
        
        # Create result
        return self._create_result(
            questions, answer_key, qrm_result, passage_result, 
            form_id, num_options
        )
    
    def _build_inline_prompt(
        self,
        qrm_result,
        passage_result,
        num_options: int
    ) -> str:
        """Build prompt without template (fallback)"""
        
        # Format QRM questions
        qrm_text = ""
        for q in qrm_result.questions:
            qrm_text += f"\n{'─' * 80}\n"
            qrm_text += f"Question {q.question_number} ({q.question_type.value}, {q.cognitive_demand})\n"
            qrm_text += f"Evidence Location: {q.evidence_location}\n"
            qrm_text += f"Content Requirement: {q.content_requirement}\n"
            qrm_text += f"Distractor Guidance: {q.distractor_guidance}\n"
        
        return f"""
Generate {qrm_result.total_questions} multiple choice questions for this comprehension passage.

PASSAGE:
{passage_result.passage_text}

QUESTION SPECIFICATIONS (from QRM):
{qrm_text}

CONSTRAINTS:
- Total Questions: {qrm_result.total_questions}
- Answer Options Per Question: {num_options} (from Bank 6 for Grade {qrm_result.grade})
- Grade Level: {qrm_result.grade}
- Genre: {qrm_result.genre}

REQUIREMENTS FOR EACH QUESTION:

1. **Question Text:**
   - Clear, grade-appropriate language
   - Directly tests the requirement from QRM
   - Complete question with proper grammar

2. **Answer Options:**
   - EXACTLY {num_options} options labeled A, B, C, D (or A, B, C for K-2)
   - ONE correct answer
   - {num_options - 1} plausible distractors
   - All options similar length and structure
   - Distractors follow QRM guidance

3. **Distractor Quality:**
   - Use QRM distractor guidance for each question
   - Make distractors plausible but clearly wrong
   - Avoid "all of the above" or "none of the above"
   - Test comprehension, not trick questions

4. **Evidence:**
   - Identify WHERE in passage the answer is found
   - Extract exact text that supports correct answer
   - Evidence must be from passage (not inference for explicit questions)

OUTPUT FORMAT (JSON):
{{
  "questions": [
    {{
      "question_number": 1,
      "question_text": "What is Maya's name?",
      "question_type": "explicit",
      "cognitive_demand": "low",
      "answer_options": [
        {{"letter": "A", "text": "Maya", "is_correct": true, "distractor_type": null}},
        {{"letter": "B", "text": "Jordan", "is_correct": false, "distractor_type": "character_confusion"}},
        {{"letter": "C", "text": "Maria", "is_correct": false, "distractor_type": "similar_name"}}
      ],
      "correct_answer": "A",
      "evidence_location": "beginning",
      "evidence_text": "Maya Rodriguez stood at the entrance of Lincoln Elementary School.",
      "points_possible": 1
    }},
    // ... more questions
  ]
}}

CRITICAL REQUIREMENTS:
- Generate ALL {qrm_result.total_questions} questions
- Follow QRM specifications exactly
- Use EXACTLY {num_options} answer options per question
- Extract evidence directly from passage
- Make distractors plausible using QRM guidance
- Ensure questions span entire passage (beginning, middle, end, throughout)

Generate the questions now:
        """.strip()
    
    def _build_prompt_from_template(
        self,
        qrm_result,
        passage_result,
        num_options: int
    ) -> str:
        """Build prompt using Jinja2 template"""
        return self.template.render(
            qrm=qrm_result,
            passage=passage_result,
            num_options=num_options
        )
    
    def _parse_response(
        self,
        response: str,
        qrm_result,
        num_options: int
    ) -> List[Question]:
        """Parse AI response into Question objects"""
        
        import json
        
        # Extract JSON from response
        json_str = response.strip()
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0].strip()
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0].strip()
        
        data = json.loads(json_str)
        
        # Parse questions
        questions = []
        for q_data in data["questions"]:
            # Parse answer options
            answer_options = []
            for opt_data in q_data["answer_options"]:
                answer_options.append(AnswerOption(
                    letter=opt_data["letter"],
                    text=opt_data["text"],
                    is_correct=opt_data["is_correct"],
                    distractor_type=opt_data.get("distractor_type")
                ))
            
            # Create question
            questions.append(Question(
                question_number=q_data["question_number"],
                question_text=q_data["question_text"],
                question_type=QuestionType(q_data["question_type"]),
                cognitive_demand=q_data["cognitive_demand"],
                answer_options=answer_options,
                correct_answer=q_data["correct_answer"],
                evidence_location=q_data["evidence_location"],
                evidence_text=q_data["evidence_text"],
                points_possible=q_data.get("points_possible", 1)
            ))
        
        return questions
    
    def _create_answer_key(self, questions: List[Question]) -> AnswerKey:
        """Create answer key from questions"""
        
        answer_key_summary = {}
        total_points = 0
        
        for q in questions:
            answer_key_summary[q.question_number] = q.correct_answer
            total_points += q.points_possible
        
        return AnswerKey(
            questions=questions,
            total_questions=len(questions),
            total_points=total_points,
            answer_key_summary=answer_key_summary
        )
    
    def _validate_questions(self, questions: List[Question], qrm_result):
        """Validate questions match QRM specifications"""
        
        # Check total count
        if len(questions) != qrm_result.total_questions:
            print(f"Warning: Generated {len(questions)} questions, expected {qrm_result.total_questions}")
        
        # Check question types
        generated_types = {}
        for q in questions:
            q_type = q.question_type.value
            generated_types[q_type] = generated_types.get(q_type, 0) + 1
        
        for q_type, expected_count in qrm_result.type_distribution.items():
            actual_count = generated_types.get(q_type, 0)
            if actual_count != expected_count:
                print(f"Warning: Type '{q_type}' - expected {expected_count}, got {actual_count}")
        
        # Check cognitive demands
        generated_cognitive = {}
        for q in questions:
            cog = q.cognitive_demand
            generated_cognitive[cog] = generated_cognitive.get(cog, 0) + 1
        
        for cog_level, expected_count in qrm_result.cognitive_distribution.items():
            actual_count = generated_cognitive.get(cog_level, 0)
            if actual_count != expected_count:
                print(f"Warning: Cognitive '{cog_level}' - expected {expected_count}, got {actual_count}")
        
        print(f"✓ Questions validation: {len(questions)}/{qrm_result.total_questions} questions generated")
    
    def _create_result(
        self,
        questions: List[Question],
        answer_key: AnswerKey,
        qrm_result,
        passage_result,
        form_id: str,
        num_options: int
    ) -> QuestionGeneratorResult:
        """Create final result object"""
        
        # Calculate distributions
        type_distribution = {}
        cognitive_distribution = {}
        
        for q in questions:
            q_type = q.question_type.value
            type_distribution[q_type] = type_distribution.get(q_type, 0) + 1
            
            cog = q.cognitive_demand
            cognitive_distribution[cog] = cognitive_distribution.get(cog, 0) + 1
        
        # Track bank usage
        bank_usage = {
            "Bank 4 (Comprehension Blueprint)": "Via QRM for question specifications",
            "Bank 6 (Answer Options)": f"Grade {qrm_result.grade} → {num_options} answer options"
        }
        
        return QuestionGeneratorResult(
            questions=questions,
            total_questions=len(questions),
            answer_key=answer_key,
            grade=qrm_result.grade,
            genre=qrm_result.genre,
            band=qrm_result.band,
            form_id=form_id,
            type_distribution=type_distribution,
            cognitive_distribution=cognitive_distribution,
            qrm_form_id=qrm_result.form_id,
            passage_form_id=passage_result.form_id,
            num_answer_options=num_options,
            generated_at=datetime.now().isoformat(),
            schema_version=self.schema_version,
            bank_usage=bank_usage
        )


def create_question_generator(ai_client):
    """Factory function to create question generator"""
    return QuestionGenerator(ai_client)


# Example usage
if __name__ == "__main__":
    from qrm_generator import create_qrm_generator
    from pib_generator import create_pib_generator
    from comprehension_passage_generator import create_comprehension_passage_generator
    
    # Mock AI client
    class MockAI:
        def complete(self, prompt):
            if "Question Requirement Matrix" in prompt:
                return self._qrm_response()
            elif "Passage Information Bank" in prompt:
                return self._pib_response()
            elif "Generate" in prompt and "multiple choice questions" in prompt:
                return self._questions_response()
            else:
                return self._passage_response()
        
        def _qrm_response(self):
            import json
            return json.dumps({
                "questions": [
                    {"question_number": 1, "question_type": "explicit", "cognitive_demand": "low", "evidence_location": "beginning", "content_requirement": "Maya's name", "distractor_guidance": "other names"},
                    {"question_number": 2, "question_type": "explicit", "cognitive_demand": "low", "evidence_location": "middle", "content_requirement": "tag game", "distractor_guidance": "other games"},
                    {"question_number": 3, "question_type": "implicit", "cognitive_demand": "medium", "evidence_location": "middle", "content_requirement": "Jordan's feelings", "distractor_guidance": "wrong emotions"},
                    {"question_number": 4, "question_type": "implicit", "cognitive_demand": "medium", "evidence_location": "end", "content_requirement": "friendship outcome", "distractor_guidance": "wrong outcomes"},
                    {"question_number": 5, "question_type": "vocabulary", "cognitive_demand": "medium", "evidence_location": "middle", "content_requirement": "hesitant meaning", "distractor_guidance": "wrong definitions"},
                    {"question_number": 6, "question_type": "main_idea", "cognitive_demand": "high", "evidence_location": "throughout", "content_requirement": "theme about kindness", "distractor_guidance": "details not theme"}
                ],
                "total_questions": 6,
                "type_distribution": {"explicit": 2, "implicit": 2, "vocabulary": 1, "main_idea": 1},
                "cognitive_distribution": {"low": 2, "medium": 3, "high": 1},
                "evidence_distribution": {"beginning": 1, "middle": 3, "end": 1, "throughout": 1},
                "required_vocabulary": ["hesitant"],
                "required_content_elements": ["Maya", "Jordan", "tag", "kindness"],
                "required_structure_elements": ["chronological"]
            })
        
        def _pib_response(self):
            import json
            return json.dumps({
                "scenes": [
                    {"scene_number": 1, "scene_type": "opening", "location_in_passage": "beginning", "purpose": "Intro", "content_description": "Maya arrives", "required_details": ["Maya name"], "supports_questions": [1], "vocabulary_placement": []},
                    {"scene_number": 2, "scene_type": "action", "location_in_passage": "middle", "purpose": "Tag game", "content_description": "Maya invites Jordan to tag", "required_details": ["tag game", "hesitant"], "supports_questions": [2, 3, 4], "vocabulary_placement": ["hesitant"]}
                ],
                "total_scenes": 2,
                "characters": [{"name": "Maya", "role": "main", "key_traits": ["kind"], "actions_to_show": ["invites"], "supports_questions": [1, 3]}],
                "opening_hook": "Maya at school",
                "central_conflict_or_topic": "Making friends",
                "resolution_or_conclusion": "Friendship",
                "target_lexile": "300-400L",
                "target_word_count": 125,
                "vocabulary_targets": ["hesitant"],
                "vocabulary_contexts": {"hesitant": "Jordan looks hesitant"},
                "text_structure": "chronological",
                "organizational_features": [],
                "question_coverage_map": {"1": [1], "2": [2], "3": [2], "4": [2]}
            })
        
        def _passage_response(self):
            return """Making New Friends

Maya was excited for second grade. She stood at the school entrance with her red backpack.

At recess, Maya saw a new boy named Jordan. He looked hesitant to join the other kids playing tag. Maya ran over. "Do you want to play?" she asked with a smile.

Jordan nodded and joined the game. By the end of recess, they were both laughing and running together. Maya felt happy she had invited him to play."""
        
        def _questions_response(self):
            import json
            return json.dumps({
                "questions": [
                    {
                        "question_number": 1,
                        "question_text": "What is the main character's name?",
                        "question_type": "explicit",
                        "cognitive_demand": "low",
                        "answer_options": [
                            {"letter": "A", "text": "Maya", "is_correct": True, "distractor_type": None},
                            {"letter": "B", "text": "Jordan", "is_correct": False, "distractor_type": "character_confusion"},
                            {"letter": "C", "text": "Maria", "is_correct": False, "distractor_type": "similar_name"}
                        ],
                        "correct_answer": "A",
                        "evidence_location": "beginning",
                        "evidence_text": "Maya was excited for second grade.",
                        "points_possible": 1
                    },
                    {
                        "question_number": 2,
                        "question_text": "What game did Maya invite Jordan to play?",
                        "question_type": "explicit",
                        "cognitive_demand": "low",
                        "answer_options": [
                            {"letter": "A", "text": "Hide and seek", "is_correct": False, "distractor_type": "other_game"},
                            {"letter": "B", "text": "Tag", "is_correct": True, "distractor_type": None},
                            {"letter": "C", "text": "Kickball", "is_correct": False, "distractor_type": "other_game"}
                        ],
                        "correct_answer": "B",
                        "evidence_location": "middle",
                        "evidence_text": "He looked hesitant to join the other kids playing tag.",
                        "points_possible": 1
                    },
                    {
                        "question_number": 3,
                        "question_text": "How did Jordan feel before Maya invited him to play?",
                        "question_type": "implicit",
                        "cognitive_demand": "medium",
                        "answer_options": [
                            {"letter": "A", "text": "Excited", "is_correct": False, "distractor_type": "opposite"},
                            {"letter": "B", "text": "Unsure", "is_correct": True, "distractor_type": None},
                            {"letter": "C", "text": "Angry", "is_correct": False, "distractor_type": "wrong_emotion"}
                        ],
                        "correct_answer": "B",
                        "evidence_location": "middle",
                        "evidence_text": "He looked hesitant to join the other kids",
                        "points_possible": 1
                    },
                    {
                        "question_number": 4,
                        "question_text": "What happened after Maya invited Jordan to play?",
                        "question_type": "implicit",
                        "cognitive_demand": "medium",
                        "answer_options": [
                            {"letter": "A", "text": "They became friends", "is_correct": True, "distractor_type": None},
                            {"letter": "B", "text": "Jordan went home", "is_correct": False, "distractor_type": "wrong_outcome"},
                            {"letter": "C", "text": "They played alone", "is_correct": False, "distractor_type": "partial_wrong"}
                        ],
                        "correct_answer": "A",
                        "evidence_location": "end",
                        "evidence_text": "By the end of recess, they were both laughing and running together.",
                        "points_possible": 1
                    },
                    {
                        "question_number": 5,
                        "question_text": "What does the word 'hesitant' mean in this story?",
                        "question_type": "vocabulary",
                        "cognitive_demand": "medium",
                        "answer_options": [
                            {"letter": "A", "text": "Excited and ready", "is_correct": False, "distractor_type": "opposite"},
                            {"letter": "B", "text": "Uncertain or unsure", "is_correct": True, "distractor_type": None},
                            {"letter": "C", "text": "Angry and upset", "is_correct": False, "distractor_type": "wrong_emotion"}
                        ],
                        "correct_answer": "B",
                        "evidence_location": "middle",
                        "evidence_text": "He looked hesitant to join the other kids",
                        "points_possible": 1
                    },
                    {
                        "question_number": 6,
                        "question_text": "What is the main idea of this story?",
                        "question_type": "main_idea",
                        "cognitive_demand": "high",
                        "answer_options": [
                            {"letter": "A", "text": "Being kind helps make friends", "is_correct": True, "distractor_type": None},
                            {"letter": "B", "text": "Maya has a red backpack", "is_correct": False, "distractor_type": "detail_not_main"},
                            {"letter": "C", "text": "Recess is fun", "is_correct": False, "distractor_type": "too_general"}
                        ],
                        "correct_answer": "A",
                        "evidence_location": "throughout",
                        "evidence_text": "Maya felt happy she had invited him to play.",
                        "points_possible": 1
                    }
                ]
            })
    
    mock_ai = MockAI()
    
    print("=" * 80)
    print("QUESTION GENERATOR TEST")
    print("=" * 80)
    
    # Step 1: Generate QRM
    print("\n[STEP 1] Generating QRM...")
    qrm_gen = create_qrm_generator(mock_ai)
    qrm = qrm_gen.generate(grade="2", genre="narrative", band="early")
    print(f"✓ QRM: {qrm.total_questions} questions planned")
    
    # Step 2: Generate PIB
    print("\n[STEP 2] Generating PIB...")
    pib_gen = create_pib_generator(mock_ai)
    pib = pib_gen.generate(qrm_result=qrm)
    print(f"✓ PIB: {pib.total_scenes} scenes planned")
    
    # Step 3: Generate Passage
    print("\n[STEP 3] Generating Passage...")
    passage_gen = create_comprehension_passage_generator(mock_ai)
    passage = passage_gen.generate(qrm_result=qrm, pib_result=pib)
    print(f"✓ Passage: {passage.actual_word_count} words")
    
    # Step 4: Generate Questions
    print("\n[STEP 4] Generating Questions...")
    question_gen = create_question_generator(mock_ai)
    result = question_gen.generate(qrm_result=qrm, passage_result=passage)
    
    print("\n" + "=" * 80)
    print("QUESTIONS GENERATED SUCCESSFULLY")
    print("=" * 80)
    print(f"\nForm ID: {result.form_id}")
    print(f"Total Questions: {result.total_questions}")
    print(f"Answer Options: {result.num_answer_options} (Grade {result.grade} from Bank 6)")
    print(f"Total Points: {result.answer_key.total_points}")
    
    print(f"\nType Distribution:")
    for q_type, count in result.type_distribution.items():
        print(f"  {q_type}: {count}")
    
    print(f"\nCognitive Distribution:")
    for cog, count in result.cognitive_distribution.items():
        print(f"  {cog}: {count}")
    
    print(f"\nBank Usage:")
    for bank, usage in result.bank_usage.items():
        print(f"  - {bank}: {usage}")
    
    print("\n" + "=" * 80)
    print("SAMPLE QUESTIONS")
    print("=" * 80)
    
    for q in result.questions[:2]:  # Show first 2 questions
        print(f"\n{'─' * 80}")
        print(f"Question {q.question_number} ({q.question_type.value}, {q.cognitive_demand})")
        print(f"{'─' * 80}")
        print(f"{q.question_text}\n")
        for opt in q.answer_options:
            marker = "✓" if opt.is_correct else " "
            print(f"  [{marker}] {opt.letter}. {opt.text}")
        print(f"\nCorrect Answer: {q.correct_answer}")
        print(f"Evidence: \"{q.evidence_text}\"")
    
    print("\n" + "=" * 80)
    print("ANSWER KEY")
    print("=" * 80)
    for q_num, answer in result.answer_key.answer_key_summary.items():
        print(f"  Question {q_num}: {answer}")
    
    print("\n" + "=" * 80)
    print("COMPLETE WORKFLOW")
    print("=" * 80)
    print(f"""
✓ Step 1 (QRM): {qrm.total_questions} questions planned
✓ Step 2 (PIB): {pib.total_scenes} scenes blueprinted  
✓ Step 3 (Passage): {passage.actual_word_count}-word passage written
✓ Step 4 (Questions): {result.total_questions} questions with answer key

Complete Assessment Package:
  - QRM Form: {result.qrm_form_id}
  - PIB Form: {pib.form_id}
  - Passage Form: {result.passage_form_id}
  - Questions Form: {result.form_id}
  
Ready for: Packaging into complete assessment document
    """)
