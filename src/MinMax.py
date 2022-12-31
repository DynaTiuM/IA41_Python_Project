from random import random, randint

import state


class MinMax:

    def __init__(self, ia, model):
        self.ia = ia
        self.model = model

    def min_max(self, node, depth):
        v = self.max_value(node, depth)
        self.model.force_turn(self.ia, True)

        print("MAX : ", v[0], v[1].tower[0].x, v[1].tower[0].y)
        while v[1].depth != 1:
            v[1] = v[1].father
            depth -= 1
        return v[1]

    def max_value(self, node, depth):
        self.model.force_turn(self.ia, True)
        print("----------- MAX CALLED ----------- depth : ", depth)

        if depth != 0:
            self.ia.determine_states(node)

        if node.children == [] or depth == 0:
            print("- max EVAL : ", node.evaluation(False))
            return [node.evaluation(False), node]

        return_state = [-10000000, None]

        for child in node.children:
            temp_tab = self.min_value(child, depth - 1)

            if temp_tab[0] >= return_state[0]:
                return_state[0] = temp_tab[0]
                return_state[1] = temp_tab[1]

        print("- max : ", return_state[0])

        print("\n")
        return return_state

    def min_value(self, node, depth):
        self.model.force_turn(self.ia, False)
        print("----------- MIN CALLED ----------- depth : ", depth)

        if depth != 0:
            self.ia.determine_states(node)

        if node.children == [] or depth == 0:
            print("- min EVAL : ", node.evaluation(True))
            return [node.evaluation(True), node]

        return_state = [+10000000, None]

        for child in node.children:
            temp_tab = self.max_value(child, depth - 1)
            if temp_tab[0] <= return_state[0]:
                return_state[0] = temp_tab[0]
                return_state[1] = temp_tab[1]

        print("- min : ", return_state[0])

        print("\n")

        return return_state
