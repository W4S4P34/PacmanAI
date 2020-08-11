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
