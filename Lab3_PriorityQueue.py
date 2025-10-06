import heapq

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

def priority_queue_search(initial_state, goal_state):
    pq = []
    heapq.heappush(pq, (0, initial_state, [initial_state]))
    visited = set()

    while pq:
        cost, state, path = heapq.heappop(pq)
        state_tuple = tuple(state)
        if state == goal_state:
            return path
        if state_tuple not in visited:
            visited.add(state_tuple)
            for successor in get_successors(state):
                heapq.heappush(pq, (cost + 1, successor, path + [successor]))
    return "No Solution Found"

if __name__ == "__main__":
    initial_state = [1, 1, 1, 0, 0, 0, 0]
    goal_state = [0, 0, 0, 0, 0, 1, 1]
    solution = priority_queue_search(initial_state, goal_state)
    print("Solution Path:")
    for step in solution:
        print(step)
