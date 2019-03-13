import numpy as np

class MultiClassPerceptron(object):
	def __init__(self,num_class,feature_dim):
		"""Initialize a multi class perceptron model.

		This function will initialize a feature_dim weight vector,
		for each class.

		The LAST index of feature_dim is assumed to be the bias term,
			self.w[:,0] = [w1,w2,w3...,BIAS]
			where wi corresponds to each feature dimension,
			0 corresponds to class 0.

		Args:
		    num_class(int): number of classes to classify
		    feature_dim(int): feature dimension for each example
		"""

		self.w = np.zeros((feature_dim+1,num_class))

	def train(self,train_set,train_label):
		""" Train perceptron model (self.w) with training dataset.

		Args:
		    train_set(numpy.ndarray): training examples with a dimension of (# of examples, feature_dim)
		    train_label(numpy.ndarray): training labels with a dimension of (# of examples, )
		"""

		# YOUR CODE HERE
		# should be abt 0.01
		learning_rate = 0.01
		print(len(train_set))
		for _ in range(100):
			print(_)
			sum_error = 0.0
			for idx in range(len(train_set)):
				#print("index "+str(idx))
				row = train_set[idx]
				prediction = self.predict(row)
				error = row[-1] - prediction
				sum_error += error**2
				self.w[0][0] = self.w[0][0] + learning_rate * error
				self.w[0][1] = train_label[0]
				for i in range(len(row)-1):
					self.w[i + 1][0] = self.w[i + 1][0] + learning_rate * error * row[i]
					self.w[i + 1][1] = train_label[i+1]

	def predict(self, row):
		activation = self.w[0][0]
		for i in range(len(row)-1):
			activation += self.w[i + 1][0] * row[i]
		if activation >= 0.0:
			return 1.0
		return 0.0

	def test(self,test_set,test_label):
		""" Test the trained perceptron model (self.w) using testing dataset.
			The accuracy is computed as the average of correctness
			by comparing between predicted label and true label.

		Args:
		    test_set(numpy.ndarray): testing examples with a dimension of (# of examples, feature_dim)
		    test_label(numpy.ndarray): testing labels with a dimension of (# of examples, )

		Returns:
			accuracy(float): average accuracy value
			pred_label(numpy.ndarray): predicted labels with a dimension of (# of examples, )
		"""

		# YOUR CODE HERE
		accuracy = 0
		pred_label = np.zeros((len(test_set)))

		pass

		return accuracy, pred_label

	def save_model(self, weight_file):
		""" Save the trained model parameters
		"""

		np.save(weight_file,self.w)

	def load_model(self, weight_file):
		""" Load the trained model parameters
		"""

		self.w = np.load(weight_file)
