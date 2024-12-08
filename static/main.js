const ws = new WebSocket(`ws://${location.host}/ws`);

window.addEventListener('keyup', (e) => {
    sendKey(e.key);
});

/**
 * Отправляет название кнопки роботу
 * @param {string} key 
 */
function sendKey(key) {
    ws.send(JSON.stringify({ key: key.toLowerCase() }));
}