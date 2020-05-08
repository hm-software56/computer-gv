import cv2 as cv
import numpy as np

img = cv.imread("C:/Users/user/Desktop/1111/123.jpg")
grayscaled = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
#retval, threshold = cv2.threshold(img,125, 255, cv2.THRESH_TOZERO)
retval1,threshold1 = cv.threshold(img,145, 255, cv.THRESH_BINARY)

th2 = cv.adaptiveThreshold(grayscaled, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,19, 20)
th3 = cv.adaptiveThreshold(grayscaled, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV,19, 20)

#cv2.imshow('THRESH_BINARY',threshold1)
#cv2.imshow('threshold2',grayscaled)
cv.imshow('ADAPTIVE_THRESH_GAUSSIAN_C',th2)
cv.imshow('ADAPTIVE_THRESH_MEAN_C',th3)
cv.waitKey(0)
cv.destroyAllWindows()