from random import randint
import pyecm
from sympy import factorint, isprime
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

def find_g(p, q):
    g = 2
    while find(g, q, p) == 1:
        g += 1
    return g

p, q = find_p()
print("p = {}, длина = {}".format(p, len(str(p))))
print("q = {}, длина = {}".format(q, len(str(q))))
g = find_g(p, q)
print('g: ', g)

keyPrivateA = randint(1, 10**100)
print('Секретный ключ А: ', keyPrivateA)
keyPrivateB = randint(1, 10**100)
print('Секретный ключ B: ', keyPrivateB)
keyPublicA = find(g, keyPrivateA, p)
print('Открытый ключ A: ', keyPublicA)
keyPublicB = find(g, keyPrivateB, p)
print('Открытый ключ B: ', keyPublicB)

keyfullA = find(keyPublicB, keyPrivateA, p)
keyfullB = find(keyPublicA, keyPrivateB, p)

if keyfullA == keyfullB:
    print('Общий ключ сгенерирован верно!')

print("Общий ключ: {}, длина = {}".format(keyfullA, len(str(keyfullA))))
print('Время выполнения: ', time() - start)
