import controller
import ia_mode_controller

class Game:
    game_mode = 0

    def __init__(self):
        self.gamemode = None
        self.controller = None
        self.ask()

    def ask(self):
        answer = ''
        while answer != ('solo' or 'ia'):
            answer = input("Choose your mode, solo or ia :")
            if answer == 'solo':
                print("You chose solo mode")
                self.game_mode = 1
            elif answer == 'ia':
                print("You chose ia mode")
                self.game_mode = 2

        if self.game_mode == 1:
            self.controller = controller.Controller(self.game_mode)
        else:
            self.controller = ia_mode_controller.IA_Mode_Controller(self.game_mode)
