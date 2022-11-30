import math

import pawn


class Model_Player:
    pawns = []
    towers = []
    winner = "nobody"
    turn = "white"

    clicked = False
    ref = None

    def __init__(self, ref_controller):
        self.ref_controller = ref_controller
        self.temp_click_j = None
        self.temp_click_i = None
        print("New Model!")

        # Creating the towers of white pawns
        for i in range(3):
            if i == 3:
                break
            for y in range(2):
                self.pawns.append(pawn.Pawn(0, i, 'white'))
            self.towers.append(self.pawns)
            self.pawns = []

        # Creating the towers of black pawns
        for i in range(3):
            if i == 3:
                break
            for y in range(2):
                self.pawns.append(pawn.Pawn(2, i, 'black'))
            self.towers.append(self.pawns)
            self.pawns = []

    def __del__(self):
        self.pawns.clear()
        self.towers.clear()

    def get_winner(self):
        if self.winner != "nobody":
            return self.winner

    def is_winner(self):
        if self.winner != "nobody":
            return True
        return False

    def decide_type_of_moving(self, j, i, number_of_moving):
        # Searching for if a tower already exists on the new position
        for tower in self.towers:
            # If this is the case,
            if j == tower[0].x and i == tower[0].y:
                self.move_to(number_of_moving, j, i, tower, False)
                return

        # No tower exists, the new position is free
        self.move_to(number_of_moving, j, i, self.towers, True)

    def switch_players(self):
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"

    def move_to(self, amount, x, y, tower, isFree):
        for i in range(amount):
            # New position of the pawns
            self.ref[0].x = x
            self.ref[0].y = y
            # We add to pawns list the pawns that we move
            self.pawns.append(self.ref[0])
            # We remove the pawn from the latest location
            self.ref.pop(0)

        if not isFree:
            self.pawns += tower
            tower.clear()
            for p in self.pawns:
                tower.append(p)

        # if self.ref is NULL
        if not self.ref:
            # We remove it from the towers list
            self.towers.remove(self.ref)

        if isFree:
            self.towers.append(self.pawns)
        self.pawns = []
        self.ref = None

        return

    def distance(self, x, y, dx, dy):
        dist = math.sqrt(math.pow((dx - x), 2) + math.pow((dy - y), 2))

        if dist == 1:
            return 1
        elif dist > 2:
            return 3
        return 2

    def check_win(self):
        count_white = 0
        count_black = 0
        for t in self.towers:
            if t[0].color == "white":
                count_white += 1
            if t[0].color == "black":
                count_black += 1

        if count_white == 0:
            self.winner = "Black"
            print("Black won!")
        elif count_black == 0:
            self.winner = "White"
            print("White won!")