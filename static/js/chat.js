// This file contains the javascript code for the chat app
const username = JSON.parse(document.getElementById('provider-username').textContent)
const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + username
    + '/'
);    

function addElement(message, user){
    var chatBox = document.getElementById('chatBox');
    var userMessage = '<div class="message '+ user+'-message">' + message + '</div>';
    chatBox.innerHTML += userMessage;
    document.getElementById('userInput').value = '';
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
}

document.querySelector('#chat-message-submit').onclick = function(e){
    e.preventDefault();
    var message = document.getElementById('userInput').value;
    if (message){
        console.log(message)
        chatSocket.send(JSON.stringify({
            "message":message,
            "username":username,
     }))
    }
}

chatSocket.onclose = function(e) {
    console.log("onclose");
}

chatSocket.onmessage = function(event){
    const data = JSON.parse(event.data);
    message = data['message'];
    addElement(message, 'user');
}



