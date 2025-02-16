import time
from src.thread import threaded_sum
from src.multiprocessing import process_sum
from src.sequential import sequential_sum

def run_sequential(n):
    total_start_time = time.time()
    
    # Sequential execution of the summation
    seq_result = sequential_sum(n)
    
    total_end_time = time.time()
    return seq_result, total_end_time - total_start_time

def run_threads(n, num_threads=4):
    total_start_time = time.time()
    
    # Threaded execution of the summation
    thread_result = threaded_sum(n, num_threads)
    
    total_end_time = time.time()
    return thread_result, total_end_time - total_start_time

def run_multiprocessing(n, num_processes=4):
    total_start_time = time.time()
    
    # Multiprocessing execution of the summation
    process_result = process_sum(n, num_processes)
    
    total_end_time = time.time()
    return process_result, total_end_time - total_start_time

def performance_analysis(n):
    # Run sequential case to get baseline time
    seq_result, seq_time = run_sequential(n)
    print(f"Sequential Sum from 1 to {n}: {seq_result}, Time: {seq_time:.4f} seconds")
    
    # Run threading case
    thread_result, thread_time = run_threads(n)
    print(f"Threaded Sum: {thread_result}, Time: {thread_time:.4f} seconds")

    # Run multiprocessing case
    process_result, process_time = run_multiprocessing(n)
    print(f"Process Sum: {process_result}, Time: {process_time:.4f} seconds")

    # Calculate speedups
    speedup_threads = seq_time / thread_time
    speedup_multiprocessing = seq_time / process_time
    
    # Calculate efficiency
    num_threads = 4  # Threads for parallel execution
    num_processes = 4  # Processes for parallel execution
    
    efficiency_threads = speedup_threads / num_threads
    efficiency_multiprocessing = speedup_multiprocessing / num_processes
    
    # Assume P (parallelizable portion) to be around 0.95 (assuming 95% of the task is parallelizable)
    P = 0.95

    # Amdahl's Law for speedup (assuming 4 workers, 4 threads or processes)
    amdahl_speedup_threads = 1 / ((1 - P) + (P / num_threads))
    amdahl_speedup_multiprocessing = 1 / ((1 - P) + (P / num_processes))
    
    # Gustafson's Law for speedup (assuming N workers)
    gustafson_speedup_threads = num_threads - ((1 - P) * num_threads)
    gustafson_speedup_multiprocessing = num_processes - ((1 - P) * num_processes)

    # Print results
    print("\nPerformance Analysis:")
    print(f"Speedup (Threads): {speedup_threads:.4f}")
    print(f"Speedup (Multiprocessing): {speedup_multiprocessing:.4f}")
    
    print(f"Efficiency (Threads): {efficiency_threads:.4f}")
    print(f"Efficiency (Multiprocessing): {efficiency_multiprocessing:.4f}")
    
    print(f"Amdahl's Speedup (Threads): {amdahl_speedup_threads:.4f}")
    print(f"Amdahl's Speedup (Multiprocessing): {amdahl_speedup_multiprocessing:.4f}")
    
    print(f"Gustafson's Speedup (Threads): {gustafson_speedup_threads:.4f}")
    print(f"Gustafson's Speedup (Multiprocessing): {gustafson_speedup_multiprocessing:.4f}")

if __name__ == "__main__":
    # Set the value of n (for large summation)
    n = 10**8

    # Run the performance analysis once
    performance_analysis(n)