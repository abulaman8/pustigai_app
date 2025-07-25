import psutil
import signal
from collections import deque
import base64
import asyncio
import json
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Request, Form, HTTPException
import sys
import os
import time
import traceback
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates


from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'src')))

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def handle_shutdown(signum, frame):
    print("Received shutdown signal")
    sys.exit(0)


signal.signal(signal.SIGINT, handle_shutdown)
signal.signal(signal.SIGTERM, handle_shutdown)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/exercises-api")
async def get_exercises_api(db: Session = Depends(get_db)):
    print("Fetching exercises from database")
    exercises = crud.get_all_exercises(db)
    return [{"id": ex.id, "name": ex.name} for ex in exercises]


@app.get("/manage-exercises", response_class=HTMLResponse)
async def manage_exercises_page(request: Request, db: Session = Depends(get_db)):
    exercises = crud.get_all_exercises(db)
    return templates.TemplateResponse("manage_exercises.html", {"request": request, "exercises": exercises})


@app.get("/add-exercise", response_class=HTMLResponse)
async def add_exercise_page(request: Request):
    return templates.TemplateResponse("exercise_form.html", {"request": request, "exercise": None, "action_url": "/add-exercise"})


@app.post("/add-exercise", response_class=RedirectResponse)
async def handle_add_exercise(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    # Convert form data to a dictionary to pass to the Pydantic model
    exercise_dict = {key: value for key, value in form.items()}
    # Create the Pydantic model instance for validation
    exercise_data = schemas.ExerciseCreate(**exercise_dict)
    # Create the exercise in the database
    crud.create_exercise(db=db, exercise=exercise_data)
    # Redirect to the management page (status_code 303 is correct for POST-redirect-GET)
    return RedirectResponse(url="/manage-exercises", status_code=303)


@app.get("/edit-exercise/{exid}", response_class=HTMLResponse)
async def edit_exercise_page(request: Request, exid: str, db: Session = Depends(get_db)):
    exercise = crud.get_exercise(db, exid)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return templates.TemplateResponse("exercise_form.html", {"request": request, "exercise": exercise, "action_url": f"/edit-exercise/{exid}"})


@app.post("/edit-exercise/{exid}", response_class=RedirectResponse)
async def handle_edit_exercise(request: Request, exid: str, db: Session = Depends(get_db)):
    form = await request.form()
    crud.update_exercise(db=db, exid=exid, exercise_data=form._dict)
    return RedirectResponse(url="/manage-exercises", status_code=303)


@app.delete("/exercises/{exid}")
async def delete_exercise_api(exid: str, db: Session = Depends(get_db)):
    success = crud.delete_exercise(db, exid)
    if not success:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return {"message": "Exercise deleted successfully"}


@app.websocket("/ws/stream")
async def stream_video(websocket: WebSocket):
    await websocket.accept()
    db = SessionLocal()

    session_data = {"start_time": None}
    frame_queue = deque(maxlen=10)
    batch_size = 2
    is_initialized = False
    processing_task = None

    # This is a placeholder for your frame processing logic.
    # It must be defined within the WebSocket endpoint's scope.
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
                    # Assuming process_frame_batch exists and is imported
                    from src.obfuscated.processor import process_frame_batch
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
            await asyncio.sleep(0.083)  # ~12 FPS
        return False

    try:
        # Start the frame processing task
        processing_task = asyncio.create_task(process_frames())

        while True:
            message = await websocket.receive()
            if "bytes" in message:
                if not is_initialized:
                    print("Frame received before initialization")
                    await websocket.send_text(json.dumps({"error": "Exercise data not initialized"}))
                    continue
                frame_queue.append(message["bytes"])
            elif "text" in message:
                try:
                    data = json.loads(message["text"])
                    user_id = data.get("user_id")
                    exid = data.get("exercise_id")

                    user_info = crud.get_user(db, user_id)
                    if user_info:
                        session_data["user_name"] = user_info.user_name
                        session_data["exid"] = exid

                        exdata_obj = crud.get_exercise(db, exid)
                        if exdata_obj:
                            # Convert SQLAlchemy object to dictionary for processing
                            session_data["exdata"] = crud.to_dict(exdata_obj)
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
        if processing_task and not processing_task.done():
            processing_task.cancel()
        db.close()
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    print("Starting FastAPI server")
    # Recommended to run uvicorn with the string path for reload to work correctly
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
