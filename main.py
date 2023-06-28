#################################################################################
# Name        : snake_game_v1.py
#
# Description : Initial attempt to make a snake game that could be played by a human
#
# Name        : Dries Borstlap
# Student #   : 4648099
##################################################################################


# imports
from genetic_algorithm import initialize_population, evolve_population, evaluate_fitness
from save_data import save_genes, save_score
from snake_game import run_game
import numpy as np

# constants
POPULATION_SIZE = 1000
MUTATION_RATE = 0.01
PARENT_FRACTION = 0.01
GENERATIONS = 1000
MAX_AGE = 1000


run_evolution = True


if run_evolution:
    population = initialize_population(POPULATION_SIZE)

    for generation in range(GENERATIONS):
        print('Generation:', generation)

        # Evaluate fitness, perform selection, crossover, and mutation
        population, best_snake, scores = evolve_population(population, POPULATION_SIZE, PARENT_FRACTION, MUTATION_RATE, MAX_AGE)

        # save the best snake genes of every generation in a csv file
        save_genes(best_snake.genes, generation)

        # save the scores of every generation in a csv file
        save_score(scores, generation)

        best_score, average_score = scores
        print('Best fitness:',best_score, 'Average fitness:', average_score)

    # end result best snake
    print(best_snake.genes)







