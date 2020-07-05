import numpy as np
import cv2
from matplotlib import pyplot as plt

bodydetection = cv2.CascadeClassifier('aa.xml')
img = cv2.imread('12.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
body = bodydetection.detectMultiScale(gray, 1.3, 5)
for (x,y,w,h) in body:
   cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()