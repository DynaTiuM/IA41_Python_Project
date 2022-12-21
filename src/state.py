class State:
    def __init__(self, model, ia, dx, dy, distance, root=False):
        self.previous_towers = None
        self.previous_tower = None
        self.depth = None
        self.towers = []
        self.tower = []
        self.ia = ia
        self.attacker = True
        self.adversary_tower = []
        self.root = root
        self.children = []
        self.father = None
        self.x = self.y = None
        if not root:
            self.dx = dx
            self.dy = dy
            self.distance = distance

        self.eval = 0
        self.model = model

    def add_child(self, child):
        self.children.append(child)

    def set_hierarchy(self, depth):
        self.depth = depth

    def previous_move_information(self):
        print("\n")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("PREVIOUS TOWERS :")
        for t in self.father.towers:
            print(t[0].x, t[0].y)
        if self.father.tower:
            print("FATHER TOWER : ", self.father.tower[0].x, self.father.tower[0].y)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("\n")

    def determine_new_tower(self):
        for t in self.towers:
            if t[0].x == self.dx and t[0].y == self.dy:
                self.tower = t

    def set_father(self, father):
        self.father = father

    def evaluation(self, attacker):
        self.attacker = attacker
        self.adversary_tower = self.model.determine_tower(self.tower[0].x, self.tower[0].y, self.father.towers)

        self.eval += self.take()
        # self.eval += self.move()
        # self.eval += self.instant_retake()

        # self.sum += self.end_of_game()
        print("eval : ", self.eval)
        for t in self.tower:
            print(t.color)
        print("POSITION OF THE PAWN :", self.tower[0].x, self.tower[0].y, "| COLOR : ",
              self.tower[0].color, "| HIERARCHY :", self.depth)

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
        if self.father.distance == len(self.father.tower) and self.adversary_tower == []:
            print(" NO loss and NO gain!")
            return 0
        # No loss and gain
        elif self.father.tower[self.father.distance - 1].color == self.model.get_color() and self.adversary_tower != [] \
                and self.father.tower[0].color == self.adversary_tower[0].color:
            print("NO loss and GAIN!")
            if self.attacker:
                return 2
            else:
                return -2
        # Loss and gain
        elif self.father.tower[self.father.distance - 1].color != self.model.get_color() and self.adversary_tower != [] \
                and self.father.tower[0].color != self.adversary_tower[0].color:
            print("LOSS and GAIN!!")
            if self.attacker:
                return -1
            else:
                return 1
        # Loss and no gain
        else:
            print("LOSS and NO gain!")
            if self.attacker:
                return -2
            else:
                return -2

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
            if new_tower[i + 1].color == self.model.get_color() and limit > 0:
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
