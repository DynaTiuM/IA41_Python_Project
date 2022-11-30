import view
import model_player


class Controller:
    def __init__(self, mode):
        self.temp_click_j = None
        self.temp_click_i = None
        self.clicked = False
        self.view = None
        self.model = None
        self.mode = mode
        self.launch()
        print("launching!")

    def launch(self):
        if self.mode == 1:
            self.model = model_player.Model_Player(self)
            self.view = view.View(self)

    def get_towers(self):
        return self.model.towers

    def get_winner(self):
        return self.model.get_winner()

    def is_winner(self):
        return self.model.is_winner()

    def action(self, j, i):
        print("new Action!")
        towers = self.get_towers()

        print(towers)
        if self.is_winner:
            print("No Winner")
            if not self.clicked:
                for t in towers:
                    if j == t[0].x and i == t[0].y and t[0].color == self.model.turn:
                        self.model.ref = t
                        self.temp_click_j = j
                        self.temp_click_i = i
                        self.clicked = True
            elif j != self.temp_click_j or i != self.temp_click_i:
                self.model.switch_players()
                # number_of_moving corresponds to the number of pawns that we are able to move
                number_of_moving = self.model.distance(self.temp_click_j, self.temp_click_i, j, i)

                if len(self.model.ref) >= number_of_moving:
                    self.clicked = False
                    self.model.decide_type_of_moving(j, i, number_of_moving)
                else:
                    print("You don't have enough pawns! (", len(self.model.ref), ")")

        self.model.check_win()
