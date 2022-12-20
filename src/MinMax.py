import state


class MinMax:

    def __init__(self, ia, model):
        self.state = state.State(model, [], 0, 0, 0, True)
        self.ia = ia
        self.model = model

    def min_max(self, node, depth):
        self.max_value(node, depth)
        print("MAX : ", self.state.eval)
        self.model.force_turn(self.ia)

        return self.state

    def max_value(self, node, depth):
        self.ia.determine_states(node)
        if node.tower:
            print("max color : ", node.tower[0].color)
        if node.children == [] or depth == 0:
            return node.evaluation()
        v = -10000000
        # v = -100000
        # 1st child : v = -2
        # 2nd child : v = 0
        # 3rd child : v = 0
        for child in node.children:
            v = max(v, self.min_value(child, depth - 1))
            print("max : ", v)
            print("------------")
            if self.state.eval <= v:
                self.state.eval = v
                self.state = child
        self.model.switch_players()
        return v

    def min_value(self, node, depth):
        self.ia.determine_states(node)
        print("min color :", node.tower[0].color)
        if node.children == [] or depth == 0:
            return node.evaluation()
        v = +10000000
        for child in node.children:
            v = min(v, self.max_value(child, depth - 1))
            print("min : ", v)
            print("------------")
            if self.state.eval >= v:
                self.state.eval = v
                self.state = child
        self.model.switch_players()
        return v
