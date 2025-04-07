
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import cv2
import numpy as np
import random

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def get_home():
    return HTMLResponse(open("static/index.html").read())



def process_frame(frame_bytes):
    nparr = np.frombuffer(frame_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    
    h, w = img.shape[:2]
    x1, y1 = random.randint(0, w-100), random.randint(0, h-100)
    x2, y2 = x1 + 100, y1 + 100
    color = (0, 255, 0)
    cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)

    
    _, encoded = cv2.imencode('.jpg', img)
    return encoded.tobytes()


@app.websocket("/ws/stream")
async def stream_video(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            processed = process_frame(data)
            await websocket.send_bytes(processed)
    except Exception as e:
        print("WebSocket disconnected:", e)
