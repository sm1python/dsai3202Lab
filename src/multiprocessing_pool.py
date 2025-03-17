# src/multiprocessing_pool.py
import time
import multiprocessing
from src.square import square  # Adjusted import to reflect the new path

def multiprocessing_pool_map(numbers):
    with multiprocessing.Pool() as pool:
        results = pool.map(square, numbers)
    return results

def multiprocessing_pool_apply(numbers):
    with multiprocessing.Pool() as pool:
        results = [pool.apply(square, (num,)) for num in numbers]
    return results

def run_multiprocessing_pool(numbers):
    # Test map
    start_time = time.time()
    multiprocessing_pool_map(numbers)
    multiprocessing_pool_map_time = time.time() - start_time
    print(f"Multiprocessing Pool map() Time: {multiprocessing_pool_map_time:.4f} seconds")
    
    # Test apply
    start_time = time.time()
    multiprocessing_pool_apply(numbers)
    multiprocessing_pool_apply_time = time.time() - start_time
    print(f"Multiprocessing Pool apply() Time: {multiprocessing_pool_apply_time:.4f} seconds")
