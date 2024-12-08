const ws = new WebSocket("ws://127.0.0.1:8000/ws");

window.addEventListener('keyup', (e) => {
    ws.send(JSON.stringify({ key: e.key }))
});

setInterval()