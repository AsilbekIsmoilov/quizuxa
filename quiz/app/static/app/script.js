let totalSeconds = 600;

function startTimer() {
    const timer = document.getElementById('timer');
    if (sessionStorage.getItem('test_started')) {
        sessionStorage.removeItem('test_started');
        window.location.href = '/accounts/logout/';
        return;
    }

    sessionStorage.setItem('test_started', 'true');

    const interval = setInterval(() => {
        const minutes = Math.floor(totalSeconds / 60);
        const seconds = totalSeconds % 60;
        timer.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        totalSeconds--;

        if (totalSeconds < 0) {
            clearInterval(interval);
            sessionStorage.removeItem('test_started');
            document.getElementById('test-form').submit();
        }
    }, 1000);
}

window.onload = startTimer;
