import math
from copy import copy, deepcopy

import pawn
import ia
import player


class Model:
    pawns = []
    towers = []
    winner = None

    ref = None

    def __init__(self, ref_controller, mode):
        self.saved_towers = None
        self.ref_controller = ref_controller
        self.mode = mode

        if mode == 1:
            self.player1 = player.Player("white", True, self)
            self.player2 = player.Player("black", False, self)
        elif mode == 2:
            self.player1 = player.Player("white", True, self)
            self.player2 = ia.IA("black", False, self)
        else:
            self.player1 = ia.IA("white", True, self)
            self.player2 = ia.IA("black", False, self)

        print("New Model!")
        # Creating the towers of white pawns
        for i in range(3):
            self.pawns.append(pawn.Pawn(0, i, 'white'))
            self.towers.append(self.pawns)
            self.pawns = []

        # Creating the towers of black pawns
        for i in range(3):
            self.pawns.append(pawn.Pawn(2, i, 'black'))
            self.towers.append(self.pawns)
            self.pawns = []

    def __del__(self):
        self.pawns.clear()
        self.towers.clear()

    def force_turn(self, ref_player, forced):
        if ref_player == self.player2 and forced:
            self.player2.turn = True
            self.player1.turn = False
        elif not forced:
            self.player2.turn = False
            self.player1.turn = True

    def get_winner(self):
        if self.winner != "nobody":
            return self.winner

    def get_color(self):
        if self.player1.turn:
            return self.player1.color
        else:
            return self.player2.color

    def determine_tower(self, x, y, towers):
        for t in towers:
            if x == t[0].x and y == t[0].y and t[0].color == self.get_color():
                return t
        return []

    def is_winner(self):
        if self.winner is not None:
            return True
        return False

    def send_tower_clicked(self, tower):
        self.ref_controller.tower_clicked(tower)

    def switch_players(self):
        if self.player1.turn:
            self.player1.turn = False
            self.player2.turn = True
            # if self.mode != 1:
            #    self.ref_controller.action(None, None)
        else:
            self.player1.turn = True
            self.player2.turn = False

    def decide_type_of_moving(self, x, y, number_of_moving, towers, player_):
        # Searching for if a tower already exists on the new position
        for destination_tower in towers:
            # If this is the case,
            if x == destination_tower[0].x and y == destination_tower[0].y:
                return self.move_to(number_of_moving, x, y, destination_tower, towers, False, player_)

        # No tower exists, the new position is free
        return self.move_to(number_of_moving, x, y, [], towers, True, player_)

    def move_to(self, amount, x, y, tower, towers, is_free, player_):
        if not player_:
            tower = deepcopy(tower)
            towers = deepcopy(towers)
            for t in towers:
                if self.ref[0].x == t[0].x and self.ref[0].y == t[0].y:
                    self.ref = t
        '''
        print("FIRST ~~~~~~~~~~~~~~~~~~~~~~")
        for t in towers:
            for p in t:
                print(p.color)
        print(towers)
        '''

        for i in range(amount):
            # New position of the pawns
            self.ref[0].x = x
            self.ref[0].y = y

            # We add to pawns list the pawns that we move
            self.pawns.append(self.ref[0])
            # We remove the pawn from the latest location
            self.ref.pop(0)

        if not is_free:
            self.pawns += tower
            for t in towers:
                for p in t:
                    if p.x == tower[0].x and p.y == tower[0].y:
                        if t in towers:
                            towers.remove(t)

            for p in self.pawns:
                tower.append(p)
            towers.append(self.pawns)

        # if self.ref is NULL
        if not self.ref:
            # We remove it from the towers list
            towers.remove(self.ref)

        if is_free:
            towers.append(self.pawns)
        self.pawns = []
        self.ref = None
        '''
        print("LAST ~~~~~~~~~~~~~~~~~~~~~~")
        for t in towers:
            for p in t:
                print(p.color)
        print(towers)
        '''

        return towers

    def distance(self, x, y, dx, dy):
        dist = math.sqrt(math.pow((dx - x), 2) + math.pow((dy - y), 2))
        if x == dx and y == dy:
            return -1
        if dist == 1:
            return 1
        elif math.sqrt(math.pow(1, 2) + math.pow(2, 2)) - 0.1 < dist < math.sqrt(math.pow(1, 2) + math.pow(2, 2)) + 0.1:
            return 3
        elif dist < math.sqrt(math.pow(2, 2) + math.pow(2, 2)):
            return 2
        return -1

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
