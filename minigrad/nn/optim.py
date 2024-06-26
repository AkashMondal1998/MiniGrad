import numpy as np


class Optimizer:
  def __init__(self, params, lr):
    self.params = params
    self.lr = lr

  def zero_grad(self):
    for param in self.params:
      if param is not None:
        param.grad = None


class SGD(Optimizer):
  def __init__(self, parameters, lr=1e-3, momentum=0.0, nesterov=False):
    super().__init__(parameters, lr)
    self.m = momentum
    self.v = [np.zeros_like(t.data) for t in self.params]
    self.nesterov = nesterov

  def step(self):
    if self.m == 0:
      for param in self.params:
        param.data -= self.lr * param.grad
    if self.m > 0:
      for i, param in enumerate(self.params):
        self.v[i] = self.m * self.v[i] - self.lr * param.grad
        param.data += self.v[i]
    if self.m > 0 and self.nesterov:
      for i, param in enumerate(self.params):
        self.v[i] = self.m * self.v[i] - self.lr * param.grad
        param.data += self.m * self.v[i] - self.lr * param.grad


class RMSProp(Optimizer):
  def __init__(self, parameters, epsilon=1e-8, beta=0.9, lr=0.001):
    super().__init__(parameters, lr)
    self.ep = epsilon
    self.b = beta
    self.m = [np.zeros_like(t.data) for t in self.params]

  def step(self):
    for i, param in enumerate(self.params):
      self.m[i] = self.b * self.m[i] + (1 - self.b) * param.grad**2
      param.data -= self.lr / (np.sqrt(self.m[i]) + self.ep) * param.grad


class Adam(Optimizer):
  def __init__(self, parameters, beta1=0.9, beta2=0.999, epsilon=1e-8, lr=0.001):
    super().__init__(parameters, lr)
    self.b1 = beta1
    self.b2 = beta2
    self.ep = epsilon
    self.m = [np.zeros_like(t.data) for t in self.params]
    self.v = [np.zeros_like(t.data) for t in self.params]
    self.t = 0

  def step(self):
    self.t += 1
    for i, param in enumerate(self.params):
      self.m[i] = self.b1 * self.m[i] + (1 - self.b1) * param.grad
      self.v[i] = self.b2 * self.v[i] + (1 - self.b2) * param.grad**2
      m_t = self.m[i] / (1 - self.b1**self.t)
      v_t = self.v[i] / (1 - self.b2**self.t)
      param.data -= (self.lr * m_t) / (np.sqrt(v_t) + self.ep)
