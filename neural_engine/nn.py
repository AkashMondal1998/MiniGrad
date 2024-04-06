import numpy as np


# Base class for adding functionalities
class Base:
    def __repr__(self):
        layers = (f"({layer_name}): {layer}" for layer_name, layer in vars(self).items())
        return self.__class__.__name__ + "(\n" + "\n".join(layers) + "\n)"
    
    def __call__(self, x):
        return self.forward(x)

    def parameters(self):
        for layer in vars(self).values():
            if isinstance(layer, Layer):
                for neuron in layer._neurons:
                    yield neuron._w
                    yield neuron._b


# A Neuron
class Neuron:
    def __init__(self, in_features):
        self._w = np.random.rand(in_features, 1)
        self._b = np.random.rand(1, 1)

    def __repr__(self):
        return f"Neuron(w={self._w.shape},b={self._b.shape})"

    def __call__(self, x):
        return x @ self._w + self._b


# A Layer of Neurons
class Layer:
    def __init__(self, in_features, no_of_neurons):
        self._in = in_features
        self._neurons = tuple(Neuron(in_features) for _ in range(no_of_neurons))

    def __repr__(self):
        return f"Layer(in_features = {self._in}, out_features = {len(self._neurons)})"

    def __call__(self, x):
        if x.ndim != 2:
            raise ValueError("Input must be a 2D matrix")
        return np.concatenate(tuple(neuron(x) for neuron in self._neurons), axis=1)


# Mean Squared error loss function
class MSELoss:
    def __call__(self, x, y):
        if x.shape != y.shape:
            raise ValueError("mat1 and mat2 be must have same shape")
        return np.mean(np.square(x - y))


# Binary CrossEntropy Loss
# handle numerical instabality
class BCELoss:
    def __call__(self, x, y):
        if x.shape != y.shape:
            raise ValueError("mat1 and mat2 be must have same shape")
        return np.mean(-y * np.log(x) + (1 - y) * np.log(1 - x))


# ReLU Activation
class ReLU:
    def __call__(self, x):
        return np.where(x > 0, x, 0)

    def __repr__(self):
        return f"ReLU()"


# Sigmoid Activation
class Sigmoid:
    def __call__(self, x):
        max_x = np.max(x)
        return np.exp(x - max_x) / (1 + np.exp(x - max_x))

    def __repr__(self):
        return f"Sigmoid()"
