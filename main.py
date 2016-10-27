#!/usr/bin/python

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
import processing as proc

import cv2
import sys
import numpy as np

import requests
import json

image_path = "images/tabule1.png"

argc = len(sys.argv)

if argc > 1:
    image_path = str(sys.argv[1])

img = cv2.imread(image_path)

text_regions = proc.get_text_regions(img)

#cv2.imshow('aaa', text_regions[1] * 255)

cv2.waitKey()

endpoints = proc.get_endpoints(text_regions[1])
strokes = proc.follow_lines(text_regions[1], endpoints)

x_coords = [ coord[0] for coord in strokes[0]]
y_coords = [ coord[1] for coord in strokes[0]]

strokes_json = utils.strokes_to_json(strokes)
strokes_json = json.dumps(strokes_json)

#res = utils.img_to_latex(img, render=True, show_reg = False)
app_key = '17ead59f-33f8-4d2d-90b5-abf4b9eefa4e'

url = 'http://cloud.myscript.com/api/v3.0/recognition/rest/math/doSimpleRecognition.json'

p = {'applicationKey': app_key, 'mathInput': strokes_json}

r = requests.post(url, params = p)

print r.status_code

print r.json()['result']['results'][0]

utils.img_to_latex(img, render = True)
