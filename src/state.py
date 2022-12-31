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
        eval_ = 0
        eval_ += self.end_of_game()

        if eval_ != 0:
            return eval_

        if self.father.distance is not None:
            eval_ += self.take()
            eval_ += self.instant_retake()
            eval_ += self.move()

        print("EVAL : ", eval_)

        return eval_
    def take(self):
        distance = self.model.distance(self.father.prev_tower[0].x, self.father.prev_tower[0].y,
                                       self.father.tower[0].x, self.father.tower[0].y)
        tower = self.father.prev_tower
        deriv_tower = self.father.tower

        self.adversary_tower = self.model.determine_tower(deriv_tower[0].x, deriv_tower[0].y, self.father.father.towers)

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

        return 0

    def move(self):
        num = 0
        limit = 3

        if len(self.tower) == 1:
            return 0

        if len(self.tower) == 2:
            return 1

        if len(self.tower) == 3:
            return 2

        for pawn in self.tower:
            if self.tower[0].color == pawn.color and limit > 0:
                num += 1
                limit -= 1
            if limit == 0:
                if self.tower[0].color != pawn.color:
                    if num > 0:
                        num -= 1

        return num - 1

    def instant_retake(self):
        num = 1000

        for tower in self.father.towers:
            if tower != self.tower and tower[0].color != self.tower[0].color:

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

        if not win:
            return 0
        elif win:
            if self.attacker:
                print("WIN!")
                return 999
            else:
                print("LOOSE!")
                return -999

        return 0
