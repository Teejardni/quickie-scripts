import multiprocessing as mu
import numpy as np
import math
import time

def divisor_sum(num):
    total = 0
    for i in range(1, int(math.sqrt(num)) + 1):
        if num % i == 0:
            total+=i
            if i != num // i: 
                total+= (num // i)
    return total


if __name__ == "__main__":
    seed = np.random.default_rng(66)

    nums = seed.integers(low=0, high=10000000, size=50000)

    
    res = []
    start = time.time()
    for i in nums:
        t = divisor_sum(i)
        res.append(t)
    end = time.time()
    print(f'done seq in {end - start} sec')
    start = time.time()
    with mu.Pool(processes=mu.cpu_count()) as pool:
        results = pool.map(divisor_sum, nums)

    end = time.time()
    print(f"there are {len(results)} results done in {end - start}. Here are the first 5 values: {results[:5]}")
