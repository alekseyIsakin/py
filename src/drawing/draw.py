from analisis.classes.classes import Line, Island
import numpy as np
import random as rnd
import cv2
import math as m
from approximation import getLine

def draw_island(island:Island, 
        mask_inv:np.ndarray, 
        clr=(0,0,255),
        draw_over=False,
        scale=(1,1)):

    test_img = np.ones((
        mask_inv.shape[0],
        mask_inv.shape[1],
        3
        )) * 255
    if draw_over:
        test_img = mask_inv
    for i in island:
        cv2.line(
            test_img, 
            (i['index'], i['top']),
            (i['index'], i['down']),
            clr
            )
    return cv2.resize(
        test_img,
        (mask_inv.shape[1] * scale[0], mask_inv.shape[0] * scale[0])
    )

def draw_islands(islands:list[Island], mask_inv:np.ndarray, backclr:int=(0,0,0), override=False,scale=(1,1)) -> np.ndarray:
    test_img = np.ones(
        (mask_inv.shape[0], mask_inv.shape[1], 3)
        ) * backclr
    if override == False:
        test_img = mask_inv
    
    for island in islands:
        clr = (
            rnd.randint(0, 255),
            rnd.randint(0, 255),
            rnd.randint(0, 255)
            )
        for i in island:
            test_img = cv2.line(
                test_img, 
                (i['index'], i['top']),
                (i['index'], i['down']),
                clr
                )
    return cv2.resize(
        test_img,
        (mask_inv.shape[1] * scale[0], mask_inv.shape[0] * scale[0])
    )

def draw_islands_final(islands:list[Island], mask_inv:np.ndarray, backclr:int=(0,0,0), override=False,scale=(1,1)) -> np.ndarray:
    test_img = np.ones(
        (mask_inv.shape[0], mask_inv.shape[1], 3)
        ) * backclr
    if override == False:
        test_img = mask_inv
    
    for island in islands:
        clr = (
            rnd.randint(0, 255),
            rnd.randint(0, 255),
            rnd.randint(0, 255)
            )
        axes_x = []
        axes_y = []
        for i in island:
            axes_x.append(i['index'])
            axes_y.append(m.ceil(m.fabs(i['down'] - (i['down'] - i['top'])/2)))

            test_img = cv2.line(
                test_img, 
                (i['index'], i['top']),
                (i['index'], i['down']),
                clr
                )
        if (len(axes_x) > 0 and len(axes_y) > 0):
            axis = getLine(axes_x, axes_y)
            print('Axis of the graph is', axis)
            test_img = cv2.line(
                test_img, 
                (m.floor(axis[0][0]), m.floor(axis[0][1])),
                (m.floor(axis[1][0]), m.floor(axis[1][1])),
                clr)
            
    return cv2.resize(
        test_img,
        (mask_inv.shape[1] * scale[0], mask_inv.shape[0] * scale[0])
    )
