#!/usr/bin/python
# -*- coding: utf-8 -*-

# detekce regionu s textem

import numpy as np
import cv2
import math

KEY_Q = 1048689

'''
funkce se pokusí najít rohy tabule v obrázku
a podle těchto rohů provede transformaci perspektivy
(obrázek bude kolmo ke kameře)

sudoku example http://opencvpython.blogspot.com/2012/06/sudoku-solver-part-2.html

parametry:
    img -- vstupní obrázek (bitmapa)
návratová hodnota:
    transformovaný obrázek (bitmapa, grayscale)
'''
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

        # thresh_final = cv2.adaptiveThreshold(
        # dst, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    return dst

'''
Created by Eiichiro Momma on 2014/08/11.
Copyright (c) 2014 Eiichiro Momma. All rights reserved.
http://www.eml.ele.cst.nihon-u.ac.jp/~momma/wiki/wiki.cgi/OpenCV/%E7%B4%B0%E7%B7%9A%E5%8C%96.html

funcke aplikuje na obrázek Guo-Hallův algoritmus,
který ztenčí všehny bílé čáry v obrázku na šířku 1px

parametry:
    img -- vstupní obrázek (bitmapa, grayscale, oprahovaný na pouze černou a bílou)

návratová hodnota:
    obrázek se ztenčenými čárami
'''
def guo_hall_thinning(img):
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

'''
funkce najde oblasti s textem v obrázku, na kazde oblasti provede morphological closing
(dilatace a eroze, jedna iterace) a poté Guo-Hallův algoritmus

V podstatě jediná funkce, kterou je potřeba zavolat na zpracování obrázku. 
Vezme obrázek z kamery a vrátí oblasti (každá oblast by měla představovat jeden příklad na tabuli), 
ze kterých je pak rekonstruován vstup pro seshat.

https://stackoverflow.com/questions/23506105/extracting-text-opencv - 3. odpověď 

parametry:
    img -- vstupní obrázek(bitmapa, funkce již volá whiteboard_detect, vstup je tedy původní obrázek z kamery)

návratová hodnota:
    list bitmap s jednotlivými oblastmi, na každou oblast bylo aplikováno prahování a Guo-Hall
'''
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

    for contour in contours:
        [x, y, w, h] = cv2.boundingRect(contour)

        if h > rows - 10 or w > cols - 10:
            continue

        if h < 60 or w < 60:
            continue

        # draw rectangle around contour on original image
        # cv2.rectangle(rgb_rect, (x, y), (x + w, y + h), (0, 255, 0), 1)

        rect_mat = leveled[y: y + h, x: x + w]
        rect_mat = cv2.adaptiveThreshold(
            rect_mat, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        rect_mat = cv2.morphologyEx(
            rect_mat, cv2.MORPH_CLOSE, kernel, iterations=1)
        
        kernel = np.ones((2,2), np.uint8)
        rect_mat = guo_hall_thinning(rect_mat)

        text_regions.append(rect_mat)

    return text_regions


def manhattan_dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

'''
parametry:
    a, b -- body (x,y)
návratová hodnota:
    True když se bod b nacházi v 8 okolí bodu a
'''
def is_neighbour(a, b):
    if a == None or b == None:
        return False

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


def euclidean_dist(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

'''
funkce najde koncové body čar v textové oblasti

parametry:
    text_region -- oblast s textem, viz výstup funkce get_text_regions (oprahované, Guo-Hall )

návratová hodnota:
    seznam koncových bodů [(x,y)]
'''
def get_endpoints(text_region):
    operators = [None] * 8

    operators[0] = np.array(np.mat('-1. -1. -1.; 1. 1. -1.; -1. -1. -1.'));
    operators[1] = np.array(np.mat('-1. 1. -1.; -1. 1. -1.; -1. -1. -1.'));
    operators[2] = np.array(np.mat('-1. -1. -1.; -1. 1. 1.; -1. -1. -1.'));
    operators[3] = np.array(np.mat('-1. -1. -1.; -1. 1. -1.; -1. 1. -1.'));
    operators[4] = np.array(np.mat('1. -1. -1.; -1. 1. -1.; -1. -1. -1.'));
    operators[5] = np.array(np.mat('-1. -1. 1.; -1. 1. -1.; -1. -1. -1.'));
    operators[6] = np.array(np.mat('-1. -1. -1.; -1. 1. -1.; 1. -1. -1.'));
    operators[7] = np.array(np.mat('-1. -1. -1.; -1. 1. -1.; -1. -1. 1.'));

    images = []

    for operator in operators:
        new_image = cv2.filter2D(text_region, cv2.CV_32FC1, operator)
        images.append(new_image)
        

    '''
    rows, cols = images[0].shape
    for i in range(0, rows):
        for j in range(0, cols):
            val = images[0][i][j]
            if val < 0:
                sys.stdout.write(".")
            elif val >= 0:
                sys.stdout.write(str(int(val)))
        print ""
    '''
    
    endpoints = []
    for image in images:
        new_endpoints = np.where(image == 2)
        if len(new_endpoints) > 0:
            new_endpoints = zip(new_endpoints[1], new_endpoints[0])
            for endpoint in new_endpoints:
                endpoints.append(endpoint)

    return endpoints

'''
pomocná funkce, vrátí souřadnice sousedůi (x,y) v 8 okolí bodu
'''
def get_neighbours(point):
    x = point[0]
    y = point[1]
    return [(x-1,y+1),(x,y+1),(x+1,y+1),
            (x-1,y),(x+1,y),(x-1,y-1),
            (x,y-1),(x+1,y-1)]



'''
funkce pro výpočet úhlu mezi dvěma vektory

návratová hodnota:
    cos(ro) = v1 . v2 / (|v1| * |v2|)
'''

def get_angle(v1, v2):
    prod = np.dot(v1, v2)

    norm_a = np.dot(v1,v1)
    norm_b = np.dot(v2,v2)

    cos = prod / (norm_a * norm_b)

    return cos

'''
funkce vytvoří sérii tahů z obrázku

parametry:
    img -- vstupní obrázek (textová oblast, viz výstup funkce get_text_regions())
    endpoits -- koncové body nalezené v obrázku (viz funkce get_endpoints())
    queue_length (= 3) -- délka fronty, ze které se počítá první směrový vektor vektor
           
návratová hodnota
    pole tahů tvořících příklad, každý tah je posloupnost bodů (x,y)
'''
def follow_lines(img, endpoints, queue_length = 3):
    temp_img = img

    strokes = []

    #do toho endpoints budu chtit zapisovat (mazat endpointy)
    #takze to asi nepude pres iterator
    for endpoint_index in range(0, len(endpoints)):

        temp_img = img
        current_point = endpoints[endpoint_index]
        endpoints[endpoint_index] = None

        if current_point == None:
            continue

        stroke = []

        queue = []
        last_point = None

        print "Stroke start == " + str(current_point)
        while current_point != None:
            neighbours = get_neighbours(current_point)

            best_next_point = None
            best_angle = 10

            for neighbour in neighbours:
                rows = neighbour[1] #y coord
                cols = neighbour[0] #x coord

                #kdyz narazim na jinej endpoint koncim tah
                if neighbour in endpoints:
                    temp_img[rows, cols] = 0
                    best_next_point = None
                    neigbour_index = endpoints.index(neighbour)
                    endpoints[neigbour_index] = None
                    break

                #hledám bod v nejlepsim smeru
                if temp_img[rows, cols] > 0:
                    temp_img[rows, cols] = 0
                    if last_point == None:
                        best_next_point = neighbour
                        break
                    
                    vect_a = np.array(current_point,dtype=float) - np.array(last_point,dtype=float)
                    vect_b = np.array(neighbour, dtype=float) - np.array(current_point, dtype=float)
                    cos = get_angle(vect_a, vect_b)
                    
                    if np.abs(cos) < best_angle:
                        best_angle = np.abs(cos)
                        print "curr point = {}".format(current_point)
                        print "last point = {}".format(last_point)
                        print "neighbour = {}".format(neighbour)
                        print "cos {}".format(best_angle)
                        best_next_point = neighbour
            
            rows = current_point[1]
            cols = current_point[0]
            temp_img[rows,cols] = 0

            #nastrel asi neco takovyhleho

            if current_point != None:
                stroke.append(current_point)
                queue.append(current_point)

                last_point = queue[0]
                if len(queue) > queue_length:
                    queue.pop(0)
            
            #last_point = current_point
            current_point = best_next_point

            print str(queue[-1]) + " -> " + str(current_point)
    
        print "---- Stroke End -----"
        print ""
        #tady nekde pak asi znova temp_img = img
        #nebo mozna ani nemusi bejt
        
        strokes.append(stroke)

    return strokes
        
    

'''
pomocná funkce pro get_clusters_dfs
'''
def do_dfs(node, nodes, cluster):
    node[1] = 'open'
 
    cluster.append(node[0])
    
    print "opening node: {}".format(node)

    neighbours = [neighbour for neighbour in nodes if (is_neighbour(node[0], neighbour[0]))]

    for neighbour in neighbours:
        print "     neighbour: {}".format(neighbour)
        if neighbour[1] == 'fresh':
            do_dfs(neighbour, nodes, cluster)


    node[1] = 'closed'

'''
funkce nalezne souvíslé komponenty v seznamu bodů, jako sousední
body jsou považovány body v 8 okolí

parametry:
    points -- seznam bodů (x,y) (zde bílé body v obrázku, získané pomocí np.nonzero())

návratová hodnota:
    seznam souvislých komponent, každá komponenta je tvořena seznamem bodů
'''
def get_clusters_dfs(points):
    clusters = []
    cluster = []

    nodes = np.array([ [point, 'fresh'] for point in points ])
    
    #seradi to vod nejlevejsiho
    #mozna by bylo lepsi predavat sem ty body uz serazeny
    nodes = np.sort(nodes, axis = 0)

    for node in nodes:
        if node[1] == 'fresh':
            do_dfs(node, nodes, cluster)
            
            if len(cluster) > 3:
                cluster.pop()
                clusters.append(cluster)
            
            cluster = []
   

    return clusters

'''
převede seznam souvislých kompnent z výstupu funkce get_clusters_dfs() do
scgink formátu pro seshat

parametry:
    clusters -- viz get_clusters_dfs()
    scgink_file -- výstupní soubor
    min_length -- minimální délka clusteru v souboru
'''
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
