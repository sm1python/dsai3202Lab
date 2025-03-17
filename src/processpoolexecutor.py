# src/processpoolexecutor.py
import time
from concurrent.futures import ProcessPoolExecutor
from src.square import square  # Adjusted import to reflect the new path

def concurrent_futures_square(numbers):
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(square, numbers))
    return results

def run_processpoolexecutor(numbers):
    start_time = time.time()
    concurrent_futures_square(numbers)
    concurrent_futures_time = time.time() - start_time
    print(f"ProcessPoolExecutor Time: {concurrent_futures_time:.4f} seconds")
