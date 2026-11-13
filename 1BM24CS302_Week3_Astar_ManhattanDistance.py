import heapq
import copy

GOAL_STATE = [[1, 2, 3],
              [8, 0, 4],
              [7, 6, 5]]

def h_manhattan(state):
    total_distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                for gi in range(3):
                    for gj in range(3):
                        if GOAL_STATE[gi][gj] == value:
                            total_distance += abs(i - gi) + abs(j - gj)
    return total_distance

def get_neighbors(state):
    neighbors = []
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                x, y = i, j
                break

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = copy.deepcopy(state)
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(new_state)
    return neighbors

def a_star_manhattan(initial_state):
    open_list = []
    heapq.heappush(open_list, (h_manhattan(initial_state), 0, initial_state, [initial_state]))
    closed_set = set()

    while open_list:
        f, g, current, path = heapq.heappop(open_list)

        if current == GOAL_STATE:
            return path

        current_tuple = tuple(tuple(row) for row in current)
        if current_tuple in closed_set:
            continue

        closed_set.add(current_tuple)

        for neighbor in get_neighbors(current):
            neighbor_tuple = tuple(tuple(row) for row in neighbor)
            if neighbor_tuple not in closed_set:
                new_g = g + 1
                new_h = h_manhattan(neighbor)
                new_f = new_g + new_h
                heapq.heappush(open_list, (new_f, new_g, neighbor, path + [neighbor]))

    return None

initial_state = [[8, 0, 3],
                 [2, 1, 4],
                 [7, 6, 5]]

print("Manhattan Distance Algorithm:")
path = a_star_manhattan(initial_state)

if path:
    for step, state in enumerate(path):
        print(f"Step {step}:")
        for row in state:
            print(row)
        print()
    print("Goal Found")
else:
    print("Goal Not Found")
