import heapq

def heuristic(state, goal_state):
    return sum(1 for s, g in zip(state, goal_state) if s != g)

def get_successors(state):
    successors = []
    n = len(state)
    for i in range(n):
        if state[i] == 1:
            if i + 2 < n and state[i + 1] == 1 and state[i + 2] == 0:
                new_state = state.copy()
                new_state[i] = 0
                new_state[i + 1] = 0
                new_state[i + 2] = 1
                successors.append(new_state)
            if i - 2 >= 0 and state[i - 1] == 1 and state[i - 2] == 0:
                new_state = state.copy()
                new_state[i] = 0
                new_state[i - 1] = 0
                new_state[i - 2] = 1
                successors.append(new_state)
    return successors

def a_star_search(initial_state, goal_state):
    frontier = []
    heapq.heappush(frontier, (heuristic(initial_state, goal_state), 0, initial_state, [initial_state]))
    explored = set()

    while frontier:
        f, g, state, path = heapq.heappop(frontier)
        state_tuple = tuple(state)
        if state == goal_state:
            return path
        if state_tuple in explored:
            continue
        explored.add(state_tuple)
        for successor in get_successors(state):
            g_new = g + 1
            f_new = g_new + heuristic(successor, goal_state)
            heapq.heappush(frontier, (f_new, g_new, successor, path + [successor]))
    return "No solution found"

if __name__ == "__main__":
    initial_state = [1, 1, 1, 0, 0, 0, 0]
    goal_state = [0, 0, 0, 0, 0, 1, 1]
    solution = a_star_search(initial_state, goal_state)
    print("Solution Path:")
    for step in solution:
        print(step)
