#################################################################################
# Name        : genetic_algorithm.py
#
# Description : All functions used for running the genetic algorithm
#
# Name        : Dries Borstlap
# Student #   : 4648099
##################################################################################

# IMPORTS
import random
import numpy as np
from snake_game import Snake, SnakeGame
from neural_net import NeuralNet



# Initialize a population of certain size
def initialize_population(population_size):

    population = []
    for _ in range(population_size):
        
        # amount of parameters (=genes) that defines a snake
        n_params = NeuralNet().n_params

        # choose random parameters (=genes) between -1 and 1 initially
        params = np.random.uniform(-1, 1, size = n_params)

        snake = Snake()
        snake.set_genes(params)
        population.append(snake)
    return population


# Evaluate the fitness of each snake
def evaluate_fitness(snake, max_age):

    # Calculate fitness based on different factors such as score, survival time, etc.
    game = SnakeGame(snake, max_age, visualize=False)
    score = game.get_score()
    age = game.age

    # Assign weights to each factor to prioritize them differently
    score_weight = 1
    age_weight = 0.0

    # Calculate the overall fitness using a weighted sum of the factors
    fitness = score_weight * score - age_weight * age

    snake.fitness = fitness
    return fitness


# Select the 'best' snakes, so they can pass on their genes
def selection(population, population_fitness, keep_fraction):

    # Sort the population based on fitness in descending order
    sorted_population = [snake for _, snake in sorted(zip(population_fitness, population), key=lambda x: x[0], reverse=True)]
    best_snake = sorted_population[0]

    # sorted_population = [snake for fitness, snake in sorted(zip(population_fitness, population))]
    # sorted_population = sorted(population, key=lambda snake: snake.fitness, reverse=True)
    
    # Select the top-performing snakes as parents for the next generation
    num_parents = int(len(sorted_population) * keep_fraction)  # Select top ..% as parents
    parents = sorted_population[:num_parents]

    return parents, best_snake


# Combine genes of parents to form a children population
def crossover(parents, offspring_size):

    offspring = []
    for _ in range(offspring_size):

        # randomly choose two parents from the selected parents
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)

        # Determine the crossover point
        crossover_point = random.randint(1, len(parent1.genes) - 1)

        # Create offspring by combining parent segments
        offspring_genes = np.hstack((parent1.genes[:crossover_point], parent2.genes[crossover_point:]))

        # make new snake, and set genes to the crossover genes of the parents
        child = Snake()
        child.set_genes(offspring_genes)

        offspring.append(child)

    return offspring


# Apply random mutations to a snake child
def mutation(population, MUTATION_RATE):

    mutated_population = []
    for snake in population:
        # Get genes which will be mutated
        mutated_genes = snake.genes

        # Apply mutation to certain percentage of genes
        for i in range(len(mutated_genes)):
            if random.random() < MUTATION_RATE:
                mutated_genes[i] = np.random.uniform(-1, 1)
        snake.set_genes(mutated_genes)

        mutated_population.append(snake)

    return mutated_population


def evolve_population(population, population_size, parent_fraction, mutation_rate, max_age):

    # Evaluate fitness for each snake
    population_fitness = [evaluate_fitness(snake, max_age) for snake in population]

    # Select parents
    parents, best_snake = selection(population, population_fitness, parent_fraction)
    # print(parents)

    # Create children
    offspring_crossover = crossover(parents, population_size)
    # print(offspring_crossover)

    # Mutate children snakes
    offspring_mutated = mutation(offspring_crossover, mutation_rate)

    # retrieve scores of current population, to be used for plotting
    scores = [max(population_fitness), np.average(population_fitness)]

    return offspring_mutated, best_snake, scores


