# src/connection_pool.py
import multiprocessing
import time
import random

class ConnectionPool:
    def __init__(self, num_connections):
        self.semaphore = multiprocessing.Semaphore(num_connections)  # Semaphore to limit access to connections
        self.num_connections = num_connections
        self.connections = [f"Connection-{i+1}" for i in range(num_connections)]  # Simulate connection pool

    def get_connection(self):
        """Acquires a connection if available"""
        self.semaphore.acquire()  # Wait for a connection to become available
        connection = self.connections.pop()  # Get a connection from the pool
        return connection

    def release_connection(self, connection):
        """Releases a connection back to the pool"""
        self.connections.append(connection)  # Add the connection back to the pool
        self.semaphore.release()  # Allow another process to acquire a connection
