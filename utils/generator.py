import sys
import os
from csv import writer
from dataclasses import dataclass
from collections import deque
from random import choice
from random import randint

@dataclass
class Cell:
    top: bool = 1
    bottom: bool = 1
    left: bool = 1
    right: bool = 1
    visited: bool = 0
    type: int = 0

    def __str__(self):
        return f'{self.top}{self.bottom}{self.left}{self.right}{self.type}'

def get_valid_neighbours(field: list[list[Cell]], coords: list[int]) -> tuple[list[(int, int)], (int, int), (int, int)]:
    x_bound, y_bound = len(field), len(field[0])
    result = []

    if (coords[1] > 0 and not field[coords[0]][coords[1] - 1].visited):
        result.append((coords[0], coords[1] - 1))

    if (coords[1] < y_bound - 1 and not field[coords[0]][coords[1] + 1].visited):
        result.append((coords[0], coords[1] + 1))

    if (coords[0] > 0 and not field[coords[0] - 1][coords[1]].visited):
        result.append((coords[0] - 1, coords[1]))

    if (coords[0] < x_bound - 1 and not field[coords[0] + 1][coords[1]].visited):
        result.append((coords[0] + 1, coords[1]))

    return result

def dfs_generate(width: int, height: int, initial_cell: tuple[int, int]) -> list[list[Cell]]:
    field = [
                [
                    Cell() for i in range(width)
                ] for j in range(height)
            ]
    
    dead_ends = []
    path = deque()
    met_end = 0

    path.append(initial_cell)
    field[initial_cell[0]][initial_cell[1]].visited = 1
    field[initial_cell[0]][initial_cell[1]].type = 1
    field[initial_cell[0]][initial_cell[1]].top = 0

    while True:
        curr_cell = path[-1]
        neighbours = get_valid_neighbours(field, curr_cell)

        if (len(neighbours) == 0):
            if (curr_cell == initial_cell):
                break
            else:
                if (not met_end):
                    met_end = 1
                    dead_ends.append(curr_cell)
                path.pop()
        else:
            met_end = 0
            next_cell = choice(neighbours)

            if (curr_cell[0] < next_cell[0]):
                field[curr_cell[0]][curr_cell[1]].right = 0
                field[next_cell[0]][next_cell[1]].left = 0
            elif (curr_cell[0] > next_cell[0]):
                field[curr_cell[0]][curr_cell[1]].left = 0
                field[next_cell[0]][next_cell[1]].right = 0
            elif (curr_cell[1] < next_cell[1]):
                field[curr_cell[0]][curr_cell[1]].bottom = 0
                field[next_cell[0]][next_cell[1]].top = 0
            else:
                field[curr_cell[0]][curr_cell[1]].top = 0
                field[next_cell[0]][next_cell[1]].bottom = 0

            field[next_cell[0]][next_cell[1]].visited = 1
            path.append(next_cell)

    finish_cell = choice(dead_ends)
    field[finish_cell[0]][finish_cell[1]].type = 2

    return (field, initial_cell, finish_cell)

initial_cell = (randint(0, int(sys.argv[1]) - 1), 0)
labyrinth = dfs_generate(int(sys.argv[1]), int(sys.argv[2]), initial_cell)

os.makedirs(os.path.join(os.path.curdir, '..', 'maps'), exist_ok = True)
with open(os.path.join(os.path.curdir, '..', 'maps', f'{sys.argv[3]}.csv'), 'w') as file:
    wr = writer(file)
    wr.writerow([sys.argv[1], sys.argv[2]])
    wr.writerow(labyrinth[1])
    wr.writerow(labyrinth[2])

    for row in zip(*labyrinth[0]):
        wr.writerow(row)