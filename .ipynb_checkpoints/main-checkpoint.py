import sys
import os
from src.threads import run_threads
from src.multiprocessor import run_multiprocessing

# Run threads and multiprocessing tasks
if __name__ == "__main__":
    run_threads(0, 1000)
    run_multiprocessing()
