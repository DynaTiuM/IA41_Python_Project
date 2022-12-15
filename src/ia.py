import state

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
        decided_state = state.State(self.model, [0], 0, 0, 0, True)
        self.model.minmax.min_max(decided_state, 2)
        self.model.check_win()
        self.model.switch_players()

    def t(self, decided_state):
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
        # self.model.decide_type_of_moving(decided_state.tower[0].x, decided_state.tower[0].y,
        # decided_state.distance, self.model.towers)
        print(num_root)
