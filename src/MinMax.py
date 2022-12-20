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
        if node.children == [] or depth == 0:
            return node.evaluation()
        v = -10000000
        for child in node.children:
            child.eval = self.min_value(child, depth - 1)
            v = max(v, child.eval)
            print("max : ", v)
            print("------------")
            if self.state.eval < v:
                self.state = child
        return v

    def min_value(self, node, depth):
        self.ia.determine_states(node)
        if node.children == [] or depth == 0:
            return node.evaluation()
        v = +10000000
        for child in node.children:
            child.eval = self.max_value(child, depth - 1)
            v = min(v, child.eval)
            print("min : ", v)
            print("------------")
            if self.state.eval > v:
                self.state = child
        return v
