import time
import pyecm
from random import randint

f = open('primes2011.txt', 'w')
start_time = time.time()
dimensionPrimeNumber = 500
startPrimeNumber = 2011
TMP = startPrimeNumber

for i in range(1000):
    print(i+1)
    while len(str(TMP)) < dimensionPrimeNumber:
        N = 4 * TMP + 2
        U = 0
        candidate = 0
        while True:
            candidate = (N + U) * TMP + 1
            a = randint(2, 5)
            if pow(a, int(candidate - 1), int(candidate)) == 1 and pow(a, int(N + U), int(candidate)) != 1: 
                TMP = candidate
                break
            else:
                U = U - 2
    print(TMP) 
    f. write("Число№ " + str(i+1) + "= " + str(TMP) + "\n") 
    startPrimeNumber = startPrimeNumber + 2
    while len(list(pyecm.factors(startPrimeNumber, False, True, 8, 1))) != 1:
        startPrimeNumber = startPrimeNumber + 2
    TMP = startPrimeNumber

print("Время выполнения: ", time.time() - start_time)
f. write("Время выполнения: " + str(time.time()-start_time) + "\n")

