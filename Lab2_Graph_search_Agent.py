from collections import deque

def get_neighbors(state):
    neighbors = []
    zero_index = state.index(0)
    swap_indices = []

    if zero_index % 3 > 0:
        swap_indices.append(zero_index - 1)
    if zero_index % 3 < 2:
        swap_indices.append(zero_index + 1)
    if zero_index // 3 > 0:
        swap_indices.append(zero_index - 3)
    if zero_index // 3 < 2:
        swap_indices.append(zero_index + 3)

    for idx in swap_indices:
        new_state = state.copy()
        new_state[zero_index], new_state[idx] = new_state[idx], new_state[zero_index]
        neighbors.append(new_state)
    return neighbors

def reconstruct_path(parent_map, end_state):
    path = [end_state]
    current = tuple(end_state)
    while current in parent_map:
        current = parent_map[current]
        path.append(list(current))
    path.reverse()
    return path

def graph_search_puzzle8(initial_state, goal_state):
    frontier = deque([initial_state])
    explored = set()
    parent_map = {}

    while frontier:
        current_state = frontier.popleft()
        if current_state == goal_state:
            return reconstruct_path(parent_map, current_state)
        explored.add(tuple(current_state))
        for neighbor in get_neighbors(current_state):
            neighbor_tuple = tuple(neighbor)
            if neighbor_tuple not in explored and neighbor not in frontier:
                frontier.append(neighbor)
                parent_map[neighbor_tuple] = tuple(current_state)
    return "No solution found"

if __name__ == "__main__":
    initial_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    solution = graph_search_puzzle8(initial_state, goal_state)
    print("Solution Path:")
    for step in solution:
        print(step)
