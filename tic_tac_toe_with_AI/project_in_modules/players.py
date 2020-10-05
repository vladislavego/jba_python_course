import random

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
