# Mission Control Quick Start Guide

## Prerequisites

1. **Python 3.7+** installed
2. **Assessment forms generated** in `samples/` directory
3. **Flask and flask-cors** installed

## Setup

### 1. Install Dependencies

```bash
cd mission_control
pip install -r requirements.txt
```

Or globally:
```bash
pip install Flask flask-cors
```

### 2. Generate Test Assessment Form

```bash
cd ..  # Go back to project root
python3 generate_simple_assessment.py --assessment-id LR-ALPH --grade K
```

This creates `samples/lr_alph_form1_k.json` which Mission Control will load.

### 3. Start Backend Server

```bash
cd mission_control/backend
python3 app.py
```

You should see:
```
MISSION CONTROL BACKEND API
======================================================================
✓ API Server: http://localhost:5002
...
```

### 4. Open Frontend

**Option A: Simple File Opening**
```bash
cd ../frontend
open assessor_view.html  # macOS
# OR
xdg-open assessor_view.html  # Linux
# OR
start assessor_view.html  # Windows
```

**Option B: Local Server (Recommended)**
```bash
cd ../frontend
python3 -m http.server 8080
```

Then open: http://localhost:8080/assessor_view.html

## Usage

1. **Assessment starts automatically** when page loads
2. **Timer begins counting up** automatically
3. **Use click cycle buttons** to mark responses:
   - ✓ Correct (default)
   - ✗ Incorrect
   - ↻ Self-Correct
   - — Omission
   - ⟲ Reset
4. **Navigate** with Previous/Next buttons
5. **Click "Stop & Score"** when complete
6. **View results** in modal dialog
7. **Results saved** to `mission_control/database/sessions/`

## Troubleshooting

### Backend won't start
- Check port 5002 is available: `lsof -i :5002`
- Kill existing process if needed

### Frontend can't connect to backend
- Ensure backend is running on port 5002
- Check browser console for CORS errors
- Verify API_BASE_URL in `js/api.js` matches backend

### No forms found
- Generate assessment form first (see Step 2)
- Check `samples/` directory contains `lr_alph_form*_*.json` files

### Items not displaying
- Check browser console for errors
- Verify form JSON structure is valid
- Ensure item has `letter`, `word`, or other display field

## Next Steps

- Customize assessment ID and form selection
- Add student information input
- Implement form selection UI
- Add session history and results viewing
