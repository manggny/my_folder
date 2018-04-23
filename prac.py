import numpy as np
import matplotlib.pyplot as plt

def step_function(x):
    if x>0:
        return 1
    else:
        return 0

def sigmoid(x):
    return 1/(1+np.exp(-x))

x = np.arange(-5.0,5.0,0.1)
y = sigmoid(x)

plt.plot(x,y)
plt.ylim(-0.1,1.1)
plt.show()

def relu(x):
    return np.maximum(0,x)


