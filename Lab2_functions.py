def is_goal(state, goal_state):
    return state == goal_state

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

def print_state(state):
    for i in range(0, 9, 3):
        row = state[i:i+3]
        print(" | ".join(str(x) if x != 0 else " " for x in row))
        if i < 6:
            print("-" * 9)

if __name__ == "__main__":
    state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    print("Is goal?", is_goal(state, goal_state))
    print("\nNeighbors:")
    for neighbor in get_neighbors(state):
        print_state(neighbor)
        print()
    print("Current state:")
    print_state(state)
