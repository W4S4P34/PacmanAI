# Support definitions
def find_adjacent(maze, pos):
    row_idx, col_idx = pos

    adjacent_list = []

    if maze[row_idx - 1][col_idx] != 1:
        adjacent_list.append((row_idx - 1, col_idx))
    if maze[row_idx + 1][col_idx] != 1:
        adjacent_list.append((row_idx + 1, col_idx))
    if maze[row_idx][col_idx - 1] != 1:
        adjacent_list.append((row_idx, col_idx - 1))
    if maze[row_idx][col_idx + 1] != 1:
        adjacent_list.append((row_idx, col_idx + 1))

    return adjacent_list


# Main definitions
def read_file(file_name):
    f = open("../../INPUT/" + file_name, "r")

    maze_size = tuple(map(int, f.readline().split(" ")))

    width, height = maze_size
    maze = [[int(attr) for attr in f.readline().split(" ")] for _ in range(height)]

    spawnpoint = tuple(map(int, f.readline().split(" ")))

    f.close()

    return maze_size, maze, spawnpoint


def handle_adjacent(maze, size):
    width, height = size

    adjacent_nodes = {}

    for row_idx in range(height):
        for col_idx in range(width):
            if maze[row_idx][col_idx] == 1:
                continue
            else:
                adjacent_nodes[(row_idx, col_idx)] = find_adjacent(maze, (row_idx, col_idx))

    return adjacent_nodes
