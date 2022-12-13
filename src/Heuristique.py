

class Heuristique:

    def __init__(self):
        self.turn = None
        self.tower = None
        self.sum = 0

    def take(self):
        pass

    def calculate_heuristique(self, tower, turn):
        self.tower = tower
        self.turn = turn

        self.sum += self.take()
        self.sum += self.size()
        self.sum += self.instant_retake()
        self.sum += self.end_of_game()

    def size(self):
        num = 0
        for pawn in self.tower:
            if pawn[0].color == self.turn:
                num += 1

        if num == 0:
            return -1
        elif num == 1:
            return 0
        elif num == 2:
            return 1
        elif num == 3:
            return 2

    def instant_retake(self):


    def end_of_game(self):
        pass

    def return_max(self):
        return self.sum
