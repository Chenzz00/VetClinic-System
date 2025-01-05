function disablePrevWeekButton() {
    const currentDate = new Date();
    const currentOffset = parseInt(new URLSearchParams(window.location.search).get('week_offset') || '0');
    const prevWeekOffset = currentOffset - 1;
    
    if (prevWeekOffset < 0) {
        document.getElementById('prev-week').disabled = true;
    } else {
        document.getElementById('prev-week').disabled = false;
    }
}

function navigateWeek(direction) {
    const currentOffset = parseInt(new URLSearchParams(window.location.search).get('week_offset') || '0');
    const newOffset = currentOffset + direction;
    window.location.search = `?week_offset=${newOffset}`;
}

window.onload = disablePrevWeekButton;