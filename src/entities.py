'''This module contains entities used in labyrinth'''

from dataclasses import dataclass
from typing import TypeAlias


@dataclass
class Cell:
    '''This class represents cell of labyrinth'''
    top: int = 1
    bottom: int = 1
    left: int = 1
    right: int = 1
    visited: int = 0
    type: int = 0

    def __str__(self):
        return f'{self.top}{self.bottom}{self.left}{self.right}{self.type}'


Coords: TypeAlias = tuple[int, int]
Field: TypeAlias = list[list[Cell]]


@dataclass
class Labyrinth:
    '''This class represents labyrinth'''
    algo: str
    field: Field
    width: int
    height: int
    start_cell: Coords
    finish_cell: Coords
