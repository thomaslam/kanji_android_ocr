from __future__ import print_function

import tensorflow as tf

class multilayer_perceptron_class:
	def __init__(self, n_input, n_classes, n_hidden_list,
		learning_rate=0.001, training_epochs=100, batch_size=100, display_step=10):
		n_hidden_1, n_hidden_2 = n_hidden_list
		self.sess = tf.Session()

		self.training_epochs = training_epochs
		self.learning_rate = learning_rate
		self.batch_size = batch_size
		self.display_step = display_step

		self.x = tf.placeholder("float", [None, n_input])
		self.y = tf.placeholder("float", [None, n_classes]) # n_classes for one-hot encoding

		self.weights = {
			1: tf.Variable(tf.random_normal([n_input, n_hidden_1])),
			2: tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
			'o': tf.Variable(tf.random_normal([n_hidden_2, n_classes])) # n_classes
		}

		self.biases = {
			1: tf.Variable(tf.random_normal([n_hidden_1])),
			2: tf.Variable(tf.random_normal([n_hidden_2])),
			'o': tf.Variable(tf.random_normal([n_classes])) # n_classes
		}

		self.pred = self.output(self.x, self.weights, self.biases)

		self.cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=self.pred, labels=self.y))
		self.optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(self.cost)

		self.init = tf.global_variables_initializer()

	def output(self, x, weights, biases):
		# Hidden layer with RELU activation
		layer_1 = tf.add(tf.matmul(x, weights[1]), biases[1])
		layer_1 = tf.nn.relu(layer_1)
		# Hidden layer with RELU activation
		layer_2 = tf.add(tf.matmul(layer_1, weights[2]), biases[2])
		layer_2 = tf.nn.relu(layer_2)
		# Output layer with linear activation
		out_layer = tf.matmul(layer_2, weights['o']) + biases['o']
		return out_layer

	def fit(self, X_train, y_train):
		self.sess.run(self.init)

		for epoch in range(self.training_epochs):
			avg_cost = 0.
			total_batch = int(X_train.shape[0]/self.batch_size)
			# Loop over all batches
			for i in range(total_batch):
				batch_x = X_train[i*self.batch_size:(i+1)*self.batch_size]
				batch_y = y_train[i*self.batch_size:(i+1)*self.batch_size]
				# Run optimization op (backprop) and cost op (to get loss value)
				_, c = self.sess.run([self.optimizer, self.cost], feed_dict={self.x: batch_x,
															self.y: batch_y})
				# Compute average loss
				avg_cost += c / total_batch
			# Display logs per epoch step
			if epoch % self.display_step == 0:
				print("Epoch:", '%04d' % (epoch+1), "cost=", \
					"{:.9f}".format(avg_cost))
		print("Optimization Finished!")

	def predict(self, X):
		return self.sess.run(self.pred, feed_dict={self.x: X})

	def accuracy(self, X, y):
		# Test model
		correct_prediction = tf.equal(tf.argmax(self.pred, 1), tf.argmax(self.y, 1))
		# Calculate accuracy
		accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
		acc = accuracy.eval({self.x: X, self.y: y}, session=self.sess)
		print("Accuracy:", acc)
		return acc