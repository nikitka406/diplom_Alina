from Input_data import *

N = 13

OX = [10, 17, 6, 13, 9, 19, 8, 4, 17, 12, 6, 19, 12]
OY = [15, 15, 15, 3, 20, 7, 8, 14, 2, 22, 12, 17, 8]

d = [[0 for j in range(N)] for i in range(N)]
for i in range(N):
    for j in range(N):
        d[i][j] = sqrt(pow((OX[i] - OX[j]),2) + pow((OY[i] - OY[j]), 2))

t = d
for i in range(N):
    for j in range(N):
        t[i][j] = round(t[i][j] / 24)

x = [[[0 for k in range(K)] for j in range(N)] for i in range(N)] # едет или нет ТС с номером К из города I в J
y = [[0 for k in range(K)] for i in range(N)] # посещает или нет ТС с номером К объект i
for k in range(K):
    y[0][k] = 1

bufer = [[0 for k in range((N + 1) * 2)]for i in range(K)] #сохраняет последовательное посещение городов для каждой машины
flag = [0 for i in range(N)] # флажок, если посетила город
                             # N так как с обеих сторон должны быть нули (выезжает из депо и возвращ в депо)
s = [[0 for k in range(K)] for i in range(N)]  # время работы ТС c номером К на объекте i
a = [[0 for k in range(K)] for i in range(N)]  # время прибытия ТС с номером К на объект i

#красивая печать
def BeautifulPrint(X, Y, Sresh, A):
    for k in range(K):
        print('Номер машины ', k)
        for i in range(N):
            for j in range(N):
                print(X[i][j][k], end = ' ')
            print("\n")

        print("E = ", end=' ')
        for i in range(N):
            print(E[i], end=' ')
        print("\n")

        print("y = ", end=' ')
        for  i in range(N):
            print(Y[i][k], end=' ')
        print("\n")

        print("a = ", end=' ')
        for  i in range(N):
            print(A[i][k], end=' ')
        print("\n")

        print("s = ", end=' ')
        for  i in range(N):
            print(Sresh[i][k], end=' ')
        print("\n")
    for i in range(N):
        for k in range (N):
           print(t[i][k], end=' ')
        print('\n')

    # for i in range(N):
    #     #     for k in range (N):
    #     #         print(d[i][k], end=' ')
    #     #     print('\n')


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

def Add_vershiny_k_resheniu(bufer, flag, X, Y, Ss, A, x, y, s, a, new_client, car, nomer_sosed, l_p, sosed, kyda):
    bufer[car][nomer_sosed] = new_client
    Y[new_client][car] = 1
    Ss[new_client][car] = S[new_client]
    if E[new_client] >= l_p and kyda == "right":
        A[new_client][car] = E[new_client]
    elif E[new_client] < l_p and kyda == "right":
        A[new_client][car] = l_p

    if E[sosed] >= l_p and kyda == "left":
        A[new_client][car] = E[new_client] - S[j] - t[j][bufer[car][nomer_sosed]]
    elif E[new_client] < l_p and kyda == "left":
        A[new_client][car] = E[new_client] - S[j] - t[j][bufer[car][nomer_sosed]]

    if kyda == "right":
        X[sosed][new_client][car] = 1
        X[sosed][0][car] = 0
        X[new_client][0][car] = 1
    elif kyda == "left":
        X[new_client][sosed][car] = 1
        X[0][sosed][car] = 0
        X[0][new_client][car] = 1

    if VerificationOfBoundaryConditions(X, Y, Ss, A) != 1:
        X = x
        Y = y
        A = a
        Ss = s
    else:
        x = X
        y = Y
        a = A
        s = Ss
        flag[new_client] = 1

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

                x[bufer[k][i-1]][bufer[k][i]][k] = 1  # туда
               # x[bufer[k][i]][bufer[k][i-1]][k] = 1  # обратно

                y[bufer[k][i-1]][k] = 1
                y[bufer[k][i]][k] = 1

                s[bufer[k][i]][k] = S[bufer[k][i]]

                if E[bufer[k][i]] > t[0][bufer[k][i]] / 24:
                    a[bufer[k][i]][k] = E[bufer[k][i]]
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


def TC_equal_K(K, y):
    bufer1 =0
    # Add constraint: sum (y[i][k])<=K[i]
    for i in range(1, N):
        if i != 0:
            for k in range(K):
                bufer1 += y[i][k]
            if bufer1 > skvaj[i]:
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
            if E[i] > a[i][k] and y[i][k] == 1:
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
    result = X_join_Y(x, y, K) * V_jobs(s, K) * TC_equal_K(K, y) * ban_driling(s, y, K) * window_time_down(a, y, K) * window_time_up(a, s, y, K) * ban_cycle(a, x, s, y, K) * positive_a_and_s(x, y, a, s, K)
    if result == 1:
        print("vse ogr rabotayut")  # good
        return 1

    else:
        print("ogr slomalis")
        return 0


def AddTwoCityInRoute(i, j, m, x, y, s, a, bufer):
    X = x
    Y = y
    A = a
    Ss = s
    # print (10)
    indicator = 0
    while indicator != 1:
        bufer[m][N] = j  # двойной массив, где первое - это номер машины, второе - это маршрут
        bufer[m][N + 1] = i
        Y[i][m] = 1
        Y[j][m] = 1
        Ss[i][m] = S[i]
        Ss[j][m] = S[j]
        if E[j] >= t[0][j]:
            A[j][m] = E[j]
            # print(100)
        else:
            A[j][m] = t[0][j]
        A[i][m] = A[j][m] + Ss[j][m] + t[i][j]
        X[0][j][m] = 1
        X[j][i][m] = 1
        X[i][0][m] = 1
        # print(200)
        # BeautifulPrint(X, Y, Ss, A)
        if window_time_up(A, Ss, Y, K) != 1:
            X = x
            Y = y
            A = a
            Ss = s
            bufer[m][N] = i  # двойной массив, где первое - это номер машины, второе - это маршрут
            bufer[m][N + 1] = j
            Y[i][m] = 1
            Y[j][m] = 1
            Ss[i][m] = S[i]
            Ss[j][m] = S[j]
            # print(300)
            if E[i] >= t[0][i]:
                A[i][m] = E[i]
                # print(400)
            else:
                A[i][m] = t[0][i]
                # print(500)
            A[j][m] = A[i][m] + Ss[i][m] + t[i][j]
            X[0][i][m] = 1
            X[i][j][m] = 1
            X[j][0][m] = 1
            indicator = window_time_up(A, Ss, Y, K)
        else:
            x = X
            y = Y
            a = A
            s = Ss
            indicator = window_time_up(A, Ss, Y, K)
            break