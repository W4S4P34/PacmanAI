import handle_input as handlein


if __name__ == "__main__":
    file_name = "Pacman_map_lv1_1.txt"

    maze_size, maze, spawnpoint = handlein.read_file(file_name)
    print(maze_size)
    for row in maze:
        for ele in row:
            print(ele, end=' ')
        print()
    print(spawnpoint)

    adjacent_nodes = handlein.handle_adjacent(maze, maze_size)
    for k, v in adjacent_nodes.items():
        print("K:", k, "V:", v)

    input()
