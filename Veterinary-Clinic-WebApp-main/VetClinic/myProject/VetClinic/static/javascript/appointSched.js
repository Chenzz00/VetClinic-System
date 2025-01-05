// Load walk-in hours from localStorage when the page loads
function loadWalkInHours() {
    const savedWalkInHours = localStorage.getItem('walkInHours') || "Walk in Hours: 1PM-6PM";
    document.getElementById('walk-in-hours').value = savedWalkInHours; // Restore input field
    document.getElementById('display-walk-in-hours').textContent = savedWalkInHours; // Display restored hours
}

// Save walk-in hours to localStorage
function saveWalkInHours() {
    const walkInHours = document.getElementById('walk-in-hours').value.trim();
    localStorage.setItem('walkInHours', walkInHours); // Save to localStorage
}

// Function to update walk-in hours and save to localStorage
function updateWalkInHours() {
    const walkInHours = document.getElementById('walk-in-hours').value.trim();
    if (walkInHours) {
        document.getElementById('display-walk-in-hours').textContent = walkInHours; // Display updated hours
        saveWalkInHours(); // Save to localStorage
        alert('Walk-in hours updated successfully!');
    } else {
        alert('Please enter valid walk-in hours.');
    }
}
// Call the load function when the window loads
window.onload = loadWalkInHours;

function notifySpeciesAdded() {
    alert("New pet species added successfully!");
    return true; // Allow form submission
}

function notifyServiceAdded() {
    alert("New service added successfully!");
    return true; // Allow form submission
}




document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.paid-button');

    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const id = this.getAttribute('data-id');

            fetch(`/admin/`, {  
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}' 
                },
                body: JSON.stringify({ id: id }) 
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.message); 
                    const row = this.closest('tr');
                    row.querySelector('td:nth-child(6)').textContent = 'Completed';
                    row.querySelector('td:nth-child(7)').textContent = 'Paid';
                } else {
                    alert('Failed to update status: ' + data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});

function confirmPayment(scheduleId) {
    const confirmation = confirm("Are you sure you want to mark this appointment as paid?");
    if (confirmation) {
        // If confirmed, submit the form
        document.getElementById('form-' + scheduleId).submit();
    }
}