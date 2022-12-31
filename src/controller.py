import view
import model


class Controller:
    view = view.View
    model = model.Model

    def __init__(self, mode):
        self.mode = mode
        self.model = model.Model(self, self.mode)
        self.view = view.View(self)
        print("launching!")

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

    def tower_clicked(self, tower):
        self.view.selected_tower = tower

    # An action has been made by the player of the ia
    def action(self, x, y):
        print("new Action!")
        towers = self.get_towers()

        # We make this action depending on the player's turn
        self.get_turn().action(x, y, towers)

    # Method used to launch the ai vs ai mode
    def launch_ia_vs_ia(self):
        self.model.ia_vs_ia()

