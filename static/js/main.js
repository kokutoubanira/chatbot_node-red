(function () {

    function showMessage(message) {
        $('#messages').append('<li>' + message)
    }

    if (!window.WebSocket) {
        if (window.MozWebSocket) {
            window.WebSocket = window.MozWebSocket;
        } else {
            showMessage("Your browser doesn't support WebSockets")
        }
    }

    let scheme = window.location.protocol === "https:" ? 'wss://' : 'ws://';
    let webSocketUri = scheme
        + window.location.hostname
        + (location.port ? ':' + location.port : '')
        + $SCRIPT_ROOT + '/websocket';
    let ws = new WebSocket(webSocketUri);

    ws.onopen = function (evt) {
        showMessage('Connected to chat.')
    }

    ws.onmessage = function (evt) {
        showMessage(evt.data)
    }

    ws.onclose = function (evt) {
        $('#messages').append('<li>WebSocket connection closed.</li>');
    }

    $('#send-message').on("submit", function () {
        let message = $('#name').val() + ": " + $('#message').val();
        showMessage(message)
        ws.send(message);
        $('#message').val('').trigger('focus');
        return false;
    });
}());