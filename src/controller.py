import view
import model_player


class Controller:
    def __init__(self, mode):
        self.view = None
        self.model = None
        self.mode = mode
        self.launch()
        print("launching!")

    def launch(self):
        self.model = model_player.Model_Player(self, self.mode)
        self.view = view.View(self)

    def get_towers(self):
        return self.model.towers

    def get_winner(self):
        return self.model.get_winner()

    def is_winner(self):
        return self.model.is_winner()

    def is_selected(self):
        return

    def get_turn(self):
        if self.model.player1.turn:
            return self.model.player1
        else:
            return self.model.player2

    def action(self, j, i):
        if self.mode == 3:
            return
        print("new Action!")
        towers = self.get_towers()

        player_action = self.get_turn()

        player_action.action(j, i, towers)
