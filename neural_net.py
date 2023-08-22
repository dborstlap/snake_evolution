import numpy as np


NODES = [6,5,4]
def change_nodes(x):
    global NODES 
    NODES = [6,5,4]

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def relu(x):
    return np.maximum(0, x)


ACTIVATION_FUNCTION = relu





class Linear:
    def __init__(self, n_inputs, n_outputs):

        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.weights = np.zeros((n_outputs, n_inputs))
        self.bias = np.zeros(n_outputs)

        self.n_weights = len(self.weights.flatten())
        self.n_bias = len(self.bias.flatten())

    def forward(self, X):
        Y = np.dot(self.weights, X) + self.bias
        return Y
    
    def set_weights(self, weights):
        self.weights = weights

    def set_bias(self, bias):
        self.bias = bias

    def get_weights(self):
        return self.weights
    
    def get_bias(self):
        return self.bias
    

# def calculate_n_params(nodes):
#     nn_example = NeuralNet(nodes)
#     return nn_example.n_params


class NeuralNet:
    def __init__(self):

        self.nodes = NODES
        self.n_layers = len(self.nodes)
        

        self.nn = []
        for i in range(1,self.n_layers):
            n_inputs = self.nodes[i-1]
            n_outputs = self.nodes[i]

            layer = Linear(n_inputs, n_outputs)

            self.nn.append(layer)

        # self.n_params_total = 0
        # for layer in self.nn:
        #     self.n_params_total += layer.n_weights + layer.n_bias

        self.n_params = sum([layer.n_weights + layer.n_bias for layer in self.nn])

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

    def get_params(self):
        return self.params


    def forward(self, X):

        for layer in self.nn:
            X = ACTIVATION_FUNCTION(layer.forward(X))

        return X





# class NeuralNetwork:
#     def __init__(self, params):
#         self.set_params(params)

#     def forward(self, x):
#         # hidden1 = relu(np.dot(self.weights1, x) + self.bias1)
#         # hidden2 = relu(np.dot(self.weights2, hidden1) + self.bias2)
#         output = relu(np.dot(self.weights1, x) + self.bias1)
#         return output
    
#     # get all weights and biases in list. These are optimisation variables
#     def get_params(self):
#         weights1 = self.weights1.flatten()

#         params = np.hstack([weights1])
#         return params
    
#     def set_params(self, params):
#         params = np.array(params)
#         self.weights1 = params.reshape((N_Y, N_X))

#         self.bias1 = 0
#         self.bias2 = 0
#         self.bias3 = 0



# class NeuralNetwork:
#     def __init__(self, params):
#         self.N_X = N_X
#         self.N_H = N_H
#         self.N_Y = N_Y
#         self.num_weights = NUM_WEIGHTS

#         # self.weights1 = np.random.randn(N_H1, N_X)
#         # self.bias1 = 0 # np.random.randn(N_H1)
#         # self.weights2 = np.random.randn(N_H2, N_H1)
#         # self.bias2 = 0 # np.random.randn(N_H2)
#         # self.weights3 = np.random.randn(N_Y, N_H2)
#         # self.bias3 = 0 # np.random.randn(N_Y)

#         self.set_params(params)


#     def forward(self, x):
#         hidden1 = relu(np.dot(self.weights1, x) + self.bias1)
#         # hidden2 = relu(np.dot(self.weights2, hidden1) + self.bias2)
#         output = relu(np.dot(self.weights3, hidden1) + self.bias3)
#         return output
    
#     # get all weights and biases in list. These are optimisation variables
#     def get_params(self):
#         weights1 = self.weights1.flatten()
#         weights2 = self.weights2.flatten()
#         weights3 = self.weights3.flatten()

#         params = np.hstack([weights1, weights2, weights3])
#         return params
    
#     def set_params(self, params):
#         params = np.array(params)
#         self.weights1 = params[ : N_X*N_H1].reshape((N_H1, N_X))
#         self.weights2 = params[N_X*N_H1 : N_X*N_H1 + N_H2*N_H1].reshape((N_H2, N_H1))
#         self.weights3 = params[N_X*N_H1 + N_H2*N_H1 : ].reshape((N_Y, N_H2))

#         self.bias1 = 0
#         self.bias2 = 0
#         self.bias3 = 0



# Create an instance of the neural network
# model = NeuralNetwork()
# input_array = np.random.randn(N_X)
# output_array = model.forward(input_array)
# print(output_array)


# def check_obstacles(segments, direction, grid_size):
#     head = segments[0]
#     dx, dy = direction

#     # Calculate the positions of the blocks to the left, front, and right
#     left_block = ((head[0] - dy) % grid_size, (head[1] + dx) % grid_size)
#     front_block = ((head[0] + dx) % grid_size, (head[1] + dy) % grid_size)
#     right_block = ((head[0] + dy) % grid_size, (head[1] - dx) % grid_size)

#     # Check if the blocks are occupied by snake segments
#     left_occupied = left_block in segments
#     front_occupied = front_block in segments
#     right_occupied = right_block in segments

#     return left_occupied, front_occupied, right_occupied


# def get_nn_inputs(snake, food):
#     # Get the current direction of the snake's head
#     head_direction = snake.direction

#     # Get the position of the snake's head
#     head_x, head_y = snake.segments[0]

#     # Get the position of the food
#     food_x, food_y = food.position

#     # Calculate the angle between the snake's head and the food
#     angle_to_food = math.atan2(food_y - head_y, food_x - head_x) - math.atan2(head_direction[0],head_direction[1])

#     # Check if the block on the right, left, and front of the snake is occupied or not
#     right_obstacle = snake.is_collision(head_x + 1, head_y)
#     left_obstacle = snake.is_collision(head_x - 1, head_y)
#     front_obstacle = snake.is_collision(head_x, head_y + 1)

#     nn_inputs = [angle_to_food, right_obstacle, left_obstacle, front_obstacle]

#     return nn_inputs




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

    nn_inputs = [d_food_x, d_food_y, obstacles[0], obstacles[1], obstacles[2], obstacles[3]]

    return nn_inputs



# pop_size = 3
# num_weights = N_X*N_H1 + N_H1*N_H2 + N_H2*N_Y
# pop_shape = num_weights*pop_size

# params = np.random.uniform(-1, 1, size = num_weights)

# nn = NeuralNetwork(params)
# inputs = [1,2,3,4, 5, 6]
# y = nn.forward(inputs)
# new_params = nn.get_params()
# nn.set_params(new_params)
# y2 = nn.forward(inputs)

# print(y, y2)
