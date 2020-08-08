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

    for i in range(1, height - 2):
        for j in range(1, weight - 2):
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

file_name = "D:\Learning Stuff\AI\Project Pacman\Pacman_map_lv1_1.txt"

size = []
matrix = []

size = read_file(file_name, matrix)

weight = int(size[0][0])
height = int(size[0][1])

spawn = matrix.pop()

print(weight, height, end = "\n")
for i in range(0, height):
    for j in range(0, weight):
        print(matrix[i][j], end = " ")
    print(end = "\n")
print(spawn, end = "\n")

dict = {}
dict = add_adjacent(matrix, weight, height)
for i in dict:
    print(i)