import math as m

def test_connection():
    print('Connected')

def getLine(x, y): #Возвращает предполагаемую ось, принимает 2 массива содержащих координаты точек графика для каждой оси

    ###########functions###########

    def get_min_max(arr): #Максимальное  и минимальное значение в массиве
        cur_max = 0
        cur_min = arr[0]

        for value in arr:
            if (value > cur_max):
                cur_max = value
            elif (value < cur_min):
                cur_min = value
        
        result = [cur_min, cur_max]
        return result

    def get_avg(arr): #Среднее значение в массиве
        avg_val = 0
        for val in arr:
            avg_val += val
        return avg_val/len(arr)

    def get_equation_result(i, j, k):
        return m.exp(i+j*k)

    def perform_exp_interp(): #Апроксимация
        x_sum = 0
        x_sum_pow = 0
        x_log_pow = 0
        y_log = 0
        x_ylog = 0
        n = len(x_linear)

        for ind in range(0, n):
            x_sum += x_linear[ind]
            x_sum_pow += x_linear[ind] ** 2
            y_log += m.log(y_linear[ind])
            x_log_pow += m.log(x_linear[ind]) ** 2
            x_ylog += x_linear[ind] * m.log(y_linear[ind])

        b = (n*x_ylog-x_sum*y_log)/(n*x_sum_pow-x_sum**2) #Экспоненциальная
        a = (1/n)*y_log-(b/n)*x_sum #Экспоненциальная
        
        res = [a, b, n]
        return res

    def perform_clearance(start, tolerance, a, b): #Приземляет значения, нахожящиеся от апроксимации на расстоянии большем tolerance
        for ind in range(start, len(x_linear)):
            y_new = get_equation_result(a, b, x_linear[ind])
            if (m.fabs(y_new - y_linear[ind]) > tolerance):
                #x_linear.remove(x_linear[ind])
                y_linear[ind] = y_new + m.copysign(tolerance, y_new - y_linear[ind])
                perform_clearance(ind - 1, tolerance, a, b)
                return

    ###########functions###########

    x_linear = x.copy()
    y_linear = y.copy()

    koeff = perform_exp_interp()
    perform_clearance(0, 15, koeff[0], koeff[1])
    koeff = perform_exp_interp()

    x1 = []
    y1 = []

    x_min_max = get_min_max(x)
    x1.append(x_min_max[0])
    x1.append(x_min_max[1])
    y_temp = [get_equation_result(koeff[0], koeff[1], x1[0]), get_equation_result(koeff[0], koeff[1], x1[1])]

    y_avg = get_avg(y_linear)
    fault = m.fabs(y_temp[0] - y_avg)-m.fabs(y_temp[1] - y_avg)

    y1.append(y_temp[0]+fault)
    y1.append(y_temp[1]+fault)

    line = [[x1[0], y1[0]], [x1[1], y1[1]]]

    return line