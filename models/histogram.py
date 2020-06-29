from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
import numpy as np
# from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
# plt.switch_backend('TKAgg')
from random import randint
from markupsafe import Markup
import numpy as np
from cv2 import cv2


class Histogram(FlaskForm):
    validators = [FileRequired(message='There was no file!'),
                  FileAllowed(['png', 'jpg'], message='ທ່ານ​ຕ້ອງ​ເລືອກ​ໄຟ​ຣ png, jpg ເທົ່າ​ນັ້ນ')]
    save = SubmitField('Save')
    photo = FileField('', validators=validators)

    def covertoimg(self, path, img_name, list):
        img = cv2.imread(path + img_name, 1)
        """gray = cv2.cvtColor(img, cv2.COLOR_)
        f_name = str(randint(1000000000, 9999999999)) + img_name
        cv2.imwrite(path + f_name, gray)"""

        green_channel = img[:, :, int(list)]
        green_img = np.zeros(img.shape)
        green_img[:, :, int(list)] = green_channel
        f_name = str(randint(1000000000, 9999999999)) + img_name
        cv2.imwrite(path + f_name, green_img)
        return f_name

    def htg(self, path, filename, action):
        img = cv2.imread(path + filename)
        if (int(action) < 3):
            if (int(action) == 0):
                colcor = "blue"
            elif (int(action) == 1):
                colcor = "green"
            else:
                colcor = "red"
            histr = cv2.calcHist([img], [int(action)], None, [256], [0, 256])
            plt.plot(histr, color=colcor)
            plt.xlim([0, 256])
        else:
            color = ('b', 'g', 'r')
            for i, col in enumerate(color):
                print(i)
                histr = cv2.calcHist([img], [i], None, [256], [0, 256])
                plt.plot(histr, color=col)
                plt.xlim([0, 256])
        f_name = str(randint(1000000000, 9999999999)) + '.png'
        plt.savefig(path + '/' + f_name)
        plt.close()
        return f_name
