import cv2


class Line():
  def __init__(self, index, top, down) -> None:
    self.index = index
    self.down = down
    self.top = top

  def __getitem__(self, key):
    if key == 0: return self.index
    if key == 1: return self.top
    if key == 2: return self.down
    
  def __repr__(self):
    return ("{ index: " + str(self.index) + ", " +\
            "top: " + str(self.top) + ", "+ \
            "down: " + str(self.down) + "}")
  
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


class Island():
  def __init__(self):
    self.maxH = 0
    self.maxW = 0
    self.minH = 0
    self.minW = 0
    self.lines = []
    pass

  def __getitem__(self, key):
    return self.lines[key]
  
  def __len__(self):
    return len(self.lines)
  
  def append_one_line(self, l:Line):
    if len(self.lines) == 0:
      self.lines = [l]
      self.maxH = l.top
      self.maxW = l.index
      self.minH = l.down
      self.minW = l.index
      return
    else:
      self.lines.append(l)
      self.lines = sorted(self.lines)
      
      self.maxH = max(l.top, self.maxH)
      self.maxW = max(l.index, self.maxW)
      self.minH = min(l.down, self.minH)
      self.minW = min(l.index, self.minW)
  
  def __add__(self, other):
    for i in other:
      self.append_one_line(i)
    return self

class App:
  def __init__(self):
    cv2.namedWindow("window")
  def run(self):
    key = ''
    while key != 'q':
        k = cv2.waitKey(0)
        key = chr(k)
        print(k, key)

    cv2.destroyAllWindows()