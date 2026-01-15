"""
QRM (Question Requirement Matrix) Generator

Generates a structured plan of questions BEFORE passage creation to ensure all
questions will be answerable from the passage content.

Bank Usage:
- Bank 4 (comprehension_blueprint.py): Question specifications by grade

Purpose:
- Pre-passage planning step
- Defines required question types and cognitive demands
- Ensures passage will support all questions
- Feeds into PIB (Passage Information Bank) generator

Created: 2026-01-12
Schema Version: 2026.1
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum


class QuestionType(Enum):
    """Question types from Bank 4"""
    EXPLICIT = "explicit"
    IMPLICIT = "implicit"
    VOCABULARY = "vocabulary"
    MAIN_IDEA = "main_idea"
    TEXT_STRUCTURE = "text_structure"
    INFERENCE_ADVANCED = "inference_advanced"
    AUTHORS_PURPOSE = "authors_purpose"
    COMPARE_CONTRAST = "compare_contrast"
    CAUSE_EFFECT = "cause_effect"
    SEQUENCE = "sequence"
    PICTURE_BASED = "picture_based"


class CognitiveDemand(Enum):
    """Cognitive complexity levels"""
    LOW = "low"  # Recall, locate
    MEDIUM = "medium"  # Understand, interpret
    HIGH = "high"  # Analyze, synthesize, evaluate


@dataclass
class QuestionRequirement:
    """Single question specification in the matrix"""
    question_number: int
    question_type: QuestionType
    cognitive_demand: CognitiveDemand
    evidence_location: str  # Where in passage (beginning/middle/end/throughout)
    content_requirement: str  # What passage must contain to answer this
    distractor_guidance: str  # How to create wrong answers
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "question_number": self.question_number,
            "question_type": self.question_type.value,
            "cognitive_demand": self.cognitive_demand.value,
            "evidence_location": self.evidence_location,
            "content_requirement": self.content_requirement,
            "distractor_guidance": self.distractor_guidance
        }


@dataclass
class QRMResult:
    """Complete Question Requirement Matrix"""
    
    # Question specifications
    questions: List[QuestionRequirement]
    total_questions: int
    
    # Distribution analysis
    type_distribution: Dict[str, int]  # question_type -> count
    cognitive_distribution: Dict[str, int]  # cognitive_level -> count
    evidence_distribution: Dict[str, int]  # location -> count
    
    # Passage requirements derived from questions
    required_content_elements: List[str]  # What passage must include
    required_vocabulary: List[str]  # Target words for vocabulary questions
    required_structure_elements: List[str]  # Organizational features needed
    
    # Metadata
    grade: str
    genre: str  # narrative/nonfiction
    band: str  # early/late
    form_id: str
    generated_at: str
    schema_version: str
    bank_usage: Dict[str, str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "questions": [q.to_dict() for q in self.questions],
            "total_questions": self.total_questions,
            "type_distribution": self.type_distribution,
            "cognitive_distribution": self.cognitive_distribution,
            "evidence_distribution": self.evidence_distribution,
            "required_content_elements": self.required_content_elements,
            "required_vocabulary": self.required_vocabulary,
            "required_structure_elements": self.required_structure_elements,
            "grade": self.grade,
            "genre": self.genre,
            "band": self.band,
            "form_id": self.form_id,
            "generated_at": self.generated_at,
            "schema_version": self.schema_version,
            "bank_usage": self.bank_usage
        }


class QRMGenerator:
    """
    Generates Question Requirement Matrix using AI with Bank 4 constraints.
    
    This is the FIRST step in comprehension passage generation:
    1. QRM: Define what questions need to be asked
    2. PIB: Define what content passage needs to answer questions
    3. Passage: Write passage with required content
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
            from src.banks import get_blueprint
            self.get_blueprint = get_blueprint
        except ImportError:
            print("Warning: Could not import banks, using mock data")
            self.get_blueprint = self._mock_get_blueprint
    
    def _mock_get_blueprint(self, grade: str) -> Dict[str, Any]:
        """Mock bank data for testing"""
        # Simplified mock - real Bank 4 has full specifications
        # Return a simple object that has attributes
        from types import SimpleNamespace
        return SimpleNamespace(
            total_questions=6,
            distribution=SimpleNamespace(
                to_dict=lambda: {
                    "explicit": 2,
                    "implicit": 2,
                    "vocabulary": 1,
                    "main_idea": 1
                }
            ),
            cognitive_demands=SimpleNamespace(
                to_dict=lambda: {
                    "low": 2,
                    "medium": 3,
                    "high": 1
                }
            )
        )
    
    def _load_template(self):
        """Load Jinja2 template for QRM prompt"""
        try:
            from src.utils import load_template
            self.template = load_template("comp_qrm.j2")
        except ImportError:
            # Fallback template if utils not available
            self.template = None
            print("Warning: Template loader not available, using inline prompt")
    
    def generate(
        self,
        grade: str,
        genre: str,
        band: str,
        topic: Optional[str] = None,
        form_id: Optional[str] = None,
        max_retries: int = 3
    ) -> QRMResult:
        """
        Generate Question Requirement Matrix with retry logic.
        
        Args:
            grade: Grade level (K-8+)
            genre: "narrative" or "nonfiction"
            band: "early" or "late"
            topic: Optional topic guidance (e.g., "animals", "space")
            form_id: Optional form identifier
            max_retries: Maximum number of retry attempts (default: 3)
        
        Returns:
            QRMResult with complete question specifications
        """
        
        # Get question specifications from Bank 4
        blueprint_obj = self.get_blueprint(grade)
        
        # Convert to dict for easier access
        blueprint = {
            "total_questions": blueprint_obj.total_questions,
            "question_types": blueprint_obj.distribution.to_dict(),
            "cognitive_demands": blueprint_obj.cognitive_demands.to_dict()
        }
        
        # Generate form ID if not provided
        if not form_id:
            import time, random
            ts = int(time.time() * 1000)
            rng = random.randint(1000, 9999)
            form_id = f"COMP-{grade.upper()}-{band.upper()}-QRM-{ts}-{rng}"
        
        # Retry loop
        last_error = None
        for attempt in range(max_retries):
            try:
                # Build prompt from template or inline
                if self.template:
                    prompt = self._build_prompt_from_template(
                        grade, genre, band, topic, blueprint, last_error
                    )
                else:
                    prompt = self._build_inline_prompt(
                        grade, genre, band, topic, blueprint, last_error
                    )
                
                # Call AI to generate QRM
                response = self.ai_client.complete(prompt)
                
                # Parse response into structured QRM
                qrm_result = self._parse_response(
                    response, grade, genre, band, form_id, blueprint
                )
                
                # Validate QRM meets bank requirements
                self._validate_qrm(qrm_result, blueprint)
                
                # Success!
                if attempt > 0:
                    print(f"✓ QRM generated successfully on attempt {attempt + 1}")
                return qrm_result
                
            except ValueError as e:
                last_error = str(e)
                if attempt < max_retries - 1:
                    print(f"⚠ Attempt {attempt + 1} failed: {last_error}")
                    print(f"  Retrying... ({attempt + 2}/{max_retries})")
                else:
                    print(f"❌ All {max_retries} attempts failed")
                    raise
    
    def _build_inline_prompt(
        self,
        grade: str,
        genre: str,
        band: str,
        topic: Optional[str],
        blueprint: Dict[str, Any],
        last_error: Optional[str] = None
    ) -> str:
        """Build prompt without template (fallback)"""
        
        topic_guidance = f"\nTopic: {topic}" if topic else ""
        
        error_feedback = ""
        if last_error:
            error_feedback = f"""
⚠️ PREVIOUS ATTEMPT FAILED WITH ERROR:
{last_error}

PLEASE FIX THIS ERROR IN YOUR RESPONSE. Pay special attention to matching the EXACT counts specified in the distributions above.
"""
        
        return f"""
Generate a Question Requirement Matrix (QRM) for a comprehension assessment.

SPECIFICATIONS FROM BANK 4:
Grade: {grade}
Genre: {genre}
Band: {band}{topic_guidance}
Total Questions: {blueprint['total_questions']}
Question Type Distribution: {blueprint['question_types']}
Cognitive Demand Distribution: {blueprint['cognitive_demands']}
{error_feedback}
YOUR TASK:
Create a detailed plan for {blueprint['total_questions']} questions that will test 
comprehension of a passage that hasn't been written yet. For each question, specify:

1. Question Type: {', '.join(blueprint['question_types'].keys())}
2. Cognitive Demand: low/medium/high
3. Evidence Location: where in passage the answer will be found
4. Content Requirement: what the passage MUST contain to make this question answerable
5. Distractor Guidance: how to create plausible wrong answers

CRITICAL CONSTRAINTS:
- MUST match exact counts from Bank 4 distribution above
- Questions must span beginning, middle, and end of passage
- Content requirements must be specific enough to guide passage writing
- For vocabulary questions, specify the target word type and context needed
- For implicit questions, specify what must be stated vs. inferred

OUTPUT FORMAT (JSON):
{{
  "questions": [
    {{
      "question_number": 1,
      "question_type": "explicit",
      "cognitive_demand": "low",
      "evidence_location": "beginning",
      "content_requirement": "Passage must state the main character's name and age in the first paragraph",
      "distractor_guidance": "Use other character names from the passage; use ages close to correct answer"
    }},
    // ... more questions
  ],
  "required_content_elements": [
    "Character introduction with name and age",
    "Setting description (time and place)",
    // ... more elements
  ],
  "required_vocabulary": ["resilient", "abundant"],  // if vocab questions
  "required_structure_elements": ["chronological sequence", "cause-effect relationship"]
}}

Generate the QRM now:
        """.strip()
    
    def _build_prompt_from_template(
        self,
        grade: str,
        genre: str,
        band: str,
        topic: Optional[str],
        blueprint: Dict[str, Any],
        last_error: Optional[str] = None
    ) -> str:
        """Build prompt using Jinja2 template"""
        return self.template.render(
            grade=grade,
            genre=genre,
            band=band,
            topic=topic,
            blueprint=blueprint,
            last_error=last_error
        )
    
    def _parse_response(
        self,
        response: str,
        grade: str,
        genre: str,
        band: str,
        form_id: str,
        blueprint: Dict[str, Any]
    ) -> QRMResult:
        """Parse AI response into QRMResult structure"""
        
        import json
        
        # Extract JSON from response (handle markdown fences)
        json_str = response.strip()
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0].strip()
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0].strip()
        
        data = json.loads(json_str)
        
        # Parse questions
        questions = []
        for q_data in data["questions"]:
            questions.append(QuestionRequirement(
                question_number=q_data["question_number"],
                question_type=QuestionType(q_data["question_type"]),
                cognitive_demand=CognitiveDemand(q_data["cognitive_demand"]),
                evidence_location=q_data["evidence_location"],
                content_requirement=q_data["content_requirement"],
                distractor_guidance=q_data["distractor_guidance"]
            ))
        
        # Calculate distributions
        type_dist = {}
        cognitive_dist = {}
        evidence_dist = {}
        
        for q in questions:
            type_dist[q.question_type.value] = type_dist.get(q.question_type.value, 0) + 1
            cognitive_dist[q.cognitive_demand.value] = cognitive_dist.get(q.cognitive_demand.value, 0) + 1
            evidence_dist[q.evidence_location] = evidence_dist.get(q.evidence_location, 0) + 1
        
        # Track bank usage
        bank_usage = {
            "Bank 4 (Comprehension Blueprint)": f"Grade {grade} question specifications"
        }
        
        return QRMResult(
            questions=questions,
            total_questions=len(questions),
            type_distribution=type_dist,
            cognitive_distribution=cognitive_dist,
            evidence_distribution=evidence_dist,
            required_content_elements=data.get("required_content_elements", []),
            required_vocabulary=data.get("required_vocabulary", []),
            required_structure_elements=data.get("required_structure_elements", []),
            grade=grade,
            genre=genre,
            band=band,
            form_id=form_id,
            generated_at=datetime.now().isoformat(),
            schema_version=self.schema_version,
            bank_usage=bank_usage
        )
    
    def _validate_qrm(self, qrm: QRMResult, blueprint: Dict[str, Any]):
        """Validate QRM matches Bank 4 requirements"""
        
        # Check total questions
        if qrm.total_questions != blueprint["total_questions"]:
            raise ValueError(
                f"Question count mismatch: got {qrm.total_questions}, "
                f"expected {blueprint['total_questions']}"
            )
        
        # Check question type distribution
        for q_type, expected_count in blueprint["question_types"].items():
            actual_count = qrm.type_distribution.get(q_type, 0)
            if actual_count != expected_count:
                raise ValueError(
                    f"Question type '{q_type}' count mismatch: "
                    f"got {actual_count}, expected {expected_count}"
                )
        
        # Check cognitive demand distribution
        for demand, expected_count in blueprint["cognitive_demands"].items():
            actual_count = qrm.cognitive_distribution.get(demand, 0)
            if actual_count != expected_count:
                raise ValueError(
                    f"Cognitive demand '{demand}' count mismatch: "
                    f"got {actual_count}, expected {expected_count}"
                )
        
        print(f"✓ QRM validation passed - matches Bank 4 specifications")


def create_qrm_generator(ai_client):
    """Factory function to create QRM generator"""
    return QRMGenerator(ai_client)


# Example usage
if __name__ == "__main__":
    # Mock AI client for testing
    class MockAI:
        def complete(self, prompt):
            return '''
{
  "questions": [
    {
      "question_number": 1,
      "question_type": "explicit",
      "cognitive_demand": "low",
      "evidence_location": "beginning",
      "content_requirement": "Passage must state the main character's name in first paragraph",
      "distractor_guidance": "Use other character names; use similar-sounding names"
    },
    {
      "question_number": 2,
      "question_type": "explicit",
      "cognitive_demand": "low",
      "evidence_location": "middle",
      "content_requirement": "Passage must describe what the character did at school",
      "distractor_guidance": "Use activities mentioned but not done by this character"
    },
    {
      "question_number": 3,
      "question_type": "implicit",
      "cognitive_demand": "medium",
      "evidence_location": "throughout",
      "content_requirement": "Character's actions must show they are brave (stated actions, reader infers trait)",
      "distractor_guidance": "Use other personality traits that could fit but aren't supported"
    },
    {
      "question_number": 4,
      "question_type": "implicit",
      "cognitive_demand": "medium",
      "evidence_location": "end",
      "content_requirement": "Passage must show cause-effect: character's choice leads to specific outcome",
      "distractor_guidance": "Use other outcomes mentioned; use logical but unsupported outcomes"
    },
    {
      "question_number": 5,
      "question_type": "vocabulary",
      "cognitive_demand": "medium",
      "evidence_location": "middle",
      "content_requirement": "Include grade-appropriate word with strong context clues (synonyms, examples)",
      "distractor_guidance": "Use words with similar sounds; use words from same semantic field"
    },
    {
      "question_number": 6,
      "question_type": "main_idea",
      "cognitive_demand": "high",
      "evidence_location": "throughout",
      "content_requirement": "Passage must have clear central message supported by multiple details",
      "distractor_guidance": "Use details from passage; use overly specific statements; use unsupported generalizations"
    }
  ],
  "required_content_elements": [
    "Character introduction with name",
    "School setting",
    "Actions demonstrating bravery",
    "Choice with clear consequences",
    "Target vocabulary word with context clues",
    "Central theme about courage/growth"
  ],
  "required_vocabulary": ["determined"],
  "required_structure_elements": ["chronological sequence", "cause-effect relationship"]
}
            '''
    
    # Create generator
    mock_ai = MockAI()
    generator = create_qrm_generator(mock_ai)
    
    # Generate QRM
    print("=" * 80)
    print("QRM GENERATOR TEST")
    print("=" * 80)
    
    qrm = generator.generate(
        grade="2",
        genre="narrative",
        band="early",
        topic="school adventure"
    )
    
    print(f"\n✓ QRM Generated Successfully")
    print(f"  Grade: {qrm.grade}")
    print(f"  Genre: {qrm.genre}")
    print(f"  Band: {qrm.band}")
    print(f"  Total Questions: {qrm.total_questions}")
    print(f"\n  Type Distribution: {qrm.type_distribution}")
    print(f"  Cognitive Distribution: {qrm.cognitive_distribution}")
    print(f"  Evidence Distribution: {qrm.evidence_distribution}")
    
    print(f"\n  Required Content Elements:")
    for elem in qrm.required_content_elements:
        print(f"    - {elem}")
    
    print(f"\n  Required Vocabulary: {qrm.required_vocabulary}")
    print(f"  Required Structure: {qrm.required_structure_elements}")
    
    print(f"\n  Bank Usage: {qrm.bank_usage}")
    
    print("\n" + "=" * 80)
    print("QUESTION DETAILS")
    print("=" * 80)
    for q in qrm.questions:
        print(f"\nQ{q.question_number}: {q.question_type.value} ({q.cognitive_demand.value})")
        print(f"  Location: {q.evidence_location}")
        print(f"  Requirement: {q.content_requirement}")
        print(f"  Distractors: {q.distractor_guidance}")
