"""
Calculates the sum of numbers from 1 to n sequentially.
    
Parameters:
n (int): The upper limit of the range to sum.
    
Returns:
int: The sum of numbers from 1 to n.
"""
def sequential_sum(n):
    seq = sum(range(1, n + 1))
    return (seq)

# n = 4
# k = 10000
# step = int(k/n)
# s = 0
# for i in range(n):
#     s += sum.chunk(start=int(k/n), end = (1+i)*step)
    
# s+=k
