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
    plt.grid()
    plt.show()

