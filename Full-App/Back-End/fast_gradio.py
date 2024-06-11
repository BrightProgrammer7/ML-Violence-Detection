import numpy as np
import cv2
import uvicorn
from keras.models import load_model
from collections import deque
import io
import os
import logging
import tempfile
from PIL import Image, ImageEnhance
import gradio as gr
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, UploadFile, File, HTTPException

app = FastAPI()
# Allow requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.ERROR)

# Load the pre-trained model
model = load_model('modelnew.h5')
Q = deque(maxlen=128)


# @app.post("/detect_violence")
@app.post("/")
async def detect_violence(video: str):
# async def detect_violence(video: UploadFile = File(...)):
    tmp_file_path = None

    if video is None:
        return {"message": "File Required"}

        
    # if not video.filename.endswith(('.mp4', '.avi', '.mpeg')):
    #     raise HTTPException(status_code=400, detail="Invalid file format. Supported formats: mp4, avi, mpeg")
    
    try:
        # # Save the uploaded video to a temporary file
        # with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        #     # Read the file content and write it to the temporary file
        #     contents = await video.read()
        #     tmp_file.write(contents)

        # Open the video file using cv2.VideoCapture
        # vs = cv2.VideoCapture(tmp_file_path)
        vs = cv2.VideoCapture(video)

        # Initialize variables for output video and frame with detected violence
        writer = None
        frame_with_violence = None
        (W, H) = (None, None)
        true_count = 0


        # Iterate over frames
        while True:
            # Read the next frame
            (grabbed, frame) = vs.read()

            # Check if frame was read successfully
            if not grabbed:
                break
                return {"error": "Failed to read frame from video"}
            

            if W is None or H is None:
                (H, W) = frame.shape[:2]
                
            # Preprocess frame for prediction
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame_rgb, (128, 128)).astype("float32") / 255.0

            # Make predictions on the frame
            preds = model.predict(np.expand_dims(frame, axis=0))[0]
            label = (preds > 0.50)
            Q.append(preds)

            # Perform prediction averaging over previous predictions
            results = np.array(Q).mean(axis=0)
                
            text_color = (0, 255, 0)  # default: green

            # Draw label on the frame if violence is detected
            if label:  # Violence prob
                text_color = (0, 0, 255)  # red
                true_count += 1
                frame_with_violence = frame_rgb

            text = "Violence: {}".format(label)
            FONT = cv2.FONT_HERSHEY_SIMPLEX

            cv2.putText(frame, text, (35, 50), FONT, 1.25, text_color, 3)
           

            # Write frame to output video
            if writer is None:
                fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                writer = cv2.VideoWriter("output.avi", fourcc, 30, (W, H), True)
            writer.write(frame)

        # Release resources
        vs.release()
        writer.release()
        cv2.destroyAllWindows()
    
        # Convert frame with detected violence to JPG image
        if frame_with_violence is not None:
            _, img_encoded = cv2.imencode(".jpg", frame_with_violence)
            img_bytes = io.BytesIO(img_encoded)

            # Save the image bytes to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                tmp_file.write(img_bytes)

            # Return the path to the temporary image file
            return tmp_file.name
            
        else:
            img_bytes = None
        

        # Return response
        # return {"message": "Processing completed"}

        # Return completion message and frame with detected violence as JPG image
        return StreamingResponse(io.BytesIO(img_bytes.getvalue()), media_type="image/jpeg")
        # return StreamingResponse(io.BytesIO(img_bytes), media_type="image/jpeg")



    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    finally:
        # Delete temporary file
        if tmp_file_path is not None:
            os.unlink(tmp_file_path)
        # Delete output file if it exists
        output_file_path = "output.avi"
        if os.path.exists(output_file_path):
            os.remove(output_file_path)


# Define Gradio interface
# input_video = gr.Video(label="Upload Video")
input_video = gr.File(label="Upload Video", file_types=['video', '.mp4'])
# output_text = gr.Textbox(label="Output")
output_text = gr.Image(label="Output", value="PIL.Image.Image")
# output_text = gr.File(label="Output", file_types=['image', '.jpeg'])

demo = gr.Interface(
    fn=detect_violence,
    inputs=input_video,
    outputs=output_text,
    title="Violence Detection",
    description="Upload a video to detect violence.",
)

app = gr.mount_gradio_app(app, demo, path="/gradio")
# Mount Gradio interface on a separate path
# app.mount("/gradio", gr.apps.FastAPI(demo))

if __name__ == "__main__":
    uvicorn.run("fast_gradio:app", host="0.0.0.0", port=8000, reload=True)