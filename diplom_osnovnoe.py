from functions import *
from math import *
# Hello world
#километровый выигрыш
km_win = [[0 for j in range(N)] for i in range(N)]
for i in range(N):
    for j in range(N):
        if i != j:
            km_win[i][j] = d[0][i] + d[0][j] - d[i][j]

for i in range(N):
    for j in range(N):
        print(d[i][j], end=" ")
    print("\n")
#Алгоритм:
#ищем макс километровый выигрыш

# x = [[[0 for k in range(K)] for j in range(N)] for i in range(N)] # едет или нет ТС с номером К из города I в J
# y= [[0 for k in range(K)] for i in range(N)] # посещает или нет ТС с номером К объект i
bufer = [[0 for k in range((N + 1) * 2)]for i in range(K)] #сохраняет последовательное посещение городов для каждой машины
flag = [0 for i in range(N)] # флажок, если посетила город
                             # N+1 так как с обеих сторон должны быть нули (выезжает из депо и возвращ в депо)

i, j = searchMax(km_win)
print("i = ", i)
print("j = ", j)
bufer[0][N] = j              #двойной массив, где первое - это номер машины, второе - это маршрут
bufer[0][N+1] = i
flag[0] = 1
flag[i] = 1
flag[j] = 1
summa = 0

for i in range(K):
    for j in range((N + 1) * 2):
        print(bufer[i][j], end=" ")
    print("\n")

while summa != N:
    summa = 0
    i, j = searchMax(km_win)          # нашли новый максимум
    print("i = ", i)
    print("j = ", j)
    print("\n")
    m, n = searchIndex(bufer, i) #если в маршруте нашли индекс i
    # print(m, " ", n)
    p, r = searchIndex(bufer, j) #  p - номер маршрута, r - номер позиции в маршруте для другого города
    #смотрим есть ли один из новых индексов в маршруте, возвращает номер маршрута в котором находится  итый город
    # m - номер маршрута, n - номер позиции в маршруте
    if m != -1 and n != -1 and p != -1 and r != -1:
        print(0)
    else:
        if m != -1 and n != -1:  # если не -1 то мы нашли
            if n > N and bufer[m][n+1] == 0:  # если больше половины и стоит 0, а не какое-то число, то вставляем в конец
                bufer[m][n + 1] = j
                flag[j] = 1
                print(1)
            elif n <= N and bufer[m][n-1] == 0:  # если меньше половины, то вставляем в начало
                bufer[m][n - 1] = j
                flag[j] = 1
                print(3)

        # print(p, " ", r)
        if p != -1 and r != -1:
            if r > N and bufer[p][r+1] == 0:  # если больше половины, то вставляем в конец
                bufer[p][r + 1] = i
                flag[i] = 1
                print(2)
            elif r <= N and bufer[p][r-1] == 0:  # если меньше половины, то вставляем в начало
                bufer[p][r - 1] = i
                flag[i] = 1
                print(4)

        if m == -1 and n == -1 and p == -1 and r == -1:
            m = search_pustoy_marchrut(bufer)  # возвращает номер маршрута, который пустой
            bufer[m][N] = j  # двойной массив, где первое - это номер машины, второе - это маршрут
            bufer[m][N + 1] = i
            flag[i] = 1
            flag[j] = 1
            print(5)
    for i in range(N):
        summa += flag[i]


    for i in range(K):
        for j in range((N + 1) * 2):
            print(bufer[i][j], end=" ")
        print("\n")

x, y, s, a = Start_solution(bufer)
result = CalculationOfObjectiveFunction(x)
print('result = ', result)

for k in range(K):
    print("Номер машины = ", k)
    for i in range(N):
        for j in range(N):
            print(x[i][j][k], end = " ")
        print("\n")
    print("\n")
    for i in range(N):
        print(y[i][k], end = ' ')
    print("\n")
#
# for i in range(N):
#     for k in range(K):
#         print(y[i][k], end = ' ')
#     print("\n")
# print("\n")
#
# for i in range(N):
#     for k in range(K):
#         print(a[i][k], end = ' ')
#     print("\n")
# print("\n")
#
# for i in range(N):
#     for k in range(K):
#         print(s[i][k], end = ' ')
#     print("\n")
# print("\n")
#
# for i in range(N):
#     print(l[i], end = ' ')
# print("\n")
assert VerificationOfBoundaryConditions(x, y, s, a) == 1




