import random

def generate_random_k_sat(k, m, n):
    variables = list(range(1, n + 1))
    formula = []
    for _ in range(m):
        clause = []
        chosen = random.sample(variables, k)
        for var in chosen:
            if random.random() < 0.5:
                literal = var
            else:
                literal = -var
            clause.append(literal)
        formula.append(clause)
    return formula

if __name__ == "__main__":
    k = 3
    m = 5
    n = 4
    formula = generate_random_k_sat(k, m, n)
    print("Random k-SAT Formula:", formula)
