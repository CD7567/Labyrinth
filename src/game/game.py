import pygame
import os
from math import ceil
from src.core.entities import Tile
from src.core.generator import generators
from src.game.views import TextView
from src.game.views import TextSwiper
from src.game.views import EditText
from src.game.views import Button


class Game:
    def __init__(self, assets_path: str, conf: dict):
        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

        self.width = self.window.get_width()
        self.height = self.window.get_height()
        self.assets_path = assets_path
        self.conf = conf
        self.scale = conf['SCALE']
        self.tile_dim = None
        self.skipping_to_menu = False

        self.background_spr = pygame.transform.scale(
            pygame.image.load(os.path.join(self.assets_path, 'background.png')),
            (self.width, self.height))

        pygame.display.set_caption('Labyrinth')

    def menu_loop(self):
        title_tv = TextView((self.width // 2, ceil(450 * self.scale)), 'Labyrinth', self.get_font(150),
                            self.conf['INTERFACE_COLOR'], self.window)
        play_btn = Button((self.width // 2, ceil(1100 * self.scale)), 'PLAY', self.get_font(75),
                          self.conf['INTERFACE_COLOR'], self.conf['BUTTON_FOCUS_COLOR'], self.window)
        settings_btn = Button((self.width // 2, ceil(1250 * self.scale)), 'SETTINGS', self.get_font(75),
                              self.conf['INTERFACE_COLOR'], self.conf['BUTTON_FOCUS_COLOR'], self.window)
        quit_btn = Button((self.width // 2, ceil(1400 * self.scale)), 'QUIT', self.get_font(75),
                          self.conf['INTERFACE_COLOR'], self.conf['BUTTON_FOCUS_COLOR'], self.window)

        views = [title_tv, play_btn, settings_btn, quit_btn]

        running = True
        while running:
            self.clock.tick(self.conf['FPS'])
            self.window.blit(self.background_spr, (0, 0))

            self.skipping_to_menu = False

            mouse_pos = pygame.mouse.get_pos()

            for view in views:
                view.update(mouse_pos)

            pygame.display.flip()

            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        running = False

                    case pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.creation_loop()
                        elif event.key == pygame.K_ESCAPE:
                            running = False

                    case pygame.MOUSEBUTTONDOWN:
                        if play_btn.check_hit(mouse_pos):
                            self.creation_loop()
                        elif settings_btn.check_hit(mouse_pos):
                            pass
                        elif quit_btn.check_hit(mouse_pos):
                            running = False

    def creation_loop(self):
        algo = 'dfs'
        width = 10
        height = 10

        title_tv = TextView((self.width // 2, ceil(450 * self.scale)), 'Configure your game', self.get_font(100),
                            self.conf['INTERFACE_COLOR'], self.window)

        type_tv = TextView((self.width // 2, ceil(800 * self.scale)), 'Game type', self.get_font(60),
                           self.conf['INTERFACE_COLOR'], self.window)

        type_sw = TextSwiper((self.width // 2, ceil(875 * self.scale)), ['singleplayer', 'multiplayer'], self.get_font(40),
                             self.conf['INTERFACE_COLOR'], self.conf['BUTTON_FOCUS_COLOR'], self.window)

        algo_tv = TextView((self.width // 2, ceil(1025 * self.scale)), 'Generation algorithm', self.get_font(60),
                           self.conf['INTERFACE_COLOR'], self.window)

        algo_sw = TextSwiper((self.width // 2, ceil(1100 * self.scale)), list(generators.keys()), self.get_font(40),
                             self.conf['INTERFACE_COLOR'], self.conf['BUTTON_FOCUS_COLOR'], self.window)

        width_tv = TextView((self.width // 2, ceil(1250 * self.scale)), 'Width', self.get_font(60),
                            self.conf['INTERFACE_COLOR'], self.window)

        width_et = EditText((self.width // 2, ceil(1325 * self.scale)), None, 'Enter width', self.get_font(40),
                            self.conf['INTERFACE_COLOR'], self.conf['BUTTON_FOCUS_COLOR'], self.window)

        height_tv = TextView((self.width // 2, ceil(1475 * self.scale)), 'Height', self.get_font(60),
                             self.conf['INTERFACE_COLOR'], self.window)

        height_et = EditText((self.width // 2, ceil(1550 * self.scale)), None, 'Enter height', self.get_font(40),
                             self.conf['INTERFACE_COLOR'], self.conf['BUTTON_FOCUS_COLOR'], self.window)

        start_btn = Button((self.width // 2 - ceil(450 * self.scale), ceil(1675 * self.scale)), 'START', self.get_font(60),
                           self.conf['INTERFACE_COLOR'], self.conf['BUTTON_FOCUS_COLOR'], self.window)

        quit_btn = Button((self.width // 2 + ceil(450 * self.scale), ceil(1675 * self.scale)), 'QUIT', self.get_font(60),
                          self.conf['INTERFACE_COLOR'], self.conf['BUTTON_FOCUS_COLOR'], self.window)

        views = [title_tv, type_tv, type_sw, algo_tv, algo_sw, width_tv, width_et, height_tv, height_et, start_btn,
                 quit_btn]

        running = True
        while running and not self.skipping_to_menu:
            self.clock.tick(self.conf['FPS'])
            self.window.blit(self.background_spr, (0, 0))

            mouse_pos = pygame.mouse.get_pos()

            for view in views:
                view.update(mouse_pos)

            pygame.display.flip()

            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        running = False

                    case pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.single_game_loop(algo, width, height)
                        elif event.key == pygame.K_ESCAPE:
                            if width_et.is_being_edited:
                                width_et.abort_editing()
                            elif height_et.is_being_edited:
                                height_et.abort_editing()
                            else:
                                running = False

                        elif event.key == pygame.K_RETURN:
                            if width_et.is_being_edited:
                                width_et.finish_editing()
                            elif height_et.is_being_edited:
                                height_et.finish_editing()
                        elif event.unicode:
                            if width_et.is_being_edited:
                                width_et.edit(event.unicode)
                            elif height_et.is_being_edited:
                                height_et.edit(event.unicode)

                    case pygame.MOUSEBUTTONDOWN:
                        if width_et.check_hit(mouse_pos):
                            width_et.start_editing()
                        elif width_et.is_being_edited:
                            width_et.finish_editing()

                        if height_et.check_hit(mouse_pos):
                            height_et.start_editing()
                        elif height_et.is_being_edited:
                            height_et.finish_editing()

                        if algo_sw.check_hit(mouse_pos):
                            algo_sw.swipe()
                        elif type_sw.check_hit(mouse_pos):
                            type_sw.swipe()
                        elif start_btn.check_hit(mouse_pos):
                            try:
                                if type_sw.text == 'singleplayer':
                                    self.single_game_loop(algo_sw.text, int(width_et.text), int(height_et.text))
                                else:
                                    self.multi_game_loop(algo_sw.text, int(width_et.text), int(height_et.text))
                            except:
                                pass
                        elif quit_btn.check_hit(mouse_pos):
                            running = False

    def single_game_loop(self, algo, width, height):
        labyrinth = generators[algo](width, height).generate()

        dim_x = 4 * self.width // 5 // labyrinth.width
        dim_y = self.height // labyrinth.height

        self.tile_dim = min(dim_x, dim_y)

        if self.height - labyrinth.height * self.tile_dim < 2 \
                or 4 * self.width // 5 - labyrinth.width * self.tile_dim < 2:
            self.tile_dim -= 1

        offset_x = 2 * self.width // 5 - (labyrinth.width * self.tile_dim) // 2
        offset_y = self.height // 2 - (labyrinth.height * self.tile_dim) // 2

        player_1_spr = pygame.transform.scale(pygame.image.load(os.path.join(self.assets_path, 'player_1.png')),
                                              (self.tile_dim, self.tile_dim))

        finish_sprite = pygame.transform.scale(pygame.image.load(os.path.join(self.assets_path, 'finish.png')),
                                               (self.tile_dim, self.tile_dim))

        player_x, player_y = labyrinth.start_tile
        click_counter = 0

        counter_title_tv = TextView((9 * self.width // 10, ceil(50 * self.scale)), 'Player steps', self.get_font(40),
                                    self.conf['INTERFACE_COLOR'], self.window)

        counter_tv = TextView((9 * self.width // 10, ceil(100 * self.scale)), '0', self.get_font(40),
                              self.conf['INTERFACE_COLOR'], self.window)

        quit_btn = Button((9 * self.width // 10, self.height - ceil(100 * self.scale)), 'QUIT', self.get_font(40),
                          self.conf['INTERFACE_COLOR'], self.conf['BUTTON_FOCUS_COLOR'], self.window)

        views = [counter_title_tv, counter_tv, quit_btn]

        running = True

        while running and not self.skipping_to_menu:
            self.clock.tick(self.conf['FPS'])
            self.window.blit(self.background_spr, (0, 0))

            mouse_pos = pygame.mouse.get_pos()

            pygame.draw.line(self.window,
                             self.conf['INTERFACE_COLOR'],
                             (4 * self.width // 5, 0),
                             (4 * self.width // 5, self.height),
                             2)

            for row in labyrinth.board:
                for tile in row:
                    self.draw_tile(tile, offset_x, offset_y)

            for view in views:
                view.update(mouse_pos)

            self.window.blit(player_1_spr,
                             (offset_x + player_x * self.tile_dim,
                              offset_y + player_y * self.tile_dim))
            self.window.blit(finish_sprite,
                             (offset_x + labyrinth.finish_tile[0] * self.tile_dim,
                              offset_y + labyrinth.finish_tile[1] * self.tile_dim))

            pygame.display.flip()

            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        running = False

                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_ESCAPE:
                                running = False
                                self.skipping_to_menu = True

                            case pygame.K_UP:
                                if not labyrinth.board[player_x][player_y].top \
                                        and (player_x, player_y) != labyrinth.start_tile:
                                    player_y -= 1
                                    click_counter += 1

                            case pygame.K_DOWN:
                                if not labyrinth.board[player_x][player_y].bottom:
                                    player_y += 1
                                    click_counter += 1

                            case pygame.K_LEFT:
                                if not labyrinth.board[player_x][player_y].left:
                                    player_x -= 1
                                    click_counter += 1

                            case pygame.K_RIGHT:
                                if not labyrinth.board[player_x][player_y].right:
                                    player_x += 1
                                    click_counter += 1

                        counter_tv.text = str(click_counter)

                    case pygame.MOUSEBUTTONDOWN:
                        if quit_btn.check_hit(mouse_pos):
                            running = False
                            self.skipping_to_menu = True

            if (player_x, player_y) == labyrinth.finish_tile:
                self.single_game_over_loop(click_counter)

    def multi_game_loop(self, algo, width, height):
        labyrinth = generators[algo](width, height).generate()

        dim_x = 4 * self.width // 5 // labyrinth.width
        dim_y = self.height // labyrinth.height

        self.tile_dim = min(dim_x, dim_y)

        if self.height - labyrinth.height * self.tile_dim < 2 \
                or 4 * self.width // 5 - labyrinth.width * self.tile_dim < 2:
            self.tile_dim -= 1

        offset_x = 2 * self.width // 5 - (labyrinth.width * self.tile_dim) // 2
        offset_y = self.height // 2 - (labyrinth.height * self.tile_dim) // 2

        player_1_spr = pygame.transform.scale(pygame.image.load(os.path.join(self.assets_path, 'player_1.png')),
                                              (self.tile_dim, self.tile_dim))
        player_2_spr = pygame.transform.scale(pygame.image.load(os.path.join(self.assets_path, 'player_2.png')),
                                              (self.tile_dim, self.tile_dim))
        player_1_m_spr = pygame.transform.scale(pygame.image.load(os.path.join(self.assets_path, 'player_1.png')),
                                                (self.tile_dim // 2, self.tile_dim // 2))
        player_2_m_spr = pygame.transform.scale(pygame.image.load(os.path.join(self.assets_path, 'player_2.png')),
                                                (self.tile_dim // 2, self.tile_dim // 2))
        finish_spr = pygame.transform.scale(pygame.image.load(os.path.join(self.assets_path, 'finish.png')),
                                            (self.tile_dim, self.tile_dim))

        player_1_x, player_1_y = labyrinth.start_tile
        player_2_x, player_2_y = labyrinth.start_tile
        click_counter_1 = 0
        click_counter_2 = 0

        counter_title_1_tv = TextView((9 * self.width // 10, ceil(50 * self.scale)), 'Player 1 steps', self.get_font(40),
                                      self.conf['INTERFACE_COLOR'], self.window)

        counter_1_tv = TextView((9 * self.width // 10, ceil(100 * self.scale)), '0', self.get_font(40),
                                self.conf['INTERFACE_COLOR'], self.window)

        counter_title_2_tv = TextView((9 * self.width // 10, ceil(200 * self.scale)), 'Player 2 steps', self.get_font(40),
                                      self.conf['INTERFACE_COLOR'], self.window)

        counter_2_tv = TextView((9 * self.width // 10, ceil(250 * self.scale)), '0', self.get_font(40 * self.scale),
                                self.conf['INTERFACE_COLOR'], self.window)

        quit_btn = Button((9 * self.width // 10, self.height - ceil(100 * self.scale)), 'QUIT', self.get_font(40),
                          self.conf['INTERFACE_COLOR'], self.conf['BUTTON_FOCUS_COLOR'], self.window)

        views = [counter_title_1_tv, counter_1_tv, counter_title_2_tv, counter_2_tv, quit_btn]

        running = True

        while running and not self.skipping_to_menu:
            self.clock.tick(self.conf['FPS'])
            self.window.blit(self.background_spr, (0, 0))

            mouse_pos = pygame.mouse.get_pos()

            pygame.draw.line(self.window,
                             self.conf['INTERFACE_COLOR'],
                             (4 * self.width // 5, 0),
                             (4 * self.width // 5, self.height),
                             2)

            for row in labyrinth.board:
                for tile in row:
                    self.draw_tile(tile, offset_x, offset_y)

            for view in views:
                view.update(mouse_pos)

            if player_1_x == player_2_x and player_1_y == player_2_y:
                self.window.blit(player_1_m_spr,
                                 (offset_x + self.tile_dim // 2 + player_1_x * self.tile_dim,
                                  offset_y + player_1_y * self.tile_dim))

                self.window.blit(player_2_m_spr,
                                 (offset_x + player_2_x * self.tile_dim,
                                  offset_y + self.tile_dim // 2 + player_2_y * self.tile_dim))
            else:
                self.window.blit(player_1_spr,
                                 (offset_x + player_1_x * self.tile_dim,
                                  offset_y + player_1_y * self.tile_dim))

                self.window.blit(player_2_spr,
                                 (offset_x + player_2_x * self.tile_dim,
                                  offset_y + player_2_y * self.tile_dim))

            self.window.blit(finish_spr,
                             (offset_x + labyrinth.finish_tile[0] * self.tile_dim,
                              offset_y + labyrinth.finish_tile[1] * self.tile_dim))

            pygame.display.flip()

            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        running = False

                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_ESCAPE:
                                running = False
                                self.skipping_to_menu = True

                            case pygame.K_UP:
                                if not labyrinth.board[player_1_x][player_1_y].top \
                                        and (player_1_x, player_1_y) != labyrinth.start_tile:
                                    player_1_y -= 1
                                    click_counter_1 += 1

                            case pygame.K_DOWN:
                                if not labyrinth.board[player_1_x][player_1_y].bottom:
                                    player_1_y += 1
                                    click_counter_1 += 1

                            case pygame.K_LEFT:
                                if not labyrinth.board[player_1_x][player_1_y].left:
                                    player_1_x -= 1
                                    click_counter_1 += 1

                            case pygame.K_RIGHT:
                                if not labyrinth.board[player_1_x][player_1_y].right:
                                    player_1_x += 1
                                    click_counter_1 += 1

                            case pygame.K_w:
                                if not labyrinth.board[player_2_x][player_2_y].top \
                                        and (player_2_x, player_2_y) != labyrinth.start_tile:
                                    player_2_y -= 1
                                    click_counter_2 += 1

                            case pygame.K_s:
                                if not labyrinth.board[player_2_x][player_2_y].bottom:
                                    player_2_y += 1
                                    click_counter_2 += 1

                            case pygame.K_a:
                                if not labyrinth.board[player_2_x][player_2_y].left:
                                    player_2_x -= 1
                                    click_counter_2 += 1

                            case pygame.K_d:
                                if not labyrinth.board[player_2_x][player_2_y].right:
                                    player_2_x += 1
                                    click_counter_2 += 1

                        counter_1_tv.text = str(click_counter_1)
                        counter_2_tv.text = str(click_counter_2)

                    case pygame.MOUSEBUTTONDOWN:
                        if quit_btn.check_hit(mouse_pos):
                            running = False
                            self.skipping_to_menu = True

            if (player_1_x, player_1_y) == labyrinth.finish_tile:
                self.multi_game_over_loop('Player 1', click_counter_1)
            elif (player_2_x, player_2_y) == labyrinth.finish_tile:
                self.multi_game_over_loop('Player 2', click_counter_2)

    def single_game_over_loop(self, steps):
        running = True

        winner_tv = TextView((self.width // 2, self.height // 2), f'You won with {steps} steps!', self.get_font(150),
                             self.conf['INTERFACE_COLOR'], self.window)

        while running:
            self.clock.tick(self.conf['FPS'])
            self.window.blit(self.background_spr, (0, 0))

            winner_tv.update(pygame.mouse.get_pos())

            pygame.display.flip()

            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        running = False
                        self.skipping_to_menu = True
                    case pygame.KEYDOWN:
                        running = False
                        self.skipping_to_menu = True

                    case pygame.MOUSEBUTTONDOWN:
                        running = False
                        self.skipping_to_menu = True

    def multi_game_over_loop(self, winner, steps):
        winner_tv = TextView((self.width // 2, self.height // 2), f'{winner} won with {steps} steps!', self.get_font(150),
                             self.conf['INTERFACE_COLOR'], self.window)

        running = True

        while running:
            self.clock.tick(self.conf['FPS'])
            self.window.blit(self.background_spr, (0, 0))

            winner_tv.update(pygame.mouse.get_pos())

            pygame.display.flip()

            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        running = False
                        self.skipping_to_menu = True

                    case pygame.KEYDOWN:
                        running = False
                        self.skipping_to_menu = True

                    case pygame.MOUSEBUTTONDOWN:
                        running = False
                        self.skipping_to_menu = True

    def draw_tile(self, tile: Tile, offset_x, offset_y):
        x = tile.x * self.tile_dim + offset_x
        y = tile.y * self.tile_dim + offset_y

        if tile.top:
            pygame.draw.line(self.window,
                             self.conf['INTERFACE_COLOR'],
                             (x, y),
                             (x + self.tile_dim, y),
                             2)
        if tile.bottom:
            pygame.draw.line(self.window,
                             self.conf['INTERFACE_COLOR'],
                             (x, y + self.tile_dim),
                             (x + self.tile_dim, y + self.tile_dim),
                             2)
        if tile.left:
            pygame.draw.line(self.window,
                             self.conf['INTERFACE_COLOR'],
                             (x, y),
                             (x, y + self.tile_dim),
                             2)
        if tile.right:
            pygame.draw.line(self.window,
                             self.conf['INTERFACE_COLOR'],
                             (x + self.tile_dim, y),
                             (x + self.tile_dim, y + self.tile_dim),
                             2)

    def get_font(self, size):
        return pygame.font.Font(os.path.join(self.assets_path, 'font.ttf'), ceil(size * self.scale))

    def play(self):
        self.menu_loop()
