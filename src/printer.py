"""This module contains printing algorithm"""

from .entities import Labyrinth


class Printer:
    __cell_filler = {-1: '*', 0: ' ', 1: ' ', 2: '¤'}
    __cell_cross_delimiter = {'110011': '╔', '110001': '║',
                              '100010': '═', '101000': '═', '100011': '╔', '101001': '╗',
                              '101010': '═', '101011': '╦',
                              '010101': '║', '010111': '╠',
                              '000001': '║', '000010': '═', '000011': '╔', '000100': '║',
                              '000101': '║', '000110': '╚', '000111': '╠',
                              '001000': '═', '001001': '╗', '001010': '═', '001011': '╦',
                              '001100': '╝', '001101': '╣', '001110': '╩', '001111': '╬'}

    def print_labyrinth(self, labyrinth: Labyrinth) -> None:
        """Takes labyrinth and prints it into shell"""

        print(f'Labyrinth size: {labyrinth.width}x{labyrinth.height}')
        print(f'Start cell: {labyrinth.start_cell}')
        print(f'Finish cell: {labyrinth.finish_cell}')
        print(f'Algo: {labyrinth.algo}', '\n')

        for j in range(labyrinth.width):
            print(' ', '↓' if (j, 0) == labyrinth.start_cell else ' ', sep='', end='')
        print(' ')

        for i in range(labyrinth.height):
            if i == 0:
                for j in range(labyrinth.width):
                    if j == 0:
                        print(self.__cell_cross_delimiter['1100'
                                                          + str(labyrinth.field[j][i].top)
                                                          + str(labyrinth.field[j][i].left)],
                              '═' if labyrinth.field[j][i].top else ' ',
                              sep='', end='')
                    else:
                        print(self.__cell_cross_delimiter['10'
                                                          + str(labyrinth.field[j - 1][i].top)
                                                          + '0' + str(labyrinth.field[j][i].top)
                                                          + str(labyrinth.field[j][i].left)],
                              '═' if labyrinth.field[j][i].top else ' ',
                              sep='', end='')

                print('╗' if labyrinth.field[-1][i].top else '║')

            else:
                for j in range(labyrinth.width):
                    if j == 0:
                        print(self.__cell_cross_delimiter['010'
                                                          + str(labyrinth.field[j][i - 1].left)
                                                          + str(labyrinth.field[j][i].top)
                                                          + str(labyrinth.field[j][i].left)],
                              '═' if labyrinth.field[j][i].top else ' ',
                              sep='', end='')
                    else:
                        print(self.__cell_cross_delimiter['00'
                                                          + str(labyrinth.field[j - 1][i].top)
                                                          + str(labyrinth.field[j][i - 1].left)
                                                          + str(labyrinth.field[j][i].top)
                                                          + str(labyrinth.field[j][i].left)],
                              '═' if labyrinth.field[j][i].top else ' ',
                              sep='', end='')

                print('╣' if labyrinth.field[-1][i].top else '║')

            for j in range(labyrinth.width):
                print('║' if labyrinth.field[j][i].left else ' ',
                      self.__cell_filler[labyrinth.field[j][i].type],
                      sep='', end='')
            print('║')

        for j in range(labyrinth.width):
            print('╚' if j == 0 else ('╩' if labyrinth.field[j][-1].left else '═'),
                  '═',
                  sep='', end='')
        print('╝')
