from functions import *
from math import *

N = 13
g = 5000

OX = [10, 17, 6, 13, 9, 19, 8, 4, 17, 12, 6, 19, 12]
OY = [15, 15, 15, 3, 20, 7, 8, 14, 2, 22, 12, 17, 8]

d = [[0 for j in range(N)] for i in range(N)]
for i in range(N):
    for j in range(N):
        d[i][j] = sqrt(pow((OX[i] - OX[j]), 2) + pow((OY[i] - OY[j]), 2))
        if d[i][j] > g and i == 0:
            d[i][j] = -1


for i in range(N):
    for j in range(N):
        print(d[i][j], end=" ")
    print("\n")


#километровый выигрыш
km_win = [[0 for j in range(N)] for i in range(N)]
for i in range(N):
    for j in range(N):
        if i != j:
            km_win[i][j] = d[0][i] + d[0][j] - d[i][j]

print('km_win = ')
for i in range(N):
    for j in range(N):
        print(km_win[i][j], end=" ")
    print("\n")

t = d
for i in range(N):
    for j in range(N):
        t[i][j] = (t[i][j]/24)

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
print("i = ", i)
print("j = ", j)
X = x
Y = y
A = a
Ss = s
AddTwoCityInRoute(i, j,0, x, y, s, a, bufer)
# #####################3
# X = x
# Y = y
# A = a
# Ss = s
# # print (10)
# indicator = 0
# while indicator != 1:
#
#     bufer[0][N] = j  # двойной массив, где первое - это номер машины, второе - это маршрут
#     bufer[0][N + 1] = i
#     Y[i][0] = 1
#     Y[j][0] = 1
#     Ss[i][0] = S[i]
#     Ss[j][0] = S[j]
#     if E[j] >= t[0][j]:
#         A[j][0] = E[j]
#         # print(100)
#     else:
#         A[j][0] = t[0][j]
#     A[i][0] = A[j][0] + Ss[j][0] + t[i][j]
#     X[0][j][0] = 1
#     X[j][i][0] = 1
#     X[i][0][0] = 1
#     # print(200)
#     # BeautifulPrint(X, Y, Ss, A)
#     if window_time_up(A, Ss, Y, K) != 1:
#         X = x
#         Y = y
#         A = a
#         Ss = s
#         bufer[0][N] = i  # двойной массив, где первое - это номер машины, второе - это маршрут
#         bufer[0][N + 1] = j
#         Y[i][0] = 1
#         Y[j][0] = 1
#         Ss[i][0] = S[i]
#         Ss[j][0] = S[j]
#         # print(300)
#         if E[i] >= t[0][i]:
#             A[i][0] = E[i]
#             # print(400)
#         else:
#             A[i][0] = t[0][i]
#             # print(500)
#         A[j][0] = A[i][0] + Ss[i][0] + t[i][j]
#         X[0][i][0] = 1
#         X[i][j][0] = 1
#         X[j][0][0] = 1
#         indicator = window_time_up(A, Ss, Y, K)
#     else:
#         x = X
#         y = Y
#         a = A
#         s = Ss
#         indicator = window_time_up(A, Ss, Y, K)
#         break
        #####################
flag[0] = 1
flag[i] = 1
flag[j] = 1

# print (11)
# for i in range(K):
#     for j in range((N + 1) * 2):
#         print(bufer[i][j], end=" ")
#     print("\n")
# print (12)

summa = 0
while summa != N:
    summa = 0
    i, j = searchMax(km_win)          # нашли новый максимум
    print("i = ", i)
    print("j = ", j)
    print("\n")

    m, n = searchIndex(bufer, i) #если в маршруте нашли индекс i
    print(m, " ", n)
    p, r = searchIndex(bufer, j) #  p - номер маршрута, r - номер позиции в маршруте для другого города
    print(p, " ", r)
    #смотрим есть ли один из новых индексов в маршруте, возвращает номер маршрута в котором находится  итый город
    # m - номер маршрута, n - номер позиции в маршруте
    if m != -1 and n != -1 and p != -1 and r != -1:
        print("Оба города есть, то ничего не делаем")
    else:
        if m != -1 and n != -1 and p == -1 and r == -1:               # если не -1 то мы нашли индекс i
            if n > N and bufer[m][n+1] == 0:  # если больше половины и стоит 0, а не какое-то число, то вставляем в конец
                # bufer[m][n + 1] = j
                l_p = A[bufer[m][n]][m] + Ss[bufer[m][n]][m] + t[bufer[m][n]][j]#время приезда к соседу + время на работу + время от соседа до нового клиента
                Add_vershiny_k_resheniu(bufer, flag, X, Y, Ss, A, x, y, s, a, j, m, n+1, l_p, i, "right")
                print(1)
                flag[i] = 1
                flag[j] = 1
            elif n <= N and bufer[m][n-1] == 0:  # если меньше половины, то вставляем в начало
                # bufer[m][n - 1] = j
                if E[j] >= t[0][j]:
                    l_p = E[j] + S[j] + t[j][bufer[m][n]]
                else:
                    l_p = t[0][j] + S[j] + t[j][bufer[m][n]]
                Add_vershiny_k_resheniu(bufer, flag, X, Y, Ss, A, x, y, s, a, j, m, n - 1, l_p, i, "left")
                print(3)
                flag[i] = 1
                flag[j] = 1
        else: print("ничего не делаем")

        # print(p, " ", r)
        if m == -1 and n == -1 and p != -1 and r != -1: #если нашли индекс j
            if r > N and bufer[p][r+1] == 0:  # если больше половины, то вставляем в конец
                # bufer[p][r + 1] = i
                l_p = A[bufer[p][r]][p] + Ss[bufer[p][r]][p] + t[bufer[p][r]][i]
                Add_vershiny_k_resheniu(bufer, flag, X, Y, Ss, A, x, y, s, a, i, p, r+1, l_p, j, "right")
                print(2)
                flag[i] = 1
                flag[j] = 1
            elif r <= N and bufer[p][r-1] == 0:  # если меньше половины, то вставляем в начало
                # bufer[p][r - 1] = i
                l_p = A[bufer[p][r]][p] + Ss[bufer[p][r]][p] + t[bufer[p][r]][i]
                Add_vershiny_k_resheniu(bufer, flag, X, Y, Ss, A, x, y, s, a, i, p, r-1, l_p, j, "left")
                print(4)
                flag[i] = 1
                flag[j] = 1
        # if (m != -1 and n == -1) or (n != -1 and m == 1):
        #     print(444)

        if m == -1 and n == -1 and p == -1 and r == -1:
            m = search_pustoy_marchrut(bufer)  # возвращает номер маршрута, который пустой
            AddTwoCityInRoute(i, j, m, x, y, s, a, bufer)

            flag[i] = 1
            flag[j] = 1
            print(5)
            for i in range(K):
                for j in range((N + 1) * 2):
                    print(bufer[i][j], end=" ")
                print("\n")
            print(10)

    for i in range(N):
        summa += flag[i]

    print(summa)
    for i in range(K):
        for j in range((N + 1) * 2):
            print(bufer[i][j], end=" ")
        print("\n")
print (13)
# x, y, s, a = Start_solution(bufer)
result = CalculationOfObjectiveFunction(x)
print('result = ', result)

for i in range(K):
    for j in range((N + 1) * 2):
        print(bufer[i][j], end=" ")
    print("\n")

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
print("\n")

for i in range(N):
    for k in range(K):
        print(a[i][k], end = ' ')
    print("\n")
print("\n")
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
#assert VerificationOfBoundaryConditions(x, y, s, a) == 1




