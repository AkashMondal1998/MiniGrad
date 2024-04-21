# Minigrad

- Tensor (wrapper for numpy arrays)
- Dense Layer
- Forward pass
- Backward pass
- Sigmoid Activation 
- ReLU Activation 
- MSE loss
- Optimizer(SGD)



### A simple linear regression model using MiniGrad
``` python
from minigrad import Tensor
from minigrad.optim import SGD
import minigrad.nn as nn

# Neural network 
class Net(nn.Base):
    def __init__(self):
        self.l1 = nn.Linear(2,1)

    def forward(self,x):
        return self.l1(x)


# sample training data
x_train = Tensor([[2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8]])
y_train = Tensor([[10, 12, 14, 16, 18, 20]])

# instantiate the network    
model = Net()

# forward pass
model(x)

# optimizer
optim = SGD([model.l1.weight],lr=0.01)

# traning the model
epochs=100
for _ in range(epochs):
    optim.zero_grad() # zero the gradients (current implementation does not need this)
    loss = model(x_train).mean_squared_error(y_train)
    loss.backward()
    optim.step()   # upate the weights and bias
```