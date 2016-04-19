# sudoku example http://opencvpython.blogspot.com/2012/06/sudoku-solver-part-2.html
# detekce regionu s textem
# https://stackoverflow.com/questions/23506105/extracting-text-opencv

import numpy as np
import cv2

KEY_Q = 1048689

def whiteboard_detect(img):
    rows, cols, ch = img.shape

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # ten gaussian blur mozna nemusi bejt, nebo treba jinak nastavenej
    gray_blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # to nastaveni prahovani je pomerne dulezity, nejlip vychazi:
    #ADAPTIVE_THRESH_MEAN_C, THRESH_BINARY, 11, 2
    # akora nahovno ze u toho vobrazku pod uhlem to veme misto jednoho rohu
    # ten stin takze je to trochu rozmazany
    thresh = cv2.adaptiveThreshold(
        gray_blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_img = np.zeros((rows, cols), dtype=np.uint8)

    cv2.drawContours(contours_img, contours, -1, (255, 255, 255), 1)

    biggest = None
    max_area = 0

    thresh_final = None

    # na tohle se este podivat
    for i in contours:
        area = cv2.contourArea(i)
        if area > 100:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area

    if biggest is not None:
        for point in biggest:
            x, y = point[0].ravel()
            cv2.circle(img, (x, y), 4, 255, -1)

        # najdu ctyri rohy podle kterejch vobrazek vyrovnam
        top_left = min(biggest, key=lambda p: p[0][0] + p[0][1])
        bottom_right = max(biggest, key=lambda p: p[0][0] + p[0][1])
        top_right = max(biggest, key=lambda p: p[0][0] - p[0][1])
        bottom_left = min(biggest, key=lambda p: p[0][0] - p[0][1])

        pts1 = np.float32([top_left, bottom_left, top_right, bottom_right])
        pts2 = np.float32([[0, 0], [0, rows], [cols, 0], [cols, rows]])

        M = cv2.getPerspectiveTransform(pts1, pts2)
        dst = cv2.warpPerspective(gray, M, (rows, cols))

        # mozna taky zkusit
        # https://stackoverflow.com/questions/23506105/extracting-text-opencv
        # pro detekci regionu s textem

        #thresh_final = cv2.adaptiveThreshold(
        #    dst, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    return dst


def contours_to_scgink(contours, scgink_file, min_length=9):
    contours_filtered = [
        contour for contour in contours if len(contour) >= min_length]

    with open(scgink_file, 'w') as ink_file:
        ink_file.write("SCG_INK\n")
        ink_file.write("{}\n".format(len(contours_final_filtered)))
        for contour in contours_final_filtered:
            ink_file.write("{}\n".format(len(contour)))
            for coord in contour:
                ink_file.write("{} {}\n".format(
                    coord[0][0], coord[0][1]))
