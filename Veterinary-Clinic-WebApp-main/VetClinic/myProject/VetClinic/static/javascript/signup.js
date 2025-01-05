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

    // Check if email format is correct
    if (!checkEmailFormat(emailInput)) {
        alert("Please enter a valid email address ending with @gmail.com");
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

function validateForm(event) {
    event.preventDefault(); // Prevent form submission initially

    // Show a custom notification with only the OK button
    alert("Your account is being registered. Click OK to continue.");

    // After the user clicks OK, submit the form
    document.getElementById("registration-form").submit();
}
