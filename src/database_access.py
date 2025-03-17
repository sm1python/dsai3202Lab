# src/database_access.py
import time
import random
import multiprocessing  # <-- Add this import

def access_database(connection_pool):
    # Simulate acquiring a connection from the pool
    connection = connection_pool.get_connection()
    
    # Print that the process has acquired a connection
    print(f"Process {multiprocessing.current_process().name} has acquired {connection}")
    
    # Simulate performing a database operation (sleep for a random duration)
    time.sleep(random.uniform(1, 3))  # Simulating work
    
    # Release the connection back to the pool
    connection_pool.release_connection(connection)
    
    # Print that the process has released the connection
    print(f"Process {multiprocessing.current_process().name} has released {connection}")
