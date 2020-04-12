import sys
sys.path.append('..')

import numpy as np
import matplotlib.pyplot as plt
from keras.datasets import mnist

from net.layers import Dense
from net.activations import Tanh
from net.losses import MSE
from net.optimizers import SGD
from net.utils import create_model, train, test, forward

def noise(image):
    noise = np.random.randn(*image.shape)
    noise = (noise > 1.2).astype('int')
    return np.array([[min(x, 1) for x in arr] for arr in image + noise])

def load_data(n):
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    x_train = x_train.reshape(x_train.shape[0], 1, 28*28)
    x_train = x_train.astype('float32')
    x_train /= 255

    x_test = x_test.reshape(x_test.shape[0], 1, 28*28)
    x_test = x_test.astype('float32')
    x_test /= 255

    x_train_noise = [noise(x) for x in x_train[:n]]
    x_test_noise = [noise(x) for x in x_test]
    return (x_train[:n], x_train_noise), (x_test, x_test_noise)

model = create_model([
    Dense(28 * 28, 30),
    Tanh(),
    Dense(30, 16),
    Tanh(),
    Dense(16, 30),
    Tanh(),
    Dense(30, 28 * 28)
], SGD, {'learning_rate': 0.1})
mse = MSE()

(x_train, x_train_noise), (x_test, x_test_noise) = load_data(1000)
train(model, mse, x_train_noise, x_train, epochs=50)
print('error on test set:', test(model, mse, x_test_noise, x_test))

encoder = model[:4]
decoder = model[4:]

f, ax = plt.subplots(5, 3)
for i in range(5):
    image = np.reshape(x_test_noise[i], (28, 28))
    code = forward(encoder, x_test_noise[i])
    reconstructed = np.reshape(forward(decoder, code), (28, 28))
    ax[i][0].imshow(image, cmap='gray')
    ax[i][1].imshow(np.reshape(code, (4, 4)), cmap='gray')
    ax[i][2].imshow(reconstructed, cmap='gray')
plt.show()
