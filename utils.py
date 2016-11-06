# -*- coding: utf-8 -*-

import subprocess
import os
import processing 
import cv2
import requests
import json


KEY_Q = 1048689
PATH_TO_SESHAT = '/home/ggljzr/Documents/git/nao-mathematica/seshat/' 
PATH_TO_SCGINK = PATH_TO_SESHAT + '/SampleMathExps'

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
               
'''
funkce se pokusí nalézt a rozpoznat příklady v obrázku pomocí funkcí
z processing.py (předzpracování s OpenCV) a programu Seshat

parametry:
    img -- vstupní obrázek (bitmapa)
    render ( = False) -- má Seshat vytvořit obrázky ze vstupních dat? (viz parametr -r u Seshatu)
    show_reg ( = False) -- při True před zpracováním zobrazí každou nalezenou textovou oblast pomocí cv.imshow()
    write_reg ( = False) -- při True každou oblast zapíše do souboru
    remove_scgink ( = True) -- při True smaže vygenerované scgink soubory po zpracování Seshatem

návratová hodnota:
    pole Latex řetězců, které reprezentují nalezení příklady (jeden řetězec za každý příklad)
'''
def img_to_latex(img, render = False, show_reg = False, write_reg = False, remove_scgink = True):
    text_regions = processing.get_text_regions(img)
    print("Detected {} text regions".format(len(text_regions)))
    reg_n = 0
    results = []

    os.chdir(PATH_TO_SESHAT)
    for region in text_regions:

        if show_reg == True:
            print('Showing region {}'.format(reg_n))
            cv2.imshow('region {}'.format(reg_n), region)
            cv2.waitKey()

        if write_reg == True:
            print('Writing region {}'.format(reg_n))
            cv2.imwrite('region{}.png'.format(reg_n), region * 255)

        print('Processing region {} (image processing)'.format(reg_n))

        try:
            strokes = processing.follow_lines(region, queue_length = 5)
        except:
            continue

        path_to_inkfile = '{}/region{}.scgink'.format(PATH_TO_SCGINK, reg_n)
        clusters_to_scgink(strokes, path_to_inkfile, min_length = 1)

        
        seshat_cmd = './seshat -c Config/CONFIG -i ' + path_to_inkfile
       
        if render == True:
            seshat_cmd = seshat_cmd + ' -r render/region_{}.pgm'.format(reg_n)
        
        print('Processing region {} (Seshat)'.format(reg_n))
        output = subprocess.check_output(seshat_cmd + ' | tail -n 1', shell=True)

        if remove_scgink == True:
            subprocess.call(['rm', '-f', path_to_inkfile])
        
        results.append(output)
        reg_n += 1

    return results


def strokes_to_json(strokes):
    strokes_json = {
        'resultTypes': ['LATEX'],
        'columnOperation': False,
        'userResources': []
    }

    strokes_json['components'] = []

    for stroke in strokes:
        x_coords = [coord[0] for coord in stroke]
        y_coords = [coord[1] for coord in stroke]

        component = {'type' : 'stroke', 'x' : x_coords, 'y' : y_coords}

        strokes_json['components'].append(component)

    return json.dumps(strokes_json)

def img_to_json(img):
    text_regions = processing.get_text_regions(img)
    
    expressions = []

    for region in text_regions:
        try:
            strokes = processing.follow_lines(region)
        except:
            continue

        strokes_json = strokes_to_json(strokes)
        expressions.append(strokes_json)

    return expressions

def call_myscript(math_input, api_key):
    url = 'http://cloud.myscript.com/api/v3.0/recognition/rest/math/doSimpleRecognition.json'
    p = {'applicationKey': api_key, 'mathInput': math_input}
     
    r = requests.post(url, params = p)
    r.raise_for_status()

    return r.json()






