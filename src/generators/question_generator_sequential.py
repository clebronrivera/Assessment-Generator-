"""
Sequential Question Generator - One Question at a Time

Generates questions individually instead of in batch to avoid JSON parsing issues.
This is more reliable but slower due to multiple AI calls.

Created: 2026-01-15
Schema Version: 2026.1
"""

import json
import re
from typing import List, Dict, Any, Optional
from datetime import datetime

# Import from standard question generator
from .question_generator import (
    QuestionType, AnswerOption, Question, AnswerKey, QuestionGeneratorResult
)


class SequentialQuestionGenerator:
    """Generates questions one at a time for maximum reliability"""
    
    def __init__(self, ai_client):
        """Initialize with AI client and bank access"""
        self.ai_client = ai_client
        self.schema_version = "2026.1"
        self._load_banks()
    
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
        if grade in ["K", "1", "2"]:
            return 3
        else:
            return 4
    
    def generate(
        self,
        qrm_result,
        passage_result,
        form_id: Optional[str] = None,
        max_retries: int = 3
    ) -> QuestionGeneratorResult:
        """Generate questions one at a time"""
        
        num_options = self.get_num_options(qrm_result.grade)
        
        if not form_id:
            form_id = f"COMP-{qrm_result.grade.upper()}-{qrm_result.band.upper()}-QUESTIONS-001"
        
        print(f"   Generating {qrm_result.total_questions} questions sequentially...")
        
        questions = []
        for i, qrm_question in enumerate(qrm_result.questions, 1):
            print(f"   [{i}/{qrm_result.total_questions}] Generating question {qrm_question.question_number}...")
            
            question = self._generate_single_question(
                qrm_question, passage_result, num_options, max_retries
            )
            questions.append(question)
        
        # Create answer key
        answer_key = self._create_answer_key(questions)
        
        # Validate
        self._validate_questions(questions, qrm_result)
        
        # Create result
        return self._create_result(
            questions, answer_key, qrm_result, passage_result,
            form_id, num_options
        )
    
    def _generate_single_question(
        self,
        qrm_question,
        passage_result,
        num_options: int,
        max_retries: int
    ) -> Question:
        """Generate a single question with retry logic"""
        
        last_error = None
        for attempt in range(1, max_retries + 1):
            try:
                prompt = self._build_single_question_prompt(
                    qrm_question, passage_result, num_options, last_error
                )
                
                response = self.ai_client.complete(prompt)
                question = self._parse_single_question(response, num_options)
                
                return question
                
            except Exception as e:
                last_error = str(e)
                if attempt < max_retries:
                    print(f"      Retry {attempt}/{max_retries}: {str(e)[:50]}")
        
        raise Exception(f"Failed to generate question {qrm_question.question_number} after {max_retries} attempts")
    
    def _build_single_question_prompt(
        self,
        qrm_question,
        passage_result,
        num_options: int,
        last_error: Optional[str] = None
    ) -> str:
        """Build prompt for a single question"""
        
        error_feedback = ""
        if last_error:
            error_feedback = f"""
PREVIOUS ATTEMPT ERROR:
{last_error}

IMPORTANT: Fix the JSON error. Ensure all strings are properly quoted.
"""
        
        return f"""Generate ONE multiple choice question for this passage.

PASSAGE:
{passage_result.passage_text}

QUESTION SPECIFICATION:
- Question Number: {qrm_question.question_number}
- Type: {qrm_question.question_type.value}
- Cognitive Demand: {qrm_question.cognitive_demand}
- Evidence Location: {qrm_question.evidence_location}
- Content Requirement: {qrm_question.content_requirement}
- Distractor Guidance: {qrm_question.distractor_guidance}

REQUIREMENTS:
1. Create {num_options} answer options (A, B, C, D)
2. ONE correct answer
3. {num_options - 1} plausible distractors based on guidance
4. Extract evidence text from passage
5. Use simple language - avoid apostrophes and special characters

Return ONLY this JSON (no markdown, no comments):
{{
  "question_number": {qrm_question.question_number},
  "question_text": "Your question here",
  "question_type": "{qrm_question.question_type.value}",
  "cognitive_demand": "{qrm_question.cognitive_demand}",
  "answer_options": [
    {{"letter": "A", "text": "Option A", "is_correct": true, "distractor_type": null}},
    {{"letter": "B", "text": "Option B", "is_correct": false, "distractor_type": "plausible"}},
    {{"letter": "C", "text": "Option C", "is_correct": false, "distractor_type": "detail"}},
    {{"letter": "D", "text": "Option D", "is_correct": false, "distractor_type": "opposite"}}
  ],
  "correct_answer": "A",
  "evidence_location": "{qrm_question.evidence_location}",
  "evidence_text": "Exact text from passage",
  "points_possible": 1
}}
{error_feedback}"""
    
    def _parse_single_question(self, response: str, num_options: int) -> Question:
        """Parse a single question from AI response"""
        
        # Extract JSON
        json_str = response.strip()
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0].strip()
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0].strip()
        
        # Clean JSON
        json_str = self._clean_json(json_str)
        
        # Parse
        data = json.loads(json_str)
        
        # Build question
        answer_options = []
        for opt_data in data["answer_options"]:
            answer_options.append(AnswerOption(
                letter=opt_data["letter"],
                text=opt_data["text"],
                is_correct=opt_data["is_correct"],
                distractor_type=opt_data.get("distractor_type")
            ))
        
        return Question(
            question_number=data["question_number"],
            question_text=data["question_text"],
            question_type=QuestionType(data["question_type"]),
            cognitive_demand=data["cognitive_demand"],
            answer_options=answer_options,
            correct_answer=data["correct_answer"],
            evidence_location=data["evidence_location"],
            evidence_text=data["evidence_text"],
            points_possible=data.get("points_possible", 1)
        )
    
    def _clean_json(self, json_str: str) -> str:
        """Clean JSON string"""
        # Remove comments
        json_str = re.sub(r'//.*?\n', '\n', json_str)
        json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)
        
        # Replace smart quotes
        json_str = json_str.replace('"', '"').replace('"', '"')
        json_str = json_str.replace("'", "'").replace("'", "'")
        
        # Fix trailing commas
        json_str = re.sub(r',\s*}', '}', json_str)
        json_str = re.sub(r',\s*]', ']', json_str)
        
        return json_str
    
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
        if len(questions) != qrm_result.total_questions:
            print(f"Warning: Generated {len(questions)} questions, expected {qrm_result.total_questions}")
        
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


def create_sequential_question_generator(ai_client):
    """Factory function to create sequential question generator"""
    return SequentialQuestionGenerator(ai_client)
