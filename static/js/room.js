const room_slug = JSON.parse(document.getElementById("room-slug").textContent);
const username = JSON.parse(document.getElementById("user-name").textContent);
console.log(room_slug);
const chatSocket = new WebSocket(
  "ws://" + window.location.host + "/ws/chatroom/" + room_slug + "/"
);

chatSocket.onclose = function (e) {
  console.log("onclose");
};

document.querySelector("#chat-message-submit").onclick = function (e) {
  const messageInput = document.querySelector("#input-message");
  const message = messageInput.value;
  console.log(message);
  // e.preventDefault();
  chatSocket.send(
    JSON.stringify({
      message: message,
      username: username,
      room_slug: room_slug,
    })
  );
  messageInput.value = "";
  // scrollChatToBottom();
};

function addElement(message) {
  var chat_conatiner = document.getElementById("chat-message");
  var userMessage =
    '<p class="username">' +
    username +
    '</p><p class="content">' +
    message +
    "</p>";
  chat_conatiner.innerHTML += userMessage;
  document.getElementById("input-message").value = "";
  chat_conatiner.scrollTop = chat_conatiner.scrollHeight;
}

chatSocket.onmessage = function (event) {
  const data = JSON.parse(event.data);
  message = data["message"];
  addElement(message, "user");
};
