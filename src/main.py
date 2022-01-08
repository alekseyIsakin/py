from pprint import pprint as pp
from funcs import *
from paths import PATH_TO_INPUT_JPG

# E:\Piter\project\src\input.jpg
img = cv2.imread(PATH_TO_INPUT_JPG, cv2.IMREAD_GRAYSCALE)
img_clr = cv2.imread(PATH_TO_INPUT_JPG)

mask_inv = get_mask_from_gray(img)

graph = get_lines(mask_inv)

ecg = []
raw_islands = []

time_start = time.time()
print ("first build islands")

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

time_end = time.time()
print ("finish first build islands", time_end-time_start, end="\n\n\n")

isl_rest = 0
complete = []
ecg = raw_islands

print(len(ecg))
# cv2.imwrite(PATH_TO_ISLANDS_JPG, draw_islands(raw_islands, img_clr.copy(), draw_over=True))

time_start = time.time()
print ("second build islands")    
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

    # print("--------------------------", len(ecg))

  complete.append(ecg.pop())
    # draw_islands(complete, mask_inv, clr=(255,0,0))
time_end = time.time()
print ("finish second build islands", time_end-time_start, end="\n\n\n")  

cv2.imwrite(PATH_TO_ISLANDS_JPG, draw_islands(complete, img_clr.copy()))

# t = get_low_up(get_lines(mask_inv), img)

cv2.imwrite(PATH_TO_MASK_JPG,mask_inv)
# cv2.imwrite(PATH_TO_OUTPUT_JPG,img)
# cv2.imwrite(r'../images/output/output.png',blank3)