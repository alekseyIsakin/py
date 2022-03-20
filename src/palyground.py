import cProfile

from pprint import pprint as pp
from logger import lg
from logger import lg, initLogger

from numpy import ndarray
from analisis.loader.img_analizer import *
from analisis.loader.mask_loader import *
from analisis.loader.islands import build_islands_from_fragmets, fragment_calculate
from drawing.draw import *
from drawing.show import *
from constant.paths import PATH_TO_INPUT_, PATH_TO_OUTPUT_
from collections import namedtuple
from main import first_column_fragments, middle_fragments

fileName = "test11.png"

img:ndarray          = cv2.imread(PATH_TO_INPUT_ + fileName, cv2.IMREAD_GRAYSCALE)
img_clr:ndarray      = cv2.imread(PATH_TO_INPUT_ + fileName)
img_isl:np.ndarray   = img_clr.copy()

count_of_ecg = 4
count_of_col = 5

step_x = img.shape[1] // count_of_col
step_y = img.shape[0] // count_of_ecg

x=3
y=0
bottom_line = 200
upper_line = 255
step = 2

for up_value in range(bottom_line,upper_line,step):
  mask_inv = get_mask_from_gray(img, upper_val=up_value)      
  islandsInFragment = fragment_calculate(y*step_y,x*step_x,  step_y+1,step_x+1, mask_inv)

  one_of_works = False
  #------------------------------------------------------
  img_isl[y*step_y:(y+1)*step_y, x*step_x:(x+1)*step_x] = 255
  img_isl = cv2.rectangle(img_isl, (x*step_x, y*step_y),((x+1)*step_x,(y+1)*step_y,), color=(0,0,255))
  img_isl = draw_islands(islandsInFragment, img_isl)
  lg.info(f"{up_value}, {len(islandsInFragment)}")
  cv2.imshow('w', img_isl)
  cv2.waitKey(10)
  #------------------------------------------------------

  if x == 0:
    one_of_works = first_column_fragments(islandsInFragment,x,y,step_x,step_y)
  elif x == count_of_ecg:
    one_of_works = True
  else:
    one_of_works = middle_fragments(islandsInFragment,x,y,step_x,step_y)
  
  cv2.imwrite(PATH_TO_OUTPUT_ + f"{up_value}.png", img_isl)
  if one_of_works == True:
    cv2.imwrite(PATH_TO_OUTPUT_ + f"{x}_{y}_{up_value}.png", img_isl)
    break
