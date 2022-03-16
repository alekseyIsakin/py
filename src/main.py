import cProfile
from pprint import pprint as pp
from copy import deepcopy

from logger import lg, initLogger

from numpy import ndarray
from analisis.loader.img_analizer import *
from analisis.loader.mask_loader import *
from analisis.loader.islands import build_islands_from_fragmets, fragment_calculate
from drawing.draw import *
from drawing.show import *
from constant.paths import PATH_TO_INPUT_, PATH_TO_OUTPUT_

#last execute: 1min with 140 black
initLogger(lg.INFO)

lg.info("Start")

# fileName = "test5.png"
fileName = "input.jpg"

img:ndarray     = cv2.imread(PATH_TO_INPUT_ + fileName, cv2.IMREAD_GRAYSCALE)
img_clr:ndarray = cv2.imread(PATH_TO_INPUT_ + fileName)

lg.info(f"load image '{fileName}'")
lg.debug(f"resolution '{fileName}' is {img.shape}")
fragmentsWithIslands:list[list[list[Island]]] = []

step_x = img.shape[1] // 5
step_y = img.shape[0] // 4
# step_y = 80
lg.debug(f"step_x [{step_x}], step_y [{step_y}] ")

mask_inv = get_mask_from_gray(img, upper_val=100)

masks:list[np.ndarray] = []

img_isl        :np.ndarray   = img_clr.copy()
cv2.imshow('w', img_isl)

lg.info(f"start fragment building")
for x in range(mask_inv.shape[1] // step_x):
  fragmentsWithIslands.append([])
  for y in range(mask_inv.shape[0] // step_y):
    # lg.debug(f">> step {i} [{x}|{y}][{x*step_x}, {y*step_y}]")

    islandsInFragment = fragment_calculate(y*step_y,x*step_x,  step_y, step_x, mask_inv)
    # img_isl[y*step_y:(y+1)*step_y, x*step_x:(x+1)*step_x] = 255
    img_isl = draw_islands(islandsInFragment, img_isl)
    img_isl = cv2.rectangle(img_isl, (x*step_x, y*step_y),((x+1)*step_x,(y+1)*step_y,), color=(0,0,255))

    fragmentsWithIslands[x].append(islandsInFragment.copy())

    # lg.debug(f">> coord:{(x,y)}, black:{up_value_from + i*up_value_step}, found [{len(complete)}]")
    cv2.imshow('w', img_isl)
    cv2.waitKey(10)

cv2.imwrite(PATH_TO_OUTPUT_ + "islands1.png", img_isl)

img_isl     :np.ndarray   = np.full_like(img_clr, 255)
complete_isl:list[Island] = build_islands_from_fragmets(fragmentsWithIslands, step_x, step_y)

img_isl = draw_islands(complete_isl, img_isl)
cv2.imwrite(PATH_TO_OUTPUT_ + "islands.png", img_isl)
# complete_isl.extend(sorted(rowsWithIslands[0], key=len))

# del fragmentsWithIslands
lg.info("fin")