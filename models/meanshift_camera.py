from flask import Flask, session, request
import cv2
import threading
import os
import datetime, time
from pathlib import Path
from random import randint
from werkzeug.utils import secure_filename
import numpy as np

root = os.path.dirname(os.path.abspath(__file__))
thread = None


class Camera:
    def __init__(self, fps=20, video_source=1):
        self.video = cv2.VideoCapture(video_source)
        self.r, self.h, self.c, self.w = 200, 100, 300, 100
        self.track_window = (self.c, self.r, self.w, self.h)

    def get_frame(self, bytes=True):
        ret, frame = self.video.read()

        # set up the ROI for tracking
        roi = frame[self.r:self.r + self.h, self.c:self.c + self.w]
        hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
        roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
        cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

        # Setup the termination criteria, either 10 iteration or move by at least 1 pt
        term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
        if ret == True:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

            # apply meanshift to get the new location
            ret, self.track_window = cv2.meanShift(dst, self.track_window, term_crit)

            # Draw it on image
            x, y, w, h = self.track_window
            img2 = cv2.rectangle(frame, (x, y), (x + w, y + h), 255, 2)
        ret, jpeg = cv2.imencode('.jpg', img2)

        return jpeg.tobytes()
