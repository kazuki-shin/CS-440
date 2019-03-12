import numpy as np

class NaiveBayes(object):
	def __init__(self,num_class,feature_dim,num_value):
		"""Initialize a naive bayes model.

		This function will initialize prior and likelihood, where
		prior is P(class) with a dimension of (# of class,)
			that estimates the empirical frequencies of different classes in the training set.
		likelihood is P(F_i = f | class) with a dimension of
			(# of features/pixels per image, # of possible values per pixel, # of class),
			that computes the probability of every pixel location i being value f for every class label.

		Args:
		    num_class(int): number of classes to classify
		    feature_dim(int): feature dimension for each example
		    num_value(int): number of possible values for each pixel
		"""

		self.num_value = num_value
		self.num_class = num_class
		self.feature_dim = feature_dim

		self.prior = np.zeros((num_class))
		self.likelihood = np.zeros((feature_dim,num_value,num_class))

	def train(self,train_set,train_label):
		""" Train naive bayes model (self.prior and self.likelihood) with training dataset.
			self.prior(numpy.ndarray): training set class prior (in log) with a dimension of (# of class,),
			self.likelihood(numpy.ndarray): traing set likelihood (in log) with a dimension of
				(# of features/pixels per image, # of possible values per pixel, # of class).
			You should apply Laplace smoothing to compute the likelihood.

		Args:
		    train_set(numpy.ndarray): training examples with a dimension of (# of examples, feature_dim)
		    train_label(numpy.ndarray): training labels with a dimension of (# of examples, )
		"""

		# YOUR CODE HERE

		print("<<< training model... >>>")
		print("")
		#reading in 50000 images, mapping occurence of each value to corresponding pixel
		# class_dict {class -> pixel number -> pixel value}
		class_dict={};
		for curr_image in range(len(train_set)):
			image_type = train_label[curr_image]
			for pixel_idx in range(len(train_set[curr_image])):
				pixel_color = train_set[curr_image][pixel_idx]
				if image_type in class_dict:
					if pixel_idx in class_dict[image_type]:
						if pixel_color in class_dict[image_type][pixel_idx]:
							class_dict[image_type][pixel_idx][pixel_color] += 1
						else:
							class_dict[image_type][pixel_idx][pixel_color] = 1
					else:
						 class_dict[image_type][pixel_idx] = {pixel_color: 1}
				else:
					class_dict[image_type] = {pixel_idx:{pixel_color: 1}}

		print("<<< calculating likelihood... >>>")
		print("")

		laplace = 1

		# calculates probability for each value with laplace smoothing
		for x in range(784):
			for y in range(255):
				for z in range(10):
					#print("On pixel: " +str(x) + " value: "+str(y)+" class: "+str(z))
					if class_dict[z][x].get(y) is not None:
						prob = (class_dict[z][x][y]+laplace)/(50000+laplace)     # laplace smoothing
						self.likelihood[x][y][z] = prob
					else:
						self.likelihood[x][y][z] = laplace/(50000+laplace)

		print("<<< creating likelihood set... >>>")

		print("<<< regurgitating sample likelihood for all classes on pixel 300 value 100 >>>")
		print(self.likelihood[300][100])
		print("")

		for class_num in range(10):
			self.prior[class_num] = (len(class_dict[class_num])+laplace)/(50000+laplace)

		print("<<< creating prior probability set... >>>")
		print(self.prior)

		print("")
		print("<<< TRAINING COMPLETED >>>")

		return



	def test(self,test_set,test_label):
		""" Test the trained naive bayes model (self.prior and self.likelihood) on testing dataset,
			by performing maximum a posteriori (MAP) classification.
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


	def save_model(self, prior, likelihood):
		""" Save the trained model parameters
		"""

		np.save(prior, self.prior)
		np.save(likelihood, self.likelihood)

	def load_model(self, prior, likelihood):
		""" Load the trained model parameters
		"""

		self.prior = np.load(prior)
		self.likelihood = np.load(likelihood)

	def intensity_feature_likelihoods(self, likelihood):
	    """
	    Get the feature likelihoods for high intensity pixels for each of the classes,
	        by sum the probabilities of the top 128 intensities at each pixel location,
	        sum k<-128:255 P(F_i = k | c).
	        This helps generate visualization of trained likelihood images.

	    Args:
	        likelihood(numpy.ndarray): likelihood (in log) with a dimension of
	            (# of features/pixels per image, # of possible values per pixel, # of class)
	    Returns:
	        feature_likelihoods(numpy.ndarray): feature likelihoods for each class with a dimension of
	            (# of features/pixels per image, # of class)
	    """
	    # YOUR CODE HERE

	    feature_likelihoods = np.zeros((likelihood.shape[0],likelihood.shape[2]))

	    return feature_likelihoods

def load_dataset(data_dir=''):
    """Load the train and test examples
    """
    x_train = np.load("data/x_train.npy")
    y_train = np.load("data/y_train.npy")
    x_test = np.load("data/x_test.npy")
    y_test = np.load("data/y_test.npy")

    return x_train, y_train, x_test, y_test

if __name__=="__main__":
	# Load dataset.
    x_train, y_train, x_test, y_test = load_dataset()
    # Initialize naive bayes model.
    num_class = len(np.unique(y_train))
    feature_dim = len(x_train[0])
    num_value = 256
    NB = NaiveBayes(num_class,feature_dim,num_value)
    # Train model.
    NB.train(x_train,y_train)



# space for comfort
