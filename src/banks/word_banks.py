"""
Word Banks Module

Word lists and content banks organized by grade level, assessment type, and difficulty.
Used by simple assessment generators for form generation.
"""

from typing import List, Dict, Optional
import random


# === LETTER RECOGNITION ===
LETTERS_UPPERCASE = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
LETTERS_LOWERCASE = list("abcdefghijklmnopqrstuvwxyz")
LETTERS_ALL = LETTERS_UPPERCASE + LETTERS_LOWERCASE

# === CONSONANTS AND DIGRAPHS ===
CONSONANTS_SINGLE = list("bcdfghjklmnpqrstvwxyz")
CONSONANTS_DIGRAPHS = ["ch", "sh", "th", "wh", "ph", "ck"]
CONSONANTS_ALL = CONSONANTS_SINGLE + CONSONANTS_DIGRAPHS


# === WORD LISTS BY GRADE ===

# Grade K Word Lists (Simple CVC, High Frequency) - Used for CVC Blending
WORDS_GRADE_K = [
    "cat", "dog", "bat", "hat", "sit", "run", "sun", "fun",
    "map", "cap", "top", "mop", "big", "pig", "wig", "fig",
    "bed", "red", "leg", "peg", "cup", "pup", "bus", "us",
    "fox", "box", "fix", "mix", "yes", "web", "get", "let",
    "not", "hot", "pot", "lot", "had", "mad", "sad", "dad",
    "can", "man", "pan", "van", "ten", "pen", "hen", "men"
]

# === DOLCH SIGHT WORDS BY GRADE ===
# Dolch word lists for Word Reading Fluency (FL-WRF)

# Pre-K (Pre-Primer) Dolch Words
DOLCH_PREK = [
    "a", "and", "away", "big", "blue", "can", "come", "down", "find", "for",
    "funny", "go", "help", "here", "I", "in", "is", "it", "jump", "little",
    "look", "make", "me", "my", "not", "one", "play", "red", "run", "said",
    "see", "the", "three", "to", "two", "up", "we", "where", "yellow", "you"
]

# Kindergarten (Primer) Dolch Words
DOLCH_K = [
    "all", "am", "are", "at", "ate", "be", "black", "brown", "but", "came",
    "did", "do", "eat", "four", "get", "good", "have", "he", "into", "like",
    "must", "new", "no", "now", "on", "our", "out", "please", "pretty", "ran",
    "ride", "saw", "say", "she", "so", "soon", "that", "there", "they", "this",
    "too", "under", "want", "was", "well", "went", "what", "white", "who", "will",
    "with", "yes"
]

# 1st Grade Dolch Words
DOLCH_1 = [
    "after", "again", "an", "any", "as", "ask", "by", "could", "every", "fly",
    "from", "give", "going", "had", "has", "her", "him", "his", "how", "just",
    "know", "let", "live", "may", "of", "old", "once", "open", "over", "put",
    "round", "some", "stop", "take", "thank", "them", "then", "think", "walk", "were",
    "when"
]

# 2nd Grade Dolch Words
DOLCH_2 = [
    "always", "around", "because", "been", "before", "best", "both", "buy", "call", "cold",
    "does", "don't", "fast", "first", "five", "found", "gave", "goes", "green", "its",
    "left", "made", "many", "off", "or", "pull", "read", "right", "sing", "sit",
    "sleep", "tell", "their", "these", "those", "upon", "us", "use", "very", "wash",
    "which", "why", "wish", "work", "would", "write", "your"
]

# 3rd Grade Dolch Words
DOLCH_3 = [
    "about", "better", "bring", "carry", "clean", "cut", "done", "draw", "drink", "eight",
    "fall", "far", "full", "got", "grow", "hold", "hot", "hurt", "if", "keep",
    "kind", "laugh", "light", "long", "much", "myself", "never", "only", "own", "pick",
    "seven", "shall", "show", "six", "small", "start", "ten", "today", "together", "try",
    "warm"
]

# Grade 1 Word Lists (CVC, CVCC, CCVC, Simple Sight Words)
WORDS_GRADE_1 = [
    "jump", "lamp", "best", "nest", "fast", "last", "hand", "land",
    "wind", "find", "cold", "hold", "told", "fold", "stop", "drop",
    "frog", "clog", "swim", "trim", "skip", "chip", "snap", "trap",
    "drum", "grum", "plug", "slug", "club", "flub", "swim", "brim",
    "then", "when", "this", "that", "with", "what", "they", "them",
    "have", "give", "live", "five", "came", "name", "same", "game",
    "like", "bike", "make", "take", "time", "lime", "come", "some",
    "want", "went", "sent", "bent", "tent", "rent", "help", "yelp"
]

# Grade 2 Word Lists (Long Vowels, Blends, Digraphs)
WORDS_GRADE_2 = [
    "boat", "coat", "goat", "road", "soap", "toast", "beach", "teach",
    "reach", "peach", "chair", "pair", "fair", "hair", "care", "dare",
    "share", "square", "bird", "third", "girl", "curl", "turn", "burn",
    "corn", "torn", "born", "thorn", "blue", "glue", "true", "clue",
    "snow", "grow", "show", "blow", "flow", "know", "moon", "soon",
    "cool", "pool", "tool", "fool", "book", "look", "took", "hook",
    "light", "right", "night", "fight", "tight", "bright", "sight", "might",
    "catch", "match", "patch", "watch", "witch", "pitch", "switch", "stretch"
]

# Grade 3 Word Lists (Multisyllabic, Complex Patterns)
WORDS_GRADE_3 = [
    "butter", "better", "letter", "water", "matter", "pattern", "latter", "batter",
    "fishing", "wishing", "washing", "crashing", "smashing", "rushing", "brushing", "pushing",
    "happy", "puppy", "funny", "sunny", "runny", "bunny", "penny", "jenny",
    "candle", "handle", "bundle", "middle", "riddle", "paddle", "saddle", "meddle",
    "eagle", "beagle", "people", "apple", "middle", "bubble", "trouble", "double",
    "garden", "hardened", "pardon", "bargain", "margin", "carpet", "market", "target",
    "silent", "polent", "client", "recent", "decent", "percent", "accent", "ascent",
    "complete", "compete", "delete", "repeat", "defeat", "retreat", "concrete", "discrete"
]


# === PHONEME SEGMENTATION WORDS ===
# Simple words for phoneme segmentation (3-5 phonemes)
PHONEME_SEGMENTATION_WORDS = [
    "cat", "dog", "sun", "hat", "mop", "leg", "cup", "fox",
    "fish", "book", "hand", "jump", "lamp", "wind", "cold", "stop",
    "frog", "swim", "nest", "fast", "then", "this", "chip", "snap",
    "clock", "black", "stamp", "plant", "splash", "truck", "dress", "brush"
]


# === RHYMING WORD PAIRS ===
# Format: (word1, word2, rhymes: bool)
RHYMING_PAIRS = [
    # Rhyming pairs (True)
    ("cat", "hat", True),
    ("dog", "frog", True),
    ("sun", "fun", True),
    ("mop", "hop", True),
    ("leg", "peg", True),
    ("cup", "pup", True),
    ("fox", "box", True),
    ("fish", "wish", True),
    ("book", "look", True),
    ("hand", "land", True),
    ("jump", "bump", True),
    ("lamp", "stamp", True),
    ("wind", "find", True),
    ("cold", "hold", True),
    ("stop", "drop", True),
    ("chair", "pair", True),
    ("bird", "word", True),
    ("light", "night", True),
    ("boat", "coat", True),
    ("moon", "soon", True),
    
    # Non-rhyming pairs (False)
    ("cat", "dog", False),
    ("sun", "hat", False),
    ("mop", "leg", False),
    ("cup", "fox", False),
    ("fish", "book", False),
    ("hand", "jump", False),
    ("lamp", "wind", False),
    ("cold", "stop", False),
    ("chair", "bird", False),
    ("light", "boat", False),
    ("moon", "cat", False),
    ("dog", "sun", False),
    ("hat", "mop", False),
    ("leg", "cup", False),
    ("fox", "fish", False),
    ("book", "hand", False),
    ("jump", "lamp", False),
    ("wind", "cold", False),
    ("stop", "chair", False),
    ("bird", "light", False)
]


# === ONSET-RIME PAIRS ===
# Format: (onset, rime, word)
ONSET_RIME_PAIRS = [
    ("b", "at", "bat"),
    ("c", "at", "cat"),
    ("h", "at", "hat"),
    ("m", "at", "mat"),
    ("s", "at", "sat"),
    ("d", "og", "dog"),
    ("f", "og", "fog"),
    ("l", "og", "log"),
    ("j", "og", "jog"),
    ("s", "un", "sun"),
    ("r", "un", "run"),
    ("f", "un", "fun"),
    ("b", "ed", "bed"),
    ("r", "ed", "red"),
    ("l", "ed", "led"),
    ("w", "ed", "wed"),
    ("c", "up", "cup"),
    ("p", "up", "pup"),
    ("m", "op", "mop"),
    ("t", "op", "top"),
    ("h", "op", "hop"),
    ("p", "op", "pop"),
    ("b", "ig", "big"),
    ("p", "ig", "pig"),
    ("w", "ig", "wig"),
    ("d", "ig", "dig"),
    ("f", "ox", "fox"),
    ("b", "ox", "box"),
    ("f", "ix", "fix"),
    ("m", "ix", "mix")
]


# === SYLLABLE SEGMENTATION WORDS ===
# Format: (word, syllable_count)
SYLLABLE_WORDS = [
    ("cat", 1),
    ("dog", 1),
    ("sun", 1),
    ("hat", 1),
    ("mop", 1),
    ("butter", 2),
    ("water", 2),
    ("happy", 2),
    ("puppy", 2),
    ("apple", 2),
    ("candle", 2),
    ("garden", 2),
    ("eagle", 2),
    ("table", 2),
    ("tiger", 2),
    ("butterfly", 3),
    ("elephant", 3),
    ("banana", 3),
    ("camera", 3),
    ("hospital", 3),
    ("computer", 3),
    ("telephone", 3),
    ("beautiful", 3),
    ("family", 3),
    ("animal", 3)
]


# === LETTER-WORD MIXES BY GRADE BAND ===

# Kindergarten: Mostly letters, few simple words
LETTER_WORD_K = (
    ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
     "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"] +
    ["cat", "dog", "sun", "hat"]
) * 2  # Repeat to get ~40 items

# Grade 1: Mix of letters and simple words
LETTER_WORD_G1 = (
    ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"] +
    ["cat", "dog", "run", "jump", "hat", "map", "top", "leg", "cup", "fox",
     "fish", "book", "hand", "lamp", "wind", "cold", "stop", "then", "this", "with"]
) * 2  # Repeat to get ~40 items

# Grades 2-3: More words, fewer letters
LETTER_WORD_G2_3 = (
    ["A", "B", "C", "D", "E"] +
    ["boat", "coat", "beach", "chair", "bird", "blue", "snow", "light", "catch", "match",
     "butter", "water", "happy", "garden", "eagle", "complete", "fishing", "candle", "silent", "people"]
) * 2  # Repeat to get ~40 items


# === HELPER FUNCTIONS ===

def get_words_by_grade(grade: str) -> List[str]:
    """Get word list for a specific grade (CVC words - used for CVC Blending)"""
    grade = grade.upper()
    if grade == "K":
        return WORDS_GRADE_K.copy()
    elif grade == "1":
        return WORDS_GRADE_1.copy()
    elif grade == "2":
        return WORDS_GRADE_2.copy()
    elif grade == "3":
        return WORDS_GRADE_3.copy()
    else:
        return WORDS_GRADE_K.copy()  # Default


def get_dolch_words_by_grade(grade: str) -> List[str]:
    """Get Dolch sight words for a specific grade (used for Word Reading Fluency)"""
    grade = grade.upper()
    if grade == "K":
        # Combine Pre-K and K Dolch words for Kindergarten
        return (DOLCH_PREK + DOLCH_K).copy()
    elif grade == "1":
        return DOLCH_1.copy()
    elif grade == "2":
        return DOLCH_2.copy()
    elif grade == "3":
        return DOLCH_3.copy()
    else:
        # Default to Pre-K + K for unknown grades
        return (DOLCH_PREK + DOLCH_K).copy()


def get_rhyming_pairs(count: int = 20, seed: Optional[int] = None) -> List[Dict[str, any]]:
    """Get rhyming word pairs"""
    if seed is not None:
        random.seed(seed)
    pairs = RHYMING_PAIRS.copy()
    random.shuffle(pairs)
    return [
        {"word1": w1, "word2": w2, "rhymes": rhymes, "correct": rhymes}
        for w1, w2, rhymes in pairs[:count]
    ]


def get_onset_rime_pairs(count: int = 20, seed: Optional[int] = None) -> List[Dict[str, str]]:
    """Get onset-rime pairs"""
    if seed is not None:
        random.seed(seed)
    pairs = ONSET_RIME_PAIRS.copy()
    random.shuffle(pairs)
    return [
        {"onset": o, "rime": r, "word": w}
        for o, r, w in pairs[:count]
    ]


def get_syllable_words(count: int = 20, seed: Optional[int] = None) -> List[Dict[str, any]]:
    """Get words with syllable counts"""
    if seed is not None:
        random.seed(seed)
    words = SYLLABLE_WORDS.copy()
    random.shuffle(words)
    return [
        {"word": w, "syllable_count": count}
        for w, count in words[:count]
    ]


def get_letter_word_mix(grade_band: str, count: int = 40, seed: Optional[int] = None) -> List[str]:
    """Get letter-word mix for grade band"""
    if seed is not None:
        random.seed(seed)
    
    if grade_band == "K":
        items = LETTER_WORD_K.copy()
    elif grade_band == "G1":
        items = LETTER_WORD_G1.copy()
    elif grade_band == "G2_3":
        items = LETTER_WORD_G2_3.copy()
    else:
        items = LETTER_WORD_K.copy()
    
    random.shuffle(items)
    return items[:count]


def get_all_letters(scrambled: bool = True, seed: Optional[int] = None) -> List[str]:
    """Get all 52 letters (upper + lower)"""
    letters = LETTERS_ALL.copy()
    if scrambled:
        if seed is not None:
            random.seed(seed)
        random.shuffle(letters)
    return letters


def get_consonants(count: int = 24, seed: Optional[int] = None) -> List[str]:
    """Get consonant letters and digraphs"""
    if seed is not None:
        random.seed(seed)
    consonants = CONSONANTS_ALL.copy()
    random.shuffle(consonants)
    return consonants[:count]


def get_phoneme_segmentation_words(count: int = 20, seed: Optional[int] = None) -> List[str]:
    """Get words for phoneme segmentation"""
    if seed is not None:
        random.seed(seed)
    words = PHONEME_SEGMENTATION_WORDS.copy()
    random.shuffle(words)
    return words[:count]
