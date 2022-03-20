count_of_ecg = 2
count_of_col = 2

ecg_cells = []

for i in range(count_of_ecg):
  ecg_cells.append([0]*count_of_col)

array1 = [[0,1],[1,1],[1,3],[2,2],[2,2]]
array2 = [[0,3],[2,2],[2,2]]

fr_to_coincidences = 0

for i in array1:
  if (i[0] == i[1]):
    fr_to_coincidences+=1

print(fr_to_coincidences)