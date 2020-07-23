from flask import Flask, render_template, request, Response, redirect, url_for, session, Blueprint, send_from_directory
import os
from models.templatematching import Templatematching
from PIL import Image
from cv2 import cv2 as cv2
from random import randint

templatematching_route = Blueprint('templatematching_route', __name__)
root = os.path.dirname(os.path.abspath(__file__))


@templatematching_route.route("/cleantemplate", methods=['GET', 'POST'])
def cleantemplate():
    session.clear()
    return redirect(url_for('templatematching_route.template_matching'))


@templatematching_route.route("/template-matching", methods=['GET', 'POST'])
def template_matching():
    form = Templatematching()
    try:
        form.UploadPhotoTemplate(form)
    except:
        print("Error upload template")
    return render_template("/template_matching.html", form=form)


@templatematching_route.route("/matching", methods=['GET', 'POST'])
def matching():
    form = Templatematching()
    try:
        form.UploadPhotoMatching(form)
    except:
        print('error upload matching')
    session['template_img'] = ''
    return render_template("/template_matching.html", form=form)


@templatematching_route.route("/cropper-img", methods=['GET', 'POST'])
def cropper_img():
    if request.form.get('x'):
        x = int(request.form.get('x'))
        y = int(request.form.get('y'))
        w = int(request.form.get('w'))
        h = int(request.form.get('h'))
        img = cv2.imread(os.path.join(root, '..', 'static', 'photos', session['template_img']))
        crop_img = img[y:y + h, x:x + w]
        filename = str(randint(1000000000, 9999999999)) + session['template_img']
        cv2.imwrite(os.path.join(root, '..', 'static', 'dataset', filename), crop_img)
        all_file = os.listdir(os.path.join(root, '..', 'static', 'dataset'))
        session['dataset_img'] = all_file
        session['template_img'] = ''
        try:
            Templatematching().matching()
        except:
            print('Not image matching')
    return redirect(url_for('templatematching_route.template_matching'))
