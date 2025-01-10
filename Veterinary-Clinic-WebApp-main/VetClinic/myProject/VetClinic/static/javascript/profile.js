let initialValues = {};

// Store initial values when the page loads
window.onload = () => {
    const inputs = document.querySelectorAll('input[type="text"], input[type="email"], input[type="password"]');
    inputs.forEach(input => {
        initialValues[input.id] = input.value;
        if (input.id !== 'email') {
            input.setAttribute('readonly', true);  // Set inputs to readonly initially, except for the email field
        }
    });
};

function toggleEditMode() {
    const inputs = document.querySelectorAll('input[type="text"], input[type="password"]');  // Exclude email input
    const editButton = document.getElementById('edit-button');
    const isReadonly = inputs[0].hasAttribute('readonly');
    const form = document.querySelector('form');

    if (isReadonly) {
        // Enter edit mode: Remove readonly for all fields except email
        inputs.forEach(input => input.removeAttribute('readonly'));
        editButton.textContent = "Save";
    } else {
        // Exit edit mode: Check for changes
        const valid = notifyChange(); // Call your validation function
        if (valid) {
            // Check if any field was edited
            let hasChanges = false;
            inputs.forEach(input => {
                if (input.value !== initialValues[input.id]) {
                    hasChanges = true;
                }
            });

            if (hasChanges) {
                // Log success message
                console.log("Form has been successfully saved.");

                // Show confirmation dialog with only OK
                alert("Changes have been saved successfully.");

                // Submit the form after confirmation
                form.submit();
            }
        }

        // Switch back to readonly for all fields except email
        inputs.forEach(input => input.setAttribute('readonly', true));
        editButton.textContent = "Edit";
    }
}

function notifyChange() {
    // Add your validation logic here
    return true; // Assume always valid for simplicity
}

function checkEmailFormat(input) {
    const warning = document.getElementById('email-warning');
    const gmailPattern = /^[a-zA-Z0-9._%+-]+@gmail\.com$/;

    // Ensure email is valid and ends with @gmail.com
    if (input.value.indexOf('@') !== -1 && !input.value.endsWith('@gmail.com')) {
        warning.classList.remove('d-none');
        input.setCustomValidity("Invalid email format. Only @gmail.com is allowed.");
        input.value = input.value.substring(0, input.value.indexOf('@') + 1) + "gmail.com";  // Automatically fix domain
    } else {
        warning.classList.add('d-none');
        input.setCustomValidity("");  // Reset validation
    }
}

function validatePhone() {
    const phoneInput = document.getElementById('phone');

    // Ensure phone number starts with "09" and remove any non-numeric characters
    let phoneValue = phoneInput.value.replace(/[^0-9]/g, '');  // Remove letters and special characters

    // If phone number doesn't start with "09", adjust it
    if (!phoneValue.startsWith('09')) {
        phoneValue = '09' + phoneValue.slice(2);  // Ensure the first two digits are "09"
    }

    // Limit the phone number to a maximum of 11 digits
    if (phoneValue.length > 11) {
        phoneValue = phoneValue.slice(0, 11);  // Truncate to 11 digits
    }

    // Update the phone number input field with the cleaned value
    phoneInput.value = phoneValue;
}

function validateForm() {
    const phoneInput = document.getElementById('phone');

    // Check if the phone number has exactly 11 digits
    if (phoneInput.value.length !== 11) {
        alert("Phone number must be exactly 11 digits.");
        return false;  // Prevent form submission
    }

    return true;  // Allow form submission
}

function togglePasswordVisibility(inputId) {
    const passwordField = document.getElementById(inputId);
    const passwordFieldType = passwordField.type;

    // Toggle password visibility
    if (passwordFieldType === 'password') {
        passwordField.type = 'text';
    } else {
        passwordField.type = 'password';
    }   
}
