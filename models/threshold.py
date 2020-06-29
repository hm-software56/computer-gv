from flask_wtf import FlaskForm
from flask import Flask, session, request, redirect, url_for
from wtforms import TextField, SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from random import randint
import numpy as np
from cv2 import cv2 as cv2
import os
from werkzeug.utils import secure_filename


class Threshold(FlaskForm):
    validators = [FileRequired(message='There was no file!'),
                  FileAllowed(['png', 'jpg'], message='ທ່ານ​ຕ້ອງ​ເລືອກ​ໄຟ​ຣ png, jpg ເທົ່າ​ນັ້ນ')]
    save = SubmitField('Save')
    photo = FileField('', validators=validators)

    def covertoGray(self, path):
        img = cv2.imread(path + session['file_name'], 1)
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        f_name = str(randint(1000000000, 9999999999)) + session['file_name']
        cv2.imwrite(path + f_name, gray)
        return f_name

    def covertoThresh(self, path):
        self.removesessionAdt()
        try:
            img = cv2.imread(path + session['file_name'])
            grayscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            retval1, threshold = cv2.threshold(grayscaled, int(session['thd_value']), int(session['max']),
                                               self.threshold())
            f_name = str(randint(1000000000, 9999999999)) + session['file_name']
            cv2.imwrite(path + f_name, threshold)
            return f_name
        except:
            return None

    def covertoAdaptiveThresh(self, path):
        try:
            img = cv2.imread(path + session['file_name'])
            grayscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            adaptivethreshold = cv2.adaptiveThreshold(grayscaled, int(session['max']), self.adaptiveThresh(),
                                                      self.threshold(),
                                                      int(session['bs']), int(session['pr']))
            f_name = str(randint(1000000000, 9999999999)) + session['file_name']
            cv2.imwrite(path + f_name, adaptivethreshold)
            return f_name
        except:
            return None

    def adaptiveThresh(self):
        if session['adt_type'] == "ADAPTIVE_THRESH_MEAN_C":
            adthd = cv2.ADAPTIVE_THRESH_MEAN_C
        elif session['adt_type'] == "ADAPTIVE_THRESH_GAUSSIAN_C":
            adthd = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
        return adthd

    def threshold(self):
        if session['thd_type'] == "THRESH_BINARY":
            thd = cv2.THRESH_BINARY
        elif session['thd_type'] == "THRESH_BINARY_INV":
            thd = cv2.THRESH_BINARY_INV
        elif session['thd_type'] == "THRESH_TRUNC":
            thd = cv2.THRESH_TRUNC
        elif session['thd_type'] == "THRESH_TOZERO":
            thd = cv2.THRESH_TOZERO
        elif session['thd_type'] == "THRESH_TOZERO_INV":
            thd = cv2.THRESH_TOZERO_INV
        return thd

    def defaultvalue(self):
        if session['thd_type'] == "THRESH_BINARY":
            session['max'] = 255
            session['thd_value'] = 150
        elif session['thd_type'] == "THRESH_BINARY_INV":
            session['max'] = 150
            session['thd_value'] = 100
        elif session['thd_type'] == "THRESH_TRUNC":
            session['max'] = 255
            session['thd_value'] = 255
        elif session['thd_type'] == "THRESH_TOZERO":
            session['max'] = 255
            session['thd_value'] = 0
        elif session['thd_type'] == "THRESH_TOZERO_INV":
            session['max'] = 255
            session['thd_value'] = 255

    def defaultvalueAdt(self):
        if session['adt_type'] == "ADAPTIVE_THRESH_GAUSSIAN_C":
            session['bs'] = 3
            session['pr'] = 11
        elif session['adt_type'] == "ADAPTIVE_THRESH_MEAN_C":
            session['bs'] = 3
            session['pr'] = 11

    def removesessionAdt(self):
        session['adt_type'] = ''
        session['bs'] = ''
        session['pr'] = ''

    def removesessionAll(self):
        session.clear()

    def actionSummit(self, form, app):
        if form.validate_on_submit():
            self.removesessionAll()
            f = form.photo.data
            filename = secure_filename(f.filename)
            ext = filename.rsplit(".", 1)[1]
            filename = str(randint(1000000000, 9999999999)) + '.' + ext
            f.save(os.path.join(app.static_folder, 'photos', filename))
            session['file_name'] = filename
            session['file_name_gray'] = form.covertoGray(os.path.join(app.static_folder, 'photos/'))

    def AllAction(self, form, app):
        if request.args.get('thd_type'):
            session['thd_type'] = request.args.get('thd_type')
            form.defaultvalue()
            session['file_name_thd'] = form.covertoThresh(os.path.join(app.static_folder, 'photos/'))
        elif request.args.get('thd_value'):
            session['thd_value'] = request.args.get('thd_value')
            session['file_name_thd'] = form.covertoThresh(os.path.join(app.static_folder, 'photos/'))
        elif request.args.get('max'):
            session['max'] = request.args.get('max')
            session['file_name_thd'] = form.covertoThresh(os.path.join(app.static_folder, 'photos/'))
        elif request.args.get('bs'):
            if int(request.args.get('bs')) % 2 == 0:
                session['bs'] = int(request.args.get('bs')) + 1
            else:
                session['bs'] = int(request.args.get('bs'))
            session['file_name_thd'] = form.covertoAdaptiveThresh(os.path.join(app.static_folder, 'photos/'))
        elif request.args.get('adt'):
            session['adt_type'] = request.args.get('adt')
            form.defaultvalueAdt()
            session['file_name_thd'] = form.covertoAdaptiveThresh(os.path.join(app.static_folder, 'photos/'))
        elif request.args.get('pr'):
            session['pr'] = int(request.args.get('pr'))
            session['file_name_thd'] = form.covertoAdaptiveThresh(os.path.join(app.static_folder, 'photos/'))
