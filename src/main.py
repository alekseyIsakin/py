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

initLogger(lg.DEBUG)

lg.info("Start")



def _get_dir_dictionary()->dict:
  return {'left': 0, 'down':1, 'top': 2, 'right':3, 'scum':4, 'none':5}



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

  while check_index > mid and dir_come_to == WALL_DIR['none']:
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



def middle_fragments(islands:list[Island], x:int, y:int, step_x:int, step_y:int):
  if len(islands) == 0:
    return []
  
  WALL_DIR = _get_dir_dictionary()
  dir_fr_counter = {key:0 for key in WALL_DIR.values()}
  dir_to_counter = {key:0 for key in WALL_DIR.values()}

  dir_couple = namedtuple('couple', ['fr', 'to'])
  fr_to_array:list[dir_couple] = []

  dir_come_from = WALL_DIR['scum']
  dir_come_to = WALL_DIR['scum']

  islands.sort(key=lambda x: x.left)

  for single in islands:
    
    # if (single.right < (x+1) * step_x and
    #     single.left  > (x)   * step_x and
    #     single.down  < (y+1) * step_y and
    #     single.top   > (y)   * step_y):
    #     continue
    
    dir_come_from = WALL_DIR['scum']
    dir_come_to = WALL_DIR['scum']

    dir_come_from = check_from_dir(single,x,y,step_x,step_y)

    if dir_come_from == WALL_DIR['scum'] or (dir_come_from != dir_come_to and dir_come_to != WALL_DIR['scum']):
      fr_to_array.append (
        dir_couple(fr=dir_come_from, to=dir_come_to))
      dir_fr_counter[dir_come_from] += 1
      dir_to_counter[dir_come_to] += 1
      continue
    
    dir_come_to = check_to_dir(single,x,y,step_x,step_y)

    # if single.width <= 3:
    #   dir_come_to = WALL_DIR['scum']
    
    fr_to_array.append (
      dir_couple(fr=dir_come_from, to=dir_come_to))
    
    dir_fr_counter[dir_come_from] += 1
    dir_to_counter[dir_come_to] += 1
  x = 10

  if len(fr_to_array) == 0:
    return []

  if all([i.fr==WALL_DIR['scum'] for i in fr_to_array]):
    return []

  if all([i.fr == WALL_DIR['left'] and i.to==WALL_DIR['scum'] for i in fr_to_array]):
    return []
  
  if all([i.fr==WALL_DIR['scum'] and i.to == WALL_DIR['right'] for i in fr_to_array]):
    return []

  total_top = dir_fr_counter[WALL_DIR['top']] + dir_to_counter[WALL_DIR['top']]
  total_bottom = dir_fr_counter[WALL_DIR['down']] + dir_to_counter[WALL_DIR['down']]

  if (total_top % 2 != 0 or total_bottom % 2 != 0):
    return []

  # fr_to_array.sort(key=lambda x: x.fr)

  return fr_to_array



def _middle_fragments(islands:list[Island], x:int, y:int, step_x:int, step_y:int):
  if len(islands) == 0:
    return []
  
  WALL_DIR = _get_dir_dictionary()
  dir_fr_counter = {key:0 for key in WALL_DIR.values()}
  dir_to_counter = {key:0 for key in WALL_DIR.values()}

  dir_couple = namedtuple('couple', ['fr', 'to'])
  fr_to_array:list[dir_couple] = []

  dir_come_from = WALL_DIR['scum']
  dir_come_to = WALL_DIR['scum']

  islands.sort(key=lambda x: x.left)

  for single in islands:
    if (single.right < (x+1) * step_x or
        single.left  > (x)   * step_x or
        single.down  < (y+1) * step_y or
        single.top   > (y)   * step_y ):
        continue
    for i in single:
      pass
  return []


if __name__ == "__main__":
  #fileName = "nameless.png"
  fileName = "test1.png"

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

  cv2.imshow('w', img_isl)
  cv2.waitKey(0)

  cells = [[[] for x in range(count_of_col)] for y in range(count_of_ecg)]
  
  lg.info(f"start fragment building")
  for x in x_sequence:
    for y in y_sequence:
      bottom_line = 200
      upper_line = 255
      step = 2
      for up_value in range(bottom_line,upper_line,step):
        lg.debug(f">> step [{x}|{y}][{up_value}]")

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
        black_saturation[x][y] = up_value
        cv2.imshow('w', img_isl)
        cv2.waitKey(10)
        #------------------------------------------------------

        if x == 0:
          one_of_works = True
          # one_of_works = first_column_fragments(islandsInFragment,x,y,step_x,step_y)
        elif x == count_of_ecg:
          one_of_works = True
        else:
          var = middle_fragments(islandsInFragment,x,y,step_x,step_y)
          cells[y][x] = var.copy()
          one_of_works = len(var) > 0
        
        if one_of_works == True:
          lg.debug(f"При насыщенности {up_value} островов найдено {len(islandsInFragment)}")
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
