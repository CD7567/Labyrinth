import sys
import os
from csv import writer
from csv import reader
from dataclasses import dataclass
from collections import deque
from random import choice
from random import sample
from random import randint
from typing import TypeAlias

@dataclass
class Cell:
    '''Class representing cell of labyrinth'''
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
    '''Class representing labyrinth'''
    algo: str
    field: Field
    width: int
    height: int
    initial_cell: Coords
    finish_cell: Coords

def dfs_generate(width: int, height: int, initial_cell: Coords) -> Labyrinth:
    '''Takes field dimensions and generates labyrinth via DFS'''

    def get_valid_neighbours(field: Field, coords: Coords) -> list[Coords]:
        '''Takes field and one of its cells, returns valid non-visited neighbours'''
        x_bound, y_bound = len(field), len(field[0])
        result = []

        if coords[1] > 0 and not field[coords[0]][coords[1] - 1].visited:
            result.append((coords[0], coords[1] - 1))

        if coords[1] < y_bound - 1 and not field[coords[0]][coords[1] + 1].visited:
            result.append((coords[0], coords[1] + 1))

        if coords[0] > 0 and not field[coords[0] - 1][coords[1]].visited:
            result.append((coords[0] - 1, coords[1]))

        if coords[0] < x_bound - 1 and not field[coords[0] + 1][coords[1]].visited:
            result.append((coords[0] + 1, coords[1]))

        return result

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

        if len(neighbours) == 0:
            if curr_cell != initial_cell:
                if not met_end:
                    met_end = 1
                    dead_ends.append(curr_cell)
                path.pop()
            else:
                break
        else:
            met_end = 0
            next_cell = choice(neighbours)

            if curr_cell[0] < next_cell[0]:
                field[curr_cell[0]][curr_cell[1]].right = 0
                field[next_cell[0]][next_cell[1]].left = 0
            elif curr_cell[0] > next_cell[0]:
                field[curr_cell[0]][curr_cell[1]].left = 0
                field[next_cell[0]][next_cell[1]].right = 0
            elif curr_cell[1] < next_cell[1]:
                field[curr_cell[0]][curr_cell[1]].bottom = 0
                field[next_cell[0]][next_cell[1]].top = 0
            else:
                field[curr_cell[0]][curr_cell[1]].top = 0
                field[next_cell[0]][next_cell[1]].bottom = 0

            field[next_cell[0]][next_cell[1]].visited = 1
            path.append(next_cell)

    finish_cell = choice(dead_ends)
    field[finish_cell[0]][finish_cell[1]].type = 2

    return Labyrinth('dfs', field, width, height, initial_cell, finish_cell)

def wilson_generate(width: int, height: int, initial_cell: Coords) -> Labyrinth:
    '''Takes field dimensions and generates labyrinth via Wilson algorithm'''

    def get_valid_neighbours(field: Field, coords: Coords, failed_cells: list[Coords]) -> list[Coords]:
        '''Takes field and one of its cells, returns valid neighbours'''
        x_bound, y_bound = len(field), len(field[0])
        result = []

        if coords[1] > 0 and (coords[0], coords[1] - 1) not in failed_cells:
            result.append((coords[0], coords[1] - 1))

        if coords[1] < y_bound - 1 and (coords[0], coords[1] + 1) not in failed_cells:
            result.append((coords[0], coords[1] + 1))

        if coords[0] > 0 and (coords[0] - 1, coords[1]) not in failed_cells:
            result.append((coords[0] - 1, coords[1]))

        if coords[0] < x_bound - 1 and (coords[0] + 1, coords[1]) not in failed_cells:
            result.append((coords[0] + 1, coords[1]))

        return result

    field = [
                [
                    Cell() for i in range(height)
                ] for j in range(width)
            ]

    field[initial_cell[0]][initial_cell[1]].visited = 1
    field[initial_cell[0]][initial_cell[1]].type = 1
    field[initial_cell[0]][initial_cell[1]].top = 0

    unvisited_set = set([(i, j) for i in range(width) for j in range(height)])
    unvisited_set.remove(initial_cell)

    dead_ends = []

    while len(unvisited_set) > 0:
        base_cell = sample(unvisited_set, 1)[0]
        path = deque()
        failed_cells = []

        dead_ends.append(base_cell)
        path.append(base_cell)

        while True:
            if (len(path) == 0):
                break

            curr_cell = path[-1]
            next_cell = curr_cell
            neighbours = get_valid_neighbours(field, curr_cell, failed_cells)

            while len(neighbours) > 0 and next_cell in path:
                next_cell = choice(neighbours)
                neighbours.remove(next_cell)

            if len(neighbours) == 0 and next_cell in path:
                failed_cells.append(path.pop())
            else:
                path.append(next_cell)

                if field[next_cell[0]][next_cell[1]].visited == 1:
                    break

        while len(path) > 1:
            curr_cell = path.popleft()
            next_cell = path[0]
            field[curr_cell[0]][curr_cell[1]].visited = 1
            unvisited_set.remove(curr_cell)

            if curr_cell[0] < next_cell[0]:
                field[curr_cell[0]][curr_cell[1]].right = 0
                field[next_cell[0]][next_cell[1]].left = 0
            elif curr_cell[0] > next_cell[0]:
                field[curr_cell[0]][curr_cell[1]].left = 0
                field[next_cell[0]][next_cell[1]].right = 0
            elif curr_cell[1] < next_cell[1]:
                field[curr_cell[0]][curr_cell[1]].bottom = 0
                field[next_cell[0]][next_cell[1]].top = 0
            else:
                field[curr_cell[0]][curr_cell[1]].top = 0
                field[next_cell[0]][next_cell[1]].bottom = 0

    finish_cell = choice(dead_ends)
    field[finish_cell[0]][finish_cell[1]].type = 2
    return Labyrinth('wilson', field, width, height, initial_cell, finish_cell)

def save_csv(labyrinth: Labyrinth, save_path: str, name: str):
    '''Saves labyrinth in csv file'''
    os.makedirs(save_path, exist_ok = True)
    with open(os.path.join(save_path, f'{name}.csv'), 'w', encoding = 'utf-8') as file:
        file_writer = writer(file)
        file_writer.writerow([labyrinth.width, labyrinth.height])
        file_writer.writerow(labyrinth.initial_cell)
        file_writer.writerow(labyrinth.finish_cell)
        file_writer.writerow(labyrinth.algo)


        for row in zip(*labyrinth.field):
            file_writer.writerow(row)

def load_csv(load_path: str, name: str) -> Labyrinth:
    '''Loads labyrinth from csv file'''

    def join_str(string: list[chr]) -> str:
        result = ''

        for i in string:
            result += i

        return result

    with open(os.path.join(load_path, f'{name}.csv'), 'r', encoding = 'utf-8') as file:
        file_reader = list(reader(file))
        labyrinth = Labyrinth(join_str(file_reader[3]), [], int(file_reader[0][0]), int(file_reader[0][1]), (int(file_reader[1][0]), int(file_reader[1][1])), (int(file_reader[2][0]), int(file_reader[2][1])))

        for column in zip(*file_reader[4:]):
            labyrinth.field.append([Cell(int(i[0]), int(i[1]), int(i[2]), int(i[3]), 0, int(i[4])) for i in column])

        return labyrinth

if __name__ == '__main__':
    init_cell = (randint(0, int(sys.argv[1]) - 1), 0)
    lab = dfs_generate(int(sys.argv[1]), int(sys.argv[2]), init_cell)

    save_csv(lab, os.path.join(os.path.dirname(__file__), '..', 'maps'), sys.argv[3])