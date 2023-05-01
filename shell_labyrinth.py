"""This module provides shell functionality"""

import os
import re
import json
from termcolor import COLORS
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
    conf: dict = None
    style: dict = None
    solver = Solver()
    lab_loader = Loader(os.path.join(os.path.dirname(__file__), 'maps'))

    def __init__(self):
        self.conf = Loader(os.path.join(os.path.dirname(__file__), 'conf')).load_json('conf')
        self.style = Loader(os.path.join(os.path.dirname(__file__), 'conf')).load_json('styles')

        super().__init__()

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
                              self.curr_labyrinth.finish_cell),
                    self.conf, self.style
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

        self.lab_loader.save_labyrinth_csv(self.curr_labyrinth, name)
        print(f'Labyrinth \'{name}\' successfully saved')

    def do_load(self, args):
        """This method provides solve command"""

        split_args = re.split(r'\s+', args)
        name = split_args[0]

        if os.path.isfile(os.path.join(os.path.dirname(__file__), 'maps', f'{name}.csv')):
            self.curr_labyrinth = self.lab_loader.load_labyrinth_csv(name)
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
            Printer(self.curr_labyrinth, self.conf, self.style).print_labyrinth()

    def do_list(self, _):
        """This method provides list command"""

        saves = []

        for file in os.listdir(os.path.join(os.path.dirname(__file__), 'maps')):
            saves.append(file.split('.')[0])

        print('Existing saves:', *saves, sep='\n* ')

    def do_configure(self, args):
        """This method provides configure command"""
        args = args.split()

        if args and args[0] == '--show':
            if args[0]:
                print(json.dumps(self.conf, sort_keys=True, indent=4, separators=(',', ': ')))
            else:
                print(f'No such flag was found: {args}')
        else:
            first_iter = 1

            while first_iter or input('\nContinue configurating? [y/n] ') == 'y':
                first_iter = 0
                print('Configurable properties:', *self.conf.keys(), sep='\n * ', end='\n\n')
                prop = input('Enter property name: ').upper()

                if prop in self.conf.keys():
                    match prop:
                        case 'BORDER_STYLE':
                            print('Available styles:', *self.style['border'].keys(), sep='\n * ', end='\n\n')
                            val = input('Enter desired value: ')

                            if val in self.style['border'].keys():
                                self.conf[prop] = val
                            else:
                                print('No such style was found')

                        case 'PATH_STYLE':
                            print('Available styles:', *self.style['border'].keys(), sep='\n * ', end='\n\n')
                            val = input('Enter desired value: ')

                            if val in self.style['path'].keys():
                                self.conf[prop] = val
                            else:
                                print('No such style was found')

                        case 'BORDER_COLOR' | 'PATH_COLOR' | 'ENTRY_COLOR' | 'FINISH_COLOR':
                            print('Available colors:', *COLORS.keys(), sep='\n * ', end='\n\n')
                            val = input('Enter desired value: ')

                            if val in COLORS.keys():
                                self.conf[prop] = val
                            else:
                                print('No such color was found')

                else:
                    print('Incorrect property name')

    def do_exit(self, _):
        """This method provides exit command"""
        last_conf = Loader(os.path.join(os.path.dirname(__file__), 'conf')).load_json('conf')

        if ((set(last_conf.items()) - set(self.conf.items())) or (set(self.conf.items()) - set(last_conf.items())))\
                and input('Save your current configuration? [y/n] ') == 'y':
            Loader(os.path.join(os.path.dirname(__file__), 'conf')).save_json('conf', self.conf)

        return True


lab_cmd = LabCmd()
lab_cmd.cmdloop('Welcome to shell labyrinth generator!')
