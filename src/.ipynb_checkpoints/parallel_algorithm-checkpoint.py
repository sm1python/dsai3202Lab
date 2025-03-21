# this is parallel_algorithm.py:
from mpi4py import MPI
import numpy as np
import time
import pandas as pd
from genetic_algorithms_functions import calculate_fitness, select_in_tournament, order_crossover, mutate, generate_unique_population

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def main():
    # Load distance matrix on all nodes
    start = time.time()
    if rank == 0:
        distance_matrix = pd.read_csv('city_distances.csv').to_numpy()
        num_nodes = distance_matrix.shape[0]
    else:
        distance_matrix, num_nodes = None, None
    
    # Broadcast distance matrix and parameters
    distance_matrix = comm.bcast(distance_matrix, root=0)
    num_nodes = comm.bcast(num_nodes, root=0)
    
    # Parameters (same as before)
    population_size = 10000
    num_tournaments = 4
    mutation_rate = 0.1
    num_generations = 200
    
    # Generate initial population on root
    if rank == 0:
        population = generate_unique_population(population_size, num_nodes)
    else:
        population = None
    
    for generation in range(num_generations):
        # Scatter population chunks to workers
        population_chunk = comm.scatter(
            np.array_split(population, size) if rank == 0 else None,
            root=0
        )
        
        # Local fitness calculation
        local_fitness = np.array(
            [calculate_fitness(route, distance_matrix) for route in population_chunk]
        )
        
        # Gather all fitness values at root
        fitness_values = comm.gather(local_fitness, root=0)
        
        if rank == 0:
            # Rest of GA logic (selection, crossover, etc.)
            fitness_values = np.concatenate(fitness_values)
            
            # Check for stagnation
            current_best_fitness = np.min(fitness_values)
            best_individual = population[np.argmin(fitness_values)]
            
            # Selection, crossover, and mutation
            selected = select_in_tournament(population, fitness_values)
            offspring = []
            for i in range(0, len(selected), 2):
                parent1, parent2 = selected[i], selected[i + 1]
                route1 = order_crossover(parent1[1:], parent2[1:])
                offspring.append([0] + route1)
            mutated_offspring = [mutate(route, mutation_rate) for route in offspring]
            
            # Replacement
            for i, idx in enumerate(np.argsort(fitness_values)[::-1][:len(mutated_offspring)]):
                population[idx] = mutated_offspring[i]
            
            # Ensure population uniqueness
            unique_population = set(tuple(ind) for ind in population)
            while len(unique_population) < population_size:
                individual = [0] + list(np.random.permutation(np.arange(1, num_nodes)))
                unique_population.add(tuple(individual))
            population = [list(individual) for individual in unique_population]
            
            # Broadcast new population to all workers
            population = comm.bcast(population, root=0)
        else:
            population = comm.bcast(None, root=0)
    
    # Finalize
    if rank == 0:
        # Output best solution
        end = time.time()
        print(f"Best Solution: {best_individual}")
        print(f"Total Distance: {current_best_fitness}")
        print("Total Time:", time)

if __name__ == "__main__":
    main()