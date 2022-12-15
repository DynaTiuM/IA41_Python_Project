class Heuristique:

    def __init__(self, model):
        self.adversary_tower = None
        self.sum = 0
        self.distance = None
        self.x = self.y = 0
        self.model = model
        self.tower = []
        self.turn = None

    def calculate_heuristique(self, tower, x, y, turn, distance):
        self.x = x
        self.y = y
        self.distance = distance
        self.tower = tower
        self.turn = turn

        self.adversary_tower = self.model.determine_tower(x, y)

        self.sum += self.take()
        self.sum += self.size()
        # sum_ += self.instant_retake()
        # self.sum += self.end_of_game()

        return self.sum

    # [w, b, b, w, b, b]
    # ---> moving 2 :
    # [b, w, b, b]
    #  ^
    # /|\
    #  |
    # Moving with no loss !
    def take(self):
        # No loss and no gain
        if self.distance > len(self.tower) and self.adversary_tower is not None:
            print("coming here2 !")
            return 0
        # No loss and gain
        elif self.tower[self.distance - 1].color == self.model.get_color() and self.adversary_tower is not None\
                and self.tower[0].color != self.adversary_tower[0].color:
            print("coming here3 !")
            return 2
        # Loss and gain
        elif self.tower[self.distance - 1].color != self.model.get_color() and self.adversary_tower is not None\
                and self.tower[0].color != self.adversary_tower[0].color:
            print("coming here4 !")
            return -1
        # Loss and no gain
        else:
            return -2

    def size(self):
        num = 0
        print(self.tower)
        for pawn in self.tower:
            if pawn.color == self.turn:
                num += 1

        return num - 1

    def instant_retake(self):
        pass

    def end_of_game(self):
        pass