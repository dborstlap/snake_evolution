#################################################################################
# Name        : main.py
#
# Description : Main file, used to run the genetic optimisation algorithm
#
# Name        : Dries Borstlap
# Student #   : 4648099
##################################################################################


# TODO
# make it possible to run main.py in terminal, and give it standard inputs to choose between play_yourself of train_ai
# check installation procedure in readme
# Readme maybe add problem defenition and goals for this project in the beginning.
# and Readme also add section about hyperparameters maybe


# IMPORTS
from genetic_algorithm import initialize_population, evolve_population, evaluate_fitness
from save_data import save_genes, save_score, save_dict_to_file
import neural_net
import numpy as np


# SETTINGS
POPULATION_SIZE = 1000
MUTATION_RATE = 0.01
PARENT_FRACTION = 0.15
GENERATIONS = 2000
MAX_AGE = 1000


# Save hyperparameters to file, so can be reviewed when analysing data
hyper_params = {
    'POPULATION_SIZE': POPULATION_SIZE,
    'MUTATION_RATE': MUTATION_RATE,
    'PARENT_FRACTION': PARENT_FRACTION,
    'GENERATIONS': GENERATIONS,
    'MAX_AGE': MAX_AGE,
    'NODES': neural_net.NODES }
save_dict_to_file(hyper_params)
     

#-----------------------
# GENETIC OPTIMISATION
#-----------------------

# initialize the population of snakes
population = initialize_population(POPULATION_SIZE)

# perform genetic algorithm for n generations
for generation in range(GENERATIONS):

    # Evaluate fitness, perform selection, crossover, and mutation
    population, best_snake, scores = evolve_population(population, POPULATION_SIZE, PARENT_FRACTION, MUTATION_RATE, MAX_AGE)
    best_score, average_score = scores

    # print results
    print('Generation:', generation)
    print('Best fitness:',best_score, 'Average fitness:', average_score)

    # save results for future analysis
    save_score(scores, generation, filename='final/scores_'+str(neural_net.NODES))
    save_genes(best_snake.genes, generation)

# print trained result
print('Best fitness:',best_score, 'Average fitness:', average_score)
print('DONE')
