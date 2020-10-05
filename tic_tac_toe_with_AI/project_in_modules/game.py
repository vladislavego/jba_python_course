import random
import time

import game_field
import players

class Game:

    def __init__(self):
        self.status = "Game not finished"
        self.game_field = game_field.GameField()

    def __update_status(self):
        self.status = self.game_field.check_status()

    @staticmethod
    def __is_correct_user_input(user_input: list) -> int:
        correct_parameters = {"easy", "user", "medium", "hard"}
        length = len(user_input)
        play_game = length == 3 and user_input[0] == "start" and user_input[1] in correct_parameters and \
            user_input[2] in correct_parameters
        exit_game = length == 1 and user_input[0] == "exit"
        if play_game or exit_game:
            return length
        return 0

    @staticmethod
    def __get_user_choice():
        user_input = input("""Input "start player1 player2" to play.
player1 and player2 can only have "user", "easy", "medium" or "hard" value. 
For example: print "start easy easy" to watch AI battle.
To compete with it print "start user medium" if you want to move first or "start medium user" in other case. 
For hardcore choose "hard" opponent.          

Input "exit" to exit game.

Input command: """).split()
        return user_input

    def __ask_to_play(self):
        user_input = self.__get_user_choice()
        while not self.__is_correct_user_input(user_input) in (1, 3):
            print()
            print("Bad parameters")
            print()
            user_input = self.__get_user_choice()
        if self.__is_correct_user_input(user_input) == 3:
            return user_input[1::]
        else:
            return False

    def start_game(self):
        play = self.__ask_to_play()
        if not play:
            return False
        player_one_type, player_two_type = play
        player_one, player_two = players.Players(self, player_one_type), players.Players(self, player_two_type)
        self.game_field.print_game_field()
        self.__update_status()
        self.__start_game_cycle(player_one, player_two)
        print()
        if self.status == "Draw":
            print("Draw")
        elif self.status == "X wins":
            print("X wins")
        elif self.status == "O wins":
            print("O wins")
        return True 

    def __start_game_cycle(self, player_one, player_two):
        while self.status == "Game not finished":
            self.__make_move(player_one)
            if self.status != "Game not finished":
                break
            self.__make_move(player_two)

    def __make_user_move(self, player):
        cell = player.ask_cell_coordinates()
        while not self.game_field.is_cell_empty(cell):
            print("This cell is occupied! Choose another one!")
            cell = player.ask_cell_coordinates()
        self.game_field.update_field_state(player.number, cell)

        self.game_field.print_game_field()
        self.__update_status()

    def __make_computer_move(self, player):
        cell = player.generate_cell_to_fill()
        print()
        print(f'Making move level "{player.level}"...')
        while not self.game_field.is_cell_empty(cell):
            cell = player.generate_cell_to_fill()
        time.sleep(random.randint(2, 5))
        self.game_field.update_field_state(player.number, cell)
        self.game_field.print_game_field()
        self.__update_status()

    def __make_move(self, player):
        if player.player_type == "user":
            self.__make_user_move(player)
        else:
            self.__make_computer_move(player)
