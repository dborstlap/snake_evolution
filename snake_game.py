#################################################################################
# Name        : snake_game.py
#
# Description : All functions and variables used for running the snake game.
#               Run this file to play snake manually
#
# Name        : Dries Borstlap
# Student #   : 4648099
##################################################################################

# Imports
import pygame
import random
from neural_net import get_nn_inputs, NeuralNet
import numpy as np
import cv2
import os

# Game constants
GRID_WIDTH = 10
GRID_HEIGHT = 10
GRID_SIZE = 30
WINDOW_WIDTH = GRID_WIDTH*GRID_SIZE
WINDOW_HEIGHT = GRID_HEIGHT*GRID_SIZE
FPS = 8

# Colors
BLACK = (0, 0, 0)
DARK_GREY = (10, 10, 10)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
RIGHT = (1, 0)
LEFT = (-1, 0)

DIRECTIONS = [UP, DOWN, RIGHT, LEFT]


# makes pygame quit when pressing the cross buttun or esc
def exitgame(running): 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    return running



def keyboard_snake_control(snake, food):
    # if event.type == pygame.KEYDOWN:
    #     if event.key == pygame.K_UP and snake.direction != DOWN:
    #         snake.direction = UP
    #     elif event.key == pygame.K_DOWN and snake.direction != UP:
    #         snake.direction = DOWN
    #     elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
    #         snake.direction = LEFT
    #     elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
    #         snake.direction = RIGHT

    keys=pygame.key.get_pressed()
    if keys[pygame.K_UP] and snake.direction != DOWN:
        snake.direction = UP
    elif keys[pygame.K_DOWN] and snake.direction != UP:
        snake.direction = DOWN
    elif keys[pygame.K_RIGHT] and snake.direction != LEFT:
        snake.direction = RIGHT
    elif keys[pygame.K_LEFT] and snake.direction != RIGHT:
        snake.direction = LEFT


# Hardcoded snake control function
def automatic_snake_control(snake, food):
    head_x, head_y = snake.segments[0]
    food_x, food_y = food.position

    # Determine the direction to move based on the relative positions of the head and food
    if head_x < food_x:
        snake.direction = RIGHT
    elif head_x > food_x:
        snake.direction = LEFT
    elif head_y < food_y:
        snake.direction = DOWN
    elif head_y > food_y:
        snake.direction = UP


# Neural net control function
def ai_snake_control(snake, food):

    # get inputs for neural net based on gameplay
    nn_inputs = get_nn_inputs(snake, food, [GRID_WIDTH, GRID_HEIGHT])

    # Do forward pass of neural net and get outputs
    output = snake.nn.forward(nn_inputs)

    # Transform outputs into a 'best' direction
    max_index = np.argmax(output)
    direction = DIRECTIONS[max_index]

    # Set new direction based on neural net outputs
    if direction == UP and snake.direction != DOWN:
        snake.direction = UP
    elif direction == DOWN and snake.direction != UP:
        snake.direction = DOWN
    elif direction == RIGHT and snake.direction != LEFT:
        snake.direction = RIGHT
    elif direction == LEFT and snake.direction != RIGHT:
        snake.direction = LEFT



# Snake game class. Defines game behaviour
class SnakeGame:
    def __init__(self, snake, max_age=np.inf, visualize=True, record=False, control_mode='ai_control'):
        self.visualize = visualize
        if self.visualize:
            pygame.init()
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            pygame.display.set_caption("Snake Game")
            self.clock = pygame.time.Clock()

            self.start_screen()

        self.record = record
        if self.record:
            self.frame_list = []

        self.food = Food()
        self.score = 0
        self.alive = True
        self.age = 0
        self.max_age = max_age
        self.snake = snake
        self.control_mode = control_mode
        

    def run(self):
        running = True
        while running:

            if self.visualize:
                # stop pygame if you click close button or press ESC
                running = exitgame(running)

                # draw everything in pygame
                self.draw()
                pygame.display.flip()
                self.clock.tick(FPS)

                if self.record:
                    frame = pygame.surfarray.array3d(self.screen)
                    self.frame_list.append(frame)


            # control directions based on arrow keys
            if self.control_mode == 'key_control':
                keyboard_snake_control(self.snake, self.food)

            # controlled by hardcoded function
            if self.control_mode == 'auto_control':
                automatic_snake_control(self.snake, self.food)

            # controlled by ai
            if self.control_mode == 'ai_control':
                ai_snake_control(self.snake, self.food)

            # update the snake position one step using the chosen algorithm
            self.update()

            # if snake is older then maximum age, it dies (so it does not run forever)
            if self.age > self.max_age:
                self.alive = False

            if not self.alive:
                running = False

                # visualize game over screen
                if self.visualize:
                    self.game_over()
                    if self.record:
                        frame = pygame.surfarray.array3d(self.screen)
                        self.frame_list.append(frame)

        # quit pygame
        if self.visualize:
            pygame.quit()

            if self.record:
                self.save_recording()

    # Move the snake and update game
    def update(self):
        self.age +=1
        self.snake.move(self.food)
        if self.snake.collides_with_food(self.food):
            self.score += 1
            self.food.generate_new_position(self.snake.segments)

        if self.snake.collides_with_self() or self.snake.collides_with_wall():
            self.alive = False
                
    # visualize game state on pygame screen
    def draw(self):

        # draw backround, snake and food
        self.screen.fill(BLACK)
        self.snake.draw(self.screen)
        self.food.draw(self.screen)

        # draw gridlines
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, BLACK, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, BLACK, (0, y), (WINDOW_WIDTH, y))

        # draw score
        font = pygame.font.SysFont(None, 24)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))


    # Start screen
    def start_screen(self):
        press2start = True

        font = pygame.font.Font(None, 30)
        start_screen_text = font.render("Press Space to Start", True, (255, 255, 255))
    
        # while loop for start screen
        while press2start:

            # Check if space bar is pressed. If so start game
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    press2start=False
            self.screen.blit(start_screen_text, (WINDOW_WIDTH // 2 - start_screen_text.get_width() // 2, WINDOW_HEIGHT // 2))
            pygame.display.flip()
            self.clock.tick(FPS)

    # Snake dies
    def game_over(self):
        font = pygame.font.SysFont(None, 48)
        game_over_text = font.render("Game Over", True, RED)
        self.screen.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, WINDOW_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)

    # Get current score
    def get_score(self):
        self.run()
        return self.score 
    
    # save recordings of gameplay to rewatch later
    def save_recording(self):
        pygame.surfarray.use_arraytype("numpy")
        output_file =os.path.join(os.getcwd(), 'video/snake_recorded.mp4')
        frame_rate = FPS
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        video_writer = cv2.VideoWriter(output_file, fourcc, frame_rate, (WINDOW_WIDTH, WINDOW_HEIGHT))
        for frame in self.frame_list:
            frame = np.rot90(frame)
            frame = np.flip(frame, 0)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            video_writer.write(frame_rgb)
        video_writer.release()
        print('video saved')
           
    

# Snake class, which defines one snake individual
class Snake:
    def __init__(self):
        self.direction = RIGHT
        self.segments = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.fitness = 0

    def set_genes(self, params):
        self.genes = params
        self.nn = NeuralNet()
        self.nn.set_params(params)
    
        # N_X, N_H1, N_H2, N_Y = self.nn.N_X, self.nn.N_H1, self.nn.N_H2, self.nn.N_Y
        # self.params = params

    def move(self, food):
        x, y = self.segments[0]
        dx, dy = self.direction
        new_segment = ((x + dx), (y + dy))
        self.segments.insert(0, new_segment)

        if not self.collides_with_food(food):
            self.segments.pop()

    def collides_with_food(self, food):
        head = self.segments[0]
        return head == food.position
    
    def collides_with_wall(self):
        head = self.segments[0]
        return (
            head[0] < 0 or head[0] >= GRID_WIDTH or
            head[1] < 0 or head[1] >= GRID_HEIGHT
        )

    def collides_with_self(self):
        head = self.segments[0]
        return head in self.segments[1:]

    def draw(self, screen):
        for segment in self.segments:
            x, y = segment
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, GREEN, rect)

# Food class
class Food:
    def __init__(self):
        self.position = self.generate_random_position()

    def generate_random_position(self):
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        return x, y

    def generate_new_position(self, snake_segments):
        possible_positions = [(x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)]
        available_positions = list(set(possible_positions) - set(snake_segments))
        self.position = random.choice(available_positions)

    def draw(self, screen):
        x, y = self.position
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, RED, rect)



# run a game once with given snake genes
def run_game(genes, visualize=True, record=True):
    snake = Snake()
    snake.set_genes(genes)
    game = SnakeGame(snake, visualize=visualize, record=record)
    game.run()




# Play the game manually by running this file
if __name__ == "__main__":
    snake = Snake()
    game = SnakeGame(snake=snake, control_mode='key_control')
    game.run()


