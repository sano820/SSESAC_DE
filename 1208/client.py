import module as md
import tensorflow
from tensorflow import keras
from keras.layers import Dropout

result = md.AND(1,1)
print(result)

md.plot_xy()
md.plot_relu()
md.plot_sigmoid()



train_scaled, train_target, test_scaled, test_target = md.data()

history, model = md.train(train_scaled, train_target, epochs=20, validation_split = 0.1, layer = keras.layers.Dropout(0.3))
md.plot_history(history)
md.eval(model, test_scaled, test_target)