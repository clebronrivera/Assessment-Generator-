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
    """Main dashboard with assessment matrix"""
    # Get matrix status
    matrix_status = assessment_matrix.get_status(SAMPLES_DIR)
    
    # Load actual sample files for cards
    samples = []
    if SAMPLES_DIR.exists():
        for file in SAMPLES_DIR.glob("*.json"):
            if "_manifest" not in file.name:
                sample_name = file.stem
                manifest = load_manifest(sample_name)
                
                samples.append({
                    'name': sample_name,
                    'file': file.name,
                    'size_kb': file.stat().st_size / 1024,
                    'modified': datetime.fromtimestamp(file.stat().st_mtime).strftime('%Y-%m-%d %H:%M'),
                    'manifest': manifest
                })
    
    return render_template('index.html', 
                         samples=samples,
                         matrix_status=matrix_status)

@app.route('/matrix')
def matrix():
    """Assessment matrix view"""
    matrix_status = assessment_matrix.get_status(SAMPLES_DIR)
    return render_template('matrix.html', matrix_status=matrix_status)

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
    
    # Build command to run generator
    if assessment_type == 'orf':
        # Run ORF generator
        cmd = [
            sys.executable,
            str(PROJECT_ROOT / 'generate_orf_assessment.py'),
            '--grade', grade
        ]
    else:
        # Run comprehension generator
        cmd = [
            sys.executable,
            str(PROJECT_ROOT / 'generate_comprehension_assessment.py'),
            '--grade', grade,
            '--genre', genre
        ]
    
    print(f"🚀 Launching generation command: {' '.join(cmd)}")
    
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
    
    return render_template('pdf_preview.html',
                         sample_name=sample_name,
                         sample=sample,
                         manifest=manifest)

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
