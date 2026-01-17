/**
 * Click Cycle Module
 * Manages response state cycling
 */

let currentState = 'correct';

const STATE_CYCLE = ['correct', 'incorrect', 'self_correct', 'omission', 'omission', 'reset'];

function getNextState(current) {
    const currentIndex = STATE_CYCLE.indexOf(current);
    if (currentIndex === -1) {
        return 'correct';
    }
    const nextIndex = (currentIndex + 1) % STATE_CYCLE.length;
    return STATE_CYCLE[nextIndex];
}

function setState(state) {
    currentState = state;
    updateStateButtons();
}

function getCurrentState() {
    return currentState;
}

function resetState() {
    currentState = 'correct';
    updateStateButtons();
}

function updateStateButtons() {
    // Remove active class from all buttons
    document.querySelectorAll('.state-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Add active class to current state button
    const activeBtn = document.querySelector(`[data-state="${currentState}"]`);
    if (activeBtn) {
        activeBtn.classList.add('active');
    }
}

// Initialize state button click handlers
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.state-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const state = this.dataset.state;
            setState(state);
        });
    });
    
    // Initialize to 'correct'
    resetState();
});
