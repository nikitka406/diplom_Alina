from math import *

# число объектов
N = 13

#набор всех ТС
K = 4

shtraf = 100
relocate_param = 10
TwoOpt_param = 30

kolvoTabu = 10

# крастность повторений круга табу
M = 2

# цена за аренду машины
# car_cost = 1000

# пороговое значение (в км)
g = 5000

# отвечает за то сколько раз вызываем операторы
NumberStartOper = 5
# NumberStartOper = 0
# if N > 30:
#     NumberStartOper = N * 20 / 100
# else:
#     NumberStartOper = N


#координаты депо и объектов
# OX = [10, 17, 6, 13, 9, 19, 8, 4, 17, 12, 6, 19, 12]
# OY = [15, 15, 15, 3, 20, 7, 8, 14, 2, 22, 12, 17, 8]
#
# #расстояние между городами: d[i][j]
# d = [[0 for j in range(N)] for i in range(N)]
# for i in range(N):
#     for j in range(N):
#         d[i][j] = sqrt(pow((OX[i] - OX[j]), 2) + pow((OY[i] - OY[j]), 2))
#         if d[i][j] > g and i == 0:
#             d[i][j] = -1
#
#
# #время перемещения между городами: t[i][j]
# t = d
# for i in range(N):
#     for j in range(N):
#         t[i][j] =(t[i][j] / 24)

# начало работы на i объекте: e[i]
#    0  1    2  3   4   5   6   7  8   9  10  11 12
E = [0, 16, 12, 36, 15, 13, 55, 8, 25, 9, 63, 11, 47]
# e = [0 for j in range(N)]
# for i in range(1, N):
#     e[i] = e[i-1] + 5
# число скважин i-го объекта k[i]
#        0  1  2  3  4  5  6  7  8  9  10 11 12
skvaj = [0, 1, 3, 2, 1, 2, 1, 1, 4, 1, 2, 1, 3]



# число рабочих дней, необходимых одному ТС для выполнения всех работ на i объекте: S[i]
S = [0 for j in range(N)]
for i in range(N):
    S[i] = skvaj[i] * 1



# конец работы на i объекте: l[i]
l = [0 for j in range(N)]

for i in range(0, N):
    l[i] = E[i] + 10*S[i]
