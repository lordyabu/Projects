import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
# keras is go to when building neural network (API)
from tensorflow.keras import layers
from tensorflow.keras.datasets import mnist

physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)

(x_train, y_train), (x_test, y_test) = mnist.load_data()
print(x_train.shape)  # prints (60000, 28, 28) aka 60000 images that are 28x28
print(y_train.shape)  # prints (60000,)

# flattens the values makes easier to send to network sets type as float for easier and divides by 255 to save space
# -1 means keep the value on dimension in this case 60000
# these are numpy arrays which gets converted to tensors automatically
x_train = x_train.reshape(-1, 28*28).astype("float32") / 255.0
x_test = x_test.reshape(-1, 28*28).astype("float32") / 255.0

# Sequential API (very convenient, not very flexible) bc 1 input to 1 output
model = tf.keras.models.Sequential(
    [
        tf.keras.Input(shape=(28*28)),
        layers.Dense(512, activation='relu'),  # a fully connected layer has 512 nodes and activation is relu
        layers.Dense(256, activation='relu'),
        layers.Dense(10),
    ]
)
# print(model.summary())  # able to print because of keras.layers.inputlayer
# import sys
# sys.exit()

# SEQUENTIAL
# both are ways to define model
model = tf.keras.models.Sequential()
model.add(tf.keras.Input(shape=784))
model.add(layers.Dense(512, activation='relu'))
# print(model.summary()) here it is helpful for debugging
model.add(layers.Dense(256, activation='relu', name='my_layer'))
model.add(layers.Dense(10))
# print(model.summary())  # able to print because of keras.layers.inputlayer

# model = tf.keras.Model(inputs=model.inputs, outputs=[layer.output for layer in model.layers])
# # model.layers[-2].output returns layer before output or model.get_layer('my_layer').output
# # feature = model.predict(x_train)
# # print(feature.shape)
#
# features = model.predict(x_train)
# for feature in features:
#     print(feature.shape)
# import sys
# sys.exit()

# this specifies network configuration

# Functional API
inputs = tf.keras.Input(shape=(784))
x = layers.Dense(512, activation='relu', name='first_layer')(inputs)
x = layers.Dense(256, activation='relu', name='second_layer')(x)
outputs = layers.Dense(10, activation='softmax')(x)
model = tf.keras.Model(inputs=inputs, outputs=outputs)
# print(model.summary())

model.compile(
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),  # tells keras how to configure training part changing from True to false for functional API
    # from_logits = true bc not self mapped activation so itll send into self map first then sparsecategorical
    # sparce means y train label are integer for correct label e.x for digit 3 y train will be 3
    optimizer=tf.keras.optimizers.Adam(learning_rate = 0.001),
    metrics=["accuracy"],
)

# specifies training of network
model.fit(x_train, y_train, batch_size=32, epochs=5, verbose=2)
model.evaluate(x_test, y_test, batch_size=32, verbose=2)  # add verbose=2 so prints after every for both
