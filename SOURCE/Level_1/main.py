import handle_input as handlein
from path_finding import A_star


if __name__ == '__main__':
    level = 'Level_1'
    file_name = 'Map-2.txt'

    maze_size, maze, spawnpoint = handlein.read_file(level, file_name)

    adjacent_nodes, food = handlein.handle_adjacent(maze, maze_size)

    # Find food
    path = A_star(maze, adjacent_nodes, spawnpoint, food)

    if path is not None:
        print(path)
    else:
        print("No solution")

    input()
