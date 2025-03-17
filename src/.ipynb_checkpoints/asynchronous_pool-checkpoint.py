# src/asynchronous_pool.py
import time
import multiprocessing
from src.square import square  # Adjusted import to reflect the new path

def asynchronous_pool_apply_async(numbers):
    with multiprocessing.Pool() as pool:
        async_results = [pool.apply_async(square, (num,)) for num in numbers]
        results = [result.get() for result in async_results]
    return results

def run_asynchronous_pool(numbers):
    start_time = time.time()
    asynchronous_pool_apply_async(numbers)
    asynchronous_pool_time = time.time() - start_time
    print(f"Asynchronous Pool apply_async() Time: {asynchronous_pool_time:.4f} seconds")
