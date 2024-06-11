import numpy as np
import argparse
import pickle
import cv2
# from google.colab.patches import cv2_imshow
import os
import time
from keras.models import load_model
from collections import deque
# from firebase_admin import credentials, firestore, storage, auth

# cap = cv2.VideoCapture(0)

def detectViolence(video, limit=None):
        trueCount = 0
        imageSaved = 0
        filename = 'savedImage.jpg'
        my_image = 'finalImage.jpg'
        face_image = 'faces.png'
        sendAlert = 0

        print("Loading model ...")
        model = load_model('modelnew2.h5')
        Q = deque(maxlen=128)
        vs = cv2.VideoCapture(video)
        # vs = cap
        
        writer = None
        (W, H) = (None, None)
        count = 0
        while True:
            (grabbed, frame) = vs.read()


            if not grabbed:
                break

            # if the frame dimensions are empty, grab them
            if W is None or H is None:
                (H, W) = frame.shape[:2]

            # clone the output frame, then convert it from BGR to RGB
            # ordering, resize the frame to a fixed 128x128, and then
            # perform mean subtraction


            output = frame.copy()

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (128, 128)).astype("float32")
            frame = frame.reshape(128, 128, 3) / 255

            # make predictions on the frame and then update the predictions
            # queue
            preds = model.predict(np.expand_dims(frame, axis=0))[0]
#             print("preds",preds)
            Q.append(preds)

            # perform prediction averaging over the current history of
            # previous predictions
            results = np.array(Q).mean(axis=0)
            i = (preds > 0.50)[0]
            label = i

            text_color = (0, 255, 0) # default : green

            if label: # Violence prob
                text_color = (0, 0, 255) # red
                trueCount = trueCount + 1

            else:
                text_color = (0, 255, 0)

            text = "Violence: {}".format(label)
            FONT = cv2.FONT_HERSHEY_SIMPLEX

            cv2.putText(output, text, (35, 50), FONT,1.25, text_color, 3)

            # check if the video writer is None
            if writer is None:
                # initialize our video writer
                fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                writer = cv2.VideoWriter("recordedVideo.avi", fourcc, 30,(W, H), True)

            # write the output frame to disk
            writer.write(output)

            # show the output image
            # cv2_imshow(output)

            # Window name in which image is displayed 
            window_name = 'image'
    
            # Using cv2.imshow() method to Display the image 
            cv2.imshow(window_name, output)

            # if(trueCount == 40):
            if(trueCount == 60):
              if(imageSaved == 0):
                if(label):
                  cv2.imwrite(filename, output)
                  imageSaved = 1

              if(sendAlert == 0):
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

                sendAlert = 1

            key = cv2.waitKey(1) & 0xFF

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break
        # release the file pointersq
        print("[INFO] cleaning up...")
        writer.release()
        vs.release()