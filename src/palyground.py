import cProfile

from pprint import pprint as pp
from logger import lg
from logger import lg, initLogger

from numpy import ndarray
from analisis.classes.classes import get_line_dtype
from analisis.loader.img_analizer import *
from analisis.loader.mask_loader import *
from analisis.loader.islands import build_islands_from_fragmets, fragment_calculate
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

fileName = "nameless.png"

img:ndarray          = cv2.imread(PATH_TO_INPUT_ + fileName, cv2.IMREAD_GRAYSCALE)
img_clr:ndarray      = cv2.imread(PATH_TO_INPUT_ + fileName)

img_isl:np.ndarray   = img_clr.copy()

count_of_ecg = 4
count_of_col = 5

step_x = img.shape[1] // count_of_col
step_y = img.shape[0] // count_of_ecg

x_sequence = [2]
y_sequence = [0,1]

bottom_line = 212
upper_line = 255
step = 1

ecg_cells = []
WALL_DIR = _get_dir_dictionary()

for i in range(count_of_ecg):
  ecg_cells.append([[]]*count_of_col)

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
      lg.info(f"{up_value}, {len(islandsInFragment)}")
      cv2.imshow('w', img_isl)
      cv2.waitKey(10)
      #------------------------------------------------------

      one_cell = []

      if x == 0:
        one_of_works = True
        # one_of_works = first_column_fragments(islandsInFragment,x,y,step_x,step_y)
      elif x == count_of_ecg:
        one_of_works = True
      else:
        one_cell = middle_fragments(islandsInFragment,x,y,step_x,step_y)
        one_of_works = len(one_cell) > 0
        ecg_cells[y][x] = one_cell.copy()
      
      if len(ecg_cells[y][x]) == 0:
        continue

      fr_upper_cell = 0
      to_upper_cell = 0
      fr_cur_cell = 0
      to_cur_cell = 0
      
      cv2.imwrite(PATH_TO_OUTPUT_ + f"{x}{y}.png", img_isl)
      if y > 0:
        for direct in ecg_cells[y-1][x]:
          if direct.fr == WALL_DIR['down']:
            fr_upper_cell+=1

          if direct.to == WALL_DIR['down']:
            to_upper_cell+=1
        
        if fr_upper_cell + to_upper_cell > 0:
          for direct in ecg_cells[y][x]:
            if direct.fr == WALL_DIR['top'] and direct.to != WALL_DIR['scum']: 
              fr_cur_cell+=1
            if direct.to == WALL_DIR['top'] and direct.fr != WALL_DIR['scum']:
              to_cur_cell+=1
        
        if fr_cur_cell != to_upper_cell or to_cur_cell != fr_upper_cell:
          one_of_works = False
      
      if one_of_works == True:
        pp(sorted(one_cell, key=lambda x: x.fr))
        cv2.imwrite(PATH_TO_OUTPUT_ + f"out_{x}_{y}_{up_value}.png", img_isl)
        break
