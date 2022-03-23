import cProfile

from pprint import pprint as pp
from analisis.classes.classes import Fragment_info
from logger import lg
from logger import lg, initLogger

from numpy import ndarray
from analisis.loader.img_analizer import *
from analisis.loader.mask_loader import *
from analisis.loader.islands import build_islands_from_fragmets, fragment_calculate
from constant.other import _get_line_dtype
from drawing.draw import *
from constant.paths import PATH_TO_INPUT_, PATH_TO_OUTPUT_
from collections import namedtuple
from main import middle_fragments, _get_dir_dictionary, check_cnt_top_side, check_cnt_bottom_side

# dtype_line = get_line_dtype()
# isl = Island()
# lines = np.zeros(5, dtype=dtype_line)

# lines['index'] = [ 1,  2,  3,  4,  5]
# lines['top']   = [ 0,  1,  0,  0,  1]
# lines['down']  = [10, 15, 15, 10, 15]

# isl += lines
# isl.solidify()

# img:ndarray = np.ones((30,30))*255
# img = draw_island(isl, img)

# test1 = check_cnt_top_side(isl, 0, 0)
# test2 = check_cnt_bottom_side(isl, 0, 15)

# cv2.imwrite(PATH_TO_OUTPUT_ + 'test.png', img)
# lg.debug(test1)
# lg.debug(test2)
# exit()

fileName = "test2.png"

img:ndarray          = cv2.imread(PATH_TO_INPUT_ + fileName, cv2.IMREAD_GRAYSCALE)
img_clr:ndarray      = cv2.imread(PATH_TO_INPUT_ + fileName)

img_isl:np.ndarray   = img_clr.copy()

count_of_ecg = 4
count_of_col = 5

step_x = img.shape[1] // count_of_col
step_y = img.shape[0] // count_of_ecg

x_sequence = [1]
y_sequence = [2, 3]

bottom_line = 150
upper_line = 255
step = 3

ecg_cells = []
WALL_DIR = _get_dir_dictionary()

for i in range(count_of_ecg):
  ecg_cells.append([Fragment_info()]*count_of_col)

for x in x_sequence:
  for y in y_sequence:
    for up_value in range(bottom_line,upper_line,step):
      mask_inv = get_mask_from_gray(img, upper_val=up_value)      
      islandsInFragment = fragment_calculate(y*step_y,x*step_x,  step_y+1,step_x+1, mask_inv)

      i=0
      while i != len(islandsInFragment):
        if len(islandsInFragment[i]) <= 3 and islandsInFragment[i].down - islandsInFragment[i].top <= 2:
          del islandsInFragment[i]
        else:
          i+=1
      one_of_works = False

      #------------------------------------------------------
      img_isl[y*step_y:(y+1)*step_y, x*step_x:(x+1)*step_x] = 255
      img_isl = cv2.rectangle(img_isl, (x*step_x, y*step_y),((x+1)*step_x,(y+1)*step_y,), color=(0,0,255))
      img_isl = draw_islands(islandsInFragment, img_isl)
      # lg.info(f"{up_value}, {len(islandsInFragment)}")
      cv2.imshow('w', img_isl)
      cv2.waitKey(10)
      #------------------------------------------------------

      one_cell:Fragment_info

      if x == 0:
        one_of_works = True
        # one_of_works = first_column_fragments(islandsInFragment,x,y,step_x,step_y)
      elif x == count_of_ecg:
        one_of_works = True
      else:
        one_cell = middle_fragments(islandsInFragment,x,y,step_x,step_y)
        ecg_cells[y][x] = one_cell
      
      if len(one_cell) == 0:
        continue

      upper_cell_trash = 0
      cur_cell_trash = 0
      
      cv2.imwrite(PATH_TO_OUTPUT_ + f"{x}{y}.png", img_isl)
        
      if y == 0:
        one_of_works = True
      else:
        for direct in ecg_cells[y-1][x]:
          if direct.fr == WALL_DIR['down'] and direct.to == WALL_DIR['scum']:
            upper_cell_trash += 1
          if direct.to == WALL_DIR['down'] and direct.fr == WALL_DIR['scum']:
            upper_cell_trash += 1
        
        expecting_top_crossing = ecg_cells[y-1][x].cnt_bottom_intersection - upper_cell_trash

        for direct in one_cell:
          if direct.fr == WALL_DIR['top'] and direct.to == WALL_DIR['scum']: 
            cur_cell_trash += 1
          if direct.to == WALL_DIR['top'] and direct.fr == WALL_DIR['scum']:
            cur_cell_trash += 1
            
        actually_top_crossing = one_cell.cnt_top_intersection - cur_cell_trash

        if expecting_top_crossing == actually_top_crossing:
          one_of_works = True
      
      if one_of_works == True:
        pp(sorted(one_cell, key=lambda x: x.fr))
        cv2.imwrite(PATH_TO_OUTPUT_ + f"out_{x}_{y}_{up_value}.png", img_isl)
        break
