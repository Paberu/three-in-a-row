import re
import sys
from typing import Final
import os

from GameBoard import GameBoard

class GameMaster:
    """ Класс управления игрой. Содержит статус проверки пользовательского ввода и значение последнего хода. Отвечает
    за вывод игрового процесса на экран.

    Четыре значения для статуса проверки пользовательского ввода (USER_INPUT_NIL - начало игры, ни одного хода не было
    сделано, USER_INPUT_COORDINATES - пользователь ввёл верные координаты, USER_INPUT_COORDINATES_WRONG - пользователь
    ввёл неверные координаты, USER_INPUT_EXIT - пользователь выбрал выйти из игры, USER_INPUT_FAILED- пользователь
    выполнил неверный ввод).
    """
    USER_INPUT_NIL: Final = 0
    USER_INPUT_COORDINATES: Final = 1
    USER_INPUT_COORDINATES_WRONG: Final = 2
    USER_INPUT_EXIT: Final = 3
    USER_INPUT_FAILED: Final = 4

    def __init__(self):
        """ Создаёт и инициализирует два атрибута - запись последнего хода и статус проверки пользовательского хода.
        """
        self._last_move = ''
        self._user_input_status = self.USER_INPUT_NIL

    # КОМАНДЫ
    def display(self, board):
        os.system('cls' if os.name == 'nt' else 'clear')  # Очистка окна консоли
        if self._user_input_status in (self.USER_INPUT_COORDINATES_WRONG, self.USER_INPUT_FAILED):
            self.handle_bad_coordinates()
        print(board)
        moves, score, failed_attempts = board.get_counters()
        print(f'Moves: {moves}. Score: {score}. Failed attempts: {failed_attempts} of 5')

    @staticmethod
    def game_over():
        """ Выводит на экран информацию об окончании игры.

        :return: Ничего. Это функция вывода на экран.
        """
        os.system('cls' if os.name == 'nt' else 'clear')  # Очистка окна консоли
        print('Game Over')
        sys.exit()

    @staticmethod
    def handle_bad_coordinates():
        """ Выводит на экран сообщение о неверных координатах

        :return: Ничего. Это функция вывода на экран.
        """
        print('Coordinates aren\'t valid. Try again.')

    # ЗАПРОСЫ
    def check_user_input(self, user_input):
        """ Проверяет пользовательский ввод.

        :param user_input: Строка с пользовательским вводом.
        :return: Возвращает кортеж полученных значений (или пустой кортеж, если ввели неверные координаты).
        """
        pattern = r'^[A-H]\d+\s[A-H]\d+$'

        if user_input == 'EXIT':
            self._user_input_status = self.USER_INPUT_EXIT
            return set()

        if re.match(pattern, user_input):
            y1, x1, y2, x2 = GameBoard.get_coordinates_from_str(user_input)
            if GameBoard.validate_coordinates(y1, x1, y2, x2):
                self._user_input_status = self.USER_INPUT_COORDINATES
                return y1, x1, y2, x2

        self._user_input_status = self.USER_INPUT_FAILED
        return set()

    # ЗАПРОСЫ СТАТУСОВ
    def get_user_input_status(self):
        return self._user_input_status


if __name__ == '__main__':
    game_master = GameMaster()
    game_board = GameBoard()
    while True:
        game_board.remove_accidental_coincidences()
        game_master.display(game_board)
        coordinates_to_swap = game_master.check_user_input(input('Enter coordinates: ').upper().strip())
        if game_board.failed_game() or game_master.get_user_input_status() == game_master.USER_INPUT_EXIT:
            game_master.game_over()
        if game_master.get_user_input_status() in (game_master.USER_INPUT_FAILED, game_master.USER_INPUT_COORDINATES_WRONG):
            game_board.increase_failed_attempts_counter()
            continue
        if game_master.get_user_input_status() == game_master.USER_INPUT_COORDINATES:
            indexes = game_board.match_checker(coordinates_to_swap)
            if game_board.has_match():
                game_board.make_the_move(coordinates_to_swap, indexes)
