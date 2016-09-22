# -*- coding: utf-8 -*-

import subprocess
import os
import processing 
import cv2

KEY_Q = 1048689
PATH_TO_SESHAT = '/home/ggljzr/Documents/git/nao-mathematica/seshat/' 
PATH_TO_SCGINK = PATH_TO_SESHAT + '/SampleMathExps/temp.scgink'

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

def img_to_latex(img, render = False, show_reg = False):
    text_regions = processing.get_text_regions(img)
    print("Detected {} text regions".format(len(text_regions)))
    reg_n = 0
    results = []

    os.chdir(PATH_TO_SESHAT)
    for region in text_regions:

        if show_reg == True:
            print('Showing region {}'.format(reg_n))
            cv2.imshow('region', region)
            cv2.waitKey()

        print('Processing region {} (image processing)'.format(reg_n))

        endpoints = processing.get_endpoints(region)
        strokes = processing.follow_lines(region, endpoints, queue_length = 5)
        clusters_to_scgink(strokes, PATH_TO_SCGINK, min_length = 1)

        
        seshat_cmd = './seshat -c Config/CONFIG -i ' + PATH_TO_SCGINK
       
        if render == True:
            seshat_cmd = seshat_cmd + ' -r render/region_{}.pgm'.format(reg_n)
        
        print('Processing region {} (Seshat)'.format(reg_n))
        output = subprocess.check_output(seshat_cmd, shell=True)

        subprocess.call(['rm', '-f', PATH_TO_SCGINK])
        results.append(output)
        reg_n += 1

    return results






