from distutils.archive_util import make_archive
from pprint import pprint as pp
from copy import deepcopy
from logger import lg

from numpy import ndarray
from analisis.loader.img_analizer import *
from analisis.loader.mask_loader import *
from analisis.loader.islands import islands_from_lines
from drawing.draw import *
from drawing.show import *
from constant.paths import PATH_TO_INPUT_JPG, \
                  PATH_TO_INPUT_, \
                  PATH_TO_ISLANDS_JPG,  \
                  PATH_TO_MASK_JPG, \
                  PATH_TO_MASK_, \
                  PATH_TO_OUTPUT_JPG
lg.info("Start")

file = r"E:\NIRS-BrTSU\py-b\JuPiter-main\images\input\(190)-test17.png"
img:ndarray     = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
img_clr:ndarray = cv2.imread(PATH_TO_INPUT_ + file)

lg.info(f"load image '{file}'")
lg.debug(f"resolution '{file}' is {img.shape}")
completeFull:list[list[Island]] = []

step_x = img.shape[1] // 5
step_y = img.shape[0] // 4

def fragment_calculate(coord_x:int, coord_y:int,
  step_x:int, step_y:int, mask_inv:np.ndarray) -> list[Island]:
    lines_arr = get_lines(mask_inv [
      coord_x:coord_x + step_x,
      coord_y:coord_y + step_y], coord_x, coord_y)
    complete = islands_from_lines(lines_arr)

    return complete

mask_inv = get_mask_from_gray(img, upper_val=100)
mask = cv2.cvtColor(mask_inv, cv2.COLOR_GRAY2BGR) 
isl = mask.copy()

#def picture_analis(img):
    

for x in range(img.shape[1] // step_x):
  for y in range(img.shape[0] // step_y):
    for up_value in range(180,210,10):
      lg.debug(f">> step [{x}|{y}][{x*step_x}, {y*step_y}]")
      mask_inv = get_mask_from_gray(img, upper_val=up_value)

      # lines_arr = get_lines(mask_inv)
      # complete = islands_from_lines(lines_arr)

      complete = fragment_calculate(y*step_y,x*step_x,  step_y+1,step_x+1, mask_inv)
      
      i=0
      while i != len(complete):
          if len(complete[i]) <= 3 or complete[i].maxH - complete[i].minH <= 2:
              del complete[i]
          else:
              i+=1
      
      isl[y*step_y:(y+1)*step_y, x*step_x:(x+1)*step_x] = 255
      isl = draw_islands(complete, isl)
      isl = cv2.rectangle(isl, (x*step_x, y*step_y),((x+1)*step_x,(y+1)*step_y,), color=(0,0,255))
      completeFull.append(complete.copy())
      lg.info(f"{up_value}, {len(complete)}")
      cv2.imshow('w', isl)
      cv2.imwrite(r"E:\NIRS-BrTSU\py-b\JuPiter-main\images\output\\" + f"{up_value}_{len(complete)}.png", isl)
      cv2.waitKey(200)
      
cv2.imwrite(PATH_TO_MASK_ + "_test.png", isl)

input()

isl:np.ndarray = img_clr.copy()
for i in completeFull:
  isl = draw_islands(i, isl)
  # cv2.imshow('w', isl)
  # cv2.waitKey(200)
cv2.imwrite(PATH_TO_ISLANDS_JPG, isl)
  

exit()

lines_arr = get_lines(mask_inv[:250,:250])
lg.debug(f"find [{len(lines_arr)}] lines")

complete = islands_from_lines(lines_arr)
lg.info(f"find [{len(complete)}] islands")

cv2.imwrite(PATH_TO_ISLANDS_JPG, draw_islands(complete, img_clr.copy(), draw_over=True))

# t = get_low_up(get_lines(mask_inv), img)
test_img = np.ones((img.shape[0],img.shape[1], 3)) * 255
complete[0].smooth()
test_isl:Island = deepcopy(complete[0])
# test_isl.set_wide_x2()

# pnt = get_low_up(test_isl, test_img)
# # pnt = get_low_up(complete[0], test_img)
test_img = draw_islands(complete, test_img)
# sum_avg = 0
# step = 4

# for i in range(step):
#   sum_avg += pnt[i]

# test_img[step-1, int(sum_avg / step)] = (255,0,0)

# t = len(pnt)
# for i, j in enumerate(pnt[step:]):
#   sum_avg = sum_avg - pnt[i] + pnt[i+step]
#   test_img[int(sum_avg/step), complete[0][0].index + i + step] = (255,0,0)

cv2.imwrite(PATH_TO_MASK_JPG, img)
cv2.imwrite(PATH_TO_MASK_ + "_test.png", test_img)
lg.info("complete")

# cv2.imwrite(PATH_TO_OUTPUT_JPG,img)
# cv2.imwrite(r'../images/output/output.png',blank3)
