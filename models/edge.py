from flask_wtf import FlaskForm
from flask import Flask, session, request, redirect, url_for
from wtforms import TextField, SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from random import randint
import numpy as np
from cv2 import cv2 as cv2
import os
from werkzeug.utils import secure_filename

root = os.path.dirname(os.path.abspath(__file__))


class Edge(FlaskForm):
    validators = [FileRequired(message='There was no file!'),
                  FileAllowed(['png', 'jpg'], message='ທ່ານ​ຕ້ອງ​ເລືອກ​ໄຟ​ຣ png, jpg ເທົ່າ​ນັ້ນ')]
    photo = FileField('', validators=validators)

    def UploadPhoto(self, form):
        if form.validate_on_submit():
            f = form.photo.data
            filename = secure_filename(f.filename)
            ext = filename.rsplit(".", 1)[1]
            filename = str(randint(1000000000, 9999999999)) + '.' + ext
            f.save(os.path.join(root, '..', 'static', 'photos', filename))
            session['img_name_org_edge'] = filename

    def CovertCanny(self):
        img = cv2.imread(os.path.join(root, '..', 'static', 'photos', session['img_name_org_edge']))
        edges = cv2.Canny(img, 100, 200)
        filename = str(randint(1000000000, 9999999999)) + session['img_name_org_edge']
        cv2.imwrite(os.path.join(root, '..', 'static', 'photos', filename), edges)
        session['img_name_covert_edge'] = filename
        session['covert_title_edge'] = "Detection By Canny"

    def CovertSobel(self):
        img = cv2.imread(os.path.join(root, '..', 'static', 'photos', session['img_name_org_edge']))
        sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)  # x
        # sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)  # y
        filename = str(randint(1000000000, 9999999999)) + session['img_name_org_edge']
        cv2.imwrite(os.path.join(root, '..', 'static', 'photos', filename), sobelx)
        session['img_name_covert_edge'] = filename
        session['covert_title_edge'] = "Detection By Sobel"

    def CovertLaplacian(self):
        img = cv2.imread(os.path.join(root, '..', 'static', 'photos', session['img_name_org_edge']))
        laplacian = cv2.Laplacian(img, cv2.CV_64F)
        filename = str(randint(1000000000, 9999999999)) + session['img_name_org_edge']
        cv2.imwrite(os.path.join(root, '..', 'static', 'photos', filename), laplacian)
        session['img_name_covert_edge'] = filename
        session['covert_title_edge'] = "Detection By Laplacian"

    def CovertCountour(self):
        img = cv2.imread(os.path.join(root, '..', 'static', 'photos', session['img_name_org_edge']))
        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

        filename = str(randint(1000000000, 9999999999)) + session['img_name_org_edge']
        cv2.imwrite(os.path.join(root, '..', 'static', 'photos', filename), img)
        session['img_name_covert_edge'] = filename
        session['covert_title_edge'] = "Detection By Countour"
