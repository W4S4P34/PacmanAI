import game_flags as flags
import handle_input as input
import pygame as pg


class MazeDrawer:
    def __init__(self, maze=None, size=None, background=None, background_rect=None):
        # Information
        self.maze = maze
        self.size = size
        self.background = background
        self.background_rect = background_rect

    # Get rid of food or monsters
    def flatten_maze(self, maze, size):
        width, height = size
        return [[1 if maze[i][j] == 1 else 0 for j in range(width)] for i in range(height)]

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
            input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_BLANK, pos)
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
                input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_BORDER_CONR_DL, pos)
            else:
                input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_BORDER_CONR_LD, pos)
        # ES
        elif border_pos == 1:
            sub_x, sub_y = sub_direction[2]
            if maze[sub_x][sub_y] == 1:
                input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_BORDER_CONR_UL, pos)
            else:
                input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_BORDER_CONR_LU, pos)
        # WN
        elif border_pos == 2:
            sub_x, sub_y = sub_direction[1]
            if maze[sub_x][sub_y] == 1:
                input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_BORDER_CONR_DR, pos)
            else:
                input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_BORDER_CONR_RD, pos)
        # WS
        elif border_pos == 3:
            sub_x, sub_y = sub_direction[0]
            if maze[sub_x][sub_y] == 1:
                input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_BORDER_CONR_UR, pos)
            else:
                input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_BORDER_CONR_RU, pos)
        # E
        elif border_pos == 4:
            prime_x, prime_y = prime_direction[1]

            if maze[prime_x][prime_y] == 0:
                input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_BORDER_EDGE_L, pos)
            else:
                sub_x_1, sub_y_1 = sub_direction[2]
                sub_x_2, sub_y_2 = sub_direction[3]
                if maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 0:
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_BORDER_INTRSE_L, pos)
                elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 0:
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_BORDER_INTRSE_UL, pos)
                elif maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 1:
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_BORDER_INTRSE_DL, pos)
                elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 1:
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_BORDER_INTRSE_EDGE_L, pos)
        # W
        elif border_pos == 5:
            prime_x, prime_y = prime_direction[0]

            if maze[prime_x][prime_y] == 0:
                input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_BORDER_EDGE_R, pos)
            else:
                sub_x_1, sub_y_1 = sub_direction[0]
                sub_x_2, sub_y_2 = sub_direction[1]
                if maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 0:
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_BORDER_INTRSE_R, pos)
                elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 0:
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_BORDER_INTRSE_UR, pos)
                elif maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 1:
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_BORDER_INTRSE_DR, pos)
                elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 1:
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_BORDER_INTRSE_EDGE_R, pos)
        # S
        elif border_pos == 6:
            prime_x, prime_y = prime_direction[3]

            if maze[prime_x][prime_y] == 0:
                input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_BORDER_EDGE_U, pos)
            else:
                sub_x_1, sub_y_1 = sub_direction[0]
                sub_x_2, sub_y_2 = sub_direction[2]
                if maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 0:
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_BORDER_INTRSE_U, pos)
                elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 0:
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_BORDER_INTRSE_RU, pos)
                elif maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 1:
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_BORDER_INTRSE_LU, pos)
                elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 1:
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_BORDER_INTRSE_EDGE_U, pos)
        # N
        elif border_pos == 7:
            prime_x, prime_y = prime_direction[2]

            if maze[prime_x][prime_y] == 0:
                input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_BORDER_EDGE_D, pos)
            else:
                sub_x_1, sub_y_1 = sub_direction[1]
                sub_x_2, sub_y_2 = sub_direction[3]
                if maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 0:
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_BORDER_INTRSE_D, pos)
                elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 0:
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_BORDER_INTRSE_RD, pos)
                elif maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 1:
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_BORDER_INTRSE_LD, pos)
                elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 1:
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_BORDER_INTRSE_EDGE_D, pos)
        else:
            adjacents = [False for _ in range(4)]
            for dir, coor in prime_direction.items():
                x, y = coor
                if maze[x][y] == 1:
                    adjacents[dir] = True

            # Not be surrounded
            if adjacents.count(True) == 0:
                input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_CENTER, pos)

            # 1 block surrounds
            elif adjacents.count(True) == 1:
                # E
                if adjacents == [True, False, False, False]:
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_HORIZONTAL_END_L, pos)
                # W
                elif adjacents == [False, True, False, False]:
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_HORIZONTAL_END_R, pos)
                # S
                elif adjacents == [False, False, True, False]:
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_VERTICAL_END_U, pos)
                # N
                elif adjacents == [False, False, False, True]:
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_VERTICAL_END_D, pos)

            # 2 blocks surround
            elif adjacents.count(True) == 2:
                # EW
                if adjacents == [True, True, False, False]:
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_HORIZONTAL, pos)
                # SN
                elif adjacents == [False, False, True, True]:
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_VERTICAL, pos)
                # ES
                elif adjacents == [True, False, True, False]:
                    sub_x, sub_y = sub_direction[1]
                    if maze[sub_x][sub_y] == 0:
                        input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_CONR_RD, pos)
                    else:
                        input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_CONR_RD, pos)
                # EN
                elif adjacents == [True, False, False, True]:
                    sub_x, sub_y = sub_direction[0]
                    if maze[sub_x][sub_y] == 0:
                        input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_CONR_RU, pos)
                    else:
                        input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_CONR_RU, pos)
                # WS
                elif adjacents == [False, True, True, False]:
                    sub_x, sub_y = sub_direction[3]
                    if maze[sub_x][sub_y] == 0:
                        input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_CONR_LD, pos)
                    else:
                        input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_CONR_LD, pos)
                # WN
                elif adjacents == [False, True, False, True]:
                    sub_x, sub_y = sub_direction[2]
                    if maze[sub_x][sub_y] == 0:
                        input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_CONR_LU, pos)
                    else:
                        input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_CONR_LU, pos)

            # 3 blocks surround
            elif adjacents.count(True) == 3:
                # EWS -> ES & WS
                if adjacents == [True, True, True, False]:
                    sub_x_1, sub_y_1 = sub_direction[1]
                    sub_x_2, sub_y_2 = sub_direction[3]
                    if maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 0:
                        input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_D, pos)
                    elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 0:
                        input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_LD, pos)
                    elif maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 1:
                        input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_RD, pos)
                    elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 1:
                        input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INNER_D, pos)
                # EWN -> EN & WN
                elif adjacents == [True, True, False, True]:
                    sub_x_1, sub_y_1 = sub_direction[0]
                    sub_x_2, sub_y_2 = sub_direction[2]
                    if maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 0:
                        input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_U, pos)
                    elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 0:
                        input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_LU, pos)
                    elif maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 1:
                        input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_RU, pos)
                    elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 1:
                        input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INNER_U, pos)
                # ESN -> EN & ES
                elif adjacents == [True, False, True, True]:
                    sub_x_1, sub_y_1 = sub_direction[0]
                    sub_x_2, sub_y_2 = sub_direction[1]
                    if maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 0:
                        input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_R, pos)
                    elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 0:
                        input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_DR, pos)
                    elif maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 1:
                        input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_UR, pos)
                    elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 1:
                        input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INNER_R, pos)
                # WSN -> WN & WS
                elif adjacents == [False, True, True, True]:
                    sub_x_1, sub_y_1 = sub_direction[2]
                    sub_x_2, sub_y_2 = sub_direction[3]
                    if maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 0:
                        input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_L, pos)
                    elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 0:
                        input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_DL, pos)
                    elif maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 1:
                        input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_UL, pos)
                    elif maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 1:
                        input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INNER_L, pos)

            # 4 blocks surroung
            elif adjacents.count(True) == 4:
                sub_x_1, sub_y_1 = sub_direction[0]
                sub_x_2, sub_y_2 = sub_direction[1]
                sub_x_3, sub_y_3 = sub_direction[2]
                sub_x_4, sub_y_4 = sub_direction[3]
                if (maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 0
                   and maze[sub_x_3][sub_y_3] == 0 and maze[sub_x_4][sub_y_4] == 0):
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_CENTER, pos)
                elif (maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 1
                      and maze[sub_x_3][sub_y_3] == 1 and maze[sub_x_4][sub_y_4] == 1):
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_BLANK, pos)
                elif (maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 1
                      and maze[sub_x_3][sub_y_3] == 1 and maze[sub_x_4][sub_y_4] == 0):
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_CENTER_LD, pos)
                elif (maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 1
                      and maze[sub_x_3][sub_y_3] == 0 and maze[sub_x_4][sub_y_4] == 1):
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_CENTER_LU, pos)
                elif (maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 0
                      and maze[sub_x_3][sub_y_3] == 1 and maze[sub_x_4][sub_y_4] == 1):
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_CENTER_RD, pos)
                elif (maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 1
                      and maze[sub_x_3][sub_y_3] == 1 and maze[sub_x_4][sub_y_4] == 1):
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_CENTER_RU, pos)
                elif (maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 1
                      and maze[sub_x_3][sub_y_3] == 0 and maze[sub_x_4][sub_y_4] == 0):
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_CENTER_R, pos)
                elif (maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 0
                      and maze[sub_x_3][sub_y_3] == 0 and maze[sub_x_4][sub_y_4] == 1):
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_CENTER_SYM_1, pos)
                elif (maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 0
                      and maze[sub_x_3][sub_y_3] == 1 and maze[sub_x_4][sub_y_4] == 1):
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_CENTER_L, pos)
                elif (maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 1
                      and maze[sub_x_3][sub_y_3] == 1 and maze[sub_x_4][sub_y_4] == 0):
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_CENTER_SYM_2, pos)
                elif (maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 1
                      and maze[sub_x_3][sub_y_3] == 0 and maze[sub_x_4][sub_y_4] == 1):
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_CENTER_D, pos)
                elif (maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 0
                      and maze[sub_x_3][sub_y_3] == 1 and maze[sub_x_4][sub_y_4] == 0):
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_CENTER_U, pos)
                elif (maze[sub_x_1][sub_y_1] == 1 and maze[sub_x_2][sub_y_2] == 0
                      and maze[sub_x_3][sub_y_3] == 0 and maze[sub_x_4][sub_y_4] == 0):
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_CENTER_UR, pos)
                elif (maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 0
                      and maze[sub_x_3][sub_y_3] == 0 and maze[sub_x_4][sub_y_4] == 1):
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_CENTER_DL, pos)
                elif (maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 0
                      and maze[sub_x_3][sub_y_3] == 1 and maze[sub_x_4][sub_y_4] == 0):
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_CENTER_UL, pos)
                elif (maze[sub_x_1][sub_y_1] == 0 and maze[sub_x_2][sub_y_2] == 1
                      and maze[sub_x_3][sub_y_3] == 0 and maze[sub_x_4][sub_y_4] == 0):
                    input.render_img(self.background, flags.MAZE_TYPE, flags.MAZE_INTRSE_CENTER_DR, pos)

    def setup_maze(self):
        # Set background
        bg_width, bg_height = self.size
        self.background = pg.Surface((bg_width * 32, bg_height * 32)).convert()
        self.background_rect = self.background.get_rect()
        self.background.fill((0, 0, 0))

        # Set maze
        flatmaze = self.flatten_maze(self.maze, self.size)

        width, height = self.size
        for row_idx in range(height):
            for col_idx in range(width):
                border_pos = self.check_border((row_idx, col_idx), self.size)
                self.draw_cell(flatmaze, (row_idx, col_idx), border_pos)
