"""This file contains available labyrinth visual styles"""

"""Border styles"""

border_single = {'110011': '┌', '110001': '│',
                 '100010': '─', '101000': '─', '100011': '┌', '101001': '┐',
                 '101010': '─', '101011': '┬',
                 '010101': '│', '010111': '├',
                 '000001': '│', '000010': '─', '000011': '┌', '000100': '│',
                 '000101': '│', '000110': '└', '000111': '├',
                 '001000': '─', '001001': '┐', '001010': '─', '001011': '┬',
                 '001100': '┘', '001101': '┤', '001110': '┴', '001111': '┼'}

border_double = {'110011': '╔', '110001': '║',
                 '100010': '═', '101000': '═', '100011': '╔', '101001': '╗',
                 '101010': '═', '101011': '╦',
                 '010101': '║', '010111': '╠',
                 '000001': '║', '000010': '═', '000011': '╔', '000100': '║',
                 '000101': '║', '000110': '╚', '000111': '╠',
                 '001000': '═', '001001': '╗', '001010': '═', '001011': '╦',
                 '001100': '╝', '001101': '╣', '001110': '╩', '001111': '╬'}

border_styles = {'single': border_single, 'double': border_double}

"""Path styles"""

path_single = {-6: '┐', -5: '┌', -4: '┘', -3: '└',
               -2: '─', -1: '│'}

path_double = {-6: '╗', -5: '╔', -4: '╝', -3: '╚',
               -2: '═', -1: '║'}

path_styles = {'single': path_single, 'double': path_double}