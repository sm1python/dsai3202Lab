import numpy as np
import random

def calculate_fitness(route, distance_matrix):
    """
    Calculates the total distance traveled in the given route.
    Returns a large penalty if the route is infeasible.

    Parameters:
        - route (list): A list representing the order of nodes visited.
        - distance_matrix (numpy.ndarray): A matrix where [i, j] is the distance between nodes i and j.

    Returns:
        - float: The negative total distance traveled (negative for minimization).
    """
    try:
        distances = [distance_matrix[n1, n2] for n1, n2 in zip(route, route[1:])]
        if 10000 in distances:
            return -1e6  # Penalty for infeasible routes
        return -sum(distances)  # Negative for minimization
    except IndexError:
        return 1e6  # Return penalty in case of an invalid index

def select_in_tournament(population, scores, number_tournaments=4, tournament_size=3):
    """
    Tournament selection for genetic algorithms.

    Parameters:
        - population (list): The current population.
        - scores (np.array): The fitness scores.
        - number_tournaments (int): Number of tournaments.
        - tournament_size (int): Number of competitors in each tournament.

    Returns:
        - list: Selected individuals.
    """
    selected = []
    for _ in range(number_tournaments):
        participants = np.random.choice(range(len(population)), tournament_size, replace=False)
        best_idx = min(participants, key=lambda x: scores[x])  # Pick best based on min score
        selected.append(population[best_idx])
    return selected

def order_crossover(parent1, parent2):
    """
    Order crossover (OX) for permutations.

    Parameters:
        - parent1 (list): The first parent.
        - parent2 (list): The second parent.

    Returns:
        - list: The offspring.
    """
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    
    offspring = [-1] * size
    offspring[start:end + 1] = parent1[start:end + 1]
    
    fill_values = (x for x in parent2 if x not in offspring[start:end + 1])
    offspring = [next(fill_values) if x == -1 else x for x in offspring]
    
    return offspring

def mutate(route, mutation_rate=0.1):
    """
    Mutates a route by swapping two nodes.

    Parameters:
        - route (list): The route.
        - mutation_rate (float): Probability of mutation.

    Returns:
        - list: Mutated route.
    """
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(route)), 2)
        route[i], route[j] = route[j], route[i]
    return route

def generate_unique_population(population_size, num_nodes):
    """
    Generate a unique population of routes.

    Parameters:
        - population_size (int): Size of the population.
        - num_nodes (int): Number of nodes (including starting node).

    Returns:
        - list: A list of unique individuals.
    """
    individuals = {tuple([0] + list(np.random.permutation(range(1, num_nodes)))) for _ in range(population_size)}
    
    # Ensure we have enough individuals
    while len(individuals) < population_size:
        individuals.add(tuple([0] + list(np.random.permutation(range(1, num_nodes)))))
    
    return [list(ind) for ind in individuals]
