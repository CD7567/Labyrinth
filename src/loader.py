'''This module contains saving and loading algorithms'''

import os
from csv import reader
from csv import writer

from .entities import Cell
from .entities import Labyrinth

def save_csv(labyrinth: Labyrinth, save_path: str, name: str):
    '''Saves labyrinth in csv file'''

    os.makedirs(save_path, exist_ok = True)
    with open(os.path.join(save_path, f'{name}.csv'), 'w', encoding = 'utf-8') as file:
        file_writer = writer(file)
        file_writer.writerow([labyrinth.width, labyrinth.height])
        file_writer.writerow(labyrinth.start_cell)
        file_writer.writerow(labyrinth.finish_cell)
        file_writer.writerow(labyrinth.algo)


        for row in zip(*labyrinth.field):
            file_writer.writerow(row)

def load_csv(load_path: str, name: str) -> Labyrinth:
    '''Loads labyrinth from csv file'''

    with open(os.path.join(load_path, f'{name}.csv'), 'r', encoding = 'utf-8') as file:
        file_reader = list(reader(file))
        labyrinth = Labyrinth(''.join(file_reader[3]), [],
                                       int(file_reader[0][0]), int(file_reader[0][1]),
                                       (int(file_reader[1][0]), int(file_reader[1][1])),
                                       (int(file_reader[2][0]), int(file_reader[2][1])))

        for column in zip(*file_reader[4:]):
            labyrinth.field.append([Cell(int(i[0]), int(i[1]),
                                         int(i[2]), int(i[3]),
                                         0, int(i[4])) for i in column])

        return labyrinth
