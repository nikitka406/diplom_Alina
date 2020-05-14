from Input_data import *
import random
from WorkWithFile import *


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

# сохраняет последовательное посещение городов для каждой машины
bufer = [[0 for k in range((N + 1) * 2)] for i in range(K)]
flag = [0 for i in range(N)]  # флажок, если посетила город
# N так как с обеих сторон должны быть нули (выезжает из депо и возвращ в депо)
s = [[0 for k in range(K)] for i in range(N)]  # время работы ТС c номером К на объекте i
a = [[0 for k in range(K)] for i in range(N)]  # время прибытия ТС с номером К на объект i


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
    # for i in range(N):
    #     for k in range(N):
    #         print(t[i][k], end=' ')
    #     print('\n')

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


def Zapolnenie(X, Y, Ss, kyda, new_client, sosed, car,nomer_sosed):
    bufer[car][nomer_sosed] = new_client
    Y[new_client][car] = 1
    Ss[new_client][car] = S[new_client]

    if kyda == "right":
        X[sosed][new_client][car] = 1
        X[sosed][0][car] = 0
        X[new_client][0][car] = 1
    elif kyda == "left":
        X[new_client][sosed][car] = 1
        X[0][sosed][car] = 0
        X[0][new_client][car] = 1


def Add_vershiny_k_resheniu(bufer, flag, X, Y, Ss, A, x, y, s, a, new_client, car, nomer_sosed, l_p, sosed, kyda):
    if kyda == "right":

        if E[new_client] >= l_p:
            A[new_client][car] = E[new_client]
            Zapolnenie(X, Y, Ss, "right", new_client, sosed, car, nomer_sosed)
            flag[i] = 1
            flag[j] = 1
        # and l[new_client] >= l_p + S[new_client] and kyda == "right":  # если время начала работы нового клиента больше чем время прибытия + работы + переезда предыдущего

        elif E[new_client] < l_p:
            A[new_client][car] = l_p
            Zapolnenie(X, Y, Ss, "right", new_client, sosed, car, nomer_sosed)
            flag[i] = 1
            flag[j] = 1
        # and l[new_client] >= l_p + S[new_client] and kyda == "right":

        # elif l[new_client] < l_p + S[new_client]:
        #     print("не можем вставить, т.к. не успеет закончить работу вовремя")


    elif kyda == "left":
        if A[sosed][car] >= l_p and kyda == "left":
            A[new_client][car] = A[sosed][car] - S[new_client] - t[new_client][bufer[car][nomer_sosed]]
            Zapolnenie(X, Y, Ss, "left", new_client, sosed, car, nomer_sosed)
            flag[i] = 1
            flag[j] = 1
            if A[new_client][car] <= E[new_client]:
                A[new_client][car] = E[new_client]
        elif A[sosed][car] < l_p and kyda == "left":
            print("ne podhodit dlya marchruta")


        ############################
        # if E[j] >= t[0][j]:
        #     l_p = E[j] + S[j] + t[j][bufer[m][n]]  # мы не можем начать работать раньше, чем временное окно
        # else:
        #     l_p = t[0][j] + S[j] + t[j][bufer[m][n]]
        ##############################

    else:
        print("введено неправильно right или left")


    # if E[sosed] >= l_p and kyda == "left":
    #     A[new_client][car] = t[0][new_client]
    #     # A[new_client][car] = E[sosed] - S[new_client] - t[new_client][bufer[car][nomer_sosed]]
    #
    # elif E[sosed] < l_p and kyda == "left":
    #     A[new_client][car] = E[new_client] - S[new_client] - t[new_client][bufer[car][nomer_sosed]]

    if VerificationOfBoundaryConditionsForStartSolution(X, Y, Ss, A) != 1:  # если сломались граничные условия, то не сохраняем
        X = x.copy()
        Y = y.copy()
        A = a.copy()
        Ss = s.copy()
    else:
        x = X.copy()
        y = Y.copy()
        a = A.copy()
        s = Ss.copy()
        # flag[new_client] = 1



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
                shtraf_sum += max(0, (a[i][k] + s[i][k] - l[i]) * shtraf) #* iterations)
            # if a[i][k] < E[i]:
            #     shtraf_sum += max(0, (E[i] - a[i][k]) * prostoy)
    return shtraf_sum


# подсчет значения целевой функции
def CalculationOfObjectiveFunction(x, shtrafFunction):
    target_function = 0
    for k in range(K):
        for i in range(N):
            for j in range(N):
                target_function += d[i][j] * x[i][j][k]

    # print("target_function в самой функции подсчета без штрафа = ", target_function)
    target_function += shtrafFunction
    # print("target_function в самой функции подсчета со штрафом = ", target_function)
    return target_function


# Граничные условия
def X_join_Y(x, y, k, file='def'):
    bufer1 = 0
    bufer2 = 0
    # Add constraint:
    for k in range(K):
        for j in range(N):
            for i in range(N):
                bufer1 += x[i][j][k]
                bufer2 += x[j][i][k]
            if bufer1 != bufer2 or bufer2 != y[j][k] or bufer1 != y[j][k]:
                if file != 'def':
                    file.write("сломалось первое ограничение, несовместность переменных х, у" + '\n')
                else:
                    print("сломалось первое ограничение, несовместность переменных х, у")
                return 0
            bufer1 = 0
            bufer2 = 0
    return 1


def V_jobs(s, k, file='def'):
    bufer1 = 0
    # Add constraint: sum (s[i][k])==S[i]
    for i in range(1, N):
        if i != 0:
            for k in range(K):
                bufer1 += s[i][k]
            if int(bufer1) != S[i]:
                if file != 'def':
                    file.write("slomalos 2: общий объем работ на каждом объекте" + '\n')

                else:
                    print("slomalos 2: общий объем работ на каждом объекте" + '\n')
                return 0
            bufer1 = 0
    return 1


def TC_equal_K(y, k, file='def'):
    bufer1 = 0
    # Add constraint: sum (y[i][k])<=K[i]
    for i in range(1, N):
        if i != 0:
            for k in range(K):
                bufer1 += y[i][k]
            if bufer1 > skvaj[i]:
                if file != 'def':
                    file.write(" slomalos 3: ТС не больше, чем скважин" + str(i) + "больше чем число скважин" + '\n')
                else:
                    print(" slomalos 3: ТС не больше, чем скважин" + str(i) + "больше чем число скважин" + '\n')

                return 0
            bufer1 = 0
    return 1


def ban_driling(s, y, k, file='def'):
    # Add constraint: s[i][k] <=S[i]*y[i][k]
    for i in range(1, N):
        for k in range(K):
            if s[i][k] > S[i] * y[i][k]:
                if file != 'def':
                    file.write("slomalos 4: установка не работает, если не приехала на объект" + '\n')
                else:
                    print("slomalos 4: установка не работает, если не приехала на объект" + '\n')
                return 0
    return 1


def window_time_down(a, y, k, file='def'):
    # Add constraint: e[i]<=a[i][k]
    for i in range(1, N):
        for k in range(K):
            if E[i] > a[i][k] and y[i][k] == 1:
                if file != 'def':
                    file.write(
                        "slomalos 5: нельзя начать работу раньше, чем приехал" + '\n')  # не работает это ограничение
                # else:
                #     print("slomalos 5: нельзя начать работу раньше, чем приехал" + '\n')
                return 0
    return 1


def window_time_up(a, s, y, k, file='def'):
    # Add constraint: a[i][k] + s[i][k] <= l[i]
    for i in range(1, N):
        for k in range(K):
            if a[i][k] + s[i][k] > l[i] and y[i][k] == 1:
                if file != 'def':
                    file.write("slomalos 6: нельзя закончить работу позже, чем временное окно" + '\n')
                # else:
                #     print("slomalos 6: нельзя закончить работу позже, чем временное окно" + '\n')
                return 0
    return 1


def ban_cycle(a, x, s, y, file='def'):
    # Add constraint: a[i][k] - a[j][k] +x[i][j][k]*t[i][j] + s[i][k] <= l[i](1-x[i][j][k])
    for i in range(1, N):
        for j in range(1, N):
            for k in range(K):
                if a[i][k] - a[j][k] + x[i][j][k] * t[i][j] + s[i][k] > l[i] * (1 - x[i][j][k]) and y[i][k] == 1:
                    if file != 'def':
                        file.write("slomalos 7:запрещ циклы, которые не проходят через депо" + '\n')
                    else:
                        print("slomalos 7:запрещ циклы, которые не проходят через депо" + '\n')
                    return 0
    return 1


def positive_a_and_s(x, y, a, s, file='def'):
    # Add constraint: s[i][k] >= 0 and a[i][k] >= 0
    for i in range(N):
        for j in range(N):
            for k in range(K):
                if s[i][k] < 0 or a[i][k] < 0:
                    if file != 'def':
                        file.write("slomalos 8: область изменения перменных" + '\n')
                    else:
                        ("slomalos 8: область изменения перменных" + '\n')
                    return 0
                if x[i][j][k] != 0 and x[i][j][k] != 1:
                    print("ERROR from positive_a_and_s: сломалось седьмое ограничение, "
                          "неправильное значение переменной x")
                    return 0
                if y[i][k] != 0 and y[i][k] != 1:
                    print("ERROR from positive_a_and_s: сломалось седьмое ограничение, "
                          "неправильное значение переменной y")
                    return 0
    return 1


# проверка выполнения граничных условий
def VerificationOfBoundaryConditions(x, y, s, a, shtraf="false", file='def'):
    # по дефолту смотрим все огр, но если тру то не рассматриваем огр на своевременный конец работ
    if shtraf == "false":
        result = X_join_Y(x, y, file) * V_jobs(s, file) * TC_equal_K(y, file) * ban_driling(s, y, file) * \
                 window_time_down(a, y, file) * window_time_up(a, s, y, file) * \
                 ban_cycle(a, x, s, y, file) * positive_a_and_s(x, y, a, s, file)

    elif shtraf == "true":
        result = X_join_Y(x, y, file) * V_jobs(s, file) * TC_equal_K(y, file) * ban_driling(s, y, file) * \
                 window_time_down(a, y, file) * positive_a_and_s(x, y, a, s, file)

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


# Проверка ограничений и подсчет целевой
def Checker(X, Y, Ss, A, iterations, name, file):
    file.write("    СЛЕДУЮЩИЕ ТРИ ERROR УПУСТИТЬ" + '\n')
    if window_time_up(A, Ss, Y, file) == 0:
        if VerificationOfBoundaryConditions(X, Y, Ss, A, "true", file) == 1:
            file.write("    NOTIFICATION from " + name + ": вставили с нарушением временного окна" + '\n')
            Target_Function = CalculationOfObjectiveFunction(X, shtrafFunction(Ss, A, iterations))
            file.write("    Подсчет целевой функции после вставления " + str(Target_Function) + '\n')
            return X, Y, Ss, A, Target_Function
        else:
            file.write(
                "   ERROR from " + name + ": не получилось переставить, потому что сломались ограничения, возвращаем "
                                          "стартовое" + '\n')
            return -1

    elif VerificationOfBoundaryConditions(X, Y, Ss, A, "false", file) == 1:
        file.write("    NOTIFICATION from " + name + ": вставили без нарушений ограничений" + '\n')
        Target_Function = CalculationOfObjectiveFunction(X, shtrafFunction(Ss, A, iterations))
        file.write("    Подсчет целевой функции после вставления " + str(Target_Function) + '\n')
        return X, Y, Ss, A, Target_Function
    else:
        file.write("ERROR from " + name + ": не получилось переставить, потому что сломались ограничения, возвращаем "
                                          "стартовое" + '\n')
        return -1


# определяем время приезда для всех локаций
def TimeOfArrival(x, y, s, file="def"):
    if file != "def":
        file.write("Начнем заполнять время прибытия\n")
    else:
        print("Начнем заполнять время прибытия\n")
    a = [[0 for k in range(len(s[0]))] for i in range(N)]
    for k in range(len(s[0])):
        if CarIsWork(y, k):
            # print("ЗАходим в рекурсию")
            RecursiaForTime(x, s, a, 0, k, 0)
    if not a:
        return -1
    return a


# Возвращает число скважин которые не уложились во временное окно
def CountskvajWithFane(s, a, i, k):
    # Если приехали во временное окно
    if E[i] <= a[i][k] <= l[i]:
        # мах на случай если уложились
        return max(0, ceil((a[i][k] + s[i][k] - l[i]) / 2))
    # Если приехали позже окончания работ
    else:
        # Возвращаем число скважин конкретно на этом объекте этой машиной
        return int(s[i][k] / (S[i] / skvaj[i]))


# Cохраняем промежуточное решение в хелпе
def SaveHelp(local_x, local_y, local_s, local_a):
    file = open('Help.txt', 'w')

    # Печатаем в файл Х
    for i in range(N):
        for j in range(N):
            for k in range(len(local_y[0])):
                file.write(str(local_x[i][j][k]) + ' ')
            file.write("\n")
        # file.write("\n")
    # Печатаем в файл Y
    for i in range(N):
        for k in range(len(local_y[0])):
            file.write(str(local_y[i][k]) + ' ')
        file.write("\n")
    # Печатаем в файл S
    for i in range(N):
        for k in range(len(local_y[0])):
            file.write(str(local_s[i][k]) + ' ')
        file.write("\n")
    # Печатаем в файл A
    for i in range(N):
        for k in range(len(local_y[0])):
            file.write(str(local_a[i][k]) + ' ')
        file.write("\n")

    file.close()


# Проверка на содержание скважин тех же объектов car у soseda
def IsContainskvaj2(sequence, client, place='all'):
    if place == 'all':
        size = len(sequence)
    else:
        size = sequence.index(place)
    for i in range(size):
        if sequence[i] == client:
            return True
    return False

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

        A[j][m] = A[i][m] + Ss[i][m] + t[i][j]

        if A[j][m] <= E[j]:
            A[j][m] = E[j]

        X[0][i][m] = 1
        X[i][j][m] = 1
        X[j][0][m] = 1
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

        A[i][m] = A[j][m] + Ss[j][m] + t[j][i]

        if A[i][m] <= E[i]:
            A[i][m] = E[i]

        X[0][j][m] = 1
        X[j][i][m] = 1
        X[i][0][m] = 1

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
def SearchSosedLeftOrRight(x, y, client, leftOrRight, k=-1):
    if k == -1:
        k = NumberCarClienta(y, client)  # номер машины которая обслуживает клиента
        # print("номер машины, которая обслуживает клиента ", k)
    if leftOrRight == "left":
        for i in range(N):  # ищем по столбцу                             ### здесь измененя
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


# удаляем клиента из выбранного  маршрут
def DeleteClientaFromPath(x, y, s, a, client, k):
    # k = NumberCarClienta(y, client)  # номер машины которая обслуживает клиента
    clientLeft = SearchSosedLeftOrRight(x, y, client, "left", k)  # ищем город перед клиентом
    clientRight = SearchSosedLeftOrRight(x, y, client, "right", k)  # ищем город после клиента
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
        a[0][k] = 0
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


# Подбрасываем монетку, берем эту окрестность или нет
def ResultCoins(monetochka=coins_Reloc):
    coins = random.choice(monetochka)
    if coins == 1:
        return True
    else:
        return False


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


# def OperatorJoin(x, y, s, a, client, sosed, arr, iterations): # p
#     Xl, Yl, Sl, Al = ReadSolutionOfFile("Relocate.txt")
#     XR, YR, SR, AR = ReadSolutionOfFile("Relocate.txt")
#
#     sosedK = NumberCarClienta(Yl, sosed)
#     clientK = NumberCarClienta(Yl, client)
#
#     sosedLeft = SearchSosedLeftOrRight(Xl, Yl, sosed, "left")  # левый сосед соседа
#     sosedRight = SearchSosedLeftOrRight(Xl, Yl, sosed, "right")  # правый сосед соседа
#
#     print("sosed_left = ", sosedLeft)
#     print("sosed_right = ", sosedRight)
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
#     # Вставляем клиента справа от соседа и смотрим что время окончания работ последовательно
#     # т.е. есди сосед справа не ноль то вставляем между кем-то, или просто вставляем справа
#     try:
#         print("Вставляем клиента к соседу справа")
#         # машина соседа будет работать у клиента столько же
#         SR[client][sosedK] = SR[client][clientK]
#
#         # Чтобы все корректно работало, сначала надо написать
#         # новое время приезда и новое время работы, потом
#         # удалить старое решение, и только потом заполнять Х и У
#         XR, YR, SR, AR = DeleteClientaFromPath(XR, YR, SR, AR, client)
#         XR[sosed][sosedRight][sosedK] = 0
#         XR[sosed][client][sosedK] = 1
#         XR[client][sosedRight][sosedK] = 1
#         YR[client][sosedK] = 1  # тепреь машина соседа обслуживает клиента
#
#         arr[0] = clientLeft
#         arr[1] = client
#         arr[2] = clientK
#         arr[3] = sosed
#         arr[4] = sosedRight
#         arr[5] = sosedK
#
#         # Подсчет времени приезда к клиенту от соседа
#         AR = TimeOfArrival(XR, YR, SR)
#
#     except IOError:
#         print("Объект не удален")
#         XR[sosed][sosedRight][sosedK] = 1
#         XR[sosed][client][sosedK] = 0
#         XR[client][sosedRight][sosedK] = 0
#         YR[client][sosedK] = 0  # тепреь машина соседа обслуживает клиента
#
#         # Подсчет времени приезда к клиенту от соседа
#         AR = TimeOfArrival(XR, YR, SR)
#
#     try:
#         print("Вставляем клиента к соседу слева")
#         # машина соседа будет работать у клиента столько же
#         Sl[client][sosedK] = Sl[client][clientK]
#
#         # Чтобы все корректно работало, сначала надонаписать
#         # новое время приезда и новое время работы, потом
#         # удалить старое решение, и только потом заполнять Х и У
#         Xl, Yl, Sl, Al = DeleteClientaFromPath(Xl, Yl, Sl, Al, client)
#         Xl[sosedLeft][sosed][sosedK] = 0
#         Xl[sosedLeft][client][sosedK] = 1
#         Xl[client][sosed][sosedK] = 1
#         Yl[client][sosedK] = 1  # теперь машина соседа обслуживает клиента
#
#         # Подсчет времени приезда к клиенту от соседа
#         Al = TimeOfArrival(Xl, Yl, Sl)
#
#     except IOError:
#         print("Объект не удален")
#         Xl[sosedLeft][sosed][sosedK] = 1
#         Xl[sosedLeft][client][sosedK] = 0
#         Xl[client][sosed][sosedK] = 0
#         Yl[client][sosedK] = 0  # теперь машина соседа обслуживает клиента
#
#         arr[0] = clientLeft
#         arr[1] = client
#         arr[2] = clientK
#         arr[3] = sosedLeft
#         arr[4] = sosed
#         arr[5] = sosedK
#
#         # Подсчет времени приезда к клиенту от соседа
#         Al = TimeOfArrival(Xl, Yl, Sl)
#
#     print("СЛЕДУЮЩИЕ ТРИ ERROR УПУСТИТЬ для левого")
#     if window_time_up(Al, Sl, Yl, K) == 0:
#         if VerificationOfBoundaryConditions(Xl, Yl, Sl, Al, "true") == 1:
#             print("NOTIFICATION from Relocate: вставили с нарушением временного окна")
#             targetL = CalculationOfObjectiveFunction(Xl, shtrafFunction(SR, AR, iterations))
#             print("Подсчет целевой функции для левого вставления ", targetL)
#         else:
#             targetL = -1
#             print(
#                 "ERROR from Relocate: из-за сломанных вышестоящих ограничений, решение не сохранено")
#     elif VerificationOfBoundaryConditions(Xl, Yl, Sl, Al) == 1:
#         print("NOTIFICATION from Relocate: вставили без нарушений ограничений")
#         targetL = CalculationOfObjectiveFunction(Xl, shtrafFunction(SR, AR, iterations))
#         print("Подсчет целевой функции для левого вставления ", targetL)
#     else:
#         targetL = -1
#         print("ERROR from Relocate: не получилось переставить, что-то пошло нет")
#
#     print("СЛЕДУЮЩИЕ ТРИ ERROR УПУСТИТЬ для правого")
#     if window_time_up(AR, SR, YR, K) == 0:
#         if VerificationOfBoundaryConditions(XR, YR, SR, AR, "true") == 1:
#             print("NOTIFICATION from Relocate: вставили с нарушением временного окна")
#             targetR = CalculationOfObjectiveFunction(XR, shtrafFunction(SR, AR,  iterations))
#             print("Подсчет целевой функции для правого вставления ", targetR)
#         else:
#             targetR = -1
#             print(
#                 "ERROR from Relocate: из-за сломанных вышестоящих ограничений, решение не сохранено")
#     elif VerificationOfBoundaryConditions(XR, YR, SR, AR) == 1:
#         print("NOTIFICATION from Relocate: вставили без нарушений ограничений")
#         targetR = CalculationOfObjectiveFunction(XR, shtrafFunction(SR, AR,iterations))
#         print("Подсчет целевой функции для правого вставления ", targetR)
#     else:
#         targetR = -1
#         print("ERROR from Relocate: не получилось переставить, что-то пошло нет")
#
#     print("Теперь ищем минимум из двух целевых")
#     minimum = min(targetL, targetR)
#     if minimum == targetL and minimum != -1:
#         iterations += 2
#         print("Выбрали левого у него целевая меньше")
#         return Xl, Yl, Sl, Al, targetL, iterations
#
#     elif minimum == targetR and minimum != -1:
#         iterations += 2
#         print("Выбрали правого у него целевая меньше")
#         return XR, YR, SR, AR, targetR, iterations
#
#     else:
#         print("Все пошло по пизде ничего не сохранили")
#         return x, y, s, a, CalculationOfObjectiveFunction(x, shtrafFunction(SR, AR, iterations)), iterations


# def Relocate(X, Y, Ss, A, target_function_start, arr, iterations):
#     # копируем чтобы не испортить решение
#     SaveSolution(X, Y, Ss, A, "Relocate.txt", 'w')
#     TargetFunction = target_function_start
#     buf_targ = 0
#
#     while TargetFunction != buf_targ:  # пока меняется
#         buf_targ = TargetFunction
#         X, Y, Ss, A = ReadSolutionOfFile("Relocate.txt")
#
#         # for Q in range(1, 7):  # это сколько я буду брать рандомных клиентов и переставлять
#         # Bыбираем клиента
#         client = random.randint(1, (
#                     N - 1))  # Берем рандомного клиента -1 потому что иногда может появится 10, а это выход за граници
#
#         print("Переставляем клиентa ", client)
#         print("С машины", NumberCarClienta(Y, client))
#
#         for sosed in range(1, N):
#             if client != sosed:
#                 sosedK = NumberCarClienta(Y, sosed)
#
#                 print("К соседу ", sosed)
#                 print("На машине ", sosedK)
#                 # print("Время перемещение от 0 до всех ", t[0])
#                 # print("Время перемещение от ", client, " до ", sosed, " = ", t[client][sosed])
#                 # print("Время перемещение от соседа до 0 ", t[sosed][0])
#
#                 x, y, s, a, target_function, iterations = OperatorJoin(X, Y, Ss, A, client, sosed, arr, iterations)
#
#                 print("Выбираем минимальное решение")
#                 minimum = min(TargetFunction, target_function)
#                 if minimum == target_function:
#                     print("Новое перемещение, лучше чем то что было, сохраняем это решение")
#                     SaveSolution(x, y, s, a, "Relocate.txt", "w")
#
#                     TargetFunction = target_function
#                 elif minimum == TargetFunction:
#                     print("Новое перемещение, хуже чем то что было, возвращаем наше старое решение")
#                     # ReadRelocateOfFile(X, Y, Ss, A)
#
#         # iterations += 1
#
#
#     ReadSolutionOfFile("Relocate.txt")
#
#     return TargetFunction, X, Y, Ss, A, iterations


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


def GettingTheSequence(X):  # получаем двумерную послед-ть
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
    for k in range(K): #len(X[0][0])
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


##############Functions for Exchange##########

# Добавляем подпоследовательности в маршрут в Exchange
def AddSubSeqInPath(X, Y, Ss, subseq1, subseq2Left, car2, time1, start=0):
    for i in range(start, len(subseq1)):
        X[subseq2Left][subseq1[i]][car2] = 1
        Y[subseq1[i]][car2] = 1
        Ss[subseq1[i]][car2] += time1[i]
        subseq2Left = subseq1[i]
    return X, Y, Ss, subseq2Left

# Проверка на содержание скважин тех же объектов car у soseda
def IsContainskvaj(sequence, client, file, place='all', flag='start'):
    file.write("IsContainskvaj start: ->\n")
    if flag == 'start':
        if place == 'all':
            size = len(sequence)
        else:
            size = sequence.index(place)
        for i in range(size+1):
            file.write("    " + str(sequence[i]) + ' == ' + str(client) + '     ')
            if sequence[i] == client:
                file.write("\nIsContainskvaj stop: <-\n")

                return True
        file.write("\nIsContainskvaj stop: <-\n")
        return False

    elif flag == 'end':
        start = sequence.index(place)
        for i in range(start, len(sequence)):
            file.write("    " + str(sequence[i]) + ' == ' + str(client) + '    ')
            if sequence[i] == client:
                file.write("\nIsContainskvaj stop: <-\n")
                return True
        file.write("\nIsContainskvaj stop: <-\n")
        return False


# Сохраняем время работы
def SaveTime(s, tail, car, file):
    file.write("    SaveTime start: ->" + '\n')
    time = []
    for i in range(len(tail)):
        index = tail[i]
        time.append(s[index][car])
    file.write("        Время работы на каждом объекте хвоста = \n")
    file.write("        " + str(time) + '\n')
    file.write("    SaveTime stop: <-\n")
    return time


# Удаление хвоста
def DeleteTail(x, y, s, a, sosed, tail, car,  file, tail0="def"):
    file.write("    DeleteTail start: ->\n")
    sos = sosed
    for i in range(len(tail)):
        x[sos][tail[i]][car] = 0
        sos = tail[i]
        y[tail[i]][car] = 0
        s[tail[i]][car] = 0
        a[tail[i]][car] = 0

    if tail0 != 'def':
        x[tail[-1]][tail0][car] = 0

    file.write("    DeleteTail stop: <-\n")
    return x, y, s, a


# печать конкретного маршрута и время работы
def PrintForCar(lokal_X, lokal_Ss, car1, file, car2):
    sequenceX2 = GettingTheSequence(lokal_X)
    file.write("car1 = " + str(sequenceX2[car1]) + '\n')
    for i in range(N):
        file.write(str(lokal_Ss[i][car1]) + ' ')
    file.write("\n")

    file.write("car2 = " + str(sequenceX2[car2]) + '\n')
    for i in range(N):
        file.write(str(lokal_Ss[i][car2]) + ' ')
    file.write("\n")


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


# функция, которая проверяет встречалось уже такое решение (полностью) в списке запретов или нет
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
