"""
Picture Description Generator (K-1 Specific)
Uses Bank 4 (Comprehension Blueprint) for K-1 requirements
Generates illustrator-ready picture descriptions for listening comprehension passages
"""

from typing import Dict, Any, Optional
from datetime import datetime

from ..banks import get_blueprint
from ..utils.template_loader import TemplateLoader
from ..utils.ai_client import AIClient


class PictureDescriptionGenerator:
    """Generates picture descriptions for K-1 listening comprehension passages."""
    
    def __init__(self, ai_client: AIClient, template_dir: Optional[str] = None):
        self.ai_client = ai_client
        self.template_loader = TemplateLoader(template_dir)
        self.max_attempts = 3
    
    def generate(
        self,
        passage_text: str,
        grade: str,
        max_attempts: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate a picture description for a K-1 passage.
        
        Args:
            passage_text: The passage text to create a picture for
            grade: Grade level ("K" or "1")
            max_attempts: Maximum retry attempts (default: 3)
            
        Returns:
            Dictionary with picture description and metadata
        """
        if grade not in ["K", "1"]:
            raise ValueError(f"Picture Description Generator only supports grades K and 1, got: {grade}")
        
        if max_attempts is None:
            max_attempts = self.max_attempts
        
        # Get K-1 requirements from Bank 4
        blueprint = get_blueprint(grade)
        specs = self._get_specs_from_banks(grade, blueprint, passage_text)
        
        # Render template
        prompt = self.template_loader.render("picture_description.j2", **specs)
        
        # Generate picture description
        attempts = 0
        picture_description = None
        last_error = None
        
        while attempts < max_attempts:
            try:
                picture_description = self.ai_client.complete(prompt)
                
                # Validate
                validation_results = self._validate_description(picture_description, specs)
                
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
        
        if picture_description is None:
            raise RuntimeError(f"Failed to generate picture description after {max_attempts} attempts. Last error: {last_error}")
        
        # Final validation
        validation_results = self._validate_description(picture_description, specs)
        
        # Build result
        result = {
            "success": validation_results["valid"],
            "picture_description": picture_description,
            "metadata": {
                "grade": grade,
                "passage_length": len(passage_text),
                "passage_word_count": self._count_words(passage_text),
                "timestamp": datetime.now().isoformat(),
                "schema_version": "2026.1",
                "generator": "PictureDescriptionGenerator",
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
        blueprint,
        passage_text: str
    ) -> Dict[str, Any]:
        """Get specifications from banks."""
        specs = {
            'grade': grade,
            'passage_text': passage_text,
            'text_access_mode': blueprint.text_access_mode.value,
            'supports_allowed': blueprint.supports_allowed,
            'bank_usage': {
                'Bank 4 (Comprehension Blueprint)': f"Grade {grade} - {blueprint.text_access_mode.value} mode, supports: {blueprint.supports_allowed}"
            }
        }
        
        return specs
    
    def _validate_description(self, description: str, specs: Dict[str, Any]) -> Dict[str, Any]:
        """Validate generated picture description."""
        validation = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "checks": {}
        }
        
        if not description or len(description.strip()) < 50:
            validation["valid"] = False
            validation["errors"].append("Description is empty or too short (minimum 50 characters)")
            validation["checks"]["has_content"] = False
            return validation
        
        validation["checks"]["has_content"] = True
        
        # Check for key elements mentioned in template
        description_lower = description.lower()
        
        # Should mention characters
        if not any(word in description_lower for word in ["character", "child", "children", "boy", "girl", "person", "people"]):
            validation["warnings"].append("Description may not clearly identify main character(s)")
        else:
            validation["checks"]["has_characters"] = True
        
        # Should mention setting
        if not any(word in description_lower for word in ["setting", "place", "location", "background", "scene", "park", "home", "school", "room"]):
            validation["warnings"].append("Description may not clearly identify setting")
        else:
            validation["checks"]["has_setting"] = True
        
        # Should be single scene (check for time indicators that suggest multiple scenes)
        time_indicators = ["then", "next", "after", "later", "first", "second", "finally", "before", "during", "while"]
        if any(indicator in description_lower for indicator in time_indicators):
            validation["warnings"].append("Description may contain multiple scenes or time progression")
        else:
            validation["checks"]["single_scene"] = True
        
        # Check length (should be 4-6 sentences as per template)
        sentence_count = description.count('.') + description.count('!') + description.count('?')
        if sentence_count < 3:
            validation["warnings"].append(f"Description has only {sentence_count} sentences (recommended: 4-6)")
        elif sentence_count > 8:
            validation["warnings"].append(f"Description has {sentence_count} sentences (recommended: 4-6)")
        else:
            validation["checks"]["appropriate_length"] = True
        
        return validation
    
    def _count_words(self, text: str) -> int:
        """Count words in text."""
        return len(text.split())


def create_picture_description_generator(
    ai_client: AIClient,
    template_dir: Optional[str] = None
) -> PictureDescriptionGenerator:
    """
    Factory function to create a Picture Description Generator.
    
    Args:
        ai_client: AI client for text generation
        template_dir: Optional custom template directory
        
    Returns:
        PictureDescriptionGenerator instance
    """
    return PictureDescriptionGenerator(ai_client, template_dir)
