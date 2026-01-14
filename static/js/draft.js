document.addEventListener('DOMContentLoaded', () => {
    console.log("Hextech Analytics Engine Initialized...");
    
    // Smooth transitions for section loading
    const sections = document.querySelectorAll('.hex-container');
    sections.forEach(s => s.style.opacity = '1');
});

// Placeholder for real-time draft updates
function updateDraftPrediction(currentPicks) {
    // This will be connected to your Flask API
    console.log("Calculating win probability for:", currentPicks);
}
