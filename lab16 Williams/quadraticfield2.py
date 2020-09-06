import time
from gmpy2 import mpz, mul, gcd, f_mod, invert

class QuadraticField(): #реализует объект вида - иррациональное квадратичное (квадратичные иррациональности) число a+b*sqrt(c). Вызываем как ф-ю и передаем a, b, c
    """

    x+y*sqrt(c)

    x is Re
    y is Im

    """
    #для задания объекта вызывается конструктор класса
    def __init__(self, x, y, c):
        self.re = x
        self.im = y
        self.c = c

    #вывод числа вида a+b*sqrt(c)
    def __str__(self):
        if self.im > 0:
            return f"{self.re}+{self.im}*sqrt({self.c})"
        else:
            return f"{self.re}{self.im}*sqrt({self.c})"
    
    #В начале проверка корня из с. Если у чисел разные корни из с,то нельзя выполнять операции.
    #сложение - покоординатно
    def __add__(self, other):
        if self.c != other.get_root():
            raise Exception("different roots")
        x = self.re + other.x()
        y = self.im + other.y()
        return QuadraticField(x,y,self.c)
    #умножение
    def __mul__(self, other):
        if self.c != other.get_root():
            raise Exception("different roots")
        x = self.re * other.x() + self.c * self.im * other.y()
        y = self.re * other.y() + self.im * other.x()
        return QuadraticField(x, y, self.c)
    #вычитание - покоординатно
    def __sub__(self, other):
        if self.c != other.get_root():
            raise Exception("different roots")
        x = self.re - other.x()
        y = self.im - other.y()
        return QuadraticField(x,y,self.c)
    #делим число по модулю на сопряжённое (обратное)
    def divmod_on_conj(self, N):
        Z = invert(mpz(self.x()**2-(self.y()**2)*self.c),N)
        X = ((self.x()**2+(self.y()**2)*self.c)*Z) % N
        Y = (2*self.x()*self.y()*Z) % N
        return QuadraticField(X, Y, self.c)

    def get_root(self):
        return self.c

    def x(self):
        return self.re

    def y(self):
        return self.im

    def conjugate(self):
        return QuadraticField(self.re, - self.im, self.c)
