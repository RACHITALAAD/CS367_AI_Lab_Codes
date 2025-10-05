from collections import deque

start_state = [1, 1, 1, 0, -1, -1, -1]
goal_state = [-1, -1, -1, 0, 1, 1, 1]

def valid_moves(state):
    moves = []
    empty = state.index(0)

    if empty > 0:
        s = state.copy()
        s[empty], s[empty-1] = s[empty-1], s[empty]
        moves.append(s)
    if empty < len(state)-1:
        s = state.copy()
        s[empty], s[empty+1] = s[empty+1], s[empty]
        moves.append(s)
    if empty > 1:
        s = state.copy()
        s[empty], s[empty-2] = s[empty-2], s[empty]
        moves.append(s)
    if empty < len(state)-2:
        s = state.copy()
        s[empty], s[empty+2] = s[empty+2], s[empty]
        moves.append(s)

    return moves

def bfs_rabbit(start, goal):
    queue = deque([(start, [])])
    visited = set()
    while queue:
        state, path = queue.popleft()
        state_t = tuple(state)
        if state_t in visited:
            continue
        visited.add(state_t)
        path = path + [state]
        if state == goal:
            return path
        for next_state in valid_moves(state):
            queue.append((next_state, path))
    return None

solution_bfs = bfs_rabbit(start_state, goal_state)

print("BFS Solution:")
for step in solution_bfs:
    print(step)
