
class State:
    def __init__(self, model, tower, dx, dy, distance, root=False):
        self.adversary_tower = []
        self.root = root
        self.children = []
        self.tower = tower

        if not root:
            self.x = tower[0].x
            self.y = tower[0].y
            self.dx = dx
            self.dy = dy
            self.distance = distance

        self.heuristic = 0
        self.model = model

    def add_child(self, child):
        self.children.append(child)

    def calculate_heuristic(self):
        self.adversary_tower = self.model.determine_tower(self.dx, self.dy)

        self.heuristic += self.take()
        self.heuristic += self.size()
        self.heuristic += self.instant_retake()
        # self.sum += self.end_of_game()

        temp_heuristic = self.heuristic
        self.heuristic = 0

        return temp_heuristic

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
        elif self.tower[self.distance - 1].color == self.model.get_color() and self.adversary_tower is not None \
                and self.tower[0].color != self.adversary_tower[0].color:
            return 2
        # Loss and gain
        elif self.tower[self.distance - 1].color != self.model.get_color() and self.adversary_tower is not None \
                and self.tower[0].color != self.adversary_tower[0].color:
            return -1
        # Loss and no gain
        else:
            return -2

    def size(self):
        num = 0
        limit = 3
        for pawn in self.tower:
            if pawn.color == self.model.get_color() and limit > 0:
                num += 1
            limit -= 1

        if limit > 0:
            if self.adversary_tower:
                for pawn in self.adversary_tower:
                    if pawn.color == self.model.get_color() and limit > 0:
                        num += 1
                    limit -= 1

        # Imagine [w, b, w] for the current tower,  [b, b] for the enemy's tower
        # --> limit = 3
        # --> num = 0
        # 1st iteration : num = 1   |   limit = 2
        # 2nd iteration : limit = 1 |
        # 3rd iteration : num = 2   |   limit = 0
        # We stop here

        return num - 1

    def instant_retake(self):
        for tower in self.model.towers:
            distance = self.model.distance(self.x, self.y, tower[0].x, tower[0].y)
            if len(tower) >= distance:
                # the tower can instantly retake the tower, but with loss
                if tower[distance - 1].color != self.model.get_color():
                    return 1
                # the tower can instantly retake the tower
                elif tower[distance - 1].color == self.model.get_color() and tower[0].x != 1 and tower[0].y != 1:
                    return 0
            # the tower cannot instantly retake the tower, and the tower of the player is at the middle of the game
            elif tower[0].x == 1 and tower[0].y == 1:
                return 3
            # the tower cannot instantly retake the tower and the tower of the player is not at the middle
            else:
                return 2

    def end_of_game(self):
        pass
