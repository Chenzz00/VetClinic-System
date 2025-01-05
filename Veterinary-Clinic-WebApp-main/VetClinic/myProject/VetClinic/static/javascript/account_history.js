// Search functionality
document.getElementById('search-button').addEventListener('click', function() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const rows = document.querySelectorAll('table tbody tr');
    
    rows.forEach(row => {
        const cells = row.getElementsByTagName('td');
        let match = false;
        
        for (let cell of cells) {
            if (cell.textContent.toLowerCase().includes(searchTerm)) {
                match = true;
                break;
            }
        }
        
        row.style.display = match ? '' : 'none';
    });
});

// Sort functionality
document.getElementById('sort-button').addEventListener('click', function() {
    const selectedColumn = document.getElementById('sort-column').value;
    const table = document.querySelector('table tbody');
    const rows = Array.from(table.querySelectorAll('tr'));

    // Sort based on the selected column
    rows.sort((a, b) => {
        let cellA, cellB;
        switch (selectedColumn) {
            case 'first-name':
                cellA = a.cells[0].textContent.toLowerCase();
                cellB = b.cells[0].textContent.toLowerCase();
                break;
            case 'last-name':
                cellA = a.cells[1].textContent.toLowerCase();
                cellB = b.cells[1].textContent.toLowerCase();
                break;
            case 'email':
                cellA = a.cells[2].textContent.toLowerCase();
                cellB = b.cells[2].textContent.toLowerCase();
                break;
            case 'address':
                cellA = a.cells[3].textContent.toLowerCase();
                cellB = b.cells[3].textContent.toLowerCase();
                break;
            case 'phone':
                cellA = a.cells[4].textContent.toLowerCase();
                cellB = b.cells[4].textContent.toLowerCase();
                break;
            default:
                break;
        }

        return cellA.localeCompare(cellB);
    });

    // Clear the table and re-append sorted rows
    table.innerHTML = '';
    rows.forEach(row => table.appendChild(row));
});
