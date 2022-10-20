# Class of a pawn
class Pawn:
    x = 0
    y = 0
    z = 0
    color = ''

    # Definition of the constructor
    def __init__(self, x, y, z, color):
        # We originally put the coordinates of the pawn and its color according to them passed into parameters
        self.x = x
        self.y = y
        self.z = z
        self.color = color

        # print(x, y, color)

    # We can move a pawn into a direction and a number of grids
    def move(self, direction, number):
        if direction == 1:
            self.x += number
        elif direction == 0:
            self.y += number
