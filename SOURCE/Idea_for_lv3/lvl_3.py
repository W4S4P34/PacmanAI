from path_finding import A_star, manhattan_distance
import handle_input as handlein


def lv3(matrix, dict, spawn, width, height):

    i = spawn[0]
    j = spawn[1]

    score = 0

    for n in range(height):
        for m in range(width):
            step[n][m].append(0)

    total = 0
    for n in range(height):
        for m in range(width):
            for key, values in dict.items():
                if n == key[0] and m == key[1]:
                    step[n][m] = sum(1 for v in values if v)
            total += step[n][m]
    step[i][j] -= 1

    for each_node_step in range(total):
        for n in range(-3, 3):
            for m in range(-3, 3):
                if i + n < 0 or j + m < 0 or i + n >= height or j + m >= witdh:
                    continue
                if matrix[i + n][j + m] != 1 and matrix[i + n][j + m] != 3:
                    list_zone.append((i + n, j + m))

        zone_with_adj = handlein.handle_adjacent(list_zone, (7, 7))

        list_food_heuristic = []

        have_2 = False
        for k in list_zone:
            if matrix[k[0]][k[1]] == 2:
                #Add heuristic to find the shortest from current position to food and count the score
                temp = manhattan_distance((i, j), k)
                list_food_heuristic.append((temp, k))
                print("Help")
                have_2 = True
                i = k[0]
                j = k[1]

        if have_2 == True:
            if min(list_food_heuristic)[0]:
                path = A_star(zone_with_adj, (i, j), (list_food_heuristic)[1])  # Calculate the shortest path to min food.
            continue
        else:
            for key in dict.keys():
                if (i, j) == key:
                    if (i, j + 1) in dict.values() and step[i][j + 1] > 0:
                        j += 1
                        step[i][j] -= 1
                        score -= 1
                        break
                    if (i + 1, j) in dict.values() and step[i + 1][j] > 0:
                        i += 1
                        step[i][j] -= 1
                        score -= 1
                        break
                    if (i - 1, j) in dict.values() and step[i - 1][j] > 0:
                        j -= 1
                        step[i][j] -= 1
                        score -= 1
                        break
                    if (i, j - 1) in dict.values() and step[i][j - 1] > 0:
                        j -= 1
                        step[i][j] -= 1
                        score -= 1
                        break

    return score
