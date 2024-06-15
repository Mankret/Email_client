function showMessageDetails(messageId) {
    fetch(`/messages/${messageId}/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('message-list').style.display = 'none';
            document.getElementById('message-details').style.display = 'block';
            document.getElementById('message-content').innerHTML = `
                <button onclick="hideMessageDetails()">Back to Inbox</button>
                <div>
                    <h3>From: ${data.from_who}</h3>
                    <p><strong>Subject:</strong> ${data.subject}</p>
                    <p>${data.body}</p>
                </div>
            `;
        });
}

function hideMessageDetails() {
    document.getElementById('message-list').style.display = 'block';
    document.getElementById('message-details').style.display = 'none';
    document.getElementById('message-content').innerHTML = '';
}

