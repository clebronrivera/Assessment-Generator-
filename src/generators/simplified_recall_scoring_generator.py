"""
Simplified Recall Scoring Generator

Generates simplified recall scoring guides using character + key detail approach.
Each sentence gets a simple 2-point scoring:
- 2 points: Character name + key detail
- 1 point: Either character name OR key detail  
- 0 points: Neither

This simplified approach:
1. Reduces JSON complexity (6x fewer fields)
2. Makes AI responses more reliable
3. Creates practical, assessor-friendly scoring guides
4. Matches real-world teacher scoring practices

Created: 2026-01-14
Author: Simplified from original recall_scoring_generator.py
"""

from dataclasses import dataclass
from typing import List
import json
import re
from datetime import datetime


@dataclass
class SimplifiedSentenceScoring:
    """Simplified sentence scoring - just character + detail"""
    sentence_number: int
    sentence_text: str
    character_name: str  # Who is this sentence about
    key_detail: str  # What happened / what's important
    scoring_note: str  # Simple guide for assessor
    max_points: int = 2  # Always 2 points per sentence


@dataclass
class SimplifiedRecallGuide:
    """Simplified recall scoring guide"""
    total_sentences: int
    max_total_points: int  # total_sentences * 2
    sentences: List[SimplifiedSentenceScoring]
    general_instructions: str
    
    # Metadata
    passage_title: str
    grade: str
    genre: str
    form_id: str
    passage_form_id: str
    created_at: str
    schema_version: str = "2026.1"


class SimplifiedRecallScoringGenerator:
    """
    Generates simplified recall scoring guides.
    
    Uses character + key detail approach for simple, reliable scoring.
    """
    
    def __init__(self, ai_client=None, template_loader=None):
        """
        Initialize the simplified recall scoring generator.
        
        Args:
            ai_client: AI client for generation (OpenAI, Anthropic, etc.)
            template_loader: Optional template loader for prompts
        """
        self.ai_client = ai_client
        self.template_loader = template_loader
        
    def generate(self, passage_result, max_retries: int = 3) -> SimplifiedRecallGuide:
        """
        Generate simplified recall scoring guide.
        
        Args:
            passage_result: Passage generation result with text and metadata
            max_retries: Maximum number of retry attempts for validation
            
        Returns:
            SimplifiedRecallGuide with character + detail scoring
            
        Raises:
            ValueError: If generation fails after all retries
        """
        # Split passage into sentences
        sentences = self._split_into_sentences(passage_result.passage_text)
        
        # Retry loop for reliability
        last_error = None
        for attempt in range(1, max_retries + 1):
            try:
                # Build prompt
                prompt = self._build_prompt(
                    passage_result=passage_result,
                    sentences=sentences,
                    last_error=last_error
                )
                
                # Get AI response
                response = self.ai_client.complete(prompt)
                
                # Parse response
                scoring_guide = self._parse_response(
                    response=response,
                    passage_result=passage_result,
                    sentences=sentences
                )
                
                # Validate
                self._validate_scoring_guide(scoring_guide, sentences)
                
                # Success!
                if attempt > 1:
                    print(f"✓ Recall scoring validation passed")
                    print(f"✓ Recall scoring generated successfully on attempt {attempt}")
                
                return scoring_guide
                
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                last_error = str(e)
                if attempt < max_retries:
                    print(f"⚠ Attempt {attempt} failed: {last_error}")
                    print(f"  Retrying... ({attempt + 1}/{max_retries})")
                else:
                    raise ValueError(
                        f"Failed to generate valid recall scoring after {max_retries} attempts. "
                        f"Last error: {last_error}"
                    )
    
    def _split_into_sentences(self, passage_text: str) -> List[str]:
        """
        Split passage into sentences.
        
        Args:
            passage_text: Full passage text
            
        Returns:
            List of sentence strings
        """
        # Simple sentence splitting on . ! ?
        # Handle common abbreviations
        text = passage_text.replace("Mr.", "Mr").replace("Mrs.", "Mrs").replace("Ms.", "Ms")
        text = text.replace("Dr.", "Dr").replace("St.", "St")
        
        # Split on sentence terminators
        sentences = re.split(r'[.!?]+', text)
        
        # Clean up
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return sentences
    
    def _build_prompt(self, passage_result, sentences: List[str], last_error: str = None) -> str:
        """
        Build prompt for AI to generate simplified recall scoring.
        
        Args:
            passage_result: Passage with metadata
            sentences: List of sentences from passage
            last_error: Previous error message if retrying
            
        Returns:
            Prompt string for AI
        """
        # Try template first
        if self.template_loader:
            try:
                template = self.template_loader.get_template('prompts/simplified_recall_scoring.j2')
                return template.render(
                    passage=passage_result,
                    sentences=sentences,
                    sentence_count=len(sentences),
                    last_error=last_error
                )
            except Exception:
                pass  # Fall back to inline prompt
        
        # Inline prompt
        prompt = f"""Generate a simplified recall scoring guide for this passage.

PASSAGE INFORMATION:
Title: {passage_result.passage_title}
Grade: {passage_result.grade}
Genre: {passage_result.genre}

PASSAGE TEXT:
{passage_result.passage_text}

SENTENCES TO SCORE ({len(sentences)} total):
"""
        
        for i, sentence in enumerate(sentences, 1):
            prompt += f"{i}. {sentence}\n"
        
        prompt += """

TASK: For each sentence, identify:
1. The CHARACTER NAME (who the sentence is about - name, pronoun, or "they/them" if multiple)
2. The KEY DETAIL (what happened, what's important, the main action or information)

SCORING RULE (same for every sentence):
- 2 points: Student recalls BOTH the character name AND the key detail
- 1 point: Student recalls EITHER the character name OR the key detail
- 0 points: Student recalls NEITHER

Return ONLY valid JSON in this exact format:
{
  "sentences": [
    {
      "sentence_number": 1,
      "sentence_text": "exact sentence text here",
      "character_name": "name or pronoun",
      "key_detail": "brief description of what's important",
      "scoring_note": "2 pts: [character] + [detail] | 1 pt: either | 0 pts: neither"
    }
  ],
  "general_instructions": "For each sentence, award 2 points if student recalls BOTH the character and key detail, 1 point for either one, 0 points for neither. Allow paraphrasing."
}

IMPORTANT:
- Return ONLY valid JSON, no markdown formatting
- Include ALL {len(sentences)} sentences
- Keep character names and details brief (3-8 words each)
- Use simple, clear language
- Ensure all quotes are properly escaped
"""

        if last_error:
            prompt += f"""

PREVIOUS ERROR: {last_error}
Please fix this error and ensure valid JSON format.
"""
        
        return prompt
    
    def _parse_response(self, response: str, passage_result, sentences: List[str]) -> SimplifiedRecallGuide:
        """
        Parse AI response into SimplifiedRecallGuide.
        
        Args:
            response: AI response string
            passage_result: Original passage result
            sentences: List of sentences
            
        Returns:
            SimplifiedRecallGuide object
            
        Raises:
            json.JSONDecodeError: If JSON is malformed
            KeyError: If required fields are missing
        """
        # Clean response
        json_str = response.strip()
        
        # Remove markdown code blocks if present
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0].strip()
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0].strip()
        
        # Parse JSON
        data = json.loads(json_str)
        
        # Build sentence scoring list
        sentence_scoring = []
        for s_data in data["sentences"]:
            sentence_scoring.append(
                SimplifiedSentenceScoring(
                    sentence_number=s_data["sentence_number"],
                    sentence_text=s_data["sentence_text"],
                    character_name=s_data["character_name"],
                    key_detail=s_data["key_detail"],
                    scoring_note=s_data.get("scoring_note", "2 pts: both | 1 pt: either | 0 pts: neither"),
                    max_points=2
                )
            )
        
        # Create scoring guide
        scoring_guide = SimplifiedRecallGuide(
            total_sentences=len(sentence_scoring),
            max_total_points=len(sentence_scoring) * 2,
            sentences=sentence_scoring,
            general_instructions=data.get(
                "general_instructions",
                "For each sentence, award 2 points if student recalls BOTH the character and key detail, "
                "1 point for either one, 0 points for neither. Allow paraphrasing."
            ),
            passage_title=passage_result.passage_title,
            grade=passage_result.grade,
            genre=passage_result.genre,
            form_id=f"RECALL-{passage_result.form_id}",
            passage_form_id=passage_result.form_id,
            created_at=datetime.now().isoformat(),
            schema_version="2026.1"
        )
        
        return scoring_guide
    
    def _validate_scoring_guide(self, scoring_guide: SimplifiedRecallGuide, sentences: List[str]):
        """
        Validate the scoring guide.
        
        Args:
            scoring_guide: Generated scoring guide
            sentences: Original sentences
            
        Raises:
            ValueError: If validation fails
        """
        # Check sentence count matches
        if scoring_guide.total_sentences != len(sentences):
            raise ValueError(
                f"Sentence count mismatch: got {scoring_guide.total_sentences}, expected {len(sentences)}"
            )
        
        # Check all sentences are present
        if len(scoring_guide.sentences) != len(sentences):
            raise ValueError(
                f"Sentence list length mismatch: got {len(scoring_guide.sentences)}, expected {len(sentences)}"
            )
        
        # Check max points calculation
        expected_max = len(sentences) * 2
        if scoring_guide.max_total_points != expected_max:
            raise ValueError(
                f"Max points mismatch: got {scoring_guide.max_total_points}, expected {expected_max}"
            )
        
        # Check each sentence has required fields
        for i, sent_scoring in enumerate(scoring_guide.sentences, 1):
            if not sent_scoring.character_name:
                raise ValueError(f"Sentence {i} missing character_name")
            if not sent_scoring.key_detail:
                raise ValueError(f"Sentence {i} missing key_detail")
            if sent_scoring.max_points != 2:
                raise ValueError(f"Sentence {i} has max_points={sent_scoring.max_points}, expected 2")


def create_simplified_recall_scoring_generator(ai_client, template_loader=None):
    """
    Factory function to create a simplified recall scoring generator.
    
    Args:
        ai_client: AI client for generation
        template_loader: Optional template loader
        
    Returns:
        SimplifiedRecallScoringGenerator instance
    """
    return SimplifiedRecallScoringGenerator(ai_client, template_loader)
