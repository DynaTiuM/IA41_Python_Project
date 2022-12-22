import state


class MinMax:

    def __init__(self, ia, model):
        self.ia = ia
        self.model = model

    def min_max(self, node, depth):
        v = self.max_value(node, depth)
        self.model.force_turn(self.ia, True)

        # print("MAX : ", v[0], "| STATE ASSOCIATED : ", v[1].father.tower[0].x, ", ", v[1].father.tower[0].y)
        while depth != 1:
            v[1] = v[1].father
            depth -= 1
        return v[1]

    def determine_state(self, v):
        print(self.ia.states)
        for s in self.ia.states:
            if s.eval == v:
                return s

    def max_value(self, node, depth):       # depth = 2
        self.model.force_turn(self.ia, True)

        print("----------- MAX CALLED -----------", depth)
        # print("AI'S TURN : ", self.model.player2.turn)
        if depth != 0:
            self.ia.determine_states(node)      # we determine the  3 children of the node
        if node.children == [] or depth == 0:
            print("- max EVAL : ", node.evaluation(False), node.tower[0].x, node.tower[0].y)
            return [node.evaluation(False), node]
        # v = -100000
        # 1st child : v = -2
        # 2nd child : v = 0
        # 3rd child : v = 0
        return_state = [-10000000, None]

        for child in node.children:        # For every child of the node
            # BLACK PLAYING
            temp_tab = self.min_value(child, depth - 1)     # temp = the highest value of its children
            # print("Fighting between :", temp_tab[0], "and ", return_state[0])
            if temp_tab[0] >= return_state[0]:  # If this value is higher than the return_state value :
                return_state[0] = temp_tab[0]   # We save it
                return_state[1] = temp_tab[1]   # Also its state position
                # print("return_state : ", return_state[1].dx, return_state[1].dy)

        print("- max : ", return_state[0])

        print("\n")

        return return_state

    def min_value(self, node, depth):
        self.model.force_turn(self.ia, False)
        print("----------- MIN CALLED -----------", depth)
        # print("AI'S TURN : ", self.model.player2.turn)
        if depth != 0:
            self.ia.determine_states(node)

        if node.children == [] or depth == 0:
            print("- min EVAL : ", node.evaluation(True), node.tower[0].x, node.tower[0].y)
            return [node.evaluation(True), node]

        return_state = [+10000000, None]

        for child in node.children:
            temp_tab = self.max_value(child, depth - 1)
            # print("hierarchy : ", temp_tab[1].depth, " : ", temp_tab[1].x, temp_tab[1].y)
            # print("Fighting between :", temp_tab[0], "and ", return_state[0])
            if temp_tab[0] <= return_state[0]:
                return_state[0] = temp_tab[0]
                return_state[1] = temp_tab[1]
                # print("return_state : ", return_state[1].dx, return_state[1].dy)

        print("- min : ", return_state[0])

        print("\n")

        return return_state
