import sys
import os
from csv import reader

with open(os.path.join(os.path.curdir, 'maps', f'{sys.argv[1]}.csv'), 'r') as file:
    r = list(reader(file))
    x_bound, y_bound = int(r[0][0]), int(r[0][1])

    print(f'Labyrinth size: {x_bound}x{y_bound}')
    print(f'Initial cell: ({int(r[1][0])}, {int(r[1][1])})')
    print(f'Finish cell: ({int(r[2][0])}, {int(r[2][1])})')


    print('._' * y_bound + '.')

    for row in r[3:]:
        for cell in row:
            print('.' if cell[2] == '0' else '|', ' ' if cell[1] == '0' else '_', sep = '', end = '')
            
        print('|')