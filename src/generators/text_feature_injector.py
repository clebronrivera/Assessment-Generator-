"""
Text Feature Injector (Grades 6+ Specific)
Uses Bank 7 (Text Structures) for organizational features
Adds headings and organizational features to nonfiction passages for grades 6+
"""

from typing import Dict, Any, Optional
from datetime import datetime
import re

from ..banks import get_comp_word_count, get_structure_names
from ..utils.template_loader import TemplateLoader
from ..utils.ai_client import AIClient


class TextFeatureInjector:
    """Adds text features (headings, lists, etc.) to nonfiction passages for grades 6+."""
    
    def __init__(self, ai_client: AIClient, template_dir: Optional[str] = None):
        self.ai_client = ai_client
        self.template_loader = TemplateLoader(template_dir)
        self.max_attempts = 3
    
    def generate(
        self,
        passage_text: str,
        grade: str,
        genre: str = "nonfiction",
        max_attempts: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Add text features to a nonfiction passage for grades 6+.
        
        Args:
            passage_text: The original passage text
            grade: Grade level ("6", "7", "8", or "8+")
            genre: Text genre (default: "nonfiction")
            max_attempts: Maximum retry attempts (default: 3)
            
        Returns:
            Dictionary with enhanced passage and metadata
        """
        if grade not in ["6", "7", "8", "8+"]:
            raise ValueError(f"Text Feature Injector only supports grades 6, 7, 8, and 8+, got: {grade}")
        
        if max_attempts is None:
            max_attempts = self.max_attempts
        
        # Get specifications from banks
        word_count_spec = get_comp_word_count(grade)
        structure_names = get_structure_names(genre)
        specs = self._get_specs_from_banks(grade, genre, passage_text, word_count_spec, structure_names)
        
        # Render template
        prompt = self.template_loader.render("text_features.j2", **specs)
        
        # Generate enhanced passage
        attempts = 0
        enhanced_passage = None
        last_error = None
        
        while attempts < max_attempts:
            try:
                enhanced_passage = self.ai_client.complete(prompt)
                
                # Validate
                validation_results = self._validate_enhanced_passage(
                    enhanced_passage, passage_text, specs
                )
                
                if validation_results["valid"]:
                    break
                else:
                    last_error = validation_results["errors"][0] if validation_results["errors"] else "Validation failed"
                    attempts += 1
                    if attempts < max_attempts:
                        # Add error feedback to prompt for retry
                        prompt = f"{prompt}\n\nPrevious attempt failed: {last_error}\nPlease try again with the corrections."
            except Exception as e:
                last_error = str(e)
                attempts += 1
                if attempts < max_attempts:
                    continue
                else:
                    raise
        
        if enhanced_passage is None:
            raise RuntimeError(f"Failed to add text features after {max_attempts} attempts. Last error: {last_error}")
        
        # Final validation
        validation_results = self._validate_enhanced_passage(
            enhanced_passage, passage_text, specs
        )
        
        # Extract features for metadata
        features = self._extract_features(enhanced_passage)
        
        # Build result
        result = {
            "success": validation_results["valid"],
            "original_passage": passage_text,
            "enhanced_passage": enhanced_passage,
            "features": features,
            "metadata": {
                "grade": grade,
                "genre": genre,
                "original_word_count": self._count_words(passage_text),
                "enhanced_word_count": self._count_words(enhanced_passage),
                "word_count_change": self._count_words(enhanced_passage) - self._count_words(passage_text),
                "timestamp": datetime.now().isoformat(),
                "schema_version": "2026.1",
                "generator": "TextFeatureInjector",
                "attempts": attempts + 1
            },
            "bank_usage": specs['bank_usage'],
            "validation": validation_results,
            "prompt_used": prompt
        }
        
        return result
    
    def _get_specs_from_banks(
        self,
        grade: str,
        genre: str,
        passage_text: str,
        word_count_spec,
        structure_names
    ) -> Dict[str, Any]:
        """Get specifications from banks."""
        original_word_count = self._count_words(passage_text)
        
        specs = {
            'grade': grade,
            'passage_text': passage_text,
            'word_count_min': word_count_spec.min_word_count,
            'word_count_max': word_count_spec.max_word_count,
            'target_word_count': word_count_spec.target_word_count,
            'original_word_count': original_word_count,
            'structure_names': structure_names,
            'bank_usage': {
                'Bank 3 (Comp Word Counts)': f"Grade {grade} - Target: {word_count_spec.target_word_count} words (range: {word_count_spec.min_word_count}-{word_count_spec.max_word_count})",
                'Bank 7 (Text Structures)': f"Genre: {genre}, Structures: {', '.join(structure_names)}"
            }
        }
        
        return specs
    
    def _validate_enhanced_passage(
        self,
        enhanced_passage: str,
        original_passage: str,
        specs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate enhanced passage with text features."""
        validation = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "checks": {}
        }
        
        if not enhanced_passage or len(enhanced_passage.strip()) < 50:
            validation["valid"] = False
            validation["errors"].append("Enhanced passage is empty or too short")
            validation["checks"]["has_content"] = False
            return validation
        
        validation["checks"]["has_content"] = True
        
        # Check for headings (1-2 required)
        headings = self._extract_headings(enhanced_passage)
        heading_count = len(headings)
        
        if heading_count == 0:
            validation["valid"] = False
            validation["errors"].append("No headings found (1-2 headings required)")
            validation["checks"]["has_headings"] = False
        elif heading_count > 2:
            validation["warnings"].append(f"Found {heading_count} headings (recommended: 1-2)")
            validation["checks"]["has_headings"] = True
        else:
            validation["checks"]["has_headings"] = True
        
        # Check for organizational feature (one required)
        has_bullets = bool(re.search(r'^[\s]*[•\-\*]\s+', enhanced_passage, re.MULTILINE))
        has_numbered = bool(re.search(r'^\s*\d+\.\s+', enhanced_passage, re.MULTILINE))
        has_comparison = bool(re.search(r'\b(while|whereas|however|in contrast|on the other hand)\b', enhanced_passage, re.IGNORECASE))
        
        feature_count = sum([has_bullets, has_numbered, has_comparison])
        
        if feature_count == 0:
            validation["valid"] = False
            validation["errors"].append("No organizational feature found (one required: bullets, numbered list, or comparison)")
            validation["checks"]["has_organizational_feature"] = False
        elif feature_count > 1:
            validation["warnings"].append("Multiple organizational features found (one recommended)")
            validation["checks"]["has_organizational_feature"] = True
        else:
            validation["checks"]["has_organizational_feature"] = True
        
        # Check word count (should stay within reasonable range)
        enhanced_word_count = self._count_words(enhanced_passage)
        original_word_count = self._count_words(original_passage)
        word_increase = enhanced_word_count - original_word_count
        
        # Text features should add minimal words (headings + list formatting)
        # Allow up to 20% increase for features
        max_increase = int(original_word_count * 0.2)
        
        if word_increase > max_increase:
            validation["warnings"].append(
                f"Word count increased by {word_increase} words (original: {original_word_count}, "
                f"enhanced: {enhanced_word_count}). Text features should add minimal words."
            )
        else:
            validation["checks"]["word_count_reasonable"] = True
        
        # Check that original content is preserved
        # Simple check: original passage words should mostly appear in enhanced
        original_words = set(original_passage.lower().split())
        enhanced_words = set(enhanced_passage.lower().split())
        
        # Allow for some word changes (e.g., "first" -> "1."), but most should remain
        overlap = len(original_words & enhanced_words)
        overlap_ratio = overlap / len(original_words) if original_words else 0
        
        if overlap_ratio < 0.7:
            validation["warnings"].append(
                f"Only {overlap_ratio:.0%} of original words preserved. "
                "Enhanced passage may have changed core content."
            )
        else:
            validation["checks"]["content_preserved"] = True
        
        return validation
    
    def _extract_headings(self, text: str) -> list:
        """Extract headings from text (lines that are standalone, typically capitalized)."""
        headings = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Heading indicators:
            # 1. Standalone line (not part of paragraph)
            # 2. Often capitalized or title case
            # 3. Short (typically 2-8 words)
            # 4. Not ending with punctuation (except colon)
            # 5. Not starting with bullet/number
            
            is_standalone = (
                len(line.split()) <= 10 and  # Short
                not line.endswith('.') and  # Not a sentence
                not line.endswith('!') and
                not line.endswith('?') and
                not re.match(r'^[\s]*[•\-\*]\s+', line) and  # Not a list item
                not re.match(r'^\s*\d+\.\s+', line) and  # Not numbered list
                (line[0].isupper() if line else False)  # Starts with capital
            )
            
            if is_standalone:
                # Check if next line is content (not another heading)
                headings.append(line)
        
        return headings
    
    def _extract_features(self, text: str) -> Dict[str, Any]:
        """Extract text features from enhanced passage."""
        headings = self._extract_headings(text)
        
        has_bullets = bool(re.search(r'^[\s]*[•\-\*]\s+', text, re.MULTILINE))
        has_numbered = bool(re.search(r'^\s*\d+\.\s+', text, re.MULTILINE))
        has_comparison = bool(re.search(r'\b(while|whereas|however|in contrast|on the other hand)\b', text, re.IGNORECASE))
        
        feature_type = None
        if has_bullets:
            feature_type = "bulleted_list"
        elif has_numbered:
            feature_type = "numbered_list"
        elif has_comparison:
            feature_type = "comparison_text"
        
        return {
            "headings": headings,
            "heading_count": len(headings),
            "organizational_feature": feature_type,
            "has_bullets": has_bullets,
            "has_numbered": has_numbered,
            "has_comparison": has_comparison
        }
    
    def _count_words(self, text: str) -> int:
        """Count words in text."""
        return len(text.split())


def create_text_feature_injector(
    ai_client: AIClient,
    template_dir: Optional[str] = None
) -> TextFeatureInjector:
    """
    Factory function to create a Text Feature Injector.
    
    Args:
        ai_client: AI client for text generation
        template_dir: Optional custom template directory
        
    Returns:
        TextFeatureInjector instance
    """
    return TextFeatureInjector(ai_client, template_dir)
