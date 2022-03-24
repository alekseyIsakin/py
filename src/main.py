import cProfile

from pprint import pprint as pp
from turtle import left
from logger import lg
from logger import lg, initLogger

import numpy as np
import cv2
# from analisis.loader.img_analizer import 
from analisis.loader.mask_loader import get_mask_from_gray
from analisis.loader.islands import build_islands_from_fragmets, fragment_calculate
from analisis.classes.classes import Island, Fragment_info
from constant.paths import PATH_TO_INPUT_, PATH_TO_OUTPUT_
from constant.other import _get_dir_dictionary, _get_fragment_dir_tuple
from drawing.draw import draw_island, draw_islands

initLogger(lg.DEBUG)
lg.info("Start")

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
  cell = Fragment_info()

  if len(islands) == 0:
    return cell
  
  WALL_DIR = _get_dir_dictionary()

  dir_couple = _get_fragment_dir_tuple()
  fr_to_array:list[dir_couple] = []

  total_top    = 0
  total_bottom = 0

  dir_come_from = WALL_DIR['scum']
  dir_come_to = WALL_DIR['scum']

  islands.sort(key=lambda x: x.left)

  for single in islands:
    dir_come_from = check_from_dir(single,x,y,step_x,step_y)
    if (single.width > 3):
      dir_come_to = check_to_dir(single,x,y,step_x,step_y)
    else:
      dir_come_to = WALL_DIR['scum']

    fr_to_array.append (
      dir_couple(fr=dir_come_from, to=dir_come_to))

    total_top    += check_cnt_top_side(single, y, step_y)
    total_bottom += check_cnt_bottom_side(single, y, step_y)
  x = 10

  if all([i.fr==WALL_DIR['scum'] for i in fr_to_array]):
    return cell

  if all([i.to==WALL_DIR['scum'] for i in fr_to_array if i.fr == WALL_DIR['left']]):
    return cell
  
  if all([i.fr==WALL_DIR['scum'] for i in fr_to_array if i.to == WALL_DIR['right']]):
    return cell

  fr_to_array.sort(key=lambda x: x.fr)

  cell.fr_to_array = fr_to_array
  cell.cnt_top_intersection    = total_top
  cell.cnt_bottom_intersection = total_bottom

  return cell

def last_column_fragments(islands:list[Island], x:int, y:int, step_x:int, step_y:int):
  cell = Fragment_info()
  island_len = 0

  if len(islands) == 0:
    return island_len

  WALL_DIR = _get_dir_dictionary()

  dir_come_from = WALL_DIR['scum']
  dir_come_to = WALL_DIR['scum']

  dir_couple = _get_fragment_dir_tuple()
  #fr_to_array:list[dir_couple] = []

  #islands.sort(key=lambda x: x.left)
  islands.sort(key=lambda x: (x.right - x.left), reverse=True)

  for single in islands:
    dir_come_from = check_from_dir(single,x,y,step_x,step_y)
 
    if dir_come_from == WALL_DIR["scum"]:
      return island_len

    if dir_come_from == WALL_DIR["left"] or dir_come_from == WALL_DIR["down"]:
      if (single.width > 3):
        dir_come_to = check_to_dir(islands[0],x,y,step_x,step_y)
        if dir_come_to != WALL_DIR['scum']:
          continue
        else:
          island_len = single.width
          return island_len
  
  return island_len

  # for single in islands:

  #   dir_come_from = check_from_dir(single,x,y,step_x,step_y)

  #   if (single.width > 3):
  #     dir_come_to = check_to_dir(single,x,y,step_x,step_y)
  #   else:
  #     dir_come_to = WALL_DIR['scum']
      
  #   fr_to_array.append (
  #     dir_couple(fr=dir_come_from, to=dir_come_to))

  #   total_top    += check_cnt_top_side(single, y, step_y)
  #   total_bottom += check_cnt_bottom_side(single, y, step_y)
  # x = 10

  # if all([i.fr==WALL_DIR['scum'] for i in fr_to_array]):
  #   return cell

  # if all([i.fr==WALL_DIR['scum'] for i in fr_to_array if i.to == WALL_DIR['right']]):
  #   return cell

  # if all([i.to==WALL_DIR['scum'] for i in fr_to_array if i.fr == WALL_DIR['left']]):
  #   return cell

  # return cell

#|ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ|
#|ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ|
#|ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ|



if __name__ == "__main__":
  
  #fileName = "nameless.png"
  fileName = "test3.png"

  img:np.ndarray     = cv2.imread(PATH_TO_INPUT_ + fileName, cv2.IMREAD_GRAYSCALE)
  img_clr:np.ndarray = cv2.imread(PATH_TO_INPUT_ + fileName)

  lg.info(f"load image '{fileName}'")
  lg.debug(f"resolution '{fileName}' is {img.shape}")
  fragmentsWithIslands:list[list[list[Island]]] = []

  #-----------------
  count_of_ecg = 4
  count_of_col = 5
  #-----------------

  ecg_cells:list[list[Fragment_info]] = []
  cells_saturation = []
  islands_len = []
  counting = 0
  index = 0
  sredn_arifm = 0
  

  for i in range(count_of_ecg):
    ecg_cells.append([0]*count_of_col)
    cells_saturation.append([0]*count_of_col)

  step_x = img.shape[1] // count_of_col
  step_y = img.shape[0] // count_of_ecg
  lg.debug(f"step_x [{step_x}], step_y [{step_y}] ")

  mask_inv             = get_mask_from_gray(img, upper_val=100)
  img_isl:np.ndarray   = img_clr.copy()
  WALL_DIR = _get_dir_dictionary()

  fragmentsWithIslands = [[] for x in range(img.shape[1] // step_x)]
  sequence   = [x for x in range(1, img.shape[1] // step_x -1)]
  y_sequence = [y for y in range(img.shape[0] // step_y)]
  x_sequence = sequence


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
        one_cell:Fragment_info
        
        one_cell = middle_fragments(islandsInFragment,x,y,step_x,step_y)
        
        if len(one_cell) == 0:
          continue

        upper_cell_trash = 0
        cur_cell_trash = 0
        
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
          lg.debug(f"При насыщенности {up_value} островов найдено {len(islandsInFragment)}")

          one_cell.saturation = up_value
          ecg_cells[y][x] = one_cell
          cells_saturation[y][x] = up_value

          if index < (count_of_ecg * (count_of_col-2)):
            sredn_arifm += up_value
            index += 1
          if index == (count_of_ecg * (count_of_col-2)):
            index = (count_of_ecg * count_of_col)
            sredn_arifm /= (count_of_ecg * (count_of_col-2))
            sredn_arifm += 5
              
          fragmentsWithIslands[x].append(islandsInFragment.copy())
          cv2.imwrite(PATH_TO_OUTPUT_ + f"{x}_{y}.png", img_isl)
          break
  
  # x = count_of_ecg
  
  # for y in y_sequence:
  #   bottom_line = 150
  #   upper_line = 255
  #   step = 3
  #   islands_len.clear()
   
  #   bottom_line = round(sredn_arifm)
  #   bottom_line -= step*5

  #   for up_value in range(bottom_line,upper_line,step):

  #     lg.debug(f">> step [{x}|{y}][{up_value}]")
  #     # lg.debug(f">> step [{x}|{y}][{up_value}]")

  #     mask_inv = get_mask_from_gray(img, upper_val=up_value)      
  #     islandsInFragment = fragment_calculate(y*step_y,x*step_x,  step_y+1,step_x+1, mask_inv)

  #     i=0
  #     while i != len(islandsInFragment):
  #       if islandsInFragment[i].width <= 3 and islandsInFragment[i].height <= 3:
  #         del islandsInFragment[i]
  #       else:
  #         i+=1

  #     #------------------------------------------------------
  #     img_isl[y*step_y:(y+1)*step_y, x*step_x:(x+1)*step_x] = 255
  #     img_isl = cv2.rectangle(img_isl, (x*step_x, y*step_y),((x+1)*step_x,(y+1)*step_y,), color=(0,0,255))
  #     img_isl = draw_islands(islandsInFragment, img_isl)
  #     cv2.imshow('w', img_isl)
  #     cv2.waitKey(10)
  #     #------------------------------------------------------


  #     one_of_works = False
  #     one_cell:Fragment_info
  #     len_of_island = 0

  #     len_of_island = last_column_fragments(islandsInFragment,x,y,step_x,step_y)      

  #     if len(islands_len) < 5:
  #       islands_len.append(len_of_island)
  #       continue
    
  #     summ1 = sum(islands_len) - islands_len[-1]
  #     summ2 = sum(islands_len) - islands_len.pop(0)
      
  #     summ1 = summ1/4
  #     summ2 = summ2/4
  #     # didn't work
  #     if (summ2 >= summ1 and summ2 <= summ1 + 5):
  #       continue

  #     upper_cell_trash = 0
  #     cur_cell_trash = 0

  #     if y == 0:
  #       one_of_works = True
  #     else:
  #       for direct in ecg_cells[y-1][x]:
  #         if direct.fr == WALL_DIR['down'] and direct.to == WALL_DIR['scum']:
  #           upper_cell_trash += 1
  #         if direct.to == WALL_DIR['down'] and direct.fr == WALL_DIR['scum']:
  #           upper_cell_trash += 1
        
  #       expecting_top_crossing = ecg_cells[y-1][x].cnt_bottom_intersection - upper_cell_trash

  #       for direct in one_cell:
  #         if direct.fr == WALL_DIR['top'] and direct.to == WALL_DIR['scum']: 
  #           cur_cell_trash += 1
  #         if direct.to == WALL_DIR['top'] and direct.fr == WALL_DIR['scum']:
  #           cur_cell_trash += 1
            
  #       actually_top_crossing = one_cell.cnt_top_intersection - cur_cell_trash

  #       if expecting_top_crossing == actually_top_crossing:
  #         one_of_works = True


  #     if one_of_works == True:
  #       lg.debug(f"При насыщенности {up_value} островов найдено {len(islandsInFragment)}")

  #       one_cell.saturation = up_value
  #       ecg_cells[y][x] = one_cell

  #       fragmentsWithIslands[x].append(islandsInFragment.copy())
  #       cv2.imwrite(PATH_TO_OUTPUT_ + f"{x}_{y}.png", img_isl)
  #       break

        

  cv2.imwrite(PATH_TO_OUTPUT_ + "_islands1.png", img_isl)


  img_isl     :np.ndarray   = np.full_like(img_clr, 255)
  complete_isl:list[Island] = build_islands_from_fragmets(fragmentsWithIslands, step_x, step_y)

  for isl in complete_isl:
    isl.solidify()

  complete_isl = sorted(complete_isl, key=len)

  img_isl = draw_islands(complete_isl, img_isl)

  cv2.imwrite(PATH_TO_OUTPUT_ + "_FinalCut.png",img_isl)

  lg.info("fin")
