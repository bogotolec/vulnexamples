var socket = new WebSocket('ws://' + window.location.host + '/chat/');

socket.onmessage = function(e) {
    var response = JSON.parse(e.data);

    var li = document.createElement("li");
    if (response.error) {
        li.innerHTML = '<font color="red">' + response['error'] + '</font>';
    } else {
        li.innerHTML = '<b>' + response['username'] + ':</b> ';
        li.append(response['message']);
    }

    var chat = document.getElementById('chat');
    chat.insertBefore(li, chat.children[0])
};

socket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.getElementById('chatform').onsubmit = function(e) {
	e.preventDefault();
    var messageEl = document.getElementById('message');
    socket.send(JSON.stringify({'message': messageEl.value}));
    messageEl.value = '';
    messageEl.focus();
};