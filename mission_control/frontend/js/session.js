/**
 * Session Management Module
 * Handles assessment session state
 */

let sessionId = null;
let currentItemIndex = 0;
let totalItems = 0;
let items = [];
let responses = {};

function setSession(id, total) {
    sessionId = id;
    totalItems = total;
    currentItemIndex = 0;
    responses = {};
    updateProgressDisplay();
}

function getSessionId() {
    return sessionId;
}

function getCurrentItemIndex() {
    return currentItemIndex;
}

function setCurrentItemIndex(index) {
    currentItemIndex = Math.max(0, Math.min(index, totalItems - 1));
    updateProgressDisplay();
    updateNavigationButtons();
}

function recordResponse(itemIndex, state) {
    responses[itemIndex] = {
        itemIndex: itemIndex,
        state: state,
        timestamp: new Date().toISOString()
    };
}

function getResponses() {
    return responses;
}

function getResponseCount() {
    return Object.keys(responses).length;
}

function updateProgressDisplay() {
    const currentEl = document.getElementById('current-item');
    const totalEl = document.getElementById('total-items');
    const progressFill = document.getElementById('progressFill');
    
    if (currentEl) currentEl.textContent = currentItemIndex + 1;
    if (totalEl) totalEl.textContent = totalItems;
    
    if (progressFill) {
        const progress = ((currentItemIndex + 1) / totalItems) * 100;
        progressFill.style.width = `${progress}%`;
    }
}

function updateNavigationButtons() {
    const prevBtn = document.getElementById('btn-prev');
    const nextBtn = document.getElementById('btn-next');
    
    if (prevBtn) {
        prevBtn.disabled = currentItemIndex === 0;
    }
    
    if (nextBtn) {
        nextBtn.disabled = currentItemIndex >= totalItems - 1;
    }
}
