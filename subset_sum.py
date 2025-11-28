import itertools
import random
import time

def generate_sums_dp(arr):
    sums = {0}
    for num in arr:
        new_sums = set()
        for s in sums:
            new_sums.add(s + num)
        sums |= new_sums
    sums.remove(0)
    return sums

def subset_sum_meet_in_middle(X, s):
    n = len(X)
    
    mid = n // 2
    left = X[:mid]
    right = X[mid:]
    
    left_sums = generate_sums_dp(left)
    
    right_sums = generate_sums_dp(right)
    
    if s in left_sums:
        return True
    
    if s in right_sums:
        return True
    
    for left_sum in left_sums:
        if (s - left_sum) in right_sums:
            return True
    
    return False

def subset_sum_brute_force(X, s):
    n = len(X)
    for i in range(1, 2**n):
        total = 0
        for j in range(n):
            if (i >> j) & 1:
                total += X[j]
        if total == s:
            return True
    return False

def manual_testing():
    print("=== РУЧНОЕ ТЕСТИРОВАНИЕ ===")
    
    test_cases = [
        ([1, 2, 3], 3, True),
        ([1, 2, 3], 6, True),
        ([1, 2, 3], 7, False),
        ([4, 2, 7, 1], 11, True),
        ([4, 2, 7, 1], 3, True),
        ([1, 3, 5, 7], 14, False),
        ([], 0, False),
        ([5], 5, True),
        ([5], 3, False),
    ]
    
    for i, (X, s, expected) in enumerate(test_cases, 1):
        result = subset_sum_meet_in_middle(X, s)
        brute_result = subset_sum_brute_force(X, s)
        status = "Yes" if result == expected and result == brute_result else "No"
        print(f"Тест {i}: {status}")
        print(f"  Множество: {X}, целевая сумма: {s}")
        print(f"  Ожидаемый: {expected}, Полученный: {result}")
        print(f"  Полный перебор: {brute_result}")
        print()

def generate_random_test(n, value_range=(-100, 100)):
    X = [random.randint(value_range[0], value_range[1]) for _ in range(n)]
    
    if random.random() < 0.5:
        k = random.randint(1, n)
        subset = random.sample(X, k)
        s = sum(subset)
        has_solution = True
    else:
        max_sum = sum(max(0, x) for x in X)
        min_sum = sum(min(0, x) for x in X)
        s = random.randint(min_sum - 100, max_sum + 100)
        has_solution = subset_sum_brute_force(X, s)
    
    return X, s, has_solution

def performance_testing():
    print("=== ТЕСТИРОВАНИЕ ПРОИЗВОДИТЕЛЬНОСТИ ===")
    
    sizes = [10, 15, 20, 22, 24, 26]
    times = []
    
    for n in sizes:
        total_time = 0
        num_tests = 5
        
        for _ in range(num_tests):
            X, s, _ = generate_random_test(n)
            
            start_time = time.time()
            subset_sum_meet_in_middle(X, s)
            end_time = time.time()
            
            total_time += (end_time - start_time)
        
        avg_time = total_time / num_tests
        times.append(avg_time)
        
        print(f"n = {n}: среднее время = {avg_time:.6f} сек")
    
    return sizes, times

def main():
    manual_testing()
    
    print("=== ДОПОЛНИТЕЛЬНЫЕ ПРИМЕРЫ ===")
    examples = [
        ([1, 2, 3, 4, 5], 9),
        ([10, -2, 5, 8], 13),
        ([1, 1, 1, 1], 3),
    ]
    
    for X, s in examples:
        result = subset_sum_meet_in_middle(X, s)
        print(f"Множество: {X}, целевая сумма: {s} -> {'Существует' if result else 'Не существует'}")
    
    performance_testing()
    
if __name__ == "__main__":
    main()