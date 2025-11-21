import random

def epsilon_greedy(binary_bandit, epsilon=0.1, episodes=1000):
    Q = [0.0, 0.0] 
    N = [0, 0]       
    
    for t in range(episodes):
        if random.random() < epsilon:
            action = random.choice([0, 1])  
        else:
            action = Q.index(max(Q))        
        
        reward = binary_bandit(action + 1)  
        
        N[action] += 1
        Q[action] += (reward - Q[action]) / N[action]
    
    best_action = Q.index(max(Q)) + 1
    return Q, best_action

def binaryBanditA(action):
    if action == 1:
        return 1 if random.random() < 0.7 else 0 
    else:
        return 1 if random.random() < 0.4 else 0  

Q_values, optimal_action = epsilon_greedy(binaryBanditA, epsilon=0.1, episodes=1000)
print("Estimated values:", Q_values)
print("Best action:", optimal_action)
