import random
import time


class GameField:

    def __init__(self, initial_state: list = None):
        if initial_state is None:
            self.state = list("         ")
        else:
            self.state = initial_state

    def __get_row_list(self):
        return [self.state[cell:cell+3] for cell in (0, 3, 6)]

    def __get_column_list(self):
        return [self.state[cell::-3] for cell in (6, 7, 8)]

    def print_game_field(self):
        field_state = self.__get_row_list()
        row_number = 3
        print()
        print("       ---------")
        for field_line in field_state:
            print(f"     {row_number} | {' '.join(field_line)} |")
            row_number -= 1
        print("       ---------")
        print("         1 2 3")

    def is_cell_empty(self, cell_coordinates: tuple):
        column, row = cell_coordinates
        field_state = self.__get_column_list()
        if field_state[column][row] == ' ':
            return True
        return False

    def __fill_cell(self, who_update, cell_coordinates: tuple):
        column, row = cell_coordinates
        field_state = self.__get_column_list()
        if who_update == 1:
            field_state[column][row] = 'X'
        elif who_update == 2:
            field_state[column][row] = 'O'
        self.state = field_state

    def __swap_rows_to_columns(self):
        field_lines = [[self.state[i][k] for i in range(3)] for k in (2, 1, 0)]
        self.state = [cell for line in field_lines for cell in line]

    def update_field_state(self, who_update, cell_coordinates: tuple):
        if self.is_cell_empty(cell_coordinates):
            self.__fill_cell(who_update, cell_coordinates)
            self.__swap_rows_to_columns()

    def __is_empty_cells(self):
        return any(cell == ' ' for cell in self.state)

    def __is_win_combination(self, win_combination: list):
        win_combination = win_combination
        rows = self.__get_row_list()
        columns = self.__get_column_list()
        is_win_row = any(row == win_combination for row in rows)
        is_win_column = any(column == win_combination for column in columns)
        x_or_o = win_combination[0]
        is_win_diagonal = all(rows[i][i] == x_or_o for i in range(3)) or all(columns[i][i] == x_or_o for i in range(3))
        return is_win_row or is_win_column or is_win_diagonal

    def check_status(self):
        x_win_combination = ['X', 'X', 'X']
        o_win_combination = ['O', 'O', 'O']
        if self.__is_win_combination(x_win_combination):
            return "X wins"
        if self.__is_win_combination(o_win_combination):
            return "O wins"
        if not self.__is_empty_cells():
            return "Draw"
        return "Game not finished"


class Players:

    players_number = 0

    def __new__(cls, player_type="user"):
        Players.players_number += 1
        if player_type == "user":
            user = object.__new__(User)
            User.users_number += 1
            user.class_number = User.users_number
            user.number = cls.players_number
            return user
        computer = object.__new__(Computer)
        Computer.computers_number += 1
        computer.class_number = Computer.computers_number
        computer.level = player_type
        computer.number = cls.players_number
        return computer


class User(Players):

    player_type = "user"
    users_number = 0

    def __init__(self, level=None):
        pass

    @staticmethod
    def __is_initial_correct(initial_cells: str) -> bool:
        correct_symbols = ['X', 'O', '_']
        correct_length = 9
        return all([cell in correct_symbols for cell in initial_cells]) and len(initial_cells) == correct_length

    def get_initial_field_state(self) -> list:
        initial_cells = (input("Enter cells: ")).upper()
        while not self.__is_initial_correct(initial_cells):
            initial_cells = input("Unknown sequence. Enter cells: ")
        return list(initial_cells.replace('_', ' '))

    @staticmethod
    def __is_coordinates_correct(cell_coordinates: list):
        correct_length = 2
        correct_values = ['1', '2', '3']
        if not ''.join(cell_coordinates).isdigit():
            print("You should enter numbers!")
            return False
        if len(cell_coordinates) != correct_length:
            print("You should enter exact two number!")
            return False
        if not all(coordinate in correct_values for coordinate in cell_coordinates):
            print("Coordinates should be from 1 to 3!")
            return False
        return True

    def ask_cell_coordinates(self) -> tuple:
        print()
        cell_coordinates = input('Enter the coordinates "column row": ').split()
        while not self.__is_coordinates_correct(cell_coordinates):
            cell_coordinates = input("Enter the coordinates: ").split()
        return int(cell_coordinates[0]) - 1, int(cell_coordinates[1]) - 1


class Computer(Players):

    player_type = "computer"
    computers_number = 0

    def __init__(self, level):
        level = level

    @staticmethod
    def __generate_cell_to_fill():
        return random.randint(0, 2), random.randint(0, 2)


class Game:

    def __init__(self):
        self.status = "Game not finished"

    def __update_status(self, game_field):
        self.status = game_field.check_status()

    @staticmethod
    def __generate_cell_to_fill():
        return random.randint(0, 2), random.randint(0, 2)

    @staticmethod
    def __is_correct_user_input(user_input: list):
        correct_parameters = ["easy", "user"]
        length = len(user_input)
        if length == 3 and user_input[0] == "start" and \
           user_input[1] in correct_parameters and user_input[2] in correct_parameters \
           or length == 1 and user_input[0] == "exit":
            return length
        return False

    @staticmethod
    def __get_user_choice():
        user_input = input("""Input "start player1 player2" to play.
player1 and player2 can only have "user" or "easy" value. 
For example: print "start easy easy" to watch AI battle.           
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
            return
        player_one_type, player_two_type = play
        player_one, player_two = Players(player_one_type), Players(player_two_type)
        game_field = GameField()
        game_field.print_game_field()
        self.__update_status(game_field)
        self.__start_game_cycle(game_field, player_one, player_two)
        print()
        if self.status == "Draw":
            print("Draw")
        elif self.status == "X wins":
            print("X wins")
        elif self.status == "O wins":
            print("O wins")

    def __start_game_cycle(self, game_field, player_one, player_two):
        while self.status == "Game not finished":
            self.__make_move(game_field, player_one)
            if self.status != "Game not finished":
                break
            self.__make_move(game_field, player_two)

    def __make_user_move(self, game_field, player):
        cell = player.ask_cell_coordinates()
        while not game_field.is_cell_empty(cell):
            print("This cell is occupied! Choose another one!")
            cell = player.ask_cell_coordinates()
        game_field.update_field_state(player.number, cell)

        game_field.print_game_field()
        self.__update_status(game_field)

    def __make_computer_move(self, game_field, player):
        cell = self.__generate_cell_to_fill()
        print()
        print(f'Making move level "{player.level}"...')
        time.sleep(2)
        while not game_field.is_cell_empty(cell):
            cell = self.__generate_cell_to_fill()
        game_field.update_field_state(player.number, cell)
        game_field.print_game_field()
        self.__update_status(game_field)

    def __make_move(self, game_field, player):
        if player.player_type == "user":
            self.__make_user_move(game_field, player)
        else:
            self.__make_computer_move(game_field, player)


game = Game()
game.start_game()
