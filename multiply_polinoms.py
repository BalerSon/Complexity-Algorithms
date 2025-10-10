import random
import time

"""Наивный алгоритм умножения столбиком"""
def naive_multiplication(a, b):
    result = 0
    while b > 0:
        if b & 1 == 1:
            result ^= a
        a <<= 1
        b >>= 1
    
    return result

"""Алгоритм умножения с предподсчетом"""
def pre_calculation(a, b):
    result = 0
    return
    
"""Алгоритм умножения со сжатием"""
def compression(a, b):
    result = 0
    return
    
"""Измерение времени работы алгоритмов"""
def measure_performance():
    
    return
    
"""Создание тестовых битовых масок многочленов заданной степени"""
def test_generation(degree):
    coefficients = [random.randint(0, 1) for _ in range (degree + 1)]
    coefficients[degree] = 1
    
    return coefficients

"""Перевод битовой маски в число"""
def bitmask_to_int(a):
    a = int(''.join(str(i) for i in a), 2)
    return a
    
"""Вывод результатов работы алгоритмов"""
def demonstration():
    a = test_generation(4)
    b = test_generation(3)
    
    print(f'a = {a}')
    print(f'b = {b}')
    print()
    
    a = bitmask_to_int(a)
    b = bitmask_to_int(b)
    
    print('#'*60)
    print(f"{'\033[92m'}Standart algorithm:{'\033[0m'}")
    print('#'*60)
    
    print(f'result = {bin(naive_multiplication(a, b))[2:]}')
    
    print('#'*60)
    print(f"{'\033[92m'}Pre-calculation algorithm:{'\033[0m'}")
    print('#'*60)
    
    print(f'result = {bin(pre_calculation(a, b))[2:]}')
    
    print('#'*60)
    print(f"{'\033[92m'}Compression algorithm:{'\033[0m'}")
    print('#'*60)
    
    print(f'result = {bin(compression(a, b))[2:]}')
    
    return

if __name__ == "__main__":
    
    demonstration()
    