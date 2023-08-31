#################################################################################
# Name        : save_data.py
#
# Description : Save various types of data to files
#
# Name        : Dries Borstlap
# Student #   : 4648099
##################################################################################

# Imports
import csv
import os
import numpy as np
import json

# current working directory
cwd = os.getcwd()


# create directory of it doesnt exist yet
def make_dir(file_path):
    directory_path = os.path.dirname(file_path)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


# save genes to file
def save_genes(snake_genes, generation, filename='best_genes'):

    file_path = os.path.join(cwd, 'data/'+filename+'.csv')
    make_dir(file_path)

    # make clean file at start of run
    if generation == 0:
        open(file_path, 'w').close()
    
    # Open our existing CSV file in append mode
    with open(file_path, 'a', newline='') as file:
    
        # Pass this file object to csv.writer()
        writer = csv.writer(file)
    
        # Pass the list as an argument into the writerow()
        writer.writerow(snake_genes)
    
        # Close the file object
        file.close()


# Save best and average scores of populatioin to file
def save_score(score, generation, filename='scores'):
    
    file_path = os.path.join(cwd, 'data/'+filename+'.csv')
    make_dir(file_path)

    # make clean file at start of run
    if generation == 0:
        open(file_path, 'w').close()
    
    # Open our existing CSV file in append mode
    with open(file_path, 'a', newline='') as file:
    
        # Pass this file object to csv.writer()
        writer = csv.writer(file)
    
        row_data= np.hstack((generation, score))
        
        # Pass the list as an argument into the writerow()
        writer.writerow(row_data)
    
        # Close the file object
        file.close()


# Save a dictionary to a file
def save_dict_to_file(dictionary, filename='hyper_parameters'):
    file_path = 'data/'+filename+'.json'
    make_dir(file_path)
    with open(file_path, 'w') as file:
        json.dump(dictionary, file)


# Load a dictiary from a file, that was saved using 'save_dict_to_file' function
def load_dict_from_file(file_path):
    with open(file_path, 'r') as file:
        dictionary = json.load(file)
    return dictionary


