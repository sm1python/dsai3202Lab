import numpy as np
import pandas as pd
import time
from enhanced_genetic_algorithms_functions import calculate_fitness, \
    select_in_tournament, order_crossover, mutate, \
    generate_unique_population

start = time.time()

# Load the distance matrix
distance_matrix = np.loadtxt('../datasets/city_distances.csv', delimiter=',', skiprows=1)

# Parameters
num_nodes = distance_matrix.shape[0]
population_size = 20000
num_tournaments = 4  # Number of tournaments to run
mutation_rate = 0.2
num_generations = 200
infeasible_penalty = 1e6  # Penalty for infeasible routes
stagnation_limit = 5  # Number of generations without improvement before regeneration

# Generate initial population
np.random.seed(42)  # For reproducibility
population = generate_unique_population(population_size, num_nodes)

# Track initial best fitness
initial_best_fitness = -calculate_fitness(min(population, key=lambda x: calculate_fitness(x, distance_matrix)), distance_matrix)
print(f"Initial Best Route Distance: {initial_best_fitness}")

# Initialize stagnation tracking
best_calculate_fitness = 1e6
stagnation_counter = 0

# Main GA loop
for generation in range(num_generations):
    # Evaluate fitness
    calculate_fitness_values = np.array(list(map(lambda route: -calculate_fitness(route, distance_matrix), population)))

    # Check for stagnation
    current_best_calculate_fitness = np.min(calculate_fitness_values)
    if current_best_calculate_fitness < best_calculate_fitness:
        best_calculate_fitness = current_best_calculate_fitness
        stagnation_counter = 0
    else:
        stagnation_counter += 1

    # Regenerate population if stagnation occurs
    if stagnation_counter >= stagnation_limit:
        print(f"Regenerating population at generation {generation} due to stagnation")
        
        # Keep the top 10% of the best individuals
        top_10_indices = np.argsort(calculate_fitness_values)[:population_size // 10]
        top_10_percent = [population[i] for i in top_10_indices]  
        
        # Generate new individuals to replace the rest
        new_population = generate_unique_population(population_size - len(top_10_percent), num_nodes)
        
        # Combine old top individuals with new individuals
        population = top_10_percent + new_population  
    
        stagnation_counter = 0
        continue

    # Selection, crossover, and mutation
    selected = select_in_tournament(population, calculate_fitness_values)
    offspring = [[0] + order_crossover(p1[1:], p2[1:]) for p1, p2 in zip(selected[::2], selected[1::2])]
    mutated_offspring = list(map(lambda route: mutate(route, mutation_rate), offspring))

    # Replace a random subset of individuals
    replace_indices = np.random.choice(range(len(population)), len(mutated_offspring), replace=False)
    for i, idx in enumerate(replace_indices):
        population[idx] = mutated_offspring[i]

    # Print best fitness
    print(f"Generation {generation}: Best Route Distance = {current_best_calculate_fitness}")

# Final fitness evaluation
calculate_fitness_values = np.array(list(map(lambda route: -calculate_fitness(route, distance_matrix), population)))

# Output the best solution
best_solution = min(population, key=lambda x: -calculate_fitness(x, distance_matrix))
end = time.time()
execution_time = end - start

print("Best Solution:", best_solution)
print("Total Distance:", -calculate_fitness(best_solution, distance_matrix))
print("Total Time:", execution_time)
