import random


class GameField:

    def __init__(self, initial_state: list = None):
        if initial_state is None:
            self.state = list("         ")
        else:
            self.state = initial_state

    def __get_row_list(self):
        return [[self.state[i] for i in range(k, k + 3)] for k in (0, 3, 6)]

    def __get_column_list(self):
        return [[self.state[i] for i in range(k, k - 7, -3)] for k in (6, 7, 8)]

    def print_game_field(self):
        field_state = self.__get_row_list()
        print("---------")
        for field_line in field_state:
            print(f"| {' '.join(field_line)} |")
        print("---------")

    def is_cell_empty(self, cell_coordinates: tuple):
        column, row = cell_coordinates
        field_state = self.__get_column_list()
        if field_state[column][row] == ' ':
            return True
        return False

    def __fill_cell(self, who_update, cell_coordinates: tuple):
        column, row = cell_coordinates
        field_state = self.__get_column_list()
        if who_update == "computer":
            field_state[column][row] = 'O'
        elif who_update == "player":
            field_state[column][row] = 'X'
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


class Computer:
    def __init__(self):
        self.level = 'easy'

    @staticmethod
    def fill_cell():
        return random.randint(0, 2), random.randint(0, 2)


class Player:

    def __init__(self):
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
        cell_coordinates = input("Enter the coordinates: ").split()
        while not self.__is_coordinates_correct(cell_coordinates):
            cell_coordinates = input("Enter the coordinates: ").split()
        return int(cell_coordinates[0]) - 1, int(cell_coordinates[1]) - 1


class Game:

    def __init__(self):
        self.status = "Game not finished"

    def update_status(self, game_field):
        self.status = game_field.check_status()

    def start_game(self):
        player = Player()
        game_field = GameField()
        computer = Computer()
        game_field.print_game_field()
        self.update_status(game_field)
        self.start_game_cycle(game_field, player, computer)
        if self.status == "Draw":
            print("Draw")
        elif self.status == "X wins":
            print("X wins")
        elif self.status == "O wins":
            print("O wins")

    def start_game_cycle(self, game_field, player, computer):
        while self.status == "Game not finished":
            self.start_player(game_field, player)
            if self.status != "Game not finished":
                break
            self.start_computer(game_field, computer)

    def start_player(self, game_field, player):
        cell = player.ask_cell_coordinates()
        while not game_field.is_cell_empty(cell):
            print("This cell is occupied! Choose another one!")
            cell = player.ask_cell_coordinates()
        game_field.update_field_state("player", cell)
        game_field.print_game_field()
        self.update_status(game_field)

    def start_computer(self, game_field, computer):
        cell = computer.fill_cell()
        print(f'Making move level "{computer.level}"')
        while not game_field.is_cell_empty(cell):
            cell = computer.fill_cell()
        game_field.update_field_state("computer", cell)
        game_field.print_game_field()
        self.update_status(game_field)


game = Game()
game.start_game()
