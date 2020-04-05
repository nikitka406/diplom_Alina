from builtins import range

from functions import *
from math import *

ClearTabu()

result = 0  # значение целевой функции
N = 13
g = 5000

OX = [10, 17, 6, 13, 9, 19, 8, 4, 17, 12, 6, 19, 12]
OY = [15, 15, 15, 3, 20, 7, 8, 14, 2, 22, 12, 17, 8]

# массив, который сохраняет перемещение оператора с минимальной целевой функцией, где М - кратность повторений списка табу
arr = [[0 for i in range(6)] for n in range(1*NumberStartOper)]    # krat - отвечает на каком круге мы сейчас (кратность круга)
# arr[][0] - клиент, ОТ которого перемещают
# arr[][1] - клиент, КОТОРОГО перемещают
# arr[][2] - машина перемещаемого клиента на которой он БЫЛ
# arr[][3] - клиент, К которому перемещают
# arr[][4] - клиент, который ТЕПЕРЬ СПРАВА от перемещаемого
# arr[][5] - машина перемещаемого клиента на которой он ТЕПЕРЬ

d = [[0 for j in range(N)] for i in range(N)]
for i in range(N):
    for j in range(N):
        d[i][j] = sqrt(pow((OX[i] - OX[j]), 2) + pow((OY[i] - OY[j]), 2))
        if d[i][j] > g:
            d[i][j] = 0
            print("слишком далеко, туда не еду")

# print("d[i][j] = ")
# for i in range(N):
#     for j in range(N):
#         print(d[i][j], end=" ")
#     print("\n")


#километровый выигрыш
km_win = [[0 for j in range(N)] for i in range(N)]
for i in range(N):
    for j in range(N):
        if i != j:
            km_win[i][j] = d[0][i] + d[0][j] - d[i][j]

# print('km_win = ')
# for i in range(N):
#     for j in range(N):
#         print(km_win[i][j], end=" ")
#     print("\n")

# t = d
# for i in range(N):
#     for j in range(N):
#         t[i][j] = (t[i][j])

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
# print("i = ", i)
# print("j = ", j)
X = x
Y = y
A = a
Ss = s
AddTwoCityInRoute(i, j, 0, x, y, s, a, bufer)

flag[0] = 1
flag[i] = 1
flag[j] = 1

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
        if E[new_client] >= l_p and l[new_client] >= l_p + S[new_client] and kyda == "right":  # если время начала работы нового клиента больше чем время прибытия + работы + переезда предыдущего
            A[new_client][car] = E[new_client]
            Zapolnenie(X, Y, Ss, "right", new_client, sosed, car, nomer_sosed)
            flag[i] = 1
            flag[j] = 1
        elif E[new_client] < l_p and l[new_client] >= l_p + S[new_client] and kyda == "right":
            A[new_client][car] = l_p
            Zapolnenie(X, Y, Ss, "right", new_client, sosed, car, nomer_sosed)
            flag[i] = 1
            flag[j] = 1
        elif l[new_client] < l_p + S[new_client]:
            print("не можем вставить, т.к. не успеет закончить работу вовремя")


    elif kyda == "left":
        ############################
        # if E[j] >= t[0][j]:
        #     l_p = E[j] + S[j] + t[j][bufer[m][n]]  # мы не можем начать работать раньше, чем временное окно
        # else:
        #     l_p = t[0][j] + S[j] + t[j][bufer[m][n]]
        ##############################
        if A[sosed][car] >= l_p and kyda == "left": #
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


summa = 3 # уже построено начальное решение, а значит посетили депо и двух клиентов = 3
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
                # flag[j] = 1
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


        if m == -1 and n == -1 and p == -1 and r == -1:
            m = search_pustoy_marchrut(bufer)  # возвращает номер маршрута, который пустой
            flag[i] = 1
            flag[j] = 1

            AddTwoCityInRoute(i, j, m, x, y, s, a, bufer)


            # for i in range(K):
            #     for j in range((N + 1) * 2):
            #         print(bufer[i][j], end=" ")
            #     print("\n")


    for i in range(N):
        summa += flag[i]


    # for i in range(K):
    #     for j in range((N + 1) * 2):
    #         print(bufer[i][j], end = " ")
    #     print("\n")

# BeautifulPrint(x, y, s, a)

# штрафная функция
def shtrafFunction(s, a):
    shtraf_sum = 0
    for i in range(N):
        for k in range(K):
            if a[i][k] + s[i][k] > l[i]:
                shtraf_sum += ((a[i][k] + s[i][k]) - l[i]) * shtraf
    return shtraf_sum

# подсчет значения целевой функции
def CalculationOfObjectiveFunction(x, shtrafFunction = 0):
    target_function = 0
    for k in range(K):
        for i in range(N):
            for j in range(N):
                target_function += d[i][j]*x[i][j][k]
    print("target_function в самой функции подсчета = ", target_function)
    target_function += shtrafFunction

    return target_function

target_function = CalculationOfObjectiveFunction(x)
print("target_function_start_solution = ", target_function)




# assert VerificationOfBoundaryConditions(X_operator[0], Y_operator[0], Ss_operator[0], A_operator[], "true") == 1

# start_operator(X_operator, Y_operator, Ss_operator, A_operator, Target_operator, x, y, s, a, target_function, arr, i)
# BeautifulPrint(x, y, s, a)
#
# SaveSolution(x, y, s, a, 'StartSolution.txt')
# ###### Печатаем оператор перемещения
# for reloc in range(NumberStartOper):
#     ReadSolutionOfFile(x, y, s, a, 'StartSolution.txt')
#     target_function = JoiningClientToNewSosed(x, y, s, a, target_function, arr, p)
# # схр изменения
#
#
#     print("target_function pri relocate operator = ", target_function)
#     print("\n")
#     BeautifulPrint(x, y, s, a)
#     print("\n")


# Поиск с запретами
# создан массив, который будет сохранять решения всех операторов, размера = кол-во операторов * заданное число в инпут дате
# Todo поменять кол-во операторов, если увеличится
X_operator, Y_operator, Ss_operator, A_operator, Target_operator = SolutionStore(1 * NumberStartOper) # лучше через ctr+shift+R
# создан массив поиска с запретами, размер = 10, заполняем
# X_tabu, Y_tabu, Ss_tabu, A_tabu, Target_tabu = SolutionStore(10)
arr_Tabu = []
Target_Tabu = []
for k in range(M):   # кратность круга (номер круга)
    for p in range(10):  # места
    # while len(arr_Tabu) < 10 and w <= 12: # чтобы while не работал бесконечное число раз, в крайнем случае сработает 20 раз
        # assert VerificationOfBoundaryConditions(X_operator[i], Y_operator[i], Ss_operator[i], A_operator[i],
        # "true") == 1
        start_operator(Target_operator, x, y, s, a, target_function, arr)

        for i in range(len(Target_operator)):
            ReadSolutionOfFile(X_operator[i], Y_operator[i], Ss_operator[i], A_operator[i], "ResultOperator.txt")
            # print("arr = ", arr[i])

        # выбирает минимум из (кол-во операторов * NumberStartOper) элементов
        min_in_target = MinFromTarget(Target_operator)
        if min_in_target != -1:
            # print("\n")
            print("index = ", min_in_target)  # печатает индекс минимального
            # index = Target_operator.index(min_in_target)
            # print("index min_in_target = ", index)
            print("Target_operator = ", Target_operator)  # печатает список длины = NumberStartOper
            print("arr_min = ", arr[min_in_target])
            print("\n")

            # если такого решения еще не было, то
            if ProverKNaVstrechu(arr_Tabu, arr[min_in_target]) != 1:
                SaveSolution(x, y, s, a, 'StartSolution.txt', 'w')

                if len(arr_Tabu) < 10:
                    print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
                    print("на этом шаге вставляем в TargetTabu ", Target_operator[min_in_target])
                    print ("на этом шаге вставляем в arrTabu ", arr[min_in_target])
                    print("\n")
                    arr_Tabu.append(arr[min_in_target])
                    Target_Tabu.append(Target_operator[min_in_target])

                elif len(arr_Tabu) == 10:
                    print("yyyyyyyyyy")
                    print("на этом шаге вставляем в TargetTabu ", Target_operator[min_in_target])
                    print("на этом шаге вставляем в arrTabu ", arr[min_in_target])
                    print("\n")
                    deleteTabuArr = arr_Tabu.pop(0)
                    arr_Tabu.append(arr[min_in_target])
                    deleteTabuTarget = Target_Tabu.pop(0)
                    Target_Tabu.append(Target_operator[min_in_target])




                # сохраняем в список запретов arr и целевую
                # SaveTabu(arr[min_in_target], Target_operator[min_in_target])
                # сохраняем решение с мин целевой функцией в StartSolution.txt
                # ReadTabu(arr_Tabu, Target_Tabu)
                # BeautifulPrint(x, y, s, a)
                # print("Target_Tabu = ", Target_Tabu)
                # print("arr_Tabu = ", arr_Tabu)
                # Zzero(X[i], Y[i], Ss[i], A[i], arr[i], Target_function[i])

            # если решение с мин целевой ф уже встречалось, то его никуда не сохраняем и пользуемся предыдущим решением еще раз
            else:
                print("SSSSSSSSSSSS в ProverknaVstrechu ушли в else")
                ReadSolutionOfFile(x, y, s, a, 'StartSolution.txt')
                print("\n")

    print("Target_Tabu = ", Target_Tabu)
    print("arr_Tabu = ", arr_Tabu)

TheBestSolution = MinFromTarget(Target_Tabu)
print("TheBestindex = ", TheBestSolution )
print("TheBestTarget = ", Target_Tabu[TheBestSolution])
print("TheBestarr = ", arr_Tabu[TheBestSolution])

    #     j = MinFromTarget(Target_operator)
    #     X_tabu[p] = X_operator[j]
    #     Y_tabu[p] = Y_operator[j]
    #     Ss_tabu[p] = Ss_operator[j]
    #     A_tabu[p] = A_operator[j]
    #     Target_tabu[p] = Target_operator[j]
    #     # print("123456789")
    #
    # print("Target_tabu = ", Target_tabu)
#
##############################################



# for TwoOp in range(TwoOpt_param):
#     target_function = RealizationTwoOpt(x, y, s, a, target_function)
#     print("target_function pri TwoOpt operator = ", target_function)



