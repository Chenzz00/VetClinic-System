function validateLogin(event) {
    event.preventDefault();  

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    if (!email || !password) {
        alert("Please enter both email and password.");
        return;
    }

    fetch(window.loginUrl, {
        method: "POST",
        headers: {
            "X-CSRFToken": window.csrfToken,
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
            email: email,
            password: password
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert("Login successful! Redirecting...");
            if (data.is_admin) {
                window.location.href = "Appointment-Schedule";  // Redirect admin to Appointment-Schedule
            } else if (data.is_vet) {
                window.location.href = "Client-Records";  // Redirect vet to Client-Records
            } else {
                window.location.href = window.ownerUrl;  // Redirect regular users
            }
        } else {
            alert(data.message);  // Show error message
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred. Please try again.");
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const carousels = document.querySelectorAll('.carousel'); // Get both types of carousels

    carousels.forEach((carousel) => {
        let currentIndex = 0;  // Index of the currently displayed slide
        const carouselImages = carousel.querySelector('.carousel-images'); // Get the container for the slides
        const totalSlides = carouselImages.querySelectorAll('.carousel-slide').length; // Get the total number of slides dynamically
        const visibleCount = 4; // Number of visible slides (adjust this if needed)

        // Function to move the slide based on direction
        function moveSlide(direction) {
            // Calculate the new index after moving (direction is -1 for previous, 1 for next)
            let newIndex = currentIndex + direction;

            // Ensure the newIndex is within bounds
            if (newIndex < 0) {
                newIndex = 0; // Prevent moving past the first slide
            } else if (newIndex > totalSlides - visibleCount) {
                newIndex = totalSlides - visibleCount; // Prevent moving past the last set of slides
            }

            // Apply the new index to the carousel
            currentIndex = newIndex;

            // Move the slides by changing the transform property
            const offset = -currentIndex * (100 / visibleCount); // Calculate the offset for sliding effect
            carouselImages.style.transform = `translateX(${offset}%)`; // Apply the transform
        }

        // Initialize the carousel to show the first set of slides
        moveSlide(0);

        // Attach event listeners to buttons
        carousel.querySelector('.prev').addEventListener('click', () => moveSlide(-1));
        carousel.querySelector('.next').addEventListener('click', () => moveSlide(1));
    });
});


document.addEventListener('DOMContentLoaded', function() {
    var appointmentLink = document.getElementById('appointment-link');
    // Get the logged-in status from the data attribute
    var loggedIn = document.querySelector('.login-container').getAttribute('data-logged-in') === 'true';

    if (!loggedIn) {
        appointmentLink.style.display = 'none';
    } else {
        appointmentLink.style.display = 'inline';  // Ensure it is visible when logged in
    }
});
