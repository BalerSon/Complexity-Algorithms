import numpy as np
import time
import random

def strassen_z2(A, B):
    """
    Умножение матриц над Z₂ (GF(2)) алгоритмом Штрассена
    """
    n = len(A)
    
    if n <= 2:
        return naive_matrix_multiply_z2(A, B)
    
    mid = n // 2
    
    A11 = [row[:mid] for row in A[:mid]]
    A12 = [row[mid:] for row in A[:mid]]
    A21 = [row[:mid] for row in A[mid:]]
    A22 = [row[mid:] for row in A[mid:]]
    
    B11 = [row[:mid] for row in B[:mid]]
    B12 = [row[mid:] for row in B[:mid]]
    B21 = [row[:mid] for row in B[mid:]]
    B22 = [row[mid:] for row in B[mid:]]
    
    A11_plus_A22 = matrix_add_z2(A11, A22)
    B11_plus_B22 = matrix_add_z2(B11, B22)
    M1 = strassen_z2(A11_plus_A22, B11_plus_B22)
    
    A21_plus_A22 = matrix_add_z2(A21, A22)
    M2 = strassen_z2(A21_plus_A22, B11)
    
    B12_minus_B22 = matrix_add_z2(B12, B22)
    M3 = strassen_z2(A11, B12_minus_B22)
    
    B21_minus_B11 = matrix_add_z2(B21, B11)
    M4 = strassen_z2(A22, B21_minus_B11)
    
    A11_plus_A12 = matrix_add_z2(A11, A12)
    M5 = strassen_z2(A11_plus_A12, B22)
    
    A21_minus_A11 = matrix_add_z2(A21, A11)
    B11_plus_B12 = matrix_add_z2(B11, B12)
    M6 = strassen_z2(A21_minus_A11, B11_plus_B12)
    
    A12_minus_A22 = matrix_add_z2(A12, A22)
    B21_plus_B22 = matrix_add_z2(B21, B22)
    M7 = strassen_z2(A12_minus_A22, B21_plus_B22)
    
    C11 = matrix_add_z2(M1, M4)
    C11 = matrix_add_z2(C11, M7)
    C11 = matrix_add_z2(C11, M5)
    
    C12 = matrix_add_z2(M3, M5)
    
    C21 = matrix_add_z2(M2, M4)
    
    C22 = matrix_add_z2(M1, M2)
    C22 = matrix_add_z2(C22, M3)
    C22 = matrix_add_z2(C22, M6)
    
    return combine_submatrices(C11, C12, C21, C22)

def naive_matrix_multiply_z2(A, B):
    """Наивное умножение матриц над Z₂"""
    n = len(A)
    C = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for k in range(n):
            if A[i][k]:
                for j in range(n):
                    C[i][j] ^= B[k][j]
    
    return C

def matrix_add_z2(A, B):
    """Сложение матриц над Z₂ (XOR)"""
    n = len(A)
    return [[A[i][j] ^ B[i][j] for j in range(n)] for i in range(n)]

def combine_submatrices(C11, C12, C21, C22):
    """Объединяет 4 подматрицы в одну"""
    n = len(C11) * 2
    C = [[0] * n for _ in range(n)]
    
    mid = n // 2
    
    for i in range(mid):
        for j in range(mid):
            C[i][j] = C11[i][j]
            C[i][j + mid] = C12[i][j]
            C[i + mid][j] = C21[i][j]
            C[i + mid][j + mid] = C22[i][j]
    
    return C

def create_random_matrix_z2(n):
    """Создает случайную матрицу над Z₂"""
    return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]

def create_identity_matrix(n):
    """Создает единичную матрицу над Z₂"""
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def matrices_equal(A, B):
    """Проверяет равенство матриц"""
    n = len(A)
    for i in range(n):
        for j in range(n):
            if A[i][j] != B[i][j]:
                return False
    return True

def test_correctness():
    """Тестирование корректности алгоритма"""
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ КОРРЕКТНОСТИ")
    print("=" * 60)
    
    print("\n1. Умножение на единичную матрицу:")
    A = create_random_matrix_z2(4)
    I = create_identity_matrix(4)
    
    result_strassen = strassen_z2(A, I)
    result_naive = naive_matrix_multiply_z2(A, I)
    
    print(f"Результаты совпадают: {matrices_equal(A, result_strassen)}")
    print(f"Сравнение с наивным: {matrices_equal(result_strassen, result_naive)}")
    
    print("\n2. Случайные матрицы 2x2:")
    A = [[1, 0], [1, 1]]
    B = [[1, 1], [0, 1]]
    
    result_strassen = strassen_z2(A, B)
    result_naive = naive_matrix_multiply_z2(A, B)
    expected = [[1, 1], [1, 0]]
    
    print(f"A = {A}")
    print(f"B = {B}")
    print(f"Strassen: {result_strassen}")
    print(f"Naive:    {result_naive}")
    print(f"Ожидаем:  {expected}")
    print(f"Корректно: {matrices_equal(result_strassen, expected)}")
    
    print("\n3. Случайные матрицы 4x4:")
    A = create_random_matrix_z2(4)
    B = create_random_matrix_z2(4)
    
    result_strassen = strassen_z2(A, B)
    result_naive = naive_matrix_multiply_z2(A, B)
    
    print(f"Результаты совпадают: {matrices_equal(result_strassen, result_naive)}")

def measure_performance():
    """Измерение производительности"""
    print("\n" + "=" * 60)
    print("ИЗМЕРЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ")
    print("=" * 60)
    
    sizes = [2**n for n in range(3, 9)]
    
    print(f"{'Размер':>8} | {'Штрассен (мс)':>12} | {'Наивный (мс)':>12} | {'Ускорение':>10}")
    print("-" * 60)
    
    for size in sizes:
        A = create_random_matrix_z2(size)
        B = create_random_matrix_z2(size)
        
        start_time = time.perf_counter()
        result_strassen = strassen_z2(A, B)
        strassen_time = (time.perf_counter() - start_time) * 1000
        
        if size <= 64:
            start_time = time.perf_counter()
            result_naive = naive_matrix_multiply_z2(A, B)
            naive_time = (time.perf_counter() - start_time) * 1000
            
            if not matrices_equal(result_strassen, result_naive):
                print(f"ОШИБКА: Результаты не совпадают для размера {size}")
            
            speedup = naive_time / strassen_time if strassen_time > 0 else 0
            print(f"{size:8} | {strassen_time:12.3f} | {naive_time:12.3f} | {speedup:10.2f}x")
        else:
            print(f"{size:8} | {strassen_time:12.3f} | {'—':>12} | {'—':>10}")

def analyze_complexity():
    """Анализ асимптотической сложности"""
    print("\n" + "=" * 60)
    print("АНАЛИЗ АСИМПТОТИЧЕСКОЙ СЛОЖНОСТИ")
    print("=" * 60)
    
    sizes = [2**n for n in range(3, 7)]
    times = []
    
    for size in sizes:
        A = create_random_matrix_z2(size)
        B = create_random_matrix_z2(size)
        
        start_time = time.perf_counter()
        strassen_z2(A, B)
        elapsed_time = time.perf_counter() - start_time
        times.append(elapsed_time)
        
        print(f"Размер {size:3}: {elapsed_time:.6f} сек")
    
    print("\nОценка сложности O(n^a):")
    for i in range(1, len(times)):
        ratio = times[i] / times[i-1]
        alpha = np.log2(ratio) / np.log2(2)
        print(f"n={sizes[i-1]}-{sizes[i]}: время выросло в {ratio:.2f} раз, a = {alpha:.3f}")
    
if __name__ == "__main__":
    random.seed(42)
    
    test_correctness()
    measure_performance()
    analyze_complexity()