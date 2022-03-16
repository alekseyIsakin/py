from audioop import reverse
from distutils.archive_util import make_archive
from pprint import pprint as pp
from copy import deepcopy
from logger import lg
import cProfile

from logger import lg, initLogger

from numpy import ndarray
from analisis.loader.img_analizer import *
from analisis.loader.mask_loader import *
from analisis.loader.islands import build_islands_from_fragmets, fragment_calculate
from drawing.draw import *
from drawing.show import *
from constant.paths import PATH_TO_INPUT_, PATH_TO_OUTPUT_

initLogger(lg.DEBUG)

lg.info("Start")

#fileName = "(190)-test17.png"
fileName = "test6.png"
#fileName = "Screenshot1.png"

img:ndarray     = cv2.imread(PATH_TO_INPUT_ + fileName, cv2.IMREAD_GRAYSCALE)
img_clr:ndarray = cv2.imread(PATH_TO_INPUT_ + fileName)

lg.info(f"load image '{fileName}'")
lg.debug(f"resolution '{fileName}' is {img.shape}")
fragmentsWithIslands:list[list[list[Island]]] = []

#-----------------
# Это база!
count_of_ecg = 4
#-----------------

step_x = img.shape[1] // 5
step_y = img.shape[0] // count_of_ecg
lg.debug(f"step_x [{step_x}], step_y [{step_y}] ")

mask_inv = get_mask_from_gray(img, upper_val=100)
img_isl        :np.ndarray   = img_clr.copy()

lg.info(f"start fragment building")

for x in range(img.shape[1] // step_x):
  fragmentsWithIslands.append([])
  for y in range(img.shape[0] // step_y):
    bottom_line = 170
    upper_line = 255
    step = 1
    for up_value in range(bottom_line,upper_line,step):
      largest_island_has_been_found = False
      #lg.debug(f">> step [{x}|{y}][{x*step_x}, {y*step_y}]")
      mask_inv = get_mask_from_gray(img, upper_val=up_value)      
      islandsInFragment = fragment_calculate(y*step_y,x*step_x,  step_y+1,step_x+1, mask_inv)

      i=0
      while i != len(islandsInFragment):
        if len(islandsInFragment[i]) <= 3 or islandsInFragment[i].down - islandsInFragment[i].top <= 2:
          del islandsInFragment[i]
        else:
          i+=1

      one_of_works = False

      for single in islandsInFragment:
        if x == 0:
          if len(single) >= step_x and (single.down == (y+1)*step_y or single.right == (x+1)*step_x or single.top == y*step_y):
            one_of_works = True
            break
        elif x == count_of_ecg:
          if len(single) >= step_x and (single.down == (y+1)*step_y or single.left == x*step_x or single.top == y*step_y):
            one_of_works = True
            break
        else:
          if len(single) >= step_x and single.left == x*step_x and single.right == (x+1)*step_x:
            one_of_works = True
            break
      
      if one_of_works == True:
        print(f"При насыщенности {up_value} островов найдено {len(islandsInFragment)}")
        #------------------------------------------------------
        img_isl[y*step_y:(y+1)*step_y, x*step_x:(x+1)*step_x] = 255
        img_isl = draw_islands(islandsInFragment, img_isl)
        img_isl = cv2.rectangle(img_isl, (x*step_x, y*step_y),((x+1)*step_x,(y+1)*step_y,), color=(0,0,255))
        #lg.info(f"{up_value}, {len(islandsInFragment)}")
        fragmentsWithIslands[x].append(islandsInFragment.copy())
        cv2.imshow('w', img_isl)
        cv2.imwrite(r"E:\NIRS-BrTSU\py-b\JuPiter-main\images\output\\" + f"{up_value}_{len(islandsInFragment)}.png", img_isl)
        cv2.waitKey(10)
        #------------------------------------------------------
        break

      islandsInFragment.sort(key=len, reverse=True)
      i=0
      #while i < len(islandsInFragment):
      #  if islandsInFragment[i] 
      
cv2.imwrite(PATH_TO_OUTPUT_ + "islands1.png", img_isl)


img_isl     :np.ndarray   = np.full_like(img_clr, 255)
complete_isl:list[Island] = build_islands_from_fragmets(fragmentsWithIslands, step_x, step_y)

for isl in complete_isl:
  isl.solidify()

complete_isl = sorted(complete_isl, key=len)

img_isl = draw_islands(complete_isl, img_isl)

cv2.imwrite(PATH_TO_OUTPUT_ + "FinalCut.png",img_isl)

lg.info("fin")
