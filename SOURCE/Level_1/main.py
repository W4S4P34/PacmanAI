import handle_input as handlein
from path_finding import A_star
import time


if __name__ == "__main__":
    level = "Level_1"
    file_name = "Map-1.txt"

    maze_size, maze, spawnpoint = handlein.read_file(level, file_name)

    adjacent_nodes, food = handlein.handle_adjacent(maze, maze_size)

    # Find food
    timer_start = time.perf_counter()
    path, score = A_star(maze, adjacent_nodes, spawnpoint, food)
    timer_end = time.perf_counter()
    print(path)
    print("Total score: " + score)
    print(f"Time for Pacman to get to the food: {timer_end - timer_start} seconds")

    input()
