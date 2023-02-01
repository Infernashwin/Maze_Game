'''
Program Name: Maze_Game_Final.py
Programmer Name: Ashwin Mayurathan
Date: 06-17-2022
Description: This is a simple maze game where the player's objective is to reach the flag located at the bottom right corner of the maze.
             The Maze portion of the code is randomly generated. The player moves around using the arrow keys, and can click "s" to ge the
             solution for the maze. 
'''
#Import Statements
import pygame
from pygame.locals import*
from Tiles import *
from pygame import mixer
import time
import random

#Declare Constants
WIDTH = 440
HEIGHT = 440
FPS = 30
WHITE = (255, 255, 255)
GREEN = (0, 255, 0,)
BLUE = (0, 0, 255)
YELLOW = (255 ,255 ,0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

#Pygame Stuff
pygame.init()
pygame.mixer.init()

#Creates the screen 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")
clock = pygame.time.Clock()

#Declares Variables
x = 0                    
y = 0                    
tile_width = 20                   
grid = []
grid_list = []
visited = []
stack = []
solution = {}
wrong_moves = []

#Builds the grid
def build_grid(x, y, w):
    #Makes the grid 20 by 20
    for i in range(20):
        x = 20                                                            
        y += 20
        #Creates a row
        row = []   

        #Draws the grid
        for j in range(20):
            pygame.draw.line(screen, WHITE, [x, y], [x + w, y])          
            pygame.draw.line(screen, WHITE, [x + w, y], [x + w, y + w])   
            pygame.draw.line(screen, WHITE, [x + w, y + w], [x, y + w])   
            pygame.draw.line(screen, WHITE, [x, y + w], [x, y])           
            grid.append((x,y))
            #Fills the row with tiles
            row.append(Tile())                                            
            x = x + 20   
        
        #Fills the grid list with rows of tiles
        grid_list.append(row)

#Breaks into the tile above the grid
def clear_up(x, y):
    pygame.draw.rect(screen, BLUE, (x + 1, y - tile_width + 1, 19, 39), 0) 

#Breaks into the tile below the grid
def clear_down(x, y):
    pygame.draw.rect(screen, BLUE, (x +  1, y + 1, 19, 39), 0)

#Breaks into the tile left of the gird
def clear_left(x, y):
    pygame.draw.rect(screen, BLUE, (x - tile_width +1, y +1, 39, 19), 0)

#Breaks into the tile right of the grid
def clear_right(x, y):
    pygame.draw.rect(screen, BLUE, (x +1, y +1, 39, 19), 0)            
   
#Makes a square as the direction needed to go to solve the maze
def solution_cell(x,y):
    pygame.draw.rect(screen, YELLOW, (x+8, y+8, 5, 5), 0)             

#Carves out the maze from a grid
def carve_out_maze(x,y):                                            
    stack.append((x,y))                                            
    visited.append((x,y)) 

    while (len(stack) > 0):                                          
        cell = [] 
        #Checks if it is possible to go in a certain direction for every direction                                                 
        if (((x + tile_width, y) not in visited) and ((x + tile_width, y) in grid)):       
            cell.append("right")                                   

        if (((x - tile_width, y) not in visited) and ((x - tile_width, y) in grid)):       
            cell.append("left")

        if (((x , y + tile_width) not in visited) and ((x , y + tile_width) in grid)):     
            cell.append("down")

        if (((x, y - tile_width) not in visited) and ((x , y - tile_width) in grid)):      
            cell.append("up")

        #If a cell can be chosen to travel to choose 1 of the possible cells
        if (len(cell) > 0):                                          
            cell_chosen = (random.choice(cell))                    

            #Allows the user to move that direction in that particular cell
            if (cell_chosen == "right"):                             
                clear_right(x, y)                                   
                grid_list[x//20-1][y//20-1].open_right()
                solution[(x + tile_width, y)] = x, y                        
                x = x + tile_width                                          
                visited.append((x, y))                              
                stack.append((x, y))                                
                grid_list[x//20-1][y//20-1].open_left()

            elif (cell_chosen == "left"):
                clear_left(x, y)
                grid_list[x//20-1][y//20-1].open_left()
                solution[(x - tile_width, y)] = x, y
                x = x - tile_width
                visited.append((x, y))
                stack.append((x, y))
                grid_list[x//20-1][y//20-1].open_right()

            elif (cell_chosen == "down"):
                clear_down(x, y)
                grid_list[x//20-1][y//20-1].open_down()
                solution[(x , y + tile_width)] = x, y
                y = y + tile_width
                visited.append((x, y))
                stack.append((x, y))
                grid_list[x//20-1][y//20-1].open_up()

            elif (cell_chosen == "up"):
                clear_up(x, y)
                grid_list[x//20-1][y//20-1].open_up()
                solution[(x , y - tile_width)] = x, y
                y = y - tile_width
                visited.append((x, y))
                stack.append((x, y))
                grid_list[x//20-1][y//20-1].open_down()
 
        #Else remove the cell from the stack (cells to be looked at)
        else:
            x, y = stack.pop()

#Trims the solution list to only have the direct path stored
def trim_solution(solution):
    #Solves from the end to the begining
    x = 400
    y = 400
    trim = {}

    while ((x, y) != (20,20)):
        trim[x, y] = solution[x, y]                                  
        x, y = solution[x, y] 

    solution = trim.copy()      
    return solution                           

#Plots the route from the player to the flag (End)
def plot_route_back(x,y,player_x,player_y, wrong_moves,solution):
    solution_cell(x, y) #Marks tile as the solution

    #If the player is on the right path just draw from their co-ordinate to the end
    if (((player_x,player_y) in solution.keys()) or ((player_x, player_y) == (20,20))):                                    
       #Keep drawing until you are at the player's co-ordinate
        while ((x, y) != (player_x,player_y)):                                     
            x, y = solution[x, y]                                    
            solution_cell(x, y) 

    #If the player made a wrong move
    else:
        #Use information of the wrong moves the user had taken to find the path back to the solution
        corrections = wrong_moves.copy()
        corrections.reverse()

        #Marks the path back to the solution
        for direction in corrections:
            if (direction == "up"):
                player_y -= 20

            if (direction == "down"):
                player_y += 20

            if (direction == "left"):
                player_x -= 20

            if (direction == "right"):
                player_x += 20

            solution_cell(player_x, player_y)

        #Recalls the function, this time at a point connected to the solution path
        plot_route_back(x, y, player_x, player_y , wrong_moves, solution)

#The main function
def main(): 
    running = True
    main_menu()
    while (running):
        running = game()

#Promts the user to play again
def play_again():
    #Generating text on the window
    font = pygame.font.Font('freesansbold.ttf', 23)
    text_a = font.render('CLICK SPACE TO PLAY AGAIN', True, WHITE, BLACK)
    text_b = font.render('CLICK ESCAPE TO CLOSE WINDOW', True, WHITE, BLACK)   
    textRect_a = text_a.get_rect()
    textRect_a.center = (WIDTH // 2, 175)
    textRect_b = text_b.get_rect()
    textRect_b.center = (WIDTH // 2, 225)
    running = True
    screen.fill(BLACK)
    screen.blit(text_a, textRect_a)
    screen.blit(text_b, textRect_b)

    #While window should be running
    while (running):

        #If something happens
        for event in pygame.event.get():
    
            #Lets player "x" out of the game
            if (event.type == pygame.QUIT):
                pygame.quit()
                quit()

            #If player clicked a button
            if (event.type == pygame.KEYDOWN):

                #If player clicked space let them play again
                if (event.key == pygame.K_SPACE):
                    continue_game = True
                    running = False
                
                #If player clicked escape close the game
                if (event.key == pygame.K_ESCAPE):
                    running = False
                    continue_game = False
                    pygame.quit()
                    quit()

        pygame.display.update()  
        
    return continue_game

#The actual game
def game(): 
    #Resets the global variables
    del grid[:]
    del grid_list[:]
    del visited[:]
    del stack[:]
    solution.clear()
    
    #Makes the screen black
    screen.fill(BLACK) 

    #Builds the actual maze, player, flag, adds music, all of the fun stuff.   
    x, y = 20, 20                     
    build_grid(40, 0, 20)             
    carve_out_maze(x,y)    
    player_right = pygame.image.load("player_right.png")
    player_left = pygame.image.load("player_left.png")
    player = player_right
    flag = pygame.image.load("flag.png")
    pygame.display.update()
    mixer.music.load("HoliznaCC0 - Day Dreams.mp3")
    mixer.music.set_volume(0.2)
    mixer.music.play()
    running = True

    #Stores the trimmed solution
    solu = trim_solution(solution)

    #Initializes Variables
    tile_x = 0
    tile_y = 0
    play_x = 26
    play_y = 22
    size = 16
    wrong_moves = []

    #Draws the flag
    screen.blit(flag, (402, 402))

    #While the game should run
    while (running):
        #Makes the game run smoother
        clock.tick(FPS)
        #If something happens
        for event in pygame.event.get():

            #Lets the player 'x' out
            if (event.type == pygame.QUIT):
                running = False
        
            #If a key is clicked
            if (event.type == pygame.KEYDOWN):

                #Lets the user move in a direction if it is a valid move
                if ((event.key == pygame.K_LEFT) and (grid_list[tile_x][tile_y].check_left())):
                    pygame.draw.rect(screen, BLUE, (play_x, play_y, 8, size))
                    play_x -= tile_width
                    tile_x -= 1
                    player = player_left

                    #If the player made a mistake
                    if ((play_x-6, play_y-2) not in solu.keys()):
                        #If its is the first mistake make sure to record it
                        if (wrong_moves == []):
                            wrong_moves.append("right")

                        #Otherwise make sure they did not counter their last move
                        else:
                            #If countered then remove the countered movement and don't add anything
                            if (wrong_moves[-1] == "left"):
                                wrong_moves.pop()
                            #Else add the movement to the list
                            else:
                                wrong_moves.append("right")

                if event.key == pygame.K_RIGHT and grid_list[tile_x][tile_y].check_right():
                    pygame.draw.rect(screen, BLUE, (play_x, play_y, 8, size))
                    play_x += tile_width
                    tile_x += 1
                    player = player_right

                    #Same concepts as before, just for the right movement
                    if ((play_x-6, play_y-2) not in solu.keys()):

                        if (wrong_moves == []):
                            wrong_moves.append("left")

                        else:
                            if (wrong_moves[-1] == "right"):
                                wrong_moves.pop()

                            else:
                                wrong_moves.append("left")

                if ((event.key == pygame.K_DOWN) and (grid_list[tile_x][tile_y].check_down())):
                    pygame.draw.rect(screen, BLUE, (play_x, play_y, 8, size))
                    play_y += tile_width
                    tile_y += 1
                    #Same as before but for the down movement
                    if ((play_x-6, play_y-2) not in solu.keys()):

                        if (wrong_moves == []):
                            wrong_moves.append("up")

                        else:
                            if (wrong_moves[-1] == "down"):
                                wrong_moves.pop()

                            else:
                                wrong_moves.append("up")
            
                if ((event.key == pygame.K_UP) and (grid_list[tile_x][tile_y].check_up())):
                    pygame.draw.rect(screen, BLUE, (play_x, play_y, 8, size))
                    play_y -= tile_width
                    tile_y -= 1
                    if (play_x-6, play_y-2) not in solu.keys():
                        if wrong_moves == []:
                            wrong_moves.append("down")
                        else:
                            if wrong_moves[-1] == "up":
                                wrong_moves.pop()
                            else:
                                wrong_moves.append("down")

                #If player is on the right path reset wrong moves to make sure it is empty
                if ((play_x-6, play_y-2) in solu.keys()):
                    wrong_moves = []

                #Shows the solution if "s" is clicked
                if (event.key == pygame.K_s):
                    plot_route_back(400,400, play_x-6, play_y-2, wrong_moves, solu)
        
        #Draws the player
        screen.blit(player, (play_x, play_y))

        #Updates the screen
        pygame.display.update()

        #Checks if the player has won.
        if (tile_x == 19 and tile_y == 19):
            time.sleep(2)
            return play_again()

#Loads the starting menu
def main_menu():
    #Sets up the text on the menu
    font_big = pygame.font.Font('freesansbold.ttf', 64)
    font_small = pygame.font.Font('freesansbold.ttf', 32)
    title = font_big.render('MAZE GAME', True, WHITE, BLACK)
    text = font_small.render('CLICK SPACE TO BEGIN', True, WHITE, BLACK)  
    textRect = text.get_rect()
    titleRect = title.get_rect()
    textRect.center = (WIDTH // 2, 350)
    titleRect.center = (WIDTH//2, 125)
    running = True
    screen.fill(BLACK)
    screen.blit(text, textRect)
    screen.blit(title, titleRect)

    #While the menu should run
    while (running):

        #If something happens
        for event in pygame.event.get():

            #Lets the player 'x' out
            if (event.type == pygame.QUIT):
                pygame.quit()
                quit()

            #If the player clicks space proceed to the instructions
            if (event.type == pygame.KEYDOWN):

                if (event.key == pygame.K_SPACE):
                    running = instructions()

        #Updates the screen
        pygame.display.update()  
          
#Shows the player the instructions for the game                                     
def instructions():
    #Generates the text for the screen
    font = pygame.font.Font('freesansbold.ttf', 20) 
    text_a = font.render('CLICK SPACE TO START', True, WHITE, BLACK)  
    text_b = font.render('Use arrow keys to move', True, WHITE, BLACK)
    text_c = font.render('Try to find the red flag', True, WHITE, BLACK)
    text_d = font.render('If you are lost click S', True, WHITE, BLACK)  
    text_a_rect = text_a.get_rect()
    text_b_rect = text_b.get_rect()
    text_c_rect = text_c.get_rect()
    text_d_rect = text_d.get_rect()
    text_a_rect.center = (200, 350)
    text_b_rect.center = (200, 50)
    text_c_rect.center = (200, 100)
    text_d_rect.center = (200, 150) 
    running = True
    screen.fill(BLACK)
    screen.blit(text_a, text_a_rect)
    screen.blit(text_b, text_b_rect)
    screen.blit(text_c, text_c_rect)
    screen.blit(text_d, text_d_rect)

    #While the window should be running
    while (running):

        #If something happens
        for event in pygame.event.get():
    
            #Let's the user 'x' out
            if (event.type == pygame.QUIT):
                pygame.quit()
                quit()

            #If a button is clicked
            if (event.type == pygame.KEYDOWN):

                #If the user clicks space then proceed to the game
                if (event.key == pygame.K_SPACE):
                    running = False

        #Updates the window
        pygame.display.update() 

    #To make the code move on to the game when it goes back to where instructions() was called
    return False

main()