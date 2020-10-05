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
