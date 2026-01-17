"""
Assessment Matrix - Tracks all possible assessment combinations
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from pathlib import Path
import json
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from src.assessments.registry import ASSESSMENTS, get_assessment
except ImportError:
    ASSESSMENTS = {}
    get_assessment = lambda x: None


@dataclass
class AssessmentSpec:
    """Specification for an assessment"""
    grade: str
    assessment_type: str  # 'orf', 'comprehension', or simple assessment IDs like 'LR-ALPH'
    genre: str = None  # Only for comprehension
    assessment_id: str = None  # For simple assessments (LR-ALPH, FL-WRF, etc.)
    form_number: int = None  # For form-based assessments
    
    @property
    def domain(self):
        """Get reading domain for this assessment"""
        if self.assessment_type == 'orf':
            return 'Fluency'
        elif self.assessment_type == 'comprehension':
            return 'Comprehension'
        elif self.assessment_id:
            assessment = get_assessment(self.assessment_id)
            if assessment and 'domain' in assessment:
                return assessment['domain']
        return 'Unknown'
    
    @property
    def area(self):
        """Get area - genre for comprehension, domain for others"""
        if self.assessment_type == 'comprehension' and self.genre:
            return self.genre.title()  # narrative or nonfiction
        return self.domain
    
    @property
    def sub_domain(self):
        """Get sub-domain for this assessment - this is where the 'Area' being tested goes"""
        if self.assessment_type == 'orf':
            return 'Oral Reading Fluency'
        elif self.assessment_type == 'comprehension':
            return 'Reading Comprehension'
        elif self.assessment_id:
            assessment = get_assessment(self.assessment_id)
            if assessment:
                # For morphonemic, subdomain should be "Morphemes" not "Phonics"
                if self.assessment_id == 'PH-MPHY':
                    return 'Morphemes'
                # Use category or name as sub-domain (this is the "Area")
                if 'category' in assessment:
                    return assessment['category']
                elif 'name' in assessment:
                    return assessment['name']
        return 'Unknown'
    
    @property
    def grade_equivalent(self):
        """Get grade equivalent (full grade name)"""
        grade_map = {
            'K': 'Kindergarten',
            '1': 'First Grade',
            '2': 'Second Grade',
            '3': 'Third Grade',
            '4': 'Fourth Grade',
            '5': 'Fifth Grade',
            '6': 'Sixth Grade',
            '7': 'Seventh Grade',
            '8': 'Eighth Grade'
        }
        return grade_map.get(self.grade, f'Grade {self.grade}')
    
    @property
    def display_name(self):
        if self.assessment_type == 'orf':
            return f"Grade {self.grade} ORF"
        elif self.assessment_type == 'comprehension':
            return f"Grade {self.grade} Comprehension - {self.genre.title()}"
        elif self.assessment_id:
            # Simple assessment
            assessment = get_assessment(self.assessment_id)
            if assessment:
                name = assessment['name']
                if self.form_number:
                    return f"Grade {self.grade} {name} (Form {self.form_number})"
                return f"Grade {self.grade} {name}"
            return f"Grade {self.grade} {self.assessment_id}"
        return f"Grade {self.grade} {self.assessment_type}"
    
    @property
    def expected_filename(self):
        if self.assessment_type == 'orf':
            return f"sample_orf_grade{self.grade}"
        elif self.assessment_type == 'comprehension':
            return f"sample_comp_grade{self.grade}_{self.genre}"
        elif self.assessment_id and self.form_number:
            # Simple assessment with form number
            return f"{self.assessment_id.lower()}_form{self.form_number}_{self.grade}"
        elif self.assessment_id:
            # Simple assessment without form number (check all forms)
            return f"{self.assessment_id.lower()}_form*_{self.grade}"
        return f"sample_{self.assessment_type}_grade{self.grade}"


class AssessmentMatrix:
    """Matrix of all possible assessments"""
    
    def __init__(self):
        self.specs = self._generate_all_specs()
    
    def _generate_all_specs(self) -> List[AssessmentSpec]:
        """Generate all possible assessment combinations"""
        specs = []
        
        # ORF assessments for grades K-8 (Fluency domain)
        for grade in ['K', '1', '2', '3', '4', '5', '6', '7', '8']:
            specs.append(AssessmentSpec(
                grade=grade,
                assessment_type='orf'
            ))
        
        # Comprehension assessments for grades 1-5 (Comprehension domain)
        # Each grade has narrative and nonfiction
        # Note: Grade 6 removed - only grades 1-5 are included
        for grade in ['1', '2', '3', '4', '5']:
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
        
        # Simple assessments from registry
        for assessment_id, assessment_data in ASSESSMENTS.items():
            content = assessment_data.get('content', {})
            grade_levels = []
            
            # Determine grade levels based on assessment
            grade_range = assessment_data.get('grade_range', '')
            if 'K' in grade_range or 'PreK' in grade_range:
                grade_levels.append('K')
            if '1' in grade_range:
                grade_levels.append('1')
            if '2' in grade_range:
                grade_levels.append('2')
            if '3' in grade_range:
                grade_levels.append('3')
            
            # Default to K if no grades specified
            if not grade_levels:
                grade_levels = ['K']
            
            # Check if grade-band specific (like PH-LWID, PH-PSWD)
            if 'grade_bands' in content:
                # These are handled differently - one spec per grade band
                for grade_band in content['grade_bands']:
                    # Map grade bands to actual grades
                    # Handle different formats: 'K', 'Kindergarten', 'G1', 'Grade 1', 'G2_3', 'Grade 2-3'
                    if grade_band == 'K' or grade_band == 'Kindergarten' or 'PreK' in str(grade_band):
                        grade_levels = ['K']
                    elif grade_band == 'G1' or grade_band == 'Grade 1' or 'Grade 1' in str(grade_band):
                        grade_levels = ['1']
                    elif grade_band == 'G2_3' or grade_band == 'Grade 2-3' or 'Grade 2-3' in str(grade_band) or '2-3' in str(grade_band):
                        grade_levels = ['2', '3']
                    elif grade_band == '1':
                        grade_levels = ['1']
                    elif grade_band == '2':
                        grade_levels = ['2']
                    elif grade_band == '3':
                        grade_levels = ['3']
                    
                    for grade in grade_levels:
                        specs.append(AssessmentSpec(
                            grade=grade,
                            assessment_type='simple',
                            assessment_id=assessment_id
                        ))
            else:
                # One spec per grade
                for grade in grade_levels:
                    specs.append(AssessmentSpec(
                        grade=grade,
                        assessment_type='simple',
                        assessment_id=assessment_id
                    ))
        
        return specs
    
    # Class-level constant for working generators
    _WORKING_GENERATORS = {
        'LR-ALPH',  # Letter Recognition
        'FL-WRF',   # Word Reading Fluency
        'FL-PSF',   # Phoneme Segmentation Fluency
        'PA-RHYM',  # Rhyme Recognition
        'PA-OONS',  # Onset-Rime Blending
        'PA-PHON',  # Phoneme Segmentation
        'PA-SYLS',  # Syllable Segmentation
        'PH-CSA',   # Consonant Sound Accuracy
        'PH-LWID',  # Letter-Word Identification
        'PH-CVC',   # CVC Blending
        # RC-* assessments intentionally omitted - no generators yet
    }
    
    def _has_working_generator(self, assessment_id: str) -> bool:
        """
        Check if a generator exists for this assessment ID.
        
        Args:
            assessment_id: Assessment ID (e.g., "LR-ALPH", "RC-LIST")
        
        Returns:
            True if generator exists, False otherwise
        """
        if not assessment_id:
            return False
        return assessment_id in self._WORKING_GENERATORS
    
    def _check_forms_exist(self, assessment_id: str, grade: str, samples_dir: Path) -> bool:
        """
        Check if any form files exist for this assessment and grade.
        
        Args:
            assessment_id: Assessment ID (e.g., "LR-ALPH")
            grade: Grade level (e.g., "K", "1")
            samples_dir: Samples directory path
        
        Returns:
            True if forms exist, False otherwise
        """
        if not samples_dir.exists() or not assessment_id:
            return False
        
        # Use existing pattern matching logic (keeps dashes from .lower())
        # Pattern: lr-alph_form*_K.json (matches lr-alph_form1_K.json)
        pattern = f"{assessment_id.lower()}_form*_{grade}.json"
        form_files = list(samples_dir.glob(pattern))
        
        # Filter out manifest files
        form_files = [f for f in form_files if '_manifest' not in f.name]
        
        return len(form_files) > 0
    
    def _should_show_assessment(self, spec: AssessmentSpec, samples_dir: Path) -> bool:
        """
        Determine if assessment should appear in matrix.
        
        Rule: Only show assessments that have files (generated assessments).
        Do not show missing assessments, even if they can be generated.
        
        Args:
            spec: Assessment specification
            samples_dir: Samples directory path
        
        Returns:
            True if files exist, False otherwise
        """
        
        # Check if files exist
        if spec.assessment_type == 'simple' and spec.assessment_id:
            if self._check_forms_exist(spec.assessment_id, spec.grade, samples_dir):
                return True  # Has files, show it
        elif spec.assessment_type in ['orf', 'comprehension']:
            json_file = samples_dir / f"{spec.expected_filename}.json"
            if json_file.exists():
                return True  # Has files, show it
        
        # No files exist - hide it
        return False
    
    def get_status(self, samples_dir: Path) -> Dict:
        """Get status of all assessments"""
        status = {
            'total': 0,
            'generated': 0,
            'missing': 0,
            'assessments': []
        }
        
        # Track vocabulary assessments per grade to keep only one
        vocabulary_by_grade = {}
        # Track pseudo word assessments to keep only K-1 and 2-3
        pseudo_word_bands = set()
        
        for spec in self.specs:
            # NEW: Filter using the new method - must come FIRST
            if not self._should_show_assessment(spec, samples_dir):
                continue  # Skip assessments that shouldn't be shown
            
            # EXISTING: Filter: Remove comprehension assessments that don't exist
            # (This is now redundant but keeping for safety/clarity)
            if spec.assessment_type == 'comprehension':
                json_file = samples_dir / f"{spec.expected_filename}.json"
                if not json_file.exists():
                    continue  # Skip non-generated comprehension
            
            # Filter: For vocabulary (VO-*), keep only one per grade
            if spec.assessment_id and spec.assessment_id.startswith('VO-'):
                if spec.grade in vocabulary_by_grade:
                    # Keep the first one we encounter for this grade
                    continue
                vocabulary_by_grade[spec.grade] = spec.assessment_id
            
            # Filter: For pseudo word (PH-PSWD), keep only K-1 and 2-3
            if spec.assessment_id == 'PH-PSWD':
                # Map grades to bands: K and 1 -> K-1, 2 and 3 -> 2-3
                if spec.grade in ['K', '1']:
                    band = 'K-1'
                elif spec.grade in ['2', '3']:
                    band = '2-3'
                else:
                    continue  # Skip other grades
                
                if band in pseudo_word_bands:
                    continue  # Already have one for this band
                pseudo_word_bands.add(band)
            
            # For simple assessments, check for any forms
            if spec.assessment_type == 'simple' and spec.assessment_id:
                # Find all forms for this assessment and grade
                pattern = f"{spec.assessment_id.lower()}_form*_{spec.grade}.json"
                form_files = list(samples_dir.glob(pattern)) if samples_dir.exists() else []
                exists = len(form_files) > 0
                
                # Get all forms
                forms = []
                for form_file in form_files:
                    # Extract form number
                    form_num = None
                    parts = form_file.stem.split('_')
                    for part in parts:
                        if part.startswith('form'):
                            try:
                                form_num = int(part[4:])
                            except ValueError:
                                pass
                    
                    manifest_file = samples_dir / f"{form_file.stem}_manifest.json"
                    manifest = None
                    if manifest_file.exists():
                        with open(manifest_file, 'r') as f:
                            manifest = json.load(f)
                    
                    forms.append({
                        'form_number': form_num,
                        'filename': form_file.stem,
                        'file_path': str(form_file),
                        'manifest': manifest
                    })
                
                if exists:
                    status['generated'] += 1
                
                # Use the first form's filename for viewing (or expected_filename if no forms)
                view_filename = forms[0]['filename'] if forms else spec.expected_filename
                
                status['assessments'].append({
                    'spec': spec,
                    'exists': exists,
                    'filename': view_filename,  # Use actual filename instead of pattern
                    'forms': forms,
                    'form_count': len(forms),
                    'manifest': forms[0]['manifest'] if forms else None,
                    'file_path': forms[0]['file_path'] if forms else None
                })
            else:
                # Original logic for ORF and Comprehension
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
                    'file_path': str(json_file) if exists else None,
                    'forms': [],
                    'form_count': 1
                })
        
        # Update total count after filtering
        status['total'] = len(status['assessments'])
        status['missing'] = status['total'] - status['generated']
        
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
