from flask import Flask, session, request
import cv2
import threading
import os
import datetime, time
from pathlib import Path
from random import randint
from werkzeug.utils import secure_filename

root = os.path.dirname(os.path.abspath(__file__))
thread = None


class Camera:
    def __init__(self, fps=20, video_source=0):
        self.fps = fps
        self.video_source = video_source
        self.camera = None
        self.fource = None
        self.out = None
        # We want a max of 5s history to be stored, thats 5s*fps
        self.max_frames = 5 * self.fps
        self.frames = []
        self.isrunning = False
        self.action = 'normal'

    def run(self, start):
        global thread
        if thread is None or start == True:
            self.camera = cv2.VideoCapture(self.video_source)
            # self.fource = cv2.VideoWriter_fourcc(*'XVID')
            # frame_width = int(self.camera.get(3))
            # frame_height = int(self.camera.get(4))
            # self.out = cv2.VideoWriter(os.path.join(root, '..', 'static', 'output.avi'), self.fource, 20.0,
            #                           (frame_width, frame_height))

            thread = threading.Thread(target=self._capture_loop)
            print("Starting thread...")
            thread.start()
            self.isrunning = True
        else:
            print(thread)

    def _capture_loop(self):
        dt = 1 / self.fps
        print("Observing...")
        while self.isrunning:
            v, im = self.camera.read()
            if v:
                if len(self.frames) == self.max_frames:
                    self.frames = self.frames[1:]
                if self.action == "gray":
                    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                elif self.action == "binary":
                    gray_frame = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    ret, im = cv2.threshold(gray_frame, 127, 255, cv2.THRESH_BINARY)
                # self.out.write(im)
                self.frames.append(im)
            time.sleep(dt)
        self.out.release()

    def stop(self):
        self.isrunning = False

    def get_frame(self, bytes=True):
        if len(self.frames) > 0:
            if bytes:
                img = cv2.imencode('.png', self.frames[-1])[1].tobytes()
            else:
                img = self.frames[-1]
        else:
            with open(os.path.join(root, '..', 'static', 'default', 'no-camera.jpg'), "rb") as f:
                img = f.read()
        return img

    def gen(self, camera):
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')

    def capture_and_save(self, im):
        s = im.shape
        # Add a timestamp
        font = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (10, s[0] - 10)
        fontScale = 1
        fontColor = (20, 20, 20)
        lineType = 2

        cv2.putText(im, datetime.datetime.now().isoformat().split(".")[0], bottomLeftCornerOfText, font, fontScale,
                    fontColor, lineType)

        m = 0
        p = Path(os.path.join(root, '..', 'static', 'camera'))
        for imp in p.iterdir():
            if imp.suffix == ".png" and imp.stem != "last":
                num = imp.stem.split("_")[1]
                try:
                    num = int(num)
                    if num > m:
                        m = num
                except:
                    print("Error reading image number for", str(imp))
        m += 1
        lp = Path(os.path.join(root, '..', 'static', 'camera', "last.png"))
        if lp.exists() and lp.is_file():
            np = Path(os.path.join(root, '..', 'static', 'camera', "img_{}.png".format(m)))
            np.write_bytes(lp.read_bytes())
        cv2.imwrite(os.path.join(root, '..', 'static', 'camera', 'last.png'), im)

    def camera_gray(self):
        self.action = 'gray'

    def camera_binaries(self):
        self.action = 'binary'

    def camera_normal(self):
        self.action = 'normal'
