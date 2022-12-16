import state
import MinMax


class IA:
    possible_moves = 3
    states = []

    def __init__(self, color, turn, model):
        self.towers_to_examine = []
        self.color = color
        self.turn = turn
        self.model = model

    def determine_all_towers(self):
        for tower in self.model.towers:
            if tower[0].color == self.model.get_color():
                self.towers_to_examine.append(tower)

    def action(self, i, j, towers):
        if not self.model.is_winner():
            decided_state = state.State(self.model, [0], 0, 0, 0, True)
            minmax = MinMax.MinMax(self, self.model)
            state_ = minmax.min_max(decided_state, 1)
            if not minmax.state[1] is None:
                self.model.ref = state_.tower
                self.model.decide_type_of_moving(state_.dx, state_.dy,
                                                 state_.distance, self.model.towers)

            self.model.switch_players()

        self.model.check_win()
        return

    def determine_states(self, decided_state):
        num_root = 0
        self.determine_all_towers()
        # 0 - 1 - 2
        for amount_moves in range(self.possible_moves):
            distance = amount_moves + 1
            # We only work with the towers that the IA is able to move
            # i.e. the towers with the color black on the pawn at the first position of the tower
            for tower in self.towers_to_examine:
                for x in range(3):
                    for y in range(3):
                        if self.model.distance(tower[0].x, tower[0].y, x, y) == distance \
                                and len(tower) >= distance:
                            decided_state.add_child(state.State(self.model, tower, x, y, distance, False))
                            num_root += 1
        self.towers_to_examine.clear()
