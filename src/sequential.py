import time
from src.square import square  # Adjusted import to reflect the new path

def sequential_square(numbers):
    results = []
    for num in numbers:
        results.append(square(num))
    return results

def run_sequential(numbers):
    start_time = time.time()
    sequential_square(numbers)
    sequential_time = time.time() - start_time
    print(f"Sequential Time: {sequential_time:.4f} seconds")
