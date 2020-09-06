from random import randint
import pyecm
from sympy import factorint, isprime, gcd, legendre_symbol, jacobi_symbol
from time import time
from math import sqrt, ceil
import quadraticfield2 as qd

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

p, q = generator(3, 7)
print('Открытый ключ {R, e, C, A}: ')
R = p * q
print('R: ', R)

def find_C(p, q):
    c = 2
    while (legendre_symbol(c, p))%4 != (-p) % 4 or (legendre_symbol(c, q))%4 != (-q) % 4:
        c += 1
    return c

def find_A(c, R):
    a = 2
    while jacobi_symbol((a**2-c),R) != -1 or gcd(a, R) != 1:
        a += 1
    return a

def find_e(w):
    e = 2
    while gcd(e, w) != 1:
        e += 1
    return e

'''def find_d(e, w):
    tmp = (w+1)//2
    x = exgcd(e, w)
    nod = gcd(e,w)
    if tmp % nod == 0:
        d = (tmp*x//nod) % w
    return d'''

C = find_C(p, q)
print('C: ', C)
A = find_A(C, R)
print('A: ', A)

w = (p - legendre_symbol(C, p))*(q - legendre_symbol(C, q))*exgcd(4, R) % R
print('w: ', w)
e = find_e(w)
print('e: ', e)
d =  ((w+1)*exgcd(2, w)*exgcd(e, w)) % w
#d = (pow(e,-1,w)*(w+1)//2) % w
print('Секретный ключ d: ', d)
print('p, q, w, d держатся в секрете.')

M = int(input('Введите передаваемое сообщение: '))
M = M % R
print('Сообщение для шифрования: ', M)

def find_XY(a, b, R, e):
    X = []
    Y = []
    X.insert(0,0)
    Y.insert(0,0)
    X.insert(1,a)
    X.insert(2, (2*a**2 - 1) % R)
    Y.insert(1, b)
    Y.insert(2, (2*a*b) % R)
    i = 3
    while i < e+1:
        if i % 2 == 0:
            X.insert(i, (2*(X[i//2])**2 - 1) % R)
            Y.insert(i, (2*X[i//2]*Y[i//2]) % R)
            i += 1
        else:
            X.insert(i, (2*X[(i-1)//2]*X[((i-1)//2)+1] - a) % R)
            Y.insert(i, (2*X[(i-1)//2]*Y[((i-1)//2)+1] - b) % R)
            i += 1
    return X[e], Y[e]

def coding(M, C, R, A, e):
    if jacobi_symbol((M**2 - C), R) == 1:
        b1 = 0
        a = (M**2 + C)*exgcd(M**2 - C, R) % R
        b = 2*M*exgcd(M**2 - C, R) % R
    if jacobi_symbol((M**2 - C), R) == -1:
        b1 = 1
        a = (((M**2 + C)*(A**2 + C) + 4*A*C*M))*exgcd(((M**2 - C)*(A**2 - C)), R) % R
        b = ((2*A)*(M**2 + C) + 2*M*(A**2 + C))*exgcd(((M**2 - C)*(A**2 - C)), R) % R
    if jacobi_symbol((M**2 - C), R) == 0:
        print('Символ Якоби равен 0!')
    print('a: ', a)
    print('b: ', b)
    add = qd.QuadraticField(a, b, C)
    print(f"alfa = {add}")
    alfa = a + b*sqrt(C)
    Xe, Ye = find_XY(a, b, R, e)
    print('Xe: ', Xe)
    print('Ye: ', Ye)
    E = (Xe*exgcd(Ye, R)) % R
    b2 = a % 2
    return b1, alfa, E, b2

def encoding(E, C, d, b2, b1, A):
    alfa2e_a = ((E**2 + C)*exgcd((E**2 - C),R)) % R
    alfa2e_b = ((2*E*exgcd((E**2 - C),R))) % R
    add = qd.QuadraticField(alfa2e_a, alfa2e_b, C)
    print(f"alfa_2e = {add}")
    Xd, Yd = find_XY(alfa2e_a, alfa2e_b, R, d)
    print('Xd: ', Xd)
    print('Yd: ', Yd)
    alfa_shtrih_a = Xd
    alfa_shtrih_b = Yd
    if b2 == 1:
        if alfa_shtrih_a % 2 == 0:
            alfa_shtrih_a = (-Xd) % R
            alfa_shtrih_b = (-Yd) % R
    if b2 == 0:
        if alfa_shtrih_a % 2 == 1:
            alfa_shtrih_a = (-Xd) % R
            alfa_shtrih_b = (-Yd) % R
    alfa_2ed = alfa_shtrih_a + alfa_shtrih_b*int(sqrt(C))
    alfa_2ed = qd.QuadraticField(alfa_shtrih_a, alfa_shtrih_b, C)
    print(f"alfa_shtrih = {alfa_2ed}")

    if b1 == 1:
        #alfa_shtrih_a = ((alfa_shtrih_a*A**2 + alfa_shtrih_a*C - 2*A*alfa_shtrih_b*C)*exgcd(A**2 - C, R)) % R
        #alfa_shtrih_b = ((alfa_shtrih_b*A**2 + alfa_shtrih_b*C - 2*A*alfa_shtrih_a)*exgcd(A**2 - C, R)) % R
        add = qd.QuadraticField(A, 1, C)
        #print(f"add = {add}")
        add = add.divmod_on_conj(R)
        #print(f"add1 = {add}")
        add = qd.QuadraticField(add.x(), - add.y(), C)
        #print(f"add_conj = {add}")
        alfa_2ed = alfa_2ed*add
        alfa_2ed = qd.QuadraticField(alfa_2ed.x()%R,alfa_2ed.y()%R,alfa_2ed.c)
        print(f"alfa_shtrih = {alfa_2ed}")
    #print("alfa_shtrih_a = ", alfa_2ed.x())
    #print("alfa_shtrih_b = ", alfa_2ed.y())

    u = alfa_2ed.x()+1
    v = alfa_2ed.x()-1
    x = alfa_2ed.y()
    #print('alfa_shtrih_a: ', alfa_shtrih_a)
    #print('alfa_shtrih_b: ', alfa_shtrih_b)
    #u = alfa_shtrih_a+1
    #v = alfa_shtrih_a-1
    #x = alfa_shtrih_b

    #kor_c = find(C, (R + 1)//4, R)
    #M2 = (((c*x*(v-u)%N)*(exgcd(v**2-x**2*c, N)%N))%N + kor_c*(((u*v - x**2*c)%N)*(exgcd(v**2-x**2*c, N)%N))%N)%N

    M2a = ((C*x*(v-u)%R)*(exgcd(v**2-x**2*C, R)%R))%R
    M2b = (((u*v - x**2*C)%R)*(exgcd(v**2-x**2*C, R)%R))%R
    #M2a = ((alfa_shtrih_a**2 - alfa_shtrih_b**2*C - 1)*exgcd(alfa_shtrih_a**2 - 2*alfa_shtrih_a - alfa_shtrih_b**2*C + 1, R)) % R
    #M2b = ((-2*alfa_shtrih_b*C)*exgcd(alfa_shtrih_a**2 - 2*alfa_shtrih_a - alfa_shtrih_b**2*C + 1, R)) % R
    #add = qd.QuadraticField(M2a, M2b, C)
    #print(f"M = {add}")
    return M2a, M2b

b1, alfa, E, b2 = coding(M, C, R, A, e)
print('Криптотекст {E, b1, b2}: ')
print('b1: ', b1)
print('b2: ', b2)
print('E(M): ', E)
m1, m2 = encoding(E, C, d, b2, b1, A)
print('Исходное сообщение: ', m1, m2)

if M == m1 or M == m2:
    print('Расшифровано верно!')

print('\nЗатраченное время: ', time()-start)

