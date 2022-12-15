class State:

    def __init__(self, model, tower, dx, dy, distance):
        self.tower = tower
        self.x = tower[0].x
        self.y = tower[0].y
        self.dx = dx
        self.dy = dy
        self.distance = distance

        self.adversary_tower = None
        self.sum = 0
        self.model = model

    def calculate_heuristic(self):
        self.adversary_tower = self.model.determine_tower(self.dx, self.dy)

        self.sum += self.take()
        self.sum += self.size()
        # sum_ += self.instant_retake()
        # self.sum += self.end_of_game()

        temp_sum = self.sum
        self.sum = 0

        return temp_sum

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
            return 0
        # No loss and gain
        elif self.tower[self.distance - 1].color == self.model.get_color() and self.adversary_tower is not None\
                and self.tower[0].color != self.adversary_tower[0].color:
            return 2
        # Loss and gain
        elif self.tower[self.distance - 1].color != self.model.get_color() and self.adversary_tower is not None\
                and self.tower[0].color != self.adversary_tower[0].color:
            return -1
        # Loss and no gain
        else:
            return -2

    def size(self):
        num = 0
        for pawn in self.tower:
            if pawn.color == self.model.get_color():
                num += 1

        return num - 1

    def instant_retake(self):
        pass

    def end_of_game(self):
        pass