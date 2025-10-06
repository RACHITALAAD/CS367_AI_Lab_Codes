def backtrack_path(parent_map, goal_state):
    path = []
    current = tuple(goal_state)
    while current in parent_map:
        path.append(list(current))
        current = parent_map[current]
    path.append(list(current))
    path.reverse()
    return path

if __name__ == "__main__":
    parent_map = {
        (1, 2, 3, 4, 5, 6, 7, 0, 8): (1, 2, 3, 4, 5, 6, 0, 7, 8),
        (1, 2, 3, 4, 5, 6, 0, 7, 8): (1, 2, 3, 4, 5, 6, 7, 8, 0)
    }
    goal_state = [1, 2, 3, 4, 5, 6, 7, 0, 8]
    path = backtrack_path(parent_map, goal_state)
    print("Path from initial to goal:")
    for step in path:
        print(step)
