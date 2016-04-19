import whiteboard as wb
import sys
import cv2
import numpy

image_path = "images/orig.png"

argc = len(sys.argv)

if argc > 1:
	image_path = str(sys.argv[1])

img = cv2.imread(image_path)
thresh_final = wb.whiteboard_detect(img)

cv2.imshow("img", img)
cv2.imshow("thresh_final", thresh_final)
cv2.imwrite('dst.png', thresh_final)

#ted udelat naky to vyznaceni bloku textu
#https://stackoverflow.com/questions/23506105/extracting-text-opencv

cv2.waitKey()

