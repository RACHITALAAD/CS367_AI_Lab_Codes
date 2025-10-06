import math
import random

def compute_cost(state):
    return random.randint(0, 100)

def swap_two_pieces(state):
    new_state = state.copy()
    i, j = random.sample(range(len(state)), 2)
    new_state[i], new_state[j] = new_state[j], new_state[i]
    return new_state

def simulated_annealing(puzzle_pieces, T0, alpha, min_threshold):
    current_state = puzzle_pieces.copy()
    random.shuffle(current_state)
    best_state = current_state.copy()
    current_cost = compute_cost(current_state)
    best_cost = current_cost
    T = T0

    while T > min_threshold:
        neighbor_state = swap_two_pieces(current_state)
        neighbor_cost = compute_cost(neighbor_state)
        delta_E = neighbor_cost - current_cost

        if delta_E < 0:
            current_state = neighbor_state
            current_cost = neighbor_cost
            if current_cost < best_cost:
                best_state = current_state
                best_cost = current_cost
        else:
            p = math.exp(-delta_E / T)
            if random.random() < p:
                current_state = neighbor_state
                current_cost = neighbor_cost

        T *= alpha

    return best_state, best_cost

if __name__ == "__main__":
    puzzle_pieces = [i for i in range(1, 10)]
    T0 = 1000
    alpha = 0.95
    min_threshold = 0.1
    best_state, best_cost = simulated_annealing(puzzle_pieces, T0, alpha, min_threshold)
    print("Best arrangement:", best_state)
    print("Minimum cost:", best_cost)
