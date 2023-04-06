import sys
import os
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

with open(os.path.join(os.path.curdir, '..', 'maps', f'{sys.argv[1]}.csv'), 'r') as file:
    r = list(reader(file))
    x_bound, y_bound = int(r[0][1]), int(r[0][0])

    print(f'Labyrinth size: {x_bound}x{y_bound}')
    print(f'Initial cell: ({int(r[1][0])}, {int(r[1][1])})')
    print(f'Finish cell: ({int(r[2][0])}, {int(r[2][1])})')

    print('\n')

    for j in range(x_bound):
        print(' ', '↓' if r[3][j][4] == '1' else ' ', sep = '', end = '')
    print(' ')

    for i in range(3, y_bound + 3):
        if (i == 3):
            for j in range(x_bound):
                if (j == 0):
                    print(cell_cross_delimiter['1100' + r[i][j][0] + r[i][j][2]],
                          '═' if r[i][j][0] == '1' else ' ',
                          sep = '', end = '')
                else:
                    print(cell_cross_delimiter['10' + r[i][j - 1][0] + '0' + r[i][j][0] + r[i][j][2]],
                          '═' if r[i][j][0] == '1' else ' ',
                          sep = '', end = '')
                    
            print('╗' if r[i][-1][0] == '1' else '║')

        else:
            for j in range(x_bound):
                if (j == 0):
                    print(cell_cross_delimiter['010' + r[i - 1][j][2] + r[i][j][0] + r[i][j][2]],
                          '═' if r[i][j][0] == '1' else ' ',
                          sep = '', end = '')
                else:
                    print(cell_cross_delimiter['00' + r[i][j - 1][0] + r[i - 1][j][2] + r[i][j][0] + r[i][j][2]],
                          '═' if r[i][j][0] == '1' else ' ',
                          sep = '', end = '')
                    
            print('╣' if r[i][-1][0] == '1' else '║')

        for j in range(x_bound):
            print('║' if r[i][j][2] == '1' else ' ',
                  cell_filler[r[i][j][4]],
                  sep = '', end = '')
        print('║')

    for j in range(x_bound):
        print('╚' if j == 0 else ('╩' if r[-1][j][2] == '1' else '═'),
              '═',
              sep = '', end = '')
    print('╝')