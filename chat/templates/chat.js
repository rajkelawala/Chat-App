let chatSocket = new WebSocket("ws://localhost:8000/ws/chat/");

chatSocket.onmessage = function(event) {
    let data = JSON.parse(event.data);
    let chatBox = document.getElementById("chat-box");
    let messageElement = document.createElement("div");
    messageElement.innerHTML = `<strong>${data.sender}:</strong> ${data.message}`;
    chatBox.appendChild(messageElement);
};

function sendMessage(sender, receiver, message) {
    chatSocket.send(JSON.stringify({
        sender: sender,
        receiver: receiver,
        message: message
    }));
}

async function loadChatMessages(userId) {
    let response = await fetch(`/chat/messages/${userId}/`);
    let data = await response.json();
    
    let chatBox = document.getElementById("chat-box");
    chatBox.innerHTML = "";

    data.messages.forEach(msg => {
        let messageElement = document.createElement("div");
        messageElement.innerHTML = `<strong>${msg.sender}:</strong> ${msg.message}`;
        chatBox.appendChild(messageElement);
    });
}
