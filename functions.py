from Input_data import *
import random

N = 13

OX = [10, 17, 6, 13, 9, 19, 8, 4, 17, 12, 6, 19, 12]
OY = [15, 15, 15, 3, 20, 7, 8, 14, 2, 22, 12, 17, 8]

d = [[0 for j in range(N)] for i in range(N)]
for i in range(N):
    for j in range(N):
        d[i][j] = sqrt(pow((OX[i] - OX[j]), 2) + pow((OY[i] - OY[j]), 2))

t = d
for i in range(N):
    for j in range(N):
        t[i][j] = round(t[i][j] / 24)

x = [[[0 for k in range(K)] for j in range(N)] for i in range(N)]  # едет или нет ТС с номером К из города I в J
y = [[0 for k in range(K)] for i in range(N)]  # посещает или нет ТС с номером К объект i
for k in range(K):
    y[0][k] = 1

bufer = [[0 for k in range((N + 1) * 2)] for i in
         range(K)]  # сохраняет последовательное посещение городов для каждой машины
flag = [0 for i in range(N)]  # флажок, если посетила город
# N так как с обеих сторон должны быть нули (выезжает из депо и возвращ в депо)
s = [[0 for k in range(K)] for i in range(N)]  # время работы ТС c номером К на объекте i
a = [[0 for k in range(K)] for i in range(N)]  # время прибытия ТС с номером К на объект i


# Сохраняем стартовое решение в файл
def SaveSolution(local_x, local_y, local_s, local_a, output, option):
    file = open(output, option)

    # Печатаем в файл Х
    for i in range(N):
        for j in range(N):
            for k in range(K):
                file.write(str(local_x[i][j][k]) + ' ')
            file.write("\n")
        # file.write("\n")
    # Печатаем в файл Y
    for i in range(N):
        for k in range(K):
            file.write(str(local_y[i][k]) + ' ')
        file.write("\n")
    # Печатаем в файл S
    for i in range(N):
        for k in range(K):
            file.write(str(local_s[i][k]) + ' ')
        file.write("\n")
    # Печатаем в файл A
    for i in range(N):
        for k in range(K):
            file.write(str(local_a[i][k]) + ' ')
        file.write("\n")

    file.close()


# Читаем стартовое решение в файле
def ReadSolutionOfFile(local_x, local_y, local_s, local_a, output):
    file = open(output, 'r')
    # прочитали весь файл, получился список из строк файла
    line = file.readlines()

    index = 0
    # Печатаем в файл Х
    for i in range(N):
        for j in range(N):
            # for k in range(K):
            local_x[i][j] = line[index].split()
            for k in range(len(local_x[i][j])):
                local_x[i][j][k] = int(local_x[i][j][k])
            index += 1

    # Печатаем в файл Y
    for i in range(N):
        local_y[i] = line[index].split()
        for k in range(len(local_y[i])):
            local_y[i][k] = int(local_y[i][k])
        index += 1
    # Печатаем в файл S
    for i in range(N):
        local_s[i] = line[index].split()
        for k in range(len(local_s[i])):
            local_s[i][k] = float(local_s[i][k])
        index += 1
    # Печатаем в файл A
    for i in range(N):
        local_a[i] = line[index].split()
        for k in range(len(local_a[i])):
            local_a[i][k] = float(local_a[i][k])
        index += 1
    file.close()


def SaveTabu(arr, target):
    file = open("TabuSearch.txt", 'a')
    print("arr[i] = ", arr)
    for i in range(6):
        print("arr[i] = ", arr[i])
        file.write(str(arr[i]) + ' ')
    file.write('\n')
    file.write(str(target)+'\n')
    file.close()


#
def ReadTabu(arr, target):
    file = open("TabuSearch.txt", 'r')
    line = file.readlines()
    i = 0
    index = 0
    print(len(line))
    while index < len(line):
        print("i", i)
        arr[i] = line[index].split()

        for j in range(len(arr[i])):
            # print(arr[i][j])
            arr[i][j] = int(arr[i][j])

        index += 1
        target[i] = line[index].split()[0]
        target[i] = float(target[i])
        print("target = ", target)

        index += 1
        i += 1

def SeekTabu():
    file = open("TabuSearch.txt", 'r+')

def ClearTabu():
    file = open("TabuSearch.txt", 'w')
    file.close()
# красивая печать в файл
def BeautifulPrintInFile(loKl_X, loKl_Y, loKl_Ss, loKl_A, target_function, number_solution):
    file = open('population.txt', 'a')
    file.write('Номер решения ' + str(number_solution))
    file.write("\n")
    for k in range(len(loKl_X[0][0])):
        file.write('Номер машины ' + str(k))
        file.write("\n")
        for i in range(N):
            for j in range(N):
                file.write(str(loKl_X[i][j][k]) + ' ')
            file.write("\n")
        file.write("\n")

        file.write("e = ")
        for i in range(N):
            file.write(str(e[i]) + ' ')
        file.write("\n")

        file.write("l = ")
        for i in range(N):
            file.write(str(l[i]) + ' ')
        file.write("\n")

        file.write("y = ")
        for i in range(N):
            file.write(str(loKl_Y[i][k]) + ' ')
        file.write("\n")

        file.write("a = ")
        for i in range(N):
            file.write(str(loKl_A[i][k]) + ' ')
            # for k in range(K):
            #     print(A[i][k], end=' ')
            # print("\n")
        file.write("\n")

        file.write("s = ")
        for i in range(N):
            file.write(str(loKl_Ss[i][k]) + ' ')
            # for k in range(K):
            #     print(Ss[i][k], end=' ')
            # print("\n")
        file.write("\n")
    file.write(str(target_function))
    file.write("\n")
    file.write("\n")
    # for i in range(N):
    #     for k in range (N):
    #        file.write(t[i][k]+' ')
    #     file.write('\n')

    # for i in range(N):
    #     #     for k in range (N):
    #     #         print(d[i][k], end=' ')
    #     #     print('\n')
    file.close()

# красивая печать
def BeautifulPrint(X, Y, Ss, A):
    for k in range(K):
        print('Номер машины ', k)
        for i in range(N):
            for j in range(N):
                print(X[i][j][k], end=' ')
            print("\n")

        print("E = ", end=' ')
        for i in range(N):
            print(E[i], end=' ')
        print("\n")

        print("y = ", end=' ')
        for i in range(N):
            print(Y[i][k], end=' ')
        print("\n")

        print("a = ", end=' ')
        for i in range(N):
            print(A[i][k], end=' ')
        print("\n")

        print("s = ", end=' ')
        for i in range(N):
            print(Ss[i][k], end=' ')
        print("\n")
    for i in range(N):
        for k in range(N):
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
        for j in range((N + 1) * 2):
            if km_win[i][j] == km_win_max:
                return i, j
    return -1, -1


def search_pustoy_marchrut(bufer):
    summ = 0
    for k in range(K):
        for i in range((N + 1) * 2):
            summ += bufer[k][i]
        if summ == 0:
            return k
        summ = 0


# штрафная функция
def shtrafFunction(s, a):
    shtraf_sum = 0
    for i in range(N):
        for k in range(K):
            if a[i][k] + s[i][k] > l[i]:
                shtraf_sum += ((a[i][k] + s[i][k]) - l[i]) * shtraf
    return shtraf_sum


# подсчет значения целевой функции
def CalculationOfObjectiveFunction(x, shtrafFunction=0):
    target_function = 0
    for k in range(K):
        for i in range(N):
            for j in range(N):
                target_function += d[i][j] * x[i][j][k]
    target_function += shtrafFunction
    print("target_function в самой функции подсчета = ", target_function)
    return target_function


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
                print("slomalos 1: связность маршрутов x и y")
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
                print("slomalos 2: общий объем работ на каждом объекте")
                return 0
            bufer1 = 0
    return 1


def TC_equal_K(K, y):
    bufer1 = 0
    # Add constraint: sum (y[i][k])<=K[i]
    for i in range(1, N):
        if i != 0:
            for k in range(K):
                bufer1 += y[i][k]
            if bufer1 > skvaj[i]:
                print(" slomalos 3: ТС не больше, чем скважин")
                return 0
            bufer1 = 0
    return 1


def ban_driling(s, y, K):
    # Add constraint: s[i][k] <=S[i]*y[i][k]
    for i in range(1, N):
        for k in range(K):
            if s[i][k] > S[i] * y[i][k]:
                print("slomalos 4: установка не работает, если не приехала на объект")
                return 0
    return 1


def window_time_down(a, y, K):
    # Add constraint: e[i]<=a[i][k]
    for i in range(1, N):
        for k in range(K):
            if E[i] > a[i][k] and y[i][k] == 1:
                print("slomalos 5: нельзя начать работу раньше, чем приехал")  # не работает это ограничение
                return 0
    return 1


def window_time_up(a, s, y, K):
    # Add constraint: a[i][k] + s[i][k] <= l[i]
    for i in range(1, N):
        for k in range(K):
            if a[i][k] + s[i][k] > l[i] and y[i][k] == 1:
                print("slomalos 6: нельзя закончить работу позже, чем временное окно")
                return 0
    return 1


def ban_cycle(a, x, s, y, K):
    # Add constraint: a[i][k] - a[j][k] +x[i][j][k]*t[i][j] + s[i][k] <= l[i](1-x[i][j][k])
    for i in range(1, N):
        for j in range(1, N):
            for k in range(K):
                if a[i][k] - a[j][k] + x[i][j][k] * t[i][j] + s[i][k] > l[i] * (1 - x[i][j][k]) and y[i][k] == 1:
                    print("slomalos 7:запрещ циклы, которые не проходят через депо")
                    return 0
    return 1


def positive_a_and_s(x, y, a, s, K):
    # Add constraint: s[i][k] >= 0 and a[i][k] >= 0
    for i in range(N):
        for j in range(N):
            for k in range(K):
                if s[i][k] < 0 or a[i][k] < 0:
                    print("slomalos 8: область изменения перменных")
                    return 0
                if x[i][j][k] != 0 and x[i][j][k] != 1:
                    return 0
                if y[i][k] != 0 and y[i][k] != 1:
                    return 0
    return 1


# проверка выполнения граничных условий
def VerificationOfBoundaryConditions(x, y, s, a, shtraf="false"):
    # по дефолту смотрим все огр, но если тру то не рассматриваем огр на своевременный конец работ
    if shtraf == "false":
        result = X_join_Y(x, y, K) * V_jobs(s, K) * TC_equal_K(K, y) * ban_driling(s, y, K) * \
                 window_time_down(a, y, K) * window_time_up(a, s, y, K) * \
                 ban_cycle(a, x, s, y, K) * positive_a_and_s(x, y, a, s, K)
    elif shtraf == "true":
        result = X_join_Y(x, y, K) * V_jobs(s, K) * TC_equal_K(K, y) * ban_driling(s, y, K) * \
                 window_time_down(a, y, K) * \
                 positive_a_and_s(x, y, a, s, K)
    else:
        print("ERROR from VerificationOfBoundaryConditions: неверное значение, переменной shtraf")
        return -1
    if result == 1:
        return 1  # good
    else:
        return 0


# проверка выполнения граничных условий
def VerificationOfBoundaryConditionsForStartSolution(x, y, s, a):
    # по дефолту смотрим все огр, но если тру то не рассматриваем огр на своевременный конец работ
    result = window_time_down(a, y, K) * window_time_up(a, s, y, K)

    if result == 1:
        return 1  # good
    else:
        return 0


# def Add_vershiny_k_resheniu(bufer, flag, X, Y, Ss, A, x, y, s, a, new_client, car, nomer_sosed, l_p, sosed, kyda):
#     if E[
#         new_client] >= l_p and kyda == "right":  # если время начала работы нового клиента больше чем время прибытия + работы + переезда предыдущего
#         A[new_client][car] = E[new_client]
#         Zapolnenie(X, Y, Ss, "right", new_client, sosed, car, nomer_sosed)
#     elif E[new_client] < l_p and kyda == "right":
#         A[new_client][car] = l_p
#         Zapolnenie(X, Y, Ss, "right", new_client, sosed, car, nomer_sosed)
#
#     if A[sosed][car] >= l_p and kyda == "left":
#         A[new_client][car] = A[sosed][car] - S[new_client] - t[new_client][bufer[car][nomer_sosed]]
#         Zapolnenie(X, Y, Ss, "left", new_client, sosed, car, nomer_sosed)
#         if A[new_client][car] <= E[new_client]:
#             A[new_client][car] = E[new_client]
#     elif A[sosed][car] < l_p and kyda == "left":
#         print("ne podhodit dlya marchruta")
#
#     # if E[sosed] >= l_p and kyda == "left":
#     #     A[new_client][car] = t[0][new_client]
#     #     # A[new_client][car] = E[sosed] - S[new_client] - t[new_client][bufer[car][nomer_sosed]]
#     #
#     # elif E[sosed] < l_p and kyda == "left":
#     #     A[new_client][car] = E[new_client] - S[new_client] - t[new_client][bufer[car][nomer_sosed]]
#
#     if VerificationOfBoundaryConditionsForStartSolution(X, Y, Ss, A) != 1:
#         X = x
#         Y = y
#         A = a
#         Ss = s
#     else:
#         x = X
#         y = Y
#         a = A
#         s = Ss
#         flag[new_client] = 1


# def AddTwoCityInRoute(i, j, m, x, y, s, a, bufer):
#     X = x
#     Y = y
#     A = a
#     Ss = s
#
#     if E[j] >= t[0][j]:
#         A[j][m] = E[j]
#     else:
#         A[j][m] = t[0][j]
#
#     if A[j][m] + Ss[j][m] + t[j][i] <= l[i] - Ss[i][m]:
#         bufer[m][N] = j  # двойной массив, где первое - это номер машины, второе - это маршрут
#         bufer[m][N + 1] = i
#
#         Y[j][m] = 1
#         Y[i][m] = 1
#         Ss[j][m] = S[j]
#         Ss[i][m] = S[i]
#
#         if E[j] >= t[0][j]:
#             A[j][m] = E[j]
#         else:
#             A[j][m] = t[0][j]
#
#         A[i][m] = A[j][m] + Ss[j][m] + t[i][j]
#
#         if A[i][m] <= E[i]:
#             A[i][m] = E[i]
#
#         X[0][j][m] = 1
#         X[j][i][m] = 1
#         X[i][0][m] = 1
#         # print(200)
#         # BeautifulPrint(X, Y, Ss, A)
#         flag[i] = 1
#         flag[j] = 1
#
#
#     if E[i] >= t[0][i]:
#         A[i][m] = E[i]
#     else:
#         A[i][m] = t[0][i]
#
#
#     elif A[i][m] + Ss[i][m] + t[i][j] <= l[j] - Ss[j][m]:
#         # if window_time_up(A, Ss, Y, K) != 1:
#         X[0][j][m] = 0
#         X[j][i][m] = 0
#         X[i][0][m] = 0
#         bufer[m][N] = i  # двойной массив, где первое - это номер машины, второе - это маршрут
#         bufer[m][N + 1] = j
#         Y[i][m] = 1
#         Y[j][m] = 1
#         Ss[i][m] = S[i]
#         Ss[j][m] = S[j]
#
#         if E[i] >= t[0][i]:
#             A[i][m] = E[i]
#         else:
#             A[i][m] = t[0][i]
#
#         A[j][m] = A[i][m] + Ss[i][m] + t[i][j]
#         if A[j][m] <= E[j]:
#             A[j][m] = E[j]
#         X[0][i][m] = 1
#         X[i][j][m] = 1
#         X[j][0][m] = 1
#
#
#         flag[i] = 1
#         flag[j] = 1
#
#
#
#
#         # indicator = window_time_up(A, Ss, Y, K)
#     else:
#         print("AddTwoCityInRoute: нельзя создать новый маршрут из-за временных окон")
#         x = X
#         y = Y
#         a = A
#         s = Ss


def AddTwoCityInRoute(i, j, m, x, y, s, a, bufer):
    X = x
    Y = y
    A = a
    Ss = s

    if E[j] >= t[0][j]:
        A[j][m] = E[j]
    else:
        A[j][m] = t[0][j]

    if E[i] >= t[0][i]:
        A[i][m] = E[i]
    else:
        A[i][m] = t[0][i]

    # если временные рамки не нарушаются при вставлении j i и i j, то вставляем j i
    if A[j][m] + Ss[j][m] + t[j][i] <= l[i] - Ss[i][m] and A[i][m] + Ss[i][m] + t[i][j] <= l[j] - Ss[j][m]:
        bufer[m][N] = j  # двойной массив, где первое - это номер машины, второе - это маршрут
        bufer[m][N + 1] = i

        Y[j][m] = 1
        Y[i][m] = 1
        Ss[j][m] = S[j]
        Ss[i][m] = S[i]

        # if E[j] >= t[0][j]:
        #     A[j][m] = E[j]
        # else:
        #     A[j][m] = t[0][j]

        A[i][m] = A[j][m] + Ss[j][m] + t[i][j]

        if A[i][m] <= E[i]:
            A[i][m] = E[i]

        X[0][j][m] = 1
        X[j][i][m] = 1
        X[i][0][m] = 1
        # print(200)
        # BeautifulPrint(X, Y, Ss, A)
        # flag[i] = 1
        # flag[j] = 1

    elif A[j][m] + Ss[j][m] + t[j][i] <= l[i] - Ss[i][m] and A[i][m] + Ss[i][m] + t[i][j] > l[j] - Ss[j][m]:
        bufer[m][N] = j  # двойной массив, где первое - это номер машины, второе - это маршрут
        bufer[m][N + 1] = i

        Y[j][m] = 1
        Y[i][m] = 1
        Ss[j][m] = S[j]
        Ss[i][m] = S[i]

        # if E[j] >= t[0][j]:
        #     A[j][m] = E[j]
        # else:
        #     A[j][m] = t[0][j]

        A[i][m] = A[j][m] + Ss[j][m] + t[i][j]

        if A[i][m] <= E[i]:
            A[i][m] = E[i]

        X[0][j][m] = 1
        X[j][i][m] = 1
        X[i][0][m] = 1
        # print(200)
        # BeautifulPrint(X, Y, Ss, A)
        # flag[i] = 1
        # flag[j] = 1


    elif A[j][m] + Ss[j][m] + t[j][i] > l[i] - Ss[i][m] and A[i][m] + Ss[i][m] + t[i][j] <= l[j] - Ss[j][m]:
        # if window_time_up(A, Ss, Y, K) != 1:
        # X[0][j][m] = 0
        # X[j][i][m] = 0
        # X[i][0][m] = 0
        bufer[m][N] = i  # двойной массив, где первое - это номер машины, второе - это маршрут
        bufer[m][N + 1] = j
        Y[i][m] = 1
        Y[j][m] = 1
        Ss[i][m] = S[i]
        Ss[j][m] = S[j]

        # if E[i] >= t[0][i]:
        #     A[i][m] = E[i]
        # else:
        #     A[i][m] = t[0][i]

        A[j][m] = A[i][m] + Ss[i][m] + t[i][j]

        if A[j][m] <= E[j]:
            A[j][m] = E[j]

        X[0][i][m] = 1
        X[i][j][m] = 1
        X[j][0][m] = 1

        # flag[i] = 1
        # flag[j] = 1

        # indicator = window_time_up(A, Ss, Y, K)
    else:
        print("AddTwoCityInRoute: нельзя создать новый маршрут из-за временных окон")
        flag[i] = 0
        flag[j] = 0
        # x = X
        # y = Y
        # a = A
        # s = Ss


# Считаем кол-во используемых ТС
def AmountCarUsed(y):
    summa = 0  # счетчик
    amount = 0  # число машин
    for k in range(K):
        for j in range(N):
            summa += y[j][k]  # смотрим посещает ли К-ая машина хотя бы один город
        if summa != 0:  # если не 0 значит  посетила
            amount += 1  # прибавляем еденичку
        summa = 0  # Обнуляем счетчик
    return amount


# копирование решения
def CopyingSolution(x, y, s, a):
    X = x.copy()
    Y = y.copy()
    Ss = s.copy()
    A = a.copy()
    return X, Y, Ss, A


# ищем минимальный путь по которому можно попасть в client
def SearchTheBestSoseda(client):
    neighbor = 0  # старый сосед
    bufer = d[0][client]  # расстояние от старого соседа до клиента
    for i in range(N):
        if bufer >= d[i][client] and i != client:  # ищем мин расстояние до клиента с учетом что новый сосед не клиент
            bufer = d[i][client]
            neighbor = i
    return neighbor


# номер машины которая обслуживает клиента
def NumberCarClienta(y, client):
    for k in range(K):
        if y[client][k] == 1:
            return k
    return "не найдена машина NumberCarClienta"


# ищем соседа слева либо справа
def SearchSosedLeftOrRight(x, y, client, leftOrRight):
    k = NumberCarClienta(y, client)  # номер машины которая обслуживает клиента
    # print("номер машины, которая обслуживает клиента ", k)
    if leftOrRight == "left":
        for i in range(N):  # ищем по столбцу
            if x[i][client][k] == 1:
                return i
        return -1
    if leftOrRight == "right":
        for i in range(N):  # ищем по строке
            if x[client][i][k] == 1:
                return i
        return -1
    if leftOrRight != "left" and leftOrRight != "right":
        print("ERROR from SearchSosedLeftOrRight: неверное значение переменной leftOrRight")


# определяем время приезда на конкретную локацию
def TimeOfArrival(a, s, client, sosed, sosedK):
    # если время прибытия меньше начала работ, то ждем
    if E[client] > a[sosed][sosedK] + s[sosed][sosedK] + t[sosed][client]:
        a[client][sosedK] = E[client]
    # иначе ставим время прибытия
    else:
        a[client][sosedK] = a[sosed][sosedK] + s[sosed][sosedK] + t[sosed][client]


# удаляем клиента из выбранного  маршрута и соединяем соседние вершины
def DeleteClientaFromPath(x, y, s, a, client):
    k = NumberCarClienta(y, client)  # номер машины которая обслуживает клиента
    clientLeft = SearchSosedLeftOrRight(x, y, client, "left")  # ищем город перед клиентом
    clientRight = SearchSosedLeftOrRight(x, y, client, "right")  # ищем город после клиента
    # если у клиента есть сосед справа и слева
    if clientLeft != -1 and clientRight != -1:
        if clientLeft != clientRight:
            x[clientLeft][clientRight][k] = 1  # соединяем левого и правого соседа

        else:
            x[clientLeft][clientRight][k] = 0

        x[client][clientRight][k] = 0  # удаляем ребро клиента с правым соседом
        x[clientLeft][client][k] = 0  # удаляем ребро клиента с левым соседом

        # У и S для левого и правого не меняются, но время прибытия меняется
        y[client][k] = 0  # машина К больше не обслуживает клиента
        s[client][k] = 0  # время работы машины К у клиента = 0
        a[client][k] = 0  # машина не прибывает к клиенту
        TimeOfArrival(a, s, clientRight, clientLeft, k)

        # если удаляем клиента и остается только депо, ставим там 0
        summa = 0
        for i in range(1, N):
            summa += y[i][k]
        if summa == 0 and y[0][k] == 1:
            y[0][k] = 0

    # если клиент лист
    if clientLeft != -1 and clientRight == -1:
        print("ERROR from DeleteClientaFromPath: такого не может быть: нет ни левого ни правого соседа")


# удаляем клиента из выбранного маршрута без соединения соседних вершин для TwoOpt
def DeleteClientaForTwoOpt(x, y, s, a, client):
    k = NumberCarClienta(y, client)  # номер машины которая обслуживает клиента
    clientLeft = SearchSosedLeftOrRight(x, y, client, "left")  # ищем город перед клиентом
    clientRight = SearchSosedLeftOrRight(x, y, client, "right")  # ищем город после клиента
    # если у клиента есть сосед справа и слева
    if clientLeft != -1 and clientRight != -1:
        # x[clientLeft][clientRight][k] = 1  # соединяем левого и правого соседа
        x[client][clientRight][k] = 0  # удаляем ребро клиента с правым соседом
        x[clientLeft][client][k] = 0  # удаляем ребро клиента с левым соседом

        # У и S для левого и правого не меняются, но время прибытия меняется
        y[client][k] = 0  # машина К больше не обслуживает клиента
        s[client][k] = 0  # время работы машины К у клиента = 0
        a[client][k] = 0  # машина не прибывает к клиенту

        TimeOfArrival(a, s, clientRight, clientLeft, k)
    # если у клиента есть сосед слева, а справо депо
    if clientLeft != -1 and clientRight == 0:
        # x[clientLeft][client][k] = 0  # теперь после левого соседа машина К никуда не едет кроме депо

        # x[client][0][k] = 0  # а клиент не возвращается в депо
        y[client][k] = 0  # клиент больше не обслуживается машиной К
        s[client][k] = 0  # машиной К больше не тратит время у клиента
        a[client][k] = 0  # и не приезжает
    if clientLeft == -1:  # logir
        print("ERROR from DeleteClientaFromPath: такого не может быть нет ни левого ни правого соседа")



# оператор перемещения!!!
# вклиниваем между
def JoinClientaNonList(x, y, s, a, client, sosed, arr, p, target_function):  # ОПЕРАТОР ПЕРЕМЕЩЕНИЯ! # (arr, p)
    sosedK = NumberCarClienta(y, sosed)
    clientK = NumberCarClienta(y, client)

    sosedLeft = SearchSosedLeftOrRight(x, y, sosed, "left")  # левый сосед соседа
    sosedRight = SearchSosedLeftOrRight(x, y, sosed, "right")  # правый сосед соседа

    clientLeft = SearchSosedLeftOrRight(x, y, client, "left")  # левый сосед клиента

    # TODO когда будет время, вставить рандом на left и right: если выбралось справа, то проверяем временные окна и т.д.
    # вставляем клиента справа и проверям, чтобы было все норм у время окончания работ.
    # Если 0 слева или справа, то не смотрим на его время окончания работ
    if (l[sosed] <= l[client] <= l[sosedRight] and sosedRight != 0) or (sosedRight == 0 and l[sosed] <= l[client]):
        print("Клиента вставляем справа")
        s[client][sosedK] = s[client][clientK]  # машина соседа будет работать у клиента столько же
        TimeOfArrival(a, s, client, sosed, sosedK)  # чтобы не считать время фактическое или плановое

        DeleteClientaFromPath(x, y, s, a, client)

        x[sosed][sosedRight][sosedK] = 0
        x[sosed][client][sosedK] = 1
        x[client][sosedRight][sosedK] = 1
        y[client][sosedK] = 1  # теперь машина соседа обслуживает клиента
        # заполняем то что мы хотим запомнить, 5 параметров
        arr[p][0] = clientLeft
        arr[p][1] = client
        arr[p][2] = clientK
        arr[p][3] = sosed
        arr[p][4] = sosedRight
        arr[p][5] = sosedK

    # клиента присоединяем слева
    elif (sosedLeft != 0 and l[sosedLeft] < l[client] < l[sosed]) or (sosedLeft == 0 and l[client] < l[sosed]):
        print("Клиента вставляем слева")
        s[client][sosedK] = s[client][clientK]  # машина соседа будет работать у клиента столько же
        TimeOfArrival(a, s, client, sosed, sosedK)  # Подсчет времени приезда к клиенту от соседа

        DeleteClientaFromPath(x, y, s, a, client)

        x[sosedLeft][sosed][sosedK] = 0
        x[sosedLeft][client][sosedK] = 1
        x[client][sosed][sosedK] = 1
        y[client][sosedK] = 1
        # теперь машина соседа обслуживает клиента
        arr[p][0] = clientLeft
        arr[p][1] = client
        arr[p][2] = clientK
        arr[p][3] = sosedLeft
        arr[p][4] = sosed
        arr[p][5] = sosedK

    else:
        print("не можем переместить из-за временных окон")  # Плохооооооо!!!
        # target_function = 100000000000000000000000000000000
        # print("target_funcrion = ", target_function)


# реализация оператора перемещения!!!
# переставляем клиента к новому соседу, локальный поиск
def JoiningClientToNewSosed(x, y, s, a, target_function, arr, p):  # (arr, p)
    # копируем чтобы не испортить решение
    SaveSolution(x, y, s, a, "Joining.txt", 'w') # стартовое сохранила в другой файл
    # X, Y, Ss, A = CopyingSolution(x, y, s, a)

    ####### Bыбираем клиента #############
    client = random.randint(1, (
            N - 1))  # Берем рандомного клиента/ -1 потому что иногда может появится 10, а это выход за границы

    print("Переставляем клиента ", client)
    print("на машине ", NumberCarClienta(y, client))

    sosedK = NumberCarClienta(y, client)  # берем рандомного соседа, главное чтобы не совпал с клиентом
    while sosedK == NumberCarClienta(y, client):
        sosed = random.randint(1, (N - 1))  # выбираем нового соседа
        sosedK = NumberCarClienta(y, sosed)

    print("К соседу ", sosed)
    print("На машине ", NumberCarClienta(y, sosed))

    # вклиниваем к соседу
    JoinClientaNonList(x, y, s, a, client, sosed, arr, p, target_function)  # (arr, p)

    # X, Y, Ss, A = DeleteNotUsedCar(X, Y, Ss, A)
    # target_function = CalculationOfObjectiveFunction(X)
    # print(target_function)
    # BeautifulPrint(X, Y, Ss, A)

    # проверка на успеваемость выполнения работ
    # если не успел уложиться в срок, штраф
    print("СЛЕДУЮЩИЕ ТРИ ERROR УПУСТИТЬ")
    if window_time_up(a, s, y, K) == 0:  # сломалось ли времен окно сверху,
        if VerificationOfBoundaryConditions(x, y, s, a, "true") == 1:
            print("вставили со штрафом на временные окна")
            target_function = CalculationOfObjectiveFunction(x, shtrafFunction(s, a))
            print(target_function)

            return target_function  # X, Y, Ss, A,
            # x, y, s, a = CopyingSolution(X, Y, Ss, A)

        else:
            print(
                "ERROR from JoiningClientToNewSosed: из-за сломанных вышестоящих ограничений, решение не сохранено")

    elif VerificationOfBoundaryConditions(x, y, s, a) == 1:
        target_function = CalculationOfObjectiveFunction(x, shtrafFunction(s, a))
        print("вставили без нарушений временного окна или не вставили")

        return target_function  # X, Y, Ss, A,
        # x, y, s, a = CopyingSolution(X, Y, Ss, A)

    else:
        ReadSolutionOfFile(x, y, s, a, "Joining.txt")
        target_function = CalculationOfObjectiveFunction(x, shtrafFunction(s, a))
        print("не можем переместить клиентов, что то пошло не так")

        return target_function
    print("\n")






# Создаем хранилище решений для большего числа рещений
def SolutionStore(size):
    # Хранилище решений, первый индекс это номер решения, со второго начинается само решение
    X = [0 for n in range(size)]  # едет или нет ТС с номером К из города I в J
    for n in range(size):
        X[n] = [[[0 for k in range(K)] for j in range(N)] for i in range(N)]

    Y = [0 for n in range(size)]  # посещает или нет ТС с номером К объект i
    for n in range(size):
        Y[n] = [[0 for k in range(K)] for i in range(N)]

    Ss = [0 for n in range(size)]  # время работы ТС c номером К на объекте i
    for n in range(size):
        Ss[n] = [[0 for k in range(K)] for i in range(N)]

    A = [0 for n in range(size)]  # время прибытия ТС с номером К на объект i
    for n in range(size):
        A[n] = [[0 for k in range(K)] for i in range(N)]

    Target_Function = [0 for n in range(size)]  # здесь сохраняем результат целевой функции для каждого решения

    return X, Y, Ss, A, Target_Function


# рандомно печатаем лево или право
# def PrintRightOrLeft():
#     foo = ['left', 'right']
#     print("рандомно выбрали = ", random.choice(foo))


# беру рандомного клиента из одного маршрута,
# беру правого соседа
# затем беру другого рандомного клиента из другого маршрута и
# беру его правого соседа
# обязательно эти пары из разных маршрутов!
def TwoOpt(X, Y, Ss, A, client1, client2):
    # копируем чтобы не испортить решение
    x, y, s, a = CopyingSolution(X, Y, Ss, A)
    # выбираем 1-го клиента
    # client1 = random.randint(1, (N - 1))
    client1_K = NumberCarClienta(y, client1)  # определили на какой он машине
    sosed1 = SearchSosedLeftOrRight(x, y, client1, "right")  # нашли соседа клиента1
    sosed1_R = SearchSosedLeftOrRight(x, y, sosed1, "right")  # нашли правого соседа соседа

    # выбираем 2-го клиента
    # client2 = random.randint(1, (N - 1))
    client2_K = NumberCarClienta(y, client2)
    sosed2 = SearchSosedLeftOrRight(x, y, client2, "right")
    sosed2_R = SearchSosedLeftOrRight(x, y, sosed2, "right")

    # спиздить вайл у котика на 134 строчке кроссовер

    # если выбрали клиентов из двух разных маршрутов, то все ок
    if client1_K != client2_K:
        if sosed1_R != 0 and sosed2_R != 0:
            if l[client1] < l[sosed2] < l[sosed1_R] and l[client2] < l[sosed1] < l[sosed2_R]:
                # не знаю нужны и правильны ли следующие 2 строчки
                s[sosed1][client2_K] = s[sosed1][client1_K]
                s[sosed2][client1_K] = s[sosed2][client2_K]
                TimeOfArrival(a, s, sosed2, client1, client1_K)
                TimeOfArrival(a, s, sosed1, client2, client2_K)
                TimeOfArrival(a, s, sosed2, sosed1_R, client1_K)
                TimeOfArrival(a, s, sosed1, sosed2_R, client2_K)

                DeleteClientaForTwoOpt(x, y, s, a, sosed2)
                DeleteClientaForTwoOpt(x, y, s, a, sosed1)

                x[client1][sosed1][client1_K] = 0
                x[client1][sosed2][client1_K] = 1
                x[sosed1][sosed1_R][client1_K] = 0
                x[sosed2][sosed1_R][client1_K] = 1
                x[sosed2][sosed2_R][client2_K] = 0
                x[sosed1][sosed2_R][client2_K] = 1
                y[sosed1_R][client1_K] = 1
                y[sosed2_R][client2_K] = 1
                y[sosed1_R][client2_K] = 0
                y[sosed2_R][client1_K] = 0
                y[sosed1][client1_K] = 0
                y[sosed2][client1_K] = 1
                x[client2][sosed2][client2_K] = 0
                x[client2][sosed1][client2_K] = 1
                y[sosed2][client2_K] = 0
                y[sosed1][client2_K] = 1

                print("Переставляем соседа1 ", sosed1)
                print("который обслуживается на машине ", NumberCarClienta(y, client1))
                print("К клиенту ", client2)
                print("На машине ", client2_K)

                print("Переставляем соседа2 ", sosed2)
                print("На машине ", NumberCarClienta(y, client2))
                print("К клиенту ", client1)
                print("На машине ", client1_K)

                x, y, s, a, Target_Function = SolutionStore()



        elif sosed1_R != 0 and sosed2_R == 0:
            if l[client1] < l[sosed2] < l[sosed1_R] and l[client2] < l[sosed1]:
                s[sosed1][client2_K] = s[sosed1][client1_K]
                s[sosed2][client1_K] = s[sosed2][client2_K]
                TimeOfArrival(a, s, sosed2, client1, client1_K)
                TimeOfArrival(a, s, sosed1, client2, client2_K)
                TimeOfArrival(a, s, sosed2, sosed1_R, client1_K)
                # TimeOfArrival(a, s, sosed1, sosed2_R, client2_K)

                DeleteClientaForTwoOpt(x, y, s, a, sosed2)
                DeleteClientaForTwoOpt(x, y, s, a, sosed1)

                x[client1][sosed1][client1_K] = 0
                x[client1][sosed2][client1_K] = 1
                x[sosed1][sosed1_R][client1_K] = 0
                x[sosed2][sosed1_R][client1_K] = 1
                # x[sosed2][sosed2_R][client2_K] = 0
                # x[sosed1][sosed2_R][client2_K] = 1
                y[sosed1_R][client1_K] = 1
                # y[sosed2_R][client2_K] = 1
                y[sosed1_R][client2_K] = 0
                # y[sosed2_R][client1_K] = 0
                y[sosed1][client1_K] = 0
                y[sosed2][client1_K] = 1
                x[client2][sosed2][client2_K] = 0
                x[client2][sosed1][client2_K] = 1
                y[sosed2][client2_K] = 0
                y[sosed1][client2_K] = 1
                # возвращение в депо после обмена
                x[sosed1][0][client2_K] = 1

                print("Переставляем соседа1 ", sosed1)
                print("который обслуживается на машине ", NumberCarClienta(y, client1))
                print("К клиенту ", client2)
                print("На машине ", client2_K)

                print("Переставляем соседа2 ", sosed2)
                print("На машине ", NumberCarClienta(y, client2))
                print("К клиенту ", client1)
                print("На машине ", client1_K)

                x, y, s, a, Target_Function = SolutionStore()

        elif sosed1_R == 0 and sosed2_R != 0:
            if l[client1] < l[sosed2] and l[client2] < l[sosed1] < l[sosed2_R]:
                # не знаю нужны и правильны ли следующие 2 строчки
                s[sosed1][client2_K] = s[sosed1][client1_K]
                s[sosed2][client1_K] = s[sosed2][client2_K]
                TimeOfArrival(a, s, sosed2, client1, client1_K)
                TimeOfArrival(a, s, sosed1, client2, client2_K)
                # TimeOfArrival(a, s, sosed2, sosed1_R, client1_K)
                TimeOfArrival(a, s, sosed1, sosed2_R, client2_K)

                DeleteClientaForTwoOpt(x, y, s, a, sosed2)
                DeleteClientaForTwoOpt(x, y, s, a, sosed1)

                x[client1][sosed1][client1_K] = 0
                x[client1][sosed2][client1_K] = 1
                # x[sosed1][sosed1_R][client1_K] = 0
                # x[sosed2][sosed1_R][client1_K] = 1
                x[sosed2][sosed2_R][client2_K] = 0
                x[sosed1][sosed2_R][client2_K] = 1
                # y[sosed1_R][client1_K] = 1
                y[sosed2_R][client2_K] = 1
                # y[sosed1_R][client2_K] = 0
                y[sosed2_R][client1_K] = 0
                y[sosed1][client1_K] = 0
                y[sosed2][client1_K] = 1
                x[client2][sosed2][client2_K] = 0
                x[client2][sosed1][client2_K] = 1
                y[sosed2][client2_K] = 0
                y[sosed1][client2_K] = 1
                # возвращ в депо после обмена
                x[sosed2][0][client1_K] = 1

                print("Переставляем соседа1 ", sosed1)
                print("который обслуживается на машине ", NumberCarClienta(y, client1))
                print("К клиенту ", client2)
                print("На машине ", client2_K)

                print("Переставляем соседа2 ", sosed2)
                print("На машине ", NumberCarClienta(y, client2))
                print("К клиенту ", client1)
                print("На машине ", client1_K)

                x, y, s, a, Target_Function = SolutionStore()

        elif sosed1_R == 0 and sosed2_R == 0:
            if l[client1] < l[sosed2] and l[client2] < l[sosed1]:
                s[sosed1][client2_K] = s[sosed1][client1_K]
                s[sosed2][client1_K] = s[sosed2][client2_K]
                TimeOfArrival(a, s, sosed2, client1, client1_K)
                TimeOfArrival(a, s, sosed1, client2, client2_K)

                DeleteClientaForTwoOpt(x, y, s, a, sosed2)
                DeleteClientaForTwoOpt(x, y, s, a, sosed1)

                x[client1][sosed1][client1_K] = 0
                x[client1][sosed2][client1_K] = 1

                y[sosed1][client1_K] = 0
                y[sosed2][client1_K] = 1
                x[client2][sosed2][client2_K] = 0
                x[client2][sosed1][client2_K] = 1
                y[sosed2][client2_K] = 0
                y[sosed1][client2_K] = 1

                # после перестановки они должны возвращаться в депо
                x[sosed1][0][client2_K] = 1
                x[sosed2][0][client1_K] = 1

                print("Переставляем соседа1 ", sosed1)
                print("который обслуживается на машине ", NumberCarClienta(y, client1))
                print("К клиенту ", client2)
                print("На машине ", client2_K)

                print("Переставляем соседа2 ", sosed2)
                print("На машине ", NumberCarClienta(y, client2))
                print("К клиенту ", client1)
                print("На машине ", client1_K)

                x, y, s, a, Target_Function = SolutionStore()



    else:
        print("выбраны клиенты из одного маршрута")


def RealizationTwoOpt(X, Y, Ss, A, Target_function):
    # копируем чтобы не испортить решение
    x, y, s, a = CopyingSolution(X, Y, Ss, A)

    # Bыбираем 1- го клиента
    client1 = random.randint(1, (
                N - 1))  # Берем рандомного клиента/ -1 потому что иногда может появится 10, а это выход за границы
    # Выбираем 2-го клиента
    client2 = random.randint(1, (N - 1))
    # TODO нужно написать какой то цикл, чтобы выполнилось несколько раз  while
    TwoOpt(x, y, s, a, client1, client2)

    print("СЛЕДУЮЩИЕ ТРИ ERROR УПУСТИТЬ")
    if window_time_up(a, s, y, k) == 0:
        if VerificationOfBoundaryConditions(x, y, s, a, "true") == 1:
            target_function = CalculationOfObjectiveFunction(x, shtrafFunction(s, a))
            print(target_function)
            X, Y, Ss, A = CopyingSolution(x, y, s, a)
        else:
            print("ERROR from RealizationTwoOpt: из-за сломанных вышестоящих ограничений, решение не сохранено")

    if VerificationOfBoundaryConditions(X, Y, Ss, A) == 1:
        target_function = CalculationOfObjectiveFunction(X, shtrafFunction(Ss, A))
        X, Y, Ss, A = CopyingSolution(x, y, s, a)
    return Target_function


# функция, которая проверяет встречалось уже такое решение в списке запретов или нет
def ProverKNaVstrechu(arr_Tabu, arr):
    for r in range(len(arr_Tabu)):
        if arr_Tabu[r] == arr:
            return 1
    return 0



# зануляем
def Zzero(X, Y, Ss, A, arr, Target_function):
    Target_function = 0
    for k in range(K):
        print('Номер машины ', k)
        for i in range(N):
            for j in range(N):
                X[i][j][k] = 0

        for i in range(N):
            Y[i][k] = 0

        for i in range(N):
            A[i][k] = 0

        for i in range(N):
            Ss[i][k] = 0

    for i in range(6):
        arr[i] = "0"
    # print("10 10 10 10")


# заполняю массив, сколько операторов, столько и форов
def start_operator(local_Target_function, local_x, local_y, local_s, local_a, target_function, arr):
    # print("44444444444")
    # сначала для оператора перемещения:
    SaveSolution(local_x, local_y, local_s, local_a, 'StartSolution.txt', 'w')
    for i in range(NumberStartOper):
        local_Target_function[i] = JoiningClientToNewSosed(local_x, local_y, local_s, local_a, target_function, arr, i)
        SaveSolution(local_x, local_y, local_s, local_a, 'ResultOperator.txt', 'a') # а - дозаписывать в конец

        # local_Target_function[i] = TwoOpt(i+1)???????????
        # SaveSolution(x, y, s, a, 'ResultOperator.txt', 'a')



        # # BeautifulPrint(X[i], Y[i], Ss[i], A[i])
        # # print("5555555555")
        # # if ProverKNaVstrechu(arr, i) == 1:
        #     # Zzero(X[i], Y[i], Ss[i], A[i], arr[i], Target_function[i])
        #     # print("6666666666666")
        # print("i = ", i)
        # if VerificationOfBoundaryConditions(X[i], Y[i], Ss[i], A[i], "true") != 1:
        #     print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

    # теперь для оператора 2Opt:
    # for i in range(NumberStartOper, 2 * NumberStartOper):
    #     Target_function[i], X[i], Y[i], Ss[i], A[i] = RealizationTwoOpt(x, y, s, a, target_function)


# ищет минимальную целевую функцию, возвращает индекс
def MinFromTarget(Target_function):
    target_min = 1000000000
    for i in range(len(Target_function)):
        if Target_function[i] < target_min and Target_function[i] != 0 and Target_function[i] != 1 and Target_function[i] != 2 and \
                Target_function[i] != 3 and Target_function[i] != 4 and Target_function[i] != 5 and\
                Target_function[i] != 6 and Target_function[i] != 7 and Target_function[i] != 8 and Target_function[i] != 9:
            target_min = Target_function[i]

    # for i in range(N):
    #     if Target_function[i] == Target_min:
    #         Target_function[i] = 0
    #         return i
    # min_target = min(Target_function)
    if target_min == 1000000000:
        return -1

    print("\n")
    print("Target_min = ", target_min)
    return Target_function.index(target_min)
