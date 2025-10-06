import random

def evaluate(formula, assignment):
    satisfied = 0
    for clause in formula:
        clause_satisfied = False
        for literal in clause:
            var = abs(literal)
            if (literal > 0 and assignment[var - 1]) or (literal < 0 and not assignment[var - 1]):
                clause_satisfied = True
                break
        if clause_satisfied:
            satisfied += 1
    return satisfied

def generate_neighbors(assignment):
    neighbors = []
    for i in range(len(assignment)):
        neighbor = assignment.copy()
        neighbor[i] = not neighbor[i]
        neighbors.append(neighbor)
    return neighbors

def beam_search_3sat(formula, n, w):
    frontier = [[random.choice([True, False]) for _ in range(n)] for _ in range(w)]
    while True:
        new_frontier = []
        for assignment in frontier:
            neighbors = generate_neighbors(assignment)
            neighbors.sort(key=lambda x: evaluate(formula, x), reverse=True)
            new_frontier.extend(neighbors[:w])
        new_frontier.sort(key=lambda x: evaluate(formula, x), reverse=True)
        frontier = new_frontier[:w]
        for assignment in frontier:
            if evaluate(formula, assignment) == len(formula):
                return assignment

if __name__ == "__main__":
    formula = [
        [1, -2, 3],
        [-1, 2, -3],
        [1, 2, -3],
        [-1, -2, 3]
    ]
    n = 3
    w = 2
    result = beam_search_3sat(formula, n, w)
    print("Satisfying Assignment:", result)
