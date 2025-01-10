// Load walk-in hours from localStorage when the page loads
function loadWalkInHours() {
    const savedWalkInHours = localStorage.getItem('walkInHours') || "Available walk-in hours: 1PM-6PM";
    document.getElementById('walk-in-hours').value = savedWalkInHours; // Restore input field
    document.getElementById('display-walk-in-hours').textContent = savedWalkInHours; // Display restored hours
}

// Ensure "Available walk-in hours: " is at the start of the input
function ensurePrefix() {
    var walkInHours = document.getElementById('walk-in-hours');
    
    // If the input starts with "Available walk-in hours: ", keep it as is
    if (!walkInHours.value.startsWith("Available walk-in hours: ")) {
        walkInHours.value = "Available walk-in hours: " + walkInHours.value.replace(/^Available walk-in hours: /, '');
    }
}

// Prevent user from erasing the fixed "Available walk-in hours: " part
function preventErasePrefix(event) {
    var walkInHours = document.getElementById('walk-in-hours');
    
    // Prevent backspace or delete if the cursor is within or before the static text "Available walk-in hours: "
    if (walkInHours.selectionStart <= 25 && (event.key === 'Backspace' || event.key === 'Delete')) {
        event.preventDefault();
    }
}

// Restrict input to only A, M, P letters, numbers, and dash ('-')
function allowOnlyAMP(event) {
    const allowedKeys = ['A', 'M', 'P', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-'];
    const key = event.key;
    
    // Allow the key if it is in the allowedKeys array
    if (allowedKeys.indexOf(key) === -1) {
        event.preventDefault();  // Prevent any other characters from being entered
    }
}

// Function to update walk-in hours and save to localStorage
function updateWalkInHours() {
    const walkInHours = document.getElementById('walk-in-hours').value.trim();
    
    if (walkInHours && walkInHours.startsWith("Available walk-in hours: ")) {
        document.getElementById('display-walk-in-hours').textContent = walkInHours; // Display updated hours
        saveWalkInHours(); // Save to localStorage
        alert('Walk-in hours updated successfully!');
    } else {
        alert('Please enter valid walk-in hours.');
    }
}

// Save walk-in hours to localStorage
function saveWalkInHours() {
    const walkInHours = document.getElementById('walk-in-hours').value.trim();
    localStorage.setItem('walkInHours', walkInHours); // Save to localStorage
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



