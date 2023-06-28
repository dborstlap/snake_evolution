# TODO
# check snake sorting method
# check if sorted right way (not in reverse)
# make NN part of snake class somehow
# bring genes outside of snake class, so it can be applied to any game in one click
# decouple snake from snake_game so not working with snake_game.snake objects

import random
import numpy as np
from snake_game import Snake, SnakeGame
from neural_net import NUM_WEIGHTS
import copy




def initialize_population(population_size):
    population = []
    for _ in range(population_size):
        snake = Snake()
        params = np.random.uniform(-1, 1, size = NUM_WEIGHTS)
        snake.set_genes(params)
        population.append(snake)
    return population


def evaluate_fitness(snake, max_age):
    # Implement your fitness evaluation logic here
    # You could consider factors like score, survival time, etc.
    # Return a fitness value for the given snake

    # Calculate fitness based on different factors such as score, survival time, etc.
    game = SnakeGame(snake, max_age, visualize=False)
    score = game.get_score()
    age = game.age

    # Assign weights to each factor to prioritize them differently
    score_weight = 1
    age_weight = 0.001

    # Calculate the overall fitness using a weighted sum of the factors
    fitness = score_weight * score + age_weight * age

    snake.fitness = fitness
    return fitness


def selection(population, population_fitness, keep_fraction):
    # Perform selection based on the fitness of each snake in the population
    # You can use different selection strategies like tournament selection, rank selection, etc.
    # Return the selected snakes

    # Sort the population based on fitness in descending order
    sorted_population = [snake for _, snake in sorted(zip(population_fitness, population), key=lambda x: x[0], reverse=True)]
    best_snake = sorted_population[0]

    # sorted_population = [snake for fitness, snake in sorted(zip(population_fitness, population))]
    # sorted_population = sorted(population, key=lambda snake: snake.fitness, reverse=True)
    
    # Select the top-performing snakes as parents for the next generation
    num_parents = int(len(sorted_population) * keep_fraction)  # Select top ..% as parents
    parents = sorted_population[:num_parents]

    return parents, best_snake


def crossover(parents, offspring_size):
    # Implement crossover operation to create offspring from two parent snakes
    # Return the offspring snake

    offspring = []
    for _ in range(offspring_size):
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



def mutation(population, MUTATION_RATE):
    # Implement mutation operation to introduce random changes in the snake's behavior
    # You can modify the snake's attributes or behavior based on the mutation rate
    # Return the mutated snake

    mutated_population = []
    for snake in population:
        # Get genes which will be mutated
        mutated_genes = snake.genes

        # Apply mutation
        for i in range(len(mutated_genes)):
            if random.random() < MUTATION_RATE:
                mutated_genes[i] = np.random.uniform(-1, 1)
        snake.set_genes(mutated_genes)

        mutated_population.append(snake)

    return mutated_population


# def mutation(offspring_crossover, mutation_rate):
#     # mutating the offsprings generated from crossover to maintain variation in the population
#     for idx in range(offspring_crossover.shape[0]):
#         for i in range(offspring_crossover.shape[1]):
#             if random.uniform(0, 1) < mutation_rate:
#                 random_value = np.random.choice(np.arange(-1, 1, step = 0.001), size = (1), replace = False)
#                 offspring_crossover[idx, i] = offspring_crossover[idx, i] + random_value
#     return offspring_crossover



def evolve_population(population, population_size, parent_fraction, mutation_rate, max_age):

    # Evaluate fitness for each snake
    population_fitness = [evaluate_fitness(snake, max_age) for snake in population]

    parents, best_snake = selection(population, population_fitness, parent_fraction)
    # print(parents)

    offspring_crossover = crossover(parents, population_size)
    # print(offspring_crossover)

    offspring_mutated = mutation(offspring_crossover, mutation_rate)

    scores = [max(population_fitness), np.average(population_fitness)]

    return offspring_mutated, best_snake, scores


