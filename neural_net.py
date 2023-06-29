import numpy as np


N_X = 6
N_H1 = 5
N_H2 = 5
N_Y = 4

NUM_WEIGHTS = N_X*N_H1 + N_H1*N_H2 + N_H2*N_Y

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def relu(x):
    return np.maximum(0, x)

class NeuralNetwork:
    def __init__(self, params):
        self.N_X = N_X
        self.N_H1 = N_H1
        self.N_H2 = N_H2
        self.N_Y = N_Y
        self.num_weights = NUM_WEIGHTS

        # self.weights1 = np.random.randn(N_H1, N_X)
        # self.bias1 = 0 # np.random.randn(N_H1)
        # self.weights2 = np.random.randn(N_H2, N_H1)
        # self.bias2 = 0 # np.random.randn(N_H2)
        # self.weights3 = np.random.randn(N_Y, N_H2)
        # self.bias3 = 0 # np.random.randn(N_Y)

        self.set_params(params)


    def forward(self, x):
        hidden1 = relu(np.dot(self.weights1, x) + self.bias1)
        hidden2 = relu(np.dot(self.weights2, hidden1) + self.bias2)
        output = relu(np.dot(self.weights3, hidden2) + self.bias3)
        return output
    
    # get all weights and biases in list. These are optimisation variables
    def get_params(self):
        weights1 = self.weights1.flatten()
        weights2 = self.weights2.flatten()
        weights3 = self.weights3.flatten()

        params = np.hstack([weights1, weights2, weights3])
        return params
    
    def set_params(self, params):
        params = np.array(params)
        self.weights1 = params[ : N_X*N_H1].reshape((N_H1, N_X))
        self.weights2 = params[N_X*N_H1 : N_X*N_H1 + N_H2*N_H1].reshape((N_H2, N_H1))
        self.weights3 = params[N_X*N_H1 + N_H2*N_H1 : ].reshape((N_Y, N_H2))

        self.bias1 = 0
        self.bias2 = 0
        self.bias3 = 0



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
