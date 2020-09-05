from flask import Flask, render_template, request, Response, redirect, url_for, session, Blueprint, send_from_directory
from models.meanshift_camera import Camera

meanshift_route = Blueprint('meanshift_route', __name__)
camera = Camera()
@meanshift_route.route("/meanshift")
def meanshift():
    return render_template("meanshift_video.html")


@meanshift_route.route("/meanshift_video")
def meanshift_video():
    return Response(gen(camera),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')
