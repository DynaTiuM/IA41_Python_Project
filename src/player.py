

class Player:
    def __init__(self, color, turn, model):
        self.temp_j = None
        self.temp_i = None
        self.model = model
        self.color = color
        self.turn = turn
        self.clicked = False
        self.winner = False

    def decide_type_of_moving(self, j, i, number_of_moving, towers):
        # Searching for if a tower already exists on the new position
        for tower in towers:
            # If this is the case,
            if j == tower[0].x and i == tower[0].y:
                self.model.move_to(number_of_moving, j, i, tower, False)
                return

        # No tower exists, the new position is free
        self.model.move_to(number_of_moving, j, i, towers, True)

    def action(self, j, i, towers):
        if not self.winner:
            print("No Winner")
            # First click of the player so that he can select a pawn to move:
            if not self.clicked:
                for t in towers:
                    if j == t[0].x and i == t[0].y and t[0].color == self.color:
                        self.model.ref = t
                        self.temp_j = j
                        self.temp_i = i
                        self.clicked = True
            # The player clicked on another case:
            elif j != self.temp_j or i != self.temp_i:
                self.model.switch_players()
                # number_of_moving corresponds to the number of pawns that we are able to move
                number_of_moving = self.model.distance(self.temp_j, self.temp_i, j, i)

                if len(self.model.ref) >= number_of_moving:
                    self.clicked = False
                    self.model.decide_type_of_moving(j, i, number_of_moving)
                else:
                    print("You don't have enough pawns! (", len(self.model.ref), ")")
            # The player wants to change his pawn to move:
            else:
                self.clicked = False
                return

        self.model.check_win()
