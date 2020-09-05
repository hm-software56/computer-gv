from flask import Flask, render_template, request, Response, redirect, url_for, session, Blueprint, send_from_directory
import os
from models.corners import Corners

corners_route = Blueprint('corners_route', __name__)
root = os.path.dirname(os.path.abspath(__file__))


@corners_route.route("/cornerharris", methods=['GET', 'POST'])
def corner_harris():
    form = Corners()
    try:
        form.UploadImg(form)
    except:
        print("Error upload template")
    if request.args.get('action'):
        action = request.args.get('action')
        try:
            if action == "sift":
                form.SIFT()
            elif action == "corners":
                form.cornerHarris()
            elif action == "surf":
                form.SURF()
            elif action == "orb":
                form.ORB()
            elif action == "fast":
                form.FAST()
        except:
            print('errors')
    return render_template("/cornerharris.html", form=form)
