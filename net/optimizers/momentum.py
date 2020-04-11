from .optimizer import OptimizerBase

class Momentum(OptimizerBase):
    def __init__(self, learning_rate=0.01, mu=0.95):
        super().__init__()
        self.learning_rate = learning_rate
        self.mu = mu
        self.v = np.zeros(self.shape)

    def update(self, weights):
        return self.mu * self.v - self.learning_rate * weights