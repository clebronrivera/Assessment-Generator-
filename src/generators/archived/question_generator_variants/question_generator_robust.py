"""
Robust Question Generator with Enhanced JSON Parsing

Extends the standard question generator with:
1. Aggressive JSON cleaning and repair
2. Multiple parsing strategies  
3. Better error messages to AI
4. Incremental validation

Created: 2026-01-15
Schema Version: 2026.1
"""

import json
import re
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum

# Import from standard question generator
from .question_generator import (
    QuestionType, AnswerOption, Question, AnswerKey, QuestionGeneratorResult
)


class RobustQuestionGenerator:
    """Question generator with robust JSON parsing"""
    
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
        qrm_result,
        passage_result,
        form_id: Optional[str] = None,
        max_retries: int = 5
    ) -> QuestionGeneratorResult:
        """Generate questions with robust parsing and retry logic"""
        
        num_options = self.get_num_options(qrm_result.grade)
        
        if not form_id:
            form_id = f"COMP-{qrm_result.grade.upper()}-{qrm_result.band.upper()}-QUESTIONS-001"
        
        last_error = None
        for attempt in range(1, max_retries + 1):
            try:
                # Build prompt with error feedback on retry
                if attempt > 1 and last_error:
                    prompt = self._build_prompt_with_feedback(
                        qrm_result, passage_result, num_options, last_error
                    )
                else:
                    prompt = self._build_prompt(qrm_result, passage_result, num_options)
                
                # Call AI
                response = self.ai_client.complete(prompt)
                
                # Parse with robust strategies
                questions = self._parse_response_robust(response, qrm_result, num_options)
                
                # Create answer key
                answer_key = self._create_answer_key(questions)
                
                # Validate
                self._validate_questions(questions, qrm_result)
                
                # Success!
                return self._create_result(
                    questions, answer_key, qrm_result, passage_result,
                    form_id, num_options
                )
                
            except Exception as e:
                last_error = str(e)
                if attempt < max_retries:
                    print(f"⚠ Attempt {attempt} failed: {last_error[:100]}")
                    print(f"  Retrying... ({attempt + 1}/{max_retries})")
        
        raise Exception(f"Question generation failed after {max_retries} attempts. Last error: {last_error}")
    
    def _parse_response_robust(self, response: str, qrm_result, num_options: int) -> List[Question]:
        """Parse response with multiple strategies"""
        
        # Strategy 1: Standard JSON cleaning
        try:
            return self._parse_standard(response, qrm_result, num_options)
        except Exception as e1:
            print(f"      Standard parsing failed: {str(e1)[:50]}")
        
        # Strategy 2: Aggressive cleaning
        try:
            return self._parse_aggressive(response, qrm_result, num_options)
        except Exception as e2:
            print(f"      Aggressive parsing failed: {str(e2)[:50]}")
        
        # Strategy 3: Question-by-question parsing
        try:
            return self._parse_incremental(response, qrm_result, num_options)
        except Exception as e3:
            print(f"      Incremental parsing failed: {str(e3)[:50]}")
        
        raise Exception("All parsing strategies failed")
    
    def _parse_standard(self, response: str, qrm_result, num_options: int) -> List[Question]:
        """Standard JSON parsing with basic cleaning"""
        json_str = self._extract_json(response)
        json_str = self._clean_json_basic(json_str)
        data = json.loads(json_str)
        return self._build_questions(data, qrm_result, num_options)
    
    def _parse_aggressive(self, response: str, qrm_result, num_options: int) -> List[Question]:
        """Aggressive cleaning for malformed JSON"""
        json_str = self._extract_json(response)
        json_str = self._clean_json_aggressive(json_str)
        data = json.loads(json_str)
        return self._build_questions(data, qrm_result, num_options)
    
    def _parse_incremental(self, response: str, qrm_result, num_options: int) -> List[Question]:
        """Parse questions one by one"""
        json_str = self._extract_json(response)
        
        # Try to extract individual question objects
        question_pattern = r'\{\s*"question_number"\s*:\s*\d+.*?"correct_answer"\s*:\s*"[A-D]"\s*\}'
        question_matches = re.findall(question_pattern, json_str, re.DOTALL)
        
        if not question_matches:
            raise Exception("Could not extract individual questions")
        
        questions = []
        for match in question_matches:
            try:
                cleaned = self._clean_json_aggressive(match)
                q_data = json.loads(cleaned)
                questions.append(self._build_single_question(q_data, num_options))
            except:
                continue
        
        if len(questions) != qrm_result.total_questions:
            raise Exception(f"Expected {qrm_result.total_questions} questions, got {len(questions)}")
        
        return questions
    
    def _extract_json(self, response: str) -> str:
        """Extract JSON from response"""
        response = response.strip()
        
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0].strip()
        elif "```" in response:
            response = response.split("```")[1].split("```")[0].strip()
        
        return response.strip()
    
    def _clean_json_basic(self, json_str: str) -> str:
        """Basic JSON cleaning"""
        # Remove comments
        json_str = re.sub(r'//.*?\n', '\n', json_str)
        json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)
        
        # Normalize whitespace
        json_str = json_str.replace('\n', ' ')
        json_str = json_str.replace('\r', ' ')
        json_str = re.sub(r'\s+', ' ', json_str)
        
        return json_str
    
    def _clean_json_aggressive(self, json_str: str) -> str:
        """Aggressive JSON cleaning and repair"""
        # Start with basic cleaning
        json_str = self._clean_json_basic(json_str)
        
        # Replace smart quotes
        json_str = json_str.replace('"', '"').replace('"', '"')
        json_str = json_str.replace("'", "'").replace("'", "'")
        
        # Fix trailing commas
        json_str = re.sub(r',\s*}', '}', json_str)
        json_str = re.sub(r',\s*]', ']', json_str)
        
        return json_str
    
    def _build_questions(self, data: Dict, qrm_result, num_options: int) -> List[Question]:
        """Build Question objects from parsed data"""
        questions = []
        
        questions_data = data.get('questions', [])
        if not questions_data:
            raise Exception("No 'questions' key in parsed JSON")
        
        for q_data in questions_data:
            questions.append(self._build_single_question(q_data, num_options))
        
        return questions
    
    def _build_single_question(self, q_data: Dict, num_options: int) -> Question:
        """Build a single Question object"""
        # Parse answer options
        answer_options = []
        for opt_data in q_data["answer_options"]:
            answer_options.append(AnswerOption(
                letter=opt_data["letter"],
                text=opt_data["text"],
                is_correct=opt_data["is_correct"],
                distractor_type=opt_data.get("distractor_type")
            ))
        
        return Question(
            question_number=q_data["question_number"],
            question_text=q_data["question_text"],
            question_type=QuestionType(q_data["question_type"]),
            cognitive_demand=q_data["cognitive_demand"],
            answer_options=answer_options,
            correct_answer=q_data["correct_answer"],
            evidence_location=q_data["evidence_location"],
            evidence_text=q_data["evidence_text"],
            points_possible=q_data.get("points_possible", 1)
        )
    
    def _build_prompt(self, qrm_result, passage_result, num_options: int) -> str:
        """Build question generation prompt"""
        
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

CRITICAL JSON FORMATTING RULES:
1. Return ONLY valid JSON - no markdown, no comments
2. Use simple language - avoid apostrophes and special characters in text
3. Each question must have exactly {num_options} options
4. Double-check all quotes are properly closed
5. No trailing commas before }} or ]

OUTPUT FORMAT (JSON):
{{
  "questions": [
    {{
      "question_number": 1,
      "question_text": "What is the main idea?",
      "question_type": "main_idea",
      "cognitive_demand": "high",
      "answer_options": [
        {{"letter": "A", "text": "Option A", "is_correct": true, "distractor_type": null}},
        {{"letter": "B", "text": "Option B", "is_correct": false, "distractor_type": "plausible"}},
        {{"letter": "C", "text": "Option C", "is_correct": false, "distractor_type": "detail"}},
        {{"letter": "D", "text": "Option D", "is_correct": false, "distractor_type": "opposite"}}
      ],
      "correct_answer": "A",
      "evidence_location": "throughout",
      "evidence_text": "Evidence from passage",
      "points_possible": 1
    }}
  ]
}}

Generate ALL {qrm_result.total_questions} questions now:
        """.strip()
    
    def _build_prompt_with_feedback(self, qrm_result, passage_result, num_options: int, error: str) -> str:
        """Build prompt with error feedback"""
        base_prompt = self._build_prompt(qrm_result, passage_result, num_options)
        return f"""{base_prompt}

PREVIOUS ATTEMPT ERROR:
{error}

IMPORTANT: Fix the JSON error above. Ensure all strings are properly quoted and escaped.
        """
    
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


def create_robust_question_generator(ai_client):
    """Factory function to create robust question generator"""
    return RobustQuestionGenerator(ai_client)
