from contextlib import asynccontextmanager
import time

from imutils.video import WebcamVideoStream
import cv2

from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from robot import Robot


class Camera:
    def __init__(self, id: int = 0):
        self.stream = WebcamVideoStream(src=id).start()

    def __del__(self):
        self.stream.stop()

    def get_frame(self):
        image = self.stream.read()
        _, jpeg = cv2.imencode(".jpg", image)

        return jpeg.tobytes()


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


def gen_frames(camera: Camera):  # generate frame by frame from camera
    while True:
        frame = camera.get_frame()
        yield (
            b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n"
        )  # concat frame one by one and show $
        time.sleep(0.04)


@app.get("/video", response_class=StreamingResponse)
async def video_feed(id: int = 0):
    return StreamingResponse(
        gen_frames(Camera(id)), media_type="multipart/x-mixed-replace; boundary=frame"
    )


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
        data = await websocket.receive_text()
        key, state = data.split(";")
        move_robot(key)
        print(data)
