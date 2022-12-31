from copy import copy, deepcopy

import state
import MinMax


class IA:
    possible_moves = 3
    states = []
    turn = False

    def __init__(self, color, turn, model):
        self.towers_to_examine = []
        self.color = color
        self.turn = turn
        self.model = model

        self.minmax = MinMax.MinMax(self, self.model)

    def determine_all_towers(self, towers):
        for tower in towers:
            if tower[0].color == self.model.get_color():
                self.towers_to_examine.append(tower)

    def action(self, i, j, towers):
        if not self.model.is_winner():
            # We instantiate the state that will be decided at the end of the travel of MinMax's algorithm
            decided_state = state.State(self.model, self, None, None, None, True)
            # This initial state possess the actual towers of this game
            decided_state.towers = self.model.towers
            # It is the root of the tree, so we set it at hierarchy 0
            decided_state.set_hierarchy(0)
            # We determine the state that the MinMax algorithm has found in relation to the decided state
            state_ = self.minmax.min_max(decided_state, 2)

            if state_ is not None:
                # This state_ found possess a list of towers, in relation to the best play possible, so we just
                # need to replace the actual towers position to the state's ones found.
                self.model.towers = state_.towers
                # We don't forget to switch the players at the end
                self.model.switch_players()

        # We check if there is a winner
        self.model.check_win()
        return

    def determine_states(self, decided_state):

        # We determine the towers that the ai is able to move
        self.determine_all_towers(decided_state.towers)

        # For each of them, we check the moves that they are able to do
        for tower in self.towers_to_examine:
            # To do so, we travel a "fictional [3, 3]" two dimensial array
            for dx in range(3):
                for dy in range(3):
                    # And for each position, we calculate the distance between the tower and the destination
                    distance = self.model.distance(tower[0].x, tower[0].y, dx, dy)

                    # If the tower is able to move to this position :
                    if len(tower) >= distance != - 1:
                        # We add a new child to the tree with its characteristics
                        child = state.State(self.model, self, dx, dy, distance, False)
                        decided_state.add_child(child)
                        child.set_prev_tower(tower)
                        child.set_father(decided_state)
                        child.set_hierarchy(child.father.depth + 1)

                        self.model.ref = tower
                        child.towers = self.model.decide_type_of_moving(dx, dy, distance, decided_state.towers,
                                                                        False)

                        child.determine_new_tower()

        self.towers_to_examine.clear()