from Input_data import *
import random

# d = [[0 for j in range(N)] for i in range(N)]
# for i in range(N):
#     for j in range(N):
#         d[i][j] = sqrt(pow((OX[i] - OX[j]), 2) + pow((OY[i] - OY[j]), 2))
#         if d[i][j] > g:
#             d[i][j] = 0
#             print("слишком далеко, туда не еду")
#
# t = d
# for i in range(N):
#     for j in range(N):
#         t[i][j] = round(t[i][j] / 24)

# Строим матрицу расстояний и времени
d = [[0 for j in range(N)] for i in range(N)]  # расстояния между городами
for i in range(N):
    for j in range(N):
        d[i][j] = 111.1 * acos(sin(OX[i]) * sin(OX[j]) + cos(OX[i]) * cos(OX[j]) * cos(OY[j] - OY[i]))
        # d[i][j] = sqrt(pow((OX[i] - OX[j]), 2) + pow((OY[i] - OY[j]), 2))

t = [[0 for j in range(N)] for i in range(N)]  # время перемещения между городами
for i in range(N):
    for j in range(N):
        t[i][j] = (d[i][j] * 40) / (v * 24)


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
def ReadSolutionOfFile(output):
    local_x = [[[0 for k in range(K)] for j in range(N)] for i in
                   range(N)]  # едет или нет ТС с номером К из города I в J
    local_y = [[0 for k in range(K)] for i in range(N)]  # посещает или нет ТС с номером К объект i
    for k in range(K):
        local_y[0][k] = 1
    local_s = [[0 for k in range(K)] for i in range(N)]  # время работы ТС c номером К на объекте i
    local_a = [[0 for k in range(K)] for i in range(N)]  # время прибытия ТС с номером К на объект i

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

    return local_x, local_y, local_s, local_a


def SaveTabu(arr, target):
    file = open("TabuSearch.txt", 'a')
    print("arr[i] = ", arr)
    for i in range(6):
        print("arr[i] = ", arr[i])
        file.write(str(arr[i]) + ' ')
    file.write('\n')
    file.write(str(target) + '\n')
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


def ClearFiles():
    file = open("TabuSearch.txt", 'w')
    file.close()
    file = open("ResultOperator.txt", 'w')
    file.close()
    file = open("Joining.txt", 'w')
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
def shtrafFunction(s, a, iterations):
    shtraf_sum = 0
    for i in range(N):
        for k in range(K):
            if a[i][k] + s[i][k] > l[i]:
                shtraf_sum += max(0, (a[i][k] + s[i][k] - l[i]) * shtraf * iterations)
    return shtraf_sum

# подсчет значения целевой функции
def CalculationOfObjectiveFunction(x, shtrafFunction):
    target_function = 0
    for k in range(K):
        for i in range(N):
            for j in range(N):
                # Если время окончания не совпадает с регламентом, то умножаем разницу во времени на коэффициент
                target_function += d[i][j]*x[i][j][k]
    print("target_function в самой функции подсчета без штрафа = ", target_function)
    target_function += shtrafFunction
    print("target_function в самой функции подсчета со штрафом = ", target_function)
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
        #
    elif shtraf == "true":
        result = X_join_Y(x, y, K) * V_jobs(s, K) * TC_equal_K(K, y) * ban_driling(s, y, K) * \
                 window_time_down(a, y, K) * positive_a_and_s(x, y, a, s, K)
    #
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
    result = window_time_down(a, y, K)  # * window_time_up(a, s, y, K)

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
    X = x.copy()
    Y = y.copy()
    A = a.copy()
    Ss = s.copy()

    if E[j] >= t[0][j]:
        A[j][m] = E[j]
    else:
        A[j][m] = t[0][j]

    if E[i] >= t[0][i]:
        A[i][m] = E[i]
    else:
        A[i][m] = t[0][i]


    if E[i] < E[j] and skvaj[i] > skvaj[j]:
        bufer[m][N] = i  # двойной массив, где первое - это номер машины, второе - это маршрут
        bufer[m][N + 1] = j
        Y[i][m] = 1
        Y[j][m] = 1
        print("s перед тем как вставить", S[i], S[j])
        Ss[i][m] = S[i]
        Ss[j][m] = S[j]


        # if E[j] >= t[0][j]:
        #     A[j][m] = E[j]
        # else:
        #     A[j][m] = t[0][j]

        A[j][m] = A[i][m] + Ss[i][m] + t[i][j]

        if A[j][m] <= E[j]:
            A[j][m] = E[j]

        X[0][i][m] = 1
        X[i][j][m] = 1
        X[j][0][m] = 1
        # print(200)
        # BeautifulPrint(X, Y, Ss, A)
        # flag[i] = 1
        # flag[j] = 1

    if E[i] > E[j] and skvaj[i] < skvaj[j]:
        bufer[m][N] = j  # двойной массив, где первое - это номер машины, второе - это маршрут
        bufer[m][N + 1] = i
        Y[i][m] = 1
        Y[j][m] = 1
        print("s перед тем как вставить", S[i], S[j])
        Ss[i][m] = S[i]
        Ss[j][m] = S[j]

        # if E[j] >= t[0][j]:
        #     A[j][m] = E[j]
        # else:
        #     A[j][m] = t[0][j]

        A[i][m] = A[j][m] + Ss[j][m] + t[j][i]

        if A[i][m] <= E[i]:
            A[i][m] = E[i]

        X[0][j][m] = 1
        X[j][i][m] = 1
        X[i][0][m] = 1

    elif E[i] + skvaj[i] > E[j] + skvaj[j]:
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

        A[i][m] = A[j][m] + Ss[j][m] + t[j][i]

        if A[i][m] <= E[i]:
            A[i][m] = E[i]

        X[0][j][m] = 1
        X[j][i][m] = 1
        X[i][0][m] = 1
        # print(200)
        # BeautifulPrint(X, Y, Ss, A)
        # flag[i] = 1
        # flag[j] = 1


    elif E[i] + skvaj[i] < E[j] + skvaj[j]:
        bufer[m][N] = i  # двойной массив, где первое - это номер машины, второе - это маршрут
        bufer[m][N + 1] = j
        Y[i][m] = 1
        Y[j][m] = 1
        print("s перед тем как вставить", S[i], S[j])
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
        print("AddTwoCityInRoute: Произошел сбой")



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
        for i in range(N ):  # ищем по столбцу                             ### здесь измененя
            if x[i][client][k] == 1:
                return i
        return -1

    if leftOrRight == "right":
        for i in range(N):  # ищем по строке                            ### здесь измененя
            if x[client][i][k] == 1:
                return i
        return -1

    if leftOrRight != "left" and leftOrRight != "right":
        print("ERROR from SearchSosedLeftOrRight: неверное значение переменной leftOrRight")


###########################
def CarIsWork(y, k):
    suma = 0
    for i in range(N):
        if y[i][k] == 1:
            suma += 1

    if suma != 0:
        return 1
    else:
        return -1


# Рекурсия чтобы заполнить время прибытия
def RecursiaForTime(x, s, a, i, k, z):
    for j in range(N):
        if x[i][j][k] != 0 and j != 0 and z < N:
            # print("Нашли соседа для ", i, " справа ", j)
            # print("Время перемещения из ", i, " в ", j, " = ", t[i][j])
            # если время прибытия меньше начала работ, то ждем
            if E[j] > a[i][k] + s[i][k] + t[i][j]:
                # print("Приехали слишком рано ждем")
                a[j][k] = E[j]
                # print("a[j][k] = ", a[j][k])
            # иначе ставим время прибытия
            else:
                # print("Опоздали")
                a[j][k] = a[i][k] + s[i][k] + t[i][j]
                # print("a[j][k] = ", a[j][k])

            z += 1
            RecursiaForTime(x, s, a, j, k, z)
        elif x[i][j][k] != 0 and j == 0 and z < N:
            # print("Встретили ноль, пора заканчивать рекурсию")
            # print("Время прибытия в ", i, " = ", a[i][k])
            # print("Время работы в ", i, " = ", s[i][k])
            # print("Время переиещения из ", i, " в ", j, " = ", t[i][j])

            a[j][k] = a[i][k] + s[i][k] + t[i][j]

            # print("Время прибытия в депо = ", a[j][k])
            # for i in range(N):
            #     print(a[i][k], end=' ')
            # print('\n')

            return True

        elif z >= N:
            return -1

# определяем время приезда на конкретную локацию
def TimeOfArrival(x, y, s):
    z = 0 # глубина рекурсии

    # print("Начнем заполнять время прибытия")
    a = [[0 for k in range(len(s[0]))] for i in range(N)] #
    for k in range(len(s[0])):
        if CarIsWork(y, k) == 1:
            # print("ЗАходим в рекурсию")
            flag2 = RecursiaForTime(x, s, a, 0, k, z)
    if flag2 != -1:
        return a

    elif flag2 == -1:
        return flag2


# определяем время приезда на конкретную локацию
# def TimeOfArrival(a, s, client, sosed, sosedK):
#     # если время прибытия меньше начала работ, то ждем
#     if E[client] > a[sosed][sosedK] + s[sosed][sosedK] + t[sosed][client]:
#         a[client][sosedK] = E[client]
#     # иначе ставим время прибытия
#     else:
#         a[client][sosedK] = a[sosed][sosedK] + s[sosed][sosedK] + t[sosed][client]


# # удаляем клиента из выбранного  маршрута и соединяем соседние вершины
# def DeleteClientaFromPath(x, y, s, a, client):
#     k = NumberCarClienta(y, client)  # номер машины которая обслуживает клиента
#     clientLeft = SearchSosedLeftOrRight(x, y, client, "left")  # ищем город перед клиентом
#     clientRight = SearchSosedLeftOrRight(x, y, client, "right")  # ищем город после клиента
#     print("в перед if clientLeft = ", clientLeft)
#     print("в перед if clientRight = ", clientRight)
#     # если у клиента есть сосед справа и слева
#     if clientLeft != -1 and clientRight != -1:
#
#         if clientLeft != clientRight:
#             print("в if clientLeft = ",clientLeft)
#             print("в if clientRight = ", clientRight)
#             x[clientLeft][clientRight][k] = 1  # соединяем левого и правого соседа
#
#         else:
#             print("в else clientLeft = ", clientLeft)
#             print("в else clientRight = ", clientRight)
#             x[clientLeft][clientRight][k] = 0
#
#         x[client][clientRight][k] = 0  # удаляем ребро клиента с правым соседом
#         x[clientLeft][client][k] = 0  # удаляем ребро клиента с левым соседом
#
#         # У и S для левого и правого не меняются, но время прибытия меняется
#         y[client][k] = 0  # машина К больше не обслуживает клиента
#         s[client][k] = 0  # время работы машины К у клиента = 0
#         a[client][k] = 0  # машина не прибывает к клиенту
#         # TimeOfArrival(a, s, clientRight, clientLeft, k)
#         # a = TimeOfArrival(x, y, s)
#
#         # если удаляем клиента и остается только депо, ставим там 0
#         summa = 0
#         for i in range(1, N):
#             summa += y[i][k]
#         if summa == 0 and y[0][k] == 1:
#             y[0][k] = 0
#
#     # если клиент лист
#     elif clientLeft == -1 or clientRight == -1:
#         print("ERROR from DeleteClientaFromPath: такого не может быть: нет ни левого ни правого соседа")
#
#     # print("x[i][j][k] в delete= ")
#     # for k in range(K):
#     #     print('Номер машины ', k)
#     #     for i in range(N):
#     #         for j in range(N):
#     #             print(x[i][j][k], end=' ')
#     #         print("\n")
#     # print("s[j][k] в delete = ")
#     # for k in range(K):
#     #     for j in range(N):
#     #         print(s[j][k], end=" ")
#     #     print('\n')
#     # print("y[j][k] в delete = ")
#     # for k in range(K):
#     #     for j in range(N):
#     #         print(y[j][k], end=" ")
#     #     print('\n')
#     return x, y, s, a


# удаляем клиента из выбранного  маршрут
def DeleteClientaFromPath(x, y, s, a, client):
    k = NumberCarClienta(y, client)  # номер машины которая обслуживает клиента
    clientLeft = SearchSosedLeftOrRight(x, y, client, "left")  # ищем город перед клиентом
    clientRight = SearchSosedLeftOrRight(x, y, client, "right")  # ищем город после клиента
    # если у клиента есть сосед справо и слево
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
        # a = TimeOfArrival(x, y, s)
        # если удаляем клиента и остается только депо, ставим там 0
        summa = 0
        for i in range(1, N):
            summa += y[i][k]
        if summa == 0 and y[0][k] == 1:
            y[0][k] = 0

    elif clientLeft == -1 or clientRight == -1:
        print("ERROR from DeleteClientaFromPath: такого не может быть нет ни левого ни правого соседа")  # log
        raise IOError("ERROR from DeleteClientaFromPath: такого не может быть нет ни левого ни правого соседа")

    return x, y, s, a

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

        # TimeOfArrival(a, s, clientRight, clientLeft, k)
    # если у клиента есть сосед слева, а справо депо
    if clientLeft != -1 and clientRight == 0:
        # x[clientLeft][client][k] = 0  # теперь после левого соседа машина К никуда не едет кроме депо

        # x[client][0][k] = 0  # а клиент не возвращается в депо
        y[client][k] = 0  # клиент больше не обслуживается машиной К
        s[client][k] = 0  # машиной К больше не тратит время у клиента
        a[client][k] = 0  # и не приезжает
    if clientLeft == -1:  # logir
        print("ERROR from DeleteClientaFromPath: такого не может быть нет ни левого ни правого соседа")


def OperatorJoin(x, y, s, a, client, sosed, arr, iterations): # p
    Xl, Yl, Sl, Al = ReadSolutionOfFile("Relocate.txt")
    XR, YR, SR, AR = ReadSolutionOfFile("Relocate.txt")

    sosedK = NumberCarClienta(Yl, sosed)
    clientK = NumberCarClienta(Yl, client)

    sosedLeft = SearchSosedLeftOrRight(Xl, Yl, sosed, "left")  # левый сосед соседа
    sosedRight = SearchSosedLeftOrRight(Xl, Yl, sosed, "right")  # правый сосед соседа

    print("sosed_left = ", sosedLeft)
    print("sosed_right = ", sosedRight)

    clientLeft = SearchSosedLeftOrRight(x, y, client, "left")  # левый сосед клиента
    print("E[sosed] = ", E[sosed])
    print("E[client] = ", E[client])
    print("E[sosedRight]", E[sosedRight])
    print("E[sosedLeft] = ", E[sosedLeft])
    print("l[sosed] = ", l[sosed])
    print("l[client] = ", l[client])
    print("l[sosedRight]", l[sosedRight])
    print("l[sosedLeft] = ", l[sosedLeft])

    # Вставляем клиента справа от соседа и смотрим что время окончания работ последовательно
    # т.е. есди сосед справа не ноль то вставляем между кем-то, или просто вставляем справа
    try:
        print("Вставляем клиента к соседу справа")
        # машина соседа будет работать у клиента столько же
        SR[client][sosedK] = SR[client][clientK]

        # Чтобы все корректно работало, сначала надо написать
        # новое время приезда и новое время работы, потом
        # удалить старое решение, и только потом заполнять Х и У
        XR, YR, SR, AR = DeleteClientaFromPath(XR, YR, SR, AR, client)
        XR[sosed][sosedRight][sosedK] = 0
        XR[sosed][client][sosedK] = 1
        XR[client][sosedRight][sosedK] = 1
        YR[client][sosedK] = 1  # тепреь машина соседа обслуживает клиента

        arr[0] = clientLeft
        arr[1] = client
        arr[2] = clientK
        arr[3] = sosed
        arr[4] = sosedRight
        arr[5] = sosedK

        # Подсчет времени приезда к клиенту от соседа
        AR = TimeOfArrival(XR, YR, SR)

    except IOError:
        print("Объект не удален")
        XR[sosed][sosedRight][sosedK] = 1
        XR[sosed][client][sosedK] = 0
        XR[client][sosedRight][sosedK] = 0
        YR[client][sosedK] = 0  # тепреь машина соседа обслуживает клиента

        # Подсчет времени приезда к клиенту от соседа
        AR = TimeOfArrival(XR, YR, SR)

    try:
        print("Вставляем клиента к соседу слева")
        # машина соседа будет работать у клиента столько же
        Sl[client][sosedK] = Sl[client][clientK]

        # Чтобы все корректно работало, сначала надонаписать
        # новое время приезда и новое время работы, потом
        # удалить старое решение, и только потом заполнять Х и У
        Xl, Yl, Sl, Al = DeleteClientaFromPath(Xl, Yl, Sl, Al, client)
        Xl[sosedLeft][sosed][sosedK] = 0
        Xl[sosedLeft][client][sosedK] = 1
        Xl[client][sosed][sosedK] = 1
        Yl[client][sosedK] = 1  # теперь машина соседа обслуживает клиента

        # Подсчет времени приезда к клиенту от соседа
        Al = TimeOfArrival(Xl, Yl, Sl)

    except IOError:
        print("Объект не удален")
        Xl[sosedLeft][sosed][sosedK] = 1
        Xl[sosedLeft][client][sosedK] = 0
        Xl[client][sosed][sosedK] = 0
        Yl[client][sosedK] = 0  # теперь машина соседа обслуживает клиента

        arr[0] = clientLeft
        arr[1] = client
        arr[2] = clientK
        arr[3] = sosedLeft
        arr[4] = sosed
        arr[5] = sosedK

        # Подсчет времени приезда к клиенту от соседа
        Al = TimeOfArrival(Xl, Yl, Sl)

    print("СЛЕДУЮЩИЕ ТРИ ERROR УПУСТИТЬ для левого")
    if window_time_up(Al, Sl, Yl, K) == 0:
        if VerificationOfBoundaryConditions(Xl, Yl, Sl, Al, "true") == 1:
            print("NOTIFICATION from Relocate: вставили с нарушением временного окна")
            targetL = CalculationOfObjectiveFunction(Xl, shtrafFunction(SR, AR, iterations))
            print("Подсчет целевой функции для левого вставления ", targetL)
        else:
            targetL = -1
            print(
                "ERROR from Relocate: из-за сломанных вышестоящих ограничений, решение не сохранено")
    elif VerificationOfBoundaryConditions(Xl, Yl, Sl, Al) == 1:
        print("NOTIFICATION from Relocate: вставили без нарушений ограничений")
        targetL = CalculationOfObjectiveFunction(Xl, shtrafFunction(SR, AR, iterations))
        print("Подсчет целевой функции для левого вставления ", targetL)
    else:
        targetL = -1
        print("ERROR from Relocate: не получилось переставить, что-то пошло нет")

    print("СЛЕДУЮЩИЕ ТРИ ERROR УПУСТИТЬ для правого")
    if window_time_up(AR, SR, YR, K) == 0:
        if VerificationOfBoundaryConditions(XR, YR, SR, AR, "true") == 1:
            print("NOTIFICATION from Relocate: вставили с нарушением временного окна")
            targetR = CalculationOfObjectiveFunction(XR, shtrafFunction(SR, AR,  iterations))
            print("Подсчет целевой функции для правого вставления ", targetR)
        else:
            targetR = -1
            print(
                "ERROR from Relocate: из-за сломанных вышестоящих ограничений, решение не сохранено")
    elif VerificationOfBoundaryConditions(XR, YR, SR, AR) == 1:
        print("NOTIFICATION from Relocate: вставили без нарушений ограничений")
        targetR = CalculationOfObjectiveFunction(XR, shtrafFunction(SR, AR,iterations))
        print("Подсчет целевой функции для правого вставления ", targetR)
    else:
        targetR = -1
        print("ERROR from Relocate: не получилось переставить, что-то пошло нет")

    print("Теперь ищем минимум из двух целевых")
    minimum = min(targetL, targetR)
    if minimum == targetL and minimum != -1:
        iterations += 2
        print("Выбрали левого у него целевая меньше")
        return Xl, Yl, Sl, Al, targetL, iterations

    elif minimum == targetR and minimum != -1:
        iterations += 2
        print("Выбрали правого у него целевая меньше")
        return XR, YR, SR, AR, targetR, iterations

    else:
        print("Все пошло по пизде ничего не сохранили")
        return x, y, s, a, CalculationOfObjectiveFunction(x, shtrafFunction(SR, AR, iterations)), iterations


def Relocate(X, Y, Ss, A, target_function_start, arr, iterations):
    # копируем чтобы не испортить решение
    SaveSolution(X, Y, Ss, A, "Relocate.txt", 'w')
    TargetFunction = target_function_start
    buf_targ = 0

    while TargetFunction != buf_targ:  # пока меняется
        buf_targ = TargetFunction
        X, Y, Ss, A = ReadSolutionOfFile("Relocate.txt")

        # for Q in range(1, 7):  # это сколько я буду брать рандомных клиентов и переставлять
        # Bыбираем клиента
        client = random.randint(1, (
                    N - 1))  # Берем рандомного клиента -1 потому что иногда может появится 10, а это выход за граници

        print("Переставляем клиентa ", client)
        print("С машины", NumberCarClienta(Y, client))

        for sosed in range(1, N):
            if client != sosed:
                sosedK = NumberCarClienta(Y, sosed)

                print("К соседу ", sosed)
                print("На машине ", sosedK)
                print("Время перемещение от 0 до всех ", t[0])
                print("Время перемещение от ", client, " до ", sosed, " = ", t[client][sosed])
                print("Время перемещение от соседа до 0 ", t[sosed][0])

                x, y, s, a, target_function, iterations = OperatorJoin(X, Y, Ss, A, client, sosed, arr, iterations)

                print("Выбираем минимальное решение")
                minimum = min(TargetFunction, target_function)
                if minimum == target_function:
                    print("Новое перемещение, лучше чем то что было, сохраняем это решение")
                    SaveSolution(x, y, s, a, "Relocate.txt", "w")

                    TargetFunction = target_function
                elif minimum == TargetFunction:
                    print("Новое перемещение, хуже чем то что было, возвращаем наше старое решение")
                    # ReadRelocateOfFile(X, Y, Ss, A)


    ReadSolutionOfFile("Relocate.txt")

    return TargetFunction, X, Y, Ss, A, iterations


# оператор перемещения!!!
# вклиниваем между
# def JoinClientaNonList(x, y, s, a, client, sosed, arr, p, target_function):  # ОПЕРАТОР ПЕРЕМЕЩЕНИЯ! # (arr, p)
#     sosedK = NumberCarClienta(y, sosed)
#     clientK = NumberCarClienta(y, client)
#
#     sosedLeft = SearchSosedLeftOrRight(x, y, sosed, "left")  # левый сосед соседа
#     sosedRight = SearchSosedLeftOrRight(x, y, sosed, "right")  # правый сосед соседа
#
#     clientLeft = SearchSosedLeftOrRight(x, y, client, "left")  # левый сосед клиента
#     print("E[sosed] = ", E[sosed])
#     print("E[client] = ", E[client])
#     print("E[sosedRight]", E[sosedRight])
#     print("E[sosedLeft] = ", E[sosedLeft])
#     print("l[sosed] = ", l[sosed])
#     print("l[client] = ", l[client])
#     print("l[sosedRight]", l[sosedRight])
#     print("l[sosedLeft] = ", l[sosedLeft])
#
#     # TODO когда будет время, вставить рандом на left и right: если выбралось справа, то проверяем временные окна и т.д.
#     # вставляем клиента справа и проверям, чтобы было все норм у время окончания работ.
#     # Если 0 слева или справа, то не смотрим на его время окончания работ
#     if (l[sosed] <= l[client] <= l[sosedRight] and sosedRight != 0) or (sosedRight == 0 and l[sosed] <= l[client]):
#         print("Клиента вставляем справа")
#         print("l[sosed]", l[sosed] )
#         print("l[client]",l[client] )
#         print("l[sosedRight]", l[sosedRight])
#         print(" 1")
#         s[client][sosedK] = s[client][clientK]  # машина соседа будет работать у клиента столько же
#         # TimeOfArrival(a, s, client, sosed, sosedK)  # чтобы не считать время фактическое или плановое
#
#         x, y, s, a = DeleteClientaFromPath(x, y, s, a, client)
#         print("2 ")
#
#
#         x[sosed][sosedRight][sosedK] = 0
#         x[sosed][client][sosedK] = 1
#         x[client][sosedRight][sosedK] = 1
#         y[client][sosedK] = 1  # теперь машина соседа обслуживает клиента
#         # заполняем то что мы хотим запомнить, 5 параметров
#         arr[p][0] = clientLeft
#         arr[p][1] = client
#         arr[p][2] = clientK
#         arr[p][3] = sosed
#         arr[p][4] = sosedRight
#         arr[p][5] = sosedK
#
#         a = TimeOfArrival(x, y, s)
#
#         # print("x[i][j][k] = ")
#         # for k in range(K):
#         #     print('Номер машины ', k)
#         #     for i in range(N):
#         #         for j in range(N):
#         #             print(x[i][j][k], end=' ')
#         #         print("\n")
#         # for k in range(K):
#         #     for j in range(N):
#         #         print(s[j][k], end=" ")
#         #     print('\n')
#         # print("y[j][k] = ")
#         # for k in range(K):
#         #     for j in range(N):
#         #         print(y[j][k], end=" ")
#         #     print('\n')
#
#
#     # клиента присоединяем слева
#     elif (sosedLeft != 0 and l[sosedLeft] < l[client] < l[sosed]) or (sosedLeft == 0 and l[client] < l[sosed]):
#         print("Клиента вставляем слева")
#         print("l[sosedLeft] = ", l[sosedLeft])
#         print("l[client]", l[client] )
#         print("l[sosed]", l[sosed] )
#         s[client][sosedK] = s[client][clientK]  # машина соседа будет работать у клиента столько же
#         # TimeOfArrival(a, s, client, sosed, sosedK)  # Подсчет времени приезда к клиенту от соседа
#         print(" 3")
#         x, y, s, a = DeleteClientaFromPath(x, y, s, a, client)
#         print(" 4")
#
#
#         x[sosedLeft][sosed][sosedK] = 0
#         x[sosedLeft][client][sosedK] = 1
#         x[client][sosed][sosedK] = 1
#         y[client][sosedK] = 1
#         # теперь машина соседа обслуживает клиента
#         arr[p][0] = clientLeft
#         arr[p][1] = client
#         arr[p][2] = clientK
#         arr[p][3] = sosedLeft
#         arr[p][4] = sosed
#         arr[p][5] = sosedK
#
#         a = TimeOfArrival(x, y, s)
#
#         # print("x[i][j][k] = ")
#         # for k in range(K):
#         #     print('Номер машины ', k)
#         #     for i in range(N):
#         #         for j in range(N):
#         #             print(x[i][j][k], end=' ')
#         #         print("\n")
#         # for k in range(K):
#         #     for j in range(N):
#         #         print(s[j][k], end=" ")
#         #     print('\n')
#         # print("y[j][k] = ")
#         # for k in range(K):
#         #     for j in range(N):
#         #         print(y[j][k], end=" ")
#         #     print('\n')
#
#     elif (E[sosed] <= E[client] <= E[sosedRight] and sosedRight != 0) or (sosedRight == 0 and E[sosed] <= E[client]):
#         print("Клиента вставляем справа")
#         print("E[sosed] = ",E[sosed] )
#         print("E[client] = ", E[client] )
#         print("E[sosedRight]", E[sosedRight] )
#         s[client][sosedK] = s[client][clientK]  # машина соседа будет работать у клиента столько же
#         # TimeOfArrival(a, s, client, sosed, sosedK)  # чтобы не считать время фактическое или плановое
#         print("5 ")
#         x, y, s, a = DeleteClientaFromPath(x, y, s, a, client)
#         print(" 6")
#
#
#         x[sosed][sosedRight][sosedK] = 0
#         x[sosed][client][sosedK] = 1
#         x[client][sosedRight][sosedK] = 1
#         y[client][sosedK] = 1  # теперь машина соседа обслуживает клиента
#         # заполняем то что мы хотим запомнить, 5 параметров
#         arr[p][0] = clientLeft
#         arr[p][1] = client
#         arr[p][2] = clientK
#         arr[p][3] = sosed
#         arr[p][4] = sosedRight
#         arr[p][5] = sosedK
#
#         a = TimeOfArrival(x, y, s)
#
#         # print("x[i][j][k] = ")
#         # for k in range(K):
#         #     print('Номер машины ', k)
#         #     for i in range(N):
#         #         for j in range(N):
#         #             print(x[i][j][k], end=' ')
#         #         print("\n")
#         # for k in range(K):
#         #     for j in range(N):
#         #         print(s[j][k], end=" ")
#         #     print('\n')
#         # print("y[j][k] = ")
#         # for k in range(K):
#         #     for j in range(N):
#         #         print(y[j][k], end=" ")
#         #     print('\n')
#
#         # клиента присоединяем слева
#     elif (sosedLeft != 0 and E[sosedLeft] < E[client] < E[sosed]) or (sosedLeft == 0 and E[client] < E[sosed]):
#         print("Клиента вставляем слева")
#         print("E[sosedLeft] = ", E[sosedLeft])
#         print("E[client] = ", E[client])
#         print("E[sosed] = ", E[sosed])
#
#         s[client][sosedK] = s[client][clientK]  # машина соседа будет работать у клиента столько же
#         # TimeOfArrival(a, s, client, sosed, sosedK)  # Подсчет времени приезда к клиенту от соседа
#         print("7 ")
#         x, y, s, a = DeleteClientaFromPath(x, y, s, a, client)
#         print(" 8")
#
#
#         x[sosedLeft][sosed][sosedK] = 0
#         x[sosedLeft][client][sosedK] = 1
#         x[client][sosed][sosedK] = 1
#         y[client][sosedK] = 1
#         # теперь машина соседа обслуживает клиента
#         arr[p][0] = clientLeft
#         arr[p][1] = client
#         arr[p][2] = clientK
#         arr[p][3] = sosedLeft
#         arr[p][4] = sosed
#         arr[p][5] = sosedK
#
#         a = TimeOfArrival(x, y, s)
#
#         # print("x[i][j][k] = ")
#         # for k in range(K):
#         #     print('Номер машины ', k)
#         #     for i in range(N):
#         #         for j in range(N):
#         #             print(x[i][j][k], end=' ')
#         #         print("\n")
#         # for k in range(K):
#         #     for j in range(N):
#         #         print(s[j][k], end=" ")
#         #     print('\n')
#         # print("y[j][k] = ")
#         # for k in range(K):
#         #     for j in range(N):
#         #         print(y[j][k], end=" ")
#         #     print('\n')
#     elif  l[sosed] <= l[client]:
#         print("Клиента вставляем справа")
#         print("l[sosed]", l[sosed] )
#         print("l[client]",l[client] )
#         print("l[sosedRight]", l[sosedRight])
#         print(" 1")
#         s[client][sosedK] = s[client][clientK]  # машина соседа будет работать у клиента столько же
#         # TimeOfArrival(a, s, client, sosed, sosedK)  # чтобы не считать время фактическое или плановое
#
#         x, y, s, a = DeleteClientaFromPath(x, y, s, a, client)
#         print("2 ")
#
#         x[sosed][sosedRight][sosedK] = 0
#         x[sosed][client][sosedK] = 1
#         x[client][sosedRight][sosedK] = 1
#         y[client][sosedK] = 1  # теперь машина соседа обслуживает клиента
#         # заполняем то что мы хотим запомнить, 5 параметров
#         arr[p][0] = clientLeft
#         arr[p][1] = client
#         arr[p][2] = clientK
#         arr[p][3] = sosed
#         arr[p][4] = sosedRight
#         arr[p][5] = sosedK
#
#         a = TimeOfArrival(x, y, s)
#
#     elif  l[client] < l[sosed]:
#         print("Клиента вставляем слева")
#         print("l[client]", l[client] )
#         print("l[sosed]", l[sosed] )
#         s[client][sosedK] = s[client][clientK]  # машина соседа будет работать у клиента столько же
#         # TimeOfArrival(a, s, client, sosed, sosedK)  # Подсчет времени приезда к клиенту от соседа
#         print(" 3")
#         x, y, s, a = DeleteClientaFromPath(x, y, s, a, client)
#         print(" 4")
#
#         x[sosedLeft][sosed][sosedK] = 0
#         x[sosedLeft][client][sosedK] = 1
#         x[client][sosed][sosedK] = 1
#         y[client][sosedK] = 1
#         # теперь машина соседа обслуживает клиента
#         arr[p][0] = clientLeft
#         arr[p][1] = client
#         arr[p][2] = clientK
#         arr[p][3] = sosedLeft
#         arr[p][4] = sosed
#         arr[p][5] = sosedK
#
#         a = TimeOfArrival(x, y, s)
#     else:
#         print("не можем переместить из-за временных окон")  # Плохооооооо!!!
#         # target_function = 100000000000000000000000000000000
#         # print("target_funcrion = ", target_function)


# реализация оператора перемещения!!!
# переставляем клиента к новому соседу, локальный поиск
# def JoiningClientToNewSosed(x, y, s, a, target_function, arr, p):  # (arr, p)
#     # копируем чтобы не испортить решение
#     SaveSolution(x, y, s, a, "Joining.txt", 'w')  # стартовое сохранила в другой файл
#     # X, Y, Ss, A = CopyingSolution(x, y, s, a)
# 
#     ####### Bыбираем клиента #############
#     client = random.randint(1, (
#             N - 1))  # Берем рандомного клиента/ -1 потому что иногда может появится 10, а это выход за границы
# 
#     print("Переставляем клиента ", client)
#     print("на машине ", NumberCarClienta(y, client))
# 
#     sosedK = NumberCarClienta(y, client)  # берем рандомного соседа, главное чтобы не совпал с клиентом
#     while sosedK == NumberCarClienta(y, client):
#         sosed = random.randint(1, (N - 1))  # выбираем нового соседа
#         sosedK = NumberCarClienta(y, sosed)
# 
#     print("К соседу ", sosed)
#     print("На машине ", NumberCarClienta(y, sosed))
# 
#     # вклиниваем к соседу
#     # JoinClientaNonList(x, y, s, a, client, sosed, arr, p, target_function)  # (arr, p)
# 
# 
#     # X, Y, Ss, A = DeleteNotUsedCar(X, Y, Ss, A)
#     # target_function = CalculationOfObjectiveFunction(X)
#     # print(target_function)
#     # BeautifulPrint(X, Y, Ss, A)
#     if a != -1:
#         # проверка на успеваемость выполнения работ
#         # если не успел уложиться в срок, штраф
#         print("СЛЕДУЮЩИЕ ТРИ ERROR УПУСТИТЬ")
#         if window_time_up(a, s, y, K) == 0:  # сломалось ли времен окно сверху,
#             if VerificationOfBoundaryConditions(x, y, s, a, "true") == 1:
#                 print("вставили со штрафом на временные окна")
#                 target_function = CalculationOfObjectiveFunction(x, shtrafFunction(s, a))
#                 print(target_function)
#                 # x, y, s, a = CopyingSolution(X, Y, Ss, A)
# 
#                 # return target_function   # X, Y, Ss, A,
# 
#             else:
#                 print(
#                     "ERROR from JoiningClientToNewSosed: из-за сломанных вышестоящих ограничений, решение не сохранено")
# 
#         elif VerificationOfBoundaryConditions(x, y, s, a) == 1:
#             target_function = CalculationOfObjectiveFunction(x, shtrafFunction(s, a))
#             print("вставили без нарушений временного окна или не вставили")
# 
#             # return target_function  # X, Y, Ss, A,
#             # x, y, s, a = CopyingSolution(X, Y, Ss, A)
# 
#         else:
#             ReadSolutionOfFile(x, y, s, a, "Joining.txt")
#             target_function = CalculationOfObjectiveFunction(x, shtrafFunction(s, a))
#             print("не можем переместить клиентов, что то пошло не так")
# 
#     return target_function, x, y, s, a


def XDisplayInTheSequenceX2(x, bufer, i, k, bul):
    for j in range(N):
        if x[i][j][k] == 1:
            bul += 1
            bufer[k][bul] = j
            if j != 0:
                XDisplayInTheSequenceX2(x, bufer, j, k, bul)


def GettingTheSequence(X): # получаем двумерную послед-ть
    # N+1.txt потому что последовательность может посещать все города и при этом возвращается в 0
    sequenceX2 = [[0 for i in range(N + 1)] for j in range(K)]
    for k in range(K):
        XDisplayInTheSequenceX2(X, sequenceX2, 0, k, 0)
    return sequenceX2


def AddOneCell(sequenceX1):
    bufer = [[0 for j in range(2)] for i in range(len(sequenceX1))]
    # ячейка означает, что из этого конкретного города на этой машине нельзя ехать в следующий
    for i in range(len(sequenceX1)):
        bufer[i][0] = sequenceX1[i]
    return bufer


# преобразует 2-мерную в 1-мерную послед-ть
def TransferX2toX1(sequenceX2, X):
    sequenceX1 = [0]
    for k in range(len(X[0][0])):
        for i in range(1, N - 1):
            # случай когда находишься на цифре и следующая цифра
            if sequenceX2[k][i] != 0 and sequenceX2[k][i + 1] != 0:
                sequenceX1.append(sequenceX2[k][i])
            # случай когда находишься на цифре и следующий ноль
            if sequenceX2[k][i] != 0 and sequenceX2[k][i + 1] == 0:
                sequenceX1.append(sequenceX2[k][i])
            # случай когда находишься на нуле и предыдущая цифра
            if sequenceX2[k][i - 1] != 0 and sequenceX2[k][i] == 0:
                sequenceX1.append(sequenceX2[k][i])

    return sequenceX1


def CreateSequence(X):
    sequenceX1 = []
    sequenceX2 = []
    # Интерпритируем матрицу Х на двумерный массив
    sequenceX2 = GettingTheSequence(X)
    sequenceX1 = TransferX2toX1(sequenceX2, X)
    return sequenceX1


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
            target_function = CalculationOfObjectiveFunction(x, shtrafFunction(s, a, iterations))
            print(target_function)
            X, Y, Ss, A = CopyingSolution(x, y, s, a)
        else:
            print("ERROR from RealizationTwoOpt: из-за сломанных вышестоящих ограничений, решение не сохранено")

    if VerificationOfBoundaryConditions(X, Y, Ss, A) == 1:
        target_function = CalculationOfObjectiveFunction(X, shtrafFunction(Ss, A, iterations))
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
def start_operator(target_function, local_x, local_y, local_s, local_a, arr, iterations):

    # сначала для оператора перемещения:
    SaveSolution(local_x, local_y, local_s, local_a, 'StartSolution.txt', 'w')
    local_x, local_y, local_s, local_a = ReadSolutionOfFile('StartSolution.txt')

    # local_Target_function[i], local_x, local_y, local_s, local_a = JoiningClientToNewSosed(local_x, local_y, local_s, local_a, target_function, arr, i)

    Target_function_reloc, x_reloc, y_reloc, s_reloc, a_reloc, iterations = Relocate(local_x, local_y, local_s, local_a, target_function, arr, iterations)
    print("Target_function_reloc = ", Target_function_reloc)
    # print("s[j][k] = ")
    # for k in range(K):
    #     for j in range(N):
    #         print(local_s[j][k], end=" ")
    #     print('\n')
    # print("y[j][k] = ")
    # for k in range(K):
    #     for j in range(N):
    #         print(local_y[j][k], end=" ")
    #     print('\n')

    return Target_function_reloc, x_reloc, y_reloc, s_reloc, a_reloc, iterations

    #TODO  Раскоментить, когда появится 2-Opt
    # прочитали стартовое решение, чтобы все делать с 2-Opt:
    # local_x, local_y, local_s, local_a = ReadSolutionOfFile('StartSolution.txt')
    # TODO считаем локальный минимум для 2-Opt
    # minimum = min(Target_function_reloc, Target_function_TwoOpt)
    # if minimum == Target_function_reloc:
    #     return Target_function_reloc, x_reloc, y_reloc, s_reloc, a_reloc
    # elif minimum == Target_function_TwoOpt:
    #     return Target_function_TwoOpt, x_TwoOpt, y_TwoOpt, s_TwoOpt, a_TwoOpt


# ищет минимальную целевую функцию, возвращает индекс
def MinFromTarget(Target_function):
    target_min = 1000000000
    # print("Target = ", Target_function)
    for i in range(len(Target_function)):
        if Target_function[i] < target_min and Target_function[i] != 0 and Target_function[i] != 1 and \
                Target_function[i] != 2 and Target_function[i] != 3 and Target_function[i] != 4 and \
                Target_function[i] != 5 and Target_function[i] != 6 and Target_function[i] != 7 and \
                Target_function[i] != 8 and Target_function[i] != 9:
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
