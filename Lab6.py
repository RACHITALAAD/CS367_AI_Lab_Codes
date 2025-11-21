import numpy as np
import matplotlib.pyplot as plt

# Step 1: Define the Hopfield Network
class HopfieldNetwork:
    def __init__(self, size):
        self.size = size
        self.weights = np.zeros((size, size))

    # Step 2: Train using Hebbian Learning
    def train(self, patterns):
        for p in patterns:
            self.weights += np.outer(p, p)
        np.fill_diagonal(self.weights, 0)  # No self-connections
        self.weights /= len(patterns)

    # Step 3: Recall function
    def recall(self, pattern, steps=5):
        output = pattern.copy()
        for _ in range(steps):
            output = np.sign(self.weights @ output)
        return output

# Step 4: Create binary 10x10 patterns (+1/-1)
def create_pattern(shape=(10,10), ones_ratio=0.5):
    pattern = np.random.choice([1, -1], size=shape, p=[ones_ratio, 1-ones_ratio])
    return pattern

# Step 5: Flatten pattern for network input
def flatten_pattern(pattern):
    return pattern.flatten()

# Step 6: Main Execution
if __name__ == "__main__":
    size = 100  # 10x10 pattern
    network = HopfieldNetwork(size)

    # Generate patterns
    p1 = flatten_pattern(create_pattern())
    p2 = flatten_pattern(create_pattern())

    # Train network
    network.train([p1, p2])

    # Test recall with noisy input
    noisy = p1.copy()
    noise_idx = np.random.choice(size, 10, replace=False)
    noisy[noise_idx] *= -1

    recalled = network.recall(noisy)

    # Reshape to 10x10 for visualization
    original = p1.reshape(10,10)
    recalled_img = recalled.reshape(10,10)

    # Display results
    plt.subplot(1,2,1)
    plt.title("Original Pattern")
    plt.imshow(original, cmap='gray')

    plt.subplot(1,2,2)
    plt.title("Recalled Pattern")
    plt.imshow(recalled_img, cmap='gray')

    plt.show()
