import controller

class Game:
    def __init__(self):
        self.game_mode = None
        self.controller = None
        self.ask()

    def ask(self):
        answer = ''
        while answer != 'players' and answer != 'ai and player' and answer != 'ais':
            answer = input("Choose your mode, players, ai and player or ais :")
            if answer == 'players':
                print("You chose players mode")
                self.game_mode = 1
            if answer == 'ai and player':
                print("You chose ia and player mode")
                self.game_mode = 2
            if answer == 'ais':
                print("You chose ais mode")
                self.game_mode = 3

        self.controller = controller.Controller(self.game_mode)
