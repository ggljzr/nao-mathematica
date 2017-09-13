#!/usr/bin/python

# https://stackoverflow.com/questions/23506105/extracting-text-opencv
# for access to myscript api you will need the api key from https://developer.myscript.com/

# key is then loaded from a .ini file with following structure:
# [myscript]
# api_key = <your api key>

# if you want to use seshat for recognition (function img_to_latex()), you'll need to get it
# from https://github.com/falvaro/seshat, build it (note the compile error mentioned in issues)
# and specify the path to seshat folder in utils.py

import utils
import processing as proc

import cv2
import sys
import numpy as np

import ConfigParser

image_path = "images/tabule1.png"

argc = len(sys.argv)

if argc > 1:
    image_path = str(sys.argv[1])

img = cv2.imread(image_path)

cfg = ConfigParser.ConfigParser()
cfg.read('auth.ini')

api_key = cfg.get('myscript', 'api_key')

expressions = utils.img_to_json(img)

for exp in expressions:
    r = utils.call_myscript(exp, api_key)
    print r['result']['results']

res = utils.img_to_latex(img, render = True, write_reg=True, remove_scgink = False)
print res
