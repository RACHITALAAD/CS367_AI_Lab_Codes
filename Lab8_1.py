
import numpy as np


COLS, ROWS = 4, 3
GAMMA = 0.99
THETA = 1e-6

ACTIONS = ['U', 'D', 'L', 'R']  
ACTION_TO_DELTA = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}

def coord_to_state(x, y):
    return y * COLS + x

def state_to_coord(s):
    return (s % COLS, s // COLS)

def in_grid(x, y):
    return 0 <= x < COLS and 0 <= y < ROWS

ALL_STATES = [coord_to_state(x,y) for y in range(ROWS) for x in range(COLS)]

TERMINAL_POS = {(3, 0): +1.0, (3, 1): -1.0}
TERMINAL_STATES = {coord_to_state(x,y): r for (x,y), r in TERMINAL_POS.items()}

def transitions(s, a):
    """
    Return list of (s_prime, prob, reward) for taking action a in state s.
    """
    if s in TERMINAL_STATES:
        return [(s, 1.0, TERMINAL_STATES[s])]  # terminal: stay with terminal reward

    x, y = state_to_coord(s)
    outcomes = []
    # intended move with prob 0.8
    intended_dx, intended_dy = ACTION_TO_DELTA[a]
    intended = (x + intended_dx, y + intended_dy)
    # sideways moves: left and right relative to action
    if a in ('U','D'):
        side_actions = [('L', 0.1), ('R', 0.1)]
    else:
        side_actions = [('U', 0.1), ('D', 0.1)]

    # intended
    if in_grid(*intended):
        s_intended = coord_to_state(*intended)
    else:
        s_intended = s  # bump into wall => stay
    outcomes.append((s_intended, 0.8, None))

    # sideways
    for sa, prob in side_actions:
        dx, dy = ACTION_TO_DELTA[sa]
        nx, ny = x + dx, y + dy
        if in_grid(nx, ny):
            s_side = coord_to_state(nx, ny)
        else:
            s_side = s
        outcomes.append((s_side, prob, None))

    
    return outcomes

def value_iteration(r_step, gamma=GAMMA, theta=THETA, max_iter=10000):
    V = np.zeros(len(ALL_STATES))
    # set terminal values to their rewards initially
    for s, r in TERMINAL_STATES.items():
        V[s] = r

    for it in range(max_iter):
        delta = 0.0
        V_new = V.copy()
        for s in ALL_STATES:
            if s in TERMINAL_STATES:
                continue
            best = -1e9
            for a in ACTIONS:
                q = 0.0
                for s2, prob, _ in transitions(s, a):
                    # reward: if s2 is terminal, get terminal reward; else r_step
                    reward = TERMINAL_STATES[s2] if s2 in TERMINAL_STATES else r_step
                    q += prob * (reward + gamma * V[s2])
                if q > best:
                    best = q
            V_new[s] = best
            delta = max(delta, abs(V_new[s] - V[s]))
        V = V_new
        if delta < theta:
            break
    # extract policy
    policy = {}
    for s in ALL_STATES:
        if s in TERMINAL_STATES:
            policy[s] = None
            continue
        best = -1e9
        best_a = None
        for a in ACTIONS:
            q = 0.0
            for s2, prob, _ in transitions(s, a):
                reward = TERMINAL_STATES[s2] if s2 in TERMINAL_STATES else r_step
                q += prob * (reward + gamma * V[s2])
            if q > best:
                best = q
                best_a = a
        policy[s] = best_a
    return V, policy

def pretty_print(V, policy):
    print("Values (grid):")
    for y in range(ROWS):
        row_vals = []
        for x in range(COLS):
            s = coord_to_state(x,y)
            row_vals.append(f"{V[s]:6.2f}")
        print(" ".join(row_vals))
    print("\nPolicy (grid):")
    for y in range(ROWS):
        row_act = []
        for x in range(COLS):
            s = coord_to_state(x,y)
            if s in TERMINAL_STATES:
                row_act.append(" T ")
            else:
                row_act.append(f" {policy[s]} ")
        print(" ".join(row_act))
    print("\n")

if __name__ == "_main_":
    r_values = [-2.0, 0.1, 0.02, 1.0]
    for r in r_values:
        print("=== r(s) =", r, "===\n")
        V, pi = value_iteration(r_step=r, gamma=0.99)
        pretty_print(V, pi)
