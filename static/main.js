const ws = new WebSocket(`ws://${location.host}/ws`);

window.addEventListener('keyup', (e) => {
    sendKey(e.key);
});

function sendKey(key) {
    ws.send(JSON.stringify({ key }));
}