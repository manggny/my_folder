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

def softmax(a):
    c = np.max(a)
    exp_a = np.exp(a-c) # for avoid the overflow problem!
    sum_exp_a = np.sum(exp_a)
    y = exp_a/sum_exp_a
    return y

def MSE(y,t):
    return 0.5*np.sum((y-t)**2)

def cross_entropy_error(y,t):
    delta = 1e-7
    return -np.sum(t*np.log(y+delta))


