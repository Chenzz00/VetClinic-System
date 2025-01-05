document.addEventListener('click', function(event) {
    const dropdown = document.querySelector('.profile-dropdown ul');
    const summary = document.querySelector('.profile-dropdown summary');

    // If the click was not on the summary or within the dropdown, close it
    if (!summary.contains(event.target) && !dropdown.contains(event.target)) {
        dropdown.style.display = 'none';
    }
});

// Optional: Automatically open dropdown on click
document.querySelector('.profile-dropdown summary').addEventListener('click', function(event) {
    const dropdown = document.querySelector('.profile-dropdown ul');
    dropdown.style.display = 'block';
});