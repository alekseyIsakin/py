import math as m

def test_connection():
    print('Connected')

def getLine(x, y): #Возвращает предполагаемую ось, принимает 2 массива содержащих координаты точек графика для каждой оси
    
    ###########--functions--###########

    def slide(x,step, parametr):
        for ind_ in range(0, parametr):
            step1 = step
            for ind in range(0, len(x)):
                sum = 0
                max_arr_ind = ind
                min_arr_ind = ind
                if (ind + step1 > len(x)):
                    step1 = len(x) - ind
                for i in range(0, step1):
                    if (ind + i < len(x)):
                        sum += x[ind + i]
                        if (x[ind + i] > x[max_arr_ind]):
                            max_arr_ind = x[ind + i]
                        if (x[ind + i] < x[min_arr_ind]):
                            min_arr_ind = x[ind + i]
                x[max_arr_ind] = m.floor(sum / step1)
                x[min_arr_ind] = m.ceil(sum / step1)
        return x

    def get_min(arr): #Минимальное значение в массиве
        cur_min = arr[0]
        for value in arr:
            if (value < cur_min):
                cur_min = value
        return cur_min

    def get_max(arr):  # Максимальное значение в массиве
        cur_max = 0
        for value in arr:
            if (value > cur_max):
                cur_max = value
        return cur_max

    def get_avg(arr): #Среднее значение в массиве
        avg_val = 0
        for val in arr:
            avg_val += val
        return avg_val/len(arr)

    def get_equation_result(i, j, k):
        return i*k+j

    def perform_exp_interp(): #Регрессия
        x_sum_pow = 0
        xy_sum = 0
        n = len(x)
        avg_x = get_avg(x)
        avg_y = get_avg(y)
        
        for ind in range(0, n):
            x_sum_pow += (x[ind] - avg_x)**2
            xy_sum += (x[ind] - avg_x) * (y[ind] - avg_y)

        a = xy_sum/x_sum_pow
        b = avg_y - a*avg_x

        return [a, b, n]

    def perform_clearance(tolerance, normal): #Приземляет значения, находящиеся от апроксимации на расстоянии большем tolerance
        K=normal[1]-normal[0]
        N=normal[3]-normal[2]
        for ind in range(0, len(x_linear)):
            t=(K*x_linear[ind]+N*y_linear[ind]-K*normal[0]-N*normal[2])/((K**2)+(N**2))
            x_new=K*t+normal[0]
            y_new=N*t+normal[2]
            length=m.sqrt(((x_new-x_linear[ind])**2)+((y_new-y_linear[ind])**2))

            if (length > tolerance):
                x_linear[ind] = m.floor(x_new) + m.copysign(tolerance, x_new - x_linear[ind])
                y_linear[ind] = m.floor(y_new) + m.copysign(tolerance, y_new - y_linear[ind])

    ###########--program--###########
    x_avg = get_avg(x)
    x_min = get_min(x)
    x_max = get_max(x)

    y_avg = get_avg(y)
    y_min = get_min(y)
    y_max = get_max(y)
    

    x_linear = x.copy()
    y_linear = slide(y.copy(), 10, 100) #Сглаживает график по оси OY
    
    koeff = perform_exp_interp() #Строит экспоненциальное уравнение

    tolerance = m.fabs(m.floor(y_max/(y_avg-y_min))+m.floor(y_min/(y_max-y_avg))+m.floor(y_avg/(y_max-y_min))) 
    perform_clearance(tolerance, [x_min, x_max, get_equation_result(koeff[0], koeff[1], x_min), get_equation_result(koeff[0], koeff[1], x_max)]) #Приближает значения OY к экспоненциальной линии
    koeff = perform_exp_interp()

    #Выходные данные - линия вида: [[x1, y1];[x2, y2]]
    line = [[get_min(x_linear), get_equation_result(koeff[0], koeff[1], get_min(x_linear))], [get_max(x_linear), get_equation_result(koeff[0], koeff[1], get_max(x_linear))]]

    return line