import heapq

valid_positions = [
    [0,0,1,1,1,0,0],
    [0,0,1,1,1,0,0],
    [1,1,1,1,1,1,1],
    [1,1,1,0,1,1,1],
    [1,1,1,1,1,1,1],
    [0,0,1,1,1,0,0],
    [0,0,1,1,1,0,0]
]

initial_state = [row[:] for row in valid_positions]
initial_state[3][3] = 0  # center empty

goal_state = [ [0]*7 for _ in range(7)]
goal_state[3][3] = 1  # only center marble

def get_successors(board):
    successors = []
    directions = [(-2,0), (2,0), (0,-2), (0,2)]
    for i in range(7):
        for j in range(7):
            if valid_positions[i][j] == 1 and board[i][j] == 1:
                for dx, dy in directions:
                    x, y = i+dx, j+dy
                    mx, my = i+dx//2, j+dy//2
                    if 0<=x<7 and 0<=y<7 and valid_positions[x][y]==1:
                        if board[x][y]==0 and board[mx][my]==1:
                            new_board = [row[:] for row in board]
                            new_board[i][j] = 0
                            new_board[mx][my] = 0
                            new_board[x][y] = 1
                            successors.append(new_board)
    return successors

def priority_queue_search(initial, goal, get_successors):
    pq = []
    heapq.heappush(pq, (0, initial, [initial]))
    visited = set()
    while pq:
        cost, state, path = heapq.heappop(pq)
        state_t = tuple(tuple(row) for row in state)
        if state == goal:
            return path
        if state_t not in visited:
            visited.add(state_t)
            for next_state in get_successors(state):
                new_path = path + [next_state]
                heapq.heappush(pq, (cost + 1, next_state, new_path))
    return None

solution = priority_queue_search(initial_state, goal_state, get_successors)

if solution:
    for step, s in enumerate(solution):
        print(f"Step {step}:")
        for row in s:
            print(row)
        print()
else:
    print("No solution found.")
