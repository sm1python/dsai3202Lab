import time
import random
from src.thread import *
from src.multiprocessing import *
from src.sequential import *
from src.performance import *
"""
Runs the summation functions sequentially, using threads, and using processes.
Measures execution time for each approach and prints the results.
"""
if __name__ == "__main__":
    n = 10**8
    # start_time = time.time()
    # seq_result = sequential_sum(n)
    # seq_time = time.time() - start_time
    # print(f"Sequential Sum from 1 to n: {seq_result}, Time: {seq_time:} sec")

    # start_time = time.time()
    # thread_result = threaded_sum(n)
    # thread_time = time.time() - start_time
    # print(f"Threaded Sum: {thread_result}, Time: {thread_time:.4f} sec")

    # start_time = time.time()
    # process_result = process_sum(n)
    # process_time = time.time() - start_time
    # print(f"Process Sum: {process_result}, Time: {process_time:.4f} sec")
    
    # print("Speedup (Threads):", seq_time / thread_time)
    # print("Speedup (Processes):", seq_time / process_time)
    performance_analysis(n)
# def run_all():