import numpy as np
import matplotlib.pyplot as plt

class NonStationaryBandit:
    def _init_(self, n_arms=10, walk_std=0.01, reward_std=1.0):
        self.n_arms = n_arms
        self.walk_std = walk_std
        self.reward_std = reward_std
        self.means = np.zeros(n_arms)  

    def step(self, action):
        
        self.means += np.random.normal(0, self.walk_std, self.n_arms)
      
        reward = np.random.normal(self.means[action], self.reward_std)
        return reward


def epsilon_greedy_nonstationary(bandit, epsilon=0.1, alpha=0.1, steps=10000):
    n_arms = bandit.n_arms
    Q = np.zeros(n_arms)     
    rewards = np.zeros(steps) 

    for t in range(steps):
        
        if np.random.rand() < epsilon:
            action = np.random.randint(n_arms)
        else:
            action = np.argmax(Q)

        
        reward = bandit.step(action)
        rewards[t] = reward

       
        Q[action] = Q[action] + alpha * (reward - Q[action])

    return Q, rewards


bandit = NonStationaryBandit()
Q_values, reward_history = epsilon_greedy_nonstationary(bandit, epsilon=0.1, alpha=0.1, steps=10000)


print("Final Estimated Q-values:", Q_values)
print("Best Action Learned:", np.argmax(Q_values) + 1)


plt.figure(figsize=(8,4))
plt.plot(np.convolve(reward_history, np.ones(200)/200, mode='valid'))
plt.title("Average Reward over Time (Modified Epsilon-Greedy)")
plt.xlabel("Time Steps")
plt.ylabel("Average Reward")
plt.grid(True)
plt.show()
