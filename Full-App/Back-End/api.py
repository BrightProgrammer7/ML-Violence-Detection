from fastapi import FastAPI, UploadFile, File, HTTPException
import numpy as np
import cv2
from keras.models import load_model
from collections import deque
import io
import os
import logging
import tempfile
from fastapi.responses import StreamingResponse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from mtcnn.mtcnn import MTCNN
import pyrebase
import telepot
from PIL import Image
from PIL import ImageEnhance
from datetime import datetime
import pytz
from matplotlib import pyplot

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

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

@app.get("/test")
async def test():
    return {"message": f"Hello World:"}

@app.post("/detect")
async def detect_violence(video: UploadFile = File(...)):
    tmp_file_path = None
    if video.filename == "":
        return{"message": "File Required"}
        
    if not video.filename.endswith(('.mp4', '.avi', '.mpeg')):
        raise HTTPException(status_code=400, detail="Invalid file format. Supported formats: mp4, avi, mpeg")
      
    try:
        # Save the uploaded video to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(await video.read())
            tmp_file_path = tmp_file.name

        # Open the video file using cv2.VideoCapture
        vs = cv2.VideoCapture(tmp_file_path)

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
                writer = cv2.VideoWriter("output/v_output.avi", fourcc, 30, (W, H), True)
                
            writer.write(frame)

        # release the file pointersq
        print("[INFO] cleaning up...")
        # Release resources
        vs.release()
        writer.release()
        cv2.destroyAllWindows()
    
        # Convert frame with detected violence to JPG image
        if frame_with_violence is not None:
            _, img_encoded = cv2.imencode(".jpg", frame_with_violence)
            img_bytes = io.BytesIO(img_encoded)
            
        else:
            img_bytes = None

        # Return response
        # return {"message": "Processing completed"}

        # Return completion message and frame with detected violence as JPG image
        return StreamingResponse(io.BytesIO(img_bytes.getvalue()), media_type="image/jpeg")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    finally:
        # Delete temporary file
        if tmp_file_path is not None:
            os.unlink(tmp_file_path)
        # Delete output file if it exists
        output_file_path = "v_output.avi"
        if os.path.exists(output_file_path):
            os.remove(output_file_path)

@app.post("/detect_violence")
async def detect_violence(video: UploadFile = File(...)):
    tmp_file_path = None
    if video.filename == "":
        return{"message": "File Required"}
        
    if not video.filename.endswith(('.mp4', '.avi', '.mpeg')):
        raise HTTPException(status_code=400, detail="Invalid file format. Supported formats: mp4, avi, mpeg")
      
    try:
        # Save the uploaded video to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(await video.read())
            tmp_file_path = tmp_file.name

        # Open the video file using cv2.VideoCapture
        vs = cv2.VideoCapture(tmp_file_path)

        # Initialize variables for output video and frame with detected violence
        writer = None
        frame_with_violence = None
        (W, H) = (None, None)
        true_count = 0
        
        image_saved = 0
        file_name = 'savedImage.jpg'
        my_image = 'finalImage.jpg'
        face_image = 'faces.jpg'
        send_alert = 0
        location = "ENSAJ"
        
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

            # clone the output frame
            output = frame.copy()
            
            # Preprocess frame for prediction
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # frame = cv2.resize(frame_rgb, (128, 128)).astype("float32") / 255.0
            frame = cv2.resize(frame_rgb, (128, 128)).astype("float32") 
            frame = frame.reshape(128, 128, 3) / 255


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
                writer = cv2.VideoWriter("output/v_output.avi", fourcc, 30, (W, H), True)
                
            # writer.write(frame)
            writer.write(output)
            

            # Window name in which image is displayed 
            # window_name = 'image'
    
            # Using cv2.imshow() method to Display the image 
            # cv2.imshow(window_name, output)

            # if(true_count == 60):
            if(true_count == 40):
              if(image_saved == 0):
                if(label):
                  cv2.imwrite(file_name, output)
                  image_saved = 1
                  
              if(send_alert == 0):
                timeMoment = getTime()
                imgenhance()
                # load image from file
                pixels = pyplot.imread(my_image)
                # create the detector, using default weights
                detector = MTCNN()
                # detect faces in the image
                faces = detector.detect_faces(pixels)
                # display faces on the original image
                draw_faces(my_image, faces)

                bot = telepot.Bot('7040707538:AAEwiA1SJUO05_B9qg6eU4mTCx7TlIz1fh4') ## GET YOUR OWN TELEGRAM GROUP ID AND BOT ID
                bot.sendMessage("@violence_ai_detector", f"VIOLENCE ALERT!! \nLOCATION: {location} \nTIME: {timeMoment}")
                bot.sendPhoto("@violence_ai_detector", photo=open('finalImage.jpg', 'rb'))
                bot.sendMessage("@violence_ai_detector", "FACES OBTAINED")
                bot.sendPhoto("@violence_ai_detector", photo=open('faces.jpg', 'rb'))
                
                storage.child(my_image).put(my_image)
                storage.child(face_image).put(face_image)

                url1 = storage.child(my_image).get_url(user['idToken'])
                url2 = storage.child(face_image).get_url(user['idToken'])
                
                
                data = {'date': [timeMoment.isoformat()], 'image': url1, 'faces': url2}
                
                # Push data to the database
                # db.child(location).set(data)
                db.child(location).set(data, user['idToken'])
                # db.set(data, user['idToken'])
                # db = getDB()

                # db.collection(location).add(data)

                # data = {
                #     'date': getTime().isoformat(),
                #     'video_url': 'https://example.com/video.mp4',
                #     'violence_detected': True
                # }

                # # Push data to the database with authentication
                # db.child("violence_reports").push(data, user['idToken'])
                
                sendAlert = 1
            
        # release the file pointersq
        print("[INFO] cleaning up...")
        # Release resources
        vs.release()
        writer.release()
        cv2.destroyAllWindows()
    
        # Convert frame with detected violence to JPG image
        if frame_with_violence is not None:
            _, img_encoded = cv2.imencode(".jpg", frame_with_violence)
            img_bytes = io.BytesIO(img_encoded)
            
        else:
            img_bytes = None

        # Return response
        # return {"message": "Processing completed"}

        # Return completion message and frame with detected violence as JPG image
        return StreamingResponse(io.BytesIO(img_bytes.getvalue()), media_type="image/jpeg")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    finally:
        # Delete temporary file
        if tmp_file_path is not None:
            os.unlink(tmp_file_path)
        # Delete output file if it exists
        output_file_path = "output/v_output.avi"
        if os.path.exists(output_file_path):
            os.remove(output_file_path)


def imgenhance():
  image1 = Image.open('savedImage.jpg')
  curr_bri = ImageEnhance.Sharpness(image1)
  new_bri = 1.3
  img_brightened = curr_bri.enhance(new_bri)
  im1 = img_brightened.save("bright.jpg")

  image2 = Image.open('bright.jpg')
  curr_col = ImageEnhance.Color(image2)
  new_col = 1.5
  img_col = curr_col.enhance(new_col)
  im2 = img_col.save("finalImage.jpg")


def draw_faces(filename, result_list):
    # load the image
    data = pyplot.imread(filename)
    
    # plot each face as a subplot
    for i in range(len(result_list)):
        # get coordinates
        x1, y1, width, height = result_list[i]['box']
        x2, y2 = x1 + width, y1 + height
        # define subplot 
        pyplot.subplot(1, len(result_list), i+1)
        pyplot.axis('off')
        # plot face
        pyplot.imshow(data[y1:y2, x1:x2])
    
    # show the plot
    pyplot.savefig("faces.jpg")
    # pyplot.show()


def getTime():
  IST = pytz.timezone('Asia/Kolkata')
  timeNow = datetime.now(IST)
  return timeNow




fireConfig = {
  "type": "service_account",
  "project_id": "violence-detection-f1b24",
  "private_key_id": "ea064f03dd4d40fc01135dfd7c98d0660f6bec75",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCVEVDF2fcgLeAd\nLLRmIjZGEdHjIbzs2NVuFrxUkqsG/a6PHBGrfnrP1l3RxuRuXrRQdpLXyCYaknd3\n9Td9IzbB0mTqdG93TNlSzkqC5WcuFXaV2C30M2ALnjspZ6sRMywQ92NDVJ01Vu7f\nr6H+dX/gx8r5APq4vLHxm6tyxPlZqk+6Eg1AI8Rl7sDmmr0PeSxdyU5E4aKQXzlR\nNoGe/SWuHU0PQj/aP8/tk05tzLSpVvtCY2GPVTrRXKw+nmAX5mZa9uiT2jSXFtDO\nwpnLi/N/TNO+CaXk3aSj9u9TMaryAXw8Oe2YS8kmMOil2QxIsbVDX89fpRGTMnlk\nHJXrKZxvAgMBAAECggEAAZzXV9yczM9SPl6OcRBrr+RfdeqWhaVu4asDTJLtoLy7\n17aBBm7u2zLBfxR8wijqIHi36/exWdY9zqFrgUIRRJWHG/Y4gnzlWPz8V2At9pSq\n3MIi9SJdJqMGltMVSbFZB7H1c/QFY19WZDsdMIiK4p6mtnzpOXhpIGkDuNEitXKb\nAd84NAk5kwUDhvsitgxD2Zjd4DyG97VLxvvlqkfWPc1EU8ibf+ljDMUb/bTX5cLT\nFrvjk9PbF6c2Knu2mHZQjgGRXI8cDLHJ+ldW8BDrH2P2R9j5nOq0V484CqegIBxz\nWMnIKgetoZPRzc5/zFosX7U4BvBPp1BpMK9QPgNt4QKBgQDH0d/HdsCbLqOvmAWl\nXELpq/cTDP0cL/olgWZdqWgLFFFnRWiC5zNE55J6XsAJwR1SheVzlexLA2aGem5R\nAssV7ZMzOC4rmeFuBv9zpjZj8qugRRo8Z7ikzAA//kONcZ3oo9gDqIhYBtAy1CBe\nZzloEiaKYIscigXRmw15Tauv0QKBgQC++od1WxsWWhrY+0vn+OhOTHZZJmporwNp\npVL5plOPt/FnCLNct4NZf/zxX0RqawibiTpL9I89QE/COH8a7zn/ytzlVbmJPYmi\nSDBz/asREAeAz4AJHya2FvLbbZptCE4bohW+rQWj8P9xtiuki+f4vozF159XBYpa\nHs/zVcHYPwKBgCnKAKzsbveFV4I/nt6oXu4TosZ/LugYOI5jc48fAL1gcG3SnDrU\nM2qzq3SgIDVqB8HcctIrhpFhkq2JKU0T8nkRiHlrxGwl8HlcSUxcdH+OnsoT6Zq8\nbmc4qsy3VlVcb5PZwDFzq6ANPLmEl4hmuiDDuv+xlSZQz0q4zKaT0dYhAoGAeGcu\nm5hyvWbVYlMcigVtQGAIhTApChK8zhBC/c4VBJjtgw4DNsMj9nswl2R+l7EfXh/o\nNxbab71qC4Le77Y/FLtrBNNFA/deHIfytE4LWdiHQniPujB/kXFqb1jscS05QUaw\n+uPOmItKIQC/ByCFgVdxHRJSDOUbUrH2XO2GJrUCgYBYkCMBcL5K0Pm+7LBc11Jk\np08nMyCf9Nu7Lvu6V5jkCQnMRkwCD3kUWoYMRYoqwf1IqeOI6h26IRPKw7LKXFda\n/6pTPPsfpc3d8z5QWk+xICfDjbcJImbyXAyDos8UnEpHDhAwNV7qeHVRMITBPG6d\nuSa5srNEJ0j3kgtYPf0knA==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-86oxx@violence-detection-f1b24.iam.gserviceaccount.com",
  "client_id": "108213921729580436779",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-86oxx%40violence-detection-f1b24.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com",
  
  "apiKey": "AIzaSyDkI9NJM9jWVmosvIc_JZa_wRRdq9izBQc",
  "authDomain": "violence-detection-f1b24.firebaseapp.com",
  "databaseURL": "https://violence-detection-f1b24-default-rtdb.firebaseio.com",
  "projectId": "violence-detection-f1b24",
  "storageBucket": "violence-detection-f1b24.appspot.com",
  "messagingSenderId": "870845449897",
  "appId": "1:870845449897:web:780c755f39f1b7186d4bb8"
}

firebaseConfig = {
  "apiKey": "AIzaSyDkI9NJM9jWVmosvIc_JZa_wRRdq9izBQc",
  "authDomain": "violence-detection-f1b24.firebaseapp.com",
  "databaseURL": "https://violence-detection-f1b24-default-rtdb.firebaseio.com",
  "projectId": "violence-detection-f1b24",
  "storageBucket": "violence-detection-f1b24.appspot.com",
  "messagingSenderId": "870845449897",
  "appId": "1:870845449897:web:780c755f39f1b7186d4bb8"
};


# cred = credentials.Certificate("firebaseKey.json")
# if not firebase_admin._apps:
# #   cred = credentials.Certificate('path/to/serviceAccountKey.json')
#   default_app = firebase_admin.initialize_app(cred)
#   db = firebase.client()
  
  

firebase = pyrebase.initialize_app(fireConfig)
storage = firebase.storage()
auth = firebase.auth()
db = firebase.database()


# firebase = firebase_admin.get_app(name='[DEFAULT]')

# def getDB():
#     cred = credentials.Certificate("firebaseKey.json") 
#     firebase = firebase_admin.initialize_app(cred)
#     db = firestore.client()
#     return db

# AUTHENTICATED GMAIL ACCOUNT & PASSWORD ONLY
email = "someone.with.id.update@emailupdate.com"
password = "thisisasimplepassword"
user = auth.sign_in_with_email_and_password(email, password)


FIREBASE_WEB_API_KEY = "AIzaSyDM8vSt3jdpAZHYX4QpO0k_UvqjkoSGfrU"
rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

# def sign_in_with_email_and_password(email: str, password: str, return_secure_token: bool = True):
#     payload = json.dumps({
#         "email": email,
#         "password": password,
#         "returnSecureToken": return_secure_token
#     })

#     r = requests.post(rest_api_url,
#                       params={"key": FIREBASE_WEB_API_KEY},
#                       data=payload)

#     return r.json()

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)