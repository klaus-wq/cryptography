import sympy
from sympy import totient
from sympy import reduced_totient
import time

start = time.time()
N = 2019 #показатель
a = 2019 #основание
z = 10**2019

tot = totient(z)
i = 0
aa = a
f = open('2019.txt', 'w')
for i in range(N - 1):
    r = aa % tot
    f. write("r = "+str(r) + "\n")                
    print("r = "+str(r))
    aa = pow(a,r,z)
    f. write("a = "+str(aa) + "\n")
    print("a = " + str(aa))

f. write("Ответ: "+str(aa) + "\n")    
print(aa)
print(- start + time.time())
f. write("Время: "+str(- start + time.time()) + "\n") 
