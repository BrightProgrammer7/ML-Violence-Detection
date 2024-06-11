import numpy as np
import cv2
from keras.models import load_model
from collections import deque
import io
import os
import logging
import tempfile
from PIL import Image, ImageEnhance
import gradio as gr

# Configure logging
logging.basicConfig(level=logging.ERROR)

# Load the pre-trained model
model = load_model('modelnew.h5')
Q = deque(maxlen=128)


def detect_violence(video):
    true_count = 0

    print("Loading model ...")
    vs = cv2.VideoCapture(video)
    writer = None
    (W, H) = (None, None)

    try:
        while True:
            (grabbed, frame) = vs.read()

            if not grabbed:
                break

            if W is None or H is None:
                (H, W) = frame.shape[:2]

            output = frame.copy()

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame_rgb, (128, 128)).astype("float32") / 255.0

            preds = model.predict(np.expand_dims(frame, axis=0))[0]
            label = (preds > 0.50)
            Q.append(preds)

            results = np.array(Q).mean(axis=0)

            text_color = (0, 255, 0)  # default: green

            if label:  # Violence prob
                text_color = (0, 0, 255)  # red
                true_count += 1
                frame_with_violence = frame_rgb
                

            text = "Violence: {}".format(label)
            FONT = cv2.FONT_HERSHEY_SIMPLEX

            cv2.putText(output, text, (35, 50), FONT, 1.25, text_color, 3)

            if writer is None:
                fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                writer = cv2.VideoWriter("output.avi", fourcc, 30, (W, H), True)
            writer.write(output)

    except Exception as e:
        logging.error(f"An error occurred during video processing: {e}")

    finally:
        # Release resources
        if writer:
            writer.release()
        if vs:
            vs.release()
        cv2.destroyAllWindows()
        


async def process_video(video):
    tmp_file_path = None
    
    if video is None:
        return {"message": "File Required"}

    # if not video.name.endswith(('.mp4', '.avi', '.mpeg')):
    #     raise ValueError("Invalid file format. Supported formats: mp4, avi, mpeg")

    
    try:
        # Save the uploaded video to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(await video.read())
            tmp_file_path = tmp_file.name

        # Detect violence in the video
        detect_violence(tmp_file_path)

        # Return completion message
        return "Processing completed"

    except Exception as e:
        # logging.error(f"An error occurred during video processing: {e}")
        return "Internal Server Error"

    finally:
        # Delete temporary file
        if tmp_file_path:
            os.unlink(tmp_file_path)


# Define Gradio interface
input_video = gr.Video(label="Upload Video")
output_text = gr.Textbox(label="Output")

demo = gr.Interface(
    fn=process_video,
    inputs=input_video,
    outputs=output_text,
    title="Violence Detection",
    description="Upload a video to detect violence.",
)


if __name__ == "__main__":
    demo.launch()
