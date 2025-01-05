// Handle cancellation logic
function handleCancel() {
    const cancelOption = document.getElementById('cancel-option').value;
    if (cancelOption === 'yes') {
        const reason = prompt("Please provide a reason for cancellation:");
        if (reason) {
            alert(`Your appointment has been cancelled for the following reason: ${reason}`);
        } else {
            alert("Cancellation reason not provided.");
        }
    } else if (cancelOption === 'no') {
        alert("Your appointment will remain scheduled.");
    } else {
        alert("Please select an option.");
    }
}

// Close dropdowns when clicking outside
document.addEventListener('click', function(event) {
    const profileDropdown = document.querySelector('.profile-dropdown');
    const notificationDropdown = document.querySelector('.notification-content');
    
    // Close profile dropdown if it's open and click is outside
    if (profileDropdown.open && !profileDropdown.contains(event.target) && !event.target.matches('.profile-dropdown summary')) {
        profileDropdown.removeAttribute('open');
    }
    
    // Close notification dropdown if it's open and click is outside
    const notificationParent = notificationDropdown.parentNode;
    if (notificationParent.open && !notificationDropdown.contains(event.target) && !event.target.matches('.notification-icon')) {
        notificationParent.removeAttribute('open');
    }
});

// Prevent dropdowns from closing when interacting with their content
document.querySelectorAll('.profile-dropdown, .notification-content').forEach(dropdown => {
    dropdown.addEventListener('click', function(event) {
        event.stopPropagation(); // Prevent the click from bubbling up to the document
    });
});

// Display updated walk-in hours on the homepage if available in localStorage
window.onload = function() {
    const walkInHours = localStorage.getItem('walkInHours');
    if (walkInHours) {
        document.getElementById('display-walk-in-hours').textContent = walkInHours;
    }
};

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
