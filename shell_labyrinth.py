"""This module provides shell functionality"""

import os
import re
from datetime import datetime
from cmd import Cmd

from src.entities import Labyrinth
from src.generator import DFSGenerator
from src.generator import WilsonGenerator
from src.generator import PrimGenerator
from src.generator import Solver
from src.loader import Loader
from src.printer import Printer

generate = {'dfs': DFSGenerator, 'wilson': WilsonGenerator, 'prim': PrimGenerator}


class LabCmd(Cmd):
    """This class represents interactive labyrinth shell"""
    prompt = '> '

    curr_labyrinth: Labyrinth = None
    curr_name: str = None
    solver = Solver()
    loader = Loader(os.path.join(os.path.dirname(__file__), 'maps'))

    def do_generate(self, args):
        """This method provides generate command"""

        split_args = re.split(r'\s+', args)

        try:
            if len(split_args) == 3:
                split_args.append('dfs')
            elif len(split_args) < 3:
                print('*** Incorrect args set')
                return False

            x_bound, y_bound = int(split_args[0]), int(split_args[1])
        except ValueError:
            print('*** Incorrect args set')
            return False

        try:
            if split_args[3] in generate.keys():
                begin = datetime.now()
                self.curr_labyrinth = generate[split_args[3]](int(x_bound), int(y_bound)).generate()
                end = datetime.now()

                print('Labyrinth generated in:', '{:.3f}'.format((end - begin).microseconds / 1000), 'ms')
            else:
                print('*** Incorrect args set: No such generation algorithm')
        except ValueError as err:
            print(f'*** Incorrect args set: {err}')

        self.curr_name = split_args[2]

    def do_solve(self, _):
        """This method provides solve command"""

        if self.curr_name is not None:
            begin = datetime.now()
            solved = self.solver.solve(self.curr_labyrinth)
            end = datetime.now()

            Printer(Labyrinth(self.curr_labyrinth.algo,
                              solved,
                              self.curr_labyrinth.width,
                              self.curr_labyrinth.height,
                              self.curr_labyrinth.start_cell,
                              self.curr_labyrinth.finish_cell)
                    ).print_labyrinth()

            print('Labyrinth solved in:', '{:.3f}'.format((end - begin).microseconds / 1000), 'ms')
        else:
            print('*** No labyrinth is focused')
            return False

    def do_save(self, args):
        """This method provides save command"""

        split_args = re.split(r'\s+', args)

        if len(split_args) == 0:
            name = self.curr_name
        else:
            name = split_args[0]

        if self.curr_labyrinth is None:
            print('*** No labyrinth is focused')
            return False

        if os.path.isfile(os.path.join(os.path.dirname(__file__), 'maps', f'{name}.csv')):
            print(f'Save named {name} already exists, overwrite? [y/n]')

            if input() != 'y':
                return False

        self.loader.save_csv(self.curr_labyrinth, name)
        print(f'Labyrinth \'{name}\' successfully saved')

    def do_load(self, args):
        """This method provides solve command"""

        split_args = re.split(r'\s+', args)
        name = split_args[0]

        if os.path.isfile(os.path.join(os.path.dirname(__file__), 'maps', f'{name}.csv')):
            self.curr_labyrinth = self.loader.load_csv(name)
            self.curr_name = name
            print(f'Labyrinth \'{self.curr_name}\' successfully loaded')
        else:
            print(f'*** Labyrinth \'{name}\' does not exist')

    def do_focus(self, _):
        """This method provides focus command"""

        if self.curr_name is None:
            print('*** No labyrinth is focused')
        else:
            print(self.curr_name)

    def do_show(self, _):
        """This method provides show command"""

        if self.curr_labyrinth is None:
            print('*** No labyrinth is focused')
        else:
            Printer(self.curr_labyrinth).print_labyrinth()

    def do_list(self, _):
        """This method provides list command"""

        saves = []

        for file in os.listdir(os.path.join(os.path.dirname(__file__), 'maps')):
            saves.append(file.split('.')[0])

        print('Existing saves:', *saves, sep='\n* ')

    def do_exit(self, _):
        """This method provides exit command"""

        return True


lab_cmd = LabCmd()
lab_cmd.cmdloop('Welcome to shell labyrinth generator!')
