#################################################################################
# Name        : snake_game_v1.py
#
# Description : Initial attempt to make a snake game that could be played by a human
#               Is outdated and not used anymore
#
# Name        : Dries Borstlap
# Student #   : 4648099
##################################################################################









##############################---SNAKE---######################################

# IMPORTS
import pygame as pg
from colour import Color
import random as rd
pg.init()

# -------------------VARIABLES----------------------------
speed = 7               # speed of the snake
grid = [10,10]          # pixels in x and y direction respectively

blocksize = 50          # size of the blocks
edgedeath = True        # you will die colliding with edges


class Colors:
    white = (255,255,255)
    grey = (150,150,150)
    black = (0,0,0)
    red = (255,0,0)
    orange = (255,153,51)
    yellow = (255,255,0)
    green = (0,255,0)
    blue = (0,0,255)
    darkblue = (10,10,50)
    purple = (0,0,0)
    pink = (255,0,255)

    def color(color_name):
        return getattr(Colors, color_name)

gridcolor = Colors.color("black")        # color of gridlines
backgroundcolor = Colors.color("black")  # color of background
snakecolor = Colors.color("green")       # color of snake
foodcolor = Colors.color("red")         # color of blocks that snake needs to eat


#----------------------- FUNCTIONS --------------------------------



def direction(direc): #direc is direction of snake, controlled by arrow key presses
    keys=pg.key.get_pressed()
    if keys[pg.K_UP] or keys[pg.K_w]:
        if direc != 'down':
            direc='up'
    if keys[pg.K_RIGHT] or keys[pg.K_d]:
        if direc != 'left':
            direc = 'right'
    if keys[pg.K_DOWN] or keys[pg.K_s]:
        if direc != 'up':   
            direc = 'down'
    if keys[pg.K_LEFT] or keys[pg.K_a]:
        if direc != 'right':
            direc = 'left'
    return direc


def movesnake(snake0,direc,grid): #code to make snake move in direction of direc
    if direc == 'right':
        if snake0[0] < grid[0]-1:
            snake0[0] += 1
        else:
            snake0[0] = 0
    if direc == 'left':
        if snake0[0] > 0:
            snake0[0] -= 1
        else:
            snake0[0] = grid[0]-1
    if direc == 'down':
        if snake0[1] < grid[1]-1:
            snake0[1] +=1
        else:
            snake0[1] = 0
    if direc == 'up':
        if snake0[1] > 0:
            snake0[1] -= 1
        else:
            snake0[1] = grid[1]-1
    return snake0


def foodlocation(food,loc,xpixels,ypixels): # makes blocks on screen for the snake to eat
    if food == False:
        xloc = rd.randint(0,xpixels-1)
        yloc = rd.randint(0,ypixels-1)
        loc = (xloc,yloc)
        food = True
        return food,loc
    else:
        return food,loc


def death(snake,edgedeath,direc,grid): # checks if the snake died by colliding with itself, or with the wall if edgedeath is true
    dead = False
    for s in snake[1:]:
        if snake[0] == s:
            dead = True
    if edgedeath == True:
        if direc == 'right' and snake[0][0] == grid[0]-1:
            dead = True
        if direc == 'left' and snake[0][0] == 0:
            dead = True
        if direc == 'down' and snake[0][1] == grid[1]-1:
            dead = True
        if direc == 'up' and snake[0][1] == 0:
            dead = True
    return dead


def initgame(playing): # enables game to start by pressing enter, without having to reload the whole thing
    keys=pg.key.get_pressed()
    if keys[pg.K_RETURN]: # enter key
        playing=True
        return playing


def exitgame(running): # makes pygame quit when pressing the cross buttun or esc.
    keys=pg.key.get_pressed()
    if keys[pg.K_ESCAPE]: # escape key
        running=False
    for event in pg.event.get():
        if event.type==pg.QUIT: #close window button
            running=False
    return running


# -----------------------------------------------------------

# size of the screen
screenwidth = int(grid[0]*blocksize)
screenheight = int(grid[1]*blocksize)

# initialize pagame screen
scr = pg.display.set_mode((screenwidth,screenheight))                  

# create the grid
blocks = []  
for y in range(grid[1]):
    blockrow = []
    for x in range(grid[0]):
        block = (x*blocksize, y*blocksize, blocksize, blocksize)
        blockrow.append(block)
    blocks.append(blockrow)

# PLAY
running=True
playing=False
while running:
    # START screen
    if not playing: 
        playing=initgame(playing)
        scr.fill(backgroundcolor)
        
        if playing:
            # START POSITION
            snake = [[rd.randint(0,grid[0]-1), rd.randint(0,grid[1]-1)]]
            direc = 'none'
            food,loc = True,(rd.randint(0,grid[0]-1), rd.randint(0,grid[1]-1))
            tprev = pg.time.get_ticks()*0.001 # check the time
            time = 0
            
            
    # PLAY game loop        
    if playing:    
        t=pg.time.get_ticks()*0.001
        dt=t-tprev
        tprev=t
        time += dt
     
        direc =  direction(direc)
    
        if time >= 1/speed:
            time = 0
            
            dead = death(snake,edgedeath,direc,grid)
            if dead:
                playing = False
           
            
            scr.fill(backgroundcolor)
            
            snake0 = [snake[0][0], snake[0][1]]
            snake0 = movesnake(snake0, direc, grid)

            
            if loc == (snake[0][0], snake[0][1]):
                food = False
                snake = [snake0] + snake
            else:
                snake = [snake0] + snake[:-1]
                
     
            food,loc = foodlocation(food, loc, grid[0], grid[1])
            scr.fill(foodcolor,(loc[0]*blocksize, loc[1]*blocksize, blocksize,blocksize))
           
            for l in range(len(snake)):
                scr.fill(snakecolor,blocks[snake[l][1]][snake[l][0]])
            
            for blockrow in blocks:
                for block in blockrow:
                    pg.draw.rect(scr, gridcolor, block, 1) 
                
    pg.display.flip()
    
    running = exitgame(running)
pg.quit() #close window










