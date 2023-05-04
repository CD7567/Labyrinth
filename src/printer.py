"""This module contains printing algorithm"""

from termcolor import colored
from .entities import Labyrinth
from copy import deepcopy


class Printer:
    """Class for printing labyrinths in console"""
    def __init__(self, labyrinth: Labyrinth, conf: dict, styles: dict):
        self.__labyrinth = labyrinth

        self.__border = deepcopy(styles['border'][conf['BORDER_STYLE']])
        self.__path = deepcopy(styles['path'][conf['PATH_STYLE']])

        for k, v in self.__border.items():
            self.__border[k] = colored(v, conf['BORDER_COLOR'])

        for k, v in self.__path.items():
            self.__path[k] = colored(v, conf['PATH_COLOR'])

        self.__path.update({'0': ' ', '1': ' ',
                            '2': colored(conf['FINISH'], conf['FINISH_COLOR']),
                            '3': colored(conf['ENTRY'], conf['ENTRY_COLOR'])})

    def print_labyrinth(self) -> None:
        """Takes labyrinth and prints it into shell"""

        print(f'Labyrinth size: {self.__labyrinth.width}x{self.__labyrinth.height}')
        print(f'Start cell: {self.__labyrinth.start_cell}')
        print(f'Finish cell: {self.__labyrinth.finish_cell}')
        print(f'Algo: {self.__labyrinth.algo}', '\n')

        for j in range(self.__labyrinth.width):
            print(' ', self.__path['3'] if (j, 0) == self.__labyrinth.start_cell else ' ', sep='', end='')
        print(' ')

        for i in range(self.__labyrinth.height):
            if i == 0:
                for j in range(self.__labyrinth.width):
                    if j == 0:
                        print(self.__border['1100'
                                            + str(self.__labyrinth.field[j][i].top)
                                            + str(self.__labyrinth.field[j][i].left)],
                              self.__border['101010'] if self.__labyrinth.field[j][i].top else ' ',
                              sep='', end='')
                    else:
                        print(self.__border['10'
                                            + str(self.__labyrinth.field[j - 1][i].top)
                                            + '0' + str(self.__labyrinth.field[j][i].top)
                                            + str(self.__labyrinth.field[j][i].left)],
                              self.__border['101010'] if self.__labyrinth.field[j][i].top else ' ',
                              sep='', end='')

                print(self.__border['001001'] if self.__labyrinth.field[-1][i].top else self.__border['010101'])

            else:
                for j in range(self.__labyrinth.width):
                    if j == 0:
                        print(self.__border['010'
                                            + str(self.__labyrinth.field[j][i - 1].left)
                                            + str(self.__labyrinth.field[j][i].top)
                                            + str(self.__labyrinth.field[j][i].left)],
                              self.__border['101010'] if self.__labyrinth.field[j][i].top else ' ',
                              sep='', end='')
                    else:
                        print(self.__border['00'
                                            + str(self.__labyrinth.field[j - 1][i].top)
                                            + str(self.__labyrinth.field[j][i - 1].left)
                                            + str(self.__labyrinth.field[j][i].top)
                                            + str(self.__labyrinth.field[j][i].left)],
                              self.__border['101010'] if self.__labyrinth.field[j][i].top else ' ',
                              sep='', end='')

                print(self.__border['001101'] if self.__labyrinth.field[-1][i].top else self.__border['010101'])

            for j in range(self.__labyrinth.width):
                print(self.__border['010101'] if self.__labyrinth.field[j][i].left else ' ',
                      self.__path[self.__labyrinth.field[j][i].type],
                      sep='', end='')
            print(self.__border['010101'])

        for j in range(self.__labyrinth.width):
            print(self.__border['000110'] if j == 0 else (
                self.__border['001110'] if self.__labyrinth.field[j][-1].left else self.__border['101010']),
                  self.__border['101010'],
                  sep='', end='')
        print(self.__border['001100'])
