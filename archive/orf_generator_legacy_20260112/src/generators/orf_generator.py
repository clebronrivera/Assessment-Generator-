"""
ORF (Oral Reading Fluency) Passage Generator
Uses Bank 1 (Lexile), Bank 2 (ORF Word Counts), Bank 7 (Text Structures)
"""

from typing import Dict, Any, Optional
from datetime import datetime

from ..banks import (
    get_lexile_range,
    get_midpoint_lexile,
    get_orf_target,
)
from ..utils.template_loader import TemplateLoader
from ..utils.ai_client import AIClient


class ORFGenerator:
    """Generates ORF passages using templates and banks."""
    
    def __init__(self, ai_client: AIClient, template_dir: Optional[str] = None):
        self.ai_client = ai_client
        self.template_loader = TemplateLoader(template_dir)
        self.max_attempts = 3
    
    def generate(
        self,
        grade: str,
        band: str = "early",
        topic_constraint: Optional[str] = None,
        prohibited_content: Optional[str] = None,
        structure: str = "chronological"
    ) -> Dict[str, Any]:
        """Generate an ORF passage."""
        # Get specs from banks
        specs = self._get_specs_from_banks(
            grade, band, topic_constraint, prohibited_content, structure
        )
        
        # Render template
        prompt = self.template_loader.render("orf_passage.j2", **specs)
        
        # Generate passage
        passage_text = self.ai_client.generate(prompt)
        
        # Validate
        validation_results = self._validate_passage(passage_text, specs)
        
        # Build result
        result = {
            "success": validation_results["valid"],
            "passage_text": passage_text,
            "metadata": {
                "grade": grade,
                "band": band,
                "lexile_range": f"{specs['lexile_min']} to {specs['lexile_max']}",
                "lexile_midpoint": specs['lexile_midpoint'],
                "target_word_count": specs['target_word_count'],
                "actual_word_count": self._count_words(passage_text),
                "structure": structure,
                "topic_constraint": topic_constraint,
                "prohibited_content": prohibited_content,
                "timestamp": datetime.now().isoformat(),
                "schema_version": "2026.1",
                "generator": "ORFGenerator"
            },
            "bank_usage": specs['bank_usage'],
            "validation": validation_results,
            "prompt_used": prompt
        }
        
        return result
    
    def _get_specs_from_banks(
        self,
        grade: str,
        band: str,
        topic_constraint: Optional[str],
        prohibited_content: Optional[str],
        structure: str
    ) -> Dict[str, Any]:
        """Get specifications from banks."""
        lexile_range = get_lexile_range(grade, band)
        lexile_midpoint = get_midpoint_lexile(grade, band)
        orf_target = get_orf_target(grade)
        
        specs = {
            'grade': grade,
            'lexile_min': lexile_range.lexile_min,
            'lexile_max': lexile_range.lexile_max,
            'lexile_midpoint': lexile_midpoint,
            'target_word_count': orf_target.target_word_count,
            'min_word_count': orf_target.min_word_count,
            'max_word_count': orf_target.max_word_count,
            'structure': structure,
            'topic_constraint': topic_constraint or "",
            'prohibited_content': prohibited_content or "",
            'bank_usage': {
                'Bank 1 (Lexile)': f"{lexile_range.lexile_min}-{lexile_range.lexile_max} (midpoint: {lexile_midpoint})",
                'Bank 2 (ORF Word Counts)': f"Target: {orf_target.target_word_count} words (±2)",
                'Bank 7 (Text Structure)': structure
            }
        }
        
        return specs
    
    def _validate_passage(self, passage_text: str, specs: Dict[str, Any]) -> Dict[str, Any]:
        """Validate generated passage."""
        validation = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "checks": {}
        }
        
        if not passage_text or len(passage_text.strip()) < 50:
            validation["valid"] = False
            validation["errors"].append("Passage is empty or too short")
            validation["checks"]["has_content"] = False
            return validation
        
        validation["checks"]["has_content"] = True
        
        word_count = self._count_words(passage_text)
        target = specs['target_word_count']
        min_allowed = specs['min_word_count']
        max_allowed = specs['max_word_count']
        
        if word_count < min_allowed:
            validation["valid"] = False
            validation["errors"].append(
                f"Word count too low: {word_count} words (minimum: {min_allowed})"
            )
            validation["checks"]["word_count_valid"] = False
        elif word_count > max_allowed:
            validation["valid"] = False
            validation["errors"].append(
                f"Word count too high: {word_count} words (maximum: {max_allowed})"
            )
            validation["checks"]["word_count_valid"] = False
        else:
            validation["checks"]["word_count_valid"] = True
            validation["warnings"].append(
                f"Word count: {word_count} (target: {target}, tolerance: ±2) ✓"
            )
        
        paragraph_count = passage_text.count('\n\n') + 1
        if paragraph_count < 2:
            validation["warnings"].append(
                "Passage has fewer than 2 paragraphs - may need paragraph breaks"
            )
            validation["checks"]["has_paragraphs"] = False
        else:
            validation["checks"]["has_paragraphs"] = True
        
        has_artifacts = any(x in passage_text for x in ['**', '##', '```', '<', '>'])
        if has_artifacts:
            validation["warnings"].append("Passage may contain formatting artifacts")
            validation["checks"]["clean_text"] = False
        else:
            validation["checks"]["clean_text"] = True
        
        return validation
    
    def _count_words(self, text: str) -> int:
        """Count words in text."""
        return len(text.split())
    
    def generate_with_retry(
        self,
        grade: str,
        band: str = "early",
        max_attempts: int = 3,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate with retry on validation failure."""
        attempts = 0
        last_result = None
        
        while attempts < max_attempts:
            attempts += 1
            
            try:
                result = self.generate(grade=grade, band=band, **kwargs)
                result['attempts'] = attempts
                
                if result['success']:
                    return result
                
                last_result = result
                print(f"Attempt {attempts}/{max_attempts} failed validation:")
                for error in result['validation']['errors']:
                    print(f"  - {error}")
                
            except Exception as e:
                print(f"Attempt {attempts}/{max_attempts} failed with error: {str(e)}")
                last_result = {
                    "success": False,
                    "passage_text": "",
                    "metadata": {"grade": grade, "band": band},
                    "validation": {"valid": False, "errors": [str(e)]},
                    "attempts": attempts
                }
        
        if last_result:
            last_result['note'] = f"Max attempts ({max_attempts}) reached - returning last attempt"
            return last_result
        
        return {
            "success": False,
            "passage_text": "",
            "metadata": {"grade": grade, "band": band},
            "validation": {"valid": False, "errors": ["Unknown error in generation"]},
            "attempts": max_attempts,
            "note": "Generation failed"
        }


def create_orf_generator(ai_client: AIClient, template_dir: Optional[str] = None) -> ORFGenerator:
    """Create an ORF generator instance."""
    return ORFGenerator(ai_client, template_dir)
