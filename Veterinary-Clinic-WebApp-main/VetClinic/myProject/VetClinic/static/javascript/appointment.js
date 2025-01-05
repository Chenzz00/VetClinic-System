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

function deleteSpecies() {
    const speciesSelect = document.getElementById("current-species");
    const speciesToDelete = speciesSelect.value;

    if (confirm(`Are you sure you want to delete the species: ${speciesToDelete}?`)) {
        fetch('', { // Use the current URL for your appointment schedule
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}' // Include CSRF token for security
            },
            body: JSON.stringify({ action: 'delete_species', species: speciesToDelete })
        })
        .then(response => {
            if (response.ok) {
                // Remove the species from the select element
                const optionToDelete = Array.from(speciesSelect.options).find(option => option.value === speciesToDelete);
                if (optionToDelete) {
                    speciesSelect.removeChild(optionToDelete);
                }
                alert("Species deleted successfully!");
            } else {
                alert("Failed to delete species.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred while deleting the species.");
        });
    }
}

function deleteService() {
    const servicesSelect = document.getElementById("current-services");
    const serviceToDelete = servicesSelect.value;

    if (confirm(`Are you sure you want to delete the service: ${serviceToDelete}?`)) {
        fetch('', { // Use the current URL for your appointment schedule
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}' // Include CSRF token for security
            },
            body: JSON.stringify({ action: 'delete_service', service: serviceToDelete })
        })
        .then(response => {
            if (response.ok) {
                // Remove the service from the select element
                const optionToDelete = Array.from(servicesSelect.options).find(option => option.value === serviceToDelete);
                if (optionToDelete) {
                    servicesSelect.removeChild(optionToDelete);
                }
                alert("Service deleted successfully!");
            } else {
                alert("Failed to delete service.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred while deleting the service.");
        });
    }
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
