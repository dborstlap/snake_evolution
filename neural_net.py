#################################################################################
# Name        : neural_net.py
#
# Description : All functions used for making the neural net based snake control work
#
# Name        : Dries Borstlap
# Student #   : 4648099
##################################################################################

# IMPORTS
import numpy as np


# Define global variable 'NODES'. This represents the amount of nodes in each layer of the neural net
NODES = [6,5,4]

# Make function that can change the global variable 'NODES'
def change_nodes(x):
    global NODES 
    NODES = x

# Define some activation functions
def sigmoid(x):
    return 1 / (1 + np.exp(-x))
def relu(x):
    return np.maximum(0, x)

# Choose which activation function to use
ACTIVATION_FUNCTION = relu



# Define a linear layer class, which is a fully connected linear layer of a neural net. Combine layers to get a NN.
class Linear:
    def __init__(self, n_inputs, n_outputs):

        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.weights = np.zeros((n_outputs, n_inputs))
        self.bias = np.zeros(n_outputs)

        self.n_weights = len(self.weights.flatten())
        self.n_bias = len(self.bias.flatten())

    # Perform a forward pass of the layer
    def forward(self, X):
        Y = np.dot(self.weights, X) + self.bias
        return Y
    
    # set weights of this layer
    def set_weights(self, weights):
        self.weights = weights

    # set biases of this layer
    def set_bias(self, bias):
        self.bias = bias

    # return the weights of this layer
    def get_weights(self):
        return self.weights
    
    # return the biases of this layer
    def get_bias(self):
        return self.bias


# Define neural net class that combines multiple linear layers to form a NN.
class NeuralNet:
    def __init__(self):

        self.nodes = NODES
        self.n_layers = len(self.nodes)
        self.nn = []

        # create a not-initialized NN with linear layers defined by 'NODES'
        for i in range(1,self.n_layers):
            n_inputs = self.nodes[i-1]
            n_outputs = self.nodes[i]

            layer = Linear(n_inputs, n_outputs)
            self.nn.append(layer)

        # total number of parameters
        self.n_params = sum([layer.n_weights + layer.n_bias for layer in self.nn])

    # set parameters (weights and biases of all layers) of the neural network.
    def set_params(self, params):

        self.params = params

        for layer in self.nn:
            n_inputs = layer.n_inputs
            n_outputs = layer.n_outputs

            n_weights = n_inputs * n_outputs
            n_bias = n_outputs

            new_weights = params[:n_weights].reshape(n_outputs, n_inputs)
            params = params[n_weights:]
            layer.weights = new_weights

            new_bias = params[:n_bias]
            params = params[n_bias:]
            layer.bias = new_bias

    # get parameters of neural network
    def get_params(self):
        return self.params

    # perform a forward pass of the whole neural net
    def forward(self, X):

        for layer in self.nn:
            X = ACTIVATION_FUNCTION(layer.forward(X))

        return X


# Function to check which sqaures in grid are occupied (snake body and edges)
def check_obstacles(segments, grid_size):
    head = segments[0]
    obstacles = [False, False, False, False]  # [UP, DOWN, RIGHT, LEFT]

    # Check up side
    up_block = (head[0], (head[1] - 1))
    if up_block in segments or up_block[1] < 0:
        obstacles[0] = True

    # Check down side
    down_block = (head[0], (head[1] + 1))
    if down_block in segments or down_block[1] > grid_size[1]:
        obstacles[1] = True

    # Check right side
    right_block = ((head[0] + 1), head[1])
    if right_block in segments or right_block[0] >= grid_size[0]:
        obstacles[2] = True

    # Check left side
    left_block = ((head[0] - 1), head[1])
    if left_block in segments or left_block[0] < 0:
        obstacles[3] = True

    return obstacles


# Get the inputs for the neural network from the game
def get_nn_inputs(snake, food, grid_size):

    # Get the position of the snake's head
    head_x, head_y = snake.segments[0]

    # Get the position of the food
    food_x, food_y = food.position

    # Distance to food in x and y
    d_food_x = food_x - head_x
    d_food_y = food_y - head_y

    # Check if the blocks next to the snake head are occupied or not
    obstacles = check_obstacles(snake.segments, grid_size)

    # define neural network
    nn_inputs = [d_food_x, d_food_y, obstacles[0], obstacles[1], obstacles[2], obstacles[3]]

    return nn_inputs
