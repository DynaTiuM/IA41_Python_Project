
class State:
    def __init__(self, model, ia, tower, dx, dy, distance, root=False):
        self.depth = None
        self.ia = ia
        self.attacker = True
        self.adversary_tower = []
        self.root = root
        self.children = []
        self.tower = tower
        self.father = None

        if not root:
            self.x = tower[0].x
            self.y = tower[0].y
            self.dx = dx
            self.dy = dy
            self.distance = distance

        self.eval = 0
        self.model = model

    def add_child(self, child):
        self.children.append(child)
        
    def set_hierarchy(self, depth):
        self.depth = depth

    def set_father(self, father):
        self.father = father

    def evaluation(self, attacker):
        self.attacker = attacker
        self.adversary_tower = self.ia.determine_tower(self.dx, self.dy)

        self.eval += self.take()
        self.eval += self.move()
        self.eval += self.instant_retake()

        # self.sum += self.end_of_game()
        print("eval : ", self.eval)

        temp_eval = self.eval
        self.eval = 0

        return temp_eval

    # [w, b, b, w, b, b]
    # ---> moving 2 :
    # [b, w, b, b]
    #  ^
    # /|\
    #  |
    # Moving with no loss !
    def take(self):
        # No loss and no gain
        if self.distance > len(self.tower) and self.adversary_tower == []:
            return 0
        # No loss and gain
        elif self.tower[self.distance - 1].color == self.model.get_color() and self.adversary_tower != [] \
                and self.tower[0].color != self.adversary_tower[0].color:
            print("NO loss and GAIN!")
            if self.attacker:
                return 2
            else:
                return -2
        # Loss and gain
        elif self.tower[self.distance - 1].color != self.model.get_color() and self.adversary_tower != [] \
                and self.tower[0].color != self.adversary_tower[0].color:
            if self.attacker:
                return -1
            else:
                return 1
        # Loss and no gain
        else:
            if self.attacker:
                return -2
            else:
                return 0

    def move(self):
        num = 0
        limit = 3
        dist = 0
        temp_tower = []

        for pawn in self.tower:
            if dist != self.distance:
                temp_tower.append(pawn)
                dist += 1

        new_tower = temp_tower + self.adversary_tower

        for i in range(len(new_tower)):
            if i == len(new_tower) - 1:
                num += 1
                if self.attacker:
                    return num
                return -num
            if new_tower[i+1].color == self.model.get_color() and limit > 0:
                num += 1
            limit -= 1

        # Imagine [b, w, b] for the current tower,  [w, w] for the enemy's tower
        # --> limit = 3
        # --> num = 0
        # 1st iteration : num = 1   |   limit = 2
        # 2nd iteration : limit = 1 |
        # 3rd iteration : num = 2   |   limit = 0
        # We stop here
        if self.attacker:
            return num
        return -num

    def instant_retake(self):
        for tower in self.model.towers:
            if tower != self.tower and tower[0].color != self.tower[0].color:
                if len(tower) >= self.distance:
                    # the tower can instantly retake the tower, but with loss
                    # [w, w, b, b]
                    # [b, b]
                    if tower[self.distance - 1].color != self.model.get_color():
                        if self.attacker:
                            return 1
                        else:
                            return -1
                    # the tower can instantly retake the tower
                    elif tower[self.distance - 1].color == self.model.get_color() and tower[0].x != 1 \
                            and tower[0].y != 1:
                        if self.attacker:
                            return -1
                        else:
                            return 1
                # the tower cannot instantly retake the tower and the tower of the player is not at the middle
                else:
                    if self.attacker:
                        return 2
                    else:
                        return -2
        return 0

    def end_of_game(self):
        pass
