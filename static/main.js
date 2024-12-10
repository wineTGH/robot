const ws = new WebSocket(`ws://${location.host}/ws`);

let lastEvent;
let heldKeys = {};

window.addEventListener('keydown', (e) => {
    if (lastEvent && lastEvent.key === e.key) {
        return;
    }

    lastEvent = e;
    heldKeys[e.key] = true;
    sendKey(e.key, 1);
});


window.addEventListener('keyup', (e) => {
    sendKey(e.key, 0);

    lastEvent = null;
    delete heldKeys[e.key];
});
/**
 * Отправляет название кнопки роботу
 * @param {string} key 
 * @param {number} state 
 */
function sendKey(key, state) {
    ws.send(`${key};${state}`);
}