import cv2
import numpy as np
import random as rnd

from analisis.classes.classes import Line, Island

def get_lines(mask_inv:np.ndarray, offset_x=0, offset_y=0) -> list[Line]:
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
            if cntBlank > 0:
                lines.append(Line(j+offset_y, higher+offset_x, lower+offset_x))
                lower = 0
                higher = 0
        if lower > 0:
            lines.append(Line(j+offset_y, higher+offset_x, lower+offset_x))
        for l in lines:
            graph.append(l)
        lines.clear()
    
    return graph



def get_low_up(graph:list[Island], img=np.zeros(0)) -> list[int]:

    prev = graph[0]

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
            
            cv2.line(img, (p[0],p[2]), (p[0], p[1]), clr)
            
            if len(img.shape) == 2:
                clr = 255 if status else 0
            else:
                clr = (255, 255, 0) \
                    if status else (0, 255, 255)
            clr = (0,0,255)
            img[mainPoints[-1]][p.index] = clr

    # if len(img.shape) > 1:
    #     cv2.imwrite(PATH_TO_OUTPUT_JPG,img)

    return mainPoints
  
def is_neighbours(l=Line(0,0,0), r=Line(0,0,0)):
  return not (not abs(l.index - r.index) > 1 and 
         ((l.top <= (r.top+1) and l.top >= (r.down-1)) or
          (l.down <= (r.top+1) and l.down >= (r.down-1)) or
          (r.top <= (l.top+1) and r.top >= (l.down-1))  or
          (r.down <= (l.top+1) and r.down >= (l.down-1))))