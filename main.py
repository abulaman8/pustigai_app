import psutil
import signal
from collections import deque
import base64
import asyncio
import json
from src.obfuscated.processor import process_frame_batch
from src.database import get_user, get_exercise, exercises_db
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import sys
import os
import time
import traceback

# Add src/ to sys.path for PyArmor runtime
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'src')))


app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Signal handler for graceful shutdown


def handle_shutdown(signum, frame):
    print("Received shutdown signal")
    sys.exit(0)


signal.signal(signal.SIGINT, handle_shutdown)
signal.signal(signal.SIGTERM, handle_shutdown)

# HTML endpoint


@app.get("/")
async def get_home():
    with open(os.path.join("static", "index.html")) as f:
        return HTMLResponse(f.read())

# Exercises endpoint


@app.get("/exercises")
async def get_exercises():
    print("Fetching exercises")
    exercises = [{"id": exid, "name": data["name"]}
                 for exid, data in exercises_db.items()]
    return exercises

# WebSocket endpoint


@app.websocket("/ws/stream")
async def stream_video(websocket: WebSocket):
    print("WebSocket connection attempt")
    await websocket.accept()
    session_data = {"start_time": None}
    frame_queue = deque(maxlen=10)
    batch_size = 2
    is_initialized = False

    async def process_frames():
        proc = psutil.Process()
        while True:
            if len(frame_queue) >= batch_size:
                batch = [frame_queue.popleft()
                         for _ in range(min(batch_size, len(frame_queue)))]
                try:
                    # Log memory usage
                    mem = proc.memory_info()
                    print(f"Process memory: {mem.rss / 1024 / 1024:.2f} MB")
                    # Process frames directly
                    start_time = time.time()
                    results = await asyncio.to_thread(process_frame_batch, batch, session_data)
                    print(
                        f"Processor output: {results}, processing time: {time.time() - start_time:.3f}s")
                    for processed, result in results:
                        if processed:
                            processed_b64 = base64.b64encode(
                                processed).decode('utf-8')
                            await websocket.send_bytes(base64.b64decode(processed_b64))
                            await websocket.send_text(json.dumps({
                                "feedback": result["feedback"],
                                "rtn1": result["rtn1"],
                                "next_exer": result["next_exer"],
                                "repe": result["repe"]
                            }))
                            if result["rtn1"] == "complete" and not result["next_exer"]:
                                print("Exercise complete, stopping processing")
                                return True
                        else:
                            print(f"Processing error in result: {result}")
                            await websocket.send_text(json.dumps({"error": result.get("error", "Unknown error")}))
                except Exception as e:
                    print(
                        f"Processing error: {e}, traceback: {traceback.format_exc()}")
                    await websocket.send_text(json.dumps({"error": f"Processing error: {str(e)}"}))
            await asyncio.sleep(0.083)  # ~12 FPS (1/12 = 0.083s)
        return False

    try:
        print("Starting process_frames task")
        processing_task = asyncio.create_task(process_frames())
        while True:
            message = await websocket.receive()
            print(f"Received message: {type(message)}")
            if "bytes" in message:
                if not is_initialized:
                    print("Frame received before initialization")
                    await websocket.send_text(json.dumps({"error": "Exercise data not initialized"}))
                    continue
                frame_queue.append(message["bytes"])
                print(f"Frame queued, queue size: {len(frame_queue)}")
            elif "text" in message:
                try:
                    data = json.loads(message["text"])
                    print(f"Received text data: {data}")
                    user_id = data.get("user_id")
                    exid = data.get("exercise_id")
                    user_info = get_user(user_id)
                    if user_info:
                        session_data["user_name"] = user_info["user_name"]
                        session_data["exid"] = exid
                        exdata = get_exercise(exid)
                        if exdata:
                            session_data["exdata"] = exdata
                            is_initialized = True
                            print(
                                f"Initialization successful: user={user_id}, exercise={exid}")
                            await websocket.send_text(json.dumps({"status": "ok", "message": "User and exercise data loaded"}))
                        else:
                            print(f"Exercise not found: {exid}")
                            await websocket.send_text(json.dumps({"error": "Exercise not found"}))
                    else:
                        print(f"User not found: {user_id}")
                        await websocket.send_text(json.dumps({"error": "User not found"}))
                except json.JSONDecodeError:
                    print("Invalid JSON received")
                    await websocket.send_text(json.dumps({"error": "Invalid JSON"}))
            if processing_task.done():
                print("Processing task completed")
                if processing_task.result():
                    break
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}, traceback: {traceback.format_exc()}")
    finally:
        print("Cleaning up WebSocket")
        processing_task.cancel()
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    print("Starting FastAPI server")
    uvicorn.run(app, host="0.0.0.0", port=8000)
