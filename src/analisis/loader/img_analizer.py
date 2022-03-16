from cmath import inf
import cv2
import numpy as np
import random as rnd

from analisis.classes.classes import Line, Island

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
  
def is_neighbours(left_line:Line, right_line:Line):
    if left_line == right_line: return False
    
    # t1 = not abs(left_line['index'] - right_line['index']) > 1
    # t2 = (left_line['down'] <= right_line['down']+1 and left_line['down'] >= (right_line['top']-1))
    # t3 = (left_line['top'] <= (right_line['down']+1) and left_line['top'] >= (right_line['top']-1))
    # t4 = (right_line['down'] <= (left_line['down']+1) and right_line['down'] >= (left_line['top']-1))
    # t5 = (right_line['top'] <= (left_line['down']+1) and right_line['top'] >= (left_line['top']-1))
    # t6 = (t1 and (t2 or t3 or t4 or t5))
    # return t6
    return (not abs(left_line['index'] - right_line['index']) > 1 and
                ((left_line['down'] <= right_line['down']+1 and left_line['down'] >= (right_line['top']-1)) or
                (left_line['top'] <= (right_line['down']+1) and left_line['top'] >= (right_line['top']-1)) or
                (right_line['down'] <= (left_line['down']+1) and right_line['down'] >= (left_line['top']-1)) or
                (right_line['top'] <= (left_line['down']+1) and right_line['top'] >= (left_line['top']-1))))