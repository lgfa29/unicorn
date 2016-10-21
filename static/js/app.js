$(function() {
    var updater = {
        socket: null,

        start: function() {
            var url = "ws://" + location.host + "/ws/color";
            updater.socket = new WebSocket(url);
            updater.socket.onmessage = function(event) {
                var msg = JSON.parse(event.data);
                updater.setColor(msg.color);
            }
        },

        setColor: function(color) {
            $("#flat").spectrum("set", color);
        }
    };

    $("#flat").spectrum({
        flat: true,
        move: function(color) {
            var msg = {
                color: color.toHexString()
            };

            updater.socket.send(JSON.stringify(msg));
        }
    });

    updater.start();
});
