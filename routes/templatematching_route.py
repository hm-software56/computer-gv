from flask import Flask, render_template, request, Response, redirect, url_for, session, Blueprint, send_from_directory
import os
from models.edge import Edge

edge_route = Blueprint('edge_route', __name__)
root = os.path.dirname(os.path.abspath(__file__))


@edge_route.after_request
def add_header(convert):
    convert.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    convert.headers["Pragma"] = "no-cache"
    convert.headers["Expires"] = "0"
    convert.headers["Cache-Control"] = "public, max-age=0"
    return convert


@edge_route.route("/cleanedge", methods=['GET', 'POST'])
def cleanedge():
    session.clear()
    return redirect(url_for('edge_route.edge'))


@edge_route.route("/edge", methods=['GET', 'POST'])
def edge():
    form = Edge()
    form.UploadPhoto(form)
    return render_template("/edge.html", form=form)


@edge_route.route("/edge-detection", methods=['GET', 'POST'])
def convert():
    form = Edge()
    try:
        if request.args.get('action') and request.args.get('action') == 'canny':
            form.CovertCanny()
        elif request.args.get('action') and request.args.get('action') == 'sobel':
            form.CovertSobel()
        elif request.args.get('action') and request.args.get('action') == 'laplacian':
            form.CovertLaplacian()
        elif request.args.get('action') and request.args.get('action') == 'countour':
            form.CovertCountour()
    except:
        return redirect(url_for('edge_route.edge'))

    return render_template("/edge.html", form=form)
