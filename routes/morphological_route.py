from flask import Flask, render_template, request, Response, redirect, url_for, session, Blueprint, send_from_directory
import os
from models.morphological import Morphological

morphological_route = Blueprint('morphological_route', __name__)
root = os.path.dirname(os.path.abspath(__file__))


@morphological_route.after_request
def add_header(convert):
    convert.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    convert.headers["Pragma"] = "no-cache"
    convert.headers["Expires"] = "0"
    convert.headers["Cache-Control"] = "public, max-age=0"
    return convert


@morphological_route.route("/morphological", methods=['GET', 'POST'])
def morphological():
    # session.clear()
    form = Morphological()
    form.UploadPhoto(form)
    return render_template("/morphological.html", form=form)


@morphological_route.route("/convert", methods=['GET', 'POST'])
def convert():
    form = Morphological()
    if request.args.get('w') and request.args.get('h'):
        w = int(request.args.get('w'))
        h = int(request.args.get('h'))
    else:
        w = 3
        h = 3
    if request.args.get('action') and request.args.get('action') == 'dilation':
        form.CovertDilation(w, h)
    elif request.args.get('action') and request.args.get('action') == 'erosion':
        form.CovertErosion(w, h)
    elif request.args.get('action') and request.args.get('action') == 'opening':
        form.CovertOpening(w, h)
    elif request.args.get('action') and request.args.get('action') == 'closing':
        form.CovertClosing(w, h)
    elif request.args.get('action') and request.args.get('action') == 'gradient':
        form.CovertGradient(w, h)
    elif request.args.get('action') and request.args.get('action') == 'tophat':
        form.CovertTophat(w, h)
    elif request.args.get('action') and request.args.get('action') == 'blackhat':
        form.CovertBlackhat(w, h)
    elif request.args.get('action') and request.args.get('action') == 'dilation_binary':
        form.CovertDilationBinary(w, h)
    elif request.args.get('action') and request.args.get('action') == 'erosion_binary':
        form.CovertErosionBinary(w, h)

    return render_template("/morphological.html", form=form)
