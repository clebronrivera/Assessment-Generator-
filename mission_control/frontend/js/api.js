/**
 * API Communication Module
 * Handles all API calls to Mission Control backend
 */

const API_BASE_URL = 'http://localhost:5002';

async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json'
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || 'API request failed');
        }
        
        return result;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Session Management
async function startAssessment(assessmentId, grade, studentId, formId = null) {
    return apiCall('/assessment/start', 'POST', {
        assessment_id: assessmentId,
        grade: grade,
        student_id: studentId,
        form_id: formId
    });
}

async function getItem(sessionId, itemIndex) {
    return apiCall(`/assessment/${sessionId}/item/${itemIndex}`);
}

async function recordResponse(sessionId, itemIndex, responseState) {
    return apiCall(`/assessment/${sessionId}/record`, 'POST', {
        item_index: itemIndex,
        response_state: responseState
    });
}

async function startTimer(sessionId) {
    return apiCall(`/assessment/${sessionId}/timer/start`, 'POST');
}

async function stopTimer(sessionId) {
    return apiCall(`/assessment/${sessionId}/timer/stop`, 'POST');
}

async function completeAssessment(sessionId) {
    return apiCall(`/assessment/${sessionId}/complete`, 'POST');
}

async function getStatus(sessionId) {
    return apiCall(`/assessment/${sessionId}/status`);
}
