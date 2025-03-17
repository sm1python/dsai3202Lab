from mpi4py import MPI
import numpy as np
from src.square import square
import time 
import random

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
print(f"which process is this {rank}, and what is the size {size}")

if rank == 0:
    numbers = np.arange(size, dtype = 'i')
    
else:
    numbers = None
    
number = np.zeros(1, dtype = 'i')

comm.Scatter(numbers, number, root = 0)
print("numbers: ", numbers)
print("number: ", number)

resualt = square(number[0])
print("resualt: ", resualt)
time.sleep(random.randint(1, 10))
request = comm.isend(resualt, dest=0, tag=rank)

if rank == 0:
    resualts = np.zeros(size, dtype="i")
    for i in range(size):
        resualts[i] = comm.irecv(source = i, tag = i).wait()
    print(f'the resualts are {resualts}')

