const ws = new WebSocket(`ws://${location.host}/ws`);

window.addEventListener('keyup', (e) => {
    ws.send(JSON.stringify({ key: e.key }))
});