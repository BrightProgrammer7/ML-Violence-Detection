import matplotlib.pyplot as plt
#WORKING PROJECT
import numpy as np
import argparse
import cv2
from cv2 import imshow
import os
import time
from keras.models import load_model
from collections import deque

# cap = cv2.VideoCapture(0)

def print_results(video, limit=None):
        #fig=plt.figure(figsize=(16, 30))
        if not os.path.exists('output'):
            os.mkdir('output')

        print("Loading model ...")
        model = load_model('modelnew.h5')
        Q = deque(maxlen=128)
        vs = cv2.VideoCapture(video)
        # vs = cap
        writer = None
        (W, H) = (None, None)
        count = 0
        writer = None  # Initialize writer outside the loop

        while True:
            # read the next frame from the file
            (grabbed, frame) = vs.read()

            # if the frame was not grabbed, then we have reached the end
            # of the stream
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

            cv2.putText(output, text, (35, 50), FONT, 1.25, text_color, 3)

            # check if the video writer is None and initialize it
            if writer is None:
                fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                writer = cv2.VideoWriter("output/v_output.avi", fourcc, 30, (W, H), True)

            # write the output frame to disk
            writer.write(output)

        # release the file pointers outside the loop
        print("[INFO] cleaning up...")
        if writer is not None:
            writer.release()

        vs.release()

