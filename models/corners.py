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


class Corners(FlaskForm):
    validators = [FileRequired(message='There was no file!'),
                  FileAllowed(['png', 'jpg'], message='ທ່ານ​ຕ້ອງ​ເລືອກ​ໄຟ​ຣ png, jpg ເທົ່າ​ນັ້ນ')]
    photo = FileField('', validators=validators)

    def UploadImg(self, form):
        if form.validate_on_submit():
            f = form.photo.data
            filename = secure_filename(f.filename)
            ext = filename.rsplit(".", 1)[1]
            filename = str(randint(1000000000, 9999999999)) + '.' + ext
            f.save(os.path.join(root, '..', 'static', 'photos', filename))
            session['org_img'] = filename

    def cornerHarris(self):
        img = cv2.imread(os.path.join(root, '..', 'static', 'photos', session['org_img']))
        img = np.float32(img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        gray = np.float32(gray)
        dst = cv2.cornerHarris(gray, 2, 5, 0.07)

        # result is dilated for marking the corners, not important
        dst = cv2.dilate(dst, None)

        # Threshold for an optimal value, it may vary depending on the image.
        img[dst > 0.01 * dst.max()] = [0, 0, 255]
        filename = str(randint(1000000000, 9999999999)) + session['org_img']
        cv2.imwrite(os.path.join(root, '..', 'static', 'photos', filename), img)
        session['corner_img'] = filename

    def SIFT(self):
        img = cv2.imread(os.path.join(root, '..', 'static', 'photos', session['org_img']))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        sift = cv2.xfeatures2d.SIFT_create()
        kp = sift.detect(gray, None)

        img = cv2.drawKeypoints(gray, kp, img)
        print(img)
        filename = str(randint(1000000000, 9999999999)) + session['org_img']
        cv2.imwrite(os.path.join(root, '..', 'static', 'photos', filename), img)
        session['corner_img'] = filename

    def SURF(self):
        img = cv2.imread(os.path.join(root, '..', 'static', 'photos', session['org_img']))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        surf = cv2.xfeatures2d.SURF_create()
        kp = surf.detect(gray, None)
        img = cv2.drawKeypoints(gray, kp, img)
        filename = str(randint(1000000000, 9999999999)) + session['org_img']
        cv2.imwrite(os.path.join(root, '..', 'static', 'photos', filename), img)
        session['corner_img'] = filename

    def ORB(self):
        img = cv2.imread(os.path.join(root, '..', 'static', 'photos', session['org_img']))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        orb = cv2.ORB_create(nfeatures=1500)
        kp = orb.detect(gray, None)
        img = cv2.drawKeypoints(gray, kp, img)
        filename = str(randint(1000000000, 9999999999)) + session['org_img']
        cv2.imwrite(os.path.join(root, '..', 'static', 'photos', filename), img)
        session['corner_img'] = filename

    def FAST(self):
        img = cv2.imread(os.path.join(root, '..', 'static', 'photos', session['org_img']))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        fast = cv2.FastFeatureDetector_create(threshold=25)
        # find and draw the keypoints
        kp = fast.detect(gray, None)
        gray = cv2.drawKeypoints(gray, kp, None, color=(255, 0, 0))
        filename = str(randint(1000000000, 9999999999)) + session['org_img']
        cv2.imwrite(os.path.join(root, '..', 'static', 'photos', filename), gray)
        session['corner_img'] = filename
