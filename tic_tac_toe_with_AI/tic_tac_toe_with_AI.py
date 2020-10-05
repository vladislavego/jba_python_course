import random
import time


class GameField:

    def __init__(self, initial_state: list = None):
        if initial_state is None:
            self.state = list("         ")
        else:
            self.state = initial_state

    def get_row_list(self):
        return [self.state[cell:cell + 3] for cell in (0, 3, 6)]

    def get_column_list(self):
        return [self.state[cell::-3] for cell in (6, 7, 8)]

    def print_game_field(self):
        field_state = self.get_row_list()
        row_number = 3
        print()
        print("       ---------")
        for field_line in field_state:
            print(f"     {row_number} | {' '.join(field_line)} |")
            row_number -= 1
        print("       ---------")
        print("         1 2 3")

    def is_cell_empty(self, cell_coordinates: tuple) -> bool:
        column, row = cell_coordinates
        field_state = self.get_column_list()
        if field_state[column][row] == ' ':
            return True
        return False

    def __fill_cell(self, who_update: int, cell_coordinates: tuple):
        column, row = cell_coordinates
        field_state = self.get_column_list()
        if who_update % 2 == 1:
            field_state[column][row] = 'X'
        else:
            field_state[column][row] = 'O'
        self.state = field_state

    def __swap_rows_to_columns(self):
        field_lines = [[self.state[i][k] for i in range(3)] for k in (2, 1, 0)]
        self.state = [cell for line in field_lines for cell in line]

    def update_field_state(self, who_update: int, cell_coordinates: tuple):
        if self.is_cell_empty(cell_coordinates):
            self.__fill_cell(who_update, cell_coordinates)
            self.__swap_rows_to_columns()

    def __is_empty_cells(self) -> bool:
        return any(cell == ' ' for cell in self.state)

    def __is_win_combination(self, win_combination: list) -> bool:
        win_combination = win_combination
        rows = self.get_row_list()
        columns = self.get_column_list()
        is_win_row = any(row == win_combination for row in rows)
        is_win_column = any(column == win_combination for column in columns)
        x_or_o = win_combination[0]
        is_win_diagonal = all(rows[i][i] == x_or_o for i in range(3)) or all(columns[i][i] == x_or_o for i in range(3))
        return is_win_row or is_win_column or is_win_diagonal

    def check_status(self) -> str:
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

    def __new__(cls, game, player_type="user"):
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
        computer.game_field = game.game_field
        return computer


class User(Players):
    player_type = "user"
    users_number = 0

    @staticmethod
    def __is_initial_correct(initial_cells: str) -> bool:
        correct_symbols = {'X', 'O', '_'}
        correct_length = 9
        return all([cell in correct_symbols for cell in initial_cells]) and len(initial_cells) == correct_length

    def get_initial_field_state(self) -> list:
        initial_cells = (input("Enter cells: ")).upper()
        while not self.__is_initial_correct(initial_cells):
            initial_cells = input("Unknown sequence. Enter cells: ")
        return list(initial_cells.replace('_', ' '))

    @staticmethod
    def __is_coordinates_correct(cell_coordinates: list) -> bool:
        correct_length = 2
        correct_values = {'1', '2', '3'}
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

    def is_pre_win_cells(self, player_number: int) -> list:
        win_cells = []
        pre_win_cells = self.__find_interesting_cells(player_number)[0]
        for pre_win in pre_win_cells:
            win_cells.extend(pre_win)
        return win_cells

    def is_priority_cells(self, player_number: int) -> list:
        cells = []
        priority_cells = self.__find_interesting_cells(player_number)[1]
        for priority in priority_cells:
            cells.extend(priority)
        return cells

    def __find_interesting_cells(self, player_number: int) -> tuple:
        marker = 'X'
        if player_number % 2 == 0:
            marker = 'O'
        rows = self.game_field.get_row_list()
        columns = self.game_field.get_column_list()
        side_diagonal = [columns[i][i] for i in range(3)]
        main_diagonal = [rows[i][i] for i in range(3)]
        more_priority_cells = ()
        pre_win_cells = self.__find_pre_win_cells(marker, rows, columns, main_diagonal, side_diagonal)
        if self.level == "hard":
            more_priority_cells = self.__find_priority_cells(marker, rows, columns, main_diagonal, side_diagonal)
        return pre_win_cells, more_priority_cells

    @staticmethod
    def __find_pre_win_cells(marker, rows, columns, main_diagonal, side_diagonal):
        # line with index i in rows have i + 2 index in game_field
        # to get game_field line index: 2 - i
        is_pre_win_row = [(n, 2 - m) for m in range(3) for n in range(3)
                          if rows[m].count(marker) == 2 and rows[m][n] == ' ']
        is_pre_win_column = [(n, m) for m in range(3) for n in range(3)
                             if columns[n].count(marker) == 2 and columns[n][m] == ' ']
        is_pre_win_main_diagonal = [(i, 2 - i) for i in range(3)
                                    if main_diagonal.count(marker) == 2 and main_diagonal[i] == ' ']
        is_pre_win_side_diagonal = [(i, i) for i in range(3)
                                    if side_diagonal.count(marker) == 2 and side_diagonal[i] == ' ']
        return is_pre_win_row, is_pre_win_column, is_pre_win_main_diagonal, is_pre_win_side_diagonal

    @staticmethod
    def __find_priority_cells(marker, rows, columns, main_diagonal, side_diagonal):
        is_row_with_single_symbol = [(n, 2 - m) for m in range(3) for n in range(3)
                                     if rows[m].count(marker) == 1 and rows[m].count(' ') == 2 and
                                     rows[m][n] == ' ']
        is_column_with_single_symbol = [(n, m) for m in range(3) for n in range(3)
                                        if columns[n].count(marker) == 1 and columns[n].count(' ') == 2 and
                                        columns[n][m] == ' ']
        is_main_diagonal_with_single_symbol = [(i, 2 - i) for i in range(3)
                                               if main_diagonal.count(marker) == 1 and main_diagonal.count(' ') == 2 and
                                               main_diagonal[i] == ' ']
        is_side_diagonal_with_single_symbol = [(i, i) for i in range(3)
                                               if side_diagonal.count(marker) == 1 and side_diagonal.count(' ') == 2 and
                                               side_diagonal[i] == ' ']
        return is_row_with_single_symbol, is_column_with_single_symbol, \
            is_main_diagonal_with_single_symbol, is_side_diagonal_with_single_symbol

    @staticmethod
    def __generate_cell() -> tuple:
        return random.randint(0, 2), random.randint(0, 2)

    def generate_cell_to_fill(self) -> tuple:
        if self.level == "easy":
            return self.__generate_cell()
        win_cell = self.__generate_cell_medium()
        if win_cell:
            return win_cell
        if self.level == "hard":
            priority_cell = self.__generate_cell_hard()
            if priority_cell:
                return priority_cell
        return self.__generate_cell()

    def __generate_cell_medium(self) -> tuple:
        computer_win_cells = self.is_pre_win_cells(self.number)
        user_win_cells = self.is_pre_win_cells(self.number + 1)
        if computer_win_cells:
            cell = random.choice(computer_win_cells)
            computer_win_cells.remove(cell)
        elif user_win_cells:
            cell = random.choice(user_win_cells)
            user_win_cells.remove(cell)
        else:
            cell = ()
        return cell

    def __generate_cell_hard(self) -> tuple:
        computer_priority_cells = self.is_priority_cells(self.number)
        user_priority_cells = self.is_priority_cells(self.number + 1)
        if user_priority_cells:
            cell = random.choice(user_priority_cells)
            user_priority_cells.remove(cell)
        elif computer_priority_cells:
            cell = random.choice(computer_priority_cells)
            computer_priority_cells.remove(cell)
        else:
            cell = self.__generate_cell()
        return cell


class Game:

    def __init__(self):
        self.status = "Game not finished"
        self.game_field = GameField()

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
        player_one, player_two = Players(self, player_one_type), Players(self, player_two_type)
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


def play_again():
    print()
    play = ask_user_to_play()
    while play != 'n' and play != 'y':
        print()
        print("Choose 'y' to play or 'n' to exit")
        print()
        play = ask_user_to_play()
    if play == 'y':
        return True
    return False

def ask_user_to_play():
    return input("Play again? (y/n): ")

def start():
    game = Game()
    if not game.start_game():
        return
    while play_again():
        print()
        game = Game()
        if not game.start_game():
            return

start()
