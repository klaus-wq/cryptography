from sympy import gcd
from random import randint
from sympy import isprime
import pyecm
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
                if pow(2, int(candidate - 1), int(candidate)) == 1 and pow(2, int(N + U), int(candidate)) != 1:
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

def find_e(p, q, fi):
    e = 2
    #i = 10 ** 2
    #while i < fi:
    if isprime(e) and (gcd(e,p-1) == gcd(e,q-1) == 1):
        if len(list(pyecm.factors(e, False, True, 8, 1))) == 1:
            #e = i
            #break
            return e % fi
    else:
        #i += 1
        e += 1
    return e % fi

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

#x = 12345678949568576072485765486
x = int(input('Введите исходное сообщение: '))
#print('Исходное сообщение x', x)
p, q = generate_p_q(200, 17)
print("p = {}, длина = {}".format(p, len(str(p))))
print("q = {}, длина = {}".format(q, len(str(q))))
m = p*q
print("m = {}, длина = {}".format(m, len(str(m))))
x = x % m
fi = (p-1)*(q-1)

e = find_e(p, q, fi)
print('Открытая экпонента e: ', e, end='\n')
d = (exgcd(e, fi)) % fi
print('Закрытый ключ d: ', d, end='\n')
y = find(x, e, m)
print('Зашифрованное сообщение y: ', y, end='\n')

x1 = find(y, d, m)
print('Расшифрованное сообщение x1: ', x1, end='\n')

if x == x1:
    print('Выполнено верно!')

print('Время выполнения:', - start + time())
