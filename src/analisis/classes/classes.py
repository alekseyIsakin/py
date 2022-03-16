from asyncio.windows_events import NULL
from cmath import inf, nan
import numpy as np
import cv2

line_np_type = np.dtype([('index', np.int32),('top', np.int32),('down', np.int32)])

class Line():
  def __init__(self, index, top, down) -> None:
    self.index = index
    self.down = down
    self.top = top

  def __getitem__(self, key):
    if key == 0 or key == 'index': return self.index
    if key == 1 or key == 'top':   return self.top
    if key == 2 or key == 'down':  return self.down
    
  def __repr__(self):
    # return ("{ index: " + str(self.index) + ", " +\
    #         "top: " + str(self.top) + ", "+ \
    #         "down: " + str(self.down) + "}")
    return f"<Line. Top: [{self.index}, {self.top}], Bottom: [{self.index}, {self.down}]>"
  
  def __lt__(self, other):
    return self.index < other.index
  def __le__(self, other):
    return self.index <= other.index
  def __gt__(self, other):
    return self.index > other.index
  def __ge__(self, other):
    return self.index >= other.index
  def __eq__(self, other):
    return (self.index == other.index and
            self.top == other.top and
            self.down == other.down)      

  # def is_neighbour(self, other)->bool:
  #   if (abs(self.index - other.index) > 1): return False
  #   if ((self.top <= (other.top+1) and self.top >= (other.down-1)) or
  #         (self.down <= (other.top+1) and self.down >= (other.down-1)) or
  #         (other.top <= (self.top+1) and other.top >= (self.down-1))  or
  #         (other.down <= (self.top+1) and other.down >= (self.down-1))): return True
  #   return False

class Island():
  def __init__(self):
    self.top = 0
    self.left = 0
    self.down = 0
    self.right = 0
    self.line_x_pos = { }
    self.lines_at_down = set()
    self.lines_at_top  = set()
    self._line_dict_step = 25
    self.lines = np.empty(0, dtype=line_np_type)
    pass

  def __getitem__(self, key) -> Line:
    return self.lines[key]
  
  def __len__(self) -> int:
    return len(self.lines)

  def get_lines_at_top(self):
    return [self.lines[i] for i in self.lines_at_top]
  
  def get_lines_at_down(self):
    return [self.lines[i] for i in self.lines_at_down]

  def get_lines_at_index(self, index:int, top:int=-inf, down:int=inf) -> list[Line]:
    if (index -1 > self.right or index +1 < self.left):
      return []
    
    expected_first_index = 0
    expected_last_index = len(self.lines)
    
    expected_first_key = index // self._line_dict_step
    if expected_first_key in self.line_x_pos:
      expected_first_index = self.line_x_pos[expected_first_key]

    expected_last_key = expected_first_key + 1
    if expected_last_key in self.line_x_pos:
      expected_last_index = self.line_x_pos[expected_last_key]

    sequence = self.lines[expected_first_index:expected_last_index]

    return [l for l in sequence if (l['index'] == index) and (l['down'] > top )]

  def sort(self) -> None:
    self.lines = np.sort(self.lines)

  def smooth(self):
    # newlines = [self.lines[0]]
    newlines = np.empty(0, dtype=line_np_type)

    newlines = np.append(newlines, self.lines[0])

    for l in self.lines[1:]:
      if newlines[-1].index != l.index:
        newlines = np.append(newlines, l)
        continue
      newlines[-1].top  = max(newlines[-1].top,  l.top)
      newlines[-1].down = min(newlines[-1].down, l.down)
    self.lines = newlines
  
  def solidify():
    pass

  def __add__(self, other):
    min_new_index = min(other['index'])
    # dict_index_key = (min_new_index // self._line_dict_step) * self._line_dict_step

    # tmp = np.empty(len(self.lines) + len(other), dtype=line_np_type)

    tmp =  np.concatenate((self.lines, other))
    #  = v

    self.top = (np.min(tmp['top']))       # topY
    self.left = (np.min(tmp['index']))     # topX
    self.down = (np.max(tmp['down']))      # downY
    self.right = (np.max(tmp['index']))     # downX

    self.lines = np.sort(tmp)
    key = 0
    # start_index = self.line_x_pos [dict_index_key] if dict_index_key in self.line_x_pos else 0

    for i, line in enumerate(self.lines):
      boundary = (key + 1) * self._line_dict_step
      if line['index'] < boundary: continue

      key = line['index'] // self._line_dict_step
      self.line_x_pos[key] = i

    self.lines_at_top  = set([i for i, l in enumerate(self.lines['top'])  if l == self.top])
    self.lines_at_down = set([i for i, l in enumerate(self.lines['down']) if l == self.down])
    return self

  def __repr__(self):
    return f"<Island. Top: [{self.left}, {self.top}], Bottom: [{self.right}, {self.down}]>"