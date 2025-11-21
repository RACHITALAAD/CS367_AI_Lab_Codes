import numpy as np

class NonStationaryBandit:
    def _init_(self, n_arms=10, walk_std=0.01, reward_std=1.0):
        self.n_arms = n_arms
        self.walk_std = walk_std
        self.reward_std = reward_std
        self.means = np.zeros(n_arms) 

    def step(self, action):

        self.means += np.random.normal(0, self.walk_std, size=self.n_arms)
        
        
        reward = np.random.normal(self.means[action], self.reward_std)
        return reward


if __name__ == "_main_":
    bandit = NonStationaryBandit()
    for t in range(5):
        action = np.random.randint(0, 10)
        reward = bandit.step(action)
        print(f"Action: {action + 1}, Reward: {reward:.3f}")
