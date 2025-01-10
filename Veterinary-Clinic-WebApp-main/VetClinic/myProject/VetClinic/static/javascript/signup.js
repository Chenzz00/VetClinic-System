function validateForm(event) {
    event.preventDefault();  

    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm_password").value;
    const phone = document.getElementById("phone").value;
    const emailInput = document.getElementById("email");

    // Check if passwords match
    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return false; 
    }

    // Phone number length validation
    if (phone.length !== 11) {
        alert("Phone number must be exactly 11 digits!");
        return false; 
    }

    
    
    // If all validations pass, submit the form
    document.getElementById("registration-form").submit();
}

// Numbers Only
function enforceDigitsOnly(evt) {
    const inputField = evt.target;
    inputField.value = inputField.value.replace(/\D/g, ''); 
}



// Check email format and show warning
function checkEmailFormat(emailInput) {
    const emailWarning = document.getElementById("email-warning");
    const emailPattern = /^[a-zA-Z0-9._%+-]+@gmail\.com$/;

    if (!emailPattern.test(emailInput.value)) {
        emailWarning.style.display = "inline";  // Show the warning
        return false;
    } else {
        emailWarning.style.display = "none";   // Hide the warning
        return true;
    }
}

// Refactored code for email input
function enforceEmailInput(event) {
    let input = event.target;
    // Remove spaces if typed in the input field
    input.value = input.value.replace(/\s/g, '');

    // Check if '@' is typed and append the domain automatically
    if (input.value.indexOf('@') !== -1 && !input.value.includes('@gmail.com')) {
        if (input.value.indexOf('@') === input.value.length - 1) {
            input.value += "gmail.com";
        }
    }

    // Only allow valid characters for the email input
    const validKeys = /^[a-zA-Z0-9@._-]$/;
    if (!validKeys.test(event.key)) {
        event.preventDefault();
    }
}

document.getElementById('email').addEventListener('input', enforceEmailInput);
document.getElementById('email').addEventListener('keydown', enforceEmailInput);



