start_state = [1, 1, 1, 0, -1, -1, -1]
goal_state = [-1, -1, -1, 0, 1, 1, 1]

def valid_moves(state):
    moves = []
    empty = state.index(0)

    # Move one step forward
    if empty > 0 and state[empty-1] == 1:
        s = state.copy()
        s[empty], s[empty-1] = s[empty-1], s[empty]
        moves.append(s)
    if empty < len(state)-1 and state[empty+1] == -1:
        s = state.copy()
        s[empty], s[empty+1] = s[empty+1], s[empty]
        moves.append(s)

    # Jump over one rabbit
    if empty > 1 and state[empty-2] == 1 and state[empty-1] == -1:
        s = state.copy()
        s[empty], s[empty-2] = s[empty-2], s[empty]
        moves.append(s)
    if empty < len(state)-2 and state[empty+2] == -1 and state[empty+1] == 1:
        s = state.copy()
        s[empty], s[empty+2] = s[empty+2], s[empty]
        moves.append(s)

    return moves

def dfs_rabbit(start, goal):
    stack = [(start, [])]
    visited = set()

    while stack:
        state, path = stack.pop()
        state_t = tuple(state)
        if state_t in visited:
            continue
        visited.add(state_t)
        path = path + [state]
        if state == goal:
            return path
        # Add successors in reverse order to explore leftmost moves first
        for next_state in reversed(valid_moves(state)):
            stack.append((next_state, path))
    return None

solution_dfs = dfs_rabbit(start_state, goal_state)

print("DFS Solution:")
if solution_dfs:
    print(f"Total moves: {len(solution_dfs)-1}")
    for i, step in enumerate(solution_dfs):
        print(f"Step {i}: {step}")
else:
    print("No solution found.")
