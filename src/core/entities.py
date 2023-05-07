"""This module contains entities used in labyrinth"""

from dataclasses import dataclass
from typing import TypeAlias


Coords: TypeAlias = tuple[int, int]


@dataclass
class Tile:
    """This class represents cell of labyrinth"""
    top: int = 1
    bottom: int = 1
    left: int = 1
    right: int = 1

    visited: int = 0
    type: str = '0'

    x: int = 0
    y: int = 0

    def __str__(self):
        return f'{self.top}{self.bottom}{self.left}{self.right}{self.type}'


Board: TypeAlias = list[list[Tile]]


@dataclass
class Labyrinth:
    """This class represents labyrinth"""
    algo: str
    board: Board
    width: int
    height: int
    start_tile: Coords
    finish_tile: Coords
