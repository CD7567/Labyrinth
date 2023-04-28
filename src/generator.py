"""This module contains generating and solving algorithms"""

from collections import deque
from random import randint
from random import sample
from copy import deepcopy

from .entities import Coords
from .entities import Field
from .entities import Cell
from .entities import Labyrinth


class Generator:
    """Base class for generators"""

    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @width.setter
    def width(self, width: int) -> None:
        if width > 0:
            self._width = width
        else:
            raise ValueError('Width must be positive')

    @height.setter
    def height(self, height: int) -> None:
        if height > 0:
            self._height = height
        else:
            raise ValueError('Height must be positive')

    def reshape(self, width: int, height: int) -> None:
        """Changes both dimensions by a single function call"""
        if width > 0 and height > 0:
            self._width = width
            self._height = height
        else:
            raise ValueError('Dimensions must be positive')

    def generate(self) -> Labyrinth:
        pass


class DFSGenerator(Generator):
    """Class generating Labyrinth instances via DFS algorithm"""

    def __get_valid_neighbours(self, field: Field, coords: Coords) -> list[Coords]:
        """Takes field and one of its cells, returns valid non-visited neighbours"""
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

    def generate(self) -> Labyrinth:
        """Generate Labyrinth via DFS algorithm"""

        """Creating field"""
        field = [
            [
                Cell() for _ in range(self._height)
            ] for _ in range(self._width)
        ]

        """Choosing initial cell"""
        initial_cell = (randint(0, self.width - 1), 0)

        """Initializing required additional data"""
        dead_ends = []
        path = deque()
        met_end = 0

        """Embedding initial cell"""
        path.append(initial_cell)
        field[initial_cell[0]][initial_cell[1]].visited = 1
        field[initial_cell[0]][initial_cell[1]].type = '1'
        field[initial_cell[0]][initial_cell[1]].top = 0

        """DFS loop"""
        while True:
            curr_cell = path[-1]
            neighbours = self.__get_valid_neighbours(field, curr_cell)

            """Checking neighbours and embedding next cell"""
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

        """Picking finish cell"""
        finish_cell = sample(dead_ends, 1)[0]
        field[finish_cell[0]][finish_cell[1]].type = '2'

        return Labyrinth('dfs', field, self._width, self._height, initial_cell, finish_cell)


class WilsonGenerator(Generator):
    """Class generating Labyrinth instances via Wilson's algorithm"""

    def __get_valid_neighbours(self, field: Field, coords: Coords) -> list[Coords]:
        """Takes field and one of its cells, returns valid neighbours"""
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

    def generate(self) -> Labyrinth:
        """Generate Labyrinth via Wilson's algorithm"""
        field = [
            [
                Cell() for _ in range(self._height)
            ] for _ in range(self._width)
        ]

        initial_cell = (randint(0, self._width - 1), 0)

        field[initial_cell[0]][initial_cell[1]].visited = 1
        field[initial_cell[0]][initial_cell[1]].type = '1'
        field[initial_cell[0]][initial_cell[1]].top = 0

        unvisited_set = {(i, j) for i in range(self._width) for j in range(self._height)}
        unvisited_set.remove(initial_cell)

        dead_ends = []

        while len(unvisited_set) > 0:
            base_cell = sample(unvisited_set, 1)[0]
            path = deque()

            dead_ends.append(base_cell)
            path.append(base_cell)

            while True:
                curr_cell = path[-1]
                neighbours = self.__get_valid_neighbours(field, curr_cell)

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
        field[finish_cell[0]][finish_cell[1]].type = '2'

        return Labyrinth('wilson', field, self._width, self._height, initial_cell, finish_cell)


class PrimGenerator(Generator):
    """
        Class generating Labyrinth instances via Prim's algorithm
        Edge weights are calculated by random height map
    """

    def __get_valid_neighbours(self, field: Field, coords: Coords) -> list[Coords]:
        """Takes field and one of its cells, returns valid neighbours"""
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

    def generate(self) -> Labyrinth:
        """Generate Labyrinth via Prim's algorithm"""
        field = [
            [
                Cell() for _ in range(self._height)
            ] for _ in range(self._width)
        ]

        max_weight = self._width * self._height
        height_map = [[randint(1, max_weight)
                       for _ in range(self._height)] for _ in range(self._width)]

        initial_cell = (randint(1, self._width - 1), randint(0, self._height - 1))
        field[initial_cell[0]][initial_cell[1]].visited = 1

        possible_paths = []
        dead_ends = []

        for vertex in self.__get_valid_neighbours(field, initial_cell):
            possible_paths.append(
                (abs(height_map[vertex[0]][vertex[1]] - height_map[initial_cell[0]][initial_cell[1]]),
                 initial_cell,
                 vertex))

        while len(possible_paths) > 0:
            path = min(possible_paths)
            curr_cell = path[1]
            next_cell = path[2]

            field[next_cell[0]][next_cell[1]].visited = 1
            neighbours = self.__get_valid_neighbours(field, next_cell)

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

        start_cell = (randint(0, self._width - 1), 0)

        field[start_cell[0]][start_cell[1]].top = 0
        field[start_cell[0]][start_cell[1]].type = '1'

        if start_cell in dead_ends:
            dead_ends.remove(start_cell)

        finish_cell = sample(dead_ends, 1)[0]
        field[finish_cell[0]][finish_cell[1]].type = '2'

        return Labyrinth('prim', field, self._width, self._height, start_cell, finish_cell)


class Solver:
    """Class solving Labyrinth via DFS"""

    __cell_codes = {'02': '-1', '20': '-1',
                    '13': '-2', '31': '-2',
                    '12': '-3', '21': '-3',
                    '23': '-4', '32': '-4',
                    '01': '-5', '10': '-5',
                    '03': '-6', '30': '-6'}

    def __init__(self):
        pass

    def __get_valid_neighbours(self, field: Field, coords: Coords) -> list[Coords]:
        """Takes field and one of its cells, returns valid neighbours"""
        x_bound, y_bound = len(field), len(field[0])
        result = []

        if coords[1] > 0 \
                and not field[coords[0]][coords[1] - 1].visited \
                and not field[coords[0]][coords[1]].top:
            result.append((coords[0], coords[1] - 1))

        if coords[1] < y_bound - 1 \
                and not field[coords[0]][coords[1] + 1].visited \
                and not field[coords[0]][coords[1]].bottom:
            result.append((coords[0], coords[1] + 1))

        if coords[0] > 0 \
                and not field[coords[0] - 1][coords[1]].visited \
                and not field[coords[0]][coords[1]].left:
            result.append((coords[0] - 1, coords[1]))

        if coords[0] < x_bound - 1 \
                and not field[coords[0] + 1][coords[1]].visited \
                and not field[coords[0]][coords[1]].right:
            result.append((coords[0] + 1, coords[1]))

        return result

    def __get_relation(self, prev_cell: Coords, curr_cell: Coords, next_cell: Coords) -> str:
        relation = ''

        if prev_cell[0] < curr_cell[0]:
            relation += '3'
        elif prev_cell[0] > curr_cell[0]:
            relation += '1'
        elif prev_cell[1] < curr_cell[1]:
            relation += '2'
        else:
            relation += '0'

        if next_cell[0] < curr_cell[0]:
            relation += '3'
        elif next_cell[0] > curr_cell[0]:
            relation += '1'
        elif next_cell[1] < curr_cell[1]:
            relation += '2'
        else:
            relation += '0'

        return relation

    def solve(self, labyrinth: Labyrinth) -> Field:
        """Solve Labyrinth via DFS"""
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
            neighbours = self.__get_valid_neighbours(field, curr_cell)

            if len(neighbours) == 0:
                if curr_cell != start_cell:
                    path.pop()
                else:
                    break
            else:
                next_cell = sample(neighbours, 1)[0]

                field[next_cell[0]][next_cell[1]].visited = 1

                path.append(next_cell)

                if next_cell == labyrinth.finish_cell:
                    break

        field[path[0][0]][path[0][1]].type = self.__cell_codes[
            self.__get_relation((path[0][0], path[0][1] - 1), path[0], path[1])]

        for i in range(1, len(path) - 1):
            field[path[i][0]][path[i][1]].type = self.__cell_codes[self.__get_relation(path[i - 1], path[i], path[i + 1])]

        return field
