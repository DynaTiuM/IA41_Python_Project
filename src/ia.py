class IA:
    def __init__(self, color, turn, model):
        self.color = color
        self.turn = turn
        self.model = model

    def action(self, x, y, towers):
        self.model.minmax.min_max(towers)
        self.model.check_win()
        self.model.switch_players()
