try:
    import sys
    # import random
    # import math
    import os
    # import getopt
    import pygame as pg
    # import socket as sk
    # import pygame.locals as pglocals
    import handle_input as handlein
    import game_settings as gst
    from path_finding import A_star
except ImportError as err:
    print("Couldn't load module. %s" % (err))
    sys.exit(2)


#######################################################################
class Game:
    def __init__(self):
        # Setup screen configuration
        self.screen = None
        self.tittle = None
        self.is_running = True

        # Setup game zone
        self.maze = None
        self.flatmaze = None
        self.maze_size = None
        self.adjacent_nodes = None
        self.spawnpoint = None
        self.food_pos = None
        self.path = None

        # Setup level
        self.level = gst.LEVEL
        self.maze_input = gst.FILENAME

    def initialize(self):
        # Set screen
        pg.init()
        self.screen = pg.display.set_mode((gst.WIDTH, gst.HEIGHT))
        self.tittle = pg.display.set_caption('Pacman AI - 18CLC6')

        # Fill background
        self.background = pg.Surface(self.screen.get_size()).convert()
        self.background.fill((0, 0, 0))

        # Set maze
        self.maze_size, self.maze, self.spawnpoint = handlein.read_file(self.level, self.maze_input)
        self.flatmaze = self.flatten_maze(self.maze, self.maze_size)
        self.setup_maze(self.flatmaze, self.maze_size)

        # Set adjacent list and food
        self.adjacent_nodes, self.food = handlein.handle_adjacent(self.maze, self.maze_size)
        self.render_img(gst.FOOD_TYPE, gst.FOOD, self.food)

        # Set character
        self.render_img(gst.CHARACTER_TYPE, gst.MAIN_CHARACTER, self.spawnpoint)

        # Blit background to screen
        self.screen.blit(self.background, (0, 0))

    # Get rid of food
    def flatten_maze(self, maze, size):
        width, height = size
        return [[1 if maze[i][j] == 1 else 0 for j in range(width)] for i in range(height)]

    def load_image(self, type, name):
        """ Load image and return image object """
        fullname = os.path.join(gst.PATH, 'ASSET', type, name)
        try:
            image = pg.image.load(fullname)
            if image.get_alpha() is None:
                image = image.convert()
            else:
                image = image.convert_alpha()
        except pg.error as message:
            print('Cannot load image:', fullname)
            raise SystemExit(message)
        return image, image.get_rect()

    def render_img(self, type, image, pos):
        y_coor, x_coor = pos
        on_bg_pos = (x_coor * 32, y_coor * 32)
        cell_image, _ = self.load_image(type, image)
        self.background.blit(cell_image, on_bg_pos)

    def check_border(self, pos, size):
        width, height = size
        x, y = pos

        #############################################
        """WN x x x x x x x x N x x x x x x x x EN"""

        """W  x x x x x x x x x x x x x x x x x  E"""

        """WS x x x x x x x x S x x x x x x x x ES"""

        maze_pivots = [
                        (0, width - 1),               # East North 0
                        (height - 1, width - 1),      # East South 1
                        (0, 0),                       # West North 2
                        (height - 1, 0),              # West South 3
                        (x, width - 1),               # East       4
                        (x, 0),                       # West       5
                        (height - 1, y),              # South      6
                        (0, y)                        # North      7
                        ]

        for idx, direction in enumerate(maze_pivots):
            if pos == direction:
                return idx

        return -1

    def draw_cell(self, maze, pos, border_pos):
        cur_x_coor, cur_y_coor = pos

        if maze[cur_x_coor][cur_y_coor] != 1:
            self.render_img(gst.MAZE_TYPE, gst.MAZE_BLANK, pos)
            return

        """ Dict 1 """  """ Dict 2 """
        """ 0 : E  """  """ 0 : EN """
        """ 1 : W  """  """ 1 : ES """
        """ 2 : S  """  """ 2 : WN """
        """ 3 : N  """  """ 3 : WS """

        prime_direction = {0: (cur_x_coor, cur_y_coor + 1), 1: (cur_x_coor, cur_y_coor - 1),
                           2: (cur_x_coor + 1, cur_y_coor), 3: (cur_x_coor - 1, cur_y_coor)}

        sub_direction = {0: (cur_x_coor - 1, cur_y_coor + 1), 1: (cur_x_coor + 1, cur_y_coor + 1),
                         2: (cur_x_coor - 1, cur_y_coor - 1), 3: (cur_x_coor + 1, cur_y_coor - 1)}

        # Border or not?
        # EN
        if border_pos == 0:
            sub_x, sub_y = sub_direction[3]
            if maze[sub_x][sub_y] == 1:
                self.render_img(gst.MAZE_TYPE, gst.MAZE_BORDER_CONR_DL, pos)
            else:
                self.render_img(gst.MAZE_TYPE, gst.MAZE_BORDER_CONR_LD, pos)
        # ES
        elif border_pos == 1:
            sub_x, sub_y = sub_direction[2]
            if maze[sub_x][sub_y] == 1:
                self.render_img(gst.MAZE_TYPE, gst.MAZE_BORDER_CONR_UL, pos)
            else:
                self.render_img(gst.MAZE_TYPE, gst.MAZE_BORDER_CONR_LU, pos)
        # WN
        elif border_pos == 2:
            sub_x, sub_y = sub_direction[1]
            if maze[sub_x][sub_y] == 1:
                self.render_img(gst.MAZE_TYPE, gst.MAZE_BORDER_CONR_DR, pos)
            else:
                self.render_img(gst.MAZE_TYPE, gst.MAZE_BORDER_CONR_RD, pos)
        # WS
        elif border_pos == 3:
            sub_x, sub_y = sub_direction[0]
            if maze[sub_x][sub_y] == 1:
                self.render_img(gst.MAZE_TYPE, gst.MAZE_BORDER_CONR_UR, pos)
            else:
                self.render_img(gst.MAZE_TYPE, gst.MAZE_BORDER_CONR_RU, pos)
        # E
        elif border_pos == 4:
            prime_x, prime_y = prime_direction[1]

            if maze[prime_x][prime_y] == 0:
                self.render_img(gst.MAZE_TYPE, gst.MAZE_BORDER_EDGE_L, pos)
            else:
                sub_x_1, sub_y_1 = sub_direction[2]
                sub_x_2, sub_y_2 = sub_direction[3]
                if maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 0:
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_BORDER_INTRSE_L, pos)
                elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 0:
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_BORDER_INTRSE_UL, pos)
                elif maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 1:
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_BORDER_INTRSE_DL, pos)
                elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 1:
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_BORDER_INTRSE_EDGE_L, pos)
        # W
        elif border_pos == 5:
            prime_x, prime_y = prime_direction[0]

            if maze[prime_x][prime_y] == 0:
                self.render_img(gst.MAZE_TYPE, gst.MAZE_BORDER_EDGE_R, pos)
            else:
                sub_x_1, sub_y_1 = sub_direction[0]
                sub_x_2, sub_y_2 = sub_direction[1]
                if maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 0:
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_BORDER_INTRSE_R, pos)
                elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 0:
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_BORDER_INTRSE_UR, pos)
                elif maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 1:
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_BORDER_INTRSE_DR, pos)
                elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 1:
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_BORDER_INTRSE_EDGE_R, pos)
        # S
        elif border_pos == 6:
            prime_x, prime_y = prime_direction[3]

            if maze[prime_x][prime_y] == 0:
                self.render_img(gst.MAZE_TYPE, gst.MAZE_BORDER_EDGE_U, pos)
            else:
                sub_x_1, sub_y_1 = sub_direction[0]
                sub_x_2, sub_y_2 = sub_direction[2]
                if maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 0:
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_BORDER_INTRSE_U, pos)
                elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 0:
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_BORDER_INTRSE_RU, pos)
                elif maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 1:
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_BORDER_INTRSE_LU, pos)
                elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 1:
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_BORDER_INTRSE_EDGE_U, pos)
        # N
        elif border_pos == 7:
            prime_x, prime_y = prime_direction[2]

            if maze[prime_x][prime_y] == 0:
                self.render_img(gst.MAZE_TYPE, gst.MAZE_BORDER_EDGE_D, pos)
            else:
                sub_x_1, sub_y_1 = sub_direction[1]
                sub_x_2, sub_y_2 = sub_direction[3]
                if maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 0:
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_BORDER_INTRSE_D, pos)
                elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 0:
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_BORDER_INTRSE_RD, pos)
                elif maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 1:
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_BORDER_INTRSE_LD, pos)
                elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 1:
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_BORDER_INTRSE_EDGE_D, pos)
        else:
            adjacents = [False for _ in range(4)]
            for dir, coor in prime_direction.items():
                x, y = coor
                if maze[x][y] == 1:
                    adjacents[dir] = True

            # Not be surrounded
            if adjacents.count(True) == 0:
                self.render_img(gst.MAZE_TYPE, gst.MAZE_CENTER, pos)

            # 1 block surrounds
            elif adjacents.count(True) == 1:
                # E
                if adjacents == [True, False, False, False]:
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_HORIZONTAL_END_L, pos)
                # W
                elif adjacents == [False, True, False, False]:
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_HORIZONTAL_END_R, pos)
                # S
                elif adjacents == [False, False, True, False]:
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_VERTICAL_END_U, pos)
                # N
                elif adjacents == [False, False, False, True]:
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_VERTICAL_END_D, pos)

            # 2 blocks surround
            elif adjacents.count(True) == 2:
                # EW
                if adjacents == [True, True, False, False]:
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_HORIZONTAL, pos)
                # SN
                elif adjacents == [False, False, True, True]:
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_VERTICAL, pos)
                # ES
                elif adjacents == [True, False, True, False]:
                    sub_x, sub_y = sub_direction[1]
                    if maze[sub_x][sub_y] == 0:
                        self.render_img(gst.MAZE_TYPE, gst.MAZE_CONR_RD, pos)
                    else:
                        self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_CONR_RD, pos)
                # EN
                elif adjacents == [True, False, False, True]:
                    sub_x, sub_y = sub_direction[0]
                    if maze[sub_x][sub_y] == 0:
                        self.render_img(gst.MAZE_TYPE, gst.MAZE_CONR_RU, pos)
                    else:
                        self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_CONR_RU, pos)
                # WS
                elif adjacents == [False, True, True, False]:
                    sub_x, sub_y = sub_direction[3]
                    if maze[sub_x][sub_y] == 0:
                        self.render_img(gst.MAZE_TYPE, gst.MAZE_CONR_LD, pos)
                    else:
                        self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_CONR_LD, pos)
                # WN
                elif adjacents == [False, True, False, True]:
                    sub_x, sub_y = sub_direction[2]
                    if maze[sub_x][sub_y] == 0:
                        self.render_img(gst.MAZE_TYPE, gst.MAZE_CONR_LU, pos)
                    else:
                        self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_CONR_LU, pos)

            # 3 blocks surround
            elif adjacents.count(True) == 3:
                # EWS -> ES & WS
                if adjacents == [True, True, True, False]:
                    sub_x_1, sub_y_1 = sub_direction[1]
                    sub_x_2, sub_y_2 = sub_direction[3]
                    if maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 0:
                        self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_D, pos)
                    elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 0:
                        self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_LD, pos)
                    elif maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 1:
                        self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_RD, pos)
                    elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 1:
                        self.render_img(gst.MAZE_TYPE, gst.MAZE_INNER_D, pos)
                # EWN -> EN & WN
                elif adjacents == [True, True, False, True]:
                    sub_x_1, sub_y_1 = sub_direction[0]
                    sub_x_2, sub_y_2 = sub_direction[2]
                    if maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 0:
                        self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_U, pos)
                    elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 0:
                        self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_LU, pos)
                    elif maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 1:
                        self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_RU, pos)
                    elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 1:
                        self.render_img(gst.MAZE_TYPE, gst.MAZE_INNER_U, pos)
                # ESN -> EN & ES
                elif adjacents == [True, False, True, True]:
                    sub_x_1, sub_y_1 = sub_direction[0]
                    sub_x_2, sub_y_2 = sub_direction[1]
                    if maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 0:
                        self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_R, pos)
                    elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 0:
                        self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_DR, pos)
                    elif maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 1:
                        self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_UR, pos)
                    elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 1:
                        self.render_img(gst.MAZE_TYPE, gst.MAZE_INNER_R, pos)
                # WSN -> WN & WS
                elif adjacents == [False, True, True, True]:
                    sub_x_1, sub_y_1 = sub_direction[2]
                    sub_x_2, sub_y_2 = sub_direction[3]
                    if maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 0:
                        self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_L, pos)
                    elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 0:
                        self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_DL, pos)
                    elif maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 1:
                        self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_UL, pos)
                    elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 1:
                        self.render_img(gst.MAZE_TYPE, gst.MAZE_INNER_L, pos)

            # 4 blocks surroung
            elif adjacents.count(True) == 4:
                sub_x_1, sub_y_1 = sub_direction[0]
                sub_x_2, sub_y_2 = sub_direction[1]
                sub_x_3, sub_y_3 = sub_direction[2]
                sub_x_4, sub_y_4 = sub_direction[3]
                if (maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 0
                   and maze[sub_x_3][sub_y_3] == 0 and maze[sub_x_4][sub_y_4] == 0):
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_CENTER, pos)
                elif (maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 1
                      and maze[sub_x_3][sub_y_3] == 1 and maze[sub_x_4][sub_y_4] == 1):
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_BLANK, pos)
                elif (maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 1
                      and maze[sub_x_3][sub_y_3] == 1 and maze[sub_x_4][sub_y_4] == 0):
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_CENTER_LD, pos)
                elif (maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 1
                      and maze[sub_x_3][sub_y_3] == 0 and maze[sub_x_4][sub_y_4] == 1):
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_CENTER_LU, pos)
                elif (maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 0
                      and maze[sub_x_3][sub_y_3] == 1 and maze[sub_x_4][sub_y_4] == 1):
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_CENTER_RD, pos)
                elif (maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 1
                      and maze[sub_x_3][sub_y_3] == 1 and maze[sub_x_4][sub_y_4] == 1):
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_CENTER_RU, pos)
                elif (maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 1
                      and maze[sub_x_3][sub_y_3] == 0 and maze[sub_x_4][sub_y_4] == 0):
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_CENTER_R, pos)
                elif (maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 0
                      and maze[sub_x_3][sub_y_3] == 0 and maze[sub_x_4][sub_y_4] == 1):
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_CENTER_SYM_1, pos)
                elif (maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 0
                      and maze[sub_x_3][sub_y_3] == 1 and maze[sub_x_4][sub_y_4] == 1):
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_CENTER_L, pos)
                elif (maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 1
                      and maze[sub_x_3][sub_y_3] == 1 and maze[sub_x_4][sub_y_4] == 0):
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_CENTER_SYM_2, pos)
                elif (maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 1
                      and maze[sub_x_3][sub_y_3] == 0 and maze[sub_x_4][sub_y_4] == 1):
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_CENTER_D, pos)
                elif (maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 0
                      and maze[sub_x_3][sub_y_3] == 1 and maze[sub_x_4][sub_y_4] == 0):
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_CENTER_U, pos)
                elif (maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 0
                      and maze[sub_x_3][sub_y_3] == 0 and maze[sub_x_4][sub_y_4] == 0):
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_CENTER_UR, pos)
                elif (maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 0
                      and maze[sub_x_3][sub_y_3] == 0 and maze[sub_x_4][sub_y_4] == 1):
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_CENTER_DL, pos)
                elif (maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 0
                      and maze[sub_x_3][sub_y_3] == 1 and maze[sub_x_4][sub_y_4] == 0):
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_CENTER_UL, pos)
                elif (maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 1
                      and maze[sub_x_3][sub_y_3] == 0 and maze[sub_x_4][sub_y_4] == 0):
                    self.render_img(gst.MAZE_TYPE, gst.MAZE_INTRSE_CENTER_DR, pos)

    def setup_maze(self, maze, size):
        width, height = size
        for row_idx in range(height):
            for col_idx in range(width):
                border_pos = self.check_border((row_idx, col_idx), size)
                self.draw_cell(maze, (row_idx, col_idx), border_pos)

    def find_path(self):
        self.path = A_star(self.maze.maze, self.adjacent_nodes, self.spawnpoint, self.food)

    def execute(self):
        self.initialize()
        while self.is_running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return

            pg.display.flip()


if __name__ == '__main__':
    game = Game()
    game.execute()
