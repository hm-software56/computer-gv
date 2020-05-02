from flask_wtf import Form
from wtforms import TextField,SubmitField
from flask_wtf.file import FileField, FileRequired,FileAllowed
from markupsafe import Markup
import numpy as np
from cv2 import cv2
import os
#from flask_uploads import UploadSet, IMAGES
#images = UploadSet('images', IMAGES)
class GrayImg(Form):
   validators = [FileRequired(message='There was no file!'),
                  FileAllowed(['png', 'jpg'], message='ທ່ານ​ຕ້ອງ​ເລືອກ​ໄຟ​ຣ png, jpg ເທົ່າ​ນັ້ນ')]
   save = SubmitField('Save')
   photo=FileField('',validators=validators)

   def covertogray(self,path,img_name):
    img = cv2.imread(path+img_name,1)
    print(cv2.COLOR_RGB2GRAY)
    gray1 = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    #gray2 = cv2.cvtColor(img, cv2.COLOR_RGB2YCR_CB)
    cv2.imwrite(path+'_1'+img_name,gray1)
    #cv2.imwrite(path+'_2'+img_name,gray2)
    green_channel = img[:,:,1]
   # create empty image with same shape as that of src image
    green_img = np.zeros(img.shape)
   #assign the green channel of src to empty image
    green_img[:,:,1] = green_channel
   #save image
    cv2.imwrite(path+'_2'+img_name,green_img)