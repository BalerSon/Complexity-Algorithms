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
def pre_calculation(a, b, m = 4):
    if isinstance(a, int):
        a_coeffs = [bool((a >> i) & 1) for i in range(a.bit_length())]
    else:
        a_coeffs = [bool(x) for x in a]
    
    if isinstance(b, int):
        b_coeffs = [bool((b >> i) & 1) for i in range(b.bit_length())]
    else:
        b_coeffs = [bool(x) for x in b]
    
    deg_a = len(a_coeffs) - 1
    deg_b = len(b_coeffs) - 1
    
    if deg_a < 0 or deg_b < 0:
        return 0 if isinstance(a, int) else []
    
    max_degree = deg_a + deg_b
    result_coeffs = [False] * (max_degree + 1)
    
    table_size = 1 << (2 * m)
    precomputed_table = [False] * table_size
    
    for i in range(1 << m):
        for j in range(1 << m):
            dot_product = False
            for k in range(m):
                if (i >> k) & 1 and (j >> k) & 1:
                    dot_product = not dot_product
            precomputed_table[(i << m) | j] = dot_product
    
    for k in range(max_degree + 1):
        total_sum = False
        block_start = 0
        
        while block_start <= k:
            block_end = min(block_start + m - 1, k)
            block_len = block_end - block_start + 1
            
            index_a = 0
            index_b = 0
            
            for offset in range(block_len):
                pos_a = block_start + offset
                pos_b = k - pos_a
                
                if pos_a < len(a_coeffs) and a_coeffs[pos_a]:
                    index_a |= (1 << offset)
                if pos_b < len(b_coeffs) and b_coeffs[pos_b]:
                    index_b |= (1 << offset)
            
            if block_len == m:
                block_result = precomputed_table[(index_a << m) | index_b]
            else:
                block_result = False
                for offset in range(block_len):
                    if (index_a >> offset) & 1 and (index_b >> offset) & 1:
                        block_result = not block_result
            
            total_sum = total_sum != block_result
            block_start += m
        
        result_coeffs[k] = total_sum
    
    if isinstance(a, int) and isinstance(b, int):
        result = 0
        for i, coeff in enumerate(result_coeffs):
            if coeff:
                result |= (1 << i)
        return result
    else:
        return result_coeffs
    
"""Алгоритм умножения со сжатием"""
def compression(a, b, word_size = 64):
    if isinstance(a, int):
        a_coeffs = [bool((a >> i) & 1) for i in range(a.bit_length())]
    else:
        a_coeffs = [bool(x) for x in a]
    
    if isinstance(b, int):
        b_coeffs = [bool((b >> i) & 1) for i in range(b.bit_length())]
    else:
        b_coeffs = [bool(x) for x in b]
    
    deg_a = len(a_coeffs) - 1
    deg_b = len(b_coeffs) - 1
    
    if deg_a < 0 or deg_b < 0:
        return 0 if isinstance(a, int) else []
    
    max_degree = deg_a + deg_b
    result_coeffs = [False] * (max_degree + 1)
    
    #Для каждого коэффициента при xᵏ находим диапазон индексов i таких что i+j=k
    for k in range(max_degree + 1):
        start_i = max(0, k - deg_b)
        end_i = min(k, deg_a)
        
        final_product = 0
        
        
        chunk_start = start_i
        while chunk_start <= end_i:
            chunk_end = min(chunk_start + word_size - 1, end_i)
            chunk_product = 0
            
            for i in range(chunk_start, chunk_end + 1):
                j = k - i
                if a_coeffs[i] and b_coeffs[j]:
                    chunk_product ^= (1 << (i - chunk_start))
            
            final_product ^= chunk_product
            chunk_start += word_size
        
        parity = False
        temp = final_product
        while temp:
            parity = not parity
            temp &= temp - 1
        
        result_coeffs[k] = parity
    
    if isinstance(a, int) and isinstance(b, int):
        result = 0
        for i, coeff in enumerate(result_coeffs):
            if coeff:
                result |= (1 << i)
        return result
    else:
        return result_coeffs
    
"""Измерение времени работы алгоритмов"""
def measure_performance(a, b):
    print('#'*60)
    print(f"{'\033[93m'}Time for a({a}) and b({b}): len(a) = {len(a)}, len(b) = {len(b)}{'\033[0m'}")
    print('#'*60)
    
    a = bitmask_to_int(a)
    b = bitmask_to_int(b)
    
    naive_start = time.perf_counter()
    naive_multiplication(a, b)
    naive_end = time.perf_counter()
    naive_time = naive_end - naive_start
    
    pre_start = time.perf_counter()
    pre_calculation(a, b)
    pre_end = time.perf_counter()
    pre_time = pre_end - pre_start
    
    compression_start = time.perf_counter()
    compression(a, b)
    compression_end = time.perf_counter()
    compression_time = compression_end - compression_start
    
    print(f"Naive multiplication: {1000 * naive_time:.10f} ms\nPre-calculation: {1000 * pre_time:.10f} ms\nCompression: {1000 * compression_time:.10f} ms\n")
    return
    
"""Создание тестовых битовых масок многочленов заданной степени"""
def test_generation(degree):
    coefficients = [random.randint(0, 1) for _ in range (degree + 1)]
    coefficients[0] = 1
    
    return coefficients

"""Перевод битовой маски в число"""
def bitmask_to_int(a):
    return int(''.join(str(i) for i in a), 2)
    
"""Вывод результатов работы алгоритмов"""
def demonstration(a, b):
    
    print(f'a = {a}')
    print(f'b = {b}\n')
    
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
    
    print(f'result = {bin(compression(a, b))[2:]}\n')
    
    return

if __name__ == "__main__":
    print("Testing with small degrees for correctness:")
    small_degrees = [2, 3, 4]
    for deg in small_degrees:
        for deg2 in small_degrees:
            a = test_generation(deg)
            b = test_generation(deg2)
            demonstration(a, b)
    
    print("\n" + "#"*80)
    print("Performance testing for degrees 2^n:")
    
    n = [500, 1000, 1500, 2000]
    for degree in n:
        a = test_generation(degree)
        b = test_generation(degree)
        times = measure_performance(a, b)