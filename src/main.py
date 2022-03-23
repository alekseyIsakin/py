from asyncio.windows_events import NULL
import cProfile
from itertools import count

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

initLogger(lg.DEBUG)
lg.info("Start")



def _get_dir_dictionary()->dict:
  return {'left': 0, 'down':1, 'top': 2, 'right':3, 'scum':4, 'none':5}



def check_cnt_top_side(island:Island, y:int, step_y:int) -> int:
  if island.top > y*step_y: return 0

  cnt = 1
  lines = island.get_lines_at_top()
  prev_x = lines[0]['index']

  for line in lines[1:]:
    if line['index'] != prev_x +1:
      cnt += 1
    prev_x = line['index']
  return cnt

def check_cnt_bottom_side(island:Island, y:int, step_y:int) -> int:
  if island.down < (y+1)*step_y: return 0

  cnt = 1
  lines = island.get_lines_at_bottom()
  prev_x = lines[0]['index']

  for line in lines[1:]:
    if line['index'] != prev_x +1:
      cnt += 1
    prev_x = line['index']
  return cnt

def check_from_dir(island:Island, x:int, y:int, step_x:int, step_y:int):
  WALL_DIR = _get_dir_dictionary()
  dir_come_from = WALL_DIR['none']
  ultraleft_lines = island.get_lines_at_index
  
  mid = island.left + island.width//2
  check_index = island.left

  if island.left == x*step_x:
    return WALL_DIR['left']      
      
  while check_index <= mid and dir_come_from == WALL_DIR['none']:
    for left_line in ultraleft_lines(check_index):
      if left_line['top'] == y*step_y:
        dir_come_from = WALL_DIR['top']
      elif left_line['down'] == (y+1)*step_y:
        dir_come_from = WALL_DIR['down']
    check_index += 1
      
  if dir_come_from == WALL_DIR['none']:
    dir_come_from = WALL_DIR['scum']

  return dir_come_from



def check_to_dir(island:Island, x:int, y:int, step_x:int, step_y:int):
  WALL_DIR = _get_dir_dictionary()
  dir_come_to = WALL_DIR['none']
  ultraright_lines = island.get_lines_at_index

  if island.right == (x+1)*step_x:
    return WALL_DIR['right']
  
  mid = island.left + island.width//2
  check_index = island.right

  while check_index >= mid and dir_come_to == WALL_DIR['none']:

    for right_line in ultraright_lines(check_index):
      if right_line['top'] == y*step_y:
        dir_come_to = WALL_DIR['top']
        break
      elif right_line['down'] == (y+1)*step_y:
        dir_come_to = WALL_DIR['down']
        break
    check_index -= 1
      
  if dir_come_to == WALL_DIR['none']:
    dir_come_to = WALL_DIR['scum']
  return dir_come_to



def first_column_fragments(islands:list[Island], x:int, y:int, step_x:int, step_y:int):
  wall_dir = {'left': 0, 'top': 1, 'right':2, 'down':3, 'scum':4}
  success = False
  dir_come_from = wall_dir['scum']
  dir_come_to = wall_dir['scum']
  first_island = True

  if len(islands) == 0:
    return False

  #islands.sort(key=lambda x: (x.right - x.left), reverse=True)
  #if len(islands[0]) >= step_x and islands[0].left == x*step_x and islands[0].right == (x+1)*step_x:
  #  return True

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
    return []
  
  WALL_DIR = _get_dir_dictionary()
  dir_fr_counter = {key:0 for key in WALL_DIR.values()}
  dir_to_counter = {key:0 for key in WALL_DIR.values()}

  dir_couple = namedtuple('couple', ['fr', 'to'])
  fr_to_array:list[dir_couple] = []

  total_top    = 0
  total_bottom = 0

  dir_come_from = WALL_DIR['scum']
  dir_come_to = WALL_DIR['scum']

  islands.sort(key=lambda x: x.left)

  for single in islands:
    dir_come_from = check_from_dir(single,x,y,step_x,step_y)
    dir_come_to = check_to_dir(single,x,y,step_x,step_y)

    fr_to_array.append (
      dir_couple(fr=dir_come_from, to=dir_come_to))

    total_top    += check_cnt_top_side(single, y, step_y)
    total_bottom += check_cnt_bottom_side(single, y, step_y)
  x = 10

  if all([i.fr==WALL_DIR['scum'] for i in fr_to_array]):
    return []

  if all([i.to==WALL_DIR['scum'] for i in fr_to_array if i.fr == WALL_DIR['left']]):
    return []
  
  if all([i.fr==WALL_DIR['scum'] for i in fr_to_array if i.to == WALL_DIR['right']]):
    return []

  if (total_top % 2 != 0 or total_bottom % 2 != 0):
    return []

  fr_to_array.sort(key=lambda x: x.fr)

  return fr_to_array



#|ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ|
#|ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ|
#|ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ|



if __name__ == "__main__":
  
  #fileName = "nameless.png"
  fileName = "test4.png"

  img:ndarray     = cv2.imread(PATH_TO_INPUT_ + fileName, cv2.IMREAD_GRAYSCALE)
  img_clr:ndarray = cv2.imread(PATH_TO_INPUT_ + fileName)

  lg.info(f"load image '{fileName}'")
  lg.debug(f"resolution '{fileName}' is {img.shape}")
  fragmentsWithIslands:list[list[list[Island]]] = []

  #-----------------
  count_of_ecg = 4
  count_of_col = 5
  #-----------------

  ecg_cells = []

  for i in range(count_of_ecg):
    ecg_cells.append([0]*count_of_col)

  step_x = img.shape[1] // count_of_col
  step_y = img.shape[0] // count_of_ecg
  lg.debug(f"step_x [{step_x}], step_y [{step_y}] ")

  mask_inv             = get_mask_from_gray(img, upper_val=100)
  img_isl:np.ndarray   = img_clr.copy()
  WALL_DIR = _get_dir_dictionary()

  fragmentsWithIslands = [[] for x in range(img.shape[1] // step_x)]
  sequence   = [x for x in range(img.shape[1] // step_x)]
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

  cv2.imshow('w', img_isl)
  cv2.waitKey(10)

  lg.info(f"start fragment building")
  for x in x_sequence:
    for y in y_sequence:
      bottom_line = 150
      upper_line = 255
      step = 3
      for up_value in range(bottom_line,upper_line,step):
        lg.debug(f">> step [{x}|{y}][{up_value}]")

        mask_inv = get_mask_from_gray(img, upper_val=up_value)      
        islandsInFragment = fragment_calculate(y*step_y,x*step_x,  step_y+1,step_x+1, mask_inv)

        i=0
        while i != len(islandsInFragment):
          if islandsInFragment[i].width <= 3 and islandsInFragment[i].height <= 3:
            del islandsInFragment[i]
          else:
            i+=1


        #------------------------------------------------------
        img_isl[y*step_y:(y+1)*step_y, x*step_x:(x+1)*step_x] = 255
        img_isl = cv2.rectangle(img_isl, (x*step_x, y*step_y),((x+1)*step_x,(y+1)*step_y,), color=(0,0,255))
        img_isl = draw_islands(islandsInFragment, img_isl)
        cv2.imshow('w', img_isl)
        cv2.waitKey(10)
        #------------------------------------------------------

        one_of_works = False
        one_cell = []

        if x == 0:
          one_of_works = True
          # one_of_works = first_column_fragments(islandsInFragment,x,y,step_x,step_y)
        elif x == count_of_ecg:
          one_of_works = True
        else:
          one_cell = middle_fragments(islandsInFragment,x,y,step_x,step_y)
          one_of_works = len(one_cell) > 0
        

        fr_upper_cell = 0
        to_upper_cell = 0
        fr_cur_cell = 0
        to_cur_cell = 0
        
        if y > 0:
          for direct in ecg_cells[y-1][x]:
            if direct.fr == WALL_DIR['down']:
              fr_upper_cell+=1

            if direct.to == WALL_DIR['down']:
              to_upper_cell+=1
          
          if fr_upper_cell + to_upper_cell > 0:
            for direct in one_cell:
              if direct.fr == WALL_DIR['top'] and direct.to != WALL_DIR['scum']: 
                fr_cur_cell+=1
              if direct.to == WALL_DIR['top'] and direct.fr != WALL_DIR['scum']:
                to_cur_cell+=1
          
          if fr_cur_cell != to_upper_cell or to_cur_cell != fr_upper_cell:
            one_of_works = False


        if one_of_works == True:
          lg.debug(f"При насыщенности {up_value} островов найдено {len(islandsInFragment)}")

          ecg_cells[y][x] = one_cell.copy()
          fragmentsWithIslands[x].append(islandsInFragment.copy())

          cv2.imwrite(PATH_TO_OUTPUT_ + f"{x}_{y}.png", img_isl)
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
