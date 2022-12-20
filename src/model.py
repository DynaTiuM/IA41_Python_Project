import math
import pawn
import ia
import player


class Model:
    pawns = []
    towers = []
    winner = None

    ref = None

    def __init__(self, ref_controller, mode):
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

    def force_turn(self, ref_player, forced):
        if ref_player == self.player1 and forced:
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

    def determine_tower(self, x, y):

        for t in self.towers:
            if x == t[0].x and y == t[0].y:
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

    def decide_type_of_moving(self, x, y, number_of_moving):
        # Searching for if a tower already exists on the new position
        for tower in self.towers:
            # If this is the case,
            if x == tower[0].x and y == tower[0].y:
                self.move_to(number_of_moving, x, y, tower, False)
                return

        # No tower exists, the new position is free
        self.move_to(number_of_moving, x, y, self.towers, True)

    def move_to(self, amount, x, y, tower, is_free):
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
            tower.clear()
            for p in self.pawns:
                tower.append(p)

        # if self.ref is NULL
        if not self.ref:
            # We remove it from the towers list
            self.towers.remove(self.ref)

        if is_free:
            self.towers.append(self.pawns)
        self.pawns = []
        self.ref = None

        return

    def distance(self, x, y, dx, dy):
        dist = math.sqrt(math.pow((dx - x), 2) + math.pow((dy - y), 2))

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
