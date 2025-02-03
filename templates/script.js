//Submit score
document.getElementById('scoreForm').onsubmit = async (e) => {
    e.preventDefault();
    const data = {
        username: document.getElementById('username').value,
        time_taken: parseFloat(document.getElementById('time_taken').value),
        emojis_used: parseInt(document.getElementById('emojis_used').value)
    };

    try {
        const response = await fetch('/api/submit-score', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        if(response.ok) {
            loadLeaderboard();
            alert('Score submitted successfully!');
        }
    } catch (error) {
        console.error('Error:', error);
    }
};

// Load leaderboard
async function loadLeaderboard() {
    try {
        const response = await fetch('/api/leaderboard');
        const data = await response.json();
        const tbody = document.querySelector('#leaderboard tbody');
        tbody.innerHTML = data.map(entry => `
            <tr>
                <td>${entry.username}</td>
                <td>${entry.time_taken}s</td>
                <td>${entry.emojis_used}</td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error:', error);
    }
}

// Initial load
loadLeaderboard();