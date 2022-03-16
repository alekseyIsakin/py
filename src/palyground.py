from collections import deque
from pprint import pprint as pp
from copy import deepcopy
import timeit
from cv2 import imwrite

from logger import lg

from numpy import ndarray
from analisis.loader.img_analizer import *
from analisis.loader.mask_loader import *
from analisis.loader.islands import islands_from_lines
from drawing.draw import *
from drawing.show import *
from constant.paths import PATH_TO_IMAGES, PATH_TO_INPUT_JPG, \
                  PATH_TO_INPUT_, \
                  PATH_TO_ISLANDS_JPG,  \
                  PATH_TO_MASK_JPG, \
                  PATH_TO_MASK_, \
                  PATH_TO_OUTPUT_
import cProfile
import pickle
import timeit
from analisis.classes.classes import Line, Island, line_np_type

# lg.info("palyground start")
# file = "input.jpg"
file = "test5.png"
img:ndarray     = cv2.imread(PATH_TO_INPUT_ + file, cv2.IMREAD_COLOR)

# img = get_mask_from_gray(img, upper_val=100)
# lg.info(f"load image {img.shape}")

# # lines_arr = get_lines(get_mask_from_gray(img).copy())
# # complete = islands_from_lines(lines_arr)
# # lg.info(f"get islands {len(complete)}")

# # with open("test.dt", mode="wb") as f:
# #   pickle.dump(complete, f, protocol=pickle.HIGHEST_PROTOCOL)

# with open("test.dt", mode="rb") as f:
#   complete = pickle.load(f)

# isl = draw_islands(complete, cv2.cvtColor(img, cv2.COLOR_GRAY2BGR))


# with open("test1.bin", mode="wb") as f:
#     pickle.dump({}, f, protocol=pickle.HIGHEST_PROTOCOL)
# with open("test2.bin", mode="wb") as f:
#     pickle.dump({}, f, protocol=pickle.HIGHEST_PROTOCOL)

def test_add(isl1:Island, isl2:Island):
  isl1 = isl1 + isl2
  pass
def test_get_lines(isl:Island, lst):
  for i in lst:
    isl.get_lines_at_index(i)

def test_pop(isl:list):
  while len(isl) > 0:
    isl.pop()

def test_extend(isl:list, isl2:list):
  isl.extend(isl2)

isl = Island()
isl2 = Island()

cnt = 1000
l = np.empty(cnt, dtype=line_np_type)
l['index'] = np.random.randint(0,100, cnt)
l['top'] = np.random.randint(0,100, cnt)
l['down'] = np.random.randint(0,100, cnt)
isl += l

cnt = 10
l = np.empty(cnt, dtype=line_np_type)
l['index'] = np.random.randint(0,100, cnt)
l['top'] = np.random.randint(0,100, cnt)
l['down'] = np.random.randint(0,100, cnt)
isl2 += l

isl = [i for i in range(cnt) ]
isl2 = [i for i in range(cnt) ]
# with open("", 'w') as f:
# isl2 = np.arange(0, cnt, 1)

setup="""
from __main__ import test_extend, isl, isl2
"""

tm = timeit.repeat('test_extend(isl, isl2)', setup=setup, repeat=1_000, number=10_000)
print(np.average(tm))
# imwrite(PATH_TO_OUTPUT_ + "islands.png", isl)
# lg.info(f"fin")
