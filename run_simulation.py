#################################################################################
# Name        : run_simulation.py
#
# Description : Runs and visualises the snake game using ai.
#               The user can run the game for any set of genes (parameters for the ai)
#
# Name        : Dries Borstlap
# Student #   : 4648099
##################################################################################


from snake_game import run_game
import numpy as np
import csv
import os



def read_last_row(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
        last_row = [float(value) for value in data[-1]]
    return np.array(last_row)


# genes_file = os.path.join(os.getcwd(), 'data/4_pop_1000_parent_0.1_relu/best_genes.csv')
genes_file = os.path.join(os.getcwd(), 'data/best_genes.csv')

best_genes = read_last_row(genes_file)

print(best_genes)

run_game(best_genes, visualize=True, record=True)




