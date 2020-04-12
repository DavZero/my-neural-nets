import numpy as np
from net.losses.loss import Loss
from net.activations.Sigmoid import sigmoid, sigmoid_prime

class BinaryCrossEntropy(Loss):
    def __init__(self, from_logits=False):
        self.from_logits = from_logits

    def call(self, y_true, y_pred):
        if self.from_logits:
            return y_true * -np.log(sigmoid(y_pred)) + (1 - y_true) * -np.log(1 - sigmoid(y_pred))
        else:
            return y_true * -np.log(y_pred) + (1 - y_true) * -np.log(1 - y_pred)

    def prime(self, y_true, y_pred):
        if self.from_logits:
            return y_true * -sigmoid_prime(y_pred) / sigmoid(y_pred) + (1 - y_true) * sigmoid_prime(y_pred) / (1 - sigmoid(y_pred))
        else:
            return y_true * -1 / y_pred + (1 - y_true) / (1 - y_pred)
