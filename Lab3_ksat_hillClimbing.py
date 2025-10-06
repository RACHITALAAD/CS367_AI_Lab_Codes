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

def hill_climbing_3sat(formula, n):
    assignment = [random.choice([True, False]) for _ in range(n)]
    while True:
        best = assignment.copy()
        for i in range(n):
            new_assignment = assignment.copy()
            new_assignment[i] = not new_assignment[i]
            if evaluate(formula, new_assignment) > evaluate(formula, best):
                best = new_assignment
        if evaluate(formula, best) <= evaluate(formula, assignment):
            return assignment
        assignment = best
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
    result = hill_climbing_3sat(formula, n)
    print("Satisfying Assignment:", result)
