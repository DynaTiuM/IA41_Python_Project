class State:
    def __init__(self, model, ia, dx, dy, distance, root=False):
        self.prev_tower = self.prev_x = self.prev_y = self.previous_towers = self.previous_tower = self.distance = None
        self.depth = self.father = None
        self.towers = []
        self.tower = []
        self.ia = ia
        self.attacker = True
        self.adversary_tower = []
        self.root = root
        self.children = []
        if not root:
            self.dx = dx
            self.dy = dy
            self.distance = distance

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

    def set_prev_tower(self, tower):
        self.prev_tower = tower

    def evaluation(self, attacker):
        self.attacker = attacker
        eval_ = 0

        if self.father.distance is not None:
            eval_ += self.take()
            self.value_retake = self.instant_retake()
            eval_ += self.value_retake
            eval_ += self.move()

            eval_ += self.end_of_game()

            print("POSITION OF THE PAWN :", self.tower[0].x, self.tower[0].y, "| COLOR : ",
                  self.tower[0].color, "| HIERARCHY :", self.depth)

        print("EVAL : ", eval_)

        return eval_

    # [w, b, b, w, b, b]
    # ---> moving 2 :
    # [b, w, b, b]
    #  ^
    # /|\
    #  |
    # Moving with no loss !
    def take(self):
        print("PREVIOUS X AND Y : ", self.father.prev_tower[0].x, self.father.prev_tower[0].y, self.father.prev_tower[0].color)
        print("ACTUAL X AND Y : ", self.father.tower[0].x, self.father.tower[0].y, self.father.tower[0].color)
        distance = self.model.distance(self.father.prev_tower[0].x, self.father.prev_tower[0].y,
                                       self.father.tower[0].x, self.father.tower[0].y)
        tower = self.father.prev_tower
        deriv_tower = self.father.tower

        self.adversary_tower = self.model.determine_tower(deriv_tower[0].x, deriv_tower[0].y, self.father.father.towers)

        if self.adversary_tower:
            print("ADVERSARY TOWER :", self.adversary_tower[0].x, self.adversary_tower[0].y,
                  self.adversary_tower[0].color)
            print("ACTUAL TOWER : ", deriv_tower[0].color)

        # TAKE WITH NO LOSS :
        if len(tower) == distance and self.adversary_tower == []:
            print("NO TAKE WITH NO LOSS!")
            return 0
        elif len(tower) == distance and self.adversary_tower[0].color != tower[0].color:
            print("TAKE WITH NO LOSS!")
            return 10
        elif len(tower) == distance and self.adversary_tower[0].color == tower[0].color:
            print("LOOSING A TOWER!!")
            return -10
        elif tower[distance].color == tower[0].color and self.adversary_tower == []:
            print("NO TAKE WITH NO LOSS 2!")
            return 0
        elif tower[distance].color == tower[0].color and self.adversary_tower[0].color != tower[0].color:
            print("TAKE WITH NO LOSS 2!")
            return 10
        elif tower[distance].color != tower[0].color and self.adversary_tower == []:
            print("NO TAKE WITH LOSS !!")
            return -4
        elif tower[distance].color != tower[0].color and self.adversary_tower[0].color != tower[0].color:
            print("TAKE WITH LOSS !!")
            return -1
        elif tower[distance].color != tower[0].color and self.adversary_tower[0].color == tower[0].color:
            print("LOOSING A TOWER 2!!")
            return -10
        elif tower[distance].color == tower[0].color and self.adversary_tower[0].color == tower[0].color:
            print("MOVING ON A SAME COLOR TOWER AND NO LOOSE!!")
            return -4

        print("PROBLEM")
        return 0

    def move(self):
        num = 0
        if len(self.tower) == 1:
            num = 0
        if len(self.tower) == 2:
            num = 1
        if len(self.tower) == 3:
            num = 2

        if len(self.tower) > 3:
            if self.tower[3].color != self.tower[0].color:
                if self.tower[0].color == self.tower[2].color:
                    num = 1
                else:
                    num = 0
            else:
                num = 2
        return num

    def instant_retake(self):
        num = 1000

        # self.father.tower = [0, 0] : BLACK
        for tower in self.father.towers:
            # print("TOWER : ", tower[0].x, tower[0].y, "| deriv : ", self.tower[0].x, self.tower[0].x)

            if tower != self.tower and tower[0].color != self.tower[0].color:
                print("TOWER FOUND : ", tower[0].x, tower[0].y, tower[0].color)
                print("DERIVATIVE TOWER : ", self.tower[0].x, self.tower[0].y, self.tower[0].color)

                distance = self.model.distance(tower[0].x, tower[0].y, self.tower[0].x, self.tower[0].y)

                if len(tower) == distance:
                    if num > -1:
                        num = -1
                        print("RETAKE THE TOWER WITHOUT LOSS : ", num)

                elif len(tower) > distance != -1:
                    if tower[distance].color == self.tower[0].color:
                        if num > 1:
                            num = 1
                            print("RETAKE THE TOWER WITH LOSS : ", num)
                    else:
                        if num > -1:
                            num = -1
                            print("RETAKE THE TOWER WITHOUT LOSS 2 : ", num)
                else:
                    if num > 2:
                        num = 2
                        print("CANNOT RETAKE THE TOWER!!", num)
        if num == 1000:
            num = 0
        return num

    def end_of_game(self):
        win = True
        for t in self.towers:
            if t[0].color != self.tower[0].color:
                win = False
        if win:
            if self.attacker:
                print("WIN!")
                return 999

        # The ai is going to loose!
        if self.value_retake == -1:
            print("LOSS !")
            return -100

        return 0
