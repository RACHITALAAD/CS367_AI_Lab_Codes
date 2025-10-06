import math
import random

def compute_cost(melody, raag_rules):
    cost = 0
    for i in range(len(melody) - 1):
        if (melody[i], melody[i + 1]) not in raag_rules:
            cost += 1
    return cost

def generate_neighbor(melody):
    neighbor = melody.copy()
    i, j = random.sample(range(len(melody)), 2)
    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
    return neighbor

def simulated_annealing_melody(initial_melody, raag_rules, T0, alpha, min_threshold):
    current_state = initial_melody.copy()
    best_state = current_state.copy()
    current_cost = compute_cost(current_state, raag_rules)
    best_cost = current_cost
    T = T0

    while T > min_threshold:
        neighbor_state = generate_neighbor(current_state)
        neighbor_cost = compute_cost(neighbor_state, raag_rules)
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

    return best_state

if __name__ == "__main__":
    raag_rules = {('Sa', 'Re'), ('Re', 'Ga'), ('Ga', 'Ma'), ('Ma', 'Pa'),
                  ('Pa', 'Dha'), ('Dha', 'Ni'), ('Ni', 'Sa')}
    initial_melody = ['Sa', 'Ga', 'Re', 'Ma', 'Pa', 'Dha', 'Ni']
    T0 = 1000
    alpha = 0.95
    min_threshold = 0.1
    best_melody = simulated_annealing_melody(initial_melody, raag_rules, T0, alpha, min_threshold)
    print("Optimized Melody Sequence:", best_melody)
