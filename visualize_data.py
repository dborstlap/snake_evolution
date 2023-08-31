#################################################################################
# Name        : visualize_data.py
#
# Description : Functions used for visualizing results
#
# Name        : Dries Borstlap
# Student #   : 4648099
##################################################################################

# Imports
import matplotlib.pyplot as plt
import numpy as np
from save_data import load_dict_from_file
from scipy.optimize import curve_fit



# PLOT NODES OPTIMISATIOIN
def plot_nodes_optimisation():
    average_scores = []
    X = []
    Y = []
    X2 = []
    Y2 = []
    for node in range(1,20):
        av_scores = []
        av_scores2 = []
        for i in range(3):

            NODES = [6,node,node,4]
            filename='data/nn_research/scores_'+str(NODES)+'_i'+str(i)+'.csv'
            scores = np.genfromtxt(filename, delimiter=',')
            final_scores = np.average(scores[-1:], axis=0)
            average_score = final_scores[2]
            av_scores.append(average_score)

            filename2='data/nn_research/scores_'+str(NODES)+'_i'+str(i)+'_x2.csv'
            scores2 = np.genfromtxt(filename2, delimiter=',')
            final_scores2 = np.average(scores2[-1:], axis=0)
            average_score2 = final_scores2[2]
            av_scores2.append(average_score2)
        
        X.append(node)
        Y.append(np.average(av_scores))

        X2.append(node)
        Y2.append(np.average(av_scores2))

    plt.plot(X, Y, color='blue', label='pop_size=200, generations=100')
    plt.plot(X2, Y2, color='red', label='pop_size=400, generations=200')

    plt.xlabel('number of nodes')
    plt.ylabel('average score')
    plt.title('average scores after training with 3 hidden layers')
    plt.legend()

    plt.savefig('figures/nn_size_3hidden.png')
    plt.show()




# PLOT HYPERPARAMETER OPTIMISATION
def plot_hyperparameter_optimisation():
    X = []
    Y = []
    Z = []
    POPULATION_SIZE = 800
    for PARENT_FRACTION in np.linspace(0.01,0.5,30):
        for MUTATION_RATE in np.linspace(0,0.1,30):
            filename='data/mut_par_research/scores_mut'+str(MUTATION_RATE)+'_par'+str(PARENT_FRACTION)+'_pop'+str(POPULATION_SIZE)+'.csv'
            scores = np.genfromtxt(filename, delimiter=',')
            final_scores = np.average(scores[-1:], axis=0)
            x = PARENT_FRACTION
            y = MUTATION_RATE
            z = final_scores[2]
            X.append(x)
            Y.append(y)
            Z.append(z)
            # ax.scatter(x,y,z, cmap='Greens')

    scatter = plt.scatter(X, Y, c=Z, cmap='jet', vmin=0, vmax=6)
    colorbar = plt.colorbar(scatter, label='Value')
    colorbar.set_label('Average score', rotation=270, labelpad=15)

    plt.xlabel('PARENT_FRACTION')
    plt.ylabel('MUTATION_RATE')
    plt.title('Average score for given hyper-parameters \n for 50 generations, with population size 800')

    # Show the plot
    plt.savefig('figures/mut_par_800.png')
    plt.show()



# PLOT GENERATION PROGRESS
def plot_generation_progress():
    data_directory = 'data/final'
    scores = np.genfromtxt(data_directory + '/scores.csv', delimiter=',')
    hyper_parameters = load_dict_from_file(data_directory + '/hyper_parameters.json')

    generation = scores[:, 0]
    best_scores = scores[:, 1]
    average_scores = scores[:, 2]

    plt.rcParams['font.size'] = 15
    plt.figure(figsize=(6, 6))

    # plot
    plt.plot(generation, best_scores, label='best score')
    plt.plot(generation, average_scores, label='average score')

    # titles
    plt.title('Evolution of snake ai over generations')
    plt.xlabel("generation")
    plt.ylabel("score")
    plt.legend()
    plt.ylim(0,50)

    # make
    plt.tight_layout()
    plt.savefig('figures/run_final.png')
    plt.show()
    plt.close()




# Make plots 
plot_generation_progress()
