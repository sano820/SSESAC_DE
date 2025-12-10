# import numpy as np 
# import matplotlib.pyplot as plt 
# import pandas as pd 
# from tensorflow import keras
# from tensorflow.keras.models import Sequential 
# from tensorflow.keras.layers import Dense, Activation, Input
# from tensorflow.keras.datasets import fashion_mnist


# from sklearn.model_selection import train_test_split

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Input
from tensorflow import keras
from sklearn.model_selection import train_test_split
from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras.layers  import Flatten

def AND(x1, x2):  
  result = 0.5*x1 + 0.5*x2 - 0.7  
  if result <= 0:
    return 0
  else:
    return 1

def plot_xy():
	x1 = np.arange(-1, 3, 0.1) 
	x2 = -x1 + (0.7/0.5) 
	plt.plot(x1, x2)
	plt.grid()
	plt.show()


def AND(x1, x2, x3=1):
    X = np.array([x1, x2])
    w = np.array([0.5, 0.5])
    b = x3 * (-0.7)
    y = np.dot(X, w) + b  # y = x1w1 + x2w2 + b

    if y <= 0:  # 활성화 함수 역할
        return 0
    else:
        return 1

def step_func(x): 
  if x > 0: 
    return 1 
  else: 
    return 0

def sigmoid(x): 
  return 1 / (1+np.exp(-x))

def relu(x): 
  return np.maximum(0,x)

def sig(x1,x2):
	x = np.arange(x1,x2,0.1)
	plt.plot(x, sigmoid(x))
	plt.grid()
	plt.show()

def rel(x1, x2):
	x = np.arange(x1, x2, 0.1)
	plt.plot(x, relu(x))
	plt.grid()
	plt.show()

def keras():
	data = np.random.random((1000,100))
	labels = np.random.randint(2, size=(1000,1))
	
	model = Sequential()
	model.add(Dense(32, activation='relu', input_dim=100))
	model.add(Dense(1, activation='sigmoid'))
	model.compile(optimizer = 'rmsprop', loss='binary_crossentropy',metrics=['accuracy'])

	model.fit(data, labels, epochs=10, batch_size=32)
	
	model.summary() 


# def data_process():
# 	(train_input, train_target), (test_input, test_target) = keras.datasets.fashion_mnist.load_data()
# 	# train_scaled = train_input / 255.0
# 	# train_scaled, val_scaled, train_target, val_target = train_test_split(train_scaled, train_target, test_size=0.2, random_state = 42)
# 	# retrun(train_scaled, val_scaled, train_target, val_target)

def data_process():
    (train_input, train_target), (test_input, test_target) = fashion_mnist.load_data()
    train_scaled = train_input / 255.0
    train_scaled, val_scaled, train_target, val_target = train_test_split(train_scaled, train_target, test_size=0.2, random_state=42)
    return (train_scaled, val_scaled, train_target, val_target)


def model_fn(a_layer=None):
	model = Sequential()
	model.add(Flatten(input_shape=(28,28)))
	model.add(Dense(100, activation='relu'))
	if a_layer:
		model.add(a_layer)
	model.add(Dense(10, activation='softmax'))
	return model
	


def compile_fit(model,train_sclaed, train_target, val_scaled, val_target):
    model.compile(loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    history = model.fit(train_sclaed, train_target, epochs=5, verbose=2, validation_data=(val_scaled, val_target))
    return history

# 그래프 그리기
def history_plot(history):
	plt.plot(history.history['loss'])  # 훈련 데이터의 손실값
	plt.plot(history.history['val_loss'])  # 검증 데이터의 손실값
	plt.xlabel('epoch')
	plt.ylabel('loss')
	plt.legend(['train','val'])
	plt.show()
