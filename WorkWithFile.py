from Input_data import *

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


# Cохраняем стартовое решение в хелпе
def SaveStartHelp(local_x, local_y, local_s, local_a):
    file = open('StartHelp.txt', 'w')

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


def ReadStartHelpOfFile():
    local_x = [[[0 for k in range(K)] for j in range(N)] for i in
               range(N)]  # едет или нет ТС с номером К из города I в J
    local_y = [[0 for k in range(K)] for i in range(N)]  # посещает или нет ТС с номером К объект i
    for k in range(K):
        local_y[0][k] = 1
    local_s = [[0 for k in range(K)] for i in range(N)]  # время работы ТС c номером К на объекте i
    local_a = [[0 for k in range(K)] for i in range(N)]  # время прибытия ТС с номером К на объект i

    file = open('StartHelp.txt', 'r')
    # прочитали весь файл, получился список из строк файла
    line = file.readlines()

    index = 0
    # Печатаем в файл Х
    for i in range(N):
        for j in range(N):
            # for k in range(KA):
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


def ReadHelpOfFile():
    local_x = [[[0 for k in range(K)] for j in range(N)] for i in range(N)]
    # едет или нет ТС с номером К из города I в J
    local_y = [[0 for k in range(K)] for i in range(N)]  # посещает или нет ТС с номером К объект i
    for k in range(K):
        local_y[0][k] = 1
    local_s = [[0 for k in range(K)] for i in range(N)]  # время работы ТС c номером К на объекте i
    local_a = [[0 for k in range(K)] for i in range(N)]  # время прибытия ТС с номером К на объект i

    file = open('Help.txt', 'r')
    # прочитали весь файл, получился список из строк файла
    line = file.readlines()

    index = 0
    # Печатаем в файл Х
    for i in range(N):
        for j in range(N):
            # for k in range(KA):
            local_x[i][j] = line[index].split()
            for k in range(len(local_x[i][j])):
                local_x[i][j][k] = int(local_x[i][j][k])
            index += 1
            # print(index)

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


# Cохраняем промежуточное решение в релоке
def SaveStartLocalSearch(local_x, local_y, local_s, local_a):
    file = open('StartLocalSearch.txt', 'w')

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


def ReadStartLocalSearchOfFile():
    local_x = [[[0 for k in range(K)] for j in range(N)] for i in
               range(N)]  # едет или нет ТС с номером К из города I в J
    local_y = [[0 for k in range(K)] for i in range(N)]  # посещает или нет ТС с номером К объект i
    for k in range(K):
        local_y[0][k] = 1
    local_s = [[0 for k in range(K)] for i in range(N)]  # время работы ТС c номером К на объекте i
    local_a = [[0 for k in range(K)] for i in range(N)]  # время прибытия ТС с номером К на объект i

    file = open('StartLocalSearch.txt', 'r')
    # прочитали весь файл, получился список из строк файла
    line = file.readlines()

    index = 0
    # Печатаем в файл Х
    for i in range(N):
        for j in range(N):
            # for k in range(KA):
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


# Cохраняем промежуточное решение в релоке
def SaveLocalSearch(local_x, local_y, local_s, local_a ):
    file = open('LocalSearch.txt', 'w')

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


def ReadLocalSearchOfFile():
    local_x = [[[0 for k in range(K)] for j in range(N)] for i in
               range(N)]  # едет или нет ТС с номером К из города I в J
    local_y = [[0 for k in range(K)] for i in range(N)]  # посещает или нет ТС с номером К объект i
    for k in range(K):
        local_y[0][k] = 1
    local_s = [[0 for k in range(K)] for i in range(N)]  # время работы ТС c номером К на объекте i
    local_a = [[0 for k in range(K)] for i in range(N)]  # время прибытия ТС с номером К на объект i

    file = open('LocalSearch.txt', 'r')
    # прочитали весь файл, получился список из строк файла
    line = file.readlines()

    index = 0
    # Печатаем в файл Х
    for i in range(N):
        for j in range(N):
            # for k in range(KA):
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


def ClearFiles():
    file = open("TabuSearch.txt", 'w')
    file.close()
    file = open("ResultOperator.txt", 'w')
    file.close()
    file = open("Joining.txt", 'w')
    file.close()
    file = open('log/helog.txt', 'w')
    file.close()
    file = open('Help.txt', 'w')
    file.close()
    file = open('StartHelp.txt', 'w')
    file.close()
    file = open('StartLocalSearch.txt', 'w')
    file.close()
    file = open('LocalSearch.txt', 'w')
    file.close()
