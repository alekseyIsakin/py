from audioop import reverse
from distutils.archive_util import make_archive
from pprint import pprint as pp
from copy import deepcopy
from logger import lg

from numpy import ndarray
from analisis.loader.img_analizer import *
from analisis.loader.mask_loader import *
from analisis.loader.islands import islands_from_lines
from drawing.draw import *
from drawing.show import *
from constant.paths import PATH_TO_INPUT_JPG, \
                  PATH_TO_INPUT_, \
                  PATH_TO_ISLANDS_JPG,  \
                  PATH_TO_MASK_JPG, \
                  PATH_TO_MASK_, \
                  PATH_TO_OUTPUT_JPG
lg.info("Start")

file = r"E:\NIRS-BrTSU\py-b\JuPiter-main\images\input\(190)-test17.png"
#file = r"E:\NIRS-BrTSU\py-b\JuPiter-main\images\input\input.jpg"
#file = r"E:\NIRS-BrTSU\py-b\JuPiter-main\images\input\Screenshot.png"
img:ndarray     = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
img_clr:ndarray = cv2.imread(PATH_TO_INPUT_ + file)

lg.info(f"load image '{file}'")
lg.debug(f"resolution '{file}' is {img.shape}")
completeFull:list[list[Island]] = []

step_x = img.shape[1] // 5
step_y = img.shape[0] // 4
#step_x = img.shape[1] // 1
#step_y = img.shape[0] // 1

def fragment_calculate(coord_x:int, coord_y:int,
  step_x:int, step_y:int, mask_inv:np.ndarray) -> list[Island]:
    lines_arr = get_lines(mask_inv [
      coord_x:coord_x + step_x,
      coord_y:coord_y + step_y], coord_x, coord_y)
    complete = islands_from_lines(lines_arr)

    return complete

mask_inv = get_mask_from_gray(img, upper_val=100)
mask = cv2.cvtColor(mask_inv, cv2.COLOR_GRAY2BGR) 
isl = mask.copy()
    

for x in range(img.shape[1] // step_x):
  for y in range(img.shape[0] // step_y):
    bottom_line = 150
    upper_line = 255
    step = 1
    for up_value in range(bottom_line,upper_line,step):
      largest_island_has_been_found = False
      #lg.debug(f">> step [{x}|{y}][{x*step_x}, {y*step_y}]")
      mask_inv = get_mask_from_gray(img, upper_val=up_value)      
      complete = fragment_calculate(y*step_y,x*step_x,  step_y+1,step_x+1, mask_inv)

      i=0
      while i != len(complete):
        if len(complete[i]) <= 3 or complete[i].maxH - complete[i].minH <= 2:
          del complete[i]
        else:
          i+=1

      for single in complete:
        if len(single) >= step_x:

          largest_island_has_been_found = True
          print(f"При насыщенности {up_value} островов найдено {len(complete)}")
          #------------------------------------------------------
          isl[y*step_y:(y+1)*step_y, x*step_x:(x+1)*step_x] = 255
          isl = draw_islands(complete, isl)
          isl = cv2.rectangle(isl, (x*step_x, y*step_y),((x+1)*step_x,(y+1)*step_y,), color=(0,0,255))
          #lg.info(f"{up_value}, {len(complete)}")
          completeFull.append(complete.copy())
          cv2.imshow('w', isl)
          cv2.imwrite(r"E:\NIRS-BrTSU\py-b\JuPiter-main\images\output\\" + f"{up_value}_{len(complete)}.png", isl)
          cv2.waitKey(10)
          #------------------------------------------------------
          break

      if largest_island_has_been_found == True:
        break

      complete.sort(key=len, reverse=True)
      i=0
      #while i < len(complete):
      #  if complete[i] 
      
cv2.imwrite(PATH_TO_MASK_ + "_test.png", isl)
cv2.imshow('w', isl)
cv2.waitKey()

isl:np.ndarray = img_clr.copy()
for i in completeFull:
  isl = draw_islands(i, isl)
  # cv2.imshow('w', isl)
  # cv2.waitKey(200)
cv2.imwrite(PATH_TO_ISLANDS_JPG, isl)
  

exit()