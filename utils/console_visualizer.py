import sys
import os
from generator import *
from csv import reader

cell_filler = {'0' : ' ', '1' : ' ', '2' : '¤'}
cell_cross_delimiter = {'110011' : '╔', '110001': '║',
                        '100010' : '═', '101000' : '═', '100011' : '╔', '101001' : '╗',
                        '101010' : '═', '101011' : '╦',
                        '010101' : '║', '010111' : '╠',
                        '000001' : '║', '000010' : '═', '000011' : '╔', '000100' : '║',
                        '000101' : '║', '000110' : '╚', '000111' : '╠',
                        '001000' : '═', '001001' : '╗', '001010' : '═', '001011' : '╦',
                        '001100' : '╝', '001101' : '╣', '001110' : '╩', '001111' : '╬'}

def print_labyrinth(labyrinth: Labyrinth):
    print(f'Labyrinth size: {labyrinth.width}x{labyrinth.height}')
    print(f'Initial cell: {labyrinth.initial_cell}')
    print(f'Finish cell: {labyrinth.finish_cell}')

    for j in range(labyrinth.width):
        print(' ', '↓' if labyrinth.map[j][0].type == 1 else ' ', sep = '', end = '')
    print(' ')

    for i in range(labyrinth.height):
        if (i == 0):
            for j in range(labyrinth.width):
                if (j == 0):
                    print(cell_cross_delimiter['1100' + str(labyrinth.map[j][i].top) + str(labyrinth.map[j][i].left)],
                          '═' if labyrinth.map[j][i].top else ' ',
                          sep = '', end = '')
                else:
                    print(cell_cross_delimiter['10' + str(labyrinth.map[j - 1][i].top) + '0' + str(labyrinth.map[j][i].top) + str(labyrinth.map[j][i].left)],
                          '═' if labyrinth.map[j][i].top else ' ',
                          sep = '', end = '')
                    
            print('╗' if labyrinth.map[-1][i].top else '║')

        else:
            for j in range(labyrinth.width):
                if (j == 0):
                    print(cell_cross_delimiter['010' + str(labyrinth.map[j][i - 1].left) + str(labyrinth.map[j][i].top) + str(labyrinth.map[j][i].left)],
                          '═' if labyrinth.map[j][i].top else ' ',
                          sep = '', end = '')
                else:
                    print(cell_cross_delimiter['00' + str(labyrinth.map[j - 1][i].top) + str(labyrinth.map[j][i - 1].left) + str(labyrinth.map[j][i].top) + str(labyrinth.map[j][i].left)],
                          '═' if labyrinth.map[j][i].top else ' ',
                          sep = '', end = '')
                    
            print('╣' if labyrinth.map[-1][i].top else '║')

        for j in range(labyrinth.width):
            print('║' if labyrinth.map[j][i].left else ' ',
                  cell_filler[str(labyrinth.map[j][i].type)],
                  sep = '', end = '')
        print('║')

    for j in range(labyrinth.width):
        print('╚' if j == 0 else ('╩' if labyrinth.map[j][-1].left else '═'),
              '═',
              sep = '', end = '')
    print('╝')

if __name__ == '__main__':
    labyrinth = load_csv(os.path.join(os.path.dirname(__file__), '..', 'maps'), sys.argv[1])

    print_labyrinth(labyrinth)