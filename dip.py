from builtins import range
from functions import *
from Input_data import *
from Operators import *
from math import *
import time
start = time.time()
ClearFiles()
iterations = 0

# d = [[0 for j in range(N)] for i in range(N)]
# for i in range(N):
#     for j in range(N):
#         d[i][j] = sqrt(pow((OX[i] - OX[j]), 2) + pow((OY[i] - OY[j]), 2))
#         if d[i][j] > g:
#             d[i][j] = 0
#             print("слишком далеко, туда не еду")
#
d = [[0 for j in range(N)] for i in range(N)]  # расстояния между городами
for i in range(N):
    for j in range(N):
        d[i][j] = 111.1 * acos(sin(OX[i]) * sin(OX[j]) + cos(OX[i]) * cos(OX[j]) * cos(OY[j] - OY[i]))
        if d[i][j] > g:
            d[i][j] = 0
            print("слишком далеко, туда не еду")


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

    else:
        print("введено неправильно right или left")

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

#километровый выигрыш
km_win = [[0 for j in range(N)] for i in range(N)]
for i in range(N):
    for j in range(N):
        if i != j:
            km_win[i][j] = d[0][i] + d[0][j] - d[i][j]

#Алгоритм:
#ищем макс километровый выигрыш

x = [[[0 for k in range(K)] for j in range(N)] for i in range(N)] # едет или нет ТС с номером К из города I в J
y = [[0 for k in range(K)] for i in range(N)] # посещает или нет ТС с номером К объект i
for k in range(K):
    y[0][k] = 1

bufer = [[0 for k in range((N + 1) * 2)]for i in range(K)] #сохраняет последовательное посещение городов для каждой машины
flag = [0 for i in range(N)] # флажок, если посетила город
                             # N так как с обеих сторон должны быть нули (выезжает из депо и возвращ в депо)
s = [[0 for k in range(K)] for i in range(N)]  # время работы ТС c номером К на объекте i
a = [[0 for k in range(K)] for i in range(N)]  # время прибытия ТС с номером К на объект i


i, j = searchMax(km_win)
X = x.copy()
Y = y.copy()
A = a.copy()
Ss = s.copy()
print("начинается процедура: добавить 2 первых города в маршрут")
AddTwoCityInRoute(i, j, 0, x, y, s, a, bufer)

flag[0] = 1
flag[i] = 1
flag[j] = 1

summa = 3 # уже построено начальное решение, а значит посетили депо и двух клиентов = 3
kolvo_Auto = 1

while summa != N:

    summa = 0
    i, j = searchMax(km_win)   # нашли новый максимум
    # print("i = ", i)
    # print("j = ", j)
    # print("\n")

    m, n = searchIndex(bufer, i) #если в маршруте нашли индекс i
    # print(m, " ", n)
    p, r = searchIndex(bufer, j) # если в маршруте нашли индекс j;
    # p - номер маршрута, r - номер позиции в маршруте для другого города
    # print(p, " ", r)
    #смотрим есть ли один из новых индексов в маршруте, возвращает номер маршрута в котором находится  итый город
    # m - номер маршрута, n - номер позиции в маршруте
    if m != -1 and n != -1 and p != -1 and r != -1:
        print("Exception : Оба города есть, то ничего не делаем")

    else:
        if m != -1 and n != -1 and p == -1 and r == -1:  # если не -1 то мы нашли индекс i
            if n > N and bufer[m][n+1] == 0:  # если больше половины и стоит 0, а не какое-то число, то вставляем в конец
                # bufer[m][n + 1] = j
                l_p = A[bufer[m][n]][m] + Ss[bufer[m][n]][m] + t[bufer[m][n]][j] # время приезда к соседу + время на работу + время от соседа до нового клиента
                Add_vershiny_k_resheniu(bufer, flag, X, Y, Ss, A, x, y, s, a, j, m, n+1, l_p, i, "right")

            elif n <= N and bufer[m][n-1] == 0:  # если меньше половины, то вставляем в начало
                if E[j] >= t[0][j]:
                    l_p = E[j] + S[j] + t[j][bufer[m][n]] # мы не можем начать работать раньше, чем временное окно
                else:
                    l_p = t[0][j] + S[j] + t[j][bufer[m][n]]
                Add_vershiny_k_resheniu(bufer, flag, X, Y, Ss, A, x, y, s, a, j, m, n - 1, l_p, i, "left")
        # else: print("Exception: нашли не индекс i, скорее всего на следующем шаге вставим в маршрут")

        if m == -1 and n == -1 and p != -1 and r != -1: #если нашли индекс j
            if r > N and bufer[p][r+1] == 0:  # если больше половины, то вставляем в конец
                l_p = A[bufer[p][r]][p] + Ss[bufer[p][r]][p] + t[bufer[p][r]][i]
                Add_vershiny_k_resheniu(bufer, flag, X, Y, Ss, A, x, y, s, a, i, p, r+1, l_p, j, "right")

            elif r <= N and bufer[p][r-1] == 0:  # если меньше половины, то вставляем в начало
                if E[i] >= t[0][i]:
                    l_p = E[i] + S[i] + t[i][bufer[m][n]] # мы не можем начать работать раньше, чем временное окно
                else:
                    l_p = t[0][i] + S[i] + t[i][bufer[m][n]]
                Add_vershiny_k_resheniu(bufer, flag, X, Y, Ss, A, x, y, s, a, i, p, r-1, l_p, j, "left")
                # l_p = A[bufer[p][r]][p] + Ss[bufer[p][r]][p] + t[bufer[p][r]][i]
                # Add_vershiny_k_resheniu(bufer, flag, X, Y, Ss, A, x, y, s, a, i, p, r-1, l_p, j, "left")

        # если ни один индекс не найден, то строим новый маршрут пока у нас есть доступные ТС, если их нет,
        # то берем новый километровй выигрыш и проходим по ифам заново
        if m == -1 and n == -1 and p == -1 and r == -1:
            if kolvo_Auto < K:
                kolvo_Auto += 1
                m = search_pustoy_marchrut(bufer)  # возвращает номер маршрута, который пустой
                # print("m = ", m)
                flag[i] = 1
                flag[j] = 1
                AddTwoCityInRoute(i, j, m, x, y, s, a, bufer)


            elif kolvo_Auto == K:
                print("Это ребро не получилось вставить")

            else:
                print("превысили количество доступных авто")

    for i in range(N):
        summa += flag[i]

print("\n")
for i in range(K):
    for j in range((N + 1) * 2):
        print(bufer[i][j], end=" ")
    print("\n")

target_function = CalculationOfObjectiveFunction(x, shtrafFunction(s, a, iterations))
print("target_function_start_solution = ", target_function)
Targer_Start = target_function
print(time.time() - start, "sec")
print(" \n")
SaveSolution(x, y, s, a, 'StartSolution.txt', 'w')

# x, y, s, a, target_function = Help(x, y, s, a, target_function, iterations)
# print("Target_function_Help = ", target_function)
# Target_Help1 = target_function

Target_Tabu = []
Sequence_Tabu = []
Best_From_Tabu = []
Best_From_Tabu.append(target_function)
Spisok_TS = []
itera = []


'''Поиск с запретами'''
for Q in range(kriteriy_ostanovki): # сколько раз я запускаю список запретов
    x, y, s, a = ReadSolutionOfFile('StartSolution.txt')
    Target_operator, x_operator, y_operator, s_operator, a_operator, SEQUENCE_operator = start_operator(x, y, s, a,
                                                                                                        iterations)
    sequenceX2 = GettingTheSequence(x_operator)
    sequenceX1 = TransferX2toX1(sequenceX2, x_operator)
    print("sequenceX1 1= ", sequenceX1)

    # x_operator, y_operator, s_operator, a_operator, Target_operator = Help(x_operator, y_operator, s_operator,
    #                                                                        a_operator, Target_operator, iterations)
    # print("Target_function_Help = ", Target_operator)
    # Target_Help2 = Target_operator
    #
    # sequenceX2 = GettingTheSequence(x_operator)
    # sequenceX1 = TransferX2toX1(sequenceX2, x_operator)
    #
    # print("sequenceX1 2= ", sequenceX1)

    # если такого решения еще не было, то

    if ProverKNaVstrechu(Sequence_Tabu, SEQUENCE_operator) != 1:
        print("Такое решение еще не встречалось")
        Spisok_TS.append(Target_operator)
        itera.append(iterations)
        if Target_operator <= min(Best_From_Tabu):
            Best_From_Tabu.append(Target_operator)

        print("Target_operator = ", Target_operator)
        SaveSolution(x_operator, y_operator, s_operator, a_operator, 'StartSolution.txt', 'w')
        sequenceSaveX2 = GettingTheSequence(x_operator)
        sequenceSaveX1 = TransferX2toX1(sequenceSaveX2, x_operator)
        print("sequence после сохранения = ", sequenceSaveX1)

        if len(Sequence_Tabu) < 7:
            print("Все хорошо, длина списка запретов < 10, сохраняем в список запретов")
            Sequence_Tabu.append(SEQUENCE_operator)
            print("на этом шаге вставляем в sequence_Tabu ", SEQUENCE_operator)
            Target_Tabu.append(Target_operator)
            print("на этом шаге вставляем в TargetTabu ", Target_operator)
            print("Target_Tabu = ", Target_Tabu)
            print("Sequence_Tabu = ", Sequence_Tabu)

        # если заполнился список запретов, то начинаем перезаписывать
        elif len(Sequence_Tabu) == 7:
            print("Начинаем потихоньку перезаписывать список запретов, потому что заполнился")
            print("\n")
            deleteSequence_Tabu = Sequence_Tabu.pop(0)
            Sequence_Tabu.append(SEQUENCE_operator)
            print("на этом шаге вставляем в Sequence_Tabu ", SEQUENCE_operator)
            deleteTabuTarget = Target_Tabu.pop(0)
            print("на этом шаге вставляем в TargetTabu ", Target_operator)
            Target_Tabu.append(Target_operator)
            print("Target_Tabu = ", Target_Tabu)
            print("Sequence_Tabu = ", Sequence_Tabu)

        else:
            x, y, s, a = ReadSolutionOfFile('StartSolution.txt')

    # если решение с мин целевой ф уже встречалось, то его никуда не сохраняем и пользуемся предыдущим решением еще раз
    else:
        print("в ProverknaVstrechu ушли в else")
        x, y, s, a = ReadSolutionOfFile('StartSolution.txt')
        print("sequenceX1 =  ", SEQUENCE_operator)
        print("\n")

    iterations += 1

print("\n")
print("Best_From_Tabu =  ", Best_From_Tabu)
print("Target_Tabu = ", Target_Tabu)
print("Sequence_Tabu = ", Sequence_Tabu)
print("\n")
print("target_function_start_solution = ", Targer_Start)
# print("target_function_Help1 = ", Target_Help1)
print("\n")
# print("target_function_Help2 = ", Target_Help2)
print("\n")
print("Spisok_TS = ", Spisok_TS)
print("Itera = ", itera)

print("kol-vo iterations = ", iterations)

##############################################


print(time.time() - start, "sec")