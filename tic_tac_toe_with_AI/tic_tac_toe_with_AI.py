class GameField:

    def __init__(self, initial_state: list):
        self.state = initial_state
        self.status = "Game not finished"

    def __get_row_list(self):
        return [[self.state[i] for i in range(k, k + 3)] for k in (0, 3, 6)]

    def __get_column_list(self):
        return [[self.state[i] for i in range(k, k - 7, -3)] for k in (6, 7, 8)]

    def print_game_field(self):
        field_state = self.__get_row_list()
        print("---------")
        for field_line in field_state:
            print(f"| {' '.join(field_line)} |")
        print("--------")

    def is_cell_empty(self, cell_coordinates: tuple):
        column, row = cell_coordinates
        field_state = self.__get_column_list()
        if field_state[column][row] == ' ':
            return True
        print("This cell is occupied! Choose another one!")
        return False

    def __fill_cell(self, cell_coordinates: tuple):
        column, row = cell_coordinates
        field_state = self.__get_column_list()
        if self.state.count('X') > self.state.count('O'):
            field_state[column][row] = 'O'
        else:
            field_state[column][row] = 'X'
        self.state = field_state

    def __swap_rows_to_columns(self):
        field_lines = [[self.state[i][k] for i in range(3)] for k in (2, 1, 0)]
        self.state = [cell for line in field_lines for cell in line]

    def update_field_state(self, cell_coordinates: tuple):
        if self.is_cell_empty(cell_coordinates):
            self.__fill_cell(cell_coordinates)
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
            self.status = "X wins"
            return "X wins"
        if self.__is_win_combination(o_win_combination):
            self.status = "O wins"
            return "O wins"
        if not self.__is_empty_cells():
            self.status = "Draw"
            return "Draw"


class Player:

    def __is_initial_correct(self, initial_cells: str) -> bool:
        correct_symbols = ['X', 'O', '_']
        correct_length = 9
        return all([cell in correct_symbols for cell in initial_cells]) and len(initial_cells) == correct_length

    def get_initial_field_state(self) -> list:
        initial_cells = (input("Enter cells: ")).upper()
        while not self.__is_initial_correct(initial_cells):
            initial_cells = input("Unknown sequence. Enter cells: ")
        return list(initial_cells.replace('_', ' '))

    def __is_coordinates_correct(self, cell_coordinates: list):
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


def start_game():
    player = Player()
    game_field = GameField(player.get_initial_field_state())
    game_field.print_game_field()
    game_field.check_status()
    while game_field.status == "Game not finished":
        cell = player.ask_cell_coordinates()
        if not game_field.is_cell_empty(cell):
            continue
        game_field.update_field_state(cell)
        game_field.print_game_field()
        game_field.check_status()
    status = game_field.status
    if status == "Draw":
        print("Draw")
    elif status == "X wins":
        print("X wins")
    elif status == "O wins":
        print("O wins")


start_game()

