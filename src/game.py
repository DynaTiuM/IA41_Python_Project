import controller


class Game:
    def __init__(self):
        self.game_mode = None
        self.controller = None
        self.ask()

    def ask(self):
        answer = ''
        while answer != 'players' and answer != 'ia and player' and answer != 'ia':
            answer = input("Choose your mode, players, ia and player or ia :")
            if answer == 'players':
                print("You chose players mode")
                self.game_mode = 1
            if answer == 'ia and player':
                print("You chose ia and player mode")
                self.game_mode = 2
            if answer == 'ia':
                print("You chose ia mode")
                self.game_mode = 3

        self.controller = controller.Controller(self.game_mode)
