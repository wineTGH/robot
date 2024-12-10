from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from robot import Robot
import time


@asynccontextmanager
async def lifespan(app: FastAPI):
    robot.stop()
    yield
    robot.stop()


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
        case "enter":
            # TODO: Load
            robot.scan_qr()
        case "shift":
            robot.rotate()

        case "i":
            robot.actuator.forward()

        case "k":
            robot.actuator.backward()

        case "u":
            robot.m_lift.forward()

        case "j":
            robot.m_lift.backward()

        case "p":
            robot.servo_platform.value = 1
            time.sleep(1)
            robot.servo_platform.value = 0

        case "o":
            robot.servo_platform.value = -1
            time.sleep(0.8)
            robot.servo_platform.value = 0

        case "n":
            robot.servo_grab.value = -1

        case "m":
            robot.servo_grab.value = 1


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        move_robot(data["key"])
        print(data)
