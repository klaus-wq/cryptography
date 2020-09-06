from random import randint
from math import log, pi 
import time

start = time.time() #время начала работы программы
N = 10**100 #крайняя правая граница выбора двух чисел а и b
M = 10000 #кол-во испытаний

#функция для отыскания НОД(a,b) - алгоритм Евклида
def NOD(a, b):
    count = 0
    while a != 0 and b != 0:
        if a > b:
            a = a % b
            NOD1 = b
        else:
            b = b % a
            NOD1 = a
        count += 1
    if NOD1 == 1: #если НОД(a,b) = 1, то a и b - взаимнопростые, иначе - нет.
        return 1
    else:
        return 0

i = 0
itter = 0
while i < M:
    a = randint(1, N) #генерация случайного числа а
    b = randint(1, N) #генерация случайного числа b
    itter += NOD(a,b) #складываем кол-во итераций, когда НОД(a,b) = 1
    i += 1

print("Кол-во итераций, когда числа оказались взаимнопростыми: ", itter)
print("Вероятность, что числа взаимнопростые: ", itter/M)
print("Теоретическая оценка: ", 6/pi**2)

if (6/pi**2) > (itter/M):
    print("Теоретическая оценка выше экспериментальной.")
else:
    print("Экспериментальная оценка выше теоретической.")
print("Время выполнения: ", time.time() - start, "секунд.")
