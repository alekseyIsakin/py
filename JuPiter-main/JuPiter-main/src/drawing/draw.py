from analisis.classes.classes import Line, Island
import numpy as np
import random as rnd
import cv2

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
            (i.index, i.top),
            (i.index, i.down),
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
                (i.index, i.top),
                (i.index, i.down),
                clr
                )
    return cv2.resize(
        test_img,
        (mask_inv.shape[1] * scale[0], mask_inv.shape[0] * scale[0])
    )
