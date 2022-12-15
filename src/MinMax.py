import Heuristique


class MinMax:
    towers_to_examine = []
    table_size = 3
    possible_moves = 3
    heuristiques = []

    def __init__(self, model):
        self.towers = None
        self.model = model

    def determine_all_towers(self):
        for tower in self.towers:
            if tower[0].color == self.model.get_color():
                self.towers_to_examine.append(tower)

    def min_max(self, towers):
        self.towers = towers
        self.determine_all_towers()
        print(self.towers_to_examine)

        # 0 - 1 - 2
        for amount_moves in range(self.possible_moves):
            # We only work with the towers that the IA is able to move
            # i.e. the towers with the color black on the pawn at the first position of the tower
            for tower in self.towers_to_examine:
                # Traveling the grid with a size of 3 by 3
                for x in range(3):
                    for y in range(3):
                        # If the distance is equal to amount_moves + 1, we calculate the heuristique
                        if tower is not None:
                            print(tower)
                            if self.model.distance(tower[0].x, tower[0].y, x, y) == amount_moves + 1 \
                                    and len(tower) >= amount_moves + 1:
                                # We pass in parameter :    the position (x,y) that we want to work with
                                #                           the tower that we manipulate
                                #                           the color of the player currently playing
                                #                           the number of moves of the tower
                                heuristique = Heuristique.Heuristique(self.model)
                                heuristique.calculate_heuristique(tower, x, y,
                                                                  self.model.get_color(),
                                                                  amount_moves + 1)
                                self.heuristiques.append(heuristique)

        self.max_value()
        self.towers_to_examine.clear()

        # return max(heuristiques)

    def max_value(self):
        max_ = 0
        ref_heuristique = None
        for heuristique in self.heuristiques:
            if max_ < heuristique.sum:
                max_ = heuristique.sum
                ref_heuristique = heuristique

        self.model.ref = ref_heuristique.tower
        print(ref_heuristique.sum)
        self.model.decide_type_of_moving(ref_heuristique.x, ref_heuristique.y, ref_heuristique.distance, self.towers)

        self.heuristiques.clear()

    def min_value(self, tower):
        pass
