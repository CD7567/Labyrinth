import os
import sys
from random import randint
from cmd import Cmd

from utils.generator import Labyrinth
from utils.generator import dfs_generate
from utils.generator import save_csv
from utils.generator import load_csv
from utils.console_visualizer import print_labyrinth

class LabCmd(Cmd):
    prompt = "> "

    curr_labyrinth: Labyrinth
    curr_name: str

    def do_generate(self, args):
        x_bound, y_bound, name = args.rsplit(' ')

        self.curr_labyrinth = dfs_generate(int(x_bound), int(y_bound), ((randint(0, int(x_bound)) - 1), 0))
        self.curr_name = name
    
    def do_save(self, _):
        save_csv(self.curr_labyrinth, os.path.join(os.path.dirname(__file__), 'maps'), self.curr_name)

    def do_load(self, name):
        self.curr_labyrinth = load_csv(os.path.join(os.path.dirname(__file__), 'maps'), name)
        self.curr_name = name

    def do_focus(self, _):
        print(self.curr_name)
    
    def do_show(self, _):
        print_labyrinth(self.curr_labyrinth)

    def do_exit(self, _):
        return True

lab_cmd = LabCmd()
lab_cmd.cmdloop('Welcome to shell labyrinth generator!')