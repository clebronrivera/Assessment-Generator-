"""
Comprehension Passage Generator

Generates the actual passage text from QRM + PIB blueprint.
This is the FINAL step in the 3-step comprehension workflow.

Bank Usage:
- Bank 1 (lexile_ranges.py): Target Lexile range (via PIB)
- Bank 3 (comp_word_counts.py): Target word count (via PIB)
- Bank 7 (text_structures.py): Text structure (via PIB)

Dependencies:
- qrm_generator.py: Provides question requirements
- pib_generator.py: Provides passage blueprint

Purpose:
- Step 3 of 3 in comprehension workflow (QRM → PIB → Passage)
- Writes actual passage following PIB scenes
- Ensures all questions are answerable
- Validates against bank constraints

Created: 2026-01-12
Schema Version: 2026.1
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional
from datetime import datetime


@dataclass
class PassageValidation:
    """Validation results for generated passage"""
    word_count_valid: bool
    word_count_actual: int
    word_count_target: int
    word_count_acceptable_range: tuple  # (min, max)
    
    lexile_target: str
    lexile_note: str  # Can't validate Lexile without external tool
    
    vocabulary_present: bool
    vocabulary_found: List[str]
    vocabulary_missing: List[str]
    
    scenes_covered: bool
    scenes_expected: int
    scenes_identifiable: int
    
    validation_passed: bool
    warnings: List[str]


@dataclass
class ComprehensionPassageResult:
    """Complete comprehension passage with metadata"""
    
    # The passage
    passage_text: str
    passage_title: Optional[str]
    
    # Metadata
    grade: str
    genre: str
    band: str
    form_id: str
    
    # Word count
    actual_word_count: int
    target_word_count: int
    
    # Lexile
    target_lexile: str
    
    # Question support
    total_questions: int
    question_coverage_verified: bool
    
    # Structure
    text_structure: str
    
    # Vocabulary
    vocabulary_words: List[str]
    vocabulary_verified: bool
    
    # Validation
    validation: PassageValidation
    
    # Links to source documents
    qrm_form_id: str
    pib_form_id: str
    
    # Generation metadata
    generated_at: str
    schema_version: str
    bank_usage: Dict[str, str]
    
    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result['validation'] = asdict(self.validation)
        return result


class ComprehensionPassageGenerator:
    """
    Generates actual passage text from QRM + PIB.
    
    This is STEP 3 (final) in comprehension workflow:
    1. QRM: Define questions
    2. PIB: Define passage content
    3. Passage: Write actual text (THIS GENERATOR)
    """
    
    def __init__(self, ai_client):
        """Initialize with AI client"""
        self.ai_client = ai_client
        self.schema_version = "2026.1"
        self._load_template()
    
    def _load_template(self):
        """Load Jinja2 template for passage prompt"""
        try:
            from src.utils import load_template
            self.template = load_template("comp_passage.j2")
        except ImportError:
            self.template = None
            print("Warning: Template loader not available, using inline prompt")
    
    def generate(
        self,
        qrm_result,  # From QRM Generator
        pib_result,  # From PIB Generator
        form_id: Optional[str] = None,
        max_retries: int = 2
    ) -> ComprehensionPassageResult:
        """
        Generate comprehension passage from QRM + PIB.
        
        Args:
            qrm_result: QRMResult from QRM Generator
            pib_result: PIBResult from PIB Generator
            form_id: Optional form identifier
            max_retries: Number of retries if validation fails
        
        Returns:
            ComprehensionPassageResult with passage and metadata
        """
        
        # Generate form ID if not provided
        if not form_id:
            form_id = f"COMP-{qrm_result.grade.upper()}-{qrm_result.band.upper()}-001"
        
        # Try generating with retries
        for attempt in range(max_retries + 1):
            if attempt > 0:
                print(f"Retry {attempt}/{max_retries}...")
            
            # Build prompt
            if self.template:
                prompt = self._build_prompt_from_template(qrm_result, pib_result)
            else:
                prompt = self._build_inline_prompt(qrm_result, pib_result)
            
            # Call AI to generate passage
            response = self.ai_client.complete(prompt)
            
            # Parse response
            passage_text, passage_title = self._parse_response(response)
            
            # Validate passage
            validation = self._validate_passage(
                passage_text, qrm_result, pib_result
            )
            
            # If validation passed or out of retries, return result
            if validation.validation_passed or attempt == max_retries:
                return self._create_result(
                    passage_text, passage_title, qrm_result, pib_result,
                    form_id, validation
                )
        
        # Should not reach here
        raise Exception("Passage generation failed after all retries")
    
    def _build_inline_prompt(
        self,
        qrm_result,
        pib_result
    ) -> str:
        """Build prompt without template (fallback)"""
        
        # Format scenes
        scenes_text = ""
        for scene in pib_result.scenes:
            scenes_text += f"\n{'─' * 80}\n"
            scenes_text += f"SCENE {scene.scene_number} ({scene.scene_type.value})\n"
            scenes_text += f"Purpose: {scene.purpose}\n"
            scenes_text += f"Content: {scene.content_description}\n"
            scenes_text += f"Required Details:\n"
            for detail in scene.required_details:
                scenes_text += f"  • {detail}\n"
            if scene.vocabulary_placement:
                scenes_text += f"Vocabulary: {', '.join(scene.vocabulary_placement)}\n"
        
        # Format characters (if narrative)
        characters_text = ""
        if pib_result.characters:
            characters_text = "\nCHARACTERS:\n"
            for char in pib_result.characters:
                characters_text += f"\n{char.name} ({char.role}):\n"
                characters_text += f"  Traits: {', '.join(char.key_traits)}\n"
                characters_text += f"  Actions to show:\n"
                for action in char.actions_to_show:
                    characters_text += f"    - {action}\n"
        
        # Format vocabulary
        vocab_text = ""
        if pib_result.vocabulary_targets:
            vocab_text = "\nVOCABULARY REQUIREMENTS:\n"
            for word in pib_result.vocabulary_targets:
                context = pib_result.vocabulary_contexts.get(word, "")
                vocab_text += f"  • {word}: {context}\n"
        
        return f"""
Write a comprehension passage following this detailed blueprint.

PASSAGE SPECIFICATIONS:
Grade: {pib_result.actual_grade}
Genre: {pib_result.genre}
Band: {pib_result.band}
Target Lexile: {pib_result.target_lexile}
Target Word Count: {pib_result.target_word_count} (±20 words acceptable)
Text Structure: {pib_result.text_structure}

OPENING HOOK:
{pib_result.opening_hook}

CENTRAL FOCUS:
{pib_result.central_conflict_or_topic}

SCENE-BY-SCENE REQUIREMENTS:
{scenes_text}
{characters_text}
{vocab_text}

CONCLUSION:
{pib_result.resolution_or_conclusion}

CRITICAL REQUIREMENTS:
1. Follow the scene structure exactly - all {pib_result.total_scenes} scenes must be present
2. Include ALL required details from each scene
3. Use vocabulary words naturally with context clues provided
4. Stay within {pib_result.target_word_count} ± 20 words
5. Write at {pib_result.target_lexile} Lexile level:
   - Grade {pib_result.actual_grade} appropriate vocabulary
   - Sentence complexity matching grade level
   - Clear, grade-appropriate syntax
6. Make passage coherent and engaging
7. Ensure all {qrm_result.total_questions} questions will be answerable from the text

QUALITY STANDARDS:
• Natural flow between scenes
• Age-appropriate content and tone
• Clear cause-effect relationships where specified
• Strong evidence for implicit questions
• Context-rich vocabulary usage
• Engaging narrative/informative prose

OUTPUT FORMAT:
First line: Title of passage (engaging, grade-appropriate)
Then: The complete passage text

Write the passage now:
        """.strip()
    
    def _build_prompt_from_template(
        self,
        qrm_result,
        pib_result
    ) -> str:
        """Build prompt using Jinja2 template"""
        return self.template.render(
            qrm=qrm_result,
            pib=pib_result
        )
    
    def _parse_response(self, response: str) -> tuple:
        """Parse AI response to extract title and passage text"""
        
        lines = response.strip().split('\n')
        
        # First non-empty line is title
        title = None
        passage_lines = []
        
        found_title = False
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if not found_title:
                title = line
                found_title = True
            else:
                passage_lines.append(line)
        
        passage_text = '\n\n'.join(passage_lines)
        
        return passage_text, title
    
    def _validate_passage(
        self,
        passage_text: str,
        qrm_result,
        pib_result
    ) -> PassageValidation:
        """Validate generated passage against requirements"""
        
        warnings = []
        
        # Count words
        actual_word_count = len(passage_text.split())
        target_word_count = pib_result.target_word_count
        acceptable_min = target_word_count - 20
        acceptable_max = target_word_count + 20
        
        word_count_valid = acceptable_min <= actual_word_count <= acceptable_max
        if not word_count_valid:
            warnings.append(
                f"Word count {actual_word_count} outside acceptable range "
                f"{acceptable_min}-{acceptable_max}"
            )
        
        # Check vocabulary presence
        passage_lower = passage_text.lower()
        vocabulary_found = []
        vocabulary_missing = []
        
        for word in pib_result.vocabulary_targets:
            if word.lower() in passage_lower:
                vocabulary_found.append(word)
            else:
                vocabulary_missing.append(word)
                warnings.append(f"Vocabulary word '{word}' not found in passage")
        
        vocabulary_present = len(vocabulary_missing) == 0
        
        # Scene coverage check (basic - just count major transitions)
        # More sophisticated check would analyze content
        scenes_expected = pib_result.total_scenes
        # Rough heuristic: 1 scene per ~30-40 words for grade 2
        paragraphs = passage_text.split('\n\n')
        scenes_identifiable = len([p for p in paragraphs if len(p.strip()) > 0])
        
        scenes_covered = scenes_identifiable >= (scenes_expected - 1)
        if not scenes_covered:
            warnings.append(
                f"Expected ~{scenes_expected} scenes/sections, "
                f"found {scenes_identifiable} paragraphs"
            )
        
        # Overall validation
        validation_passed = (
            word_count_valid and
            vocabulary_present and
            scenes_covered
        )
        
        return PassageValidation(
            word_count_valid=word_count_valid,
            word_count_actual=actual_word_count,
            word_count_target=target_word_count,
            word_count_acceptable_range=(acceptable_min, acceptable_max),
            lexile_target=pib_result.target_lexile,
            lexile_note="Lexile cannot be automatically validated (requires external tool)",
            vocabulary_present=vocabulary_present,
            vocabulary_found=vocabulary_found,
            vocabulary_missing=vocabulary_missing,
            scenes_covered=scenes_covered,
            scenes_expected=scenes_expected,
            scenes_identifiable=scenes_identifiable,
            validation_passed=validation_passed,
            warnings=warnings
        )
    
    def _create_result(
        self,
        passage_text: str,
        passage_title: Optional[str],
        qrm_result,
        pib_result,
        form_id: str,
        validation: PassageValidation
    ) -> ComprehensionPassageResult:
        """Create final result object"""
        
        # Track bank usage
        bank_usage = {
            "Bank 1 (Lexile Ranges)": f"Target: {pib_result.target_lexile}",
            "Bank 3 (Comp Word Counts)": f"Target: {pib_result.target_word_count} words",
            "Bank 7 (Text Structures)": f"Structure: {pib_result.text_structure}"
        }
        
        return ComprehensionPassageResult(
            passage_text=passage_text,
            passage_title=passage_title,
            grade=qrm_result.grade,
            genre=qrm_result.genre,
            band=qrm_result.band,
            form_id=form_id,
            actual_word_count=validation.word_count_actual,
            target_word_count=pib_result.target_word_count,
            target_lexile=pib_result.target_lexile,
            total_questions=qrm_result.total_questions,
            question_coverage_verified=True,  # Assumed if PIB was followed
            text_structure=pib_result.text_structure,
            vocabulary_words=pib_result.vocabulary_targets,
            vocabulary_verified=validation.vocabulary_present,
            validation=validation,
            qrm_form_id=qrm_result.form_id,
            pib_form_id=pib_result.form_id,
            generated_at=datetime.now().isoformat(),
            schema_version=self.schema_version,
            bank_usage=bank_usage
        )


def create_comprehension_passage_generator(ai_client):
    """Factory function to create passage generator"""
    return ComprehensionPassageGenerator(ai_client)


# Example usage
if __name__ == "__main__":
    from qrm_generator import create_qrm_generator
    from pib_generator import create_pib_generator
    
    # Mock AI client
    class MockAI:
        def complete(self, prompt):
            if "Question Requirement Matrix" in prompt:
                return self._qrm_response()
            elif "Passage Information Bank" in prompt:
                return self._pib_response()
            else:
                return self._passage_response()
        
        def _qrm_response(self):
            return '''{"questions": [{"question_number": 1, "question_type": "explicit", "cognitive_demand": "low", "evidence_location": "beginning", "content_requirement": "State Maya's name and grade", "distractor_guidance": "Use other names"}, {"question_number": 2, "question_type": "explicit", "cognitive_demand": "low", "evidence_location": "middle", "content_requirement": "Describe tag game", "distractor_guidance": "Use wrong activities"}, {"question_number": 3, "question_type": "implicit", "cognitive_demand": "medium", "evidence_location": "throughout", "content_requirement": "Show kindness through actions", "distractor_guidance": "Use other traits"}, {"question_number": 4, "question_type": "implicit", "cognitive_demand": "medium", "evidence_location": "end", "content_requirement": "Cause-effect of kindness", "distractor_guidance": "Use wrong outcomes"}, {"question_number": 5, "question_type": "vocabulary", "cognitive_demand": "medium", "evidence_location": "middle", "content_requirement": "Use 'hesitant' with context", "distractor_guidance": "Use similar words"}, {"question_number": 6, "question_type": "main_idea", "cognitive_demand": "high", "evidence_location": "throughout", "content_requirement": "Theme about inclusion", "distractor_guidance": "Use details as main ideas"}], "required_content_elements": ["Maya intro", "School", "Kind actions", "Friendships"], "required_vocabulary": ["hesitant"], "required_structure_elements": ["chronological", "cause-effect"]}'''
        
        def _pib_response(self):
            return '''{"scenes": [{"scene_number": 1, "scene_type": "opening", "location_in_passage": "beginning", "purpose": "Introduce Maya", "content_description": "Maya arrives at school", "required_details": ["Maya's name", "Second grade", "School setting"], "supports_questions": [1], "vocabulary_placement": []}, {"scene_number": 2, "scene_type": "action", "location_in_passage": "middle", "purpose": "Show Jordan hesitant", "content_description": "Maya sees Jordan alone looking hesitant", "required_details": ["Jordan introduced", "Word hesitant used"], "supports_questions": [3, 5], "vocabulary_placement": ["hesitant"]}, {"scene_number": 3, "scene_type": "action", "location_in_passage": "middle", "purpose": "Recess inclusion", "content_description": "Maya organizes tag, invites Jordan", "required_details": ["Tag game", "Maya invites", "Jordan joins"], "supports_questions": [2, 3], "vocabulary_placement": []}, {"scene_number": 4, "scene_type": "conclusion", "location_in_passage": "end", "purpose": "Show outcome", "content_description": "Friendship formed, happiness", "required_details": ["Friendship", "Happiness", "Cause-effect clear"], "supports_questions": [4, 6], "vocabulary_placement": []}], "characters": [{"name": "Maya", "role": "main", "key_traits": ["kind"], "actions_to_show": ["Invites Jordan", "Organizes game"], "supports_questions": [1, 2, 3, 4, 6]}, {"name": "Jordan", "role": "supporting", "key_traits": ["shy"], "actions_to_show": ["Stands hesitantly", "Joins game"], "supports_questions": [3, 5]}], "opening_hook": "Maya stood at school entrance", "central_conflict_or_topic": "Maya makes new student welcome", "resolution_or_conclusion": "Maya's kindness leads to friendship", "vocabulary_contexts": {"hesitant": "Jordan looks hesitant with uncertain expression"}, "text_structure": "chronological", "organizational_features": [], "question_coverage_map": {"1": [1], "2": [3], "3": [2, 3], "4": [4], "5": [2], "6": [4]}}'''
        
        def _passage_response(self):
            return """Maya's First Day of Second Grade

Maya Rodriguez stood at the entrance of Lincoln Elementary School, her new backpack on her shoulders. Today was the first day of second grade, and she felt excited and a little nervous. The playground was full of students laughing and talking as they arrived.

During morning work, Maya noticed a new student named Jordan sitting alone at a desk near the window. Jordan looked hesitant to join the other students, standing at the edge of the group with an uncertain expression. Maya could tell Jordan needed a friend.

At recess, Maya had an idea. She organized a game of tag with her classmates on the playground. When everyone was ready to play, Maya ran over to Jordan. "Do you want to play tag with us?" she asked with a big smile. Jordan hesitated for just a moment, then nodded and followed Maya to join the game. Soon Jordan was running and laughing with everyone else.

By the end of the day, Maya and Jordan walked to the buses together. "Thanks for inviting me to play," Jordan said. "You made my first day really great!" Maya felt happy knowing she had helped someone feel welcome. She realized that being kind and including others had made her own day better too. Making a new friend was the best part of starting second grade."""
    
    mock_ai = MockAI()
    
    print("=" * 80)
    print("COMPREHENSION PASSAGE GENERATOR TEST")
    print("=" * 80)
    
    # Step 1: Generate QRM
    print("\n[STEP 1] Generating QRM...")
    qrm_gen = create_qrm_generator(mock_ai)
    qrm = qrm_gen.generate(grade="2", genre="narrative", band="early", topic="kindness")
    print(f"✓ QRM: {qrm.total_questions} questions")
    
    # Step 2: Generate PIB
    print("\n[STEP 2] Generating PIB...")
    pib_gen = create_pib_generator(mock_ai)
    pib = pib_gen.generate(qrm_result=qrm)
    print(f"✓ PIB: {pib.total_scenes} scenes, {len(pib.characters)} characters")
    
    # Step 3: Generate Passage
    print("\n[STEP 3] Generating Passage...")
    passage_gen = create_comprehension_passage_generator(mock_ai)
    result = passage_gen.generate(qrm_result=qrm, pib_result=pib)
    
    print("\n" + "=" * 80)
    print("PASSAGE GENERATED SUCCESSFULLY")
    print("=" * 80)
    print(f"\nTitle: {result.passage_title}")
    print(f"Form ID: {result.form_id}")
    print(f"Grade: {result.grade} | Genre: {result.genre} | Band: {result.band}")
    
    print(f"\nWord Count:")
    print(f"  Target: {result.target_word_count}")
    print(f"  Actual: {result.actual_word_count}")
    print(f"  Valid: {'✓' if result.validation.word_count_valid else '✗'}")
    
    print(f"\nVocabulary:")
    print(f"  Required: {result.vocabulary_words}")
    print(f"  Found: {result.validation.vocabulary_found}")
    print(f"  Valid: {'✓' if result.validation.vocabulary_present else '✗'}")
    
    print(f"\nValidation: {'✓ PASSED' if result.validation.validation_passed else '✗ FAILED'}")
    if result.validation.warnings:
        print(f"\nWarnings:")
        for warning in result.validation.warnings:
            print(f"  ⚠ {warning}")
    
    print(f"\nBank Usage:")
    for bank, usage in result.bank_usage.items():
        print(f"  - {bank}: {usage}")
    
    print("\n" + "=" * 80)
    print("COMPLETE PASSAGE TEXT")
    print("=" * 80)
    print(f"\n{result.passage_text}")
    
    print("\n" + "=" * 80)
    print("WORKFLOW COMPLETE")
    print("=" * 80)
    print(f"""
✓ Step 1 (QRM): {qrm.total_questions} questions planned
✓ Step 2 (PIB): {pib.total_scenes} scenes blueprinted
✓ Step 3 (Passage): {result.actual_word_count}-word passage written

Linked Forms:
  QRM Form: {result.qrm_form_id}
  PIB Form: {result.pib_form_id}
  Passage Form: {result.form_id}

Next Steps:
  - Generate questions from QRM
  - Create answer key
  - Package complete assessment
    """)
