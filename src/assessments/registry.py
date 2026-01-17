"""
Complete Assessment Registry
All assessments with full specifications for Mission Control interface
"""

from typing import Dict, Optional
from .interfaces import (
    PresentationMode,
    AssessorInteraction,
    TimingMode,
    ClickCyclePattern,
    AssessmentInterface
)
# NEW v2026.2: Import new enums
from .enums import (
    AssessorInteractionEnum,
    TimingModeEnum,
    ResponseCaptureModeEnum,
    ResponseStateEnum,
    MetricEnum,
    ErrorCodeEnum
)


# === COMPLETE ASSESSMENT REGISTRY ===

ASSESSMENTS: Dict[str, Dict] = {
    
    # 1. LETTER RECOGNITION - CUSTOM SPEC
    "LR-ALPH": {
        "id": "LR-ALPH",
        "name": "Letter Recognition",
        "category": "Phonics",
        "domain": "Alphabetic Principle",
        "grade_range": "PreK-K",
        "description": "Uppercase and lowercase letter recognition",
        
        "content": {
            "item_type": "single_letter",
            "total_items": 52,  # 26 upper + 26 lower
            "item_order": "scrambled_fixed",
            "forms": 1
        },
        
        "interface": AssessmentInterface(
            # Student View
            student_presentation=PresentationMode.ONE_AT_A_TIME,
            student_sees_text=True,
            items_advance_mode="manual_next_button",
            
            # Assessor View
            assessor_interaction=AssessorInteraction.CLICK_CYCLE,
            click_cycle=ClickCyclePattern([
                "correct",      # 0 clicks (default)
                "incorrect",    # 1 click
                "self_correct", # 2 clicks
                "omission",     # 3 clicks
                "omission",     # 4 clicks (same as 3)
                "reset"         # 5 clicks (back to correct)
            ]),
            
            # Timing
            timing_mode=TimingMode.TIMER_UP,
            timer_direction="up",
            timer_visible_to_student=False,
            
            # Instructions
            assessor_script=[
                "Say: 'I'm going to show you some letters.'",
                "Say: 'Tell me the name of each letter.'",
                "Start the timer when you show the first letter.",
                "Click on letters the student gets wrong.",
                "Advance to next letter after student responds.",
                "Stop timer when all letters are complete."
            ],
            student_prompt="Tell me this letter."
        ),
        
        "scoring": {
            "primary_metric": "total_correct",
            "secondary_metrics": ["total_time_seconds", "accuracy_pct"],
            "error_types": ["incorrect", "omission", "self_correction"]
        }
    },
    
    # 2. WORD READING FLUENCY
    "FL-WRF": {
        "id": "FL-WRF",
        "name": "Word Reading Fluency", 
        "category": "Fluency",
        "domain": "Fluency",
        "grade_range": "K-3",
        "description": "Single-word reading automaticity",
        
        "content": {
            "item_type": "single_word",
            "total_items": 50,
            "item_order": "fixed_by_grade",
            "grade_levels": ["K", "1", "2", "3"],
            "forms_per_grade": 2
        },
        
        "interface": AssessmentInterface(
            student_presentation=PresentationMode.ONE_AT_A_TIME,
            student_sees_text=True,
            items_advance_mode="manual_next_button",
            
            assessor_interaction=AssessorInteraction.CLICK_CYCLE,
            click_cycle=ClickCyclePattern([
                "correct", "incorrect", "self_correct", "omission", "omission", "reset"
            ]),
            
            timing_mode=TimingMode.TIMER_DOWN_60,
            timer_direction="down",
            timer_visible_to_student=False,
            
            assessor_script=[
                "Say: 'Read each word as quickly and carefully as you can.'",
                "Start 60-second timer.",
                "Student reads one word at a time.",
                "Click words the student misreads.",
                "Stop at 60 seconds or when list complete."
            ],
            student_prompt="Read this word."
        ),
        
        "scoring": {
            "primary_metric": "words_correct_per_minute",
            "secondary_metrics": ["total_correct", "accuracy_pct"],
            "error_types": ["incorrect", "omission", "self_correction"]
        }
    },
    
    # 2.5. ORAL READING FLUENCY (NEW v2026.2)
    "FL-ORF": {
        "id": "FL-ORF",
        "name": "Oral Reading Fluency",
        "category": "Fluency",
        "domain": "Fluency",
        "grade_range": "K-8",
        "description": "Passage-based oral reading fluency with error analysis and prosody rating",
        
        "content": {
            "item_type": "passage_with_word_tracking",
            "total_items": 1,  # Single passage
            "item_order": "n/a",
            "grade_levels": ["K", "1", "2", "3", "4", "5", "6", "7", "8"],
            "forms_per_grade": 2
        },
        
        "interface": AssessmentInterface(
            # Student View
            student_presentation=PresentationMode.FULL_LIST,  # Full passage visible
            student_sees_text=True,
            items_advance_mode="n/a",
            
            # Assessor View - NEW ENUMS
            assessor_interaction=AssessorInteractionEnum.PASSAGE_ERROR_MARKING,
            click_cycle=None,  # No click cycle for passage marking
            
            # Timing - NEW ENUMS
            timing_mode=TimingModeEnum.TIMER_DOWN_FIXED,
            timer_direction="down",
            timer_visible_to_student=False,
            
            # ORF-specific extensions
            passage_marking_enabled=True,
            rubric_scoring_enabled=True,  # For prosody
            time_limit_seconds=60,
            
            # Instructions
            assessor_script=[
                "Say: 'I'm going to ask you to read this passage aloud.'",
                "Say: 'Read it as accurately and smoothly as you can.'",
                "Say: 'If you come to a word you don't know, I'll tell it to you.'",
                "Say: 'Do you have any questions?'",
                "[Answer questions, then continue]",
                "Say: 'Begin reading when I say start. Ready? Start.'",
                "Start 60-second timer immediately.",
                "Mark errors on assessor copy in real-time.",
                "Supply words after 3-second hesitation.",
                "At 60 seconds, say 'Stop' and mark last word read.",
                "Calculate WCPM and accuracy.",
                "Score prosody using 1-4 rubric."
            ],
            student_prompt="Read this passage aloud as accurately and smoothly as you can."
        ),
        
        # NEW v2026.2: Measurement specification with SPECIFIC bank entry IDs
        "measurement_spec_ref": {
            "schema_version": "2026.2",
            "scoring_rule_id": "ORF_SCORING_V1_60S",  # Specific entry, not bank name
            "benchmark_norm_id": "ORF_WCPM_NORMS_K8_V1",  # Specific entry
            "prosody_scale_id": "NAEP_MDFS_1_4_V1",  # Specific entry
            # Use error_codes_allowed as authoritative list (not error_code_set_id)
            "error_codes_allowed": [
                ErrorCodeEnum.SUBSTITUTION,
                ErrorCodeEnum.OMISSION,
                ErrorCodeEnum.INSERTION,
                ErrorCodeEnum.HESITATION_SUPPLY,
                ErrorCodeEnum.SELF_CORRECTION,
                ErrorCodeEnum.REPETITION
            ]
        },
        
        # NEW v2026.2: Response capture specification
        "response_capture_spec": {
            "capture_mode": ResponseCaptureModeEnum.PASSAGE_WORD_LEVEL,
            "event_schema_version": 1,
            
            # Word indexing and tokenization rules (deterministic)
            "word_index_base": 0,  # 0-based indexing
            "tokenization_policy": "whitespace_punct_preserved_v1",
            
            # Event schema
            "required_fields": [
                "word_index",  # int, 0-based
                "printed_word",  # str, from tokenization
                "response_state"  # ResponseStateEnum
            ],
            "optional_fields": [
                "error_code",  # ErrorCodeEnum | null
                "student_said",  # str | null (what student actually said)
                "was_supplied",  # bool (assessor supplied after 3s)
                "was_self_corrected",  # bool (student corrected within window)
                "timestamp_ms"  # int | null (milliseconds from start)
            ],
            
            # Controlled response states (enum values)
            "response_states": [
                ResponseStateEnum.CORRECT,
                ResponseStateEnum.ERROR,
                ResponseStateEnum.SELF_CORRECTED,
                ResponseStateEnum.SUPPLIED,
                ResponseStateEnum.NOT_REACHED
            ],
            
            "description": "Each word in passage generates one event. Events capture word-level reading accuracy. Error classification (counts_as_error) is derived from error_code via Error Codes bank, not stored per event."
        },
        
        # NEW v2026.2: Scoring specification (computable, structured dependency graph)
        "scoring": {
            "primary_metric": MetricEnum.WCPM,
            "secondary_metrics": [
                MetricEnum.ACCURACY_PCT,
                MetricEnum.PROSODY_SCORE,
                MetricEnum.TOTAL_ERRORS
            ],
            
            # Inputs required for scoring (deterministic sources)
            "inputs": {
                "last_word_index_read": {
                    "type": "int",
                    "source": "session_runtime",
                    "description": "0-based index of last word reached at time limit"
                },
                "time_seconds": {
                    "type": "int",
                    "source": "fixed",
                    "value": 60
                },
                "error_events": {
                    "type": "list",
                    "source": "response_capture",
                    "description": "All events where response_state == ERROR"
                },
                "prosody_score": {
                    "type": "int",
                    "source": "rubric",
                    "range": [1, 4],
                    "description": "Assessor-rated prosody using NAEP scale"
                }
            },
            
            # Computed outputs (deterministic from inputs)
            "computed_metrics": {
                "WORDS_READ": {
                    "formula": "last_word_index_read + 1",
                    "dependencies": ["last_word_index_read"],
                    "description": "Total words read in 60 seconds (0-based index + 1)"
                },
                "TOTAL_ERRORS": {
                    "formula": "count(error_events where error_code.counts_as_error == True)",
                    "dependencies": ["error_events", "error_code_bank"],
                    "description": "Only errors where counts_as_error=True in Error Codes bank"
                },
                "WCPM": {
                    "formula": "WORDS_READ - TOTAL_ERRORS",
                    "dependencies": ["WORDS_READ", "TOTAL_ERRORS"],
                    "description": "Words Correct Per Minute (primary metric)"
                },
                "ACCURACY_PCT": {
                    "formula": "(WORDS_READ - TOTAL_ERRORS) / WORDS_READ * 100",
                    "dependencies": ["WORDS_READ", "TOTAL_ERRORS"],
                    "description": "Accuracy percentage"
                }
            }
        },
        
        # NEW v2026.2: Session template (empty shell for runtime capture)
        "session_template": {
            "events": [],  # List of response events (populated during assessment)
            "rubric_scores": {
                "prosody_score": None  # int 1-4, entered by assessor
            },
            "inputs": {
                "last_word_index_read": None,  # CRITICAL: 0-based index of last word reached
                "time_seconds": 60,  # Fixed for standard ORF
                "started_at": None,  # ISO timestamp (optional)
                "ended_at": None  # ISO timestamp (optional)
            },
            "computed_metrics": {
                "WORDS_READ": None,
                "TOTAL_ERRORS": None,
                "WCPM": None,
                "ACCURACY_PCT": None
            }
        }
    },
    
    # 3. PHONEME SEGMENTATION FLUENCY
    "FL-PSF": {
        "id": "FL-PSF",
        "name": "Phoneme Segmentation Fluency",
        "category": "Phonological Awareness",
        "domain": "Phonological Awareness",
        "grade_range": "K-1",
        "description": "Rapid phoneme segmentation",
        
        "content": {
            "item_type": "spoken_word",
            "total_items": 20,
            "item_order": "fixed",
            "forms": 2
        },
        
        "interface": AssessmentInterface(
            student_presentation=PresentationMode.AUDIO_ONLY,
            student_sees_text=False,
            items_advance_mode="manual_next_button",
            
            assessor_interaction=AssessorInteraction.COUNT_INPUT,
            click_cycle=None,
            
            timing_mode=TimingMode.TIMER_DOWN_60,
            timer_direction="down",
            timer_visible_to_student=False,
            
            assessor_script=[
                "Say: 'I will say a word. You say all the sounds in the word.'",
                "Example: 'sat' → student says /s/ /a/ /t/",
                "Start 60-second timer.",
                "Say each word clearly.",
                "Count correct phonemes student produces.",
                "Move to next word after 3 seconds if no response."
            ],
            student_prompt="Tell me all the sounds."
        ),
        
        "scoring": {
            "primary_metric": "phonemes_correct_per_minute",
            "secondary_metrics": ["total_words_correct", "accuracy_pct"],
            "error_types": ["omission", "substitution", "no_response"]
        }
    },
    
    # 4. RHYME RECOGNITION
    "PA-RHYM": {
        "id": "PA-RHYM",
        "name": "Rhyme Recognition",
        "category": "Phonological Awareness",
        "domain": "Phonological Awareness",
        "grade_range": "PreK-K",
        "description": "Recognition of rhyming word pairs",
        
        "content": {
            "item_type": "spoken_word_pair",
            "total_items": 20,
            "item_order": "fixed",
            "forms": 2
        },
        
        "interface": AssessmentInterface(
            student_presentation=PresentationMode.AUDIO_ONLY,
            student_sees_text=False,
            items_advance_mode="manual_next_button",
            
            assessor_interaction=AssessorInteraction.YES_NO_BUTTONS,
            click_cycle=None,
            
            timing_mode=TimingMode.UNTIMED,
            timer_direction="none",
            timer_visible_to_student=False,
            
            assessor_script=[
                "Say: 'I will say two words. Tell me if they rhyme.'",
                "Example: 'cat - hat' (yes), 'sun - cup' (no)",
                "Say both words clearly with slight pause between.",
                "Mark student's yes/no response.",
                "Move to next pair."
            ],
            student_prompt="Do these words rhyme?"
        ),
        
        "scoring": {
            "primary_metric": "total_correct",
            "secondary_metrics": ["accuracy_pct", "false_positives", "false_negatives"],
            "error_types": ["false_positive", "false_negative", "no_response"]
        }
    },
    
    # 5. ONSET-RIME BLENDING
    "PA-OONS": {
        "id": "PA-OONS",
        "name": "Onset-Rime Blending",
        "category": "Phonological Awareness",
        "domain": "Phonological Awareness",
        "grade_range": "K-1",
        "description": "Blending onset and rime to form words",
        
        "content": {
            "item_type": "spoken_onset_rime",
            "total_items": 20,
            "item_order": "fixed",
            "forms": 2
        },
        
        "interface": AssessmentInterface(
            student_presentation=PresentationMode.AUDIO_ONLY,
            student_sees_text=False,
            items_advance_mode="manual_next_button",
            
            assessor_interaction=AssessorInteraction.CORRECT_INCORRECT,
            click_cycle=None,
            
            timing_mode=TimingMode.UNTIMED,
            timer_direction="none",
            timer_visible_to_student=False,
            
            assessor_script=[
                "Say: 'I will say two parts of a word. Put them together.'",
                "Example: 'b ... at' → student says 'bat'",
                "Say onset, pause 300-800ms, then say rime.",
                "Mark correct/incorrect/no response.",
                "Move to next item."
            ],
            student_prompt="What word do you hear?"
        ),
        
        "scoring": {
            "primary_metric": "total_correct",
            "secondary_metrics": ["accuracy_pct"],
            "error_types": ["incorrect_blend", "partial_blend", "no_response"]
        }
    },
    
    # 6. PHONEME SEGMENTATION
    "PA-PHON": {
        "id": "PA-PHON",
        "name": "Phoneme Segmentation",
        "category": "Phonological Awareness",
        "domain": "Phonological Awareness",
        "grade_range": "K-2",
        "description": "Segmenting spoken words into phonemes",
        
        "content": {
            "item_type": "spoken_word",
            "total_items": 20,
            "item_order": "fixed",
            "forms": 2
        },
        
        "interface": AssessmentInterface(
            student_presentation=PresentationMode.AUDIO_ONLY,
            student_sees_text=False,
            items_advance_mode="manual_next_button",
            
            assessor_interaction=AssessorInteraction.CORRECT_INCORRECT,
            click_cycle=None,
            
            timing_mode=TimingMode.UNTIMED,
            timer_direction="none",
            timer_visible_to_student=False,
            
            assessor_script=[
                "Say: 'I will say a word. Tell me all the sounds.'",
                "Example: 'sun' → student says /s/ /u/ /n/",
                "If student says whole word, prompt: 'Tell me the sounds.'",
                "Mark correct only if all phonemes are produced.",
                "Move to next word after response or 3 seconds."
            ],
            student_prompt="Tell me all the sounds."
        ),
        
        "scoring": {
            "primary_metric": "total_correct",
            "secondary_metrics": ["accuracy_pct"],
            "error_types": ["phoneme_omission", "phoneme_addition", "sequence_error", "no_response"]
        }
    },
    
    # 7. SYLLABLE SEGMENTATION
    "PA-SYLS": {
        "id": "PA-SYLS",
        "name": "Syllable Segmentation",
        "category": "Phonological Awareness",
        "domain": "Phonological Awareness",
        "grade_range": "PreK-1",
        "description": "Counting syllables in spoken words",
        
        "content": {
            "item_type": "spoken_word",
            "total_items": 20,
            "item_order": "fixed",
            "forms": 2
        },
        
        "interface": AssessmentInterface(
            student_presentation=PresentationMode.AUDIO_ONLY,
            student_sees_text=False,
            items_advance_mode="manual_next_button",
            
            assessor_interaction=AssessorInteraction.COUNT_INPUT,
            click_cycle=None,
            
            timing_mode=TimingMode.UNTIMED,
            timer_direction="none",
            timer_visible_to_student=False,
            
            assessor_script=[
                "Say: 'I will say a word. Clap the syllables.'",
                "Example: 'butter' → student claps 2 times",
                "Say word clearly.",
                "Count student's claps/segments.",
                "Enter number of correct syllables (partial credit allowed)."
            ],
            student_prompt="Clap the syllables."
        ),
        
        "scoring": {
            "primary_metric": "total_correct",
            "secondary_metrics": ["total_syllables_correct", "accuracy_pct"],
            "error_types": ["incorrect_count", "partial_segmentation", "no_response"]
        }
    },
    
    # 8. CONSONANT SOUND ACCURACY
    "PH-CSA": {
        "id": "PH-CSA",
        "name": "Consonant Sound Accuracy",
        "category": "Phonics",
        "domain": "Phonics",
        "grade_range": "PreK-1",
        "description": "Letter-sound correspondence for consonants",
        
        "content": {
            "item_type": "letter_or_digraph",
            "total_items": 24,  # b,c,d,f,g,h,j,k,l,m,n,p,q,r,s,t,v,w,x,y,z,ch,sh,th
            "item_order": "randomized_fixed",
            "forms": 2
        },
        
        "interface": AssessmentInterface(
            student_presentation=PresentationMode.ONE_AT_A_TIME,
            student_sees_text=True,
            items_advance_mode="manual_next_button",
            
            assessor_interaction=AssessorInteraction.CORRECT_INCORRECT,
            click_cycle=None,
            
            timing_mode=TimingMode.UNTIMED,
            timer_direction="none",
            timer_visible_to_student=False,
            
            assessor_script=[
                "Say: 'I will show you some letters.'",
                "Say: 'Tell me the sound each letter makes.'",
                "Show each letter one at a time.",
                "Mark correct if sound is accurate.",
                "Move to next letter."
            ],
            student_prompt="What sound does this letter make?"
        ),
        
        "scoring": {
            "primary_metric": "total_correct",
            "secondary_metrics": ["accuracy_pct"],
            "error_types": ["incorrect_sound", "no_response", "articulation_variant"]
        }
    },
    
    # 8.5. CVC BLENDING
    "PH-CVC": {
        "id": "PH-CVC",
        "name": "CVC Blending",
        "category": "CVC Blending",
        "domain": "Phonics",
        "grade_range": "K-1",
        "description": "Blending consonant-vowel-consonant words with all medial vowels",
        
        "content": {
            "item_type": "single_word",
            "total_items": 25,  # 20 real words (4 per vowel) + 5 nonsense words
            "item_order": "randomized_fixed",
            "forms": 2
        },
        
        "interface": AssessmentInterface(
            student_presentation=PresentationMode.ONE_AT_A_TIME,
            student_sees_text=True,
            items_advance_mode="manual_next_button",
            
            assessor_interaction=AssessorInteraction.CLICK_CYCLE,
            click_cycle=ClickCyclePattern([
                "correct", "incorrect", "self_correct", "omission", "omission", "reset"
            ]),
            
            timing_mode=TimingMode.UNTIMED,
            timer_direction="none",
            timer_visible_to_student=False,
            
            assessor_script=[
                "Say: 'I will show you some words. Read each word.'",
                "Show each word one at a time.",
                "Mark correct if word is read accurately.",
                "Mark incorrect if word is misread or skipped.",
                "Move to next word after response."
            ],
            student_prompt="Read this word."
        ),
        
        "scoring": {
            "primary_metric": "total_correct",
            "secondary_metrics": ["accuracy_pct", "vowel_accuracy"],
            "error_types": ["incorrect", "omission", "self_correction"]
        }
    },
    
    # 9. LETTER-WORD IDENTIFICATION
    "PH-LWID": {
        "id": "PH-LWID",
        "name": "Letter-Word Identification",
        "category": "Phonics",
        "domain": "Phonics",
        "grade_range": "K-3",
        "description": "Letter identification and word reading",
        
        "content": {
            "item_type": "letter_or_word",
            "total_items": 40,
            "item_order": "fixed_by_grade_band",
            "grade_bands": ["K", "G1", "G2_3"],
            "forms_per_band": 2
        },
        
        "interface": AssessmentInterface(
            student_presentation=PresentationMode.ONE_AT_A_TIME,
            student_sees_text=True,
            items_advance_mode="manual_next_button",
            
            assessor_interaction=AssessorInteraction.CORRECT_INCORRECT,
            click_cycle=None,
            
            timing_mode=TimingMode.UNTIMED,
            timer_direction="none",
            timer_visible_to_student=False,
            
            assessor_script=[
                "Say: 'Tell me this letter' OR 'Read this word'",
                "Show each item one at a time.",
                "Mark correct if named/read accurately.",
                "Mark incorrect if misread, skipped, or no response.",
                "Move to next item."
            ],
            student_prompt="Tell me this letter / Read this word."
        ),
        
        "scoring": {
            "primary_metric": "total_correct",
            "secondary_metrics": ["letter_correct", "word_correct", "accuracy_pct"],
            "error_types": ["misidentification", "substitution", "omission", "no_response"]
        }
    },
    
    # 10. MORPHOPHONEMIC PATTERNS
    "PH-MPHY": {
        "id": "PH-MPHY",
        "name": "Morphophonemic Patterns",
        "category": "Phonics",
        "domain": "Phonics",
        "grade_range": "3-8",
        "description": "Morphophonemic awareness and accurate pronunciation of affixed words",
        
        "content": {
            "item_type": "printed_affixed_word_with_base_context",
            "total_items": 25,
            "item_order": "fixed_persisted",
            "forms": 2,
            "difficulty_distribution": {"easy": 10, "medium": 10, "hard": 5}
        },
        
        "interface": AssessmentInterface(
            student_presentation=PresentationMode.ONE_AT_A_TIME,
            student_sees_text=True,
            items_advance_mode="manual_next_button",
            
            assessor_interaction=AssessorInteraction.CORRECT_INCORRECT,
            click_cycle=None,
            
            timing_mode=TimingMode.UNTIMED,
            timer_direction="none",
            timer_visible_to_student=False,
            
            assessor_script=[
                "Display each word one at a time.",
                "Say: 'Read this word aloud.'",
                "Mark correct if pronunciation reflects the expected morphophonemic change.",
                "Mark incorrect and select error type if applicable.",
                "No response after 3 seconds."
            ],
            student_prompt="Read this word aloud."
        ),
        
        "scoring": {
            "primary_metric": "total_correct",
            "secondary_metrics": ["total_presented", "accuracy_pct", "error_by_change_type"],
            "error_types": ["incorrect_pronunciation", "incorrect_morphological_application", "substitution", "no_response"]
        }
    },
    
    # 11. PSEUDOWORD DECODING
    "PH-PSWD": {
        "id": "PH-PSWD",
        "name": "Pseudoword Decoding",
        "category": "Phonics",
        "domain": "Phonics",
        "grade_range": "K-3",
        "description": "Phonics pattern application to novel pseudowords",
        
        "content": {
            "item_type": "printed_pseudoword",
            "total_items": 30,
            "item_order": "fixed_persisted",
            "grade_bands": ["Kindergarten", "Grade 1", "Grade 2-3"],
            "forms_per_band": 2
        },
        
        "interface": AssessmentInterface(
            student_presentation=PresentationMode.ONE_AT_A_TIME,
            student_sees_text=True,
            items_advance_mode="manual_next_button",
            
            assessor_interaction=AssessorInteraction.CORRECT_INCORRECT,
            click_cycle=None,
            
            timing_mode=TimingMode.UNTIMED,
            timer_direction="none",
            timer_visible_to_student=False,
            
            assessor_script=[
                "Say: 'Read this made-up word.'",
                "Remind student the word is not real and should be sounded out.",
                "Mark correct if pronunciation matches expected phonics pattern.",
                "Move to next word."
            ],
            student_prompt="Read this made-up word."
        ),
        
        "scoring": {
            "primary_metric": "total_correct",
            "secondary_metrics": ["total_presented", "accuracy_pct", "error_by_phonics_pattern"],
            "error_types": ["mispronunciation", "pattern_violation", "substitution", "no_response"]
        }
    },
    
    # 12. SPELLING INVENTORY
    "PH-SPEL": {
        "id": "PH-SPEL",
        "name": "Spelling Inventory",
        "category": "Phonics",
        "domain": "Phonics",
        "grade_range": "K-8",
        "description": "Orthographic feature mastery across developmental spelling stages",
        
        "content": {
            "item_type": "dictated_word_with_feature_map",
            "total_items": 20,
            "item_order": "fixed_persisted",
            "grade_levels": list(range(9)),  # K-8
            "forms_per_level": 2
        },
        
        "interface": AssessmentInterface(
            student_presentation=PresentationMode.AUDIO_ONLY,
            student_sees_text=False,
            items_advance_mode="manual_next_button",
            
            assessor_interaction=AssessorInteraction.CORRECT_INCORRECT,
            click_cycle=None,
            
            timing_mode=TimingMode.UNTIMED,
            timer_direction="none",
            timer_visible_to_student=False,
            
            assessor_script=[
                "Say the word.",
                "Use the word in a sentence.",
                "Repeat the word.",
                "Student spells the word.",
                "Record exactly what the student writes or types."
            ],
            student_prompt="Spell the word."
        ),
        
        "scoring": {
            "primary_metric": "total_words_correct",
            "secondary_metrics": ["total_features_correct", "feature_accuracy_by_band", "stage_profile"],
            "error_types": ["phoneme_omission", "grapheme_substitution", "illegal_pattern", "overgeneralization", "morpheme_error", "reversal", "no_response"]
        }
    },
    
    # 13. WORD PATTERN KNOWLEDGE
    "PH-WPAT": {
        "id": "PH-WPAT",
        "name": "Word Pattern Knowledge",
        "category": "Phonics",
        "domain": "Phonics",
        "grade_range": "1-5",
        "description": "Orthographic pattern recognition and classification",
        
        "content": {
            "item_type": "pattern_identification_or_selection",
            "total_items": 25,
            "item_order": "fixed_persisted",
            "forms": 2
        },
        
        "interface": AssessmentInterface(
            student_presentation=PresentationMode.ONE_AT_A_TIME,
            student_sees_text=True,
            items_advance_mode="manual_next_button",
            
            assessor_interaction=AssessorInteraction.CORRECT_INCORRECT,
            click_cycle=None,
            
            timing_mode=TimingMode.UNTIMED,
            timer_direction="none",
            timer_visible_to_student=False,
            
            assessor_script=[
                "Say: 'Look at these words and find the one that matches the pattern.'",
                "Or: 'Which word does not follow the same pattern?'",
                "Student selects or says the answer.",
                "Mark correct/incorrect."
            ],
            student_prompt="Which word matches the pattern?"
        ),
        
        "scoring": {
            "primary_metric": "total_correct",
            "secondary_metrics": ["total_presented", "accuracy_pct", "correct_by_pattern_category"],
            "error_types": ["pattern_confusion", "incorrect_selection", "no_response"]
        }
    },
    
    # ===== REMOVED ASSESSMENTS (No Generators Yet) =====
    # RC-* assessments have been removed from the registry until generators are built.
    # They were: RC-INFO, RC-LIST, RC-MAZE, RC-NARR, RC-SENT
    # Can be restored from git history when generators are ready.
    # ===== END REMOVED ASSESSMENTS =====
    
    # 19. EXPRESSIVE PICTURE VOCABULARY
    "VO-EPVT": {
        "id": "VO-EPVT",
        "name": "Expressive Picture Vocabulary",
        "category": "Vocabulary",
        "domain": "Vocabulary",
        "grade_range": "PreK-3",
        "description": "Oral naming of pictured objects, actions, or concepts",
        
        "content": {
            "item_type": "single_image_oral_naming",
            "total_items": 30,
            "item_order": "fixed_persisted",
            "grade_bands": ["PreK", "K", "1", "2", "3"],
            "forms_per_band": 2
        },
        
        "interface": AssessmentInterface(
            student_presentation=PresentationMode.ONE_AT_A_TIME,
            student_sees_text=False,  # Images only
            items_advance_mode="manual_next_button",
            
            assessor_interaction=AssessorInteraction.CORRECT_INCORRECT,
            click_cycle=None,
            
            timing_mode=TimingMode.UNTIMED,
            timer_direction="none",
            timer_visible_to_student=False,
            
            assessor_script=[
                "Say: 'What is this?' or 'What do you see?'",
                "Accept the first clear response only.",
                "Do not cue, prompt, or correct the student.",
                "Mark correct if response matches target_word or acceptable_synonyms."
            ],
            student_prompt="What is this?"
        ),
        
        "scoring": {
            "primary_metric": "total_correct",
            "secondary_metrics": ["accuracy_percent", "correct_by_semantic_category", "synonym_hits_count", "no_response_count"],
            "error_types": ["semantic_error", "phonological_error", "unrelated_response", "no_response"]
        }
    },
    
    # 20. MORPHOLOGICAL AWARENESS
    "VO-MORP": {
        "id": "VO-MORP",
        "name": "Morphological Awareness",
        "category": "Vocabulary",
        "domain": "Vocabulary",
        "grade_range": "2-8",
        "description": "Understanding of word meaning changes produced by prefixes, suffixes, and roots",
        
        "content": {
            "item_type": "morpheme_meaning_mcq",
            "total_items": 24,
            "item_order": "fixed_persisted",
            "grade_levels": list(range(2, 9)),  # Grade 2-8
            "forms_per_level": 2
        },
        
        "interface": AssessmentInterface(
            student_presentation=PresentationMode.ONE_AT_A_TIME,
            student_sees_text=True,
            items_advance_mode="manual_next_button",
            
            assessor_interaction=AssessorInteraction.CORRECT_INCORRECT,
            click_cycle=None,
            
            timing_mode=TimingMode.UNTIMED,
            timer_direction="none",
            timer_visible_to_student=False,
            
            assessor_script=[
                "Read each word and choose the definition that best matches its meaning.",
                "Assessor may assist with reading if needed.",
                "Student selects answer.",
                "Mark correct/incorrect."
            ],
            student_prompt="Choose the definition that best matches the word."
        ),
        
        "scoring": {
            "primary_metric": "total_correct",
            "secondary_metrics": ["accuracy_percent", "correct_by_morpheme_type"],
            "error_types": ["semantic_confusion", "affix_misinterpretation", "guessing", "no_response"]
        }
    },
    
    # 21. RECEPTIVE PICTURE VOCABULARY
    "VO-RPVT": {
        "id": "VO-RPVT",
        "name": "Receptive Picture Vocabulary",
        "category": "Vocabulary",
        "domain": "Vocabulary",
        "grade_range": "PreK-2",
        "description": "Recognition of spoken word meaning via image selection",
        
        "content": {
            "item_type": "spoken_word_to_image_selection",
            "total_items": 30,
            "item_order": "fixed_persisted",
            "grade_bands": ["PreK", "K", "1", "2"],
            "forms_per_band": 2
        },
        
        "interface": AssessmentInterface(
            student_presentation=PresentationMode.ONE_AT_A_TIME,
            student_sees_text=False,  # Images only
            items_advance_mode="manual_next_button",
            
            assessor_interaction=AssessorInteraction.CORRECT_INCORRECT,
            click_cycle=None,
            
            timing_mode=TimingMode.UNTIMED,
            timer_direction="none",
            timer_visible_to_student=False,
            
            assessor_script=[
                "Say or play the word.",
                "Student selects the matching image from four options.",
                "Assessor may repeat the word once if needed.",
                "Mark correct/incorrect."
            ],
            student_prompt="Point to or select the picture that shows the word."
        ),
        
        "scoring": {
            "primary_metric": "total_correct",
            "secondary_metrics": ["accuracy_percent", "no_response_count"],
            "error_types": ["incorrect_selection", "no_response", "random_guess"]
        }
    },
    
    # 22. VOCABULARY IN CONTEXT
    "VO-VOCA": {
        "id": "VO-VOCA",
        "name": "Vocabulary in Context",
        "category": "Vocabulary",
        "domain": "Vocabulary",
        "grade_range": "2-8",
        "description": "Understanding word meaning from sentence context",
        
        "content": {
            "item_type": "context_sentence_mcq",
            "total_items": 24,
            "item_order": "fixed_persisted",
            "grade_levels": list(range(2, 9)),  # Grade 2-8
            "forms_per_level": 2
        },
        
        "interface": AssessmentInterface(
            student_presentation=PresentationMode.ONE_AT_A_TIME,
            student_sees_text=True,
            items_advance_mode="manual_next_button",
            
            assessor_interaction=AssessorInteraction.CORRECT_INCORRECT,
            click_cycle=None,
            
            timing_mode=TimingMode.UNTIMED,
            timer_direction="none",
            timer_visible_to_student=False,
            
            assessor_script=[
                "Read the sentence.",
                "Choose the definition that best matches the highlighted word.",
                "Assessor may assist with reading if needed.",
                "Student selects answer.",
                "Mark correct/incorrect."
            ],
            student_prompt="Choose the definition that best matches the highlighted word."
        ),
        
        "scoring": {
            "primary_metric": "total_correct",
            "secondary_metrics": ["accuracy_percent"],
            "error_types": ["context_misinterpretation", "definition_confusion", "guessing", "no_response"]
        }
    }
}


def get_assessment(assessment_id: str) -> Optional[Dict]:
    """Get assessment specification by ID"""
    return ASSESSMENTS.get(assessment_id)


def get_assessment_summary():
    """Print complete assessment catalog"""
    categories = {}
    for asr_id, asr in ASSESSMENTS.items():
        cat = asr['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(asr)
    
    print("="*70)
    print("COMPLETE ASSESSMENT CATALOG")
    print("="*70)
    
    for cat, assessments in categories.items():
        print(f"\n{cat} ({len(assessments)} assessments):")
        for asr in assessments:
            print(f"  • {asr['name']} ({asr['grade_range']})")
            print(f"    - Items: {asr['content']['total_items']}")
            print(f"    - Presentation: {asr['interface'].student_presentation.value}")
            print(f"    - Timing: {asr['interface'].timing_mode.value}")
    
    print(f"\n{'='*70}")
    print(f"Total Assessments: {len(ASSESSMENTS)}")
    print(f"{'='*70}")


if __name__ == "__main__":
    get_assessment_summary()
