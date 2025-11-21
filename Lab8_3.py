import numpy as np
from math import exp, factorial
from collections import defaultdict
import time

MAX_BIKES, MAX_MOVE = 20, 5
RENTAL_REWARD, MOVE_COST, PARK_COST = 10, 2, 4
GAMMA = 0.9
rent_mean_1, rent_mean_2 = 3.0, 4.0
return_mean_1, return_mean_2 = 3.0, 2.0
POISSON_CUTOFF = 15

def poisson_pmf(n, lam):
    return exp(-lam) * (lam ** n) / factorial(n)

def precompute_poisson_probs(lam, cutoff=POISSON_CUTOFF):
    probs = [poisson_pmf(k, lam) for k in range(cutoff+1)]
    probs[-1] += 1 - sum(probs)
    return probs

rent_p1 = precompute_poisson_probs(rent_mean_1)
rent_p2 = precompute_poisson_probs(rent_mean_2)
ret_p1 = precompute_poisson_probs(return_mean_1)
ret_p2 = precompute_poisson_probs(return_mean_2)

STATES = [(i, j) for i in range(MAX_BIKES+1) for j in range(MAX_BIKES+1)]

def feasible_actions(state):
    n1, n2 = state
    actions = []
    for a in range(-MAX_MOVE, MAX_MOVE+1):
        if (a > 0 and n1 >= a and n2 + a <= MAX_BIKES) or \
           (a < 0 and n2 >= -a and n1 - a <= MAX_BIKES) or a == 0:
            actions.append(a)
    return actions

ACTIONS_CACHE = {s: feasible_actions(s) for s in STATES}

def build_transitions_and_rewards():
    next_probs, exp_reward = {}, {}
    for s in STATES:
        n1, n2 = s
        for a in ACTIONS_CACHE[s]:
            n1_after = min(MAX_BIKES, n1 - a)
            n2_after = min(MAX_BIKES, n2 + a)
            total_expected_rentals = 0.0
            trans = defaultdict(float)

            for rent1, p_r1 in enumerate(rent_p1):
                for rent2, p_r2 in enumerate(rent_p2):
                    prob_r = p_r1 * p_r2
                    actual_rent1, actual_rent2 = min(n1_after, rent1), min(n2_after, rent2)
                    reward_rent = (actual_rent1 + actual_rent2) * RENTAL_REWARD
                    b1_after_rent, b2_after_rent = n1_after - actual_rent1, n2_after - actual_rent2

                    for ret1, p_ret1 in enumerate(ret_p1):
                        for ret2, p_ret2 in enumerate(ret_p2):
                            prob = prob_r * p_ret1 * p_ret2
                            b1_next = min(MAX_BIKES, b1_after_rent + ret1)
                            b2_next = min(MAX_BIKES, b2_after_rent + ret2)
                            trans[(b1_next, b2_next)] += prob
                            total_expected_rentals += prob * (actual_rent1 + actual_rent2)

            move_cost = MOVE_COST * (abs(a) - 1) if a > 0 else MOVE_COST * abs(a)
            if n1_after > 10:
                move_cost += PARK_COST
            if n2_after > 10:
                move_cost += PARK_COST

            expected_reward = total_expected_rentals * RENTAL_REWARD - move_cost
            next_probs[(s, a)] = dict(trans)
            exp_reward[(s, a)] = expected_reward
    return next_probs, exp_reward

NEXT_PROBS, EXP_REWARD = build_transitions_and_rewards()

def policy_iteration(theta=1e-3):
    policy = {s: 0 for s in STATES}
    V = {s: 0.0 for s in STATES}

    while True:
        while True:
            delta = 0.0
            for s in STATES:
                a = policy[s]
                r = EXP_REWARD[(s, a)]
                value = r + GAMMA * sum(NEXT_PROBS[(s, a)].get(s2, 0) * V[s2] for s2 in NEXT_PROBS[(s, a)])
                delta = max(delta, abs(V[s] - value))
                V[s] = value
            if delta < theta:
                break

        stable = True
        for s in STATES:
            old_a = policy[s]
            best_a, best_val = old_a, -1e9
            for a in ACTIONS_CACHE[s]:
                val = EXP_REWARD[(s, a)] + GAMMA * sum(NEXT_PROBS[(s, a)].get(s2, 0) * V[s2] for s2 in NEXT_PROBS[(s, a)])
                if val > best_val:
                    best_val, best_a = val, a
            policy[s] = best_a
            if best_a != old_a:
                stable = False
        if stable:
            break
    return policy, V

policy, V = policy_iteration()
print("Sample results:")
for s in [(0,0),(10,10),(20,0),(0,20)]:
    print(f"{s} -> Move: {policy[s]}, V: {V[s]:.1f}")

