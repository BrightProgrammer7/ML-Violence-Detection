from fastapi import FastAPI, UploadFile, File
import cv2
from cv2 import imshow
import numpy as np
from keras.models import load_model
from collections import deque
import os
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn
import tempfile

app = FastAPI()

# Allow requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/detect_violence")
async def detect_violence(video: UploadFile = File(...)):
    if video.filename == "":
        return{"message": "File Required"}
        
    if not video.filename.endswith(('.mp4', '.avi', '.mpeg')):
        raise HTTPException(status_code=400, detail="Invalid file format. Supported formats: mp4, avi, mpeg")

    # Save the uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(await video.read())
        tmp_file_path = tmp_file.name

    # Open the temporary file using cv2.VideoCapture
    vs = cv2.VideoCapture(tmp_file_path)
    
    # video_bytes = vs.read()
    success, frame = vs.read()
    if not success:
        # Handle case where frame could not be read
        logging.error("Failed to read frame from video")
        return {"error": "Failed to read frame from video"}
    else:
        logging.info("Frame successfully read from video")

    # Convert the frame to bytes
    video_bytes = frame.tobytes()
    nparr = np.frombuffer(video_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if frame is None:
        logging.error("Failed to read frame from video")
        return {"error": "Failed to read frame from video"}
    
        
    logging.info(f"Frame shape: {frame.shape}")
        
    if frame.size == 0:
            logging.error("Empty frame received")
            return {"error": "Empty frame received"}
        
        # Process the video frames and detect violence
    preds = process_frame(frame)

        # Check if the processed video is empty or invalid
    if preds is None or len(preds) == 0:
            raise ValueError("Processed video is empty or invalid")

        # Convert back to bytes
    _, output_frame = cv2.imencode('.jpg', frame)
        
    output_bytes = output_frame.tobytes()

        # Convert processed video to bytes
        # output_bytes = cv2.imencode('.avi', preds)[1].tobytes()

    return {"prediction": preds, "processed_video": output_bytes}
    


def process_frame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (128, 128)).astype("float32")
    frame = frame.reshape(128, 128, 3) / 255

    print("Loading model ...")
    model = load_model('modelnew.h5')
    Q = deque(maxlen=128)


    # make predictions on the frame and then update the predictions
    preds = model.predict(np.expand_dims(frame, axis=0))[0]
    Q.append(preds)

    # perform prediction averaging over the current history of
    # previous predictions
    results = np.array(Q).mean(axis=0)
    i = (preds > 0.50)[0]
    label = i

    text_color = (0, 255, 0)  # default: green
    if label:  # Violence prob
        text_color = (0, 0, 255)  # red
    else:
        text_color = (0, 255, 0)

    text = "Violence: {}".format(label)
    FONT = cv2.FONT_HERSHEY_SIMPLEX

    cv2.putText(frame, text, (35, 50), FONT, 1.25, text_color, 3)

    return preds

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
