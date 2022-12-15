import state


class MinMax:

    def __init__(self, ia, model):
        self.ia = ia
        self.towers = None
        self.model = model

    def min_max(self, node, depth):
        v = self.max_value(node, depth)

        print("MAX : ", v)
        return v

    def max_value(self, node, depth):
        self.ia.t(node)
        if node.children is None or depth == 0:
            return node.calculate_heuristic()
        v = -10000000
        for child in node.children:
            v = max(v, self.min_value(child, depth - 1))
        print("max value temp : ", v)
        return v

    def min_value(self, node, depth):
        self.ia.t(node)
        if node.children is None or depth == 0:
            return node.calculate_heuristic()
        print("min children : ", node.children)
        v = +10000000
        for child in node.children:
            v = min(v, self.max_value(child, depth - 1))

        print("min value temp : ", v)
        return v
