import math

import pawn
import ia
import player


class Model_Player:
    pawns = []
    towers = []
    winner = "nobody"

    clicked = False
    ref = None

    def __init__(self, ref_controller, mode):
        self.ref_controller = ref_controller

        if mode == 1:
            self.player1 = player.Player("white", True, self)
            self.player2 = player.Player("black", False, self)
        elif mode == 2:
            self.player1 = player.Player("white", True, self)
            self.player2 = ia.IA("black", False)
        else:
            self.player1 = ia.IA("white", True)
            self.player2 = ia.IA("black", False)

        self.temp_click_j = None
        self.temp_click_i = None
        print("New Model!")

        # Creating the towers of white pawns
        for i in range(3):
            for y in range(2):
                self.pawns.append(pawn.Pawn(0, i, 'white'))
            self.towers.append(self.pawns)
            self.pawns = []

        # Creating the towers of black pawns
        for i in range(3):
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
        if self.player1.turn:
            self.player1.decide_type_of_moving(j, i, number_of_moving, self.towers)
        else:
            self.player2.decide_type_of_moving(j, i, number_of_moving, self.towers)

    def switch_players(self):
        if self.player1.turn:
            self.player1.turn = False
            self.player2.turn = True
        else:
            self.player1.turn = True
            self.player2.turn = False

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
        white = False
        black = False
        for t in self.towers:
            if t[0].color == "white":
                white = True
            if t[0].color == "black":
                black = True

        if not white:
            self.winner = "Black"
        elif not black:
            self.winner = "White"
