"""
Assessment Matrix - Tracks all possible assessment combinations
"""

from dataclasses import dataclass
from typing import List, Dict
from pathlib import Path
import json


@dataclass
class AssessmentSpec:
    """Specification for an assessment"""
    grade: str
    assessment_type: str  # 'orf' or 'comprehension'
    genre: str = None  # Only for comprehension
    
    @property
    def display_name(self):
        if self.assessment_type == 'orf':
            return f"Grade {self.grade} ORF"
        else:
            return f"Grade {self.grade} Comprehension - {self.genre.title()}"
    
    @property
    def expected_filename(self):
        if self.assessment_type == 'orf':
            return f"sample_orf_grade{self.grade}"
        else:
            return f"sample_comp_grade{self.grade}_{self.genre}"


class AssessmentMatrix:
    """Matrix of all possible assessments"""
    
    def __init__(self):
        self.specs = self._generate_all_specs()
    
    def _generate_all_specs(self) -> List[AssessmentSpec]:
        """Generate all possible assessment combinations"""
        specs = []
        
        # ORF assessments for grades K-8
        for grade in ['K', '1', '2', '3', '4', '5', '6', '7', '8']:
            specs.append(AssessmentSpec(
                grade=grade,
                assessment_type='orf'
            ))
        
        # Comprehension assessments for grades 1-6
        # Each grade has narrative and nonfiction
        for grade in ['1', '2', '3', '4', '5', '6']:
            specs.append(AssessmentSpec(
                grade=grade,
                assessment_type='comprehension',
                genre='narrative'
            ))
            specs.append(AssessmentSpec(
                grade=grade,
                assessment_type='comprehension',
                genre='nonfiction'
            ))
        
        return specs
    
    def get_status(self, samples_dir: Path) -> Dict:
        """Get status of all assessments"""
        status = {
            'total': len(self.specs),
            'generated': 0,
            'missing': 0,
            'assessments': []
        }
        
        for spec in self.specs:
            # Check if file exists
            json_file = samples_dir / f"{spec.expected_filename}.json"
            exists = json_file.exists()
            
            if exists:
                status['generated'] += 1
                # Load manifest if available
                manifest_file = samples_dir / f"{spec.expected_filename}_manifest.json"
                manifest = None
                if manifest_file.exists():
                    with open(manifest_file, 'r') as f:
                        manifest = json.load(f)
            else:
                status['missing'] += 1
                manifest = None
            
            status['assessments'].append({
                'spec': spec,
                'exists': exists,
                'filename': spec.expected_filename,
                'manifest': manifest,
                'file_path': str(json_file) if exists else None
            })
        
        return status
    
    def get_missing_assessments(self, samples_dir: Path) -> List[AssessmentSpec]:
        """Get list of missing assessments"""
        status = self.get_status(samples_dir)
        return [a['spec'] for a in status['assessments'] if not a['exists']]
    
    def get_generated_assessments(self, samples_dir: Path) -> List[Dict]:
        """Get list of generated assessments with metadata"""
        status = self.get_status(samples_dir)
        return [a for a in status['assessments'] if a['exists']]


def create_assessment_matrix():
    """Factory function"""
    return AssessmentMatrix()
