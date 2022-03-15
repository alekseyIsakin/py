from analisis.classes.classes import Line, Island
from analisis.loader.img_analizer import is_neighbours
from logger import lg

def islands_from_lines(graph:list[Line]) -> list[Island]:
  lg.debug('first stage of the island build')
  complete:list[Island] = _first_graph_config(graph)
  lg.debug(f'complete with [{len(complete)}] islands')

  lg.debug('second stage of the island build')
  complete = _second_graph_config(complete)
  lg.debug(f'complete with [{len(complete)}] islands')
  return complete

def _first_graph_config(graph:list[Line]) -> list[Island]:
  raw_islands:list[Island] = []

  while (len(graph) != 0):
    temp = [graph[0]]

    for k in graph[1:]:
      if is_neighbours(temp[-1], k):
        # slow_draw_islands([[temp[-1]], [k]], img_clr.copy(), clr=(0,0,255), sleeptime=100, draw_over=True, scale=(3,3))
        continue
      
      temp.append(k)
    
    # slow_draw_island(temp, img_clr.copy(), sleeptime=500, clr=(0,255,0), draw_over=True)
    isl = Island()

    for i in temp:
      isl.append_one_line(i)
      graph.remove(i)
    raw_islands.append(isl)
  return raw_islands


def _second_graph_config(ecg:list[Island]) -> list[Island]:
  isl_rest = 0
  complete:list[Island] = []
  while len(ecg) > 0:
    start_check_island = ecg[-1][0]

    isl_rest = 0
    
    while isl_rest < len(ecg)-1:
      found = False
      islands = ecg[isl_rest]
      
      if (ecg[-1].minW > islands.maxW or
          ecg[-1].maxW < islands.minW or
          ecg[-1].minH > islands.maxH or
          ecg[-1].maxH < islands.minH):
          # slow_draw_islands([ecg[-1], islands], mask_inv, sleeptime=3)
          isl_rest += 1
          continue

      for line in islands:
        for line2 in ecg[-1]:
          if not is_neighbours(line, line2):
              ecg[-1] = ecg[-1] + islands
              tmp = ecg[-1]
              # slow_draw_island(ecg[-1], mask_inv)
              ecg.remove(islands)
              isl_rest = 0
              found = True
              break
        if found: 
            break
        
      if not found: 
        isl_rest += 1

    complete.append(ecg.pop())
  return complete
    # draw_islands(complete, mask_inv, clr=(255,0,0))
