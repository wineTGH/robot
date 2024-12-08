from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, name="index.html")


def move_robot(key):
    match key:
        case "w":
            # TODO: Forward
            pass
        case "s":
            # TODO: Backward
            pass
        case "a":
            # TODO: Left
            pass
        case "d":
            # TODO: Right
            pass
        case " ":
            # TODO: Stop
            pass
        case "Enter":
            # TODO: Load
            pass
        case "Shift":
            # TODO: Rotate
            pass


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        move_robot(data["key"])
