import asyncio
import websockets
import cv2
import numpy as np
import random

# Dummy ML function


def process_frame(frame):
    height, width, _ = frame.shape
    size = 50
    x = (width // 2) - 25
    y = (height // 2) - 25
    color = (
        255, 255, 255
    )
    cv2.rectangle(frame, (x, y), (x + size, y + size), color, 2)
    return frame

# Decode JPEG bytes to frame


def decode_jpeg(jpeg_bytes):
    nparr = np.frombuffer(jpeg_bytes, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

# Encode frame to JPEG bytes


def encode_jpeg(frame):
    success, jpeg = cv2.imencode('.jpg', frame)
    return jpeg.tobytes() if success else None


async def handle(websocket):
    print("Client connected")
    try:
        async for message in websocket:
            frame = decode_jpeg(message)
            if frame is None:
                print("Failed to decode JPEG")
                continue
            processed = process_frame(frame)
            jpeg_bytes = encode_jpeg(processed)
            if jpeg_bytes:
                await websocket.send(jpeg_bytes)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")


async def main():
    async with websockets.serve(handle, "localhost", 8000, max_size=2**24):
        print("Server started on ws://localhost:8000")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
