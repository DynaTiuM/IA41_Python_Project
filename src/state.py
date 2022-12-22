class State:
    def __init__(self, model, ia, dx, dy, distance, root=False):
        self.prev_x = None
        self.prev_y = None
        self.previous_towers = None
        self.previous_tower = None
        self.distance = None
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

    def print_towers(self):
        pawns = 0
        for t in self.towers:
            for p in t:
                pawns += 1
        print(pawns)

    def determine_new_tower(self):
        for t in self.towers:
            if t[0].x == self.dx and t[0].y == self.dy:
                self.tower = t

    def set_father(self, father):
        self.father = father

    def set_prev_tower(self, tower):
        self.prev_tower = tower

    def evaluation(self, attacker):
        self.attacker = attacker
        # self.adversary_tower = self.model.determine_tower(self.dx, self.dy, self.towers)

        if self.father.distance is not None:
            # self.eval += self.take()
            # move = self.move()
            instant_retake = self.instant_retake()
            # print("MOVE : ", move)
            # print("INSTANT RETAKE : ", instant_retake)
            # self.eval += move
            self.eval += instant_retake
            self.eval += self.take()

            # self.eval += self.end_of_game()
            print("POSITION OF THE PAWN :", self.tower[0].x, self.tower[0].y, "| COLOR : ",
                  self.tower[0].color, "| HIERARCHY :", self.depth)

            print("EVAL : ", self.eval)
            temp_eval = self.eval
            self.eval = 0

            return temp_eval

        # NOT WORKING
        else:
            if self.attacker:
                self.eval = -999
            else:
                self.eval = 999
        return self.eval

    # [w, b, b, w, b, b]
    # ---> moving 2 :
    # [b, w, b, b]
    #  ^
    # /|\
    #  |
    # Moving with no loss !
    def take(self):
        # self.father.tower = [0, 0] : BLACK
        print("PREVIOUS X AND Y : ", self.father.prev_tower[0].x, self.father.prev_tower[0].y)
        print("ACTUAL X AND Y : ", self.father.tower[0].x, self.father.tower[0].y)
        distance = self.model.distance(self.father.prev_tower[0].x, self.father.prev_tower[0].y,
                                       self.father.tower[0].x, self.father.tower[0].y)
        tower = self.father.prev_tower
        deriv_tower = self.father.tower

        self.adversary_tower = self.model.determine_tower(deriv_tower[0].x, deriv_tower[0].y, self.father.father.towers)

        if self.adversary_tower:
            print("ADVERSARY TOWER :", self.adversary_tower[0].x, self.adversary_tower[0].y)

        # TAKE WITH NO LOSS :
        if len(tower) == distance and self.adversary_tower == []:
            print("NO TAKE WITH NO LOSS!")
            return 0
        elif len(tower) == distance and self.adversary_tower[0].color != tower[0].color:
            print("TAKE WITH NO LOSS!")
            if self.attacker:
                return 2
            else:
                return -2
        elif tower[distance - 1].color == tower[0].color and self.adversary_tower == []:
            print("NO TAKE WITH NO LOSS 2!")
            return 0
        elif tower[distance - 1].color == tower[0].color and self.adversary_tower[0].color != tower[0].color:
            print("TAKE WITH NO LOSS 2!")
            if self.attacker:
                return 2
            else:
                return -2
        elif tower[distance - 1].color != tower[0].color and self.adversary_tower == []:
            print("NO TAKE WITH LOSS !!")
            if self.attacker:
                return -2
            else:
                return 2
        elif tower[distance - 1].color != tower[0].color and self.adversary_tower[0].color != tower[0].color:
            print("TAKE WITH LOSS !!")
            if self.attacker:
                return -1
            else:
                return 1
        elif tower[distance - 1].color != tower[0].color and self.adversary_tower[0].color == tower[0].color:
            print("NO TAKE WITH LOSS 2!!")
            if self.attacker:
                return -2
            else:
                return 2
        return 0

    def move(self):
        num = 0
        limit = 3

        if len(self.father.tower) == 1:
            return 1

        if len(self.father.tower) == 2:
            return 2

        if len(self.father.tower) == 3:
            return 2

        for pawn in self.father.tower:
            if self.father.tower[0].color == pawn.color and limit > 0:
                num += 1
                limit -= 1
            if limit == 0:
                if self.father.tower[0].color != pawn.color:
                    if num > 0:
                        num -= 1

        if self.attacker:
            return num
        return -num

    def instant_retake(self):
        # self.father.tower = [0, 0] : BLACK
        for tower in self.father.towers:
            # print("TOWER : ", tower[0].x, tower[0].y, "| deriv : ", self.tower[0].x, self.tower[0].x)

            # self.tower = [0 , 0] : WHITE
            # tower = [1 , 0] : WHITE
            if tower != self.tower and tower[0].color == self.tower[0].color:
                # print("TOWER FOUND : ", tower[0].x, tower[0].y, tower[0].color)
                # print("DERIVATIVE TOWER : ", self.tower[0].x, self.tower[0].y, self.tower[0].color)
                if len(tower) >= self.distance:

                    # the tower can instantly retake the tower, but with loss
                    # [w, w, b, b]
                    # [b, b]

                    # len(tower) == 1
                    # self.distance == 1        OR self.father.distance ??????
                    # self.tower[0].x = 0 and self.father.tower[0].x = 0
                    # self.tower[0].y = 0 and self.father.tower[0].y = 0
                    if len(tower) == self.distance and self.tower[0].x == self.father.tower[0].x \
                            and self.tower[0].y == self.father.tower[0].y:
                        print("RETAKE THE TOWER WITHOUT LOSS : ")
                        if self.attacker:
                            return 2
                        else:
                            return -2
                    # If the color of the pawn is equal to the color of the father :
                    # tower = [1, 0] : White
                    # self.father.tower[0].color == Black
                    elif tower[self.distance - 1].color == self.father.tower[0].color \
                            and self.tower[0].x == self.father.tower[0].x \
                            and self.tower[0].y == self.father.tower[0].y:
                        print("RETAKE THE TOWER WITH LOSS : ", tower[0].x, tower[0].y)
                        if self.attacker:
                            return 1
                        else:
                            return -1
                    elif tower[self.distance - 1].color != self.father.tower[0].color \
                            and self.tower[0].x == self.father.tower[0].x \
                            and self.tower[0].y == self.father.tower[0].y:
                        print("RETAKE THE TOWER WITHOUT LOSS 2 : ", tower[0].x, tower[0].y)
                        if self.attacker:
                            return 2
                        else:
                            return -2

                    elif self.tower[0].x != self.father.tower[0].x and self.tower[0].y != self.father.tower[0].y:
                        print("CANNOT RETAKE THE TOWER!!")
                        if self.attacker:
                            return 0
                        else:
                            return 2
        return 0

    def end_of_game(self):
        pass
