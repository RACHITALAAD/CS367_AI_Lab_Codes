import random
import itertools

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

def flip_one_variable(assignment):
    neighbors = []
    for i in range(len(assignment)):
        neighbor = assignment.copy()
        neighbor[i] = not neighbor[i]
        neighbors.append(neighbor)
    return neighbors

def flip_two_variables(assignment):
    neighbors = []
    for i, j in itertools.combinations(range(len(assignment)), 2):
        neighbor = assignment.copy()
        neighbor[i] = not neighbor[i]
        neighbor[j] = not neighbor[j]
        neighbors.append(neighbor)
    return neighbors

def swap_two_variables(assignment):
    neighbors = []
    for i, j in itertools.combinations(range(len(assignment)), 2):
        neighbor = assignment.copy()
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        neighbors.append(neighbor)
    return neighbors

def variable_neighborhood_descent(formula, n):
    assignment = [random.choice([True, False]) for _ in range(n)]
    neighborhoods = [flip_one_variable, flip_two_variables, swap_two_variables]
    k = 0
    while k < len(neighborhoods):
        neighbors = neighborhoods[k](assignment)
        neighbors.sort(key=lambda x: evaluate(formula, x), reverse=True)
        best_neighbor = neighbors[0]
        if evaluate(formula, best_neighbor) > evaluate(formula, assignment):
            assignment = best_neighbor
            k = 0
        else:
            k += 1
        if evaluate(formula, assignment) == len(formula):
            return assignment
    return "No solution found"

if __name__ == "__main__":
    formula = [
        [1, -2, 3],
        [-1, 2, -3],
        [1, 2, -3],
        [-1, -2, 3]
    ]
    n = 3
    result = variable_neighborhood_descent(formula, n)
    print("Satisfying Assignment:", result)
