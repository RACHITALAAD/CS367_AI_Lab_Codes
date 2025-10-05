from collections import deque

def is_valid(state):
    missionaries, cannibals, boat = state
    if missionaries < 0 or cannibals < 0 or missionaries > 3 or cannibals > 3:
        return False
    if missionaries > 0 and missionaries < cannibals:
        return False
    if 3 - missionaries > 0 and 3 - missionaries < 3 - cannibals:
        return False
    return True

def get_successors(state):
    successors = []
    missionaries, cannibals, boat = state
    moves = [(2, 0), (0, 2), (1, 1), (1, 0), (0, 1)]
    if boat == 1:  # Boat on starting side
        for m, c in moves:
            new_state = (missionaries - m, cannibals - c, 0)
            if is_valid(new_state):
                successors.append(new_state)
    else:  # Boat on goal side
        for m, c in moves:
            new_state = (missionaries + m, cannibals + c, 1)
            if is_valid(new_state):
                successors.append(new_state)
    return successors

def bfs(start_state, goal_state):
    queue = deque([(start_state, [])])
    visited = set()
    while queue:
        state, path = queue.popleft()
        if state in visited:
            continue
        visited.add(state)
        path = path + [state]
        if state == goal_state:
            return path
        for successor in get_successors(state):
            queue.append((successor, path))
    return None

start_state = (3, 3, 1)
goal_state = (0, 0, 0)


solution = bfs(start_state, goal_state)

if solution:
    print("Solution found.....")
    for step in solution:
        print(step)
else:
    print("No solution found.")
