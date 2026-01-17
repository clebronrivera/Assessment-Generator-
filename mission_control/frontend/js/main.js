/**
 * Main Application Logic
 * Coordinates all modules
 */

let currentItemData = null;

// Initialize application
document.addEventListener('DOMContentLoaded', async () => {
    console.log('Mission Control initialized');
    
    try {
        // Start assessment session
        const sessionData = await startAssessment('LR-ALPH', 'K', 'test_student');
        setSession(sessionData.session_id, sessionData.total_items);
        
        // Start timer
        await startTimer(sessionData.session_id);
        startTimer();
        
        // Load first item
        await loadItem(0);
        
        console.log('Session started:', sessionData.session_id);
    } catch (error) {
        console.error('Failed to start assessment:', error);
        alert('Failed to start assessment: ' + error.message);
    }
});

async function loadItem(itemIndex) {
    if (!sessionId) {
        console.error('No session ID');
        return;
    }
    
    try {
        const itemData = await getItem(sessionId, itemIndex);
        currentItemData = itemData;
        
        // Update display
        const stimulusEl = document.getElementById('stimulus');
        if (stimulusEl) {
            if (itemData.display_text) {
                stimulusEl.innerHTML = `<div>${itemData.display_text}</div>`;
            } else {
                stimulusEl.innerHTML = '<div class="instruction">Item not available</div>';
            }
        }
        
        // Update current item index
        setCurrentItemIndex(itemIndex);
        
        // Check if there's a previous response
        if (itemData.current_response) {
            setState(itemData.current_response.response_state);
        } else {
            resetState();
        }
        
    } catch (error) {
        console.error('Failed to load item:', error);
        alert('Failed to load item: ' + error.message);
    }
}

async function prevItem() {
    if (currentItemIndex > 0) {
        // Save current response before moving
        await saveCurrentResponse();
        
        // Move to previous item
        await loadItem(currentItemIndex - 1);
    }
}

async function nextItem() {
    if (currentItemIndex < totalItems - 1) {
        // Save current response before moving
        await saveCurrentResponse();
        
        // Move to next item
        await loadItem(currentItemIndex + 1);
    }
}

async function saveCurrentResponse() {
    if (!sessionId || !currentItemData) {
        return;
    }
    
    const currentState = getCurrentState();
    
    try {
        await recordResponse(sessionId, currentItemIndex, currentState);
        recordResponse(currentItemIndex, currentState);
        
        // Reset to correct for next item
        resetState();
    } catch (error) {
        console.error('Failed to save response:', error);
    }
}

async function stopAssessment() {
    if (!confirm('Are you sure you want to stop and score the assessment?')) {
        return;
    }
    
    // Save current response
    await saveCurrentResponse();
    
    // Stop timer
    stopTimer();
    await stopTimer(sessionId);
    
    // Complete assessment
    try {
        const results = await completeAssessment(sessionId);
        showResults(results);
    } catch (error) {
        console.error('Failed to complete assessment:', error);
        alert('Failed to complete assessment: ' + error.message);
    }
}

function showResults(results) {
    const modal = document.getElementById('resultsModal');
    const content = document.getElementById('resultsContent');
    
    if (!modal || !content) {
        return;
    }
    
    content.innerHTML = `
        <p><strong>Assessment:</strong> ${results.assessment_id}</p>
        <p><strong>Form ID:</strong> ${results.form_id}</p>
        <p><strong>Total Items:</strong> ${results.total_items}</p>
        <p><strong>Answered:</strong> ${results.answered_items}</p>
        <p><strong>Correct:</strong> ${results.correct_items}</p>
        <p><strong>Accuracy:</strong> ${results.accuracy_percent}%</p>
        <p><strong>Time:</strong> ${formatTime(results.time_elapsed_seconds || 0)}</p>
        ${results.saved_to ? `<p><strong>Saved to:</strong> ${results.saved_to}</p>` : ''}
    `;
    
    modal.style.display = 'block';
}

function closeResults() {
    const modal = document.getElementById('resultsModal');
    if (modal) {
        modal.style.display = 'none';
    }
    
    // Reload page to start over
    location.reload();
}

// Make functions available globally
window.prevItem = prevItem;
window.nextItem = nextItem;
window.stopAssessment = stopAssessment;
window.closeResults = closeResults;
