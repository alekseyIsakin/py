import cv2
import numpy as np
import random as rnd
import time

from classes import Line, Island
from paths import PATH_TO_INPUT_JPG, \
                  PATH_TO_ISLANDS_JPG,  \
                  PATH_TO_MASK_JPG, \
                  PATH_TO_OUTPUT_JPG

def get_mask(img):
    # Convert BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # define range of black color in HSV
    lower_val = np.array([0,0,0])
    upper_val = np.array([50,100,100])

    # Threshold the HSV image to get only black colors
    mask = cv2.inRange(hsv, lower_val, upper_val)

    # invert mask to get black symbols on white background
    mask_inv = cv2.bitwise_not(mask)

    return mask_inv

def get_mask_from_gray(img):
    # define range of black color in HSV
    lower_val = 0
    upper_val = 100

    # Threshold the HSV image to get only black colors
    mask = cv2.inRange(img, lower_val, upper_val)
    mask = cv2.bitwise_not(mask)

    return mask

def get_lines(mask_inv):
    graph = []

    for j in range(mask_inv.shape[1]):
        higher = 0
        lower = 0

        cntBlank = 0
        lines = []

        for i in range(mask_inv.shape[0]):
            if mask_inv[i,j] == 255: 
                cntBlank += 1
                if lower == 0:
                    continue
            
            if lower == 0: lower = i
            if mask_inv[i,j] != 255: 
                higher = i
                cntBlank = 0
            if cntBlank > 1:
                lines.append(Line(j, higher, lower))
                lower = 0
                higher = 0
        # if len(lines) > 0:
        for l in lines:
            graph.append(l)
        lines.clear()
    
    return graph

def draw_island(island, mask_inv, clr=(0,0,255),draw_over=False,scale=(1,1)):
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

def draw_islands(ecg, mask_inv, clr=(), draw_over=False,scale=(1,1)):
    test_img = np.ones((
        mask_inv.shape[0],
        mask_inv.shape[1],
        3
        )) * 255
    if draw_over:
        test_img = mask_inv
    
    for island in ecg:
        clr = (
            rnd.randint(0, 255),
            rnd.randint(0, 255),
            rnd.randint(0, 255)
            )
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

def slow_draw_island(island, mask_inv, clr=(0,0,255), sleeptime=0,draw_over=False, scale=(1,1)):
    cv2.imshow("show", draw_island(island, mask_inv, clr, draw_over, scale))
    cv2.waitKey(sleeptime) 
def slow_draw_islands(islands, mask_inv, clr=(), sleeptime=0, draw_over=False, scale=(1,1)):
    cv2.imshow("show", draw_islands(islands, mask_inv, clr, draw_over, scale))
    cv2.waitKey(sleeptime) 

def get_low_up(graph, img=np.zeros(0)):

    prev = graph[0]
    lastAcc = prev[0]

    prevPoint = 0
    mainPoints = []
    mainPoints.append(graph[0].top)
    prevPoint = graph[0].down
    status = False
    shape = len(img.shape)
    print("Я начну с точки ", mainPoints[0])

    if shape > 1:
        if shape == 2:
            clr = 25
        else:
            clr = (0, 255, 0)
        img[mainPoints[0]][graph[0].index] = clr

    for p in graph[1:]:
            
        if(status == False):
            if(mainPoints[-1] < p.top):
                if(prevPoint <= p.down):
                    status = False
                    mainPoints.append(p.top)
                    prevPoint = p.down
                else:
                    if((p.top - mainPoints[-1]) > (p.down - prevPoint)):
                        status = False
                        mainPoints.append(p.top)
                        prevPoint = p.down
                    elif((p.top - mainPoints[-1]) < (p.down - prevPoint)):
                        status = True
                        mainPoints.append(p.down)
                        prevPoint = p.top
                    else:
                        status = False
                        mainPoints.append(p.top)
                        prevPoint = p.down
            elif(mainPoints[-1] > p.top):
                if(prevPoint >= p.down):
                    status = True
                    mainPoints.append(p.down)
                    prevPoint = p.top
                else:
                    status = False
                    mainPoints.append(p.top)
                    prevPoint = p.down
            else:
                if(prevPoint <= p.down):
                    status = False
                    mainPoints.append(p.top)
                    prevPoint = p.down
                else:
                    status = True
                    mainPoints.append(p.down)
                    prevPoint = p.top
        else:
            if(mainPoints[-1] > p.down):
                if(prevPoint >= p.top):
                    status = True
                    mainPoints.append(p.down)
                    prevPoint = p.top
                else:
                    if((p.down - mainPoints[-1]) < (p.top - prevPoint)):
                        status = True
                        mainPoints.append(p.down)
                        prevPoint = p.top
                    elif((p.down - mainPoints[-1]) > (p.top - prevPoint)):
                        status = False
                        mainPoints.append(p.top)
                        prevPoint = p.down
                    else:
                        status = True
                        mainPoints.append(p.down)
                        prevPoint = p.top
            elif(mainPoints[-1] < p.down):
                status = False
                mainPoints.append(p.top)
                prevPoint = p.down
            else:
                if(p.top > prevPoint):
                    status = False
                    mainPoints.append(p.top)
                    prevPoint = p.down
                else:
                    status = True
                    mainPoints.append(p.down)
                    prevPoint = p.top

        if shape > 1:
            if shape == 2:
                clr = 200
            else:
                clr = (0, 255, 0)
            
            blank3 = np.ones(img.shape, np.uint8)*255
            cv2.line(img, (p[0],p[2]), (p[0], p[1]), clr)
            cv2.line(blank3, (p[0],p[2]), (p[0], p[1]), clr)
            
            if len(img.shape) == 2:
                clr = 255 if status else 0
            else:
                clr = (255, 255, 0) \
                    if status else (0, 255, 255)
            
            img[mainPoints[-1]][p.index] = clr

    if len(img.shape) > 1:
        cv2.imwrite(PATH_TO_OUTPUT_JPG,img)

    return mainPoints
  
def is_neighbours(l=Line(0,0,0), r=Line(0,0,0)):
  return not (not abs(l.index - r.index) > 1 and 
         ((l.top <= (r.top+1) and l.top >= (r.down-1)) or
          (l.down <= (r.top+1) and l.down >= (r.down-1)) or
          (r.top <= (l.top+1) and r.top >= (l.down-1))  or
          (r.down <= (l.top+1) and r.down >= (l.down-1))))