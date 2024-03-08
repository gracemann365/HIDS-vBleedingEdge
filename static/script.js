// Get current hour
const currentHour = new Date().getHours();

// Select the element to update
const intruderStatusElement = document.getElementById('intruder-status');

// Check if the current hour is between 9 PM and 6 AM
if (currentHour >= 21 || currentHour < 6) {
    intruderStatusElement.textContent += 'Intruder';
} else {
    intruderStatusElement.textContent += 'Not Intruder';
}
