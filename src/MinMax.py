import state


class MinMax:

    def __init__(self, ia, model):
        self.state = [0, None]
        self.ia = ia
        self.towers = None
        self.model = model

    def min_max(self, node, depth):
        v = self.max_value(node, depth)

        print("MAX : ", self.state, " : ", v)
        return self.state[1]

    def max_value(self, node, depth):
        self.ia.determine_states(node)
        if node.children is None or depth == 0:
            return node.calculate_heuristic()
        v = -10000000
        for child in node.children:
            v = max(v, self.min_value(child, depth - 1))
            if self.state[0] != v:
                self.state = [v, child]
        return v

    def min_value(self, node, depth):
        self.ia.determine_states(node)
        if node.children is None or depth == 0:
            return node.calculate_heuristic()
        v = +10000000
        for child in node.children:
            v = min(v, self.max_value(child, depth - 1))
            if self.state[0] != v:
                self.state = [v, child]
        return v