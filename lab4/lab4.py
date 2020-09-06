import gmpy2 
import pyecm
from random import randint
import time
from math import pi

f = open('4.1.txt', 'w')
def is_square_free(n):
    prime_list = list(pyecm.factors(n,False,True, 8, 1))
    for i in range(len(prime_list)-1):
        if prime_list[i] == prime_list[i+1]:
            return False
    return True

N = 10**50
M = 1000

# for avg_time
summ = 0

start_time = time.time()

for i in range(M):
    a = randint(1,N)
    f. write("Число№ " + str(i+1) + "= " + str(a) + "\n") 
    print(a)
    if is_square_free(a):
        f. write("Это число свободно от квадратов." + "\n") 
        f. write("\n") 
        summ += 1
    else:
        summ += 0
        f. write("Это число не свободно от квадратов." + "\n")
        f. write("\n")  

print()
print("Эмпирическая оценка: " + str(summ/M))
f. write("Эмпирическая оценка: " + str(summ/M) + "\n")
    # print(list(pyecm.factors(a,False,True, 10, 1)))
print("Теоретическая оценка: " + str(6/pi**2))
f. write("Теоретическая оценка: " + str(6/pi**2) + "\n")
print(time.time()-start_time)
f. write("Время выполнения: " + str(time.time()-start_time) + "\n")
