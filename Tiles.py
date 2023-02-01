'''
Program Name: Tiles.py
Programmer Name: Ashwin Mayurathan
Date: 06-17-2022
Description: This is a code which contains the tile object for the code Maze_Game_Final.py.
             A tile represents an area where the player can be located, and the attributes 
             of the tile object determines the direction you are able to move from a particular
             tile.
'''
# Creates Object Tile
class Tile():

    #Initializes the tile be closed off at all borders
    def __init__(self) -> None:
        self.left = False
        self.right = False
        self.up = False
        self.down = False

    #Allows movement left
    def open_left(self):
        self.left = True

    #Allows movement right
    def open_right(self):
        self.right = True

    #Allows movement up
    def open_up(self):
        self.up = True

    #Allows movement down
    def open_down(self):
        self.down = True

    #Checks if possible to move left
    def check_left(self):
        return self.left

    #Checks if possible to move right
    def check_right(self):
        return self.right

    #Checks if possible to move up
    def check_up(self):
        return self.up

    #Checks if possible to move down
    def check_down(self):
        return self.down

    #Shows information in string layout for testing
    def show_tile(self):
        return f'Left: {self.left}, Right: {self.right}, Up: {self.up}, Down: {self.down}'
