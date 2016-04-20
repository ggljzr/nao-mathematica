#https://stackoverflow.com/questions/23506105/extracting-text-opencv
#modified answer 3, added gaussian blur and adaptive threshold
#pro ziskani strokes je asi potreba neco jako
#https://en.wikipedia.org/wiki/Topological_skeleton, coz neni v opencv

import utils
import cv2
import sys

image_path = "images/orig.png"

argc = len(sys.argv)

if argc > 1:
	image_path = str(sys.argv[1])

img = cv2.imread(image_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
leveled = utils.whiteboard_detect(img)
rgb = cv2.cvtColor(leveled, cv2.COLOR_GRAY2RGB)

thresh = cv2.GaussianBlur(leveled, (11, 11), 0 )
thresh = cv2.adaptiveThreshold(thresh, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
dilated = cv2.dilate(thresh, kernel, iterations=15) 
contours, hierarchy = cv2.findContours(
    dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

rows, cols = thresh.shape

text_regions = []

# for each contour found, draw a rectangle around it on original image
for contour in contours:
    # get rectangle bounding contour
    [x, y, w, h] = cv2.boundingRect(contour)

    #discard areas that are too big
    if h > rows - 10 or w > cols - 10:
        continue

    # discard areas that are too small
    if h < 60 or w < 60:
        continue

    # draw rectangle around contour on original image
    cv2.rectangle(rgb, (x, y), (x + w, y + h), (0, 255, 0), 1)
    rect_mat = leveled[ y : y + h, x : x + w]
    rect_mat = cv2.adaptiveThreshold(rect_mat, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    text_regions.append(rect_mat)

# write original image with added contours to disk
#cv2.imshow('orig', img)
cv2.imshow("text regions", rgb)

reg_n = 0
for region in text_regions:
    cv2.imshow('region {}'.format(reg_n), region)
    reg_n += 1

while True:
    k = cv2.waitKey(33)
    if k == utils.KEY_Q:
        break
    elif k == -1:
        continue
 
