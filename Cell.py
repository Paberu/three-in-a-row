from random import choice
from typing import Final

CELL_VALUES: Final = ['A', 'B', 'C', 'D', 'E']


class Cell:
    """ Класс игровой ячейки, хранит одно из значений из массива возможных значений CELL_VALUE.

    В рамках консольного приложения содержит один атрибут _value и ряд служебных методов для отображения,
    сравнения и сериализации на случай необходимости.
    """

    def __init__(self):
        self._value = choice(CELL_VALUES)

    def get_value(self):
        return self._value

    def __eq__(self, other):
        if isinstance(other, Cell):
            return self._value == other._value
        return False

    def __str__(self):
        return self._value

    def __repr__(self):
        return self._value


class EmptyCell(Cell):
    """ Дочерний класс игровой ячейки, переопределяет содержимое атрибута на значение, эквивалентное пустой ячейке.
    Предназначен для придания ячейке статуса пустой.
    """

    def __init__(self):
        self._value = ' '


