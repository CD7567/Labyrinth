"""This module contains saving and loading algorithms"""

import os
import json
from csv import reader
from csv import writer

from .entities import Tile
from .entities import Labyrinth


class Loader:
    """Class for loading and saving app files"""
    def __init__(self, path: str) -> None:
        self.__path = path

    @property
    def path(self) -> str:
        return self.__path

    @path.setter
    def path(self, save_path: str) -> None:
        self.__path = save_path

    def save_labyrinth_csv(self, labyrinth: Labyrinth, name: str) -> None:
        """Saves labyrinth in csv file"""

        os.makedirs(self.__path, exist_ok=True)
        with open(os.path.join(self.__path, f'{name}.csv'), 'w', encoding='utf-8') as file:
            file_writer = writer(file)
            file_writer.writerow([labyrinth.width, labyrinth.height])
            file_writer.writerow(labyrinth.start_tile)
            file_writer.writerow(labyrinth.finish_tile)
            file_writer.writerow(labyrinth.algo)

            for row in zip(*labyrinth.board):
                file_writer.writerow(row)

    def load_labyrinth_csv(self, name: str) -> Labyrinth:
        """Loads labyrinth from csv file"""

        with open(os.path.join(self.__path, f'{name}.csv'), 'r', encoding='utf-8') as file:
            file_reader = list(reader(file))
            labyrinth = Labyrinth(''.join(file_reader[3]), [],
                                  int(file_reader[0][0]), int(file_reader[0][1]),
                                  (int(file_reader[1][0]), int(file_reader[1][1])),
                                  (int(file_reader[2][0]), int(file_reader[2][1])))

            for column in zip(*file_reader[4:]):
                labyrinth.board.append([Tile(int(i[0]), int(i[1]),
                                             int(i[2]), int(i[3]),
                                             i[4]) for i in column])

            return labyrinth

    def load_json(self, name: str) -> dict:
        """Loads json conf files"""
        with open(os.path.join(self.__path, f'{name}.json'), 'r', encoding='utf-8') as json_file:
            return json.load(json_file)

    def save_json(self, name: str, json_data: dict) -> None:
        """Saves json conf files"""
        with open(os.path.join(self.__path, f'{name}.json'), 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, sort_keys=True, indent=4, separators=(',', ': '))
