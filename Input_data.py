from math import *
import csv

# # число объектов
# N = 13
#
# #набор всех ТС
# K = 3

shtraf = 1.03
prostoy = 0.5
coins = [0, 1, 2, 3, 4, 5, 6] #, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]  # Значение монетки, сколько значений такая вероятность
param_len_subseq = 2  # максимальная длина подпоследовательности в exchange, если 2 - значит состоит из трех элементов
# param_local_search = 20 # сколько раз пересатвляем каждую скважину к каждому объекту
# кратность повторений круга табу
# M = 2

# пороговое значение (в км)
g = 300

path = "input/25/"

v = 50  # скорость ТС
# Создаем пустые списки для входных данных

OX = []
OY = []
S = []
skvaj = []
E = []
l = []
N = 0
K = 0


# Читаем файл с клиентами
FILENAME1 = path + "customers1.csv"

with open(FILENAME1) as File:
    reader = csv.reader(File, delimiter=';', quotechar=';',
                        quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        if row[0] != 'Name':
            OX.append(float(row[1]))
            OY.append(float(row[2]))
            S.append(float(row[3]))
            skvaj.append(float(row[4]))
            E.append(float(row[5]))
            l.append(float(row[6]))
            N += 1

# Теперь разворачиваем решение чтобы депо было в начале
OX.reverse()
OY.reverse()
S.reverse()
skvaj.reverse()
E.reverse()
l.reverse()
# Читаем файл с машинками, из него берем координаты для депо и добавляем в конец,
# для депо ставим 0 работ , 0 скважин и нулевое время
FILENAME2 = path + "vehicles1.csv"

with open(FILENAME2) as File:
    reader = csv.reader(File, delimiter=';', quotechar=';',
                        quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        if row[0] == 'Vehicle 1':
            OX.append(float(row[1]))
            OY.append(float(row[2]))
            S.append(0)
            skvaj.append(0)
            E.append(0)
            l.append(0)
            N += 1

        # Считаем кол-во машин
        if row[0] != 'Name':
            K += 1

# Теперь разворачиваем решение чтобы депо было в начале
OX.reverse()
OY.reverse()
S.reverse()
skvaj.reverse()
E.reverse()
l.reverse()

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


# print("d = ")
# for i in range(N):
#     for j in range(N):
#         print(d[i][j], end=' ')
#     print('\n')
# print('\n')
#
# print("t = ")
# for i in range(N):
#     for j in range(N):
#         print(t[i][j], end=' ')
#     print('\n')
# print('\n')

for i in range(N):
    print(OX[i], " ", OY[i], " ", S[i], " ", skvaj[i], " ", E[i], " ", l[i])
#
print("K = ", K)
print("N = ", N)

# столько мест заполнилось в списке запретов
kriteriy_ostanovki = 10

# отвечает за то сколько раз вызываем операторы
NumberStartOper = 10
# NumberStartOper = 0
# if N > 60:
#     NumberStartOper = int(N * 20 / 100)
# elif 30 < N <= 60:
#     NumberStartOper = int(N * 30 / 100)
# else:
#     NumberStartOper = N



relocate_param = 10
TwoOpt_param = 30

# kolvoTabu = 10

# #координаты депо и объектов
# OX = [10, 17, 6, 13, 9, 19, 8, 4, 17, 12, 6, 19, 12]
# OY = [15, 15, 15, 3, 20, 7, 8, 14, 2, 22, 12, 17, 8]
# # #
# # #
# # #
# # # #время перемещения между городами: t[i][j]
# # # t = d
# # # for i in range(N):
# # #     for j in range(N):
# # #         t[i][j] =(t[i][j] / 24)
# #
# # начало работы на i объекте: e[i]
# #    0  1    2  3   4   5   6   7  8   9  10  11 12
# E = [0, 16, 12, 36, 15, 13, 55, 8, 25, 9, 63, 11, 47]
#
# # число скважин i-го объекта k[i]
# #        0  1  2  3  4  5  6  7  8  9  10 11 12
# skvaj = [0, 1, 3, 2, 1, 2, 1, 1, 4, 1, 2, 1, 3]
#
# # число рабочих дней, необходимых одному ТС для выполнения всех работ на i объекте: S[i]
# S = [0 for j in range(N)]
# for i in range(N):
#     S[i] = skvaj[i] * 1
#
#
# # конец работы на i объекте: l[i]
# l = [0 for j in range(N)]
#
# for i in range(0, N):
#     l[i] = E[i] + 10*S[i]

