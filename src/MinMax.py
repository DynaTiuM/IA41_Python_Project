import state


class MinMax:

    def __init__(self, ia, model):
        self.state = state.State(model, ia, [], 0, 0, 0, True)
        self.ia = ia
        self.model = model

    def min_max(self, node, depth):
        v = self.max_value(node, depth)
        print("REAL MAX V : ", v)
        self.model.force_turn(self.ia)

        self.state = self.determine_state(v)
        print("MAX : ", self.state.eval)
        return self.state

    def determine_state(self, v):
        print(self.ia.states)
        for s in self.ia.states:
            if s.eval == v:
                return s

    def max_value(self, node, depth):
        self.ia.determine_states(node)
        if node.tower:
            print("==============")
            print(node.tower[0].color, "PLAYING")
        if node.children == [] or depth == 0:
            print("- max EVAL : ", node.evaluation(False))
            return node.evaluation(False)
        v = -10000000
        # v = -100000
        # 1st child : v = -2
        # 2nd child : v = 0
        # 3rd child : v = 0
        for child in node.children:
            v = max(v, self.min_value(child, depth - 1))

            print("- max : ", v)
            if self.state.eval <= v:
                self.state.eval = v
        node.eval = v
        self.model.switch_players()

        print("==============")
        print("\n")
        return v

    def min_value(self, node, depth):
        self.ia.determine_states(node)
        print("==============")
        print(node.tower[0].color, "PLAYING")

        if node.children == [] or depth == 0:
            print("- min EVAL : ", node.evaluation(True))
            return node.evaluation(True)
        v = +10000000
        for child in node.children:
            v = min(v, self.max_value(child, depth - 1))

            print("- min : ", v)

            if self.state.eval >= v:
                self.state.eval = v
        node.eval = v

        print("==============")
        print("\n")
        self.model.switch_players()
        return v
