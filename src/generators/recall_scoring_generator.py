"""
Recall Scoring Generator

Generates recall assessment scoring templates from comprehension passages.
Creates sentence-by-sentence scoring guides with key ideas and partial credit keywords.

Bank Usage:
- Bank 4 (Comprehension Blueprint): Via passage metadata for grade-appropriate expectations

Dependencies:
- comprehension_passage_generator.py: Provides passage text to analyze

Purpose:
- Generate recall scoring templates
- Break passage into scorable sentences
- Identify key ideas per sentence
- Define partial credit keywords
- Create 0-1-2 point rubric per sentence

Created: 2026-01-12
Schema Version: 2026.1
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional
from datetime import datetime


@dataclass
class KeyIdea:
    """A key idea within a sentence that should be recalled"""
    idea_text: str
    importance: str  # essential, important, supporting
    points_if_recalled: float  # Contribution to sentence score


@dataclass
class SentenceScoring:
    """Scoring guide for a single sentence"""
    sentence_number: int
    sentence_text: str
    max_points: int  # Typically 2
    
    # Key ideas student should recall
    key_ideas: List[KeyIdea]
    
    # Partial credit keywords (4-8 per sentence)
    partial_keywords: List[str]
    
    # Scoring rubric for this sentence
    score_0_criteria: str  # No recall or incorrect
    score_1_criteria: str  # Partial recall (keywords or one key idea)
    score_2_criteria: str  # Complete recall (all key ideas)
    
    # Example student responses
    example_score_0: str
    example_score_1: str
    example_score_2: str


@dataclass
class RecallScoringGuide:
    """Complete recall scoring template"""
    
    # Passage information
    passage_text: str
    passage_title: Optional[str]
    total_sentences: int
    
    # Sentence-by-sentence scoring
    sentence_scoring: List[SentenceScoring]
    
    # Overall scoring
    max_total_points: int
    
    # Scoring guidelines
    general_instructions: str
    scoring_notes: List[str]
    
    # Metadata
    grade: str
    genre: str
    band: str
    form_id: str
    
    # Links
    passage_form_id: str
    
    # Generation metadata
    generated_at: str
    schema_version: str
    bank_usage: Dict[str, str]
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class RecallScoringGenerator:
    """
    Generates recall scoring templates from passages.
    
    Analyzes passage sentence-by-sentence and creates detailed
    scoring guides with key ideas, partial keywords, and rubrics.
    """
    
    def __init__(self, ai_client):
        """Initialize with AI client"""
        self.ai_client = ai_client
        self.schema_version = "2026.1"
        self._load_template()
    
    def _load_template(self):
        """Load Jinja2 template for recall scoring prompt"""
        try:
            from src.utils import load_template
            self.template = load_template("recall_scoring.j2")
        except ImportError:
            self.template = None
            print("Warning: Template loader not available, using inline prompt")
    
    def generate(
        self,
        passage_result,  # From Comprehension Passage Generator
        form_id: Optional[str] = None
    ) -> RecallScoringGuide:
        """
        Generate recall scoring template from passage.
        
        Args:
            passage_result: ComprehensionPassageResult from Passage Generator
            form_id: Optional form identifier
        
        Returns:
            RecallScoringGuide with complete scoring template
        """
        
        # Generate form ID if not provided
        if not form_id:
            form_id = f"COMP-{passage_result.grade.upper()}-{passage_result.band.upper()}-RECALL-001"
        
        # Split passage into sentences
        sentences = self._split_into_sentences(passage_result.passage_text)
        
        # Build prompt
        if self.template:
            prompt = self._build_prompt_from_template(
                passage_result, sentences
            )
        else:
            prompt = self._build_inline_prompt(
                passage_result, sentences
            )
        
        # Call AI to generate scoring guide
        response = self.ai_client.complete(prompt)
        
        # Parse response into structured scoring guide
        scoring_guide = self._parse_response(
            response, passage_result, sentences, form_id
        )
        
        return scoring_guide
    
    def _split_into_sentences(self, passage_text: str) -> List[str]:
        """Split passage into individual sentences"""
        import re
        
        # Simple sentence splitting (period, exclamation, question mark)
        # Preserve the original text exactly
        sentences = re.split(r'(?<=[.!?])\s+', passage_text.strip())
        
        # Filter out empty strings
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return sentences
    
    def _build_inline_prompt(
        self,
        passage_result,
        sentences: List[str]
    ) -> str:
        """Build prompt without template (fallback)"""
        
        # Format sentences with numbers
        sentences_text = ""
        for i, sent in enumerate(sentences, 1):
            sentences_text += f"\nSentence {i}: {sent}\n"
        
        return f"""
Generate a recall scoring template for this comprehension passage.

PASSAGE TITLE: {passage_result.passage_title or "Untitled"}

PASSAGE TEXT:
{passage_result.passage_text}

SENTENCES TO SCORE ({len(sentences)} total):
{sentences_text}

TASK:
Create a detailed scoring guide for each sentence. For EACH sentence, identify:

1. **Key Ideas (2-4 per sentence)**
   - Main concepts student should recall
   - Mark as: essential, important, or supporting
   - Assign point contribution (e.g., 0.5, 1.0)

2. **Partial Credit Keywords (4-8 per sentence)**
   - Specific words that indicate partial understanding
   - Include proper nouns, key verbs, important adjectives
   - These help score partial recall (1 point)

3. **Scoring Rubric (0-1-2 points)**
   - **0 points:** No recall or completely incorrect
   - **1 point:** Partial recall (uses some keywords OR recalls one key idea)
   - **2 points:** Complete recall (recalls all essential key ideas)

4. **Example Student Responses**
   - Example 0-point response
   - Example 1-point response  
   - Example 2-point response

OUTPUT FORMAT (JSON):
{{
  "sentence_scoring": [
    {{
      "sentence_number": 1,
      "sentence_text": "Maya was excited for second grade.",
      "max_points": 2,
      "key_ideas": [
        {{
          "idea_text": "Maya is the main character",
          "importance": "essential",
          "points_if_recalled": 1.0
        }},
        {{
          "idea_text": "She is starting second grade",
          "importance": "essential",
          "points_if_recalled": 1.0
        }},
        {{
          "idea_text": "She feels excited",
          "importance": "important",
          "points_if_recalled": 0.5
        }}
      ],
      "partial_keywords": ["Maya", "second grade", "excited", "school"],
      "score_0_criteria": "No mention of Maya, second grade, or school",
      "score_1_criteria": "Mentions Maya OR second grade, but not both key ideas",
      "score_2_criteria": "States Maya is starting second grade (both key ideas present)",
      "example_score_0": "A girl went somewhere.",
      "example_score_1": "Maya was happy.",
      "example_score_2": "Maya was excited to start second grade."
    }},
    // ... more sentences
  ],
  "general_instructions": "Read student's oral recall. Score each sentence 0-2 points based on key ideas recalled. Award partial credit for keywords even if not exact wording.",
  "scoring_notes": [
    "Accept paraphrasing if key ideas are present",
    "Award 1 point if student uses 2+ keywords but misses key ideas",
    "Award 2 points if all essential key ideas are present",
    "Do not penalize for extra details or slightly incorrect sequence"
  ]
}}

CRITICAL REQUIREMENTS:
- Create scoring for ALL {len(sentences)} sentences
- Identify 2-4 key ideas per sentence
- Provide 4-8 partial keywords per sentence
- Make 0/1/2 criteria clear and objective
- Provide realistic example responses
- Focus on meaning, not exact wording

Generate the recall scoring guide now:
        """.strip()
    
    def _build_prompt_from_template(
        self,
        passage_result,
        sentences: List[str]
    ) -> str:
        """Build prompt using Jinja2 template"""
        return self.template.render(
            passage=passage_result,
            sentences=sentences
        )
    
    def _parse_response(
        self,
        response: str,
        passage_result,
        sentences: List[str],
        form_id: str
    ) -> RecallScoringGuide:
        """Parse AI response into RecallScoringGuide structure"""
        
        import json
        
        # Extract JSON from response
        json_str = response.strip()
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0].strip()
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0].strip()
        
        data = json.loads(json_str)
        
        # Parse sentence scoring
        sentence_scoring = []
        for s_data in data["sentence_scoring"]:
            # Parse key ideas
            key_ideas = []
            for k_data in s_data["key_ideas"]:
                key_ideas.append(KeyIdea(
                    idea_text=k_data["idea_text"],
                    importance=k_data["importance"],
                    points_if_recalled=k_data["points_if_recalled"]
                ))
            
            # Create sentence scoring
            sentence_scoring.append(SentenceScoring(
                sentence_number=s_data["sentence_number"],
                sentence_text=s_data["sentence_text"],
                max_points=s_data.get("max_points", 2),
                key_ideas=key_ideas,
                partial_keywords=s_data["partial_keywords"],
                score_0_criteria=s_data["score_0_criteria"],
                score_1_criteria=s_data["score_1_criteria"],
                score_2_criteria=s_data["score_2_criteria"],
                example_score_0=s_data["example_score_0"],
                example_score_1=s_data["example_score_1"],
                example_score_2=s_data["example_score_2"]
            ))
        
        # Calculate total points
        max_total_points = sum(s.max_points for s in sentence_scoring)
        
        # Track bank usage
        bank_usage = {
            "Bank 4 (Comprehension Blueprint)": "Via passage metadata for grade expectations"
        }
        
        return RecallScoringGuide(
            passage_text=passage_result.passage_text,
            passage_title=passage_result.passage_title,
            total_sentences=len(sentences),
            sentence_scoring=sentence_scoring,
            max_total_points=max_total_points,
            general_instructions=data.get("general_instructions", ""),
            scoring_notes=data.get("scoring_notes", []),
            grade=passage_result.grade,
            genre=passage_result.genre,
            band=passage_result.band,
            form_id=form_id,
            passage_form_id=passage_result.form_id,
            generated_at=datetime.now().isoformat(),
            schema_version=self.schema_version,
            bank_usage=bank_usage
        )


def create_recall_scoring_generator(ai_client):
    """Factory function to create recall scoring generator"""
    return RecallScoringGenerator(ai_client)


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
            elif "recall scoring" in prompt.lower():
                return self._recall_response()
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
                    {"scene_number": 2, "scene_type": "action", "location_in_passage": "middle", "purpose": "Tag game", "content_description": "Maya invites Jordan to tag", "required_details": ["tag game", "hesitant"], "supports_questions": [2, 3, 4, 5, 6], "vocabulary_placement": ["hesitant"]}
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
                "question_coverage_map": {"1": [1], "2": [2], "3": [2], "4": [2], "5": [2], "6": [2]}
            })
        
        def _passage_response(self):
            return """Making New Friends

Maya was excited for second grade. She stood at the school entrance with her red backpack.

At recess, Maya saw a new boy named Jordan. He looked hesitant to join the other kids playing tag. Maya ran over. "Do you want to play?" she asked with a smile.

Jordan nodded and joined the game. By the end of recess, they were both laughing and running together. Maya felt happy she had invited him to play."""
        
        def _recall_response(self):
            import json
            return json.dumps({
                "sentence_scoring": [
                    {
                        "sentence_number": 1,
                        "sentence_text": "Maya was excited for second grade.",
                        "max_points": 2,
                        "key_ideas": [
                            {"idea_text": "Maya is the main character", "importance": "essential", "points_if_recalled": 1.0},
                            {"idea_text": "She is starting second grade", "importance": "essential", "points_if_recalled": 1.0}
                        ],
                        "partial_keywords": ["Maya", "second grade", "excited", "school"],
                        "score_0_criteria": "No mention of Maya or second grade",
                        "score_1_criteria": "Mentions Maya OR second grade, but not both",
                        "score_2_criteria": "States Maya is starting second grade",
                        "example_score_0": "A girl went to school.",
                        "example_score_1": "Maya was happy.",
                        "example_score_2": "Maya was excited to start second grade."
                    },
                    {
                        "sentence_number": 2,
                        "sentence_text": "She stood at the school entrance with her red backpack.",
                        "max_points": 2,
                        "key_ideas": [
                            {"idea_text": "She was at school entrance", "importance": "important", "points_if_recalled": 1.0},
                            {"idea_text": "She had a red backpack", "importance": "supporting", "points_if_recalled": 1.0}
                        ],
                        "partial_keywords": ["entrance", "school", "backpack", "red"],
                        "score_0_criteria": "No mention of location or backpack",
                        "score_1_criteria": "Mentions school entrance OR backpack",
                        "score_2_criteria": "Mentions both school entrance and red backpack",
                        "example_score_0": "She was there.",
                        "example_score_1": "She had a backpack.",
                        "example_score_2": "She stood at the school entrance with her red backpack."
                    },
                    {
                        "sentence_number": 3,
                        "sentence_text": "At recess, Maya saw a new boy named Jordan.",
                        "max_points": 2,
                        "key_ideas": [
                            {"idea_text": "At recess time", "importance": "important", "points_if_recalled": 0.5},
                            {"idea_text": "Maya saw a new boy", "importance": "essential", "points_if_recalled": 1.0},
                            {"idea_text": "His name is Jordan", "importance": "essential", "points_if_recalled": 0.5}
                        ],
                        "partial_keywords": ["recess", "Maya", "new", "boy", "Jordan"],
                        "score_0_criteria": "No mention of seeing someone or Jordan",
                        "score_1_criteria": "Mentions seeing a new student but not name OR mentions Jordan without context",
                        "score_2_criteria": "States Maya saw new boy named Jordan at recess",
                        "example_score_0": "Maya played.",
                        "example_score_1": "Maya saw a new student.",
                        "example_score_2": "At recess, Maya saw a new boy named Jordan."
                    },
                    {
                        "sentence_number": 4,
                        "sentence_text": "He looked hesitant to join the other kids playing tag.",
                        "max_points": 2,
                        "key_ideas": [
                            {"idea_text": "Jordan appeared hesitant/unsure", "importance": "essential", "points_if_recalled": 1.0},
                            {"idea_text": "Other kids were playing tag", "importance": "essential", "points_if_recalled": 1.0}
                        ],
                        "partial_keywords": ["hesitant", "unsure", "join", "kids", "tag", "playing"],
                        "score_0_criteria": "No mention of Jordan's feelings or the game",
                        "score_1_criteria": "Mentions tag game OR Jordan's hesitation, not both",
                        "score_2_criteria": "States Jordan was hesitant about joining tag game",
                        "example_score_0": "He stood there.",
                        "example_score_1": "Kids were playing tag.",
                        "example_score_2": "He looked unsure about joining the tag game."
                    }
                ],
                "general_instructions": "Read student's oral recall. Score each sentence 0-2 points based on key ideas recalled. Award partial credit for keywords even if not exact wording.",
                "scoring_notes": [
                    "Accept paraphrasing if key ideas are present",
                    "Award 1 point if student uses 2+ keywords but misses key ideas",
                    "Award 2 points if all essential key ideas are present",
                    "Do not penalize for extra details or slightly different sequence"
                ]
            })
    
    mock_ai = MockAI()
    
    print("=" * 80)
    print("RECALL SCORING GENERATOR TEST")
    print("=" * 80)
    
    # Step 1-3: Generate passage (same as before)
    print("\n[STEP 1-3] Generating passage...")
    qrm_gen = create_qrm_generator(mock_ai)
    qrm = qrm_gen.generate(grade="2", genre="narrative", band="early")
    
    pib_gen = create_pib_generator(mock_ai)
    pib = pib_gen.generate(qrm_result=qrm)
    
    passage_gen = create_comprehension_passage_generator(mock_ai)
    passage = passage_gen.generate(qrm_result=qrm, pib_result=pib)
    print(f"✓ Passage: {passage.actual_word_count} words, {passage.passage_title}")
    
    # Step 4: Generate Recall Scoring
    print("\n[STEP 4] Generating Recall Scoring Guide...")
    recall_gen = create_recall_scoring_generator(mock_ai)
    scoring_guide = recall_gen.generate(passage_result=passage)
    
    print("\n" + "=" * 80)
    print("RECALL SCORING GUIDE GENERATED")
    print("=" * 80)
    print(f"\nForm ID: {scoring_guide.form_id}")
    print(f"Passage: {scoring_guide.passage_title}")
    print(f"Total Sentences: {scoring_guide.total_sentences}")
    print(f"Max Total Points: {scoring_guide.max_total_points} ({scoring_guide.total_sentences} sentences × 2 points)")
    
    print(f"\nGeneral Instructions:")
    print(f"  {scoring_guide.general_instructions}")
    
    print(f"\nScoring Notes:")
    for note in scoring_guide.scoring_notes:
        print(f"  • {note}")
    
    print("\n" + "=" * 80)
    print("SAMPLE SENTENCE SCORING")
    print("=" * 80)
    
    # Show first 2 sentences
    for sent in scoring_guide.sentence_scoring[:2]:
        print(f"\n{'─' * 80}")
        print(f"SENTENCE {sent.sentence_number} (Max {sent.max_points} points)")
        print(f"{'─' * 80}")
        print(f"\"{sent.sentence_text}\"")
        
        print(f"\nKey Ideas ({len(sent.key_ideas)}):")
        for idea in sent.key_ideas:
            print(f"  • {idea.idea_text} ({idea.importance}, {idea.points_if_recalled} pts)")
        
        print(f"\nPartial Keywords ({len(sent.partial_keywords)}):")
        print(f"  {', '.join(sent.partial_keywords)}")
        
        print(f"\nScoring Rubric:")
        print(f"  0 pts: {sent.score_0_criteria}")
        print(f"  1 pt:  {sent.score_1_criteria}")
        print(f"  2 pts: {sent.score_2_criteria}")
        
        print(f"\nExample Responses:")
        print(f"  [0] \"{sent.example_score_0}\"")
        print(f"  [1] \"{sent.example_score_1}\"")
        print(f"  [2] \"{sent.example_score_2}\"")
    
    print("\n" + "=" * 80)
    print("COMPLETE COMPREHENSION ASSESSMENT")
    print("=" * 80)
    print(f"""
✓ QRM: Question planning (6 questions)
✓ PIB: Content blueprinting ({pib.total_scenes} scenes)
✓ Passage: Text generation ({passage.actual_word_count} words)
✓ Questions: Multiple choice (available separately)
✓ Recall Scoring: Complete template ({scoring_guide.total_sentences} sentences, {scoring_guide.max_total_points} points)

PHASE 2C: COMPLETE! 🎉

All comprehension assessment components ready:
  - Passages with question support
  - Multiple choice questions with answer keys
  - Recall scoring templates with detailed rubrics
    """)
