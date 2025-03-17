# src/synchronous_pool.py
import time
import multiprocessing
from src.square import square  # Adjusted import to reflect the new path

def synchronous_pool_map(numbers):
    with multiprocessing.Pool() as pool:
        results = pool.map(square, numbers)
    return results

def run_synchronous_pool(numbers):
    start_time = time.time()
    synchronous_pool_map(numbers)
    synchronous_pool_time = time.time() - start_time
    print(f"Synchronous Pool map() Time: {synchronous_pool_time:.4f} seconds")
