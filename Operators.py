from functions import *
from Input_data import *
from WorkWithFile import *


# вклиниваем между
def OperatorJoinFromReloc(x, y, s, a, target_function_start, client, clientK, sosed, sosedK, iterations, file):
    if client != sosed:
        Xl, Yl, Sl, Al = ReadStartLocalSearchOfFile()
        XR, YR, SR, AR = ReadStartLocalSearchOfFile()
        X, Y, Ss, A = ReadStartLocalSearchOfFile()

        sosedLeft = SearchSosedLeftOrRight(Xl, Yl, sosed, "left", sosedK)  # левый сосед соседа
        sosedRight = SearchSosedLeftOrRight(Xl, Yl, sosed, "right", sosedK)  # правый сосед соседа

        clientLeft = SearchSosedLeftOrRight(Xl, Yl, client, "left", clientK)
        clientRight = SearchSosedLeftOrRight(Xl, Yl, sosed, "right", sosedK)

        file.write("sosed_left = " + str(sosedLeft) + '\n')
        file.write("sosed_right = " + str(sosedRight) + '\n')

        file.write("Время окончание client = " + str(l[client]) + '\n')
        file.write("Время окончание sosed = " + str(l[sosed]) + '\n')
        file.write("Время окончание sosedLeft = " + str(l[sosedLeft]) + '\n')
        file.write("Время окончание sosedRight = " + str(l[sosedRight]) + '\n')

        # Вставляем клиента справа от соседа и смотрим что время окончания работ последовательно
        # т.е. есди сосед справа не ноль то вставляем между кем-то, или просто вставляем справа
        if sosedRight != -1 and sosed != 0:
            try:
                file.write("Вставляем клиента к соседу справа" + '\n')
                # машина соседа будет работать у клиента столько же
                buf = 0
                if sosedK != clientK:
                    SR[client][sosedK] += SR[client][clientK]
                else:
                    buf = SR[client][clientK]

                # Чтобы все корректно работало, сначала надо написать
                # новое время приезда и новое время работы, потом
                # удалить старое решение, и только потом заполнять Х и У
                XR, YR, SR, AR = DeleteClientaFromPath(XR, YR, SR, AR, client, clientK)
                # print("Beautiful print R: ")
                # BeautifulPrint(XR, YR, SR, AR)

                if sosedK == clientK:
                    SR[client][sosedK] += buf
                XR[sosed][sosedRight][sosedK] = 0
                XR[sosed][client][sosedK] = 1
                XR[client][sosedRight][sosedK] = 1
                YR[client][sosedK] = 1  # теперь машина соседа обслуживает клиента

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

            try:
                XR, YR, SR, AR, targetR = Checker(XR, YR, SR, AR, iterations, "Relocate", file)
            except TypeError:
                targetR = -1

        if sosedLeft != -1 and sosed != 0:
            try:
                file.write("Вставляем клиента к соседу слева" + '\n')
                # машина соседа будет работать у клиента столько же
                buf = 0
                if sosedK != clientK:
                    Sl[client][sosedK] += Sl[client][clientK]
                else:
                    buf = Sl[client][clientK]

                # Чтобы все корректно работало, сначала надонаписать
                # новое время приезда и новое время работы, потом
                # удалить старое решение, и только потом заполнять Х и У
                Xl, Yl, Sl, Al = DeleteClientaFromPath(Xl, Yl, Sl, Al, client, clientK)
                # print("Beautiful print L: ")
                # BeautifulPrint(Xl, Yl, Sl, Al)

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

                # Подсчет времени приезда к клиенту от соседа
                Al = TimeOfArrival(Xl, Yl, Sl, file)

            try:
                Xl, Yl, Sl, Al, targetL = Checker(Xl, Yl, Sl, Al, iterations, "Relocate", file)
            except TypeError:
                targetL = -1

        else:
            targetL = -1

        if sosed == 0 and not CarIsWork(YR, sosedK):
            try:
                file.write("    Вставляем скважину в новый маршрут" + '\n')
                # машина соседа будет работать у клиента столько же
                SR[client][sosedK] += SR[client][clientK]

                XR, YR, SR, AR = DeleteClientaFromPath(XR, YR, SR, AR, client, clientK)

                XR[sosed][client][sosedK] = 1
                XR[client][sosed][sosedK] = 1
                YR[sosed][sosedK] = 1
                YR[client][sosedK] = 1  # теперь машина соседа обслуживает клиента

                # Подсчет времени приезда к клиенту от соседа
                AR = TimeOfArrival(XR, YR, SR, file)

            except IOError:
                file.write("    Объект не удален" + '\n')

                XR[sosed][sosedRight][sosedK] = 1
                XR[sosed][client][sosedK] = 0
                XR[client][sosedRight][sosedK] = 0
                YR[client][sosedK] = 0  # тепреь машина соседа обслуживает клиента

                # Подсчет времени приезда к клиенту от соседа
                AR = TimeOfArrival(XR, YR, SR, file)

            try:
                XR, YR, SR, AR, targetR, sizeK = Checker(XR, YR, SR, AR, iterations, "Reloc", file)
                file.write("OperatorJoinFromReloc stop: <-\n")
                return XR, YR, SR, AR, targetR, sizeK
            except TypeError:
                file.write("OperatorJoinFromReloc stop: <-\n")
                return x, y, s, a, target_function_start


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
            return x, y, s, a, target_function_start


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
            X, Y, Ss, A, target = Checker(X, Y, Ss, A, iterations, "Reloc", file)
            file.write("OperatorJoinFromReloc stop: <-\n")
            return X, Y, Ss, A, target
        except TypeError:
            file.write("OperatorJoinFromReloc stop: <-\n")
            return x, y, s, a, target_function_start

    file.write("Что-то пошло не так" + '\n')
    return x, y, s, a, target_function_start


# переставляем клиента к новому соседу, локальный поиск
def Relocate(x_start, y_start, s_start, a_start, target_function_start, iterations):
    file = open("log/relog.txt", 'a')
    file.write("->Relocate start" + '\n')
    file.write("Целевая функция до применения Relocate = " + str(target_function_start) + '\n')

    SaveStartLocalSearch(x_start, y_start, s_start, a_start)
    TargetFunction = target_function_start
    SEQUENCE = []
    buf_targ = 0
    fileflag = 0

    # it = 0
    # while it < param_local_search:         #TargetFunction != buf_targ:
    #     buf_targ = TargetFunction
    X, Y, Ss, A = ReadStartLocalSearchOfFile()

    # Проходимся по всем машинам и по всем, имеющимся в них, клиентам
    for clientCar in range(K):
        for client in range(1, N):
            if Y[client][clientCar] == 1:
                file.write("Переставляем клиентa " + str(client) + '\n')
                file.write("С машины " + str(clientCar) + '\n')

                for sosedK in range(K):
                    for sosed in range(N):
                        if ResultCoins():
                            file.write(
                                "Монетка сказала что рассматриваем эту окрестность " + '\n')
                            file.write("\n")
                            # если есть сосед в маршруте и выпала монетка
                            if (Y[sosed][sosedK] == 1 and sosed != 0) or (sosed == 0 and not CarIsWork(Y, sosedK)):
                                file.write("К соседу " + str(sosed) + '\n')
                                file.write("На машине " + str(sosedK) + '\n')

                                x, y, s, a, target_function = OperatorJoinFromReloc(X, Y, Ss, A, target_function_start,
                                                                                    client, clientCar, sosed, sosedK,
                                                                                    iterations, file)
                                file.write("Число используемых машин " + str(AmountCarUsed(y)) + '\n')

                                file.write("Выбираем минимальное решение" + '\n')
                                minimum = min(TargetFunction, target_function)
                                if minimum == target_function:
                                    file.write("Новое перемещение, лучше чем то что было, сохраняем это решение" + '\n')
                                    file.write("Новая целевая функция на этом шаге = " + str(target_function) + '\n')
                                    file.write("\n")

                                    SaveLocalSearch(x, y, s, a)
                                    TargetFunction = target_function
                                    fileflag = 1
                                else:
                                    file.write(
                                        "Новое перемещение, хуже чем то что было, возвращаем наше старое решение" + '\n')
                                    file.write("А старая целевая функция была равна " + str(TargetFunction) + '\n')
                                    file.write("\n")

                        else:
                            file.write(
                                "Монетка сказала что не рассматриваем эту окрестность " + '\n')

    file.write(
        "Целевая функция последнего стартового решения = " + str(target_function_start) + '\n')

    if fileflag == 1:
        x, y, s, a = ReadLocalSearchOfFile()
        target_function = CalculationOfObjectiveFunction(x, shtrafFunction(s, a, iterations))
        file.write(
            "Целевая функция последнего минимального переставления = " + str(target_function) + '\n')
        fileflag = 0
    else:
        target_function = -1

    minimum2 = min(target_function_start, target_function)
    if minimum2 == target_function and target_function != -1:
        file.write("Новое перемещение, лучше чем стартовое, сохраняем это решение" + '\n')
        file.write("Новая целевая функция равна " + str(target_function) + '\n')

        SaveStartLocalSearch(x, y, s, a)
        target_function_start = target_function
        TargetFunction = target_function
        sequenceX2 = GettingTheSequence(x)
        SEQUENCE = TransferX2toX1(sequenceX2, x)

    else:
        file.write("Новое перемещение, хуже чем последние добавленое стартовое решение" + '\n')
        file.write("Старая целевая функция равна " + str(target_function_start) + '\n')


    file.write("While stop\n")
    x_start, y_start, s_start, a_start = ReadStartLocalSearchOfFile()

    file.write("<-Relocate stop" + '\n')
    file.close()

    return x_start, y_start, s_start, a_start, target_function_start, SEQUENCE


def OperatorJoinFromHelp(x, y, s, a, client, clientCar, sosed, sosedCar, timeWork, target_function_start, iterations, flag, file):
    file.write("OperatorJoinFromHelp start: ->\n")
    target_function = target_function_start

    sequenceX2 = GettingTheSequence(x)

    file.write("    Проверяем на равенство клиента и соседа\n")
    if client == sosed:
        file.write("    Равны\n")
        X, Y, Ss, A = ReadStartHelpOfFile()

        file.write("    Время работы до забирания скважины " + str(Ss[client][clientCar]) + "\n")
        Ss[client][clientCar] -= timeWork
        file.write("    Время работы после забирания скважины " + str(Ss[client][clientCar]) + "\n")

        Ss[sosed][sosedCar] += timeWork
        if flag == 'last':
            file.write("    Забрали с объекта все скважины, и эта оказаласть последняя, \n"
                       "    значит надо удалить посещение этого объекта в старом маршруте" + '\n')
            X, Y, Ss, A = DeleteClientaFromPath(X, Y, Ss, A, client, clientCar)

        A = TimeOfArrival(X, Y, Ss, file)

        try:
            X, Y, Ss, A, target_function = Checker(X, Y, Ss, A, iterations, "Help", file)
            file.write("    OperatorJoinFromHelp stop: <-\n")
            return X, Y, Ss, A, target_function
        except TypeError:
            file.write("    OperatorJoinFromHelp stop: <-\n")
            return x, y, s, a, target_function_start

    elif not IsContainskvaj2(sequenceX2[sosedCar], client):
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
        if sosedRight != -1:
            try:
                file.write("    Вставляем скважину к соседу справа" + '\n')
                # машина соседа будет работать у клиента столько же
                SR[client][sosedCar] += timeWork

                # на случай если мы в итоге все скважины забрали, и эта была последняя
                if flag == 'last':
                    file.write("    Забрали с объекта все скважины, и эта оказаласть последняя, "
                               "    значит надо удалить посещение этого объекта в старом маршруте" + '\n')
                    XR, YR, SR, AR = DeleteClientaFromPath(XR, YR, SR, AR, client, clientCar)

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
                YR[client][sosedCar] = 0  # теперь машина соседа обслуживает клиента

                # Подсчет времени приезда к клиенту от соседа
                AR = TimeOfArrival(XR, YR, SR, file)

            try:
                XR, YR, SR, AR, targetR = Checker(XR, YR, SR, AR, iterations, "Help", file)
            except TypeError:
                targetR = -1
        else:
            targetR = -1

        if sosedLeft != -1:
            try:
                file.write("    Вставляем клиента к соседу слева" + '\n')
                # машина соседа будет работать у клиента столько же
                Sl[client][sosedCar] += S[client] / skvaj[client]

                # на случай если мы в итоге все скважины забрали, и эта была последняя
                if flag == 'last':
                    file.write("    Забрали с объекта все скважины, и эта оказаласть последняя, "
                               "    значит надо удалить посещение этого объекта в старом маршруте" + '\n')
                    Xl, Yl, Sl, Al = DeleteClientaFromPath(Xl, Yl, Sl, Al, client, clientCar)

                Xl[sosedLeft][sosed][sosedCar] = 0
                if sosedLeft != client:
                    file.write("    Сосед слева не равен клиенту\n")
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
        else:
            targetL = -1

        if sosed == 0 and not CarIsWork(YR, sosedCar):
            try:
                file.write("    Вставляем скважину в новый маршрут" + '\n')
                # машина соседа будет работать у клиента столько же
                SR[client][sosedCar] += timeWork

                # на случай если мы в итоге все скважины забрали, и эта была последняя
                if flag == 'last':
                    file.write("    Забрали с объекта все скважины, и эта оказаласть последняя, "
                               "    значит надо удалить посещение этого объекта в старом маршруте" + '\n')
                    XR, YR, SR, AR = DeleteClientaFromPath(XR, YR, SR, AR, client, clientCar)

                XR[sosed][client][sosedCar] = 1
                XR[client][sosed][sosedCar] = 1
                YR[sosed][sosedCar] = 1
                YR[client][sosedCar] = 1  # теперь машина соседа обслуживает клиента

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
                XR, YR, SR, AR, targetR, sizeK = Checker(XR, YR, SR, AR, iterations, "Help", file)
                file.write("OperatorJoinFromHelp stop: <-\n")
                return XR, YR, SR, AR, targetR, sizeK
            except TypeError:
                file.write("OperatorJoinFromHelp stop: <-\n")
                return x, y, s, a, target_function_start

        # Выбор минимума
        if sosedLeft != -1 or sosedRight != -1:
            file.write("    Теперь ищем минимум из двух целевых" + '\n')
            minimum = min(targetL, targetR)
            if minimum == targetL and minimum != -1:
                file.write("    Выбрали левого у него целевая меньше" + '\n')
                file.write("OperatorJoinFromHelp stop: <-\n")
                # sequenceX2 = GettingTheSequence(Xl)
                # sequenceX1 = TransferX2toX1(sequenceX2, Xl)
                # print("sequenceX1 in Reloc left= ", sequenceX1)
                return Xl, Yl, Sl, Al, targetL

            elif minimum == targetR and minimum != -1:  #######and targetR != targetL:
                file.write("    Выбрали правого у него целевая меньше" + '\n')
                file.write("OperatorJoinFromHelp stop: <-\n")
                # sequenceX2 = GettingTheSequence(XR)
                # sequenceX1 = TransferX2toX1(sequenceX2, XR)
                # print("sequenceX1 in Reloc right= ", sequenceX1)
                return XR, YR, SR, AR, targetR

            else:
                file.write("    Все пошло по пизде ничего не сохранили" + '\n')
                file.write("OperatorJoinFromHelp stop: <-\n")
                return x, y, s, a, target_function_start

    file.write("    В этом маршруте есть такой объект, вернемся к нему позже\n")
    file.write("OperatorJoinFromHelp stop: <-\n")
    return x, y, s, a, target_function_start


# Возможность приезжать нескольким машинам на одну локацию
def Help(Xstart, Ystart, Sstart, Astart, target_function_start, iterations):
    file = open("log/helog.txt", 'a')
    file.write("Help START: ->" + '\n')
    print("Help START: ->")
    print("\n")

    SaveStartHelp(Xstart, Ystart, Sstart, Astart)
    file.write("Целевая функция до применения оператора хелп = " + str(target_function_start) + "\n")

    file.write("Начинаем поиск объектов, которые в маршруте не успевают закончить работу\n")
    file_flag = 0
    sequenceX1 = []
    for k in range(K):
        for client in range(1, N):
            if Ystart[client][k] == 1:
                if Astart[client][k] + Sstart[client][k] > l[client]:
                    file.write("Нашли объект который опаздывает " + str(client) + " который обслуживает машина "
                               + str(k) + '\n')
                    contskvaj = CountskvajWithFane(Sstart, Astart, client, k)
                    file.write("Всего не укладывается " + str(contskvaj) + " скважин\n")

                    howMuch = 0
                    for proebSkv in range(1, contskvaj + 1):
                        X, Y, Ss, A = ReadStartHelpOfFile()
                        TargetFunction = target_function_start

                        flag = 0
                        if proebSkv < int(Ss[client][k] / S[client] / skvaj[client]):######## #skvaj[client]:
                            flag = 'not the last'
                        elif proebSkv == int(Ss[client][k] / S[client] / skvaj[client]):####skvaj[client]:
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
                                    for sosed in range(N):
                                        if (Y[sosed][sosedK] == 1 and sosed != 0) or (sosed == 0 and not CarIsWork(Y, sosedK)):
                                            file.write("Рассматриваемый объект " + str(sosed) + "\n")
                                            file.write(
                                                "Попробую одну скважину с объекта " + str(client) + " и машины " + str(
                                                    k) + "\n")
                                            file.write(" отдать машине " + str(sosedK) + " рядом с объектом " + str(
                                                sosed) + "\n")

                                            timeWork = S[client] / skvaj[client]
                                            x, y, s, a, target_function = OperatorJoinFromHelp(X, Y, Ss, A, client, k,
                                                                                               sosed, sosedK, timeWork,
                                                                                               TargetFunction,
                                                                                               iterations, flag,
                                                                                               file)
                                            file.write(
                                                "Число используемых машин теперь " + str(AmountCarUsed(y)) + '\n')

                                            file.write(
                                                "Выбираем минимальное решение из стартового и измененного" + '\n')
                                            file.write("Последняя целевая функция = " + str(TargetFunction) + '\n')
                                            minimum1 = min(TargetFunction, target_function)
                                            if minimum1 == target_function:
                                                file.write(
                                                    "Новое перемещение, лучше чем то что было, сохраняем это решение" + '\n')
                                                file.write("Новая целевая функция равна " + str(target_function) + '\n')

                                                SaveHelp(x, y, s, a)
                                                TargetFunction = target_function
                                                file_flag = 1

                                                sequence2 = GettingTheSequence(X)
                                                sequence1 = TransferX2toX1(sequence2, X)
                                                file.write("Новое решение " + str(sequence1) + '\n')
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
                                target_function = CalculationOfObjectiveFunction(x, shtrafFunction(s, a, iterations))
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
                                sequenceX2 = GettingTheSequence(x)
                                sequenceX1 = TransferX2toX1(sequenceX2, x)
                                # print("sequenceX1 help 1= ", sequenceX1)

                            else:
                                file.write("Новое перемещение, хуже чем последние добавленое стартовое решение" + '\n')
                                file.write("Старая целевая функция равна " + str(target_function_start) + '\n')
                                # return Xstart, Ystart, Sstart, Astart, target_function_start
                                howMuch = 'all'
                                break

                    if howMuch == 'all':
                        file.write("\nПопробуем отдать несколько скважин\n")

                        file.write("Пересчитываем проебанные скважины\n")
                        contskvaj = CountskvajWithFane(Sstart, Astart, client, k)
                        file.write("Всего не укладывается " + str(contskvaj) + " скважин\n")

                        for proebSkv in range(2, contskvaj + 1):
                            file.write("Отдаем " + str(proebSkv) + " скважин\n")
                            X, Y, Ss, A = ReadStartHelpOfFile()
                            TargetFunction = target_function_start

                            flag = 0
                            if proebSkv < int(Ss[client][k] / S[client] / skvaj[client]):   #####skvaj[client]:
                                flag = 'not the last'
                            elif proebSkv == int(Ss[client][k] / S[client] / skvaj[client]): ####skvaj[client]:
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
                                            if (Y[sosed][sosedK] == 1 and sosed != 0) or (sosed == 0 and not CarIsWork(Y, sosedK)):
                                                file.write("Рассматриваемый объект " + str(sosed) + "\n")
                                                file.write(
                                                    "Попробую одну скважину с объекта " + str(
                                                        client) + " и машины " + str(
                                                        k) + "\n")
                                                file.write(" отдать машине " + str(
                                                    sosedK) + " рядом с объектом " + str(
                                                    sosed) + "\n")

                                                timeWork = proebSkv * (S[client] / skvaj[client])
                                                x, y, s, a, target_function = OperatorJoinFromHelp(X, Y, Ss, A,
                                                                                                   client, k,
                                                                                                   sosed,
                                                                                                   sosedK,
                                                                                                   timeWork,
                                                                                                   TargetFunction,
                                                                                                   iterations,
                                                                                                   flag,
                                                                                                   file)
                                                file.write(
                                                    "Число используемых машин теперь " + str(
                                                        AmountCarUsed(y)) + '\n')

                                                file.write(
                                                    "Выбираем минимальное решение из стартового и измененного" + '\n')
                                                file.write(
                                                    "Последняя целевая функция = " + str(TargetFunction) + '\n')
                                                minimum1 = min(TargetFunction, target_function)
                                                if minimum1 == target_function:
                                                    file.write(
                                                        "Новое перемещение, лучше чем то что было, сохраняем это решение" + '\n')
                                                    file.write(
                                                        "Новая целевая функция равна " + str(
                                                            target_function) + '\n')

                                                    SaveHelp(x, y, s, a)
                                                    TargetFunction = target_function
                                                    fileflag = 1
                                                    sequence2 = GettingTheSequence(x)
                                                    sequence1 = TransferX2toX1(sequence2, x)
                                                    file.write("Новое решение " + str(sequence1) + '\n')
                                                else:
                                                    file.write(
                                                        "Новое перемещение, хуже чем то что было, возвращаем наше "
                                                        "старое решение" + '\n')
                                                    file.write(
                                                        "Старая целевая функция равна " + str(
                                                            TargetFunction) + '\n')
                                                file.write('\n')

                        file.write(
                            "Целевая функция последнего стартового решения = " + str(target_function_start) + '\n')

                        if fileflag == 1:
                            x, y, s, a = ReadHelpOfFile()
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

                            SaveStartHelp(x, y, s, a)
                            target_function_start = target_function
                            sequenceX2 = GettingTheSequence(x)
                            sequenceX1 = TransferX2toX1(sequenceX2, x)
                            # print("sequenceX1 help 1= ", sequenceX1)
                        else:
                            file.write("Новое перемещение, хуже чем последние добавленое стартовое решение" + '\n')
                            file.write("Старая целевая функция равна " + str(target_function_start) + '\n')

    file.write("По максимуму постарались поделиться скважинами" + '\n')
    Xstart, Ystart, Sstart, Astart = ReadStartHelpOfFile()
    sequenceX2 = GettingTheSequence(Xstart)
    sequenceX1 = TransferX2toX1(sequenceX2, Xstart)
    # print("sequenceX1 help 2= ", sequenceX1)

    # Xstart, Ystart, Sstart, Astart = ReadStartHelpOfFile()
    file.write("<-Help STOP" + '\n')
    print("<-Help STOP")
    print("\n")
    file.close()

    return Xstart, Ystart, Sstart, Astart, target_function_start, sequenceX1


def Exchange(x_start, y_start, s_start, a_start, target_function_start, iteration): #timeLocal):
    file = open("log/exchlog.txt", 'a')

    # start = time.time()
    # timeLocal[1] += 1

    file.write("->Exchange start" + '\n')
    file.write("Целевая функция до применения Exchange = " + str(target_function_start) + '\n')

    SaveStartLocalSearch(x_start, y_start, s_start, a_start)
    TargetFunction = target_function_start
    buf_targ = 0
    sequenceX1 = []
    fileflag = 0
    buf_targ = TargetFunction
    X, Y, Ss, A = ReadStartLocalSearchOfFile()
    sequenceX2 = GettingTheSequence(X)

    # Bыбираем клиента
    for clientCar in range(K):
        for client in range(1, N):
            if Y[client][clientCar] == 1:
                for sosedCar in range(K):
                    for sosed in range(1, N):
                        # TODO случай с равными машинами
                        if Y[sosed][sosedCar] == 1 and sosedCar != clientCar:

                            subseq1 = []
                            subseq2 = []

                            indexCl = sequenceX2[clientCar].index(client)
                            indexSos = sequenceX2[sosedCar].index(sosed)

                            for i in range(indexCl, len(sequenceX2[clientCar])):
                                if i <= indexCl + param_len_subseq and sequenceX2[clientCar][i] != 0:
                                    subseq1.append(sequenceX2[clientCar][i])
                                else:
                                    break
                            for i in range(indexSos, len(sequenceX2[sosedCar])):
                                if i <= indexSos + param_len_subseq and sequenceX2[sosedCar][i] != 0:
                                    subseq2.append(sequenceX2[sosedCar][i])
                                else:
                                    break

                            if subseq1 != [] and subseq2 != []:
                                file.write("Переставляем клиентa " + str(client) + '\n')
                                file.write("С машины " + str(clientCar) + '\n')

                                file.write("К соседу " + str(sosed) + '\n')
                                file.write("На машине " + str(sosedCar) + '\n')

                                file.write("Собираем подпоследовательности\n")
                                file.write("path1 = " + str(sequenceX2[clientCar]) + '\n')
                                file.write("path2 = " + str(sequenceX2[sosedCar]) + '\n')

                                file.write("subseq1 = " + str(subseq1) + '\n')
                                file.write("subseq2 = " + str(subseq2) + '\n')

                                if indexCl - 1 == 0:
                                    sequence1Left = 0
                                else:
                                    sequence1Left = sequenceX2[clientCar][indexCl - 2]
                                if indexCl + param_len_subseq + 2 < len(sequenceX2):
                                    sequence1Right = sequenceX2[clientCar][indexCl + param_len_subseq + 2]
                                else:
                                    sequence1Right = 0

                                if indexSos - 1 == 0:
                                    sequence2Left = 0
                                else:
                                    sequence2Left = sequenceX2[sosedCar][indexSos - 2]
                                if indexSos + param_len_subseq + 2 < len(sequenceX2):
                                    sequence2Right = sequenceX2[sosedCar][indexSos + param_len_subseq + 2]
                                else:
                                    sequence2Right = 0

                                # file.write("Пред Слева от последовательности клиента " + str(sequence1Left) + "\n")
                                # file.write(
                                #     "После Справа от последовательности клиента " + str(sequence1Right) + "\n")
                                # file.write("Перд Слева от последовательности соседа " + str(sequence2Left) + "\n")
                                # file.write(
                                #     "После Справа от последовательности соседа " + str(sequence2Right) + "\n")

                                buf1 = []
                                # Отсекаем мусорные решения, если первые элементы подпоследовательностей
                                # не содержатся ни в начале ни в конце
                                if not IsContainskvaj(sequenceX2[sosedCar], subseq1[0], file, sequence2Left) \
                                        and not IsContainskvaj(sequenceX2[sosedCar], subseq1[0], file,
                                                               sequence2Right,
                                                               'end') \
                                        and not IsContainskvaj(sequenceX2[clientCar], subseq2[0], file,
                                                               sequence1Left) \
                                        and not IsContainskvaj(sequenceX2[clientCar], subseq2[0], file,
                                                               sequence1Right,
                                                               'end'):
                                    file.write("Первые элементы подпоследовательностей "
                                               "не содержатся ни в начале ни в конце\n")

                                    for i in range(len(subseq1)):
                                        if subseq1[-1] != 0:
                                            buf1.append(subseq1[i])
                                            buf2 = []
                                            for j in range(len(subseq2)):
                                                if subseq2[-1] != 0:
                                                    buf2.append(subseq2[j])
                                                    if ResultCoins(coins_Exch):
                                                        file.write("buf1 = " + str(buf1) + '\n')
                                                        for p in range(len(buf1)):
                                                            file.write(str(Ss[buf1[p]][clientCar]) + ' ')
                                                        file.write('\n')

                                                        file.write("buf2 = " + str(buf2) + '\n')
                                                        for p in range(len(buf2)):
                                                            file.write(str(Ss[buf2[p]][sosedCar]) + ' ')
                                                        file.write('\n')

                                                        x, y, s, a, target_function = OperatorJoinFromExchange(
                                                            X, Y, Ss, A, TargetFunction, client,
                                                            clientCar, buf1, sosed, sosedCar, buf2, iteration, file)
                                                        file.write(
                                                            "Число используемых машин " + str(
                                                                AmountCarUsed(y)) + '\n')

                                                        file.write("Выбираем минимальное решение" + '\n')
                                                        minimum = min(TargetFunction, target_function)
                                                        if minimum == target_function:
                                                            file.write(
                                                                "Новое перемещение, лучше чем то что было, сохраняем это решение" + '\n')
                                                            file.write(
                                                                "Новая целевая функция равна " + str(
                                                                    target_function) + '\n')

                                                            SaveLocalSearch(x, y, s, a)
                                                            TargetFunction = target_function
                                                            fileflag = 1
                                                        else:
                                                            file.write(
                                                                "Новое перемещение, хуже чем то что было, "
                                                                "возвращаем наше старое решение" + '\n')
                                                            file.write(
                                                                "Старая целевая функция равна " + str(
                                                                    TargetFunction) + '\n')
                                                    else:
                                                        file.write("Монетка сказала, не берем\n")
                                                        file.write("buf1 = " + str(buf1) + '\n')
                                                        file.write("buf2 = " + str(buf2) + '\n\n')
                                else:
                                    file.write("Отбросили мусорные решения\n")

        file.write(
            "Целевая функция последнего стартового решения = " + str(target_function_start) + '\n')

        # if fileflag == 1:
        #     x, y, s, a = ReadLocalSearchOfFile()
        #     target_function = CalculationOfObjectiveFunction(x, shtrafFunction(s, a, iteration))
        #     file.write(
        #         "Целевая функция последнего минимального переставления = " + str(
        #             target_function) + '\n')
        #     fileflag = 0
        # else:
        #     target_function = -1
        # # TODO сравнивать по вероятностb
        # minimum2 = min(target_function_start, target_function)
        # if (minimum2 == target_function and target_function != -1) or (fileflag == 1 ):
        #     file.write("Новое перемещение, лучше чем стартовое, сохраняем это решение" + '\n')
        #     file.write("Новая целевая функция равна " + str(target_function) + '\n')
        #
        #     SaveStartLocalSearch(x, y, s, a)
        #     target_function_start = target_function
        #     TargetFunction = target_function
        # else:
        #     file.write("Новое перемещение, хуже чем последние добавленое стартовое решение" + '\n')
        #     file.write("Старая целевая функция равна " + str(target_function_start) + '\n')

    file.write("While stop\n")
    if fileflag == 1:
        x_start, y_start, s_start, a_start = ReadLocalSearchOfFile()
        target_function = CalculationOfObjectiveFunction(x_start, shtrafFunction(s_start, a_start, iteration))
        file.write(
                "Целевая функция последнего минимального переставления = " + str(
                    target_function) + '\n')
        sequenceX2 = GettingTheSequence(x_start)
        sequenceX1 = TransferX2toX1(sequenceX2, x_start)
        # print("sequenceX1 1= ", sequenceX1)
    else:
        x_start, y_start, s_start, a_start = ReadStartLocalSearchOfFile()
        target_function = CalculationOfObjectiveFunction(x_start, shtrafFunction(s_start, a_start, iteration))
        file.write(
            "Целевая функция последнего минимального переставления = " + str(
                target_function) + '\n')
        sequenceX2 = GettingTheSequence(x_start)
        sequenceX1 = TransferX2toX1(sequenceX2, x_start)
        # print("sequenceX1 1= ", sequenceX1)

    # Time = time.time() - start
    # timeLocal[0] += Time
    # file.write("Время работы Exchange = " + str(Time) + 'seconds\n')

    file.write("<-Exchange stop" + '\n')
    file.close()

    return x_start, y_start, s_start, a_start, target_function_start, sequenceX1 #timeLocal


def OperatorJoinFromExchange(x, y, s, a, target_function, client, clientCar, subseq1,
                             sosed, sosedCar, subseq2, iteration, file):
    file.write("->OperatorJoinFromExchange start" + '\n')

    TargetFunction = target_function
    X, Y, Ss, A = ReadStartLocalSearchOfFile()

    subseq1Left = SearchSosedLeftOrRight(X, Y, subseq1[0], "left", clientCar)  # левый сосед клиента
    subseq1Right = SearchSosedLeftOrRight(X, Y, subseq1[-1], "right", clientCar)  # левый сосед клиента
    subseq2Left = SearchSosedLeftOrRight(X, Y, subseq2[0], "left", sosedCar)  # правый сосед соседа
    subseq2Right = SearchSosedLeftOrRight(X, Y, subseq2[-1], "right", sosedCar)  # правый сосед соседа

    # file.write("    Слева от последовательности клиента " + str(subseq1Left) + " Время работы = " + str(Ss[subseq1Left][clientCar]) + "\n")
    # file.write("    Справа от последовательности клиента " + str(subseq1Right) + " Время работы = " + str(Ss[subseq1Right][clientCar]) + "\n")
    # file.write("    Слева от последовательности соседа " + str(subseq2Left) + " Время работы = " + str(Ss[subseq2Left][sosedCar]) + "\n")
    # file.write("    Справа от последовательности соседа " + str(subseq2Right) + " Время работы = " + str(Ss[subseq2Right][sosedCar]) + "\n")

    time1 = SaveTime(Ss, subseq1, clientCar, file)
    time2 = SaveTime(Ss, subseq2, sosedCar, file)

    X, Y, Ss, A = DeleteTail(X, Y, Ss, A, subseq1Left, subseq1, clientCar, file, subseq1Right)
    X, Y, Ss, A = DeleteTail(X, Y, Ss, A, subseq2Left, subseq2, sosedCar, file, subseq2Right)

    # Сценарий когда какие-нибудь края равны соседям другой последовательности
    if subseq1[0] == subseq2Left or subseq1[-1] == subseq2Right or \
            subseq2[0] == subseq1Left or subseq2[-1] == subseq1Right:
        file.write("    Сценарий когда какие-нибудь края равны соседям другой последовательности\n")

        if subseq1[0] == subseq2Left and subseq1[-1] != subseq2Right and \
                subseq2[0] != subseq1Left and subseq2[-1] != subseq1Right:
            file.write("    subseq1[0] == subseq2Left остальные не равны\n")

            Ss[subseq1[0]][sosedCar] += time1[0]
            X, Y, Ss, subseq2Left = AddSubSeqInPath(X, Y, Ss, subseq1, subseq2Left, sosedCar, time1, 1)
            X[subseq2Left][subseq2Right][sosedCar] = 1

            X, Y, Ss, subseq1Left = AddSubSeqInPath(X, Y, Ss, subseq2, subseq1Left, clientCar, time2, 0)
            X[subseq1Left][subseq1Right][clientCar] = 1

            A = TimeOfArrival(X, Y, Ss, file)

        elif subseq1[0] != subseq2Left and subseq1[-1] == subseq2Right and \
                subseq2[0] != subseq1Left and subseq2[-1] != subseq1Right:
            file.write("    subseq1[-1] == subseq2Right остальные не равны\n")

            X, Y, Ss, subseq2Left = AddSubSeqInPath(X, Y, Ss, subseq1, subseq2Left, sosedCar, time1, 0)
            # Ss[subseq2Right][sosedCar] += time1[-1]

            X, Y, Ss, subseq1Left = AddSubSeqInPath(X, Y, Ss, subseq2, subseq1Left, clientCar, time2, 0)
            X[subseq1Left][subseq1Right][clientCar] = 1

            A = TimeOfArrival(X, Y, Ss, file)

        elif subseq1[0] == subseq2Left and subseq1[-1] == subseq2Right and \
                subseq2[0] != subseq1Left and subseq2[-1] != subseq1Right:
            file.write("    subseq1[0] == subseq2Left and subseq1[-1] == subseq2Right остальные не равны\n")

            Ss[subseq1[0]][sosedCar] += time1[0]
            X, Y, Ss, subseq2Left = AddSubSeqInPath(X, Y, Ss, subseq1, subseq2Left, sosedCar, time1, 1)
            # Ss[subseq1[-1]][sosedCar] += time1[-1]

            X, Y, Ss, subseq1Left = AddSubSeqInPath(X, Y, Ss, subseq2, subseq1Left, clientCar, time2, 0)
            X[subseq1Left][subseq1Right][clientCar] = 1

            A = TimeOfArrival(X, Y, Ss, file)

        elif subseq1[0] == subseq2Left and subseq1[-1] != subseq2Right and \
                subseq2[0] == subseq1Left and subseq2[-1] == subseq1Right:
            file.write("    Только эти не равен subseq1[-1] != subseq2Right\n")

            Ss[subseq1[0]][sosedCar] += time1[0]
            X, Y, Ss, subseq2Left = AddSubSeqInPath(X, Y, Ss, subseq1, subseq2Left, sosedCar, time1, 1)
            X[subseq2Left][subseq2Right][sosedCar] = 1

            Ss[subseq2[0]][clientCar] += time2[0]
            X, Y, Ss, subseq1Left = AddSubSeqInPath(X, Y, Ss, subseq2, subseq1Left, clientCar, time2, 1)
            # Ss[subseq2[-1]][clientCar] += time2[-1]

            A = TimeOfArrival(X, Y, Ss, file)

        elif subseq1[0] != subseq2Left and subseq1[-1] == subseq2Right and \
                subseq2[0] == subseq1Left and subseq2[-1] == subseq1Right:
            file.write("    Только эти не равен subseq1[0] != subseq2Left\n")

            X, Y, Ss, subseq2Left = AddSubSeqInPath(X, Y, Ss, subseq1, subseq2Left, sosedCar, time1, 0)
            # Ss[subseq1[-1]][sosedCar] += time1[-1]

            Ss[subseq2[0]][clientCar] += time2[0]
            X, Y, Ss, subseq1Left = AddSubSeqInPath(X, Y, Ss, subseq2, subseq1Left, clientCar, time2, 1)
            # Ss[subseq2[-1]][clientCar] += time2[-1]

            A = TimeOfArrival(X, Y, Ss, file)

        elif subseq1[0] == subseq2Left and subseq1[-1] == subseq2Right and \
                subseq2[0] == subseq1Left and subseq2[-1] == subseq1Right:
            file.write("    Все равны\n")

            Ss[subseq1[0]][sosedCar] += time1[0]
            X, Y, Ss, subseq2Left = AddSubSeqInPath(X, Y, Ss, subseq1, subseq2Left, sosedCar, time1, 1)
            # Ss[subseq1[-1]][sosedCar] += time1[-1]

            Ss[subseq2[0]][clientCar] += time2[0]
            X, Y, Ss, subseq1Left = AddSubSeqInPath(X, Y, Ss, subseq2, subseq1Left, clientCar, time2, 1)
            # Ss[subseq2[-1]][clientCar] += time2[-1]

            A = TimeOfArrival(X, Y, Ss, file)

        elif subseq1[0] == subseq2Left and subseq1[-1] != subseq2Right and \
                subseq2[0] != subseq1Left and subseq2[-1] == subseq1Right:
            file.write("    subseq1[0] == subseq2Left and subseq2[-1] == subseq1Right остальные не равны\n")

            Ss[subseq1[0]][sosedCar] += time1[0]
            X, Y, Ss, subseq2Left = AddSubSeqInPath(X, Y, Ss, subseq1, subseq2Left, sosedCar, time1, 1)
            X[subseq2Left][subseq2Right][sosedCar] = 1

            X, Y, Ss, subseq1Left = AddSubSeqInPath(X, Y, Ss, subseq2, subseq1Left, clientCar, time2, 0)
            # Ss[subseq2[-1]][clientCar] += time2[-1]

            A = TimeOfArrival(X, Y, Ss, file)

        elif subseq1[0] != subseq2Left and subseq1[-1] == subseq2Right and \
                subseq2[0] != subseq1Left and subseq2[-1] == subseq1Right:
            file.write("    subseq1[-1] == subseq2Right and subseq2[-1] == subseq1Right остальные не равны\n")

            X, Y, Ss, subseq2Left = AddSubSeqInPath(X, Y, Ss, subseq1, subseq2Left, sosedCar, time1, 0)
            # Ss[subseq1[-1]][sosedCar] += time1[-1]

            X, Y, Ss, subseq1Left = AddSubSeqInPath(X, Y, Ss, subseq2, subseq1Left, clientCar, time2, 0)
            # Ss[subseq2[-1]][clientCar] += time2[-1]

            A = TimeOfArrival(X, Y, Ss, file)

        elif subseq1[0] == subseq2Left and subseq1[-1] == subseq2Right and \
                subseq2[0] != subseq1Left and subseq2[-1] == subseq1Right:
            file.write("    Только эти не равны subseq2[0] != subseq1Left\n")

            Ss[subseq1[0]][sosedCar] += time1[0]
            X, Y, Ss, subseq2Left = AddSubSeqInPath(X, Y, Ss, subseq1, subseq2Left, sosedCar, time1, 1)
            # Ss[subseq1[-1]][sosedCar] += time1[-1]

            X, Y, Ss, subseq1Left = AddSubSeqInPath(X, Y, Ss, subseq2, subseq1Left, clientCar, time2, 0)
            # Ss[subseq2[-1]][clientCar] += time2[-1]

            A = TimeOfArrival(X, Y, Ss, file)

        elif subseq1[0] == subseq2Left and subseq1[-1] != subseq2Right and \
                subseq2[0] == subseq1Left and subseq2[-1] != subseq1Right:
            file.write("    subseq1[0] == subseq2Left and subseq2[0] == subseq1Left остальные не равны\n")

            Ss[subseq1[0]][sosedCar] += time1[0]
            X, Y, Ss, subseq2Left = AddSubSeqInPath(X, Y, Ss, subseq1, subseq2Left, sosedCar, time1, 1)
            X[subseq2Left][subseq2Right][sosedCar] = 1

            Ss[subseq2[0]][clientCar] += time2[0]
            X, Y, Ss, subseq1Left = AddSubSeqInPath(X, Y, Ss, subseq2, subseq1Left, clientCar, time2, 1)
            X[subseq1Left][subseq1Right][clientCar] = 1

            A = TimeOfArrival(X, Y, Ss, file)

        elif subseq1[0] != subseq2Left and subseq1[-1] == subseq2Right and \
                subseq2[0] == subseq1Left and subseq2[-1] != subseq1Right:
            file.write("    subseq2[0] == subseq1Left and subseq1[-1] == subseq2Right остальные не равны\n")

            X, Y, Ss, subseq2Left = AddSubSeqInPath(X, Y, Ss, subseq1, subseq2Left, sosedCar, time1, 0)
            # Ss[subseq1[-1]][sosedCar] += time1[-1]

            Ss[subseq2[0]][clientCar] += time2[0]
            X, Y, Ss, subseq1Left = AddSubSeqInPath(X, Y, Ss, subseq2, subseq1Left, clientCar, time2, 1)
            X[subseq1Left][subseq1Right][clientCar] = 1

            A = TimeOfArrival(X, Y, Ss, file)

        elif subseq1[0] == subseq2Left and subseq1[-1] == subseq2Right and \
                subseq2[0] == subseq1Left and subseq2[-1] != subseq1Right:
            file.write("    Только этот не равен subseq2[-1] != subseq1Right\n")

            Ss[subseq1[0]][sosedCar] += time1[0]
            X, Y, Ss, subseq2Left = AddSubSeqInPath(X, Y, Ss, subseq1, subseq2Left, sosedCar, time1, 1)
            # Ss[subseq1[-1]][sosedCar] += time1[-1]

            Ss[subseq2[0]][clientCar] += time2[0]
            X, Y, Ss, subseq1Left = AddSubSeqInPath(X, Y, Ss, subseq2, subseq1Left, clientCar, time2, 1)
            X[subseq1Left][subseq1Right][clientCar] = 1

            A = TimeOfArrival(X, Y, Ss, file)

        elif subseq1[0] != subseq2Left and subseq1[-1] != subseq2Right and \
                subseq2[0] == subseq1Left and subseq2[-1] == subseq1Right:
            file.write("    subseq2[0] == subseq1Left and subseq2[-1] == subseq1Right\n")

            X, Y, Ss, subseq2Left = AddSubSeqInPath(X, Y, Ss, subseq1, subseq2Left, sosedCar, time1, 0)
            X[subseq2Left][subseq2Right][sosedCar] = 1

            Ss[subseq2[0]][clientCar] += time2[0]
            X, Y, Ss, subseq1Left = AddSubSeqInPath(X, Y, Ss, subseq2, subseq1Left, clientCar, time2, 1)
            # Ss[subseq2[-1]][clientCar] += time2[-1]

            A = TimeOfArrival(X, Y, Ss, file)

        elif subseq1[0] != subseq2Left and subseq1[-1] != subseq2Right and \
                subseq2[0] == subseq1Left and subseq2[-1] != subseq1Right:
            file.write("    Только это равно subseq2[0] == subseq1Left\n")

            X, Y, Ss, subseq2Left = AddSubSeqInPath(X, Y, Ss, subseq1, subseq2Left, sosedCar, time1, 0)
            X[subseq2Left][subseq2Right][sosedCar] = 1

            Ss[subseq2[0]][clientCar] += time2[0]
            X, Y, Ss, subseq1Left = AddSubSeqInPath(X, Y, Ss, subseq2, subseq1Left, clientCar, time2, 1)
            X[subseq1Left][subseq1Right][clientCar] = 1

            A = TimeOfArrival(X, Y, Ss, file)

        elif subseq1[0] != subseq2Left and subseq1[-1] != subseq2Right and \
                subseq2[0] != subseq1Left and subseq2[-1] == subseq1Right:
            file.write("    Только этот равен subseq2[-1] == subseq1Right\n")

            X, Y, Ss, subseq2Left = AddSubSeqInPath(X, Y, Ss, subseq1, subseq2Left, sosedCar, time1, 0)
            X[subseq2Left][subseq2Right][sosedCar] = 1

            X, Y, Ss, subseq1Left = AddSubSeqInPath(X, Y, Ss, subseq2, subseq1Left, clientCar, time2, 0)
            # Ss[subseq2[-1]][clientCar] += time2[-1]

            A = TimeOfArrival(X, Y, Ss, file)

        try:
            X, Y, Ss, A, Target_Function = Checker(X, Y, Ss, A, iteration, "Exchange", file)
            PrintForCar(X, Ss, clientCar, file, sosedCar)
            file.write("OperatorJoinFromExchange stop: <-\n")
            return X, Y, Ss, A, Target_Function
        except TypeError:
            # for i in range(N):
            #     file.write("Scl = " + str(Ss[i][clientCar]) + ' ')
            # file.write('\n')
            #
            # for i in range(N):
            #     file.write("Ssos = " + str(Ss[i][sosedCar]) + ' ')
            # file.write('\n')

            file.write("OperatorJoinFromExchange stop: <-\n")
            return x, y, s, a, target_function

    else:
        file.write("    Сценарий когда никакие края не равны с соседями из другой последовательности\n")

        X, Y, Ss, subseq2Left = AddSubSeqInPath(X, Y, Ss, subseq1, subseq2Left, sosedCar, time1, 0)
        X[subseq2Left][subseq2Right][sosedCar] = 1

        X, Y, Ss, subseq1Left = AddSubSeqInPath(X, Y, Ss, subseq2, subseq1Left, clientCar, time2, 0)
        X[subseq1Left][subseq1Right][clientCar] = 1

        A = TimeOfArrival(X, Y, Ss, file)

        try:
            X, Y, Ss, A, Target_Function = Checker(X, Y, Ss, A, iteration, "Exchange", file)
            PrintForCar(X, Ss, clientCar, file, sosedCar)
            file.write("OperatorJoinFromExchange stop: <-\n")
            return X, Y, Ss, A, Target_Function
        except TypeError:
            file.write("OperatorJoinFromExchange stop: <-\n")
            return x, y, s, a, target_function
    # TODO надо рассмотреть свап, когда одна машина


# Применяю операторы для решения: заполняю массив
def start_operator(local_x, local_y, local_s, local_a, iterations):
    # сначала для оператора перемещения:
    SaveSolution(local_x, local_y, local_s, local_a, 'StartSolution.txt', 'w')
    target_function = 9999999999

    for i in range(NumberStartOper):

        local_x, local_y, local_s, local_a = ReadSolutionOfFile('StartSolution.txt')
        sequenceX2 = GettingTheSequence(local_x)
        sequenceX1 = TransferX2toX1(sequenceX2, local_x)
        print("\n")
        print("\n")
        print("sequence перед применением операторов = ", sequenceX1)

        x_reloc, y_reloc, s_reloc, a_reloc, Target_function_reloc, SEQUENCE_reloc = Relocate(local_x, local_y, local_s, local_a,
                                                                                            target_function, iterations)
        print("Target_function_reloc = ", Target_function_reloc)
        sequenceRelocX2 = GettingTheSequence(x_reloc)
        sequenceRelocX1 = TransferX2toX1(sequenceRelocX2, x_reloc)

        minimum = min(Target_function_reloc, target_function)
        if minimum == Target_function_reloc:
            SaveSolution(x_reloc, y_reloc, s_reloc, a_reloc, 'ResultOperator.txt', 'w')
            target_function = Target_function_reloc
            local_SEQUENCE = SEQUENCE_reloc
            print("min_target this is Reloc = ", target_function)
            print("sequenceX1 Reloc= ", sequenceRelocX1)

        local_x, local_y, local_s, local_a = ReadSolutionOfFile('StartSolution.txt')
        sequenceX2 = GettingTheSequence(local_x)
        sequenceX1 = TransferX2toX1(sequenceX2, local_x)
        print("sequence перед применением Exchange = ", sequenceX1)
        x_exch, y_exch, s_exch, a_exch, Target_function_exch, SEQUENCE_exch = Exchange(local_x, local_y, local_s, local_a,
                                                                        target_function, iterations)
        print("target in Exchange = ", Target_function_exch)
        sequenceExchX2 = GettingTheSequence(x_exch)
        sequenceExchX1 = TransferX2toX1(sequenceExchX2, x_exch)
        print("sequence Exchange = ", sequenceExchX1)

        minimum = min(Target_function_exch, target_function)
        if minimum == Target_function_exch:
            if Target_function_reloc == Target_function_exch:
                print("Целевая reloc = целевой exch, значит берем решение из reloc")
                target_function = Target_function_reloc
                local_SEQUENCE = SEQUENCE_reloc
            else:
                print("Целевая exch < целевой reloca")
                SaveSolution(x_exch, y_exch, s_exch, a_exch, 'ResultOperator.txt', 'w')
                target_function = Target_function_exch
                local_SEQUENCE = SEQUENCE_exch
                print("min function this is Exchange = ", target_function)



        # x_opt, y_opt, s_opt, a_opt, Target_function_opt = Two_Opt(local_x, local_y, local_s,
        #                                                                      local_a, target_function,
        #                                                                      arr, iterations)
        # minimum = min(Target_function_opt, target_function)
        # if minimum == Target_function_opt:
        #     SaveSolution(local_x, local_y, local_s, local_a, 'ResultOperator.txt', 'w')
        #     target_function = Target_function_opt
        #     print("target in 2-opt = ", target_function)

        print("local_SEQUENCE in start operator = ", local_SEQUENCE)
        local_x, local_y, local_s, local_a = ReadSolutionOfFile("ResultOperator.txt")
        return target_function, local_x, local_y, local_s, local_a, local_SEQUENCE

    # x_reloc, y_reloc, s_reloc, a_reloc = ReadSolutionOfFile('ResultOperator.txt')
    #
    # # iterations += 1
    #

    # TODO  Раскоментить, когда появится 2-Opt
    # прочитали стартовое решение, чтобы все делать с 2-Opt:
    # local_x, local_y, local_s, local_a = ReadSolutionOfFile('StartSolution.txt')
    # TODO считаем локальный минимум для 2-Opt
    # minimum = min(Target_function_reloc, Target_function_TwoOpt)
    # if minimum == Target_function_reloc:
    #     return Target_function_reloc, x_reloc, y_reloc, s_reloc, a_reloc
    # elif minimum == Target_function_TwoOpt:
    #     return Target_function_TwoOpt, x_TwoOpt, y_TwoOpt, s_TwoOpt, a_TwoOpt
