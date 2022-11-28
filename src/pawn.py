# Class of a pawn
class Pawn:
    # Definition of the constructor
    def __init__(self, x, y, color):
        # We originally put the coordinates of the pawn and its color according to them passed into parameters
        self.x = x
        self.y = y
        self.color = color

    # We can move a pawn into a direction and a number of grids
    def move(self, direction, number):
        if direction == 1:
            self.x += number
        elif direction == 0:
            self.y += number
