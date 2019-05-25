var socket = new WebSocket('ws://' + window.location.host + '/chat/');

socket.onmessage = function(e) {
    var response = JSON.parse(e.data);

    var li = document.createElement("li");
    li.classList.add(response.type);
    switch (response.type) {
        case 'connected':
            li.innerHTML = '<span class="username">' + response['username'] + '</span> has connected';
        break;
        case 'error':
            li.innerText = response['error'];
        break;
        case 'message':
            li.innerHTML = '<span class="username">' + response['username'] + ': </span>';
            li.append(response['message']);
        break;
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