"""
Mission Control Backend
Minimal viable assessment delivery system
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from datetime import datetime
import json
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# In-memory session storage (MVP only - will migrate to database)
sessions = {}

# Load assessment forms
SAMPLES_DIR = PROJECT_ROOT / "samples"


def load_form(assessment_id: str, form_id: str):
    """Load assessment form from samples directory"""
    # Form files are named: {assessment_id}_form{number}_{grade}.json
    # e.g., lr_alph_form1_k.json
    pattern = f"{assessment_id.lower()}_form*_*.json"
    form_files = list(SAMPLES_DIR.glob(pattern))
    
    if not form_files:
        return None
    
    # If form_id is provided, try to match it
    if form_id:
        for form_file in form_files:
            if form_id.lower() in form_file.stem.lower():
                with open(form_file, 'r') as f:
                    return json.load(f)
    
    # Otherwise, use first available form
    with open(form_files[0], 'r') as f:
        return json.load(f)


def calculate_elapsed_time(session):
    """Calculate elapsed time from timer start to stop"""
    if not session.get('timer_started'):
        return None
    
    timer_stopped = session.get('timer_stopped') or datetime.now().isoformat()
    
    start = datetime.fromisoformat(session['timer_started'])
    stop = datetime.fromisoformat(timer_stopped)
    
    elapsed = (stop - start).total_seconds()
    return elapsed


def save_results(results: dict):
    """Save assessment results to file"""
    results_dir = PROJECT_ROOT / "mission_control" / "database" / "sessions"
    results_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{results['session_id']}_{timestamp}.json"
    filepath = results_dir / filename
    
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)
    
    return str(filepath)


@app.route('/')
def index():
    """API index"""
    return jsonify({
        'name': 'Mission Control API',
        'version': '1.0.0',
        'endpoints': [
            'POST /assessment/start',
            'GET /assessment/<session_id>/item/<index>',
            'POST /assessment/<session_id>/record',
            'POST /assessment/<session_id>/timer/start',
            'POST /assessment/<session_id>/timer/stop',
            'POST /assessment/<session_id>/complete'
        ]
    })


@app.route('/assessment/start', methods=['POST'])
def start_assessment():
    """Initialize assessment session"""
    data = request.json
    assessment_id = data.get('assessment_id', 'LR-ALPH')
    grade = data.get('grade', 'K')
    student_id = data.get('student_id', 'test_student')
    form_id = data.get('form_id', None)
    
    # Load form
    form = load_form(assessment_id, form_id)
    if not form:
        return jsonify({'error': 'Form not found'}), 404
    
    # Create session
    session_id = f"session_{datetime.now().timestamp()}"
    
    sessions[session_id] = {
        'assessment_id': assessment_id,
        'grade': grade,
        'student_id': student_id,
        'form_id': form.get('form_id', form_id),
        'form_data': form,
        'started_at': datetime.now().isoformat(),
        'current_item': 0,
        'responses': {},
        'timer_started': None,
        'timer_stopped': None
    }
    
    return jsonify({
        'session_id': session_id,
        'total_items': len(form.get('items', [])),
        'form_id': form.get('form_id')
    })


@app.route('/assessment/<session_id>/item/<int:item_index>', methods=['GET'])
def get_item(session_id, item_index):
    """Get current assessment item"""
    if session_id not in sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    session = sessions[session_id]
    items = session['form_data'].get('items', [])
    
    if item_index < 0 or item_index >= len(items):
        return jsonify({'error': 'Item index out of range'}), 404
    
    item = items[item_index]
    
    # Extract display text based on item type
    display_text = None
    if 'letter' in item:
        display_text = item['letter']
    elif 'word' in item:
        display_text = item['word']
    elif 'word1' in item:
        display_text = f"{item['word1']} - {item['word2']}"
    elif 'onset' in item:
        display_text = f"{item['onset']} ... {item['rime']}"
    elif 'content' in item:
        display_text = item['content']
    
    return jsonify({
        'item_index': item_index,
        'item': item,
        'display_text': display_text,
        'total_items': len(items),
        'current_response': session['responses'].get(item_index, None)
    })


@app.route('/assessment/<session_id>/record', methods=['POST'])
def record_response(session_id):
    """Record student response"""
    if session_id not in sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    data = request.json
    item_index = data.get('item_index')
    response_state = data.get('response_state', 'correct')
    
    sessions[session_id]['responses'][item_index] = {
        'item_index': item_index,
        'response_state': response_state,
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify({'success': True})


@app.route('/assessment/<session_id>/timer/start', methods=['POST'])
def start_timer(session_id):
    """Start assessment timer"""
    if session_id not in sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    sessions[session_id]['timer_started'] = datetime.now().isoformat()
    return jsonify({'success': True, 'started_at': sessions[session_id]['timer_started']})


@app.route('/assessment/<session_id>/timer/stop', methods=['POST'])
def stop_timer(session_id):
    """Stop assessment timer"""
    if session_id not in sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    sessions[session_id]['timer_stopped'] = datetime.now().isoformat()
    return jsonify({'success': True, 'stopped_at': sessions[session_id]['timer_stopped']})


@app.route('/assessment/<session_id>/complete', methods=['POST'])
def complete_assessment(session_id):
    """Finalize and score assessment"""
    if session_id not in sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    session = sessions[session_id]
    responses = session['responses']
    
    # Calculate scores
    total_items = len(session['form_data'].get('items', []))
    answered_items = len(responses)
    correct_items = sum(1 for r in responses.values() if r.get('response_state') == 'correct')
    
    # Calculate accuracy
    accuracy = correct_items / answered_items if answered_items > 0 else 0
    
    # Calculate time elapsed
    time_elapsed = calculate_elapsed_time(session)
    
    results = {
        'session_id': session_id,
        'assessment_id': session['assessment_id'],
        'form_id': session['form_id'],
        'student_id': session['student_id'],
        'started_at': session['started_at'],
        'completed_at': datetime.now().isoformat(),
        'total_items': total_items,
        'answered_items': answered_items,
        'correct_items': correct_items,
        'accuracy': round(accuracy, 3),
        'accuracy_percent': round(accuracy * 100, 1),
        'time_elapsed_seconds': round(time_elapsed, 2) if time_elapsed else None,
        'responses': list(responses.values())
    }
    
    # Save to file
    filepath = save_results(results)
    results['saved_to'] = filepath
    
    return jsonify(results)


@app.route('/assessment/<session_id>/status', methods=['GET'])
def get_status(session_id):
    """Get current session status"""
    if session_id not in sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    session = sessions[session_id]
    return jsonify({
        'session_id': session_id,
        'current_item': session['current_item'],
        'total_items': len(session['form_data'].get('items', [])),
        'responses_recorded': len(session['responses']),
        'timer_started': session['timer_started'],
        'timer_stopped': session['timer_stopped']
    })


if __name__ == '__main__':
    print("\n" + "="*70)
    print("MISSION CONTROL BACKEND API")
    print("="*70)
    print(f"\n✓ API Server: http://localhost:5002")
    print(f"✓ Samples Directory: {SAMPLES_DIR}")
    print(f"\nAvailable Endpoints:")
    print(f"  POST /assessment/start")
    print(f"  GET  /assessment/<session_id>/item/<index>")
    print(f"  POST /assessment/<session_id>/record")
    print(f"  POST /assessment/<session_id>/timer/start")
    print(f"  POST /assessment/<session_id>/timer/stop")
    print(f"  POST /assessment/<session_id>/complete")
    print(f"\nPress Ctrl+C to stop\n")
    
    app.run(port=5002, debug=True)
