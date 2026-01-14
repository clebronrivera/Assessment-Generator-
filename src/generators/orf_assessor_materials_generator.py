"""
ORF Assessor Materials Generator

Generates complete assessor materials package for Oral Reading Fluency assessments.
Produces administration script, scoring sheets, and error marking grids.

Bank Usage:
- Bank 2 (orf_word_counts.py): WCPM benchmarks for scoring guidance

Dependencies:
- orf_generator.py: Generates the passage that these materials support
- base_generator.py: Base generator functionality
- template_loader.py: Loads Jinja2 templates

Created: 2026-01-12
Schema Version: 2026.1
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path for imports (adjust as needed)
sys.path.insert(0, str(Path(__file__).parent.parent))


@dataclass
class ORFAssessorMaterials:
    """Complete ORF assessor materials package"""
    
    # Administration
    timing_script: str
    word_supply_rules: str
    general_instructions: str
    
    # Scoring
    score_sheet: str
    wcpm_benchmark: Dict[str, int]  # fall/winter/spring targets
    accuracy_calculation: str
    prosody_rubric: str
    
    # Error Marking
    error_marking_grid: str
    error_types: Dict[str, str]  # error type -> description
    
    # Metadata
    grade: str
    passage_word_count: int
    form_id: str
    generated_at: str
    schema_version: str
    bank_usage: Dict[str, str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)


class ORFAssessorMaterialsGenerator:
    """
    Generates complete assessor materials for ORF assessments.
    
    Does NOT use AI - generates from templates and bank data.
    All content is deterministic and bank-driven.
    """
    
    def __init__(self):
        """Initialize generator with bank access"""
        self.schema_version = "2026.1"
        self._load_banks()
    
    def _load_banks(self):
        """Load required banks"""
        try:
            # Assuming banks are importable from src.banks
            from src.banks import get_orf_target
            self.get_orf_target = get_orf_target
        except ImportError:
            # Fallback for testing - mock bank data
            print("Warning: Could not import banks, using mock data")
            self.get_orf_target = self._mock_get_orf_target
    
    def _mock_get_orf_target(self, grade: str) -> Dict[str, Any]:
        """Mock bank data for testing without imports"""
        mock_data = {
            "1": {"spring_wcpm_50th": 60, "spring_wcpm_75th": 91, "target_words": 110},
            "2": {"spring_wcpm_50th": 100, "spring_wcpm_75th": 124, "target_words": 140},
            "3": {"spring_wcpm_50th": 112, "spring_wcpm_75th": 139, "target_words": 150},
        }
        return mock_data.get(grade, {"spring_wcpm_50th": 112, "spring_wcpm_75th": 139, "target_words": 150})
    
    def generate(
        self,
        grade: str,
        passage_text: str,
        passage_word_count: int,
        form_id: str,
        passage_metadata: Optional[Dict[str, Any]] = None
    ) -> ORFAssessorMaterials:
        """
        Generate complete assessor materials package.
        
        Args:
            grade: Grade level (1-8)
            passage_text: The ORF passage text
            passage_word_count: Exact word count of passage
            form_id: Form identifier (e.g., "ORF-2-EARLY-001")
            passage_metadata: Optional metadata from passage generation
        
        Returns:
            ORFAssessorMaterials object with all components
        """
        
        # Get WCPM benchmarks from Bank 2
        orf_spec = self.get_orf_target(grade)
        
        # Generate each component
        timing_script = self._generate_timing_script()
        word_supply_rules = self._generate_word_supply_rules()
        general_instructions = self._generate_general_instructions(grade)
        score_sheet = self._generate_score_sheet(
            grade, passage_word_count, orf_spec, form_id
        )
        wcpm_benchmark = {
            "50th_percentile": getattr(orf_spec, 'spring_wcpm_50th', None) or orf_spec.get("spring_wcpm_50th") if isinstance(orf_spec, dict) else orf_spec.spring_wcpm_50th,
            "75th_percentile": getattr(orf_spec, 'spring_wcpm_75th', None) or orf_spec.get("spring_wcpm_75th") if isinstance(orf_spec, dict) else orf_spec.spring_wcpm_75th
        }
        accuracy_calculation = self._generate_accuracy_calculation(passage_word_count)
        prosody_rubric = self._generate_prosody_rubric()
        error_marking_grid = self._generate_error_marking_grid(passage_text)
        error_types = self._generate_error_types()
        
        # Track bank usage
        bank_usage = {
            "Bank 2 (ORF Word Counts)": f"Grade {grade} WCPM benchmarks",
        }
        
        return ORFAssessorMaterials(
            timing_script=timing_script,
            word_supply_rules=word_supply_rules,
            general_instructions=general_instructions,
            score_sheet=score_sheet,
            wcpm_benchmark=wcpm_benchmark,
            accuracy_calculation=accuracy_calculation,
            prosody_rubric=prosody_rubric,
            error_marking_grid=error_marking_grid,
            error_types=error_types,
            grade=grade,
            passage_word_count=passage_word_count,
            form_id=form_id,
            generated_at=datetime.now().isoformat(),
            schema_version=self.schema_version,
            bank_usage=bank_usage
        )
    
    def _generate_timing_script(self) -> str:
        """Generate 60-second timing administration script"""
        return """
ORF TIMING PROTOCOL (60 seconds)

SETUP:
• Have stopwatch/timer ready
• Have scoring sheet prepared
• Ensure quiet environment
• Student has clean copy of passage

SAY TO STUDENT:
"I'm going to ask you to read this passage aloud. Read it as accurately and 
smoothly as you can. If you come to a word you don't know, I'll tell it to you. 
Do you have any questions?"

[Answer questions, then continue]

"Begin reading when I say 'start.' Ready? Start."

DURING READING:
• Start timer immediately
• Mark errors on scoring sheet as they occur
• Supply words after 3-second hesitation (see Word Supply Rules)
• Do not provide feedback or encouragement during reading
• Maintain neutral, supportive demeanor

AT 60 SECONDS:
• Say "Stop" clearly but calmly
• Mark the last word read with a bracket: ]
• Student may finish the word they're on, but mark where they were at 60 sec

AFTER READING:
• Thank the student
• Calculate scores (do not share with student during assessment)
• Proceed to comprehension questions if applicable
        """.strip()
    
    def _generate_word_supply_rules(self) -> str:
        """Generate 3-second word-supply rule"""
        return """
3-SECOND WORD SUPPLY RULE

WHEN TO SUPPLY A WORD:
If student hesitates for 3 full seconds on a word:
1. Supply the word clearly
2. Mark as an error on scoring sheet
3. Student continues reading

HOW TO COUNT 3 SECONDS:
• Use "one-thousand-one, one-thousand-two, one-thousand-three" method
• OR count silently while maintaining visual engagement with student
• Be consistent across all assessments

IMPORTANT:
• DO supply after 3 seconds - prevents frustration and keeps assessment moving
• DO NOT supply before 3 seconds - allow time for decoding attempts
• DO mark supplied words as errors - they count toward accuracy calculation
• DO remain neutral - no verbal encouragement or discouragement

STUDENT SELF-CORRECTIONS:
• If student self-corrects within 3 seconds: NOT an error
• If student self-corrects after moving to next word: IS an error
• Mark original error, note self-correction in margin
        """.strip()
    
    def _generate_general_instructions(self, grade: str) -> str:
        """Generate grade-appropriate general administration instructions"""
        return f"""
GENERAL ADMINISTRATION INSTRUCTIONS - GRADE {grade}

BEFORE ASSESSMENT:
□ Prepare materials: student passage, assessor copy, score sheet, timer
□ Ensure student is comfortable and ready
□ Briefly explain the task (see Timing Script)
□ Answer questions about the process, not about the passage

DURING ASSESSMENT:
□ Follow Timing Protocol exactly (60 seconds)
□ Apply 3-Second Word Supply Rule consistently
□ Mark all errors as they occur
□ Maintain neutral demeanor - no facial reactions to errors
□ Do not interrupt reading except to supply words after 3 seconds

AFTER ASSESSMENT:
□ Calculate Words Correct Per Minute (WCPM)
□ Calculate Accuracy Percentage
□ Score Prosody using rubric
□ Record all scores on score sheet
□ Do not discuss scores with student during assessment session

ENVIRONMENTAL CONSIDERATIONS:
• Quiet space with minimal distractions
• Good lighting for reading
• Comfortable seating
• Private (1-on-1) administration preferred

ASSESSMENT VALIDITY:
• If interrupted, restart with new passage
• If student is ill/distracted, reschedule
• If significant emotional distress occurs, stop assessment
        """.strip()
    
    def _generate_score_sheet(
        self,
        grade: str,
        passage_word_count: int,
        orf_spec: Dict[str, Any],
        form_id: str
    ) -> str:
        """Generate complete scoring sheet with calculations"""
        
        wcpm_50th = getattr(orf_spec, 'spring_wcpm_50th', None) or orf_spec.get("spring_wcpm_50th") if isinstance(orf_spec, dict) else orf_spec.spring_wcpm_50th
        wcpm_75th = getattr(orf_spec, 'spring_wcpm_75th', None) or orf_spec.get("spring_wcpm_75th") if isinstance(orf_spec, dict) else orf_spec.spring_wcpm_75th
        
        return f"""
═══════════════════════════════════════════════════════════════
        ORAL READING FLUENCY SCORE SHEET
═══════════════════════════════════════════════════════════════

FORM: {form_id}
GRADE: {grade}
PASSAGE WORD COUNT: {passage_word_count}

STUDENT INFORMATION:
Student Name: _______________________________________
Date: _______________  Assessor: ___________________
School: _____________________  Class: ______________

═══════════════════════════════════════════════════════════════
SCORING
═══════════════════════════════════════════════════════════════

STEP 1: WORDS READ IN 60 SECONDS
Last word read (marked with ]): Word # ________

STEP 2: COUNT ERRORS
Total errors made: ________ errors

Error Types Marked:
  Omissions: ______
  Substitutions: ______
  Insertions: ______
  Hesitations (3+ sec): ______

STEP 3: CALCULATE WCPM (Words Correct Per Minute)
Formula: Words Read - Errors = WCPM

  ________ (words read) - ________ (errors) = ________ WCPM

STEP 4: CALCULATE ACCURACY
Formula: (Words Read - Errors) / Words Read × 100

  (________ - ________) / ________ × 100 = ________%

═══════════════════════════════════════════════════════════════
BENCHMARK COMPARISON (Grade {grade})
═══════════════════════════════════════════════════════════════

Fall Target:    {wcpm_50th} WCPM (50th percentile)    Student: ________ WCPM
Winter Target:  {wcpm_75th} WCPM (75th percentile)    Student: ________ WCPM  
Spring Target:  {wcpm_75th} WCPM (75th percentile)    Student: ________ WCPM

Performance Level (check one):
□ Above Benchmark (exceeds target by 10+ WCPM)
□ At Benchmark (within ±10 WCPM of target)
□ Below Benchmark (below target by 10+ WCPM)
□ Significantly Below (below target by 30+ WCPM)

═══════════════════════════════════════════════════════════════
PROSODY RATING (See Prosody Rubric)
═══════════════════════════════════════════════════════════════

Score (1-4): ________

□ 1 - Primarily word-by-word, choppy
□ 2 - Mostly two-word phrases, limited expression
□ 3 - Mixture of three+ word phrases, appropriate phrasing
□ 4 - Consistent meaningful phrases, good expression

═══════════════════════════════════════════════════════════════
NOTES & OBSERVATIONS
═══════════════════════════════════════════════════════════════

Patterns noticed:
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________

Recommendations:
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________

═══════════════════════════════════════════════════════════════
        """.strip()
    
    def _generate_accuracy_calculation(self, passage_word_count: int) -> str:
        """Generate accuracy calculation guide with examples"""
        return f"""
ACCURACY CALCULATION GUIDE

Formula: (Words Read - Errors) / Words Read × 100 = Accuracy %

EXAMPLE with {passage_word_count}-word passage:

Scenario 1: Strong Reader
  Words read in 60 sec: 120 words
  Errors made: 2 errors
  Calculation: (120 - 2) / 120 × 100 = 98.3% accuracy
  
Scenario 2: Developing Reader
  Words read in 60 sec: 85 words
  Errors made: 8 errors
  Calculation: (85 - 8) / 85 × 100 = 90.6% accuracy

Scenario 3: Struggling Reader
  Words read in 60 sec: 45 words
  Errors made: 12 errors
  Calculation: (45 - 12) / 45 × 100 = 73.3% accuracy

ACCURACY GUIDELINES:
• 97-100%: Excellent accuracy, independent level
• 90-96%: Good accuracy, instructional level
• Below 90%: Frustration level, text may be too difficult

NOTE: Accuracy matters as much as speed. A fast reader with many 
errors needs different support than a slow but accurate reader.
        """.strip()
    
    def _generate_prosody_rubric(self) -> str:
        """Generate NAEP-aligned prosody rubric"""
        return """
MULTIDIMENSIONAL FLUENCY SCALE (Prosody)
Adapted from NAEP Oral Reading Fluency Scale

Score each dimension, then determine overall level (1-4):

PHRASING & EXPRESSION:
Level 4 - Reads with good phrasing; adheres to author's syntax; uses 
         expression to convey meaning; attention to punctuation.

Level 3 - Reads with a mixture of run-ons, mid-sentence pauses for breath,
         and some choppiness; reasonable syntax; expressive interpretation.

Level 2 - Reads with a mixture of two-word phrases and occasional 
         three-to-four-word phrases; limited expression; monotone.

Level 1 - Reads primarily word-by-word with occasional two-word phrases;
         lacks expression; ignores most punctuation.

SMOOTHNESS:
• Smooth, automatic reading with few hesitations
• Some hesitations and pauses, but generally flows
• Frequent hesitations, pauses, false starts, repetitions
• Very choppy, labored reading throughout

PACE:
• Conversational pace throughout
• Uneven pace, sometimes too fast or slow
• Consistently too slow or too fast
• Very slow, laborious pace

OVERALL PROSODY SCORE: _________ (1-4)

NOTES ON PROSODY:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
        """.strip()
    
    def _generate_error_marking_grid(self, passage_text: str) -> str:
        """Generate error marking guide with passage-specific examples"""
        
        # Get first few words of passage for examples
        words = passage_text.split()[:20] if passage_text else []
        example_segment = " ".join(words) if words else "[passage text]"
        
        return f"""
ERROR MARKING SYSTEM

Mark errors directly on the assessor copy of the passage as they occur.

═══════════════════════════════════════════════════════════════
ERROR TYPES & MARKING CONVENTIONS
═══════════════════════════════════════════════════════════════

1. SUBSTITUTION (wrong word said)
   Mark: Draw line through word, write what student said above
   Example: "The cat ran" → student says "The cat run"
            The cat ran
                    run

2. OMISSION (word skipped)
   Mark: Circle the omitted word
   Example: "jumped over the" → student says "jumped the"
            jumped (over) the

3. INSERTION (word added that isn't in text)
   Mark: Use caret (^) where word inserted, write word above
   Example: "the big dog" → student says "the really big dog"
                    really
            the ^ big dog

4. HESITATION (3+ second pause, word supplied by assessor)
   Mark: Put "H" above word
   Example: "difficult" → student pauses 3+ seconds, you supply word
                H
            difficult

5. SELF-CORRECTION (student fixes own error quickly)
   Mark: Write "SC" above; DO NOT count as error
   Example: "ran... race" → student says "ran" then self-corrects to "race"
                SC
            race

6. REPETITION (repeats word or phrase)
   Mark: Underline repeated portion; DO NOT count as error
   Example: "the dog ran" → student says "the dog... the dog ran"
            the dog ran

7. LAST WORD READ AT 60 SECONDS
   Mark: Place bracket ] after last word completed
   Example: ... the dog ran fast] across the yard

═══════════════════════════════════════════════════════════════
EXAMPLE MARKED PASSAGE SEGMENT:
═══════════════════════════════════════════════════════════════

{example_segment}...

[Mark errors as shown above directly on your copy]

═══════════════════════════════════════════════════════════════
MARKING TIPS:
═══════════════════════════════════════════════════════════════

• Mark in real-time as student reads
• Use consistent symbols across all assessments
• If unsure, mark it and review after completion
• Keep tally of each error type for analysis
• Note patterns (e.g., struggles with multi-syllable words)
        """.strip()
    
    def _generate_error_types(self) -> Dict[str, str]:
        """Generate error type definitions for reference"""
        return {
            "substitution": "Student says a different word than what is printed",
            "omission": "Student skips a word entirely",
            "insertion": "Student adds a word that is not in the text",
            "hesitation": "Student pauses 3+ seconds, assessor supplies word",
            "self_correction": "Student corrects own error immediately (not counted)",
            "repetition": "Student repeats word or phrase (not counted as error)"
        }


def create_orf_assessor_materials_generator() -> ORFAssessorMaterialsGenerator:
    """Factory function to create generator instance"""
    return ORFAssessorMaterialsGenerator()


# Example usage
if __name__ == "__main__":
    # Create generator
    generator = create_orf_assessor_materials_generator()
    
    # Generate materials for a Grade 2 passage
    materials = generator.generate(
        grade="2",
        passage_text="Sample passage text here...",
        passage_word_count=150,
        form_id="ORF-2-EARLY-001"
    )
    
    print("=" * 70)
    print("ORF ASSESSOR MATERIALS GENERATED")
    print("=" * 70)
    print(f"\nGrade: {materials.grade}")
    print(f"Form ID: {materials.form_id}")
    print(f"Passage Word Count: {materials.passage_word_count}")
    print(f"\nWCPM Benchmarks:")
    print(f"  Fall: {materials.wcpm_benchmark['fall']}")
    print(f"  Winter: {materials.wcpm_benchmark['winter']}")
    print(f"  Spring: {materials.wcpm_benchmark['spring']}")
    print(f"\nSchema Version: {materials.schema_version}")
    print(f"Generated: {materials.generated_at}")
    print(f"\nBank Usage: {materials.bank_usage}")
    print("\n" + "=" * 70)
    print("TIMING SCRIPT")
    print("=" * 70)
    print(materials.timing_script)
    print("\n" + "=" * 70)
    print("SCORE SHEET")
    print("=" * 70)
    print(materials.score_sheet)
