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


class Morphological(FlaskForm):
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
            session['img_name_org'] = filename

    def CovertDilation(self, w, h):
        img = cv2.imread(os.path.join(root, '..', 'static', 'photos', session['img_name_org']))
        kernel = np.ones((w, w), np.uint8)
        dilation = cv2.dilate(img, kernel, iterations=1)
        filename = str(randint(1000000000, 9999999999)) + session['img_name_org']
        cv2.imwrite(os.path.join(root, '..', 'static', 'photos', filename), dilation)
        session['img_name_covert'] = filename
        session['w'] = w
        session['h'] = h
        session['covert_title'] = "Dilation (" + str(w) + " X " + str(h) + ")"

    def CovertErosion(self, w, h):
        img = cv2.imread(os.path.join(root, '..', 'static', 'photos', session['img_name_org']))
        kernel = np.ones((w, w), np.uint8)
        erosion = cv2.erode(img, kernel, iterations=1)
        filename = str(randint(1000000000, 9999999999)) + session['img_name_org']
        cv2.imwrite(os.path.join(root, '..', 'static', 'photos', filename), erosion)
        session['img_name_covert'] = filename
        session['w'] = w
        session['h'] = h
        session['covert_title'] = "Erosion (" + str(w) + " X " + str(h) + ")"

    def CovertOpening(self, w, h):
        img = cv2.imread(os.path.join(root, '..', 'static', 'photos', session['img_name_org']))
        kernel = np.ones((w, w), np.uint8)
        opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        filename = str(randint(1000000000, 9999999999)) + session['img_name_org']
        cv2.imwrite(os.path.join(root, '..', 'static', 'photos', filename), opening)
        session['img_name_covert'] = filename
        session['w'] = w
        session['h'] = h
        session['covert_title'] = "Opening (" + str(w) + " X " + str(h) + ")"

    def CovertClosing(self, w, h):
        img = cv2.imread(os.path.join(root, '..', 'static', 'photos', session['img_name_org']))
        kernel = np.ones((w, w), np.uint8)
        closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        filename = str(randint(1000000000, 9999999999)) + session['img_name_org']
        cv2.imwrite(os.path.join(root, '..', 'static', 'photos', filename), closing)
        session['img_name_covert'] = filename
        session['w'] = w
        session['h'] = h
        session['covert_title'] = "Closing (" + str(w) + " X " + str(h) + ")"

    def CovertGradient(self, w, h):
        img = cv2.imread(os.path.join(root, '..', 'static', 'photos', session['img_name_org']))
        kernel = np.ones((w, w), np.uint8)
        gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)
        filename = str(randint(1000000000, 9999999999)) + session['img_name_org']
        cv2.imwrite(os.path.join(root, '..', 'static', 'photos', filename), gradient)
        session['img_name_covert'] = filename
        session['w'] = w
        session['h'] = h
        session['covert_title'] = "Gradient (" + str(w) + " X " + str(h) + ")"

    def CovertTophat(self, w, h):
        img = cv2.imread(os.path.join(root, '..', 'static', 'photos', session['img_name_org']))
        kernel = np.ones((w, w), np.uint8)
        tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
        filename = str(randint(1000000000, 9999999999)) + session['img_name_org']
        cv2.imwrite(os.path.join(root, '..', 'static', 'photos', filename), tophat)
        session['img_name_covert'] = filename
        session['w'] = w
        session['h'] = h
        session['covert_title'] = "Top Hat (" + str(w) + " X " + str(h) + ")"

    def CovertBlackhat(self, w, h):
        img = cv2.imread(os.path.join(root, '..', 'static', 'photos', session['img_name_org']))
        kernel = np.ones((w, w), np.uint8)
        blackhat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)
        filename = str(randint(1000000000, 9999999999)) + session['img_name_org']
        cv2.imwrite(os.path.join(root, '..', 'static', 'photos', filename), blackhat)
        session['img_name_covert'] = filename
        session['w'] = w
        session['h'] = h
        session['covert_title'] = "Black Hat (" + str(w) + " X " + str(h) + ")"

    def CovertDilationBinary(self, w, h):
        img = cv2.imread(os.path.join(root, '..', 'static', 'photos', session['img_name_org']))
        kernel = np.ones((w, w), np.uint8)
        ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        dilation_binary = cv2.dilate(thresh, kernel, iterations=1)
        filename = str(randint(1000000000, 9999999999)) + session['img_name_org']
        cv2.imwrite(os.path.join(root, '..', 'static', 'photos', filename), dilation_binary)
        session['img_name_covert'] = filename
        session['w'] = w
        session['h'] = h
        session['covert_title'] = "Dilation Binary (" + str(w) + " X " + str(h) + ")"

    def CovertErosionBinary(self, w, h):
        img = cv2.imread(os.path.join(root, '..', 'static', 'photos', session['img_name_org']))
        kernel = np.ones((w, w), np.uint8)
        ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        erosion_binary = cv2.erode(thresh, kernel, iterations=1)
        filename = str(randint(1000000000, 9999999999)) + session['img_name_org']
        cv2.imwrite(os.path.join(root, '..', 'static', 'photos', filename), erosion_binary)
        session['img_name_covert'] = filename
        session['w'] = w
        session['h'] = h
        session['covert_title'] = "Erosion Binary (" + str(w) + " X " + str(h) + ")"
