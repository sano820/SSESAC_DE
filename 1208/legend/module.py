import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation

## AND연산 
def AND(x1, x2, x3 = 1) : 
  X = np.array([x1,x2])
  w = np.array([0.5,0.5])
  b = x3 * ( -0.7)
  y = np.dot(X, w) + b 
  
  if y <= 0 :
    return 0 
  else : 
    return 1
  
## setp_func 
def step_func(x) :
  if x > 0 : 
    return 1 
  else :
    return 0
  
def sigmoid(x) : 
  return 1 / (1+np.exp(-x))

def relu(x) : 
  return np.maximum(0,x)

def draw_line() : 
  x1 = np.arange(-1, 3, 0.1)
  x2 = -x1 + (0.7 / 0.5)
  plt.plot(x1, x2)
  plt.grid()
  plt.show()

def draw_sigmoid() : 
  x = np.arange(-10, 10, 0.1)
  x2 = sigmoid(x)
  plt.plot(x, x2)
  plt.grid()
  plt.show()

def draw_relu() : 
  x = np.arange(-10, 10, 0.1)
  x2 = relu(x)
  plt.plot(x, x2)
  plt.grid()
  plt.show()

def keras_exam() : 
  data = np.random.random((1000,100))
  labels = np.random.randint(2, size=(1000,1))

  model = Sequential()
  model.add(Dense(64, activation='relu', input_dim = 100))  ## 그 다음층 노드의 갯수 64개 , input의 차원이 100 - 행렬 100개 , output 32개로 
  model.add(Dense(1, activation='sigmoid'))                 ## Dense는 하나도 안빼놓고 다 연결한다는것 , input은 정의 안함 , output 1개로 왜냐하면 output이 1아니면 0 
  model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])  ##rmsprop은 경사하강법 metrics는 중간에 평가를 하고 싶음(정확도로)

  model.fit(data, labels, epochs=10, batch_size=32) ##batchsize -- 몇개씩 끊어서 진행하겠다

  model.summary()
