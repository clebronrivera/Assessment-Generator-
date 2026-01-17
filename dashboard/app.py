"""
Reading Compass Dashboard - Enhanced
Features: Assessment Matrix, Generation Controls, PDF Preview
"""

from flask import Flask, render_template, jsonify, request
import json
import os
import sys
from pathlib import Path
from datetime import datetime
import subprocess

app = Flask(__name__)

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
SAMPLES_DIR = PROJECT_ROOT / "samples"
sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.assessment_matrix import create_assessment_matrix

assessment_matrix = create_assessment_matrix()

def load_sample(sample_name):
    """Load a sample JSON file"""
    sample_path = SAMPLES_DIR / f"{sample_name}.json"
    if sample_path.exists():
        with open(sample_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def load_manifest(sample_name):
    """Load a sample manifest"""
    manifest_path = SAMPLES_DIR / f"{sample_name}_manifest.json"
    if manifest_path.exists():
        with open(manifest_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

@app.route('/')
def index():
    """Main dashboard - Warehouse view with inventory summary"""
    # Get matrix status
    matrix_status = assessment_matrix.get_status(SAMPLES_DIR)
    
    # Load actual sample files and calculate inventory
    samples = []
    orf_count = 0
    comp_narrative_count = 0
    comp_nonfiction_count = 0
    orf_by_grade = set()
    comp_narrative_by_grade = set()
    comp_nonfiction_by_grade = set()
    
    if SAMPLES_DIR.exists():
        for file in SAMPLES_DIR.glob("*.json"):
            if "_manifest" not in file.name:
                sample_name = file.stem
                manifest = load_manifest(sample_name)
                modified_time = datetime.fromtimestamp(file.stat().st_mtime)
                
                # Determine assessment type
                assessment_type = None
                genre = None
                grade = None
                assessment_id = None
                
                if manifest:
                    assessment_type = manifest.get('package_type', '').lower()
                    genre = manifest.get('genre', '').lower() if manifest.get('genre') else None
                    grade = manifest.get('grade')
                    # For simple assessments, normalize assessment_type to uppercase
                    assessment_id_raw = manifest.get('assessment_type')
                    if assessment_id_raw:
                        assessment_id = assessment_id_raw.upper().strip()  # Convert "lr-alph" -> "LR-ALPH"
                    else:
                        assessment_id = None
                else:
                    # Fallback: try to infer from filename
                    if 'orf' in sample_name.lower():
                        assessment_type = 'orf'
                    elif 'comp' in sample_name.lower() or 'comprehension' in sample_name.lower():
                        assessment_type = 'comprehension'
                        if 'narrative' in sample_name.lower():
                            genre = 'narrative'
                        elif 'nonfiction' in sample_name.lower():
                            genre = 'nonfiction'
                    else:
                        # Try to match simple assessment IDs (e.g., lr_alph, fl_wrf)
                        for ass_id in ['lr_alph', 'fl_wrf', 'fl_psf', 'pa_rhym', 'pa_oons', 
                                       'pa_phon', 'pa_syls', 'ph_csa', 'ph_lwid']:
                            if ass_id in sample_name.lower():
                                assessment_type = 'simple'
                                assessment_id = ass_id.replace('_', '-').upper()
                                break
                
                # Count by type
                if assessment_type == 'orf':
                    orf_count += 1
                    if grade:
                        orf_by_grade.add(grade)
                elif assessment_type == 'comprehension':
                    if genre == 'narrative':
                        comp_narrative_count += 1
                        if grade:
                            comp_narrative_by_grade.add(grade)
                    elif genre == 'nonfiction':
                        comp_nonfiction_count += 1
                        if grade:
                            comp_nonfiction_by_grade.add(grade)
                
                samples.append({
                    'name': sample_name,
                    'file': file.name,
                    'size_kb': file.stat().st_size / 1024,
                    'modified': modified_time.strftime('%Y-%m-%d %H:%M'),
                    'modified_datetime': modified_time,
                    'manifest': manifest,
                    'type': assessment_type,
                    'genre': genre,
                    'grade': grade,
                    'assessment_id': assessment_id
                })
    
    # Sort samples by modification date (most recent first)
    samples.sort(key=lambda x: x['modified_datetime'], reverse=True)
    
    # Build recent assessments list for activity log
    recent_assessments = []
    for sample in samples[:50]:  # Last 50 assessments
        manifest = sample['manifest']
        assessment_type = sample.get('type', 'unknown')
        genre = sample.get('genre')
        grade = sample.get('grade')
        
        # Create display name
        display_name = f"Grade {grade if grade else '?'} "
        if assessment_type == 'orf':
            display_name += "ORF Assessment"
        elif assessment_type == 'comprehension':
            display_name += f"Comprehension - {genre.title() if genre else 'Unknown'}"
        elif assessment_type == 'simple' and sample.get('assessment_id'):
            # Get name from registry if available
            try:
                from src.assessments.registry import get_assessment
                ass = get_assessment(sample['assessment_id'])
                if ass:
                    display_name += ass['name']
                else:
                    display_name += sample['assessment_id'].replace('-', ' ').title()
            except:
                display_name += sample['assessment_id'].replace('-', ' ').title() if sample.get('assessment_id') else sample['name'].replace('_', ' ').title()
        else:
            display_name += sample['name'].replace('_', ' ').title()
        
        recent_assessments.append({
            'filename': sample['name'],
            'display_name': display_name,
            'type': assessment_type,
            'genre': genre,
            'grade': grade,
            'assessment_id': sample.get('assessment_id'),
            'last_modified': sample['modified'],
            'manifest': manifest
        })
    
    # Count simple assessments
    simple_assessments = {}
    simple_by_type = {}
    for sample in samples:
        if sample.get('type') == 'simple' and sample.get('assessment_id'):
            ass_id = sample['assessment_id']
            simple_assessments[ass_id] = simple_assessments.get(ass_id, 0) + 1
            simple_by_type[ass_id] = simple_by_type.get(ass_id, set())
            if sample.get('grade'):
                simple_by_type[ass_id].add(sample['grade'])
    
    # Convert sets to sorted lists
    simple_by_type = {k: sorted(v) for k, v in simple_by_type.items()}
    total_simple = sum(simple_assessments.values())
    
    # Count by reading domain
    domain_counts = {
        'Fluency': 0,
        'Phonological Awareness': 0,
        'Alphabetic Principle': 0,
        'Phonics': 0,
        'Comprehension': 0
    }
    
    # Count ORF as Fluency
    domain_counts['Fluency'] += orf_count
    
    # Count comprehension as Comprehension
    domain_counts['Comprehension'] = comp_narrative_count + comp_nonfiction_count
    
    # Count simple assessments by domain
    try:
        from src.assessments.registry import get_assessment
        for ass_id, count in simple_assessments.items():
            ass = get_assessment(ass_id)
            if ass and 'domain' in ass:
                domain = ass['domain']
                if domain in domain_counts:
                    domain_counts[domain] += count
    except ImportError:
        pass
    
    # Build inventory summary
    inventory_summary = {
        'total_assessments': orf_count + comp_narrative_count + comp_nonfiction_count + total_simple,
        'total_orf': orf_count,
        'total_comprehension': comp_narrative_count + comp_nonfiction_count,
        'total_simple': total_simple,
        'orf_count': orf_count,
        'comp_narrative_count': comp_narrative_count,
        'comp_nonfiction_count': comp_nonfiction_count,
        'simple_assessments': simple_assessments,
        'orf_by_grade': sorted(orf_by_grade),
        'comp_narrative_by_grade': sorted(comp_narrative_by_grade),
        'comp_nonfiction_by_grade': sorted(comp_nonfiction_by_grade),
        'simple_by_type': simple_by_type,
        'domain_counts': domain_counts  # Add domain counts
    }
    
    return render_template('index.html', 
                         inventory_summary=inventory_summary,
                         recent_assessments=recent_assessments,
                         matrix_status=matrix_status)

@app.route('/matrix')
def matrix():
    """Assessment matrix view"""
    matrix_status = assessment_matrix.get_status(SAMPLES_DIR)
    
    # Load registry assessments for display
    try:
        from src.assessments.registry import ASSESSMENTS, get_assessment
        # Add registry assessment data to each assessment in matrix_status
        for assessment in matrix_status['assessments']:
            if assessment['spec'].assessment_id:
                reg_assessment = get_assessment(assessment['spec'].assessment_id)
                if reg_assessment:
                    assessment['registry_assessment'] = reg_assessment
    except ImportError:
        pass
    
    return render_template('matrix_enhanced.html', matrix_status=matrix_status)

@app.route('/api/matrix/status')
def matrix_status_api():
    """API endpoint for matrix status"""
    status = assessment_matrix.get_status(SAMPLES_DIR)
    
    # Convert specs to dicts for JSON serialization
    serialized = {
        'total': status['total'],
        'generated': status['generated'],
        'missing': status['missing'],
        'assessments': []
    }
    
    for a in status['assessments']:
        serialized['assessments'].append({
            'grade': a['spec'].grade,
            'assessment_type': a['spec'].assessment_type,
            'genre': a['spec'].genre,
            'display_name': a['spec'].display_name,
            'exists': a['exists'],
            'filename': a['filename'],
            'manifest': a['manifest']
        })
    
    return jsonify(serialized)

@app.route('/api/generate', methods=['POST'])
def generate_assessment():
    """API endpoint to generate a new assessment"""
    data = request.json
    grade = data.get('grade')
    assessment_type = data.get('assessment_type')
    genre = data.get('genre')
    assessment_id = data.get('assessment_id', '').strip() if data.get('assessment_id') else None  # For simple assessments
    
    print(f"🔍 Generate request: grade={grade}, type={assessment_type}, genre={genre}, assessment_id={assessment_id}")
    
    # Build command to run generator
    if assessment_type == 'orf':
        # Run ORF generator
        cmd = [
            sys.executable,
            str(PROJECT_ROOT / 'generate_orf_assessment.py'),
            '--grade', grade
        ]
    elif assessment_id and assessment_id.strip():
        # Run simple assessment generator (has assessment_id)
        # Convert to uppercase to match registry format
        assessment_id_upper = assessment_id.upper().strip()
        cmd = [
            sys.executable,
            str(PROJECT_ROOT / 'generate_simple_assessment.py'),
            '--assessment-id', assessment_id_upper,
            '--grade', grade
        ]
        # Add form number if specified
        if data.get('form_number'):
            cmd.extend(['--form-number', str(data.get('form_number'))])
    elif assessment_type == 'comprehension':
        # Run comprehension generator
        cmd = [
            sys.executable,
            str(PROJECT_ROOT / 'generate_comprehension_assessment.py'),
            '--grade', grade,
            '--genre', genre
        ]
    else:
        return jsonify({
            'success': False,
            'error': f'Invalid assessment type: {assessment_type}. For simple assessments, assessment_id must be provided.'
        }), 400
    
    print(f"🚀 Launching generation command: {' '.join(cmd)}")
    print(f"   Grade: {grade}, Type: {assessment_type}, ID: {assessment_id}")
    
    # Run in background (non-blocking)
    try:
        # Create logs directory if it doesn't exist
        logs_dir = PROJECT_ROOT / "logs"
        logs_dir.mkdir(exist_ok=True)
        
        # Create log file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = logs_dir / f"generation_{grade}_{assessment_type}_{timestamp}.log"
        
        with open(log_file, 'w') as f:
            # Use close_fds=True to detach properly
            process = subprocess.Popen(
                cmd,
                stdout=f,
                stderr=subprocess.STDOUT,
                cwd=str(PROJECT_ROOT),
                close_fds=True
            )
        
        print(f"✅ Launched process PID: {process.pid}, logging to: {log_file}")
        
        return jsonify({
            'success': True,
            'message': f'Generation started for Grade {grade} {assessment_type}. check logs at {log_file.name}',
            'pid': process.pid,
            'log_file': str(log_file)
        })
    except Exception as e:
        print(f"❌ Failed to launch process: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/delete/<sample_name>', methods=['DELETE'])
def delete_assessment(sample_name):
    """API endpoint to delete an assessment and its manifest"""
    assessment_file = SAMPLES_DIR / f"{sample_name}.json"
    manifest_file = SAMPLES_DIR / f"{sample_name}_manifest.json"
    
    deleted_files = []
    errors = []
    
    # Delete assessment file
    if assessment_file.exists():
        try:
            assessment_file.unlink()
            deleted_files.append(assessment_file.name)
        except Exception as e:
            errors.append(f"Error deleting {assessment_file.name}: {str(e)}")
    
    # Delete manifest file
    if manifest_file.exists():
        try:
            manifest_file.unlink()
            deleted_files.append(manifest_file.name)
        except Exception as e:
            errors.append(f"Error deleting {manifest_file.name}: {str(e)}")
    
    if errors:
        return jsonify({
            'success': False,
            'error': '; '.join(errors),
            'deleted': deleted_files
        }), 500
    
    if not deleted_files:
        return jsonify({
            'success': False,
            'error': 'No files found to delete'
        }), 404
    
    return jsonify({
        'success': True,
        'message': f'Successfully deleted {len(deleted_files)} file(s)',
        'deleted': deleted_files
    })

@app.route('/api/sample/<sample_name>')
def get_sample(sample_name):
    """API endpoint to get full sample data"""
    sample = load_sample(sample_name)
    if sample:
        return jsonify(sample)
    return jsonify({'error': 'Sample not found'}), 404

@app.route('/view/<sample_name>')
def view_sample(sample_name):
    """View a specific sample"""
    sample = load_sample(sample_name)
    manifest = load_manifest(sample_name)
    
    if not sample:
        return "Sample not found", 404
    
    return render_template('sample_viewer.html', 
                         sample_name=sample_name,
                         sample=sample,
                         manifest=manifest)

@app.route('/preview/<sample_name>')
def preview_pdf(sample_name):
    """Preview assessment as it would appear printed"""
    sample = load_sample(sample_name)
    manifest = load_manifest(sample_name)
    
    if not sample:
        return "Sample not found", 404
    
    # Check if this is an ORF assessment
    if sample.get('package_type') == 'orf' or (manifest and manifest.get('package_type') == 'orf'):
        return render_template('orf_pdf_preview.html',
                             sample_name=sample_name,
                             sample=sample,
                             manifest=manifest)
    
    # Default to comprehension PDF preview
    return render_template('pdf_preview.html',
                         sample_name=sample_name,
                         sample=sample,
                         manifest=manifest)

@app.route('/assessor/<sample_name>')
def assessor_page(sample_name):
    """View printable assessor page for an assessment"""
    from src.utils.page_generator import generate_pages_for_assessment
    
    assessment_file = SAMPLES_DIR / f"{sample_name}.json"
    templates_dir = PROJECT_ROOT / "templates"
    
    if not assessment_file.exists():
        return "Assessment not found", 404
    
    try:
        pages = generate_pages_for_assessment(assessment_file, templates_dir)
        return pages['assessor']
    except Exception as e:
        return f"Error generating assessor page: {str(e)}", 500

@app.route('/student/<sample_name>')
def student_page(sample_name):
    """View printable student page for an assessment"""
    from src.utils.page_generator import generate_pages_for_assessment
    
    assessment_file = SAMPLES_DIR / f"{sample_name}.json"
    templates_dir = PROJECT_ROOT / "templates"
    
    if not assessment_file.exists():
        return "Assessment not found", 404
    
    try:
        pages = generate_pages_for_assessment(assessment_file, templates_dir)
        return pages['student']
    except Exception as e:
        return f"Error generating student page: {str(e)}", 500

@app.route('/pdf/assessor/<sample_name>')
def assessor_pdf(sample_name):
    """Generate and download assessor PDF"""
    from src.utils.page_generator import generate_pages_for_assessment, generate_pdf_from_html
    from flask import send_file
    
    assessment_file = SAMPLES_DIR / f"{sample_name}.json"
    templates_dir = PROJECT_ROOT / "templates"
    
    if not assessment_file.exists():
        return "Assessment not found", 404
    
    try:
        pages = generate_pages_for_assessment(assessment_file, templates_dir)
        
        # Create temporary PDF file
        import tempfile
        import os
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            pdf_path = tmp.name
        
        if generate_pdf_from_html(pages['assessor'], Path(pdf_path)):
            return send_file(pdf_path, as_attachment=True, 
                           download_name=f"{sample_name}_assessor.pdf",
                           mimetype='application/pdf')
        else:
            return "Error generating PDF", 500
    except ImportError as e:
        return f"PDF generation not available: {str(e)}. Install weasyprint: pip install weasyprint", 500
    except Exception as e:
        return f"Error generating PDF: {str(e)}", 500
    finally:
        # Clean up temp file after sending
        if 'pdf_path' in locals() and os.path.exists(pdf_path):
            try:
                os.unlink(pdf_path)
            except:
                pass

@app.route('/pdf/student/<sample_name>')
def student_pdf(sample_name):
    """Generate and download student PDF"""
    from src.utils.page_generator import generate_pages_for_assessment, generate_pdf_from_html
    from flask import send_file
    
    assessment_file = SAMPLES_DIR / f"{sample_name}.json"
    templates_dir = PROJECT_ROOT / "templates"
    
    if not assessment_file.exists():
        return "Assessment not found", 404
    
    try:
        pages = generate_pages_for_assessment(assessment_file, templates_dir)
        
        # Create temporary PDF file
        import tempfile
        import os
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            pdf_path = tmp.name
        
        if generate_pdf_from_html(pages['student'], Path(pdf_path)):
            return send_file(pdf_path, as_attachment=True,
                           download_name=f"{sample_name}_student.pdf",
                           mimetype='application/pdf')
        else:
            return "Error generating PDF", 500
    except ImportError as e:
        return f"PDF generation not available: {str(e)}. Install weasyprint: pip install weasyprint", 500
    except Exception as e:
        return f"Error generating PDF: {str(e)}", 500
    finally:
        # Clean up temp file after sending
        if 'pdf_path' in locals() and os.path.exists(pdf_path):
            try:
                os.unlink(pdf_path)
            except:
                pass

if __name__ == '__main__':
    print("\n" + "="*80)
    print("📊 READING COMPASS DASHBOARD - ENHANCED")
    print("="*80)
    print(f"\n✓ Project root: {PROJECT_ROOT}")
    print(f"✓ Samples directory: {SAMPLES_DIR}")
    
    # Show matrix status
    status = assessment_matrix.get_status(SAMPLES_DIR)
    print(f"\n📈 Assessment Status:")
    print(f"  • Generated: {status['generated']}/{status['total']}")
    print(f"  • Missing: {status['missing']}")
    
    print(f"\n🌐 Dashboard: http://localhost:5001")
    print("📊 Matrix View: http://localhost:5001/matrix")
    print("\n💡 New Features:")
    print("  • Assessment Matrix - See what's generated and missing")
    print("  • Generate Button - Create new assessments from UI")
    print("  • PDF Preview - See printable versions")
    print("\n  Press Ctrl+C to stop\n")
    
    app.run(debug=True, port=5001)
