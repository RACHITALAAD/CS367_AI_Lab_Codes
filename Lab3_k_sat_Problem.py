import random

def generate_k_sat(k, m, n):
    variables = [f"x{i+1}" for i in range(n)]
    formula = []

    for _ in range(m):
        clause = []
        chosen = random.sample(variables, k)
        for var in chosen:
            literal = var if random.random() < 0.5 else f"¬{var}"
            clause.append(literal)
        formula.append(clause)
    
    return formula

k = 3
m = 5
n = 6
formula = generate_k_sat(k, m, n)
for i, clause in enumerate(formula, 1):
    print(f"Clause {i}: {clause}")
