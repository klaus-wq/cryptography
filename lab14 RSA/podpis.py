from sympy import gcd
from random import randint
from sympy import isprime
import pyecm
from time import time

start = time()

def generate_p_q(prime_number, start_prime):
    tmp = start_prime
    pq = []
    for i in range(4):
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
    Pa = pq[0]
    Qa = pq[1]
    Pb = pq[2]
    Qb = pq[3]
    return Pa, Qa, Pb, Qb


def find_e(p, q, fi):
	e = 17
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
Pa, Qa, Pb, Qb = generate_p_q(200, 17)
print("Pa = {}, длина = {}".format(Pa, len(str(Pa))))
print("Qa = {}, длина = {}".format(Qa, len(str(Qa))))
print("Pb = {}, длина = {}".format(Pb, len(str(Pb))))
print("Qb = {}, длина = {}".format(Qb, len(str(Qb))))
Ma = Pa * Qa
Mb = Pb * Qb
print("Ma = {}, длина = {}".format(Ma, len(str(Ma))))
print("Mb = {}, длина = {}".format(Mb, len(str(Mb))))
if x > Ma:
    x = x % Ma
else:
    x = x % Mb

fiA = (Pa - 1)*(Qa - 1)
fiB = (Pb - 1)*(Qb - 1)

eA = find_e(Pa, Qa, fiA)
print('Открытая экпонента eA: ', eA, end='\n')
eB = find_e(Pb, Qb, fiB)
print('Открытая экпонента eB: ', eB, end='\n')
dA = (exgcd(eA, fiA)) % fiA
print('Закрытый ключ dA: ', dA, end='\n')
dB = (exgcd(eB, fiB)) % fiB
print('Закрытый ключ dB: ', dB, end='\n')
y = find(x, dA, Ma)
print('y: ', y, end='\n')
f = find(y, eB, Mb)
print('Зашифрованное сообщение f: ', f, end='\n')

u = find(f, dB, Mb)
print('u: ', u, end='\n')
w = find(u, eA, Ma)
print('Расшифрованное сообщение w: ', w, end='\n')

if x == w:
	print('Выполнено верно!')

print('Время выполнения:', - start + time())