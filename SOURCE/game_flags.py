# Game states
INTRO = 'intro'
LVLSELECT = 'levelselecting'
MAPSELECT = 'mapselecting'
HOLD = 'hold'
PLAYING = 'playing'
WINNING = 'winning'
SURRENDER = 'surrender'
GAMEOVER = 'gameover'

# Level gameplay
INP = 'INPUT'
LVL1 = 'Level_1'
LVL2 = 'Level_2'
LVL3 = 'Level_3'
LVL4 = 'Level_4'
MAPNO1 = 5
MAPNO2 = 4
MAPNO3 = 1
MAPNO4 = 1
SCORE = 20

# Map renders
# ASSET settings
# Background
MISC_TYPE = 'Miscellaneous'
BG = 'background.jpg'
LVLBG = 'pacman-level-select.png'
ICO = 'pixel-pac-man.png'
BUTTONBG = 'button-background.png'
MAPBG = 'map-background.png'

# Character settings and flags
CHARACTER_TYPE = 'Character'
# Pacman
MAIN_CHARACTER_RIGHT = ['pacman_01.png', 'pacman_02.png']
MAIN_CHARACTER_LEFT = ['pacman_04.png', 'pacman_05.png']
MAIN_CHARACTER_UP = ['pacman_06.png', 'pacman_07.png']
MAIN_CHARACTER_DOWN = ['pacman_08.png', 'pacman_09.png']
MAIN_CHARACTER_DISAPPEARED = ['pacman_03.png', 'pacman_07.png', 'pacman_10.png', 'pacman_11.png', 'pacman_12.png',
                              'pacman_13.png', 'pacman_14.png', 'pacman_15.png', 'pacman_16.png', 'pacman_17.png',
                              'pacman_18.png', 'pacman_19.png', 'pacman_20.png']

# Monter
# Level 2
MONSTER_RED = ['monster_red_01.png', 'monster_red_02.png', 'monster_red_03.png', 'monster_red_04.png',
               'monster_red_05.png', 'monster_red_06.png', 'monster_red_07.png', 'monster_red_08.png']
MONSTER_RETRIEVE = ['monster_retrieve_01.png', 'monster_retrieve_02.png',
                    'monster_retrieve_03.png', 'monster_retrieve_04.png']
# Food setting and flags
FOOD_TYPE = 'Food'
FOOD = ['food_04_01.png', 'food_04_02.png', 'food_04_03.png', 'food_04_04.png',
        'food_04_05.png', 'food_04_06.png', 'food_04_07.png', 'food_04_08.png']

# Maze settings and flags
MAZE_TYPE = 'Maze'
# Border
# EN
MAZE_BORDER_CONR_LD = 'maze_border_corner_2.png'
MAZE_BORDER_CONR_DL = 'maze_border_corner_6.png'

# ES
MAZE_BORDER_CONR_LU = 'maze_border_corner_4.png'
MAZE_BORDER_CONR_UL = 'maze_border_corner_8.png'

# WN
MAZE_BORDER_CONR_RD = 'maze_border_corner_1.png'
MAZE_BORDER_CONR_DR = 'maze_border_corner_5.png'

# WS
MAZE_BORDER_CONR_RU = 'maze_border_corner_3.png'
MAZE_BORDER_CONR_UR = 'maze_border_corner_7.png'

# E
MAZE_BORDER_EDGE_L = 'maze_border_edge_3.png'

MAZE_BORDER_INTRSE_L = 'maze_border_intersect_3.png'
MAZE_BORDER_INTRSE_UL = 'maze_border_intersect_7_inversed.png'
MAZE_BORDER_INTRSE_DL = 'maze_border_intersect_7.png'
MAZE_BORDER_INTRSE_EDGE_L = 'maze_border_edge_7.png'

# W
MAZE_BORDER_EDGE_R = 'maze_border_edge_2.png'

MAZE_BORDER_INTRSE_R = 'maze_border_intersect_2.png'
MAZE_BORDER_INTRSE_UR = 'maze_border_intersect_6.png'
MAZE_BORDER_INTRSE_DR = 'maze_border_intersect_6_inversed.png'
MAZE_BORDER_INTRSE_EDGE_R = 'maze_border_edge_6.png'

# S
MAZE_BORDER_EDGE_U = 'maze_border_edge_4.png'

MAZE_BORDER_INTRSE_U = 'maze_border_intersect_4.png'
MAZE_BORDER_INTRSE_RU = 'maze_border_intersect_8_inversed.png'
MAZE_BORDER_INTRSE_LU = 'maze_border_intersect_8.png'
MAZE_BORDER_INTRSE_EDGE_U = 'maze_border_edge_8.png'

# N
MAZE_BORDER_EDGE_D = 'maze_border_edge_1.png'

MAZE_BORDER_INTRSE_D = 'maze_border_intersect_1.png'
MAZE_BORDER_INTRSE_RD = 'maze_border_intersect_5.png'
MAZE_BORDER_INTRSE_LD = 'maze_border_intersect_5_inversed.png'
MAZE_BORDER_INTRSE_EDGE_D = 'maze_border_edge_5.png'

# 0 surround
MAZE_BLANK = 'blank.png'
MAZE_CENTER = 'maze_center.png'
# 1 surrounds
MAZE_HORIZONTAL_END_L = 'maze_horizontal_bar_1.png'
MAZE_HORIZONTAL_END_R = 'maze_horizontal_bar_3.png'
MAZE_VERTICAL_END_U = 'maze_vertical_bar_1.png'
MAZE_VERTICAL_END_D = 'maze_vertical_bar_3.png'

# 2 surrounds
MAZE_HORIZONTAL = 'maze_horizontal_bar_2.png'
MAZE_VERTICAL = 'maze_vertical_bar_2.png'
MAZE_INTRSE_CONR_RD = 'maze_corner_1.png'
MAZE_INTRSE_CONR_LD = 'maze_corner_2.png'
MAZE_INTRSE_CONR_RU = 'maze_corner_3.png'
MAZE_INTRSE_CONR_LU = 'maze_corner_4.png'
MAZE_CONR_RD = 'maze_corner_intersect_1.png'
MAZE_CONR_LD = 'maze_corner_intersect_2.png'
MAZE_CONR_RU = 'maze_corner_intersect_3.png'
MAZE_CONR_LU = 'maze_corner_intersect_4.png'

# 3 surrounds
MAZE_INNER_D = 'maze_inner_bar_1.png'
MAZE_INNER_R = 'maze_inner_bar_2.png'
MAZE_INNER_L = 'maze_inner_bar_3.png'
MAZE_INNER_U = 'maze_inner_bar_4.png'
MAZE_INTRSE_D = 'maze_intersect_1.png'
MAZE_INTRSE_R = 'maze_intersect_2.png'
MAZE_INTRSE_L = 'maze_intersect_3.png'
MAZE_INTRSE_U = 'maze_intersect_4.png'
MAZE_INTRSE_LD = 'maze_intersect_5.png'
MAZE_INTRSE_RD = 'maze_intersect_5_inversed.png'
MAZE_INTRSE_DR = 'maze_intersect_6.png'
MAZE_INTRSE_UR = 'maze_intersect_6_inversed.png'
MAZE_INTRSE_UL = 'maze_intersect_7.png'
MAZE_INTRSE_DL = 'maze_intersect_7_inversed.png'
MAZE_INTRSE_RU = 'maze_intersect_8.png'
MAZE_INTRSE_LU = 'maze_intersect_8_inversed.png'

# 4 surrounds
MAZE_INTRSE_CENTER_RD = 'maze_intersect_center_1.png'
MAZE_INTRSE_CENTER_LD = 'maze_intersect_center_2.png'
MAZE_INTRSE_CENTER_LU = 'maze_intersect_center_3.png'
MAZE_INTRSE_CENTER_RU = 'maze_intersect_center_4.png'
MAZE_INTRSE_CENTER_D = 'maze_intersect_center_5.png'
MAZE_INTRSE_CENTER_R = 'maze_intersect_center_6.png'
MAZE_INTRSE_CENTER_L = 'maze_intersect_center_7.png'
MAZE_INTRSE_CENTER_U = 'maze_intersect_center_8.png'
MAZE_INTRSE_CENTER_UL = 'maze_intersect_center_9.png'
MAZE_INTRSE_CENTER_UR = 'maze_intersect_center_10.png'
MAZE_INTRSE_CENTER_DR = 'maze_intersect_center_11.png'
MAZE_INTRSE_CENTER_DL = 'maze_intersect_center_12.png'
MAZE_INTRSE_CENTER_SYM_1 = 'maze_intersect_center_sym_1.png'
MAZE_INTRSE_CENTER_SYM_2 = 'maze_intersect_center_sym_2.png'
MAZE_INTRSE_CENTER = 'maze_intersect_center.png'
