import pyecm
from time import time
from random import randint
from sympy import legendre_symbol

start = time()

def find_powers_two(number):
    #Функция поиска степеней двойки, которые содержатся в числе
    if number % 2 == 1:
        return 0, number

    power = 0

    while number % 2 != 1:
        number //= 2
        power += 1

    return power, number 

def sqrt_mod(a, p):
    #Алгоритм вычисления квадратного корня по модулю (Алгоритм Тонелли-Шэнкса)
    #p - 1 = 2**S*Q; x**2 = a (mod p)
    if legendre_symbol(a, p) == -1:
        quit("Символ Лежандра равен -1!")

    if p <= 3:
        raise Exception("p должно быть > 3!") 

    S, Q = find_powers_two(p-1)

    #print(f"S = {S}, Q = {Q}")

    if S == 1 and p % 4 == 3:
        R = pow(a, (p+1)//4, p)

        return R%p, p-R

    if S >= 2:
        #Ищем произвольный квадратичный невычет
        z = 1
        while legendre_symbol(z,p) != -1:
            z += 1

        # print(f"z = {z}")
        c = pow(z, Q, p)
        # print(f"c = {c}")
        R = pow(a, (Q+1)//2, p)
        # print(f"R = {R}")
        t = pow(a, Q, p)
        # print(f"t = {t}")
        M = S
        # print(f"M = {M}\n")

        while True:
            # print(f"t= {t}")
            # a = input()
            if t == 1:
                return R, p-R
            
            if t == 0:
                return 0

            for i in range(1,M):
                tt = pow(t,2**i,p)
                # print(f"tt = {tt}")
                # a = input()
                if tt == 1:
                    # print(f"itter_____")
                    b = pow(c, 2**(M-i-1), p)
                    # print(f"b = {b}")
                    R = R*b % p
                    # print(f"R = {R}")
                    t = (t*((b**2) % p)) % p
                    # print(f"t = {t}")
                    c = b**2 % p
                    # print(f"c = {c}")
                    M = i
                    # print(f"M = {M}")
                    break

def generator1(dimensionPrimeNumber, startPrimeNumber):
    TMP = startPrimeNumber
    while len(str(TMP)) < dimensionPrimeNumber:
        N = 4 * TMP + 2
        U = 0
        while True:
            candidate = (N + U) * TMP + 1
            if pow(2, int(candidate - 1), int(candidate)) == 1 and pow(2, int(N + U), int(candidate)) != 1 and candidate % 8 == 5:
                TMP = candidate
                break
            else:
                U = U - 2
    return TMP

def generator2(dimensionPrimeNumber, startPrimeNumber):
    TMP = startPrimeNumber
    while len(str(TMP)) < dimensionPrimeNumber:
        N = 4 * TMP + 2
        U = 0
        while True:
            candidate = (N + U) * TMP + 1
            a = randint(2, 5)
            if pow(a, int(candidate - 1), int(candidate)) == 1 and pow(a, int(N + U), int(candidate)) != 1 and candidate % 48 == 41:
                TMP = candidate
                break
            else:
                U = U - 2
    return TMP

def find(y, d, N):
    d = bin(d)
    d = list(d[2:])
    x = y
    i = 1
    while i < len(d):
        if d[i] == '1':
            x = (x**2*y) % N
            i += 1
        else:
            x = pow(x, 2, N)
            i += 1
    return x

def funcA():
    x = []
    p = generator1(100, 17)
    print("\np = {}, длина = {}".format(p, len(str(p))))
    a = int(input('Введите а: '))
    a = a % p
    #print(find(a, (p-1)//4,p))
    if find(a, (p-1)//4,p) == 1:
        x1 = find(a, (p + 3)//8, p)
        x.append(x1 % p)
        print('x1: ', x1 % p)
        x2 = p - find(a, (p + 3)//8, p)
        x.append(x2 % p)
        print('x2: ', x2 % p)
    if find(a, (p-1)//4,p) == -1 % p:
        x3 = find(a, (p + 3)//8, p) * find(2, (p-1)//4, p)
        x.append(x3 % p)
        print('x3: ', x3 % p)
        x4 = p - find(a, (p + 3)//8, p) * find(2, (p-1)//4, p)
        x.append(x4 % p)
        print('x4: ', x4 % p)
    if find(a, (p-1)//4,p) != 1 and find(a, (p-1)//4,p) != -1 % p:
        print('Корней нет!')
    return x, p, a

def funcB():
    x = []
    p = generator2(100, 23)
    print("\np = {}, длина = {}".format(p, len(str(p))))
    a = int(input('Введите а: '))
    a = a % p
    if find(a, (p-1)//4, p) == 1: 
        if find(a, (p-1)//8, p) == 1:
            x1 = find(a, (p+7)//16, p)
            x.append(x1 % p)
            print('x1: ', x1 % p)
            x2 = p - find(a, (p+7)//16, p)
            x.append(x2 % p)
            print('x2: ', x2 % p)
        elif find(a, (p-1)//8, p) == -1 % p:
            x3 = find(a, (p+7)//16, p) * find(3, (p-1)//4, p)
            x.append(x3 % p)
            print('x3: ', x3 % p)
            x4 = p - find(a, (p+7)//16, p) * find(3, (p-1)//4, p)
            x.append(x4 % p)
            print('x4: ', x4% p)   
        else:
            print('Корней нет!')

    elif find(a, (p-1)//4, p) == -1 % p: 
        if (find(a, (p-1)//8, p)*find(3, (p-1)//4, p)) % p == 1:
            x5 = find(a, (p + 7)//16, p) * find(3, (p-1)//8, p)
            x.append(x5 % p)
            print('x5: ', x5 % p)
            x6 = p - find(a, (p + 7)//16, p) * find(3, (p-1)//8, p)
            x.append(x6 % p)
            print('x6: ', x6 % p)
        elif (find(a, (p-1)//4, p)*find(3, (p-1)//4, p)) % p == -1 % p:
            x7 = find(a, (p + 7)//16, p) * find(3, 3*(p-1)//8, p)
            x.append(x7 % p)
            print('x7: ', x7 % p)
            x8 = p - find(a, (p + 7)//16, p) * find(3, 3*(p-1)//8, p)
            x.append(x8 % p)
            print('x8: ', x8 % p)
        else:
            print('Корней нет!')
    else:
        print('Корней нет!')

    return x, p, a

n = int(input('Выберите 1) p = 5 (mod 8) или 2) p = 41 (mod 48): '))
if n == 1:
    x, p, a = funcA()
    x1, x2 = sqrt_mod(a, p)
    print('Посчитанные в общем случае: ', x1, x2)
if n == 2:
    x, p, a = funcB()
    x1, x2 = sqrt_mod(a, p)
    print('Посчитанные в общем случае: ', x1, x2)

j = 0
for i in range(len(x)):
    if find(x[i], 2, p) == a:
        j += 1
if j == len(x) and j != 0:
    print('Посчитано верно!')

print('Время выполнения: ', time() - start)
