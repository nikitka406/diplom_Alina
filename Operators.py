from functions import *
from Input_data import *
from WorkWithFile import *


# вклиниваем между
def OperatorJoinFromReloc(x, y, s, a, client, clientK, sosed, sosedK, arr, iterations, file):

    if client != sosed:
        Xl, Yl, Sl, Al = ReadStartLocalSearchOfFile()
        XR, YR, SR, AR = ReadStartLocalSearchOfFile()

        sosedLeft = SearchSosedLeftOrRight(Xl, Yl, sosed, "left", sosedK)  # левый сосед соседа
        sosedRight = SearchSosedLeftOrRight(Xl, Yl, sosed, "right", sosedK)  # правый сосед соседа

        clientLeft = SearchSosedLeftOrRight(x, y, client, "left")

        file.write("sosed_left = " + str(sosedLeft) + '\n')
        file.write("sosed_right = " + str(sosedRight) + '\n')

        file.write("Время окончание client = " + str(l[client]) + '\n')
        file.write("Время окончание sosed = " + str(l[sosed]) + '\n')
        file.write("Время окончание sosedLeft = " + str(l[sosedLeft]) + '\n')
        file.write("Время окончание sosedRight = " + str(l[sosedRight]) + '\n')

        # Вставляем клиента справа от соседа и смотрим что время окончания работ последовательно
        # т.е. есди сосед справа не ноль то вставляем между кем-то, или просто вставляем справа
        if sosedRight != -1:
            try:
                file.write("Вставляем клиента к соседу справа" + '\n')
                # машина соседа будет работать у клиента столько же
                if sosedK != clientK:
                    SR[client][sosedK] += SR[client][clientK]
                else:
                    buf = SR[client][clientK]

                # Чтобы все корректно работало, сначала надо написать
                # новое время приезда и новое время работы, потом
                # удалить старое решение, и только потом заполнять Х и У
                XR, YR, SR, AR = DeleteClientaFromPath(XR, YR, SR, AR, client, clientK)
                if sosedK == clientK:
                    SR[client][sosedK] += buf
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
                AR = TimeOfArrival(XR, YR, SR, file)

            except IOError:
                file.write("Объект не удален" + '\n')
                XR[sosed][sosedRight][sosedK] = 1
                XR[sosed][client][sosedK] = 0
                XR[client][sosedRight][sosedK] = 0
                YR[client][sosedK] = 0  # тепреь машина соседа обслуживает клиента

                # Подсчет времени приезда к клиенту от соседа
                AR = TimeOfArrival(XR, YR, SR, file)

        if sosedLeft != -1:
            try:
                file.write("Вставляем клиента к соседу слева" + '\n')
                # машина соседа будет работать у клиента столько же
                if sosedK != clientK:
                    Sl[client][sosedK] += Sl[client][clientK]
                else:
                    buf = Sl[client][clientK]

                # Чтобы все корректно работало, сначала надонаписать
                # новое время приезда и новое время работы, потом
                # удалить старое решение, и только потом заполнять Х и У
                Xl, Yl, Sl, Al = DeleteClientaFromPath(Xl, Yl, Sl, Al, client, clientK)
                if sosedK == clientK:
                    Sl[client][sosedK] += buf
                Xl[sosedLeft][sosed][sosedK] = 0
                Xl[sosedLeft][client][sosedK] = 1
                Xl[client][sosed][sosedK] = 1
                Yl[client][sosedK] = 1  # теперь машина соседа обслуживает клиента

                # Подсчет времени приезда к клиенту от соседа
                Al = TimeOfArrival(Xl, Yl, Sl, file)

            except IOError:
                file.write("Объект не удален" + '\n')
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
                Al = TimeOfArrival(Xl, Yl, Sl, file)

        if sosedLeft != -1 and sosedRight != -1:
            try:
                Xl, Yl, Sl, Al, targetL,  = Checker(Xl, Yl, Sl, Al, iterations, "Relocate", file)
            except TypeError:
                targetL = -1

            try:
                XR, YR, SR, AR, targetR,  = Checker(XR, YR, SR, AR, iterations, "Relocate", file)
            except TypeError:
                targetR = -1

            file.write("Теперь ищем минимум из двух целевых" + '\n')
            minimum = min(targetL, targetR)
            if minimum == targetL and minimum != -1:
                file.write("Выбрали левого у него целевая меньше" + '\n')
                return Xl, Yl, Sl, Al, targetL

            elif minimum == targetR and minimum != -1 and targetR != targetL:
                file.write("Выбрали правого у него целевая меньше" + '\n')
                return XR, YR, SR, AR, targetR

            else:
                file.write("Все пошло по пизде ничего не сохранили" + '\n')
                return x, y, s, a, CalculationOfObjectiveFunction(x, shtrafFunction(s, a, iterations))

        file.write("По какой-то причине нет соседей" + '\n')
        return x, y, s, a, CalculationOfObjectiveFunction(x, shtrafFunction(s, a, iterations))

    elif client == sosed and clientK != sosedK:
        X, Y, Ss, A = ReadStartLocalSearchOfFile()
        try:
            file.write("Клиент и сосед равны, добавляем время работы\n")
            Ss[sosed][sosedK] += Ss[client][clientK]
            X, Y, Ss, A = DeleteClientaFromPath(X, Y, Ss, A, client, clientK)
            A = TimeOfArrival(X, Y, Ss, file)

        except IOError:
            file.write("Объект не удален" + '\n')
            Ss[sosed][sosedK] -= S[client] / skvaj[client]
            Ss[client][clientK] += S[client] / skvaj[client]

        try:
            X, Y, Ss, A, target  = Checker(X, Y, Ss, A, iterations, "Two_Opt", file)
            file.write("OperatorJoinFromReloc stop: <-\n")
            return X, Y, Ss, A, target
        except TypeError:
            file.write("OperatorJoinFromReloc stop: <-\n")
            return x, y, s, a, CalculationOfObjectiveFunction(x, shtrafFunction(s, a, iterations))

    file.write("Что-то пошло не так" + '\n')
    return x, y, s, a, CalculationOfObjectiveFunction(x, shtrafFunction(s, a, iterations))


# переставляем клиента к новому соседу, локальный поиск
def Relocate(x_start, y_start, s_start, a_start, target_function_start, arr, iterations):
    file = open("log/relog.txt", 'a')
    file.write("->Relocate start" + '\n')
    file.write("Целевая функция до применения Relocate = " + str(target_function_start) + '\n')

    SaveStartLocalSearch(x_start, y_start, s_start, a_start)
    TargetFunction = target_function_start
    buf_targ = 0
    fileflag = 0

    while TargetFunction != buf_targ:
        buf_targ = TargetFunction
        X, Y, Ss, A = ReadStartLocalSearchOfFile()

        # Проходимся по всем машинам и по всем, имеющимся в них, клиентам
        for clientCar in range(K):
            for client in range(1, N):
                if Y[client][clientCar] == 1:
                    file.write("Переставляем клиентa " + str(client) + '\n')
                    file.write("С машины " + str(clientCar) + '\n')

                    for sosedK in range(K):
                        for sosed in range(1, N):
                            coins = ResultCoins()
                            if Y[sosed][sosedK] == 1 and coins == 1:  # если есть сосед в маршруте и выпала монетка
                                file.write(
                                    "Монетка сказала что рассматриваем эту окрестность coins = " + str(coins) + '\n')
                                file.write("К соседу " + str(sosed) + '\n')
                                file.write("На машине " + str(sosedK) + '\n')

                                x, y, s, a, target_function,  = OperatorJoinFromReloc(X, Y, Ss, A, client, clientCar,
                                                                                           sosed, sosedK, arr,
                                                                                           iterations, file)
                                file.write("Число используемых машин " + str(AmountCarUsed(y)) + '\n')

                                file.write("Выбираем минимальное решение" + '\n')
                                minimum = min(TargetFunction, target_function)
                                if minimum == target_function:
                                    file.write("Новое перемещение, лучше чем то что было, сохраняем это решение" + '\n')
                                    file.write("Новая целевая функция равна " + str(target_function) + '\n')

                                    SaveLocalSearch(x, y, s, a, )
                                    TargetFunction = target_function
                                    fileflag = 1
                                else:
                                    file.write(
                                        "Новое перемещение, хуже чем то что было, возвращаем наше старое решение" + '\n')
                                    file.write("Старая целевая функция равна " + str(TargetFunction) + '\n')

        # x_start, y_start, s_start, a_start = ReadStartLocalSearchOfFile()
        # target_function_start = CalculationOfObjectiveFunction(x_start, shtrafFunction(s_start, a_start,
        #                                                                                iterations))
        file.write(
            "Целевая функция последнего стартового решения = " + str(target_function_start) + '\n')

        if fileflag == 1:
            x, y, s, a = ReadLocalSearchOfFile()
            target_function = CalculationOfObjectiveFunction(x, shtrafFunction(s, a, iterations))
            file.write(
                "Целевая функция последнего минимального переставления = " + str(
                    target_function) + '\n')
            fileflag = 0
        else:
            target_function = -1

        minimum2 = min(target_function_start, target_function)
        if minimum2 == target_function and target_function != -1:
            file.write("Новое перемещение, лучше чем стартовое, сохраняем это решение" + '\n')
            file.write("Новая целевая функция равна " + str(target_function) + '\n')

            SaveStartLocalSearch(x, y, s, a, )
            target_function_start = target_function
            TargetFunction = target_function
        else:
            file.write("Новое перемещение, хуже чем последние добавленое стартовое решение" + '\n')
            file.write("Старая целевая функция равна " + str(target_function_start) + '\n')

    file.write("While stop\n")
    x_start, y_start, s_start, a_start = ReadStartLocalSearchOfFile()

    file.write("<-Relocate stop" + '\n')
    file.close()

    return x_start, y_start, s_start, a_start, target_function_start


def OperatorJoinFromHelp(x, y, s, a, client, clientCar, sosed, sosedCar, target_function_start, iterations, flag, file):
    file.write("OperatorJoinFromHelp start: ->\n")
    target_function = target_function_start

    file.write("    Проверяем на равенство клиента и соседа\n")
    if client == sosed:
        file.write("    Равны\n")
        X, Y, Ss, A = ReadStartHelpOfFile()

        file.write("    Время работы до забирания скважины " + str(Ss[client][clientCar]) + "\n")
        Ss[client][clientCar] -= S[client] / skvaj[client]
        file.write("    Время работы после забирания скважины " + str(Ss[client][clientCar]) + "\n")

        Ss[sosed][sosedCar] += S[client]/skvaj[client]
        if flag == 'last':
            file.write("    Забрали с объекта все скважины, и эта оказаласть последняя, "
                       "    значит надо удалить посещение этого объекта в старом маршруте" + '\n')
            X, Y, Ss, A = DeleteClientaFromPath(X, Y, Ss, A, client)

        A = TimeOfArrival(X, Y, Ss, file)

        try:
            X, Y, Ss, A, target_function = Checker(X, Y, Ss, A, iterations, "Help", file)
            file.write("    OperatorJoinFromHelp stop: <-\n")
            return X, Y, Ss, A, target_function
        except TypeError:
            file.write("    OperatorJoinFromHelp stop: <-\n")
            return x, y, s, a, target_function_start

    if not IsContainskvaj(y, client, sosedCar):
        file.write("    Не равны\n")
        Xl, Yl, Sl, Al = ReadStartHelpOfFile()
        XR, YR, SR, AR = ReadStartHelpOfFile()

        file.write("    Время работы до забирания скважины " + str(Sl[client][clientCar]) + "\n")
        file.write("    Забираем проебанную скважину\n")
        Sl[client][clientCar] -= S[client] / skvaj[client]
        SR[client][clientCar] -= S[client] / skvaj[client]
        file.write("    Время работы после забирания скважины " + str(Sl[client][clientCar]) + "\n")

        sosedLeft = SearchSosedLeftOrRight(Xl, Yl, sosed, "left", sosedCar)  # левый сосед соседа
        sosedRight = SearchSosedLeftOrRight(Xl, Yl, sosed, "right", sosedCar)  # правый сосед соседа

        file.write("    sosed_left = " + str(sosedLeft) + '\n')
        file.write("    sosed_right = " + str(sosedRight) + '\n')

        file.write("    Время окончание client = " + str(l[client]) + '\n')
        file.write("    Время окончание sosed = " + str(l[sosed]) + '\n')
        file.write("    Время окончание sosedLeft = " + str(l[sosedLeft]) + '\n')
        file.write("    Время окончание sosedRight = " + str(l[sosedRight]) + '\n')

        # Вставляем клиента справа от соседа и смотрим что время окончания работ последовательно
        # т.е. есди сосед справа не ноль то вставляем между кем-то, или просто вставляем справа
        try:
            file.write("    Вставляем скважину к соседу справа" + '\n')
            # машина соседа будет работать у клиента столько же
            SR[client][sosedCar] += S[client]/skvaj[client]

            # на случай если мы в итоге все скважины забрали, и эта была последняя
            if flag == 'last':
                file.write("    Забрали с объекта все скважины, и эта оказаласть последняя, "
                           "    значит надо удалить посещение этого объекта в старом маршруте" + '\n')
                XR, YR, SR, AR = DeleteClientaFromPath(XR, YR, SR, AR, client)

            XR[sosed][client][sosedCar] = 1
            if client != sosedRight:
                file.write("    Сосед справа не равен клиенту\n")
                XR[client][sosedRight][sosedCar] = 1
            YR[client][sosedCar] = 1  # тепреь машина соседа обслуживает клиента
            XR[sosed][sosedRight][sosedCar] = 0

            # Подсчет времени приезда к клиенту от соседа
            AR = TimeOfArrival(XR, YR, SR, file)

        except IOError:
            file.write("    Объект не удален" + '\n')
            XR[sosed][sosedRight][sosedCar] = 1
            XR[sosed][client][sosedCar] = 0
            XR[client][sosedRight][sosedCar] = 0
            YR[client][sosedCar] = 0  # тепреь машина соседа обслуживает клиента

            # Подсчет времени приезда к клиенту от соседа
            AR = TimeOfArrival(XR, YR, SR, file)

        try:
            file.write("    Вставляем клиента к соседу слева" + '\n')
            # машина соседа будет работать у клиента столько же
            Sl[client][sosedCar] += S[client]/skvaj[client]

            # на случай если мы в итоге все скважины забрали, и эта была последняя
            if flag == 'last':
                file.write("    Забрали с объекта все скважины, и эта оказаласть последняя, "
                           "    значит надо удалить посещение этого объекта в старом маршруте" + '\n')
                Xl, Yl, Sl, Al = DeleteClientaFromPath(Xl, Yl, Sl, Al, client)

            Xl[sosedLeft][sosed][sosedCar] = 0
            if sosedLeft != client:
                Xl[sosedLeft][client][sosedCar] = 1
            Xl[client][sosed][sosedCar] = 1
            Yl[client][sosedCar] = 1  # теперь машина соседа обслуживает клиента

            # Подсчет времени приезда к клиенту от соседа
            Al = TimeOfArrival(Xl, Yl, Sl, file)

        except IOError:
            file.write("    Объект не удален")
            Xl[sosedLeft][sosed][sosedCar] = 1
            Xl[sosedLeft][client][sosedCar] = 0
            Xl[client][sosed][sosedCar] = 0
            Yl[client][sosedCar] = 0  # теперь машина соседа обслуживает клиента

            # Подсчет времени приезда к клиенту от соседа
            Al = TimeOfArrival(Xl, Yl, Sl, file)

        try:
            Xl, Yl, Sl, Al, targetL = Checker(Xl, Yl, Sl, Al, iterations, "Help", file)
        except TypeError:
            targetL = -1

        try:
            XR, YR, SR, AR, targetR = Checker(XR, YR, SR, AR, iterations, "Help", file)
        except TypeError:
            targetR = -1

        file.write("    Теперь ищем минимум из двух целевых" + '\n')
        minimum = min(targetL, targetR)
        if minimum == targetL and minimum != -1:
            file.write("    Выбрали левого у него целевая меньше" + '\n')
            file.write("OperatorJoinFromHelp stop: <-\n")
            return Xl, Yl, Sl, Al, targetL

        elif minimum == targetR and minimum != -1 and targetR != targetL:
            file.write("    Выбрали правого у него целевая меньше" + '\n')
            file.write("OperatorJoinFromHelp stop: <-\n")
            return XR, YR, SR, AR, targetR

        else:
            file.write("    Все пошло по пизде ничего не сохранили" + '\n')
            file.write("OperatorJoinFromHelp stop: <-\n")
            return x, y, s, a, CalculationOfObjectiveFunction(x, shtrafFunction(s, a, iterations))

    file.write("    В этом маршруте есть такой объект, вернемся к нему позже\n")
    file.write("OperatorJoinFromHelp stop: <-\n")
    return x, y, s, a, CalculationOfObjectiveFunction(x, shtrafFunction(s, a, iterations))


# Возможность приезжать нескольким машинам на одну локацию
def Help(Xstart, Ystart, Sstart, Astart, target_function_start, iterations):
    file = open("log/helog.txt", 'w')
    file.write("Help start: ->" + '\n')

    SaveStartHelp(Xstart, Ystart, Sstart, Astart)

    file.write("Начинаем поиск объектов, которые в маршруте не успевают закончить работу\n")
    file_flag = 0
    for k in range(K):
        for client in range(1, N):
            if Ystart[client][k] == 1:
                if Astart[client][k] + Sstart[client][k] > l[client]:
                    file.write("Нашли объект который опаздывает " + str(client) + " который обслуживает машина "
                               + str(k) + '\n')
                    contskvaj = CountskvajWithFane(Sstart, Astart, client, k)
                    file.write("Всего не укладывается " + str(contskvaj) + " скважин\n")

                    for proebSkv in range(contskvaj):
                        X, Y, Ss, A = ReadStartHelpOfFile()
                        TargetFunction = target_function_start

                        flag = 0
                        if S[client]/skvaj[client] > 0:
                            flag = 'not the last'
                        elif S[client]/skvaj[client] == 0:
                            flag = 'last'
                        else:
                            flag = 'end'

                        if flag != 'end':
                            file.write("Сейчас " + flag + " скважина\n")
                            file.write("Начинаем цикл по присовыванию везде (по машинам)\n")
                            for sosedK in range(K):
                                if sosedK != k:
                                    file.write("Сейчас рассматриваем " + str(sosedK) + " машину\n")
                                    file.write("Она не похожа на ту из которой взяли скважину\n")

                                    file.write("Начинаем цикл по объектам в этой машине\n")
                                    for sosed in range(1, N):
                                        if Y[sosed][sosedK] == 1:
                                            file.write("Рассматриваемый объект " + str(sosed)+"\n")
                                            file.write(
                                                "Попробую одну скважину с объекта " + str(client) + " и машины " + str(
                                                    k)+"\n")
                                            file.write(" отдать машине " + str(sosedK) + " рядом с объектом " + str(
                                                sosed) + "\n")

                                            x, y, s, a, target_function = OperatorJoinFromHelp(X, Y, Ss, A, client, k,
                                                                                                 sosed, sosedK,
                                                                                                 TargetFunction,
                                                                                                 iterations, flag,
                                                                                                 file)
                                            file.write(
                                                "Число используемых машин теперь " + str(AmountCarUsed(y)) + '\n')

                                            file.write(
                                                "Выбираем минимальное решение из стартового и измененного" + '\n')
                                            minimum1 = min(TargetFunction, target_function)
                                            if minimum1 == target_function:
                                                file.write(
                                                    "Новое перемещение, лучше чем то что было, сохраняем это решение"+'\n')
                                                file.write("Новая целевая функция равна " + str(target_function) + '\n')

                                                SaveHelp(x, y, s, a)
                                                TargetFunction = target_function

                                                file_flag = 1
                                            else:
                                                file.write("Новое перемещение, хуже чем то что было, возвращаем наше "
                                                           "старое решение" + '\n')
                                                file.write("Старая целевая функция равна " + str(TargetFunction) + '\n')
                                            file.write('\n')

                        # Xstart, Ystart, Sstart, Astart = ReadStartHelpOfFile()
                        # target_function_start = CalculationOfObjectiveFunction(Xstart, shtrafFunction(Sstart, Astart, 1))
                        file.write(
                            "Целевая функция последнего стартового решения = " + str(target_function_start) + '\n')

                        if file_flag == 1:
                            x, y, s, a = ReadHelpOfFile()
                            target_function = CalculationOfObjectiveFunction(x, shtrafFunction(s, a, 1))
                            file.write(
                                "Целевая функция последнего минимального переставления = " + str(
                                    target_function) + '\n')
                            file_flag = 0

                        else:
                            target_function = -1

                        minimum2 = min(target_function_start, target_function)
                        if minimum2 == target_function and target_function != -1:
                            file.write("Новое перемещение, лучше чем стартовое, сохраняем это решение" + '\n')
                            file.write("Новая целевая функция равна " + str(target_function) + '\n')

                            SaveStartHelp(x, y, s, a)
                            target_function_start = target_function

                        else:
                            file.write("Новое перемещение, хуже чем последние добавленое стартовое решение" + '\n')
                            file.write("Старая целевая функция равна " + str(target_function_start) + '\n')
                            return Xstart, Ystart, Sstart, Astart, target_function_start

    file.write("По максимуму постарались поделиться скважинами" + '\n')
    Xstart, Ystart, Sstart, Astart = ReadStartHelpOfFile()
    for k in range(K):
        for i in range(N):
            for j in range(N):
                file.write(str(Xstart[i][j][k]) + ' ')
            file.write("\n")
        file.write("\n")

    Xstart, Ystart, Sstart, Astart = ReadStartHelpOfFile()
    file.write("<-Help stop" + '\n')
    file.close()

    return Xstart, Ystart, Sstart, Astart, target_function_start


# Применяю операторы для решения: заполняю массив, сколько операторов, столько и форов
def start_operator(local_target_function, local_x, local_y, local_s, local_a, arr, iterations):
    # сначала для оператора перемещения:
    SaveSolution(local_x, local_y, local_s, local_a, 'StartSolution.txt', 'w')

    for i in range(NumberStartOper):
        target_function = 999999999999999999999
        x_reloc, y_reloc, s_reloc, a_reloc, Target_function_reloc = Relocate(local_x, local_y, local_s,
                                                                             local_a, target_function,
                                                                             arr, iterations)
        print("Target_function_reloc = ", Target_function_reloc)

        minimum = min(Target_function_reloc, target_function)
        if minimum == Target_function_reloc:
            SaveSolution(local_x, local_y, local_s, local_a, 'ResultOperator.txt', 'w')
            target_function = Target_function_reloc
            print("target in reloc = ", target_function)

    x_reloc, y_reloc, s_reloc, a_reloc = ReadSolutionOfFile('ResultOperator.txt')

    # iterations += 1

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

    return target_function, x_reloc, y_reloc, s_reloc, a_reloc, iterations

    # TODO  Раскоментить, когда появится 2-Opt
    # прочитали стартовое решение, чтобы все делать с 2-Opt:
    # local_x, local_y, local_s, local_a = ReadSolutionOfFile('StartSolution.txt')
    # TODO считаем локальный минимум для 2-Opt
    # minimum = min(Target_function_reloc, Target_function_TwoOpt)
    # if minimum == Target_function_reloc:
    #     return Target_function_reloc, x_reloc, y_reloc, s_reloc, a_reloc
    # elif minimum == Target_function_TwoOpt:
    #     return Target_function_TwoOpt, x_TwoOpt, y_TwoOpt, s_TwoOpt, a_TwoOpt