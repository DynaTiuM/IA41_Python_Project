import Heuristique

class MinMax:
    def __init__(self):
        self.heuristique = Heuristique.Heuristique()

    def min_max(self, tower):
        v = self.max_value(tower)

        return v

    def max_value(self, tower):
        v = self.heuristique.return_max()
        return v

    def min_value(self, tower):
        return v

