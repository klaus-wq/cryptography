from random import randint
from sympy.ntheory import legendre_symbol
from time import time

#Эллиптические кривые представлены своими параметрами в порядке: p, a, b, q (из ГОСТ 34.10-12)
curves = {
    1: (
        0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFDC7,
        0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFDC4,
        0xE8C2505DEDFC86DDC1BD0B2B6667F1DA34B82574761CB0E879BD081CFD0B6265EE3CB090F30D27614CB4574010DA90DD862EF9D4EBEE4761503190785A71C760,
        0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF27E69532F48D89116FF22B8D4E0560609B4B38ABFAD2B85DCACDB1411F10B275

    ),
    2: (
        0x8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006F,
        0x8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006C,
        0x687D1B459DC841457E3E06CF6F5E2517B97C7D614AF138BCBF85DC806C4B289F3E965D2DB1416D217F8B276FAD1AB69C50F78BEE1FA3106EFB8CCBC7C5140116,
        0x800000000000000000000000000000000000000000000000000000000000000149A1EC142565A545ACFDB77BD9D40CFA8B996712101BEA0EC6346C54374F25BD
    ),
    3: (
        0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFDC7,
        0xDC9203E514A721875485A529D2C722FB187BC8980EB866644DE41C68E143064546E861C0E2C9EDD92ADE71F46FCF50FF2AD97F951FDA9F2A2EB6546F39689BD3,
        0xB4C4EE28CEBC6C2C8AC12952CF37F16AC7EFB6A9F69F4B57FFDA2E4F0DE5ADE038CBC2FFF719D2C18DE0284B8BFEF3B52B8CC7A5F5BF0A3C8D2319A5312557,
        0x3FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC98CDBA46506AB004C33A9FF5147502CC8EDA9E7A769A12694623CEF47F023ED
    )
}

start = time()

m = int(input('Введите сообщение: '))

def exgcd(a, b):
    x, xx, y, yy = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        x, xx = xx, x - xx*q
        y, yy = yy, y - yy*q
    return x

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
    if p <= 3:
        raise Exception("p должно быть > 3!") 

    S, Q = find_powers_two(p-1)

    #print(f"S = {S}, Q = {Q}")

    #if S == 0:
    #    raise Exception("p should be odd prime")

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

def random_point_in_curve(a, b, field):
    #Генерация случайно точки на эллиптической кривой
    if field != 3 and field != 2 and (4*a**3+27*b**2) == 0:
        raise Exception("Ограничение на a и b не выполнено!")
    x_cor = randint(1, field)
    f = x_cor**3 + a*x_cor + b
    while legendre_symbol(f, field) != 1:   
        x_cor = randint(1, field)
        f = x_cor**3 + a*x_cor + b
    y1, y2 = sqrt_mod(f, field)
    return x_cor, y1

'''def composition(x1, y1, x2, y2, p):
    #композиция P3(x3, y3) = P1(x1, y1) + P2(x2, y2)
    k = (y2 - y1)*exgcd(x2 - x1, p)
    x3 = k**2 - x1 - x2
    y3 = k*(x1 - x3) - y1
    return x3 % p, y3 % p

def double(a, p, x1, y1):
    #удвоение P3 = [2]P1
    k = (3*x1**2+a)*exgcd(2*y1, p)
    x3 = k**2 - 2*x1
    y3 = k*(x1 - x3) - y1
    return x3 % p, y3 % p

def mul(m, a, p, x, y):
    #[m]Q(x, y)
    m = bin(m)
    m = list(m[2:])
    x2 = x
    y2 = y
    x1 = 0
    y1 = 0
    i = 1
    while i < len(m):
        x2, y2 = double(a, p, x2, y2)
        if m[i] == '1':
            x2, y2 = composition(x1, y1, x2, y2, p)
        i += 1
    return x2, y2'''

def add(point_one_x, point_one_y, point_two_x, point_two_y, p): #слож 2х т. эллипт кривой

    L1 = lambda x1, x2, y1, y2, N: ((y2-y1)*exgcd(x2-x1, N)) % N
    L2 = lambda x1, y1, N: (3*x1**2 + a)*exgcd(2*y1, N) % N

    '''#случ, если одна из точек big_O, т.е нейтр эл-т по слож
    if (point_one_x == "O" and point_one_y == "O"):
        return point_two_x, point_two_y
    if (point_two_x == "O" and point_two_y == "O"):
        return point_one_x, point_one_y
        
    #случ, если т. наход на одной верт прямой 
    if (point_one_x == point_two_x and point_one_y != point_two_y):
        return Point("O","O")
    elif (point_one_y == point_two_y and point_one_y == 0):
        return Point("O","O")'''

    #все др случ считаем
    #else:
    lmbd = 0
    if point_one_x!= point_two_x:
        lmbd = L1(point_one_x, point_two_x, point_one_y, point_two_y, p)

    elif point_one_x == point_two_x and point_one_y == point_two_y:
        lmbd = L2(point_one_x, point_one_y, p)

    X = (lmbd**2 - point_one_x - point_two_x) % p
    Y = (lmbd*(point_one_x - X) - point_one_y) % p
            
    return X, Y

def mul(point_one_x, point_one_y, n):
            
    if n < 0:
        point_one_y = - point_one_y    #если множитель n<0 => склад обр т.

    point_two_x = point_one_x
    point_two_y = point_one_y
    for i in range(-n):
        point_one_x, point_one_y = add(point_one_x, point_one_y, point_two_x, point_two_y, n) #склад n раз сами с собой

    return point_one_x, point_one_y

def gen_key(q, G1, G2, a):
    #генерирует закрытый ключ и открытый из случайной точки выбранной на кривой

    secret = randint(1, q-1)    #секретный ключ Cu
    publicX, publicY = mul(G1, G2, secret)  #открытый ключ из точки и секретного ключа Du = [Cu]G
    return publicX, publicY, secret

def coding(m):

    curve_number = int(input("Введите номер кривой 1, 2 или 3: "))

    curve_id_const = curves.get(curve_number)
    p = curve_id_const[0]
    a = curve_id_const[1]
    b = curve_id_const[2]
    q = curve_id_const[3]
    print("p = ", p)
    print("a = ", a)
    print("b = ", b)
    print("q = ", q)
    G1, G2 = random_point_in_curve(a, b, p)
    print(f"\nСлучайная точка на кривой: {G1}, {G2}\n")
    A_key_pubX, A_key_pubY, A_key_sec = gen_key(q, G1, G2, a)
    print(f'Открытый ключ А: {A_key_pubX}, {A_key_pubY}')
    print(f'Закрытый ключ A: {A_key_sec}')
    B_key_pubX, B_key_pubY, B_key_sec = gen_key(q, G1, G2, a)
    print(f'Открытый ключ B: {B_key_pubX}, {B_key_pubY}')
    print(f'Закрытый ключ B: {B_key_sec}\n')
    m = m % p
    print(f'\nСообщение для шифрования: {m}\n')
    if m < p:
        K = randint(1, q-1) # Генерируем случайное число K
        print('K: ', K)
        Rx, Ry = mul(G1, G2, K) # R = [k]*G  - 1-я часть шифротекста
        Px, Py = mul(B_key_pubX, B_key_pubY, K) # P = [K]*B_open_key  
        print(f'P: {Px}, {Py}\n')
        e = m*Px % p     # e = mx mod p -  2-а часть шифротекста
        print('Шифротекст R и e: ')
        print(f'R: {Rx}, {Ry}')
        print('e: ', e)
    else:
        print('Сообщение должно быть меньше p!')
    return Rx, Ry, e, B_key_pubX, B_key_pubY, a, p

def decoding(Rx, Ry, e, B_key_pubX, B_key_pubY, a, p):
    Qx, Qy = mul(Rx, Ry, e) #Q = [B_sec_key]*R
    print(f'\nQ: {Qx}, {Qy}')
    message_decoded = (e*exgcd(Qx, p)) % p #m' = e/x mod p = e*x^(-1) mod p
    print(f'm_штрих: {message_decoded}\n')
    return message_decoded

Rx, Ry, e, B_key_pubX, B_key_pubY, a, p = coding(m)
message_decoded = decoding(Rx, Ry, e, B_key_pubX, B_key_pubY, a, p)
print('Исходное сообщение: ', message_decoded)
if message_decoded == m:
    print('Расшифровано верно!')
print('Время выполнения: ', time() - start)
