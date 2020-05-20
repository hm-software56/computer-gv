from flask_wtf import Form
from flask import Flask, session, request, redirect, url_for
from wtforms import TextField, SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from random import randint
import numpy as np
from cv2 import cv2 as cv2
import os
from werkzeug.utils import secure_filename
from matplotlib import pyplot as plt


class Equalization(Form):
    validators = [FileRequired(message='There was no file!'),
                  FileAllowed(['png', 'jpg'], message='ທ່ານ​ຕ້ອງ​ເລືອກ​ໄຟ​ຣ png, jpg ເທົ່າ​ນັ້ນ')]
    save = SubmitField('Save')
    photo = FileField('', validators=validators)

    def actionSummit(self, form, app):
        try:
            if form.validate_on_submit():
                self.removesessionAll()
                f = form.photo.data
                filename = secure_filename(f.filename)
                ext = filename.rsplit(".", 1)[1]
                filename = str(randint(1000000000, 9999999999)) + '.' + ext
                f.save(os.path.join(app.static_folder, 'photos', filename))
                session['org_name'] = filename
                session['rg_value'] = 0
                session['kz_value'] = 7
                self.equalizeHist(os.path.join(app.static_folder, 'photos/'), session['org_name'])

                session['gray_htg_gf_mf_name'] = self.covertoGray(os.path.join(app.static_folder, 'photos/'))
                session['htg_org'] = self.htgOrgGray(os.path.join(app.static_folder, 'photos/'), session['org_name'])
                session['htg_gray_htg_gf_mf'] = self.htgOrgGray(os.path.join(app.static_folder, 'photos/'),
                                                                session['gray_htg_gf_mf_name'])
                session['label_name'] = "Gray"
            else:
                if request.args.get('he'):
                    session['gray_htg_gf_mf_name'] = self.equalizeHist(os.path.join(app.static_folder, 'photos/'),
                                                                       session['org_name'])
                    session['htg_gray_htg_gf_mf'] = self.htgOrgGray(os.path.join(app.static_folder, 'photos/'),
                                                                    session['gray_htg_gf_mf_name'])
                    session['label_name'] = "Equalization"
                elif request.args.get('gf'):
                    session['gray_htg_gf_mf_name'] = self.GuassianFilter(os.path.join(app.static_folder, 'photos/'),
                                                                         session['equalize_file_name'])
                    session['htg_gray_htg_gf_mf'] = self.htgOrgGray(os.path.join(app.static_folder, 'photos/'),
                                                                    session['gray_htg_gf_mf_name'])
                    session['label_name'] = "Guassian Filter"
                elif request.args.get('mf'):
                    session['gray_htg_gf_mf_name'] = self.MedianFilter(os.path.join(app.static_folder, 'photos/'),
                                                                       session['equalize_file_name'])
                    session['htg_gray_htg_gf_mf'] = self.htgOrgGray(os.path.join(app.static_folder, 'photos/'),
                                                                    session['gray_htg_gf_mf_name'])
                    session['label_name'] = "Median Filter"
                elif request.args.get('ngmf'):
                    session['gray_htg_gf_mf_name'] = self.NoiseGMF(os.path.join(app.static_folder, 'photos/'),
                                                                   session['equalize_file_name'])
                    session['htg_gray_htg_gf_mf'] = self.htgOrgGray(os.path.join(app.static_folder, 'photos/'),
                                                                    session['gray_htg_gf_mf_name'])
                    session['label_name'] = "Noise"
                elif request.args.get('rg'):
                    session['rg_value'] = int(request.args.get('rg'))
                    self.equalizeHist(os.path.join(app.static_folder, 'photos/'), session['org_name'])
                elif request.args.get('kz'):
                    if int(request.args.get('kz')) % 2 == 0:
                        session['kz_value'] = int(request.args.get('kz')) + 1
                    else:
                        session['kz_value'] = int(request.args.get('kz'))

                    self.equalizeHist(os.path.join(app.static_folder, 'photos/'), session['org_name'])
        except:
            return None

    def covertoGray(self, path):
        try:
            img = cv2.imread(path + session['org_name'], 1)
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            f_name = str(randint(1000000000, 9999999999)) + session['org_name']
            cv2.imwrite(path + f_name, gray)
            return f_name
        except:
            return None

    def htgOrgGray(self, path, file_name):
        try:
            img = cv2.imread(path + file_name, 1)
            for i, col in enumerate(['b', 'g', 'r']):
                hist = cv2.calcHist([img], [i], None, [256], [0, 256])
                if file_name == session['gray_htg_gf_mf_name'] and session['rg_value'] == 0:
                    plt.plot(hist, color='gray')
                else:
                    plt.plot(hist, color=col)
                plt.xlim([0, 256])
            f_name = str(randint(1000000000, 9999999999)) + '.png'
            plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
            plt.savefig(path + '/' + f_name)
            plt.close()
            return f_name
        except:
            return None

    def equalizeHist(self, path, file_name):
        try:
            img = cv2.imread(path + file_name)
            if session['rg_value'] == 1:
                img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
                # equalize the histogram of the Y channel
                img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
                # convert the YUV image back to RGB format
                equ = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
            else:
                img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                equ = cv2.equalizeHist(img)
            f_name = str(randint(1000000000, 9999999999)) + session['org_name']
            session['equalize_file_name'] = f_name
            cv2.imwrite(path + f_name, equ)
            return f_name
        except:
            return None

    def GuassianFilter(self, path, file_name):
        try:
            img = cv2.imread(path + file_name, session['rg_value'])
            blur = cv2.GaussianBlur(img, (session['kz_value'], session['kz_value']), 0)
            f_name = str(randint(1000000000, 9999999999)) + session['org_name']
            cv2.imwrite(path + f_name, blur)
            return f_name
        except:
            return None

    def MedianFilter(self, path, file_name):
        try:
            img = cv2.imread(path + file_name, session['rg_value'])
            median = cv2.medianBlur(img, session['kz_value'])
            f_name = str(randint(1000000000, 9999999999)) + session['org_name']
            cv2.imwrite(path + f_name, median)
            return f_name
        except:
            return None

    def NoiseGMF(self, path, file_name):
        try:
            img = cv2.imread(path + file_name)
            gauss = cv2.GaussianBlur(img, (session['kz_value'], session['kz_value']), 0)
            median = cv2.medianBlur(img, session['kz_value'])
            images = np.concatenate((gauss, median), 1)
            f_name = str(randint(1000000000, 9999999999)) + session['org_name']
            cv2.imwrite(path + f_name, images)
            return f_name
        except:
            return None

    def removesessionAll(self):
        session.clear()
