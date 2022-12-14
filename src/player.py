

class Player:
    def __init__(self, color, turn, model):
        self.temp_x = self.temp_y = None
        self.model = model
        self.color = color
        self.turn = turn
        self.clicked = False

    def action(self, x, y, towers):
        if not self.model.is_winner():
            print("No Winner")
            # First click of the player so that he can select a pawn to move:
            if not self.clicked:
                for t in towers:
                    if x == t[0].x and y == t[0].y and t[0].color == self.color:
                        self.model.ref = t
                        self.temp_x = x
                        self.temp_y = y
                        self.clicked = True
                        self.model.send_tower_clicked(t)

            # The player already selected its pawn to move :
            # He clicked on another case:
            elif x != self.temp_x or y != self.temp_y:
                # number_of_moving corresponds to the number of pawns that we are able to move
                number_of_moving = self.model.distance(self.temp_x, self.temp_y, x, y)

                # The player has enough pawns !
                if len(self.model.ref) >= number_of_moving != -1:
                    self.clicked = False
                    self.model.send_tower_clicked([])
                    # We call the method of the Model to change the coordinates of the tower
                    self.model.towers = self.model.decide_type_of_moving(x, y, number_of_moving, self.model.towers, True)

                    self.model.switch_players()

                # The play doesn't have enough pawns
                else:
                    print("You don't have enough pawns! (", len(self.model.ref), ")")
                    return

            # The player wants to change his pawn to move (he clicked on the same pawn) :
            else:
                self.model.send_tower_clicked([])
                self.clicked = False
                return

        self.model.check_win()
