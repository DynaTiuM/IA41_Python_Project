import grid


class Game:
    grid = 0
    game_mode = 0
    beginner = False
    selected_place = 0

    def __init__(self):
        self.ask()
        self.grid = grid.Grid()

    def ask(self):
        answer = ''
        while answer != 'solo' and 'ia':
            answer = input("Choose your mode, solo or ia :")
            if answer == 'solo':
                print("You chose solo mode")
                self.game_mode = 1
            elif answer == 'ia':
                print("You chose ia mode")
                self.game_mode = 2

        if self.game_mode == 1:
            answer = input("Would you like to begin the game ?")
            if answer == 'yes':
                self.beginner = True

            else:
                self.beginner = False

    def move(self):
        selected_placed = self.grid.cursor_place
        print(selected_placed)
