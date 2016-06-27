# https://stackoverflow.com/questions/23506105/extracting-text-opencv
# pro ziskani strokes je asi potreba neco jako
# https://en.wikipedia.org/wiki/Topological_skeleton, coz neni v opencv
# distance transformation
# clusterizace
# stackoverflow -> finding continuous areas of bits in 2d bit array

# este by to teda chtelo udelat nakou tu transformaci tim morpholgy operatorem
#(dilatace a tak), protoze u toho vobrazku pod uhlem je pak treba ta sedmicka
# takova potrhana coz by asi chtelo zacelit, i kdyz ten seshat by to mozna
# vydrzel

# jinak co se tyce tech vobrazku tak to numpy.nonzero vypada dobre, akorat by to chtelo
# rozrezat ten text region este na jednotlivy znaky zase pomoci kontur a bounding boxes
# aby byly ty jednotlivy strokes jakoby voddeleny

#^^to asi nebude potreba

# a pak delat ten kazdej znak zvlast s tim, ze by se udaly ty cerny body pomoci
# toho nonzero a pak by se udal nakej clustering (naky knn nebo takovy nesmysly)
# co by dal ty sousedni body dohromady

# hledani souvisle oblasti:
# nejdriv teda asi musime najit souvislou voblast ktera bude tvorit jeden tah
# takze vzit prvni bilej bod a pak projit vsechny sousedni body a hledat
# sousedy

# ale stejne by to pak chtelo ty jednotlivy body shluknout do vetsich aby treba nebylo vic bodu tahu
# na jednim radku, to pak dela v tim seshatu celkem bordel

# este se taky podivat jesli by se nedalo nak pouzit to hierarchalClustering z opencv,
# najit nakej tutorial

#jako na to hledani tech tahu asi nakonec udelat tu dist transform a pak to hledat podle tech hrebenu

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

endpoints = utils.get_endpoints(text_regions[0])

cv2.imshow('reg 0', text_regions[0])

'''
for endpoint in endpoints:
    cv2.circle(text_regions[0], endpoint, 2, 255, -1)

cv2.imwrite('text_region.png', text_regions[0] * 255)

for region in text_regions:
    cv2.imshow('region {}'.format(reg_n), region)
    reg_n += 1

'''

num = 0
for region in text_regions:
    
    endpoints = utils.get_endpoints(region)
    strokes = utils.follow_lines(region, endpoints, queue_length = 5)
    utils.clusters_to_scgink(strokes, "seshat/SampleMathExps/priklad_{}.scgink".format(num), min_length = 1)
    
    cv2.imwrite("region{}.png".format(num), region * 255.)
    num += 1

cv2.waitKey()
