import game_settings as settings
import pygame as pg
import os


# Support definitions
def load_image(type, name):
    """ Load image and return image object """
    fullname = os.path.join(settings.PATH, 'ASSET', type, name)
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


# Directly load and render image to Surface
def render_img(surf, type, image, pos):
    x_coor, y_coor = pos
    on_bg_pos = (x_coor * 32, y_coor * 32)
    cell_image, cell_rect = load_image(type, image)
    cell_rect = cell_rect.move(tuple(reversed(on_bg_pos)))
    surf.blit(cell_image, cell_rect)


def find_adjacent(maze, pos):
    row_idx, col_idx = pos

    adjacent_list = []

    obstacles = [1, 3]

    if maze[row_idx - 1][col_idx] not in obstacles:
        adjacent_list.append((row_idx - 1, col_idx))
    if maze[row_idx + 1][col_idx] not in obstacles:
        adjacent_list.append((row_idx + 1, col_idx))
    if maze[row_idx][col_idx - 1] not in obstacles:
        adjacent_list.append((row_idx, col_idx - 1))
    if maze[row_idx][col_idx + 1] not in obstacles:
        adjacent_list.append((row_idx, col_idx + 1))

    return adjacent_list


def check_food(maze, pos):
    row_idx, col_idx = pos
    return maze[row_idx][col_idx] == 2


def check_wall(maze, pos):
    row_idx, col_idx = pos
    return maze[row_idx][col_idx] == 1


def check_monster(maze, pos):
    row_idx, col_idx = pos
    return maze[row_idx][col_idx] == 3


# Main definitions
def read_file(level, file_name):
    fullpath = os.path.join(settings.PATH, 'INPUT', level, file_name)
    f = open(fullpath, 'r')

    maze_size = tuple(map(int, f.readline().split(' ')))

    width, height = maze_size
    maze = [[int(attr) for attr in f.readline().split(' ')] for _ in range(height)]

    spawnpoint = tuple(map(int, f.readline().split(' ')))

    f.close()

    return maze_size, maze, spawnpoint


# Handle adjacents for lvl 1 and lvl 2
def handle_adjacent_1(maze, size):
    width, height = size

    adjacent_nodes = {}

    for row_idx in range(height):
        for col_idx in range(width):
            current_pos = (row_idx, col_idx)
            if check_wall(maze, current_pos):
                continue
            else:
                if check_food(maze, current_pos):  # In this level, there only one food
                    food = (row_idx, col_idx)  # Food's position
                adjacent_nodes[(row_idx, col_idx)] = find_adjacent(maze, (row_idx, col_idx))

    return adjacent_nodes, food


def handle_adjacent_2(maze, size):
    width, height = size

    adjacent_nodes = {}

    monster_list = []

    for row_idx in range(height):
        for col_idx in range(width):
            current_pos = (row_idx, col_idx)
            if check_wall(maze, current_pos):
                continue
            elif check_monster(maze, current_pos):
                monster_list.append((row_idx, col_idx))
                continue
            else:
                if check_food(maze, current_pos):  # In this level, there only one food
                    food = (row_idx, col_idx)  # Food's position
                adjacent_nodes[(row_idx, col_idx)] = find_adjacent(maze, (row_idx, col_idx))

    return adjacent_nodes, food, monster_list
