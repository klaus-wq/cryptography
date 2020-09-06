from random import randint
import pyecm
from sympy import factorint, isprime, gcd, legendre_symbol, jacobi_symbol
from time import time
from math import sqrt, ceil

start = time()

def generator(dimensionPrimeNumber, startPrimeNumber):
    pq = []
    for i in range(2):
        TMP = startPrimeNumber
        while len(str(TMP)) < dimensionPrimeNumber:
            N = 4 * TMP + 2
            U = 0
            while True:
                candidate = (N + U) * TMP + 1
                a = randint(2, 5)
                if pow(a, int(candidate - 1), int(candidate)) == 1 and pow(a, int(N + U), int(candidate)) != 1 and candidate % 4 == 3:
                    TMP = candidate
                    break
                else:
                    U = U - 2
        pq.append(TMP)
        startPrimeNumber = startPrimeNumber + 2
        while len(list(pyecm.factors(startPrimeNumber, False, True, 8, 1))) != 1:
            startPrimeNumber = startPrimeNumber + 2
        TMP = startPrimeNumber
    p = pq[0]
    q = pq[1]
    print("\np = {}, длина = {}".format(p, len(str(p))))
    print("q = {}, длина = {}".format(q, len(str(q))))
    return p,q

def exgcd(a, b):
    x, xx, y, yy = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        x, xx = xx, x - xx*q
        y, yy = yy, y - yy*q
    return x

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

'''p = 7
print('p: ', p)
q = 11
print('q: ', q)'''
p, q = generator(10**2, 17)
n = p * q
print('Открытый ключ n: ', n)

s = 2
while jacobi_symbol(s, n) != -1:
    s += 1
print('Открытый ключ s: ', s)

k = exgcd(2, n)*(exgcd(4, n)*(p-1)*(q-1)+1) % n
print('Секретный ключ k: ', k)

M = int(input('Введите сообщение: '))
M = M % n
print('Сообщение для шифрования: ', M)

'''c1 = 0
j = jacobi_symbol(M, n)
while j != (-1)**c1:
    c1 += 1'''
jac_Mn = jacobi_symbol(M,n)
if jac_Mn == 1:
    c1 = 0
else:
    c1 = 1
print('c1: ', c1)

M_shtrih = find(s, c1, n)*M % n
print('M_shtrih: ', M_shtrih)
c2 = M_shtrih % 2
print('c2: ', c2)
c = find(M_shtrih, 2, n)
print('c: ', c)

#дешифрование
'''if c2 == 0:
    M_shtrih2 = find(c, k, n)
else:
    M_shtrih2 = find(-c, k, n)'''
M_shtrih2 = find(c, k, n)
print('M_shtrih2: ', M_shtrih2)

if c2 == 1 and M_shtrih2 % 2 == 0:
    M_shtrih2 = (-M_shtrih2) % n
if c2 == 0 and M_shtrih2 % 2 == 1:
    M_shtrih2 = (-M_shtrih2) % n
#M1 = (exgcd(s**c1, n)*M_shtrih2) % n
M1 = (pow(s, -c1, n)*M_shtrih2) % n
print('M1: ', M1)
#M2 = n - M1
#print('M2: ', M2)
if M1 == M:
    print('Расшифровано верно!')

print('Время выполнения: ', time() - start)
