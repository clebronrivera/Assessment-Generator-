#!/usr/bin/env python3
"""
Enhance all generated assessments with detailed administration information:
- Assessment Details
- Presentation Mode
- Timing
- Enhanced Assessor Script
- Student Action
- What Assessor is Grading/Marking
- Additional Considerations (blank field)
"""

import json
import os
from pathlib import Path
from typing import Dict, Any

SAMPLES_DIR = Path(__file__).parent / "samples"


# Detailed administration information for each assessment type
ADMINISTRATION_SPECS = {
    "LR-ALPH": {
        "student_action": "Student sees one letter at a time on screen and orally names the letter (e.g., says 'B' or 'bee' for uppercase B, 'b' or 'buh' for lowercase b). Student can self-correct before moving to next letter.",
        "assessor_grading": "Assessor marks each item as: CORRECT (letter named correctly), INCORRECT (wrong letter name, letter sound instead of name, or confused case), SELF-CORRECT (student initially incorrect but self-corrected within reasonable time), or OMISSION (no response or skipped). Timer tracks total completion time. Final score is total correct out of 52 (all uppercase and lowercase letters).",
        "assessor_script_enhanced": [
            "SETUP: Prepare assessment materials. Ensure student is comfortable and ready.",
            "SAY TO STUDENT: 'I'm going to show you some letters. Tell me the name of each letter.'",
            "Demonstrate with one example if needed: 'This is the letter B. Can you tell me its name?'",
            "SAY: 'When you're ready, I'll start showing you letters one at a time. Say the name of each letter you see.'",
            "ADMINISTRATION:",
            "  • Start the timer when you show the first letter",
            "  • Present letters one at a time using the manual next button",
            "  • Wait for student response before advancing",
            "  • Click/tap the item to cycle through marking states:",
            "    - First click: Mark as INCORRECT (if wrong)",
            "    - Second click: Mark as SELF-CORRECT (if student self-corrected)",
            "    - Third click: Mark as OMISSION (if skipped/no response)",
            "    - Additional clicks cycle back through states",
            "  • If student is correct, leave unmarked (default is correct)",
            "  • Continue through all 52 letters",
            "  • Stop timer when assessment is complete",
            "IMPORTANT: Accept letter names (e.g., 'bee', 'ay', 'see'), not sounds. For lowercase letters, accept either case name or the letter name."
        ]
    },
    
    "FL-WRF": {
        "student_action": "Student sees one word at a time on screen and reads the word aloud. Student reads words sequentially, as quickly and accurately as possible within the 60-second time limit. Student can attempt to decode unfamiliar words or skip if needed.",
        "assessor_grading": "Assessor marks each word read during the 60-second period as: CORRECT (word read accurately), INCORRECT (word misread, substituted, or pronounced incorrectly), SELF-CORRECT (student initially incorrect but self-corrected), or OMISSION (word skipped or not attempted). Timer counts down from 60 seconds. Primary score is Words Correct Per Minute (WCPM) calculated as: (Total words attempted - errors) × (60 / time taken). Secondary metrics include total correct, accuracy percentage, and error pattern analysis.",
        "assessor_script_enhanced": [
            "SETUP: Prepare word list, timer, and scoring sheet. Ensure quiet environment.",
            "SAY TO STUDENT: 'I'm going to show you some words. Read each word as quickly and carefully as you can.'",
            "SAY: 'When I say 'start,' begin reading the words. Try to read as many words as you can in 60 seconds.'",
            "Demonstrate with one example if needed.",
            "ADMINISTRATION:",
            "  • Start the 60-second countdown timer when you say 'start'",
            "  • Present words one at a time",
            "  • Click/tap each word to mark errors as student reads:",
            "    - First click: Mark as INCORRECT",
            "    - Second click: Mark as SELF-CORRECT",
            "    - Third click: Mark as OMISSION",
            "    - Additional clicks cycle through states",
            "  • If word is read correctly, leave unmarked",
            "  • Continue presenting words until 60 seconds expire or student completes list",
            "  • At 60 seconds, say 'stop' and mark the last word attempted",
            "SCORING: Calculate WCPM = (words read correctly) × (60 / seconds elapsed). Count only words read correctly within the time limit."
        ]
    },
    
    "FL-PSF": {
        "student_action": "Student hears a word spoken by the assessor and must orally segment the word into all its individual phonemes (sounds). For example, for 'cat', student says '/k/ /a/ /t/'. Student produces sounds one at a time in sequence within the 60-second time limit.",
        "assessor_grading": "Assessor counts the number of correct phonemes the student produces for each word within the time limit. Each word receives credit for correct phonemes only if all phonemes are produced in correct sequence. Mark as: CORRECT PHONEMES COUNT (e.g., 3/3 for 'cat' = /k/ /a/ /t/), PARTIAL (e.g., 2/3 if student misses a phoneme), or NO RESPONSE (if student doesn't respond within 3 seconds or produces no phonemes). Primary score is Phonemes Correct Per Minute (PCPM) = total correct phonemes × (60 / time taken). Also track words with all phonemes correct vs. partial.",
        "assessor_script_enhanced": [
            "SETUP: Prepare word list and timer. Ensure student understands task.",
            "SAY TO STUDENT: 'I will say a word. You say all the sounds in the word.'",
            "Give example: 'If I say 'sat,' you would say /s/ /a/ /t/.' Demonstrate with one practice item if needed.",
            "SAY: 'Let's start. I'll say each word, and you tell me all the sounds.'",
            "ADMINISTRATION:",
            "  • Start the 60-second countdown timer",
            "  • Say each word clearly and distinctly (one word per item)",
            "  • Student responds by producing individual phonemes",
            "  • Count correct phonemes produced for each word",
            "  • Enter the number of correct phonemes (e.g., 3 for 'cat', 4 for 'frog')",
            "  • If student says the whole word instead, prompt once: 'Tell me the sounds, not the word'",
            "  • If no response after 3 seconds, mark as no response and move to next word",
            "  • Continue until 60 seconds expire or all words complete",
            "SCORING: Count total phonemes correct. Calculate PCPM = (total phonemes correct) × (60 / time taken)."
        ]
    },
    
    "PA-RHYM": {
        "student_action": "Student hears two words spoken by the assessor and must determine if the words rhyme. Student responds orally with 'yes' if they rhyme or 'no' if they don't rhyme. Student listens to both words before responding.",
        "assessor_grading": "Assessor marks each pair as: CORRECT (student correctly identifies rhyming or non-rhyming pairs), INCORRECT - FALSE POSITIVE (student says 'yes' for non-rhyming pair), INCORRECT - FALSE NEGATIVE (student says 'no' for rhyming pair), or NO RESPONSE (student doesn't respond). Primary score is total correct out of 20. Secondary analysis includes false positive rate (saying 'yes' too often) and false negative rate (saying 'no' too often), which indicate different aspects of phonological awareness.",
        "assessor_script_enhanced": [
            "SETUP: Prepare word pairs list. Ensure student understands concept of rhyming.",
            "SAY TO STUDENT: 'I will say two words. Tell me if they rhyme.'",
            "Give examples: 'Cat and hat - do they rhyme? Yes! Sun and cup - do they rhyme? No.'",
            "Practice with 1-2 examples if needed to ensure understanding.",
            "SAY: 'Now I'll say pairs of words. After I say both words, tell me 'yes' if they rhyme or 'no' if they don't.'",
            "ADMINISTRATION:",
            "  • Say the first word clearly, pause briefly (300-800ms), then say the second word",
            "  • Wait for student's yes/no response",
            "  • Mark response using yes/no buttons:",
            "    - Click 'Yes' if student correctly identifies rhyming pair",
            "    - Click 'No' if student correctly identifies non-rhyming pair",
            "    - System marks as incorrect if response doesn't match correct answer",
            "  • Advance to next pair after marking",
            "  • If student doesn't respond, wait 3-5 seconds, then mark as no response",
            "SCORING: Total correct out of 20. Note patterns: students who say 'yes' too often may not understand rhyme concept, while those who say 'no' too often may be overly cautious."
        ]
    },
    
    "PA-OONS": {
        "student_action": "Student hears an onset (beginning sound, e.g., /b/) and a rime (ending pattern, e.g., /at/) spoken separately by the assessor, and must blend them together to produce the complete word (e.g., 'bat'). Student responds orally with the blended word.",
        "assessor_grading": "Assessor marks each item as: CORRECT (student successfully blends onset and rime to produce correct word), INCORRECT BLEND (student produces wrong word or blends incorrectly), PARTIAL BLEND (student produces parts but not complete word), or NO RESPONSE (student doesn't respond within reasonable time). Primary score is total correct out of 20. Note error patterns: students who struggle with onset-rime blending may need additional phonemic awareness support.",
        "assessor_script_enhanced": [
            "SETUP: Prepare onset-rime pairs list. Ensure student can hear and process both parts.",
            "SAY TO STUDENT: 'I will say two parts of a word. Put them together to make a whole word.'",
            "Give example: 'If I say 'b... at,' what word do you hear? Bat!'",
            "Demonstrate with one practice item if needed.",
            "SAY: 'Now I'll say the beginning sound, pause, then the ending. Put them together and tell me the word.'",
            "ADMINISTRATION:",
            "  • Say the onset (beginning sound) clearly, pause 300-800ms, then say the rime (ending pattern)",
            "  • Student responds with the blended word",
            "  • Mark using correct/incorrect buttons:",
            "    - Click 'Correct' if student produces correct word",
            "    - Click 'Incorrect' if student produces wrong word, partial blend, or no response",
            "  • Advance to next item after marking",
            "  • If student doesn't respond after 3-5 seconds, mark as no response",
            "SCORING: Total correct out of 20. Monitor for patterns: students who consistently miss may need more practice with sound blending."
        ]
    },
    
    "PA-PHON": {
        "student_action": "Student hears a word spoken by the assessor and must orally segment the word into all its individual phonemes (sounds) in sequence. For example, for 'sun', student says '/s/ /u/ /n/'. This is untimed, allowing student to think and produce all sounds carefully.",
        "assessor_grading": "Assessor marks each item as: CORRECT (all phonemes produced correctly in sequence), INCORRECT - PHONEME OMISSION (student misses one or more phonemes), INCORRECT - PHONEME ADDITION (student adds extra sounds), INCORRECT - SEQUENCE ERROR (phonemes out of order), or NO RESPONSE (doesn't respond within 3 seconds or produces no phonemes). Primary score is total correct out of 20. Note which phonemes students typically omit or struggle with for instructional planning.",
        "assessor_script_enhanced": [
            "SETUP: Prepare word list. Ensure student understands task is different from saying whole word.",
            "SAY TO STUDENT: 'I will say a word. Tell me all the sounds in the word.'",
            "Give example: 'If I say 'sun,' you would say /s/ /u/ /n/. Do not say the whole word, just the sounds.'",
            "Practice with 1-2 examples if needed to ensure student understands.",
            "SAY: 'Now I'll say each word. After each word, tell me all the sounds you hear.'",
            "ADMINISTRATION:",
            "  • Say each word clearly and distinctly",
            "  • Wait for student to produce individual phonemes",
            "  • If student says whole word, prompt once: 'Tell me the sounds, not the word'",
            "  • Mark using correct/incorrect buttons:",
            "    - Click 'Correct' only if ALL phonemes are produced correctly in sequence",
            "    - Click 'Incorrect' if any phoneme is omitted, added, or out of sequence",
            "  • Advance to next word after marking or 3 seconds of no response",
            "SCORING: Total correct out of 20. Track error patterns: which phonemes are commonly omitted, which words are challenging."
        ]
    },
    
    "PA-SYLS": {
        "student_action": "Student hears a word spoken by the assessor and must clap or tap the number of syllables in the word. For example, for 'butter', student claps twice (but-ter). Student may also verbally count or segment syllables orally. This is untimed, allowing careful analysis.",
        "assessor_grading": "Assessor counts the number of correct syllable segments the student produces for each word. Mark as: CORRECT (correct number of syllables identified, e.g., 2 claps for 'butter'), INCORRECT COUNT (wrong number, e.g., 1 or 3 claps for 'butter'), PARTIAL SEGMENTATION (student partially segments but not complete), or NO RESPONSE (doesn't respond). Primary score is total correct out of 20. Also track total syllables correctly identified across all words for partial credit analysis.",
        "assessor_script_enhanced": [
            "SETUP: Prepare word list. Have student demonstrate understanding of syllable concept if needed.",
            "SAY TO STUDENT: 'I will say a word. Clap the syllables, or tell me how many parts the word has.'",
            "Give example: 'If I say 'butter,' you clap twice: but-ter. If I say 'cat,' you clap once.'",
            "Practice with 1-2 examples if needed.",
            "SAY: 'Now I'll say each word. Clap how many syllables you hear in each word.'",
            "ADMINISTRATION:",
            "  • Say each word clearly and distinctly",
            "  • Student claps, taps, or verbally counts syllables",
            "  • Count the number of segments/claps student produces",
            "  • Enter the number of correct syllables in the count input field",
            "  • Mark as correct if number matches expected syllable count",
            "  • Mark as incorrect if number is wrong",
            "  • If student doesn't respond, wait 3-5 seconds, then mark as no response",
            "  • Advance to next word after marking",
            "SCORING: Total correct out of 20. Note which word lengths (1, 2, or 3 syllables) are challenging."
        ]
    },
    
    "PH-CSA": {
        "student_action": "Student sees one letter or digraph displayed on screen and must orally produce the sound(s) that letter or letter combination represents. For example, for 'c', student says '/k/' or '/s/'. For 'th', student says '/θ/' or '/ð/'. Student responds with the sound, not the letter name.",
        "assessor_grading": "Assessor marks each item as: CORRECT (accurate sound production for the letter/digraph), INCORRECT SOUND (student produces wrong sound, letter name instead of sound, or confused sound), ARTICULATION VARIANT (acceptable regional pronunciation variant), or NO RESPONSE (doesn't respond within reasonable time). Primary score is total correct out of 24. Note which letters or digraphs are challenging for targeted instruction.",
        "assessor_script_enhanced": [
            "SETUP: Prepare letter/digraph list. Ensure student understands task is sounds, not names.",
            "SAY TO STUDENT: 'I will show you some letters. Tell me the sound each letter makes.'",
            "Give example: 'This letter is C. What sound does it make? /k/ or /s/.' Clarify that you want the SOUND, not the name.",
            "Practice with 1-2 examples if needed.",
            "SAY: 'Now I'll show you each letter one at a time. Tell me the sound each letter makes.'",
            "ADMINISTRATION:",
            "  • Display each letter or digraph one at a time on screen",
            "  • Student responds orally with the sound(s)",
            "  • Mark using correct/incorrect buttons:",
            "    - Click 'Correct' if sound is accurate",
            "    - Click 'Incorrect' if sound is wrong, letter name given instead, or no response",
            "    - Accept acceptable regional variants (e.g., /r/ variations)",
            "  • Advance to next letter after marking",
            "  • If student says letter name, gently redirect: 'What SOUND does it make?'",
            "SCORING: Total correct out of 24. Track which letter-sound correspondences need reteaching."
        ]
    },
    
    "PH-CVC": {
        "student_action": "Student sees one CVC (consonant-vowel-consonant) word displayed on screen and reads the word aloud. Words include both real words (e.g., 'cat', 'bed') and nonsense words (e.g., 'ced', 'vur'). Student attempts to decode each word using phonics knowledge.",
        "assessor_grading": "Assessor marks each item as: CORRECT (word read accurately with correct decoding), INCORRECT (word misread, substituted, or decoded incorrectly), SELF-CORRECT (student initially incorrect but self-corrected), or OMISSION (word skipped or not attempted). Primary score is total correct out of 25. Secondary metrics include accuracy percentage and vowel accuracy (tracking which vowels are challenging). Note performance on real words vs. nonsense words to assess pure decoding skills.",
        "assessor_script_enhanced": [
            "SETUP: Prepare CVC word list. Ensure student understands some words may be made-up.",
            "SAY TO STUDENT: 'I will show you some words. Some are real words, and some are made-up words. Read each word the best you can.'",
            "Give example: 'This word is 'cat' - a real word. This word is 'ced' - a made-up word. Try to sound it out.'",
            "SAY: 'Now I'll show you each word one at a time. Read each word aloud.'",
            "ADMINISTRATION:",
            "  • Display each word one at a time on screen",
            "  • Student reads word aloud (or attempts to decode)",
            "  • Click/tap the word to mark responses:",
            "    - First click: Mark as INCORRECT (if wrong)",
            "    - Second click: Mark as SELF-CORRECT (if self-corrected)",
            "    - Third click: Mark as OMISSION (if skipped)",
            "    - Additional clicks cycle through states",
            "  • If word is read correctly, leave unmarked (default correct)",
            "  • Advance to next word after response",
            "  • Allow reasonable time for decoding attempts",
            "SCORING: Total correct out of 25. Analyze patterns: vowel accuracy, real vs. nonsense word performance."
        ]
    },
    
    "PH-LWID": {
        "student_action": "Student sees one item at a time on screen - either a single letter or a word. For letters, student names the letter (e.g., says 'B' or 'bee'). For words, student reads the word aloud. Items are mixed together in the list. Student responds orally to each item.",
        "assessor_grading": "Assessor marks each item as: CORRECT (letter named correctly or word read accurately), INCORRECT - MISIDENTIFICATION (wrong letter name or word misread), SUBSTITUTION (student says different word/letter), OMISSION (skipped item), or NO RESPONSE (doesn't respond). Primary score is total correct out of 40. Secondary metrics include letter accuracy (out of letter items) and word accuracy (out of word items) separately, which helps identify if student struggles with letter recognition vs. word reading.",
        "assessor_script_enhanced": [
            "SETUP: Prepare mixed letter-word list. Ensure student understands items may be letters or words.",
            "SAY TO STUDENT: 'I will show you some letters and words mixed together. If you see a letter, tell me its name. If you see a word, read the word.'",
            "Give examples: 'This is the letter B - say 'B.' This is the word 'cat' - read it.'",
            "SAY: 'Now I'll show you each item one at a time. Tell me the letter name or read the word.'",
            "ADMINISTRATION:",
            "  • Display each item one at a time on screen",
            "  • For letters: Student names the letter",
            "  • For words: Student reads the word",
            "  • Mark using correct/incorrect buttons:",
            "    - Click 'Correct' if letter named correctly or word read accurately",
            "    - Click 'Incorrect' if wrong name, misread word, skipped, or no response",
            "  • Advance to next item after marking",
            "  • Note item type (letter vs. word) for analysis",
            "SCORING: Total correct out of 40. Calculate separate scores for letters and words to identify specific needs."
        ]
    }
}


def enhance_simple_assessment(assessment_data: Dict[str, Any], assessment_id: str) -> Dict[str, Any]:
    """Enhance a simple assessment with administration details"""
    if assessment_id not in ADMINISTRATION_SPECS:
        return assessment_data
    
    spec = ADMINISTRATION_SPECS[assessment_id]
    
    # Enhance interface_spec
    if "interface_spec" not in assessment_data:
        assessment_data["interface_spec"] = {}
    
    # Update assessor script with enhanced version
    assessment_data["interface_spec"]["assessor_script"] = spec["assessor_script_enhanced"]
    
    # Add student action
    assessment_data["interface_spec"]["student_action"] = spec["student_action"]
    
    # Add assessor grading information
    assessment_data["interface_spec"]["assessor_grading"] = spec["assessor_grading"]
    
    # Add additional considerations (blank for now)
    assessment_data["interface_spec"]["additional_considerations"] = ""
    
    return assessment_data


def enhance_orf_assessment(assessment_data: Dict[str, Any]) -> Dict[str, Any]:
    """Enhance ORF assessment with additional administration details"""
    
    # ORF assessments already have comprehensive assessor_materials
    # We'll add student_action and assessor_grading to the assessor_materials section
    
    if "assessor_materials" not in assessment_data:
        return assessment_data
    
    assessor_materials = assessment_data["assessor_materials"]
    
    # Add student action
    assessor_materials["student_action"] = (
        "Student reads the passage aloud from a clean copy placed in front of them. "
        "Student attempts to read as accurately and smoothly as possible within the 60-second time limit. "
        "If student encounters an unknown word and hesitates for 3 seconds, assessor supplies the word. "
        "Student may self-correct errors during reading. Student reads continuously until time expires or passage is complete."
    )
    
    # Add assessor grading information
    assessor_materials["assessor_grading"] = (
        "Assessor marks errors in real-time on a separate assessor copy of the passage as student reads. "
        "Error types include: SUBSTITUTION (wrong word said - mark by drawing line through word, write what student said above), "
        "OMISSION (word skipped - circle the omitted word), INSERTION (word added - use caret ^ where inserted, write word above), "
        "HESITATION (3+ second pause, word supplied - mark with 'H' above word), SELF-CORRECTION (student fixes own error quickly - mark 'SC', DO NOT count as error), "
        "REPETITION (repeats word/phrase - underline, DO NOT count as error). "
        "At 60 seconds, mark last word read with bracket ]. "
        "Calculate WCPM = (Words Read - Errors) and Accuracy = (Words Read - Errors) / Words Read × 100. "
        "Also score prosody using 1-4 scale based on phrasing, expression, smoothness, and pace."
    )
    
    # Add additional considerations (blank for now)
    assessor_materials["additional_considerations"] = ""
    
    return assessment_data


def enhance_comprehension_assessment(assessment_data: Dict[str, Any]) -> Dict[str, Any]:
    """Enhance comprehension assessment with administration details"""
    
    # Comprehension assessments have multiple components
    # We'll add administration details at the top level
    
    # Add student action
    assessment_data["student_action"] = (
        "Phase 1 - Reading: Student reads the passage silently or aloud (as appropriate) from beginning to end. "
        "Student may take as much time as needed to read and understand the passage. "
        "Phase 2 - Recall: After reading, passage is removed/covered. Student orally recalls everything they remember from the passage. "
        "Student may include characters, events, details, and main ideas. Assessor records recalled sentences. "
        "Phase 3 - Questions: Passage is made visible again. Student answers multiple-choice comprehension questions (typically 5-6 questions). "
        "Student may refer back to the passage while answering questions. Student selects answer choice (A, B, or C)."
    )
    
    # Add assessor grading
    assessment_data["assessor_grading"] = (
        "Assessor scores in three phases: "
        "Phase 1 - Reading: Observe and note reading behaviors, fluency, and any difficulties (not formally scored but noted). "
        "Phase 2 - Recall: For each sentence in the passage, assessor marks if student recalled: "
        "(1) the character/subject mentioned in sentence, (2) the key detail/action in sentence. "
        "Each sentence receives 2 points (both recalled), 1 point (one recalled), or 0 points (neither recalled). "
        "Total recall score = sum of sentence scores. Recall accuracy ratio = total points / max possible points. "
        "Phase 3 - Questions: Assessor marks each multiple-choice question as CORRECT (correct answer selected) or INCORRECT (wrong answer, multiple selections, or no response). "
        "Question score = total correct out of total questions. "
        "Overall comprehension performance combines both recall accuracy and question accuracy."
    )
    
    # Add additional considerations (blank for now)
    assessment_data["additional_considerations"] = ""
    
    return assessment_data


def process_assessment_file(file_path: Path) -> bool:
    """Process a single assessment file and enhance it"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Determine assessment type
        assessment_id = data.get("assessment_id")
        assessment_type = data.get("assessment_type") or data.get("package_type")
        
        # Enhance based on type
        if assessment_id and assessment_id in ADMINISTRATION_SPECS:
            # Simple assessment
            data = enhance_simple_assessment(data, assessment_id)
        elif assessment_type == "orf":
            # ORF assessment
            data = enhance_orf_assessment(data)
        elif assessment_type == "comprehension":
            # Comprehension assessment
            data = enhance_comprehension_assessment(data)
        else:
            # Unknown type, skip
            print(f"  Skipping {file_path.name} - unknown assessment type")
            return False
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
    
    except Exception as e:
        print(f"  Error processing {file_path.name}: {e}")
        return False


def main():
    """Main function to enhance all assessments"""
    print("Enhancing assessments with administration details...")
    print(f"Scanning directory: {SAMPLES_DIR}")
    
    # Get all JSON files (excluding manifest files)
    assessment_files = [
        f for f in SAMPLES_DIR.glob("*.json")
        if not f.name.endswith("_manifest.json")
    ]
    
    print(f"Found {len(assessment_files)} assessment files to process\n")
    
    processed = 0
    skipped = 0
    errors = 0
    
    for file_path in sorted(assessment_files):
        print(f"Processing: {file_path.name}...")
        success = process_assessment_file(file_path)
        
        if success:
            processed += 1
            print(f"  ✓ Enhanced successfully\n")
        else:
            skipped += 1
            print(f"  ⚠ Skipped\n")
    
    print("=" * 60)
    print(f"Enhancement complete!")
    print(f"  Processed: {processed}")
    print(f"  Skipped: {skipped}")
    print(f"  Errors: {errors}")
    print("=" * 60)


if __name__ == "__main__":
    main()
