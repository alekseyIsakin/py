import drawing.draw as draw
import cv2

def slow_draw_island(island:list, mask_inv, clr=(0,0,255), sleeptime=0,draw_over=False, scale=(1,1)):
    cv2.imshow("show", draw.draw_island(island, mask_inv, clr, draw_over, scale))
    cv2.waitKey(sleeptime) 
def slow_draw_islands(islands:list, mask_inv, clr=(), sleeptime=0, draw_over=False, scale=(1,1)):
    cv2.imshow("show", draw.draw_islands(islands, mask_inv, clr, draw_over, scale))
    cv2.waitKey(sleeptime) 