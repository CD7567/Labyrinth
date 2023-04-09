'''This module provides shell functionality'''

import os
import re
import traceback
from datetime import datetime
from cmd import Cmd

from src.entities import Labyrinth
from src.generator import dfs_generate
from src.generator import wilson_generate
from src.generator import prim_generate
from src.generator import solve_labyrinth
from src.loader import save_csv
from src.loader import load_csv
from src.printer import print_labyrinth

generate = {'dfs' : dfs_generate, 'wilson' : wilson_generate, 'prim' : prim_generate}

class LabCmd(Cmd):
    '''This class represents interactive labyrinth shell'''
    prompt = "> "

    curr_labyrinth: Labyrinth = None
    curr_name: str = None

    def do_generate(self, args):
        '''This method provides generate command'''

        splitted_args = re.split(r'\s+', args)

        try:
            if len(splitted_args) == 3:
                splitted_args.append('dfs')
            elif len(splitted_args) < 3:
                print('*** Incorrect args set')
                return False

            x_bound, y_bound= int(splitted_args[0]), int(splitted_args[1])
        except ValueError:
            print('*** Incorrect args set')
            return False

        try:
            if splitted_args[3] in generate.keys():
                begin = datetime.now()
                self.curr_labyrinth = generate[splitted_args[3]](int(x_bound), int(y_bound))
                end = datetime.now()

                print('Labyrinth generated in:', '{:.3f}'.format((end - begin).microseconds / 1000), 'ms')
            else:
                print('*** Incorrect args set')
        except Exception:
            print(f'*** Internal exception: {traceback.format_exc()}')

        self.curr_name = splitted_args[2]

    def do_solve(self, _):
        '''This method provides solve command'''

        if self.curr_name is not None:
            begin = datetime.now()
            solved = solve_labyrinth(self.curr_labyrinth)
            end = datetime.now()

            print_labyrinth(Labyrinth(self.curr_labyrinth.algo,
                                      solved,
                                      self.curr_labyrinth.width,
                                      self.curr_labyrinth.height,
                                      self.curr_labyrinth.start_cell,
                                      self.curr_labyrinth.finish_cell))  

            print('Labyrinth solved in:', '{:.3f}'.format((end - begin).microseconds / 1000), 'ms')
        else:
            print('*** No labyrinth is focused')
            return False

    def do_save(self, args):
        '''This method provides save command'''

        splitted_args = re.split(r'\s+', args)

        if len(splitted_args) == 0:
            name = self.curr_name
        else:
            name = splitted_args[0]

        if self.curr_labyrinth is None:
            print('*** No labyrinth is focused')
            return False

        if os.path.isfile(os.path.join(os.path.dirname(__file__), 'maps', f'{name}.csv')):
            print(f'Save named {name} already exists, overwrite? [y/n]')

            if input() != 'y':
                return False

        save_csv(self.curr_labyrinth, os.path.join(os.path.dirname(__file__), 'maps'), name)
        print(f'Labyrinth \'{name}\' successfully saved')

    def do_load(self, args):
        '''This method provides solve command'''

        splitted_args = re.split(r'\s+', args)
        name = splitted_args[0]

        if os.path.isfile(os.path.join(os.path.dirname(__file__), 'maps', f'{name}.csv')):
            self.curr_labyrinth = load_csv(os.path.join(os.path.dirname(__file__), 'maps'), name)
            self.curr_name = name
            print(f'Labyrinth \'{self.curr_name}\' successfully loaded')
        else:
            print(f'*** Labyrinth \'{name}\' does not exist')

    def do_focus(self, _):
        '''This method provides focus command'''

        if self.curr_name is None:
            print('*** No labyrinth is focused')
        else:
            print(self.curr_name)

    def do_show(self, _):
        '''This method provides show command'''

        if self.curr_labyrinth is None:
            print('*** No labyrinth is focused')
        else:
            print_labyrinth(self.curr_labyrinth)

    def do_list(self, _):
        '''This method provides list command'''

        saves = []

        for file in os.listdir(os.path.join(os.path.dirname(__file__), 'maps')):
            saves.append(file.split('.')[0])

        print('Existing saves:', *saves, sep = '\n* ')

    def do_exit(self, _):
        '''This method provides exit command'''

        return True

lab_cmd = LabCmd()
lab_cmd.cmdloop('Welcome to shell labyrinth generator!')
