import state


class MinMax:

    def __init__(self, ia, model):
        self.tab = [0, None]
        self.state = state.State(model, ia, [], 0, 0, 0, True)
        self.ia = ia
        self.model = model

    def min_max(self, node, depth):

        v = self.max_value(node, depth)

        print("MAX : ", v[0])

        return v[1]

    def determine_state(self, v):
        print(self.ia.states)
        for s in self.ia.states:
            if s.eval == v:
                return s

    def max_value(self, node, depth):
        self.model.force_turn(self.ia, True)

        if depth != 0:
            self.ia.determine_states(node)
        if node.children == [] or depth == 0:
            print("==============")
            print(node.tower[0].color, "PLAYING", depth)  # Black turn
            print("==============")
            print("- max EVAL : ", node.evaluation(False))
            print("returning : ", [node.evaluation(False), node])
            return [node.evaluation(False), node]
        # v = -100000
        # 1st child : v = -2
        # 2nd child : v = 0
        # 3rd child : v = 0
        return_state = [-10000000, None]
        for child in node.children:
            # BLACK PLAYING
            temp_tab = self.min_value(child, depth - 1)
            print("Fighting between :", temp_tab[0], "and ", return_state[0])
            if temp_tab[0] >= return_state[0]:
                print("COORDINATES : ", temp_tab[1].dx, temp_tab[1].dy)
                return_state[0] = temp_tab[0]
                return_state[1] = temp_tab[1]

            print("- max : ", return_state[0])

        '''
            if self.state.eval <= v:
                self.state.eval = v
        node.eval = v
        '''

        print("\n")

        self.model.switch_players()

        return return_state

    def min_value(self, node, depth):

        self.model.force_turn(self.ia, False)

        if depth != 0:
            self.ia.determine_states(node)

        if node.children == [] or depth == 0:
            print("==============")
            print(node.tower[0].color, "PLAYING", depth)  # White turn
            print("==============")
            print("returning : ", node.evaluation(True))
            return [node.evaluation(True), node]
        return_state = [+10000000, None]
        for child in node.children:
            temp_tab = self.max_value(child, depth - 1)
            # print("hierarchy : ", temp_tab[1].depth, " : ", temp_tab[1].x, temp_tab[1].y)
            print("Fighting between :", temp_tab[0], "and ", return_state[0])
            if temp_tab[0] <= return_state[0]:
                print("COORDINATES : ", temp_tab[1].dx, temp_tab[1].dy)
                return_state[0] = temp_tab[0]
                return_state[1] = temp_tab[1]

            print("- min : ", return_state[0])
        '''
            if self.state.eval >= v:
                self.state.eval = v
        node.eval = v
        '''
        print("\n")

        self.model.switch_players()

        return return_state
