f = open('../PacMan/input/Pacman_map_lv1_1.txt', 'r')
context = f.read().splitlines()

map_size, game_map, pac_spawn = context[0], context[1:-1], context[-1]
map_size_int = [int(index) for index in map_size.split(' ')]
line = [[int(numb) for numb in line_int.split(' ')] for line_int in game_map if line_int.strip() != ""]


class Node:
    # Constructor
    def __init__(self, x_cor = -1, y_cor = -1, object = -1):
        self.x_cor = x_cor
        self.y_cor = y_cor
        self.object = object

    # Methods

    # Override operators


class Map:
    rows, cols = map_size_int[0], map_size_int[-1]
    pacman_map = []

    def __init__(self):
        self.map = []
        for i in range(0, Map.rows):
            for j in range(0, Map.cols):
                self.map.append(Node(i, j, line[i][j]))

    # def create_map(self):

    def show_position(self):
        for each_node in self.map:
            Map.pacman_map.append(each_node)
            print(each_node.object, (each_node.x_cor, each_node.y_cor))
        # pass


maze = Map()

maze.show_position()
