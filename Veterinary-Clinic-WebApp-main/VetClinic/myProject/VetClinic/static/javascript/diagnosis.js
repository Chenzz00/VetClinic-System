// Function to submit the diagnosis and save to localStorage
function submitDiagnosis() {
    // Get the scheduleId from the URL query string
    const scheduleId = new URLSearchParams(window.location.search).get('scheduleId');
    const reason = document.getElementById('reason').value;
    const diagnosis = document.getElementById('diagnosis').value;

    // Save the diagnosis and status in localStorage
    const scheduleData = {
        scheduleId: scheduleId,
        reason: reason,
        diagnosis: diagnosis,
        status: 'Completed'
    };

    // Store the data in localStorage (using the scheduleId as a key)
    localStorage.setItem('schedule_' + scheduleId, JSON.stringify(scheduleData));

    // Update the status of the schedule on the vet window
    updateScheduleStatus(scheduleId, 'Completed');

    // Show confirmation message
    alert('Diagnosis submitted successfully');

    // Redirect back to the vet window or any URL you want
    window.location.href = '{% url "vet" %}';  
}

// Function to update the status in vetwindow
function updateScheduleStatus(scheduleId, newStatus) {
    // Access the schedule data from localStorage
    const schedule = JSON.parse(localStorage.getItem('schedule_' + scheduleId));

    if (schedule) {
        schedule.status = newStatus;
        localStorage.setItem('schedule_' + scheduleId, JSON.stringify(schedule));

        // Find the status element and update it on the vetwindow page (assuming it has an ID like 'status-<scheduleId>')
        const statusElement = document.getElementById('status-' + scheduleId);
        if (statusElement) {
            statusElement.innerText = newStatus;
        }
    }
}
