import tensorflow as tf
import pickle

training = []

with open ('training_file', 'rb') as fp:
	while True:
		try:
			training.append(pickle.load(fp))
		except EOFError:
			break

import numpy as np
training = np.array(training).reshape(-1,5)

X_train = training[:,:4]
y_train = training[:,4]
#print(y_train.shape)
X_tf = tf.placeholder(dtype=tf.float32, shape=(None,4), name="X")
y_tf = tf.placeholder(dtype=tf.float32, name="y")

from tensorflow.contrib.layers import fully_connected

n_inputs = 4
n_hidden = 5
n_output = 1

hidden_layer = fully_connected(X_tf,n_hidden)
output = fully_connected(hidden_layer,n_output)

error = y_tf - output
loss = tf.reduce_mean(tf.pow(error,2))

optimizer = tf.train.AdamOptimizer(learning_rate=0.3,
		epsilon=1e-8,beta1=0.9,beta2=0.99)
training_operation = optimizer.minimize(loss)
saver = tf.train.Saver()

init = tf.global_variables_initializer()
with tf.Session() as sess:
	sess.run(init)

	for epoch in range(100):
		sess.run(training_operation,feed_dict={X_tf: X_train, y_tf: y_train})
		#print(error.eval(feed_dict={X_tf: X_train, y_tf:y_train}))
	save_path = saver.save(sess,"./game.cpkt")