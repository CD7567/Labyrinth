import os
import re
from random import randint
from cmd import Cmd

from utils.generator import Labyrinth
from utils.generator import dfs_generate
from utils.generator import wilson_generate
from utils.generator import save_csv
from utils.generator import load_csv
from utils.console_visualizer import print_labyrinth

class LabCmd(Cmd):
    '''Class representing interactive labyrinth shell'''
    prompt = "> "

    curr_labyrinth: Labyrinth = None
    curr_name: str = None

    def do_generate(self, args):
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
            match splitted_args[3]:
                case 'dfs':
                    self.curr_labyrinth = dfs_generate(int(x_bound), int(y_bound), ((randint(0, int(x_bound)) - 1), 0))

                case 'wilson':
                    self.curr_labyrinth = wilson_generate(int(x_bound), int(y_bound), ((randint(0, int(x_bound)) - 1), 0))

                case _:
                    print('*** Incorrect args set')
        except Exception as exception:
            print(f'*** Internal exception: {str(exception)}')
    
        self.curr_name = splitted_args[2]

    def do_save(self, args):
        splitted_args = re.split(r'\s+', args)

        if len(splitted_args) == 0:
            name = splitted_args[0]
        else:
            name = self.curr_name

        if self.curr_labyrinth == None:
            print('*** No labyrinth is focused')
            return False

        if os.path.isfile(os.path.join(os.path.dirname(__file__), 'maps', f'{name}.csv')):
            print(f'Save named {name} already exists, overwrite? [y/n]')
            
            if input() != 'y':
                return False

        save_csv(self.curr_labyrinth, os.path.join(os.path.dirname(__file__), 'maps'), name)

    def do_load(self, args):
        splitted_args = re.split(r'\s+', args)
        name = splitted_args[0]

        if os.path.isfile(os.path.join(os.path.dirname(__file__), 'maps', f'{name}.csv')):
            self.curr_labyrinth = load_csv(os.path.join(os.path.dirname(__file__), 'maps'), name)
            self.curr_name = name
        else:
            print(f'*** Save named {name} does not exist')

    def do_focus(self, _):
        if self.curr_name == None:
            print('*** No labyrinth is focused')
        else:
            print(self.curr_name)

    def do_show(self, _):
        if self.curr_labyrinth == None:
            print('*** No labyrinth is focused')
        else:
            print_labyrinth(self.curr_labyrinth)

    def do_exit(self, _):
        return True

lab_cmd = LabCmd()
lab_cmd.cmdloop('Welcome to shell labyrinth generator!')