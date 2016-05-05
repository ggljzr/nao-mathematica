# sudoku example http://opencvpython.blogspot.com/2012/06/sudoku-solver-part-2.html
# detekce regionu s textem
# https://stackoverflow.com/questions/23506105/extracting-text-opencv

import numpy as np
import cv2
import math

KEY_Q = 1048689


def whiteboard_detect(img):
    rows, cols, ch = img.shape

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # ten gaussian blur mozna nemusi bejt, nebo treba jinak nastavenej
    gray_blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # to nastaveni prahovani je pomerne dulezity, nejlip vychazi:
    # ADAPTIVE_THRESH_MEAN_C, THRESH_BINARY, 11, 2
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

        # thresh_final = cv2.adaptiveThreshold(
        # dst, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    return dst

def guo_hall_thinning(img):
    #Created by Eiichiro Momma on 2014/08/11.
    #Copyright (c) 2014 Eiichiro Momma. All rights reserved.
    #http://www.eml.ele.cst.nihon-u.ac.jp/~momma/wiki/wiki.cgi/OpenCV/%E7%B4%B0%E7%B7%9A%E5%8C%96.html

    kpw = [None] * 8
    kpb = [None] * 8

    rows, cols = img.shape

    kpb[0] = np.array(np.mat('1. 1. 0.; 1. 0. 0.; 0. 0. 0.'));
    kpb[1] = np.array(np.mat('1. 1. 1.; 0. 0. 0.; 0. 0. 0.'));
    kpb[2] = np.array(np.mat('0. 1. 1.; 0. 0. 1.; 0. 0. 0.'));
    kpb[3] = np.array(np.mat('0. 0. 1.; 0. 0. 1.; 0. 0. 1.'));
    kpb[4] = np.array(np.mat('0. 0. 0.; 0. 0. 1.; 0. 1. 1.'));
    kpb[5] = np.array(np.mat('0. 0. 0.; 0. 0. 0.; 1. 1. 1.'));
    kpb[6] = np.array(np.mat('0. 0. 0.; 1. 0. 0.; 1. 1. 0.'));
    kpb[7] = np.array(np.mat('1. 0. 0.; 1. 0. 0.; 1. 0. 0.'));

    kpw[0] = np.array(np.mat('0. 0. 0.; 0. 1. 1.; 0. 1. 0.'));
    kpw[1] = np.array(np.mat('0. 0. 0.; 0. 1. 0.; 1. 1. 0.'));
    kpw[2] = np.array(np.mat('0. 0. 0.; 1. 1. 0.; 0. 1. 0.'));
    kpw[3] = np.array(np.mat('1. 0. 0.; 1. 1. 0.; 0. 0. 0.'));
    kpw[4] = np.array(np.mat('0. 1. 0.; 1. 1. 0.; 0. 0. 0.'));
    kpw[5] = np.array(np.mat('0. 1. 1.; 0. 1. 0.; 0. 0. 0.'));
    kpw[6] = np.array(np.mat('0. 1. 0.; 0. 1. 1.; 0. 0. 0.'));
    kpw[7] = np.array(np.mat('0. 0. 0.; 0. 1. 1.; 0. 0. 1.'));

    src_f = img.astype(dtype=np.float32)
    src_f = src_f * (1./255.)

    ret, src_f = cv2.threshold(src_f, 0.5, 1.0, cv2.cv.CV_THRESH_BINARY)
    ret, src_w = cv2.threshold(src_f, 0.5, 1.0, cv2.cv.CV_THRESH_BINARY)
    ret, src_b = cv2.threshold(src_f, 0.5, 1.0, cv2.cv.CV_THRESH_BINARY_INV)

    sum_ = 1.0

    while sum_ > 0.0:
        sum_ = 0.0
        for i in range(0,8):
            
            src_w = cv2.filter2D(src_w, cv2.CV_32FC1, kpw[i])
            src_b = cv2.filter2D(src_b, cv2.CV_32FC1, kpb[i])
            
            ret, src_w = cv2.threshold(src_w, 2.99, 1.0, cv2.cv.CV_THRESH_BINARY)
            ret, src_b = cv2.threshold(src_b, 2.99, 1.0, cv2.cv.CV_THRESH_BINARY)
            
            src_w = cv2.bitwise_and(src_w, src_b)
            
            sum_ += cv2.sumElems(src_w)[0]
            
            src_f = cv2.bitwise_xor(src_f, src_w)
           
            src_w = np.empty_like(src_f)
            src_w[:] = src_f
            ret, src_b = cv2.threshold(src_f, 0.5, 1.0, cv2.cv.CV_THRESH_BINARY_INV)


    return src_f

def get_text_regions(img):
    leveled = whiteboard_detect(img)

    # rgb_rect = cv2.cvtColor(leveled, cv2.COLOR_GRAY2RGB)

    thresh = cv2.GaussianBlur(leveled, (11, 11), 0)

    # tady asi nejlepsi nastavit malou block size, asi tak 3
    # jinak to priklady blizko u sebe veme jako jeden
    thresh = cv2.adaptiveThreshold(
        thresh, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 3, 2)
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

        # discard areas that are too big
        if h > rows - 10 or w > cols - 10:
            continue

        # discard areas that are too small
        if h < 60 or w < 60:
            continue

        # draw rectangle around contour on original image
        # cv2.rectangle(rgb_rect, (x, y), (x + w, y + h), (0, 255, 0), 1)

        # crop original leveled image and threshold it
        rect_mat = leveled[y: y + h, x: x + w]
        rect_mat = cv2.adaptiveThreshold(
            rect_mat, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

        # tady tu iteraci maximalne jednu
        # jinak uz to ten vobrazek docela rozmatla
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        rect_mat = cv2.morphologyEx(
            rect_mat, cv2.MORPH_CLOSE, kernel, iterations=1)
        
        #tady asi misto ty eroze implementovat guo-hall algorithm
        #https://web.archive.org/web/20160314104646/http://opencv-code.com/quick-tips/implementation-of-guo-hall-thinning-algorithm/
        kernel = np.ones((2,2), np.uint8)
        rect_mat = guo_hall_thinning(rect_mat)

        text_regions.append(rect_mat)

    return text_regions


def manhattan_dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def is_neighbour(a, b):
    dist = manhattan_dist(a, b)
    if dist == 1:
        return True

    if dist == 2:
        if abs(a[0] - b[1]) == 1:
            return True
        if abs(a[1] - b[0]) == 1:
            return True

        if abs(a[0] - b[0]) == 1 and abs(a[1] - b[1]) == 1:
            return True

    return False


def common_neigbours(cluster_a, cluster_b):
    for a in cluster_a:
        for b in cluster_b:
            if is_neighbour(a, b):
                return True
    return False


def euclidean_dist(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def do_dfs(node, nodes, cluster):
    node[1] = 'open'
   
    cluster.append(node[0])
    print "opening node: {}".format(node)

    for next_node in nodes:
        if is_neighbour(node[0], next_node[0]):
            print "     neighbours: {}".format(next_node)
            if next_node[1] == 'fresh':
                do_dfs(next_node, nodes, cluster)

    node[1] = 'closed'

def get_clusters_dfs(points):
    nodes = []

    clusters = []

    for point in points:
        node = [(point[0], point[1]), 'fresh']
        nodes.append(node)
    
    cluster = []
    for node in nodes:
        if node[1] == 'fresh':
            do_dfs(node, nodes, cluster)
            cluster.pop()
            clusters.append(cluster)
            cluster = []
    
    return clusters

def get_neigbours(point, points):
    neighbours = []
    for a in points:
        if is_neighbour(a, point):
            neighbours.append(a)
    return neighbours

def clusters_to_scgink(clusters, scgink_file, min_length = 9):
    clusters_filtered = [cluster for cluster in clusters if len(cluster) >= min_length]

    with open(scgink_file, 'w') as ink_file:
        ink_file.write("SCG_INK\n")
        ink_file.write("{}\n".format(len(clusters_filtered)))
        for cluster in clusters_filtered:
            ink_file.write("{}\n".format(len(cluster)))
            for coord in cluster:
                ink_file.write("{} {}\n".format(
                    coord[0], coord[1]))



def contours_to_scgink(contours, scgink_file, min_length=9):
    contours_filtered = [
        contour for contour in contours if len(contour) >= min_length]

    with open(scgink_file, 'w') as ink_file:
        ink_file.write("SCG_INK\n")
        ink_file.write("{}\n".format(len(contours_filtered)))
        for contour in contours_filtered:
            ink_file.write("{}\n".format(len(contour)))
            for coord in contour:
                ink_file.write("{} {}\n".format(
                    coord[0][0], coord[0][1]))
