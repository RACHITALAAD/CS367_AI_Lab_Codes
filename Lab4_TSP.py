import math
import random

def tour_cost(state, distance_matrix):
    cost = 0
    for i in range(len(state)):
        cost += distance_matrix[state[i]][state[(i + 1) % len(state)]]
    return cost

def generate_neighbor(state):
    neighbor = state.copy()
    i, j = random.sample(range(len(state)), 2)
    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
    return neighbor

def simulated_annealing_tsp(cities, distance_matrix, T0, alpha, min_threshold):
    current_state = cities.copy()
    random.shuffle(current_state)
    best_state = current_state.copy()
    current_cost = tour_cost(current_state, distance_matrix)
    best_cost = current_cost
    T = T0

    while T > min_threshold:
        neighbor_state = generate_neighbor(current_state)
        neighbor_cost = tour_cost(neighbor_state, distance_matrix)
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
    cities = [0, 1, 2, 3, 4]
    distance_matrix = [
        [0, 2, 9, 10, 7],
        [1, 0, 6, 4, 3],
        [15, 7, 0, 8, 3],
        [6, 3, 12, 0, 11],
        [9, 5, 4, 2, 0]
    ]
    T0 = 1000
    alpha = 0.95
    min_threshold = 0.1
    best_state, best_cost = simulated_annealing_tsp(cities, distance_matrix, T0, alpha, min_threshold)
    print("Best Tour:", best_state)
    print("Minimum Cost:", best_cost)
