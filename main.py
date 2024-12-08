from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from robot import Robot
from camera import Camera


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    print("Releasing camera")
    camera.release()


camera = Camera(0)
camera.get_frame()
robot = Robot()
app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, name="index.html")


def move_robot(key):
    match key:
        case "w":
            robot.forward()
        case "s":
            robot.backward()
        case "a":
            robot.left()
        case "d":
            robot.right()
        case " ":
            robot.stop()
        case "Enter":
            # TODO: Load
            pass
        case "Shift":
            robot.rotate()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        move_robot(data["key"])
        print(data)
