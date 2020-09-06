from random import randint
import pyecm
from sympy import factorint, isprime, gcd
from time import time

start = time()

def generate_p_q(prime_number, start_prime):
    tmp = start_prime
    pq = []
    for i in range(2):
        while len(str(tmp)) < prime_number:
            N = 4 * tmp + 2
            U = 0
            candidate = 0
            while True:
                candidate = (N + U) * tmp + 1
                if pow(2, int(candidate - 1), int(candidate)) == 1 and pow(2, int(N + U), int(candidate)) != 1 and candidate % 4 == 3:
                    tmp = candidate
                    break
                else:
                    U = U - 2
        pq.append(tmp)
        start_prime = start_prime + 2
        while len(list(pyecm.factors(start_prime, False, True, 8, 1))) != 1:
            start_prime = start_prime + 2
        tmp = start_prime
    p = pq[0]
    q = pq[1]
    return p,q

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

def exgcd(a, b):
    x, xx, y, yy = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        x, xx = xx, x - xx*q
        y, yy = yy, y - yy*q
    return x, y 

print('Закрытый ключ: ')
p, q = generate_p_q(200, 23)
print("p = {}, длина = {}".format(p, len(str(p))))
print("q = {}, длина = {}".format(q, len(str(q))))
print('Открытый ключ: ')
n = p * q
print("n = {}, длина = {}".format(n, len(str(n))))

m = int(input('Введите передаваемое сообщение: '))
m = m % n

c = find(m, 2, n)
print('Зашифрованный текст c: ', c)

#коэфф Безу
Yq, Yp = exgcd(q, p)
print('Yp: ', Yp)
print('Yq: ', Yq)

#кв корень из с по модулю
Mp = find(c, (p+1)//4, p)
print('Mp: ', Mp)
Mq = find(c, (q+1)//4, q)
print('Mq: ', Mq)

r = []
r1 = (Yp * p * Mq + Yq * q * Mp) % n
print('r1: ', r1)
r.insert(0, 0)
r.insert(1, r1)
r2 = n - r1
print('r2: ', r2)
r.insert(2, r2)
r3 = (Yp * p * Mq - Yq * q * Mp) % n
print('r3: ', r3)
r.insert(3, r3)
r4 = n - r3
print('r4: ', r4)
r.insert(4, r4)

for i in range(len(r)):
    if r[i] == m:
        print('Расшифровано верно! m = r{}'.format(i))

print('Время выполнения: ', time() - start)
