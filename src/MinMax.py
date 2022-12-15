import state


class MinMax:
    towers_to_examine = []
    table_size = 3
    possible_moves = 3
    heuristiques = []

    def __init__(self, model):
        self.towers = None
        self.model = model

    def min_max(self, node, depth):
        v = self.max_value(node, depth)
        print("Max : ", v)
        return v

    def max_value(self, node, depth):
        if depth == 0:
            return node.calculate_heuristic()
        v = -10000000
        for child in node:
            v = max(v, self.min_value(child, depth - 1))

        return v

    def min_value(self, node, depth):
        if depth == 0:
            return node.calculate_heuristic()
        v = +10000000
        for child in node:
            v = min(v, self.max_value(child, depth - 1))

        return v
