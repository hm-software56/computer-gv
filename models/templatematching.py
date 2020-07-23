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


class Templatematching(FlaskForm):
    validators = [FileRequired(message='There was no file!'),
                  FileAllowed(['png', 'jpg'], message='ທ່ານ​ຕ້ອງ​ເລືອກ​ໄຟ​ຣ png, jpg ເທົ່າ​ນັ້ນ')]
    photo = FileField('', validators=validators)

    def UploadPhotoTemplate(self, form):
        if form.validate_on_submit():
            f = form.photo.data
            filename = secure_filename(f.filename)
            ext = filename.rsplit(".", 1)[1]
            filename = str(randint(1000000000, 9999999999)) + '.' + ext
            f.save(os.path.join(root, '..', 'static', 'photos', filename))
            session['template_img'] = filename
            self.matching()

    def UploadPhotoMatching(self, form):
        if form.validate_on_submit():
            f = form.photo.data
            filename = secure_filename(f.filename)
            ext = filename.rsplit(".", 1)[1]
            filename = str(randint(1000000000, 9999999999)) + '.' + ext
            f.save(os.path.join(root, '..', 'static', 'photos', filename))
            session['matching_img'] = filename
            self.matching()

    def matching(self):
        img_rgb = cv2.imread(os.path.join(root, '..', 'static', 'photos', session['matching_img']))
        for name in session['dataset_img']:
            try:

                print(name)
                img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
                template = cv2.imread(os.path.join(root, '..', 'static', 'dataset', name), 0)
                w, h = template.shape[::-1]

                res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
                threshold = 0.8
                loc = np.where(res >= threshold)
                for pt in zip(*loc[::-1]):
                    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 1)
                filename = str(randint(1000000000, 9999999999)) + session['matching_img']
                cv2.imwrite(os.path.join(root, '..', 'static', 'photos', filename), img_rgb)
                session['matched_img'] = filename
            except:
                print('Not has file')
