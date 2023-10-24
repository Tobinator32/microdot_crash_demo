
let ws;

function heartbeat() {
    if (ws == null || ws.readyState !== WebSocket.OPEN) {
        ws = new WebSocket("ws://" + window.location.hostname, "heartbeat");
    } else {
        let heartbeat_data = JSON.stringify({heartbeat:1});
        ws.send(heartbeat_data);
    }
}