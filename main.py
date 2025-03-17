# main.py
import random
import time
import multiprocessing
from src.sequential import run_sequential
from src.multiprocessing_individual import multiprocessing_square_individual
from src.multiprocessing_pool import run_multiprocessing_pool
from src.processpoolexecutor import run_processpoolexecutor
from src.synchronous_pool import run_synchronous_pool
from src.asynchronous_pool import run_asynchronous_pool
from src.connection_pool import ConnectionPool
from src.database_access import access_database


# Generate a list of 10^6 random numbers
random_numbers = [random.randint(1, 100) for _ in range(10**6)]

def run_all_tests(numbers):
    run_sequential(numbers)
    multiprocessing_square_individual(numbers)
    run_multiprocessing_pool(numbers)
    run_processpoolexecutor(numbers)
    run_synchronous_pool(numbers)
    run_asynchronous_pool(numbers)
     # Number of connections in the pool
    num_connections = 3
    # Number of processes simulating database operations
    num_processes = 10
    # Create a connection pool with a limited number of connections
    connection_pool = ConnectionPool(num_connections)
    # Create multiple processes to simulate database access
    processes = []
    for i in range(num_processes):
        process = multiprocessing.Process(target=access_database, args=(connection_pool,))
        processes.append(process)
    # Start all processes
    for process in processes:
        process.start()
    # Wait for all processes to complete
    for process in processes:
        process.join()
        
if __name__ == "__main__":
    run_all_tests(random_numbers)