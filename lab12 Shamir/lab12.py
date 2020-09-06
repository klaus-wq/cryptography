from random import randint
import pyecm
from sympy import factorint, isprime, gcd
from time import time

start = time()

def generator(dimensionPrimeNumber, startPrimeNumber):
    TMP = startPrimeNumber
    while len(str(TMP)) < dimensionPrimeNumber:
        N = 4 * TMP + 2
        U = 0
        while True:
            candidate = (N + U) * TMP + 1
            a = randint(2, 5)
            if pow(a, int(candidate - 1), int(candidate)) == 1 and pow(a, int(N + U), int(candidate)) != 1:
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

def find_p():
    a = 3
    q = generator(100, a)
    p = 2*q + 1
    while isprime(p) == False:
        a = a + 2
        while len(list(pyecm.factors(a, False, True, 8, 1))) != 1:
            a += 2
        #print('a', a)
        q = generator(100, a)
        #print('q', q)
        p = 2*q + 1
        #print('p', p)
    if len(list(pyecm.factors(p, False, True, 8, 1))) == 1:
        #print('len', len(list(pyecm.factors(p, False, True, 8, 1))))
        return p, q

def exgcd(a, b):
    x, xx, y, yy = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        x, xx = xx, x - xx*q
        y, yy = yy, y - yy*q
    return x 

p, q = find_p()
print("p = {}, длина = {}".format(p, len(str(p))))
print("q = {}, длина = {}".format(q, len(str(q))))

def find_cd(p, i):
    while i < p-1:
        if gcd(i,p-1) == 1:
            c = i
            break
        else:
            i += 2
    d = (exgcd(c, p-1)) % p-1
    return c, d

print('Эти числа Ca, Da, Cb, Db в секрете и не передаются.')
Ca, Da = find_cd(p, 10 ** 95 - 1)
print('Ca: ', Ca)
print('Da: ', Da)
Cb, Db = find_cd(p, 10 ** 94 - 1)
print('Cb: ', Cb)
print('Db: ', Db)

m = int(input('Введите передаваемое сообщение: '))
m = m % p
x1 = find(m, Ca, p)
print('x1: ', x1)
x2 = find(x1, Cb, p)
print('x2: ', x2)
x3 = find(x2, Da, p)
print('x3: ', x3)
x4 = find(x3, Db, p)
print('x4: ', x4)
if m == x4:
    print('Сообщение передано верно!')

print('Время выполнения: ', time() - start)

