"""
Simple Assessment Generator Base Class

Base class for non-AI assessment generators that use structured data.
These generators are quick and don't require AI for content generation.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import json
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.assessments.registry import get_assessment, ASSESSMENTS
from src.generators.base_generator import BaseGenerator


class SimpleAssessmentGenerator(BaseGenerator):
    """
    Base class for simple assessment generators.
    These use structured data (word banks, letter lists) instead of AI.
    """
    
    def __init__(self, assessment_id: str, banks_module=None):
        """
        Initialize the simple generator.
        
        Args:
            assessment_id: Assessment ID from registry (e.g., "LR-ALPH")
            banks_module: Optional banks module (for compatibility with BaseGenerator)
        """
        # Don't call super().__init__ since we don't need templates
        self.assessment_id = assessment_id
        self.assessment_spec = get_assessment(assessment_id)
        
        if not self.assessment_spec:
            raise ValueError(f"Assessment {assessment_id} not found in registry")
        
        self.banks = banks_module  # May not be needed for simple generators
    
    def get_form_id(self, grade: str, form_number: int) -> str:
        """
        Generate form ID for this assessment.
        Format: {ASSESSMENT_ID}-FORM-{NUMBER:03d}
        
        Args:
            grade: Grade level
            form_number: Form number (1, 2, 3, etc.)
            
        Returns:
            Form ID string
        """
        return f"{self.assessment_id}-FORM-{form_number:03d}"
    
    def get_next_form_number(self, grade: str, samples_dir: Path) -> int:
        """
        Find the next available form number for this assessment and grade.
        
        Args:
            grade: Grade level
            samples_dir: Directory where samples are stored
            
        Returns:
            Next form number
        """
        if not samples_dir.exists():
            return 1
        
        # Pattern: {assessment_id}_form{number}_{grade}.json
        pattern = f"{self.assessment_id.lower()}_form*_{grade}.json"
        existing_files = list(samples_dir.glob(pattern))
        
        if not existing_files:
            return 1
        
        # Extract form numbers
        form_numbers = []
        for file in existing_files:
            # Extract number from filename like "lr_alph_form1_k.json"
            parts = file.stem.split('_')
            for part in parts:
                if part.startswith('form'):
                    try:
                        num = int(part[4:])  # Skip "form" prefix
                        form_numbers.append(num)
                    except ValueError:
                        continue
        
        if not form_numbers:
            return 1
        
        return max(form_numbers) + 1
    
    def create_metadata(self, grade: str, form_number: int, **kwargs) -> Dict[str, Any]:
        """
        Create metadata dictionary for the assessment form.
        
        Args:
            grade: Grade level
            form_number: Form number
            **kwargs: Additional metadata fields
            
        Returns:
            Metadata dictionary
        """
        form_id = self.get_form_id(grade, form_number)
        
        metadata = {
            "assessment_id": self.assessment_id,
            "form_id": form_id,
            "form_number": form_number,
            "grade": grade,
            "assessment_name": self.assessment_spec["name"],
            "category": self.assessment_spec["category"],
            "created_at": datetime.now().isoformat(),
            "schema_version": "2026.1",
            **kwargs
        }
        
        return metadata
    
    def create_manifest(self, grade: str, form_number: int, total_items: int, **kwargs) -> Dict[str, Any]:
        """
        Create manifest for the assessment form.
        
        Args:
            grade: Grade level
            form_number: Form number
            total_items: Total number of items in the form
            **kwargs: Additional manifest fields
            
        Returns:
            Manifest dictionary
        """
        form_id = self.get_form_id(grade, form_number)
        
        manifest = {
            "package_id": form_id,
            "assessment_type": self.assessment_id.lower(),
            "created_at": datetime.now().isoformat(),
            "grade": grade,
            "form_number": form_number,
            "schema_version": "2026.1",
            "statistics": {
                "total_items": total_items,
                **kwargs.get("statistics", {})
            },
            "ready_for_use": True,
            **{k: v for k, v in kwargs.items() if k != "statistics"}
        }
        
        return manifest
    
    @abstractmethod
    def generate_items(self, grade: str, form_number: int, **kwargs) -> list:
        """
        Generate the assessment items.
        Must be implemented by subclasses.
        
        Args:
            grade: Grade level
            form_number: Form number
            **kwargs: Additional generation parameters
            
        Returns:
            List of assessment items
        """
        pass
    
    def generate(self, grade: str, form_number: Optional[int] = None, 
                 samples_dir: Optional[Path] = None, **kwargs) -> Dict[str, Any]:
        """
        Generate complete assessment form.
        
        Args:
            grade: Grade level
            form_number: Form number (auto-increments if not provided)
            samples_dir: Directory to save samples (optional)
            **kwargs: Additional generation parameters
            
        Returns:
            Complete assessment form dictionary
        """
        # Get or determine form number
        if form_number is None:
            if samples_dir:
                form_number = self.get_next_form_number(grade, samples_dir)
            else:
                form_number = 1
        
        # Generate items
        items = self.generate_items(grade, form_number, **kwargs)
        
        # Create output structure
        output = {
            "metadata": self.create_metadata(grade, form_number, total_items=len(items)),
            "assessment_id": self.assessment_id,
            "form_id": self.get_form_id(grade, form_number),
            "form_number": form_number,
            "grade": grade,
            "items": items,
            "interface_spec": self.assessment_spec["interface"].to_dict(),
            "scoring": self.assessment_spec["scoring"]
        }
        
        # Save if samples_dir provided
        if samples_dir:
            samples_dir.mkdir(parents=True, exist_ok=True)
            filename = f"{self.assessment_id.lower()}_form{form_number}_{grade}.json"
            manifest_filename = f"{self.assessment_id.lower()}_form{form_number}_{grade}_manifest.json"
            
            filepath = samples_dir / filename
            manifest_path = samples_dir / manifest_filename
            
            # Save main file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2)
            
            # Save manifest
            manifest = self.create_manifest(grade, form_number, len(items))
            with open(manifest_path, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, indent=2)
        
        return output
    
    def validate(self, output: Dict[str, Any]) -> bool:
        """
        Validate generated output.
        
        Args:
            output: Generated content to validate
            
        Returns:
            True if valid, False otherwise
        """
        # Check required fields
        required_fields = ["assessment_id", "form_id", "grade", "items", "interface_spec"]
        for field in required_fields:
            if field not in output:
                return False
        
        # Check item count matches expected
        expected_count = self.assessment_spec["content"]["total_items"]
        if len(output["items"]) != expected_count:
            return False
        
        return True
