# src/multiprocessing_individual.py
import multiprocessing
from src.square import *

def chunked_processing(chunk, results):
    # Process a chunk of data and store the results in a list
    results.extend(map(square, chunk))

def multiprocessing_square_individual(numbers):
    # Define a chunk size
    chunk_size = 1000  # Adjust the chunk size as needed

    # Create a Pool with a smaller number of processes
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        # Create a Manager to store results from all processes
        with multiprocessing.Manager() as manager:
            results = manager.list()

            # Create chunks of numbers
            chunks = [numbers[i:i + chunk_size] for i in range(0, len(numbers), chunk_size)]

            # Use pool.map to process the chunks
            pool.starmap(chunked_processing, [(chunk, results) for chunk in chunks])

            return list(results)  # Convert manager list to a regular list
