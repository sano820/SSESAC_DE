import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def AND(x1, x2):
  result = 0.5*x1 + 0.5*x2 - 0.7
  if result <= 0:
    return 0
  else:
    return 1


def plot_xy():
    x1 = np.arange(-1, 3, 0.1)
    x2 = -x1 + (0.7/0.5)
    plt.plot(x1,x2)
    plt.title("예시")
    plt.grid()
    plt.show()


def sigmoid(x):
  return 1 / (1 + np.exp(-x))

def relu(x):
  return np.maximum(0,x)

def plot_relu():
  x = np.arange(-100, 100, 0.1)
  y = relu(x)
  plt.plot(x, y)
  plt.title("Relu")
  plt.grid()
  plt.show()

def plot_sigmoid():
  x = np.arange(-10,5,0.1)
  y = sigmoid(x)
  plt.plot(x,y)
  plt.title("Sigmoid  ")
  plt.grid()
  plt.show()


