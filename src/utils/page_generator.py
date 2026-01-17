"""
Page Generator Utility
Generates printable assessor and student pages from assessment JSON files.
"""

from pathlib import Path
from typing import Dict, Any, Optional
from jinja2 import Template
import json

# PDF generation support
try:
    from weasyprint import HTML
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    HTML = None


def load_assessment_json(filepath: Path) -> Optional[Dict[str, Any]]:
    """Load assessment JSON file"""
    if not filepath.exists():
        return None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_registry_info(assessment_id: str) -> Optional[Dict[str, Any]]:
    """Get assessment interface info from registry"""
    try:
        from src.assessments.registry import get_assessment
        assessment = get_assessment(assessment_id)
        if assessment and 'interface' in assessment:
            interface = assessment['interface']
            return {
                'assessor_script': interface.assessor_script,
                'student_prompt': interface.student_prompt,
                'assessor_interaction': interface.assessor_interaction.value,
                'timing_mode': interface.timing_mode.value,
                'student_presentation': interface.student_presentation.value,
                'click_cycle': interface.click_cycle.to_dict() if interface.click_cycle else None,
                'scoring': assessment.get('scoring', {})
            }
    except (ImportError, AttributeError) as e:
        print(f"Warning: Could not load registry info: {e}")
    
    return None


def prepare_assessor_page_data(assessment_data: Dict[str, Any], 
                                registry_info: Optional[Dict[str, Any]] = None,
                                assessment_id: Optional[str] = None) -> Dict[str, Any]:
    """Prepare data for assessor page template"""
    metadata = assessment_data.get('metadata', {})
    interface_spec = assessment_data.get('interface_spec', {})
    
    # Get assessor script (prefer registry, fallback to interface_spec, then empty)
    assessor_script = []
    if registry_info and registry_info.get('assessor_script'):
        assessor_script = registry_info['assessor_script']
    elif interface_spec.get('assessor_script'):
        assessor_script = interface_spec['assessor_script']
    
    # Get assessor interaction type
    assessor_interaction = 'correct_incorrect'  # default
    if registry_info and registry_info.get('assessor_interaction'):
        assessor_interaction = registry_info['assessor_interaction']
    elif interface_spec.get('assessor_interaction'):
        assessor_interaction = interface_spec['assessor_interaction']
    
    # Get click cycle states
    click_cycle_states = []
    if registry_info and registry_info.get('click_cycle'):
        click_cycle_states = registry_info['click_cycle'].get('states', [])
    elif interface_spec.get('click_cycle'):
        click_cycle_states = interface_spec['click_cycle'].get('states', [])
    
    # Get timing mode
    timing_mode = 'untimed'
    if registry_info and registry_info.get('timing_mode'):
        timing_mode = registry_info['timing_mode']
    elif interface_spec.get('timing_mode'):
        timing_mode = interface_spec['timing_mode']
    
    # Get scoring info
    scoring = assessment_data.get('scoring', {})
    if registry_info and registry_info.get('scoring'):
        scoring = registry_info['scoring']
    
    primary_metric = scoring.get('primary_metric', 'total_correct')
    secondary_metrics = scoring.get('secondary_metrics', [])
    error_types = scoring.get('error_types', [])
    
    # Prepare items - handle both "items" and "questions.questions" structures
    items = assessment_data.get('items', [])
    
    # If this is a comprehension assessment, convert questions to items format
    if not items and 'questions' in assessment_data:
        questions_data = assessment_data.get('questions', {})
        questions_list = questions_data.get('questions', [])
        if questions_list:
            items = questions_list  # Questions already have answer_options
    
    return {
        'assessment_id': assessment_id,
        'assessment_name': metadata.get('assessment_name', 'Assessment'),
        'grade': metadata.get('grade', 'N/A'),
        'form_number': metadata.get('form_number', 1),
        'assessor_script': assessor_script,
        'assessor_interaction': assessor_interaction,
        'click_cycle_states': click_cycle_states,
        'timing_mode': timing_mode,
        'items': items,
        'primary_metric': primary_metric,
        'secondary_metrics': secondary_metrics,
        'error_types': error_types
    }


def prepare_student_page_data(assessment_data: Dict[str, Any],
                              registry_info: Optional[Dict[str, Any]] = None,
                              assessment_id: Optional[str] = None) -> Dict[str, Any]:
    """Prepare data for student page template"""
    metadata = assessment_data.get('metadata', {})
    interface_spec = assessment_data.get('interface_spec', {})
    
    # Get student presentation mode
    student_presentation = 'one_at_a_time'  # default
    if registry_info and registry_info.get('student_presentation'):
        student_presentation = registry_info['student_presentation']
    elif interface_spec.get('student_presentation'):
        student_presentation = interface_spec['student_presentation']
    
    # Prepare items - handle both "items" and "questions.questions" structures
    items = assessment_data.get('items', [])
    
    # If this is a comprehension assessment, convert questions to items format
    if not items and 'questions' in assessment_data:
        questions_data = assessment_data.get('questions', {})
        questions_list = questions_data.get('questions', [])
        if questions_list:
            items = questions_list
    
    # Include passage for comprehension assessments
    passage = None
    if 'passage' in assessment_data:
        passage = assessment_data['passage']
    
    return {
        'assessment_id': assessment_id,
        'assessment_name': metadata.get('assessment_name', 'Assessment'),
        'grade': metadata.get('grade', 'N/A'),
        'form_number': metadata.get('form_number', 1),
        'student_presentation': student_presentation,
        'items': items,
        'passage': passage
    }


def render_page(template_path: Path, data: Dict[str, Any]) -> str:
    """Render a Jinja2 template with data"""
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    template = Template(template_content)
    return template.render(**data)


def generate_pages_for_assessment(assessment_file: Path, 
                                  templates_dir: Path,
                                  output_dir: Optional[Path] = None) -> Dict[str, str]:
    """
    Generate assessor and student pages for an assessment.
    
    Returns:
        Dict with 'assessor' and 'student' keys containing rendered HTML
    """
    # Load assessment data
    assessment_data = load_assessment_json(assessment_file)
    if not assessment_data:
        raise ValueError(f"Could not load assessment: {assessment_file}")
    
    # Get registry info
    assessment_id = assessment_data.get('assessment_id') or assessment_data.get('metadata', {}).get('assessment_id')
    registry_info = None
    if assessment_id:
        registry_info = get_registry_info(assessment_id)
    
    # Prepare template data
    assessor_data = prepare_assessor_page_data(assessment_data, registry_info, assessment_id)
    student_data = prepare_student_page_data(assessment_data, registry_info, assessment_id)
    
    # Add filename for navigation
    filename = assessment_file.stem
    assessor_data['filename'] = filename
    student_data['filename'] = filename
    
    # Load and render templates
    assessor_template = templates_dir / 'assessor_page.html'
    student_template = templates_dir / 'student_page.html'
    
    if not assessor_template.exists():
        raise FileNotFoundError(f"Assessor template not found: {assessor_template}")
    if not student_template.exists():
        raise FileNotFoundError(f"Student template not found: {student_template}")
    
    assessor_html = render_page(assessor_template, assessor_data)
    student_html = render_page(student_template, student_data)
    
    return {
        'assessor': assessor_html,
        'student': student_html
    }


def generate_pdf_from_html(html_content: str, output_path: Path) -> bool:
    """
    Generate a PDF file from HTML content using WeasyPrint.
    
    Args:
        html_content: HTML string to convert
        output_path: Path where PDF should be saved
        
    Returns:
        True if successful, False otherwise
    """
    if not PDF_AVAILABLE:
        raise ImportError("WeasyPrint is not installed. Install it with: pip install weasyprint")
    
    try:
        html_doc = HTML(string=html_content)
        html_doc.write_pdf(output_path)
        return True
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return False


def generate_pdfs_for_assessment(assessment_file: Path,
                                  templates_dir: Path,
                                  output_dir: Path) -> Dict[str, Path]:
    """
    Generate PDF files for assessor and student pages.
    
    Args:
        assessment_file: Path to assessment JSON file
        templates_dir: Directory containing HTML templates
        output_dir: Directory where PDFs should be saved
        
    Returns:
        Dict with 'assessor' and 'student' keys containing Path objects to generated PDFs
    """
    # Generate HTML first
    pages = generate_pages_for_assessment(assessment_file, templates_dir)
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate PDFs
    filename = assessment_file.stem
    assessor_pdf = output_dir / f"{filename}_assessor.pdf"
    student_pdf = output_dir / f"{filename}_student.pdf"
    
    generate_pdf_from_html(pages['assessor'], assessor_pdf)
    generate_pdf_from_html(pages['student'], student_pdf)
    
    return {
        'assessor': assessor_pdf,
        'student': student_pdf
    }
