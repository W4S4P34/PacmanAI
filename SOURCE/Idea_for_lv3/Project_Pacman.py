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

def add_adjacent(matrix, width, height):
    adjacent = {}

    for i in range(1, height - 1):
        for j in range(1, width - 1):
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
            adjacent[(i, j)] = temp

    return adjacent
def get_monsters_location(matrix, width, height):
    monsters_location = {}
    i = 0
    for row in range(1, height - 1):
        for col in range(1, width - 1):
            if matrix[row][col] == 3:
                monsters_location[i] = [row,col]
                i += 1
    return monsters_location
def lv3(matrix, dict, monsters_location, spawn, width, height):
    
    step_move = [               
		    [0, -1],            # Trái
		    [0, 0],             # Phải
		    [1, 0],             # Xuống
		    [0, 0],             # Lên
		    [0, 1],             # Phải
		    [0, 0],             # Trái
		    [-1, 0],            # Lên
		    [0, 0]              # Xuống
                ]
    
    i = spawn[0]    #Lưu spawn thành 2 điểm
    j = spawn[1]

    #Mục tiêu là đi nhiều nhất để tìm đồ ăn nên sẽ có điểm âm hơi lớn
    #Mỗi một node sẽ có một số lần đi qua nhất định để tránh việc đi lại nhiều lần, dồng thời cũng làm cho việc đi lùi khó khăn, duyệt không hết map
    #Chưa xử lý được cách né khi thấy quái

    score = 0   #Điểm ban đầu là 0

    #Tạo list các key và list các values của dictionary
    keys = []
    for k in adjacent.keys():
        keys.append(k)
    values = []
    for k in adjacent.values():
        for o in k:
            values.append(o)

    #Đây là list số lần được phép đi qua của mỗi node
    step = []
    for n in range(0, height):
        temp = []
        for m in range(0, width):
            temp.append(0)
        step.append(temp)

    total = 0   #total dùng để giới hạn thời gian đi trong map của pacman <-- Này đéo hiểu 
    for n in range(0, height):
        for m in range(0, width):
            for key, value in dict.items():
                if n == key[0] and m == key[1]:
                    step[n][m] = sum(1 for v in value if v)
            total += step[n][m]

    step[i][j] -= 1 #Điểm spawn giảm sẫn 1 bước đi

    pre_path = []   #path này dùng để lưu đường đi khi có thức ăn
    have_2 = False  #Check xem đã thấy thức ăn chưa, nếu đẵ thấy thức ăn thì đi theo path, chi đổi hướng khi thấy thức ăn khác gần hơn

    monsters_path = {}               # Lưu đường đi của từng monster với key là thứ tự và value là list đường đi
    print(monsters_location)
    monsters_step = 0
    for each_node_step in range(total):         # Mỗi turn 4 con quái sẽ di chuyển 1 lần theo thứ tự nêu phía trên
        for each_monster, each_location in monsters_location.items():
            next_location = [sum(x) for x in zip(each_location, step_move[monsters_step])]
            if matrix[next_location[0]][next_location[1]] == 1:
                continue
            each_location = next_location
            monsters_path[each_monster] = each_location
        monsters_step += 1
        if(monsters_step == 8):
           monsters_step = 0
        
        if matrix[i][j] == 2:   #Check xem chạm thức ăn chưa, nếu rồi thì thức ăn biến mất, xóa path và reset have_2
            score += 20
            matrix[i][j] = 0
            pre_path.clear()
            have_2 = False

        list_zone = []  #Tạo zone, vùng nhìn thấy của pacman, các elements trong zone là tuple tọa độ của caca1 node
        for n in range(-3, 3):
            for m in range(-3, 3):
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


        
        if have_2 == True:  #Đi theo path khi có thức ăn
            tuple = pre_path.pop(1)
            i = tuple[0]
            j = tuple[1]
            step[i][j] -= 1
            score -= 1
            continue
        else:   #Tìm đường theo một thừ tự nhất định khi không có thức ăn trong zone theo thứ tự node là phải, dưới, trên, trái
            for key in keys:    
                if (i, j) == key:
                    if (i, j + 1) in values and step[i][j + 1] > 0:
                        step[i][j + 1] -= 1
                        j += 1
                        score -= 1
                        break
                    if (i + 1, j) in values and step[i + 1][j] > 0:
                        step[i + 1][j] -= 1
                        i += 1
                        if step[i][j] == 1 and (i, j - 1) in values and (i + 1, j + 1) not in values and (i - 1, j + 1) not in values and (i - 1, j - 1) not in values and (i + 1, j - 1) not in values:
                                step[i][j] -= 1
                                step[i][j - 1] -= 1
                        score -= 1
                        break
                    if (i - 1, j) in values and step[i - 1][j] > 0:
                        step[i - 1][j] -= 1
                        i -= 1                                                             
                        score -= 1
                        break
                    if (i, j - 1) in values and step[i][j - 1] > 0:
                        step[i][j - 1] -= 1
                        j -= 1
                        if  step[i][j] > 1 and (i, j - 1) in values and (i, j + 1) in values and (i + 1, j) not in values and (i - 1, j) not in values:
                            step[i][j] -= 1
                        score -= 1
                        break
                #Còn trục trặc khi pacman đi lùi, nếu các thức ăn quá xa nhau có thể sẽ không thấy, cần fix
    return score

file_name = "C:/Users/ASUS/Documents/HCMUS/2nd/S3/AI/Bài tập/Proj/Pacman Map/Pacman_map_lv2_3.txt"

size = []
matrix = []

size = read_file(file_name, matrix)

width = int(size[0][0])
height = int(size[0][1])

spawn = matrix.pop()

adjacent = add_adjacent(matrix, width, height)
monsters_location = get_monsters_location(matrix, width, height)
score = lv3(matrix, adjacent, monsters_location, spawn, width, height)
