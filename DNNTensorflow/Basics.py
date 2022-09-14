import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)

# Initialize tensors

x = tf.constant(4, shape=(1, 1), dtype=tf.float32)  # 1x1 matrix with value 4 of type float
x = tf.constant([[1, 2, 3], [4, 5, 6]])  # 2x3 matrix
x = tf.ones((3, 3))  # 3x3 matrix of ones
x = tf.zeros((2, 3))  # 2x3 matrix of zeroes
x = tf.eye(3)  # Identity matrix of size 3x3
x = tf.random.normal((3, 3), mean=0, stddev=1)  # random 3x3 matrix with values having mean 0, standard deviation 1
x = tf.random.uniform((1, 3), minval=0, maxval=1)  # 1x3 vector filled with random numbers between 0 and 1
x = tf.range(9)  # vector from 0 to 9 not inclusive
x = tf.range(start=1, limit=10, delta=2)  # 1,3,5,7,9
x = tf.cast(x, dtype=tf.float64)  # similar to copy constructor
# tf.float(16,32,64), tf.int(8, 16, 32, 64), tf.bool

# Mathematical operations  
x = tf.constant([1, 2, 3])
y = tf.constant([9, 8, 7])
z = tf.add(x, y)
z = x + y  # same as previous line

z = tf.subtract(x, y)
z = x - y

z = tf.divide(x, y)
z = x / y

z = tf.multiply(x, y)
z = x * y

z = tf.tensordot(x, y, axes=1)  # dot products
z = tf.reduce_sum(x*y, axis=0)

z = x ** 5  # multiply each element by 5

x = tf.random.normal((2, 3))
y = tf.random.normal((3, 4))
z = tf.matmul(x, y)  # matrix multiplication
z = x @ y  # same as above

# Indexing
x = tf.constant([0, 1, 1, 2, 3, 1, 2, 3])

# print(x[:])  # prints all elements of x
# print(x[1:]) # prints everything but first value
# print(x[1:3])  # prints index 1,3 non-inclusive for 3
# print(x[::2])  # skips every other element
# print(x[::-1])  # prints in reverse order

indices = tf.constant([0, 3])
x_ind = tf.gather(x, indices)
# print(x_ind)  # prints 0 and 2 which were indices extracted

x = tf.constant([[1, 2], [3, 4], [5, 6]])

# print(x[0, :])  # prints 1,2 which is 0th dimension
# print(x[0:2, :])  # prints 2x2 matrix of 1,2 and 3,4

# Reshaping

x =tf.range(9)
x = tf.reshape(x, (3, 3))  # puts the vector into 3x3 matrix
x= tf.transpose(x, perm=[1, 0])  # swaps the axis
print(x)

