import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Flatten, Dropout

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



# 실습하기
# 데이터 불러와서 전처리
def data():
  (train_input, train_target), (test_input, test_target) = keras.datasets.fashion_mnist.load_data()
  train_scaled = train_input / 255.0
  test_scaled = test_input / 255.0
  return train_scaled, train_target, test_scaled, test_target

# 모델정의하기
def model_fn(a_layer=None):
  model = keras.Sequential()
  model.add(keras.layers.Flatten(input_shape=(28, 28)))
  model.add(keras.layers.Dense(100, activation='relu'))
  if a_layer:
    model.add(a_layer)
  model.add(keras.layers.Dense(10, activation='softmax'))
  return model

# compile 및 학습
def train(x,y, epochs, validation_split, layer=None):
  model = model_fn(layer)
  model.compile(
    loss = 'sparse_categorical_crossentropy',
    metrics = ['accuracy'],
    optimizer = 'adam'
  )
  history = model.fit(x, y, epochs=epochs, verbose=2, validation_split = validation_split)
  print(model.summary())
  return history, model

# 학습 loss 그래프 그리기
def plot_history(history):
  history.history.keys()


  plt.plot(history.history['loss'])
  plt.plot(history.history['val_loss'])
  plt.xlabel('epoch')
  plt.ylabel('loss')
  plt.legend(['train', 'val'])
  plt.show()

# 모델 평가해보기.
def eval(model, x,y):
  print(model.evaluate(x,y))
