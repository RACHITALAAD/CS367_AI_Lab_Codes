
import numpy as np
from math import exp, factorial
from collections import defaultdict
import time

MAX_BIKES = 20
MAX_MOVE = 5
RENTAL_REWARD = 10
MOVE_COST = 2
GAMMA = 0.9


rent_mean_1, rent_mean_2 = 3.0, 4.0
return_mean_1, return_mean_2 = 3.0, 2.0

POISSON_CUTOFF = 15  


def poisson_pmf(n, lam):
    
    return exp(-lam) * (lam ** n) / factorial(n)

def precompute_poisson_probs(lam, cutoff=POISSON_CUTOFF):
    probs = [poisson_pmf(k, lam) for k in range(cutoff+1)]
    tail = 1.0 - sum(probs)
    probs[-1] += tail  
    return probs


rent_p_1 = precompute_poisson_probs(rent_mean_1)
rent_p_2 = precompute_poisson_probs(rent_mean_2)
ret_p_1  = precompute_poisson_probs(return_mean_1)
ret_p_2  = precompute_poisson_probs(return_mean_2)


STATES = [(i, j) for i in range(MAX_BIKES+1) for j in range(MAX_BIKES+1)]

def feasible_actions(state):
    n1, n2 = state
    actions = []
    for a in range(-MAX_MOVE, MAX_MOVE+1):
      
        if a > 0:
            if n1 >= a and n2 + a <= MAX_BIKES:
                actions.append(a)
        elif a < 0:
          
            if n2 >= -a and n1 - a <= MAX_BIKES:
                actions.append(a)
        else:
            actions.append(0)
    return actions


ACTIONS_CACHE = {s: feasible_actions(s) for s in STATES}


def build_transitions_and_rewards():
    next_probs = {}
    exp_reward = {}
    cutoff = POISSON_CUTOFF

    
    rent_list_1 = [(k, rent_p_1[k]) for k in range(cutoff+1)]
    rent_list_2 = [(k, rent_p_2[k]) for k in range(cutoff+1)]
    ret_list_1  = [(k, ret_p_1[k])  for k in range(cutoff+1)]
    ret_list_2  = [(k, ret_p_2[k])  for k in range(cutoff+1)]

    for s in STATES:
        n1, n2 = s
        for a in ACTIONS_CACHE[s]:
         
            n1_after = min(MAX_BIKES, n1 - a)
            n2_after = min(MAX_BIKES, n2 + a)

            total_expected_rentals = 0.0
            trans = defaultdict(float)

           
            for rent1, p_r1 in rent_list_1:
                for rent2, p_r2 in rent_list_2:
                    prob_r = p_r1 * p_r2
                   
                    actual_rent1 = min(n1_after, rent1)
                    actual_rent2 = min(n2_after, rent2)
                    reward_rent = (actual_rent1 + actual_rent2) * RENTAL_REWARD

                    
                    b1_after_rent = n1_after - actual_rent1
                    b2_after_rent = n2_after - actual_rent2

                   
                    for ret1, p_ret1 in ret_list_1:
                        for ret2, p_ret2 in ret_list_2:
                            prob = prob_r * p_ret1 * p_ret2
                            b1_next = min(MAX_BIKES, b1_after_rent + ret1)
                            b2_next = min(MAX_BIKES, b2_after_rent + ret2)
                            trans[(b1_next, b2_next)] += prob
                            total_expected_rentals += prob * (actual_rent1 + actual_rent2)

           
            expected_reward = total_expected_rentals * RENTAL_REWARD - MOVE_COST * abs(a)
            next_probs[(s, a)] = dict(trans)
            exp_reward[(s, a)] = expected_reward

    return next_probs, exp_reward

print("Building transition & reward cache (this may take a minute)...")
start_time = time.time()
NEXT_PROBS, EXP_REWARD = build_transitions_and_rewards()
print("Done. Time elapsed: {:.1f}s".format(time.time() - start_time))

# Policy iteration
def policy_iteration(theta_eval=1e-3, gamma=GAMMA, max_iter=1000):
    policy = {}
    for s in STATES:
        acts = ACTIONS_CACHE[s]
        policy[s] = 0 if 0 in acts else acts[0]

    V = {s: 0.0 for s in STATES}
    while True:
        
        while True:
            delta = 0.0
            for s in STATES:
                a = policy[s]
                r = EXP_REWARD[(s, a)]
                value = r + gamma * sum(NEXT_PROBS[(s,a)].get(s2, 0.0) * V[s2] for s2 in NEXT_PROBS[(s,a)])
                delta = max(delta, abs(V[s] - value))
                V[s] = value
            if delta < theta_eval:
                break

    
        policy_stable = True
        for s in STATES:
            old_a = policy[s]
            best_a = old_a
            best_val = -1e9
            for a in ACTIONS_CACHE[s]:
                val = EXP_REWARD[(s,a)] + gamma * sum(NEXT_PROBS[(s,a)].get(s2, 0.0) * V[s2] for s2 in NEXT_PROBS[(s,a)])
                if val > best_val:
                    best_val = val
                    best_a = a
            policy[s] = best_a
            if best_a != old_a:
                policy_stable = False

        if policy_stable:
            break

    return policy, V

if __name__ == "_main_":
    policy, V = policy_iteration()
   
    print("\nSample policy entries (n1, n2) -> move:")
    for s in [(0,0),(3,3),(10,10),(20,0),(0,20),(5,10)]:
        print(f"{s} -> {policy[s]}, V={V[s]:.1f}")
    