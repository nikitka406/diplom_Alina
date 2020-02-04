from Input_data import *

def searchMax(km_win):
    km_win_max = 0
    for i in range(N):
        for j in range(i, N):
            if km_win[i][j] > km_win_max:
                km_win_max = km_win[i][j]
    for i in range(N):
        for j in range(i, N):
            if km_win[i][j] == km_win_max:
                km_win[i][j] = 0
                return i, j

def searchIndex(km_win, km_win_max):
    for i in range(K):
        for j in range((N+1)*2):
            if km_win[i][j] == km_win_max:
                return i, j
    return -1, -1

def search_pustoy_marchrut(bufer):
    summ = 0
    for k in range(K):
        for i in range((N+1)*2):
            summ += bufer[k][i]
        if summ == 0:
            return k
        summ = 0


# подсчет значения целевой функции
def CalculationOfObjectiveFunction(x, target_function = 0):
    for k in range(K):
        for i in range(N):
            for j in range(N):
                target_function += d[i][j]*x[i][j][k]
    return target_function


# Распределяем на каждую локацию по машине
def Start_solution(bufer):
    # копия переменной задачи Х, только кол-вo машин = число локаций
    x = [[[0 for k in range(K)] for j in range(N)] for i in range(N)]  # едет или нет ТС с номером К из города I в J
    y = [[0 for k in range(K)] for i in range(N)]  # посещает или нет ТС с номером К объект i
    for k in range(K):
        y[0][k] = 1
    s = [[0 for k in range(K)] for i in range(N)]  # время работы ТС c номером К на объекте i
    a = [[0 for k in range(K)] for i in range(N)]  # время прибытия ТС с номером К на объект i

    #

    for k in range(K):
        for i in range(1, (N+1)*2):
            if bufer[k][i] != 0:
                if bufer[k][i+1] == 0:
                    x[bufer[k][i]][0][k] = 1
                    # x[0][bufer[k][i]][k] = 1
                x[bufer[k][i-1]][bufer[k][i]][k] = 1  # туда

                # x[bufer[k][i]][bufer[k][i-1]][k] = 1  # обратно

                y[bufer[k][i-1]][k] = 1
                y[bufer[k][i]][k] = 1

                s[bufer[k][i]][k] = S[bufer[k][i]]

                if e[bufer[k][i]] > t[0][bufer[k][i]] / 24:
                    a[bufer[k][i]][k] = e[bufer[k][i]]
                else:
                    a[bufer[k][i]][k] = t[0][bufer[k][i]] / 24  # иначе начнет, когда приедет
                # print(a[j][k], end=' ')
            # print("\n")


    return x, y, s, a


# Граничные условия
def X_join_Y(x, y, K):
    bufer1 = 0
    bufer2 = 0
    # Add constraint:
    for k in range(K):
        for j in range(N):
            for i in range(N):
                bufer1 += x[i][j][k]
                bufer2 += x[j][i][k]
            if bufer1 != bufer2 or bufer2 != y[j][k] or bufer1 != y[j][k]:
                print("slomalos 1")
                return 0
            bufer1 = 0
            bufer2 = 0
    return 1


def V_jobs(s, K):
    bufer1 = 0
    # Add constraint: sum (s[i][k])==S[i]
    for i in range(1, N):
        if i != 0:
            for k in range(K):
                bufer1 += s[i][k]
            if bufer1 != S[i]:
                print("slomalos 2")
                return 0
            bufer1 = 0
    return 1


def TC_equal_KA(ka, y, K):
    bufer1 =0
    # Add constraint: sum (y[i][k])<=ka[i]
    for i in range(1, N):
        if i != 0:
            for k in range(K):
                bufer1 += y[i][k]
            if bufer1 > ka[i]:
                print(" slomalos 3")
                return 0
            bufer1 = 0
    return 1


def ban_driling(s, y, K):
    # Add constraint: s[i][k] <=S[i]*y[i][k]
    for i in range(1, N):
        for k in range(K):
            if s[i][k] > S[i] * y[i][k]:
                print("slomalos 4")
                return 0
    return 1


def window_time_down(a, y, K):
    # Add constraint: e[i]<=a[i][k]
    for i in range(1, N):
        for k in range(K):
            if e[i] > a[i][k] and y[i][k] == 1:
                print("slomalos 5")#не работает это ограничение
                return 0
    return 1


def window_time_up(a, s, y, K):
    # Add constraint: a[i][k] + s[i][k] <= l[i]
    for i in range(1, N):
        for k in range(K):
            if a[i][k] + s[i][k] > l[i] and y[i][k] == 1:
                print("slomalos 6")
                return 0
    return 1


def ban_cycle(a, x, s, y, K):
    # Add constraint: a[i][k] - a[j][k] +x[i][j][k]*t[i][j] + s[i][k] <= l[i](1-x[i][j][k])
    for i in range(1, N):
        for j in range(1, N):
            for k in range(K):
                if a[i][k] - a[j][k] + x[i][j][k] * t[i][j] + s[i][k] > l[i] * (1 - x[i][j][k]) and y[i][k] == 1:
                    print("slomalos 7")
                    return 0
    return 1


def positive_a_and_s(x, y, a, s, K):
    # Add constraint: s[i][k] >= 0 and a[i][k] >= 0
    for i in range(N):
        for j in range(N):
            for k in range(K):
                if s[i][k] < 0 or a[i][k] < 0:
                    print("slomalos 8")
                    return 0
                if x[i][j][k] != 0 and x[i][j][k] != 1:
                    return 0
                if y[i][k] != 0 and y[i][k] != 1:
                    return 0
    return 1

# проверка выполнения граничных условий
def VerificationOfBoundaryConditions(x, y, s, a):
    result = X_join_Y(x, y, K) * V_jobs(s, K) * TC_equal_KA(skvaj, y, K) * ban_driling(s, y, K) * window_time_down(a, y, K) * window_time_up(a, s, y, K) * ban_cycle(a, x, s, y, K) * positive_a_and_s(x, y, a, s, K)
    if result == 1:
        print("vse ogr rabotayut")  # good
        return 1

    else:
        print("ogr slomalis")
        return 0