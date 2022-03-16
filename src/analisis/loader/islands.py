from cmath import inf
from analisis.classes.classes import Line, Island, line_np_type
from analisis.loader.img_analizer import is_neighbours
from logger import lg
from pprint import pp
import numpy as np



def get_lines(mask_inv:np.ndarray, offset_x=0, offset_y=0) -> list[Line]:
    graph = []

    for j in range(mask_inv.shape[1]):
        higher = inf
        lower = -inf

        cntBlank = 0
        lines = []

        for i in range(mask_inv.shape[0]):
            if mask_inv[i,j] == 255: 
                cntBlank += 1
                if lower == -inf:
                    continue
            
            if lower == -inf: lower = i
            if mask_inv[i,j] != 255: 
                higher = i
                cntBlank = 0
            if cntBlank > 0:
                lines.append(Line(j+offset_y, lower+offset_x, higher+offset_x))
                lower = -inf
                higher = inf
        if lower > -inf:
            lines.append(Line(j+offset_y, lower+offset_x, higher+offset_x))
        for l in lines:
            graph.append(l)
        lines.clear()
    
    return graph



def islands_from_lines(graph:list[Line]) -> list[Island]:
  if (len(graph) == 0):
    return []

  raw_islands:list[Island] = []
  graph = sorted(graph)
  lines_complete:list[Line]  = []
  lines_to_check:list[Line] = [graph.pop(0)]
  
  new_check_line = lines_to_check.append
  new_complete_line = lines_complete.append
  remove_line = graph.remove

  while (len(graph) != 0 or len(lines_to_check) != 0):
    lines_complete.clear()
    if (len(lines_to_check) == 0 and len(graph) != 0):
      lines_to_check.append(graph.pop(0))

    while (len(lines_to_check) > 0):
      cur_line = lines_to_check.pop()
    
      arr_lines = []
      for line2_offset in (-1,0,1):
        arr_lines.extend([l for l in graph if l.index == cur_line.index + line2_offset])
      
      for check_line in arr_lines:
        if not is_neighbours(cur_line, check_line):
          continue
        
        lines_to_check.append(check_line)
        remove_line(check_line)
      new_complete_line(cur_line)

    isl = Island()

    l = np.empty(len(lines_complete), dtype=line_np_type)
    l['index']  = np.array([l.index for l in lines_complete ])
    l['top']    = np.array([l.top   for l in lines_complete ])
    l['down']   = np.array([l.down  for l in lines_complete ])

    isl += l
    # for i in temp:
    #   graph.remove(i)
    raw_islands.append(isl)
  return raw_islands



def fragment_calculate(coord_x:int, coord_y:int,
  step_x:int, step_y:int, mask:np.ndarray) -> list[Island]:
    lines = get_lines(mask [
      coord_x:coord_x + step_x,
      coord_y:coord_y + step_y], coord_x, coord_y)

    islands = islands_from_lines(lines)

    return islands



def _second_graph_config(islands:list[Island], top_bound=-inf, left_bound=-inf) -> list[Island]:
  isl_rest = 0
  complete:list[Island] = []
          
  isl_rest = 0

  while isl_rest < len(islands):
    if (islands[isl_rest].down  +1 < top_bound or 
        islands[isl_rest].right +1 < left_bound) :
      complete.append(islands.pop(isl_rest))
    else:
      isl_rest += 1
  
  if (len(islands) == 0):
    return complete

  remove_isl_gen = islands.remove

  islands_to_check:list[Island] = [islands.pop()]
  add_check_isl = islands_to_check.append
  pop_check_isl = islands_to_check.pop

  future_island:list[Island]    = []
  add_future_isl = future_island.append

  check_lines:list[Line] = []
  check_extend = check_lines.extend
  check_clear = check_lines.clear

  largest_isl_lines = []
  largest_isl_clear = largest_isl_lines.clear
  largest_isl_extend = largest_isl_lines.extend

  while len(islands) > 0 or len(islands_to_check) > 0:
    future_island.clear()

    if (len(islands_to_check) == 0 and len(islands) != 0):
      add_check_isl(islands.pop())

    while (len(islands_to_check) > 0):
      largest_isl = pop_check_isl()

      for check_isl in islands:
        if (largest_isl.right +1 < check_isl.left  or
            largest_isl.left  -1 > check_isl.right or
            largest_isl.down  +1 < check_isl.top   or
            largest_isl.top   -1 > check_isl.down):
            continue
        check_isl_lines = check_isl.get_lines_at_index
        cur_isl_lines = largest_isl.get_lines_at_index
        
        largest_isl_clear()

        if left_bound == -inf and top_bound == -inf:
          largest_isl_extend(largest_isl.lines)
        
        if left_bound != -inf:
          largest_isl_extend(cur_isl_lines(left_bound - 1))
          largest_isl_extend(cur_isl_lines(left_bound + 0))
          largest_isl_extend(cur_isl_lines(left_bound + 1))
        if top_bound != -inf:
          if top_bound == largest_isl.down +1:
            largest_isl_extend(largest_isl.get_lines_at_down())
          if top_bound == largest_isl.top:
            largest_isl_extend(largest_isl.get_lines_at_top())

          largest_isl_extend(largest_isl.lines)
          
        for line in largest_isl_lines:
          check_clear()

          check_extend(check_isl_lines(line['index'] - 1))
          check_extend(check_isl_lines(line['index'] + 0))
          check_extend(check_isl_lines(line['index'] + 1))
          if len(check_lines) == 0: continue

          found = False
          for line2 in check_lines:
            if not is_neighbours(line, line2): continue

            found = True
            add_check_isl(check_isl)
            break
          if found: break
      
      for i in [isl for isl in islands_to_check if isl in islands]:
        remove_isl_gen(i)

      add_future_isl(largest_isl)
    isl = Island()
    for i in future_island:
    # for i in sorted(future_island, key=len):
      isl += i
    complete.append(isl)
  return complete



def build_islands_from_fragmets(fragmentsWithIslands:list[list[list[Island]]], 
    step_x:int, step_y:int) -> list[Island]:
  complete_collumns:list[Island] = []

  lg.debug(f"start fragment building")
  for row_i, row in enumerate(fragmentsWithIslands):
    cur_row = []
    cur_row.extend(row[0])
    for col_i, col in enumerate(row[1:]):
      cur_row.extend(sorted(col, key=len))
      cur_row = _second_graph_config(cur_row, top_bound=col_i*step_y)
      cur_row = sorted(cur_row, key=len)
    lg.debug(f"в колонке {row_i+1}, найденно [{len(cur_row)}] островов")
    complete_collumns.append(cur_row)

  complete_islands:list[Island] = []
  cur_row         :list[Island] = []

  complete_islands.extend(complete_collumns[0])
  for row_i, col in enumerate(complete_collumns[1:]):
    complete_islands.extend(col)
    complete_islands = _second_graph_config(sorted(complete_islands, key=len), left_bound=((row_i+1)*step_x))
    lg.debug(f"строка {row_i+1}, всего найденно [{len(complete_islands)}] островов")
  
  return complete_islands
  # cv2.imwrite(PATH_TO_OUTPUT_ + "islands2.png", img_isl)
