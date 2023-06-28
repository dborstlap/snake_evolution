
import csv
import os
import numpy as np

# current working directory
cwd = os.getcwd()



def save_genes(snake_genes, generation):

    path = os.path.join(cwd, 'data/best_genes.csv')

    # make clean file at start of run
    if generation == 0:
        open(path, 'w').close()
    
    # Open our existing CSV file in append mode
    # Create a file object for this file
    with open(path, 'a', newline='') as file:
    
        # Pass this file object to csv.writer()
        # and get a writer object
        writer = csv.writer(file)
    
        # Pass the list as an argument into
        # the writerow()
        writer.writerow(snake_genes)
    
        # Close the file object
        file.close()



def save_score(score, generation):

    path = os.path.join(cwd, 'data/scores.csv')

    # make clean file at start of run
    if generation == 0:
        open(path, 'w').close()
    
    # Open our existing CSV file in append mode
    # Create a file object for this file
    with open(path, 'a', newline='') as file:
    
        # Pass this file object to csv.writer()
        # and get a writer object
        writer = csv.writer(file)
    
        row_data= np.hstack((generation, score))
        
        writer.writerow(row_data)
    
        # Close the file object
        file.close()

