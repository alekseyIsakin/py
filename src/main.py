from audioop import reverse
from distutils.archive_util import make_archive
from pprint import pprint as pp
from copy import deepcopy
from re import X
from turtle import left
from matplotlib.colors import to_rgba_array

from pandas import array
from logger import lg
import cProfile

from logger import lg, initLogger

from numpy import diff, ndarray
from analisis.loader.img_analizer import *
from analisis.loader.mask_loader import *
from analisis.loader.islands import build_islands_from_fragmets, fragment_calculate
from drawing.draw import *
from drawing.show import *
from constant.paths import PATH_TO_INPUT_, PATH_TO_OUTPUT_

initLogger(lg.DEBUG)

lg.info("Start")

def check_from_dir(island:Island, x:int, y:int, step_x:int, step_y:int):
  
  wall_dir = {'left': 0, 'top': 1, 'right':2, 'down':3, 'scum':4}
  dir_come_from = wall_dir['scum']
  ultraleft_lines = island.get_lines_at_index(island.left)
  
  if island.left == x*step_x:
    dir_come_from = wall_dir['left']              # if island come from left border
  else:
    for left_line in ultraleft_lines:
      if left_line['top'] == y*step_y:               # if island come from top border
        dir_come_from = wall_dir['top']
      elif left_line['down'] == (y+1)*step_y:    # if island come from down border
        dir_come_from = wall_dir['down']
      else:                                       # if island - scum GAGAGA
        dir_come_from = wall_dir['scum']
  
  return dir_come_from

def check_to_dir(island:Island, x:int, y:int, step_x:int, step_y:int):
  wall_dir = {'left': 0, 'top': 1, 'right':2, 'down':3, 'scum':4}
  dir_come_to = wall_dir['scum']

  if island.right >= (x+1)*step_x:
      dir_come_to = wall_dir['right']
  else:
    ultraright_lines = island.get_lines_at_index(island.right)
    for right_line in ultraright_lines:
      if right_line['top'] == y*step_y:
        dir_come_to = wall_dir['top']
      elif right_line['down'] == (y+1)*step_y:
        dir_come_to = wall_dir['down']
      else:                                       
          dir_come_to = wall_dir['scum']

  return dir_come_to

def first_column_fragments(islands:list[Island], x:int, y:int, step_x:int, step_y:int):
  wall_dir = {'left': 0, 'top': 1, 'right':2, 'down':3, 'scum':4}
  success = False
  dir_come_from = wall_dir['scum']
  dir_come_to = wall_dir['scum']
  first_island = True

  if len(islands) == 0:
    return False

  #if len(islands[0]) >= step_x and islands[0].left == x*step_x and islands[0].right == (x+1)*step_x:
  #  return True
  islands.sort(key=lambda x: (x.right - x.left), reverse=True)
  islands.sort(key=lambda x: x.left)

  for single in islands:
    
    dir_come_from = check_from_dir(single,x,y,step_x,step_y)

    if (dir_come_from == wall_dir['scum'] and first_island == False) or (dir_come_from != dir_come_to and dir_come_to != wall_dir['scum']):
      success = False
      continue

    dir_come_to = check_to_dir(single,x,y,step_x,step_y)

    if dir_come_to == wall_dir['right']:
      return True

    if dir_come_from == wall_dir["left"] and dir_come_to == wall_dir["scum"]:
      return False

    if dir_come_to == wall_dir['scum']:
      dir_come_from = wall_dir['scum']
    else:
      first_island = False
      success = True

  return success  

def middle_fragments(islands:list[Island], x:int, y:int, step_x:int, step_y:int):

  if len(islands) == 0:
    return False
  
  wall_dir = {'left': 0, 'top': 1, 'right':2, 'down':3, 'scum':4}
  success = False
  dir_come_from = wall_dir['scum']
  dir_come_to = wall_dir['scum']

  array_of_to = []
  array_of_from = []
  
  #if len(islands[0]) >= step_x and islands[0].left == x*step_x and islands[0].right == (x+1)*step_x:
  #  return True

  
  islands.sort(key=lambda x: x.left)
  #islands.sort(key=lambda x: (x.right - x.left), reverse=True)            #don't touch

  for single in islands:

    dir_come_from = check_from_dir(single,x,y,step_x,step_y)

    if dir_come_from == wall_dir['scum'] or (dir_come_from != dir_come_to and dir_come_to != wall_dir['scum']):
      success = False
      continue

    dir_come_to = check_to_dir(single,x,y,step_x,step_y)

    if dir_come_to == wall_dir['right']:
      return True

    if dir_come_from == wall_dir["left"] and dir_come_to == wall_dir["scum"]:
      continue

    if dir_come_to == wall_dir['scum']:
      dir_come_from = wall_dir['scum']
    else:
      success = True

  return success

#fileName = "nameless.png"
fileName = "test3.png"

img:ndarray     = cv2.imread(PATH_TO_INPUT_ + fileName, cv2.IMREAD_GRAYSCALE)
img_clr:ndarray = cv2.imread(PATH_TO_INPUT_ + fileName)

lg.info(f"load image '{fileName}'")
lg.debug(f"resolution '{fileName}' is {img.shape}")
fragmentsWithIslands:list[list[list[Island]]] = []

#-----------------
# Это база!
count_of_ecg = 4
count_of_col = 5
#-----------------

step_x = img.shape[1] // count_of_col
step_y = img.shape[0] // count_of_ecg
lg.debug(f"step_x [{step_x}], step_y [{step_y}] ")

mask_inv = get_mask_from_gray(img, upper_val=100)
img_isl        :np.ndarray   = img_clr.copy()

black_saturation = [[0 for y in range(img.shape[1] // step_x)] for x in range(img.shape[1] // step_x)]

fragmentsWithIslands = [[] for x in range(img.shape[1] // step_x)]
sequence = [x for x in range(img.shape[1] // step_x)]
y_sequence = [y for y in range(img.shape[0] // step_y)]
x_sequence = []

mid = len(sequence) // 2
x_sequence.append(mid)
l1, l2 = mid, mid

while l1 > 0 and l2 < len(sequence):
  if l1 > 0: 
    l1 -= 1
    x_sequence.append(l1)
  if l2 < len(sequence)-1: 
    l2 += 1
    x_sequence.append(l2)

lg.info(f"start fragment building")
for x in x_sequence:
  for y in y_sequence:
    bottom_line = 150
    upper_line = 255
    step = 1
    for up_value in range(bottom_line,upper_line,step):
      largest_island_has_been_found = False
      lg.debug(f">> step [{x}|{y}][{up_value}]")
      mask_inv = get_mask_from_gray(img, upper_val=up_value)      
      islandsInFragment = fragment_calculate(y*step_y,x*step_x,  step_y+1,step_x+1, mask_inv)

      #i=0
      #while i != len(islandsInFragment):
      #  if len(islandsInFragment[i]) <= 3 or islandsInFragment[i].down - islandsInFragment[i].top <= 2:
      #    del islandsInFragment[i]
      #  else:
      #    i+=1

      one_of_works = False

      # #for single in islandsInFragment:
      if x == 0:
        one_of_works = first_column_fragments(islandsInFragment,x,y,step_x,step_y)
      #   #if len(single) >= step_x and (single.down == (y+1)*step_y or single.right == (x+1)*step_x or single.top == y*step_y):
      #     one_of_works = True
      #     break
      elif x == count_of_ecg:
        one_of_works = True
      #   #if len(single) >= step_x and (single.down == (y+1)*step_y or single.left == x*step_x or single.top == y*step_y):
      #     one_of_works = True
      #     break
      else:
        one_of_works = middle_fragments(islandsInFragment,x,y,step_x,step_y)
         
      
      if one_of_works == True:
        print(f"При насыщенности {up_value} островов найдено {len(islandsInFragment)}")
        #------------------------------------------------------
        img_isl[y*step_y:(y+1)*step_y, x*step_x:(x+1)*step_x] = 255
        img_isl = draw_islands(islandsInFragment, img_isl)
        img_isl = cv2.rectangle(img_isl, (x*step_x, y*step_y),((x+1)*step_x,(y+1)*step_y,), color=(0,0,255))
        lg.info(f"{up_value}, {len(islandsInFragment)}")
        fragmentsWithIslands[x].append(islandsInFragment.copy())
        cv2.imshow('w', img_isl)
        cv2.imwrite(r"E:\NIRS-BrTSU\py-b\JuPiter-main\images\output\\" + f"{up_value}_{len(islandsInFragment)}.png", img_isl)
        cv2.waitKey(10)
        #------------------------------------------------------
        break

      

cv2.imwrite(PATH_TO_OUTPUT_ + "islands1.png", img_isl)


img_isl     :np.ndarray   = np.full_like(img_clr, 255)
complete_isl:list[Island] = build_islands_from_fragmets(fragmentsWithIslands, step_x, step_y)

for isl in complete_isl:
  isl.solidify()

complete_isl = sorted(complete_isl, key=len)

img_isl = draw_islands(complete_isl, img_isl)

cv2.imwrite(PATH_TO_OUTPUT_ + "FinalCut.png",img_isl)

lg.info("fin")
