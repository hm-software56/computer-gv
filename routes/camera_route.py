from flask import Flask, render_template, request, Response, redirect, url_for, session, Blueprint, send_from_directory
from models.camera import Camera
from pathlib import Path
import os

camera_route = Blueprint('camera_route', __name__)
camera = Camera()
root = os.path.dirname(os.path.abspath(__file__))


@camera_route.after_request
def add_header(capture):
    capture.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    capture.headers["Pragma"] = "no-cache"
    capture.headers["Expires"] = "0"
    capture.headers["Cache-Control"] = "public, max-age=0"
    return capture


@camera_route.route("/camera_normal")
def camera_normal():
    camera.camera_normal()
    return redirect(url_for('camera_route.stream_page'))


@camera_route.route("/camera_gray")
def camera_gray():
    camera.camera_gray()
    return redirect(url_for('camera_route.stream_page'))


@camera_route.route("/camera_binary")
def camera_binary():
    camera.camera_binaries()
    return redirect(url_for('camera_route.stream_page'))


@camera_route.route("/open")
def opencamera():
    camera.run(True)
    return redirect(url_for('camera_route.stream_page'))


@camera_route.route("/close")
def closecamera():
    camera.stop()
    camera.__init__()
    return redirect(url_for('camera_route.stream_page'))


@camera_route.route("/capture")
def capture():
    try:
        im = camera.get_frame(bytes=False)
        camera.capture_and_save(im)
    except:
        print('should start camera first')
    return redirect(url_for('camera_route.stream_page'))


@camera_route.route("/images/last")
def last_image():
    p = Path(os.path.join(root, '..', 'static', 'camera', 'last.png'))
    if p.exists():
        r = "last.png"
    else:
        print("No last")
        r = "not_found.jpeg"
    return send_from_directory(os.path.join('static', 'camera'), r)


@camera_route.route("/stream")
def stream_page():
    return render_template("/video.html", isrunung=camera.isrunning)


@camera_route.route("/video_feed")
def video_feed():
    return Response(gen(camera),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')
