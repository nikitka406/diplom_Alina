from math import sqrt

# число объектов
N = 13

#набор всех ТС
K = 4

# цена за аренду машины
# car_cost = 1000

#координаты депо и объектов
OX = [10, 17, 6, 13, 9, 19, 8, 4, 17, 12, 6, 19, 12]
OY = [15, 15, 15, 3, 20, 7, 8, 14, 2, 22, 12, 17, 8]

#расстояние между городами: d[i][j]
d = [[0 for j in range(N)] for i in range(N)]
for i in range(N):
    for j in range(N):
        d[i][j] = sqrt(pow((OX[i] - OX[j]),2) + pow((OY[i] - OY[j]), 2))


# время перемещения между городами: t[i][j]
t = d
for i in range(N):
    for j in range(N):
        t[i][j] = round(t[i][j])


# число скважин i-го объекта k[i]
skvaj = [0, 1, 3, 2, 1, 2, 1, 1, 4, 1, 2, 1, 3]


# число рабочих дней, необходимых одному ТС для выполнения всех работ на i объекте: S[i]
S = [0 for j in range(N)]
for i in range(N):
    S[i] = skvaj[i] * 1


# начало работы на i объекте: e[i]
e = [0, 1, 4, 2, 4, 5, 3, 4, 1, 8, 7, 5, 3]

# конец работы на i объекте: l[i]
l = [0 for j in range(N)]
for i in range(N):
    l[i] = e[i] + S[i]