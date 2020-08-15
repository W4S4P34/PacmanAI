from heapq import heappush, heappop


# Support definitions
def manhattan_distance(current_pos, food):
    return sum(map(lambda x, y: abs(x - y), current_pos, food))


def backtracking(current, parent_list):
    path = []
    tracer = current

    while True:
        path.append(tracer)
        tracer = parent_list[tracer]
        if tracer is None:
            break

    return path


# Main definitions
def A_star(maze, adjacent_nodes, spawnpoint, food):
    frontier = []
    explored = []
    parent_nodes = {}
    cost = 0

    start_node = (cost + manhattan_distance(spawnpoint, food), spawnpoint)
    parent_nodes[spawnpoint] = None

    heappush(frontier, start_node)

    # Loop to find the way out
    while True:
        # Check if there is a way out/ escapable
        if not frontier:
            return None
        else:
            # Pop from the queue head
            tmp_tuple = heappop(frontier)  # tmp_tuple is a tuple which contains pair of cost and node popped out of the queue (cost, Node)
            current_node = tmp_tuple[1]
            cost = tmp_tuple[0] - manhattan_distance(current_node, food)

            # Check whether current node is explored or not
            is_explored = False
            for explored_node in explored:
                if(current_node == explored_node):
                    is_explored = True
                    break

            if is_explored:
                continue

            # Add to explored nodes list
            explored.append(current_node)

            # STOP if find the food and backtrack the path
            if current_node == food:
                final_path = backtracking(current_node, parent_nodes)
                return final_path[::-1]

            # Expand the way from current node/ Add to frontier
            for adjacent in adjacent_nodes[current_node]:
                heappush(frontier, ((cost + 1) + manhattan_distance(adjacent, food), adjacent))
                if adjacent not in explored:
                    parent_nodes[adjacent] = current_node

def read_file(file_name, matrix):
    f = open(file_name, "r")
    size = f.readline()

    true_size = []
    true_size.append(size.split())
    
    for x in f:
        temp1 = []
        temp2 = []
        temp1.append(x.split())
        for k in temp1[0]:
            temp2.append(int(k))
        matrix.append(temp2)

    f.close()
    return true_size

def add_adjacent(matrix, weight, height):
    dict = {}

    for i in range(1, height - 1):
        for j in range(1, weight - 1):
            temp = []
            if matrix[i][j] == 1:
                continue
            if matrix[i - 1][j] != 1:
                temp.append((i - 1, j))
            if matrix[i + 1][j] != 1:
                temp.append((i + 1, j))
            if matrix[i][j - 1] != 1:
                temp.append((i, j - 1))
            if matrix[i][j + 1] != 1:
                temp.append((i, j + 1))
            dict[(i, j)] = temp

    return dict

def lv3(matrix, dict, spawn, width, height):

    i = spawn[0]    #Lưu spawn thành 2 điểm
    j = spawn[1]

    #Mục tiêu là đi nhiều nhất để tìm đồ ăn nên sẽ có điểm âm hơi lớn
    #Mỗi một node sẽ có một số lần đi qua nhất định để tránh việc đi lại nhiều lần, dồng thời cũng làm cho việc đi lùi khó khăn, duyệt không hết map
    #Chưa xử lý được cách né khi thấy quái

    score = 0   #Điểm ban đầu là 0

    #Đây là list số lần được phép đi qua của mỗi node
    step = []
    for n in range(0, height):
        temp = []
        for m in range(0, width):
            temp.append(0)
        step.append(temp)

    total = 0   #total dùng để giới hạn thời gian đi trong map của pacman
    for n in range(0, height):
        for m in range(0, width):
            for key, value in dict.items():
                if n == key[0] and m == key[1]:
                    step[n][m] = sum(1 for v in value if v)
            total += step[n][m]

    number_adj_list = []
    number_adj_list = step

    step[i][j] -= 1 #Điểm spawn giảm sẫn 1 bước đi

    pre_path = []   #path này dùng để lưu đường đi khi có thức ăn
    have_2 = False  #Check xem đã thấy thức ăn chưa, nếu đẵ thấy thức ăn thì đi theo path, chi đổi hướng khi thấy thức ăn khác gần hơn

    
    pre_position = (i, j)
    
    count_2_step = 0

    #Lấy ra danh sách vị trí quái vật
    monster_list = []
    for n in range(0, height):
        for m in range(0, width):
            if matrix[n][m] == 3:
                monster_list.append((n, m))
    
    for each_node_step in range(total):
        if matrix[i][j] == 2:   #Check xem chạm thức ăn chưa, nếu rồi thì thức ăn biến mất, xóa path và reset have_2
            score += 20
            matrix[i][j] = 0
            pre_path.clear()
            have_2 = False
            count_2_step = 0

        #Quái di chuyển bằng Heuristic tìm pacman
        for monster in monster_list:
            monster_path = []
            monster_path = BFS(matrix, dict, (i, j), (monster[0], monster[1]))
            monster_tuple = monster_path.pop(1)
            matrix[monster[0]][monster[1]] = 0
            matrix[monster_tuple[0]][monster_tuple[1]] = 3

        #Biến vùng xung quanh monster thành tường
        to_wall_list = []
        for monster in monster_list:
            for pos in monster:
                if matrix[pos[0] + 1][pos[1]] == 0:
                    matrix[pos[0] + 1][pos[1]] = 1
                    to_wall_list.append((pos[0] + 1, pos[1]))

                if matrix[pos[0]][pos[1] + 1] == 0:
                    matrix[pos[0]][pos[1 + 1]] = 1
                    to_wall_list.append((pos[0], pos[1] + 1))

                if matrix[pos[0] + 1][pos[1] + 1] == 0:
                    matrix[pos[0] + 1][pos[1] + 1] = 1
                    to_wall_list.append((pos[0] + 1, pos[1] + 1))

                if matrix[pos[0] + 1][pos[1] - 1] == 0:
                    matrix[pos[0] + 1][pos[1] - 1] = 1
                    to_wall_list.append((pos[0] + 1, pos[1] - 1))

                if matrix[pos[0] - 1][pos[1] + 1] == 0:
                    matrix[pos[0] - 1][pos[1] + 1] = 1
                    to_wall_list.append((pos[0] - 1, pos[1] + 1))

                if matrix[pos[0] - 1][pos[1]] == 0:
                    matrix[pos[0] - 1][pos[1]] = 1
                    to_wall_list.append((pos[0] - 1, pos[1]))

                if matrix[pos[0] - 1][pos[1] - 1] == 0:
                    matrix[pos[0] - 1][pos[1] - 1] = 1
                    to_wall_list.append((pos[0] - 1, pos[1] - 1))

                if matrix[pos[0]][pos[1] - 1] == 0:
                    matrix[pos[0]][pos[1] - 1] = 1
                    to_wall_list.append((pos[0], pos[1] - 1))

        dict  = add_adjacent(matrix, width, height)

        #Tạo list các key và list các values của dictionary
        keys = []
        for k in dict.keys():
            keys.append(k)
        values = []
        for k in dict.values():
            for o in k:
                values.append(o)

        list_zone = []  #Tạo zone, vùng nhìn thấy của pacman, các elements trong zone là tuple tọa độ của caca1 node
        for n in range(-4, 4):
            for m in range(-4, 4):
                if i + n < 0 or j + m < 0 or i + n >= height or j + m >= width:
                    continue
                if matrix[i + n][j + m] != 1 and matrix[i + n][j + m] != 3:
                    list_zone.append((i + n, j + m))
        
        #Tìm xem trong zone có thức ăn hay không
        for k in list_zone:
            path = []
            if matrix[k[0]][k[1]] == 2:
                path = A_star(matrix, dict, (i, j), (k[0], k[1]))
                if len(pre_path) < len(path) and len(pre_path) != 0:
                    continue
                have_2 = True
                pre_path = path
                tuple = pre_path.pop(0)
                step[tuple[0]][tuple[1]] += 1


        
        if have_2 == True:  #Đi theo path khi có thức ăn
            tuple = pre_path.pop(0)
            count_2_step += 1
            i = tuple[0]
            j = tuple[1]            
            if count_2_step > 1:
                step[i][j] -= 1
            score -= 1
            continue
        else:   #Tìm đường theo một thừ tự nhất định khi không có thức ăn trong zone theo thứ tự node là phải, dưới, trên, trái
            for key in keys:
                if (i, j) == key:
                    if (i, j + 1) in values and step[i][j + 1] > 0 and (i, j + 1) != pre_position:
                        step[i][j + 1] -= 1
                        pre_position = (i, j)
                        j += 1
                        score -= 1
                        break
                    if (i + 1, j) in values and step[i + 1][j] > 0  and (i + 1, j) != pre_position:
                        step[i + 1][j] -= 1
                        pre_position = (i, j)
                        i += 1
                        score -= 1
                        break
                    if (i - 1, j) in values and step[i - 1][j] > 0:
                        step[i - 1][j] -= 1
                        pre_position = (i, j)
                        i -= 1                                                             
                        score -= 1
                        break
                    if (i, j - 1) in values and step[i][j - 1] > 0:
                        step[i][j - 1] -= 1
                        pre_position = (i, j)
                        j -= 1
                        score -= 1
                        break
               
        #Trả về đường sau khi quái di chuyển
        for brick in to_wall_list:
            matrix[brick[0]][brick[1]] = 0

    print((i, j))
    return score

file_name = "D:\Learning Stuff\AI\Project Pacman\Pacman_map_lv1_1.txt"

size = []
matrix = []

size = read_file(file_name, matrix)

weight = int(size[0][0])
height = int(size[0][1])

spawn = matrix.pop()

dict = add_adjacent(matrix, weight, height)

score = lv3(matrix, dict, spawn, weight, height)
print(score)