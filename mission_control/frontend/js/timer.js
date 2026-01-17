/**
 * Timer Module
 * Manages assessment timer (counts up)
 */

let timerInterval = null;
let startTime = null;
let elapsedSeconds = 0;

function formatTime(seconds) {
    const mins = Math.floor(seconds / 60).toString().padStart(2, '0');
    const secs = (seconds % 60).toString().padStart(2, '0');
    return `${mins}:${secs}`;
}

function updateTimerDisplay() {
    const timerElement = document.getElementById('timer');
    if (timerElement) {
        timerElement.textContent = formatTime(elapsedSeconds);
    }
}

function startTimer() {
    if (timerInterval) {
        return; // Timer already running
    }
    
    startTime = Date.now() - (elapsedSeconds * 1000);
    timerInterval = setInterval(() => {
        elapsedSeconds = Math.floor((Date.now() - startTime) / 1000);
        updateTimerDisplay();
    }, 1000);
    
    updateTimerDisplay();
}

function stopTimer() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }
}

function resetTimer() {
    stopTimer();
    elapsedSeconds = 0;
    startTime = null;
    updateTimerDisplay();
}

function getElapsedSeconds() {
    return elapsedSeconds;
}
