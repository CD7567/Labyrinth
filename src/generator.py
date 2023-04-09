'''This module contains generating and solving algorithms'''

from collections import deque
from random import randint
from random import sample
from copy import deepcopy

from .entities import Coords
from .entities import Field
from .entities import Cell
from .entities import Labyrinth


def dfs_generate(width: int, height: int) -> Labyrinth:
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
            Cell() for _ in range(height)
        ] for _ in range(width)
    ]

    initial_cell = (randint(0, width - 1), 0)

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
            next_cell = sample(neighbours, 1)[0]

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

    finish_cell = sample(dead_ends, 1)[0]
    field[finish_cell[0]][finish_cell[1]].type = 2

    return Labyrinth('dfs', field, width, height, initial_cell, finish_cell)


def wilson_generate(width: int, height: int) -> Labyrinth:
    '''Takes field dimensions and generates labyrinth via Wilson's algorithm'''

    def get_valid_neighbours(field: Field, coords: Coords) -> list[Coords]:
        '''Takes field and one of its cells, returns valid neighbours'''
        x_bound, y_bound = len(field), len(field[0])
        result = []

        if coords[1] > 0 and (coords[0], coords[1] - 1):
            result.append((coords[0], coords[1] - 1))

        if coords[1] < y_bound - 1 and (coords[0], coords[1] + 1):
            result.append((coords[0], coords[1] + 1))

        if coords[0] > 0 and (coords[0] - 1, coords[1]):
            result.append((coords[0] - 1, coords[1]))

        if coords[0] < x_bound - 1 and (coords[0] + 1, coords[1]):
            result.append((coords[0] + 1, coords[1]))

        return result

    field = [
        [
            Cell() for _ in range(height)
        ] for _ in range(width)
    ]

    initial_cell = (randint(0, width - 1), 0)

    field[initial_cell[0]][initial_cell[1]].visited = 1
    field[initial_cell[0]][initial_cell[1]].type = 1
    field[initial_cell[0]][initial_cell[1]].top = 0

    unvisited_set = {(i, j) for i in range(width) for j in range(height)}
    unvisited_set.remove(initial_cell)

    dead_ends = []

    while len(unvisited_set) > 0:
        base_cell = sample(unvisited_set, 1)[0]
        path = deque()

        dead_ends.append(base_cell)
        path.append(base_cell)

        while True:
            curr_cell = path[-1]
            next_cell = curr_cell
            neighbours = get_valid_neighbours(field, curr_cell)

            next_cell = sample(neighbours, 1)[0]

            if next_cell in path:
                while path[-1] != next_cell:
                    path.pop()
            else:
                path.append(next_cell)

            if field[next_cell[0]][next_cell[1]].visited == 1:
                break

        if path[-1] in dead_ends:
            dead_ends.remove(path[-1])

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

    finish_cell = sample(dead_ends, 1)[0]
    field[finish_cell[0]][finish_cell[1]].type = 2

    return Labyrinth('wilson', field, width, height, initial_cell, finish_cell)


def prim_generate(width: int, height: int) -> Labyrinth:
    '''
        Takes field dimensions and generates labyrinth via Prim's algorithm
        Edge weights are calculated by random height map
    '''

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
            Cell() for j in range(height)
        ] for i in range(width)
    ]

    max_weight = width * height
    height_map = [[randint(1, max_weight)
                   for j in range(height)] for i in range(width)]

    initial_cell = (randint(1, width - 1), randint(0, height - 1))
    field[initial_cell[0]][initial_cell[1]].visited = 1

    possible_paths = []
    dead_ends = []

    for vertex in get_valid_neighbours(field, initial_cell):
        possible_paths.append(
            (abs(height_map[vertex[0]][vertex[1]] - height_map[initial_cell[0]][initial_cell[1]]),
             initial_cell,
             vertex))

    while len(possible_paths) > 0:
        path = min(possible_paths)
        curr_cell = path[1]
        next_cell = path[2]

        field[next_cell[0]][next_cell[1]].visited = 1
        neighbours = get_valid_neighbours(field, next_cell)

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

        for vertex in neighbours:
            possible_paths.append(
                (abs(height_map[vertex[0]][vertex[1]] - height_map[next_cell[0]][next_cell[1]]),
                 next_cell,
                 vertex))

        if len(neighbours) == 0:
            dead_ends.append(next_cell)

        possible_paths = [
            path for path in possible_paths if field[path[2][0]][path[2][1]].visited == 0]

    start_cell = (randint(0, width - 1), 0)

    field[start_cell[0]][start_cell[1]].top = 0
    field[start_cell[0]][start_cell[1]].type = 1

    if start_cell in dead_ends:
        dead_ends.remove(start_cell)

    finish_cell = sample(dead_ends, 1)[0]
    field[finish_cell[0]][finish_cell[1]].type = 2

    return Labyrinth('prim', field, width, height, start_cell, finish_cell)


def solve_labyrinth(labyrinth: Labyrinth) -> Field:
    '''Takes labyrinth and solves it via DFS'''

    def get_valid_neighbours(field: Field, coords: Coords) -> list[Coords]:
        '''Takes field and one of its cells, returns valid non-visited neighbours'''
        x_bound, y_bound = len(field), len(field[0])
        result = []

        if coords[1] > 0 and not field[coords[0]][coords[1] - 1].visited and not field[coords[0]][coords[1]].top:
            result.append((coords[0], coords[1] - 1))

        if coords[1] < y_bound - 1 and not field[coords[0]][coords[1] + 1].visited and not field[coords[0]][coords[1]].bottom:
            result.append((coords[0], coords[1] + 1))

        if coords[0] > 0 and not field[coords[0] - 1][coords[1]].visited and not field[coords[0]][coords[1]].left:
            result.append((coords[0] - 1, coords[1]))

        if coords[0] < x_bound - 1 and not field[coords[0] + 1][coords[1]].visited and not field[coords[0]][coords[1]].right:
            result.append((coords[0] + 1, coords[1]))

        return result

    field = deepcopy(labyrinth.field)
    start_cell = labyrinth.start_cell

    for i in range(len(field)):
        for j in range(len(field[0])):
            field[i][j].visited = 0

    path = deque()

    path.append(start_cell)
    field[start_cell[0]][start_cell[1]].visited = 1

    while True:
        curr_cell = path[-1]
        neighbours = get_valid_neighbours(field, curr_cell)

        if len(neighbours) == 0:
            if curr_cell != start_cell:
                path.pop()
            else:
                break
        else:
            next_cell = sample(neighbours, 1)[0]

            field[next_cell[0]][next_cell[1]].visited = 1

            if next_cell == labyrinth.finish_cell:
                break

            path.append(next_cell)

    for cell in path:
        field[cell[0]][cell[1]].type = -1

    return field
