#https://stackoverflow.com/questions/23506105/extracting-text-opencv
#pro ziskani strokes je asi potreba neco jako
#https://en.wikipedia.org/wiki/Topological_skeleton, coz neni v opencv
#distance transformation
#clusterizace
#stackoverflow -> finding continuous areas of bits in 2d bit array

#este by to teda chtelo udelat nakou tu transformaci tim morpholgy operatorem
#(dilatace a tak), protoze u toho vobrazku pod uhlem je pak treba ta sedmicka 
#takova potrhana coz by asi chtelo zacelit, i kdyz ten seshat by to mozna vydrzel

#jinak co se tyce tech vobrazku tak to numpy.nonzero vypada dobre, akorat by to chtelo
#rozrezat ten text region este na jednotlivy znaky zase pomoci kontur a bounding boxes
#aby byly ty jednotlivy strokes jakoby voddeleny 

#^^to asi nebude potreba

#a pak delat ten kazdej znak zvlast s tim, ze by se udaly ty cerny body pomoci
#toho nonzero a pak by se udal nakej clustering (naky knn nebo takovy nesmysly)
#co by dal ty sousedni body dohromady

#hledani souvisle oblasti:
#nejdriv teda asi musime najit souvislou voblast ktera bude tvorit jeden tah
#takze vzit prvni bilej bod a pak projit vsechny sousedni body a hledat sousedy

#ale stejne by to pak chtelo ty jednotlivy body shluknout do vetsich aby treba nebylo vic bodu tahu
#na jednim radku, to pak dela v tim seshatu celkem bordel

#este se taky podivat jesli by se nedalo nak pouzit to hierarchalClustering z opencv,
#najit nakej tutorial

import utils
import cv2
import sys
import numpy as np

image_path = "images/orig.png"

argc = len(sys.argv)

if argc > 1:
	image_path = str(sys.argv[1])


img = cv2.imread(image_path)

text_regions = utils.get_text_regions(img) 

cv2.imshow('orig', img)

reg_n = 0
for region in text_regions:
    cv2.imshow('region {}'.format(reg_n), region)
    reg_n += 1

points_array = np.nonzero(text_regions[0])
points_xy = []

points_xy = zip(points_array[1], points_array[0])

#print len(points_xy)
#print points_xy[0:20]

while True:
    k = cv2.waitKey(33)
    if k == utils.KEY_Q:
        break
    elif k == -1:
        continue
 
