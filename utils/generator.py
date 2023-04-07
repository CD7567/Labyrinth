import sys
import os
from csv import writer
from csv import reader
from dataclasses import dataclass
from collections import deque
from random import choice
from random import randint
from typing import TypeAlias

@dataclass
class Cell:
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
    map: Field
    width: int
    height: int
    initial_cell: Coords
    finish_cell: Coords

def get_valid_neighbours(field: Field, coords: Coords) -> list[Coords]:
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

def dfs_generate(width: int, height: int, initial_cell: Coords) -> Labyrinth:
    field = [
                [
                    Cell() for i in range(height)
                ] for j in range(width)
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

    return Labyrinth(field, width, height, initial_cell, finish_cell)

def save_csv(labyrinth: Labyrinth, save_path: str, name: str):
    os.makedirs(save_path, exist_ok = True)
    with open(os.path.join(save_path, f'{name}.csv'), 'w') as file:
        wr = writer(file)
        wr.writerow([labyrinth.width, labyrinth.height])
        wr.writerow(labyrinth.initial_cell)
        wr.writerow(labyrinth.finish_cell)

        for row in zip(*labyrinth.map):
            wr.writerow(row)

def load_csv(load_path: str, name: str) -> Labyrinth:
    with open(os.path.join(load_path, f'{name}.csv'), 'r') as file:
        r = list(reader(file))
        labyrinth = Labyrinth([], int(r[0][0]), int(r[0][1]), (int(r[1][0]), int(r[1][1])), (int(r[2][0]), int(r[2][1])))

        for column in zip(*r[3:]):
            labyrinth.map.append([Cell(int(i[0]), int(i[1]), int(i[2]), int(i[3]), 0, int(i[4])) for i in column])

        return labyrinth

if __name__ == '__main__':
    initial_cell = (randint(0, int(sys.argv[1]) - 1), 0)
    labyrinth = dfs_generate(int(sys.argv[1]), int(sys.argv[2]), initial_cell)

    save_csv(labyrinth, os.path.join(os.path.dirname(__file__), '..', 'maps'), sys.argv[3])