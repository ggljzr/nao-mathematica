
#sudoku example http://opencvpython.blogspot.com/2012/06/sudoku-solver-part-2.html

import cv2
import numpy as np
import sys


image_path = "images/image2.png"

argc = len(sys.argv)

if argc > 1:
	image_path = str(sys.argv[1])

img = cv2.imread(image_path)

#nejdriv prevedu na grayscale a vykreslim
#kontury podel hran (canny)
#tyhle kontury budou pro detekci primek a rohu
#a je lepsi je udelat silnejsi (2px)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

gray = cv2.GaussianBlur(gray, (5,5), 0)
thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

biggest = None
max_area = 0
for i in contours:
	area = cv2.contourArea(i)
	if area > 100:
		peri = cv2.arcLength(i,True)
		approx = cv2.approxPolyDP(i,0.02*peri,True)
		if area > max_area and len(approx)==4:
			biggest = approx
			max_area = area

print max_area
print biggest

for point in biggest:
	x,y = point[0].ravel()
	cv2.circle(img,(x,y),4,255,-1)



cv2.imshow('dst', thresh) #dst je uz vyrovnanej vobrazek, sou v nem teda este vykreselny primky a rohy
cv2.imshow('img', img) #puvodni vobrazek kde sou doplneny primky a rohy
cv2.waitKey()

