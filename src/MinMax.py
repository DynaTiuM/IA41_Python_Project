import state


class MinMax:

    def __init__(self, ia, model):
        self.state = state.State(model, [], 0, 0, 0, True)
        self.ia = ia
        self.towers = None
        self.model = model

    def min_max(self, node, depth):

        v = self.max_value(node, depth)

        print("MAX : ", self.state, " : ", v)
        self.model.force_turn(self.ia)
        return self.state

    def max_value(self, node, depth):
        self.ia.determine_states(node)
        if node.children is None or depth == 0:
            return node.calculate_heuristic()
        v = -10000000
        for child in node.children:
            v = max(v, self.min_value(child, depth - 1))
            if self.state.heuristic != v:
                child.heuristic = v
                self.state = child
        return v

    def min_value(self, node, depth):
        self.ia.determine_states(node)
        if node.children is None or depth == 0:
            return node.calculate_heuristic()
        v = +10000000
        for child in node.children:
            v = min(v, self.max_value(child, depth - 1))
            if self.state.heuristic != v:
                child.heuristic = v
                self.state = child
        return v