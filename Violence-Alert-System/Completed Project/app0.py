from fastapi import FastAPI, File, UploadFile, HTTPException
import cv2
import numpy as np
from fastapi.responses import StreamingResponse
from io import BytesIO
from violence_detection import print_results  
# Assuming your existing logic is in violence_detection.py
import pickle
import requests

app = FastAPI()
@app.get('/')
async def read_root():
    return {"Salam": "World"}


@app.post("/detect_violence")
async def detect_violence(video_file: UploadFile = File(...)):
    if not video_file.filename.endswith(('.mp4', '.avi', '.mpeg')):
        raise HTTPException(status_code=400, detail="Invalid file format. Supported formats: mp4, avi, mpeg")

    contents = await video_file.read()
    video_np = np.frombuffer(contents, dtype=np.uint8)
    video = cv2.imdecode(video_np, cv2.IMREAD_COLOR)

    # Process video frames and detect violence
    processed_video = print_results(video)
    # Check if the processed video is empty or invalid
    if processed_video is None or len(processed_video) == 0:
        raise ValueError("Processed video is empty or invalid")

    # Convert processed video to bytes
    video_bytes = cv2.imencode('.avi', processed_video)[1].tobytes()

    # Return the processed video as a streaming response
    return StreamingResponse(BytesIO(video_bytes), media_type="video/avi")
