import numpy as np
from time import time

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

		self.timer = time()

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
		train_time =  time()
		print("<<< training model... >>>")
		print("")
		#reading in 50000 images, mapping occurence of each value to corresponding pixel
		# class_dict {class -> pixel number -> pixel value}
		laplace = 0.1
		class_count=np.zeros(10)
		for example in range(len(train_set)):
		  class_count[train_label[example]]+=1

		class_dict = np.zeros(10*784*256).reshape(10,784,256)
		for curr_image in range(len(train_set)):
			image_type = train_label[curr_image]
			for pixel_idx in range(len(train_set[curr_image])):
				pixel_color = train_set[curr_image][pixel_idx]
				class_dict[image_type][pixel_idx][pixel_color] += 1

		print("<<< calculating likelihood... >>>")
		print("")

		log_dict = {}

		# calculates probability for each value with laplace smoothing
		for x in range(784):
			for y in range(255):
				for z in range(10):
					prob = ((class_dict[z][x][y]+laplace)/((class_count[z])+laplace*256))
					if prob in log_dict:
						self.likelihood[x][y][z] = log_dict[prob]
					else:
						log_val = np.log(prob)
						self.likelihood[x][y][z] = log_val
						log_dict[prob] =  log_val

		print("<<< creating likelihood set... >>>")

		print("<<< regurgitating sample likelihood for all classes on pixel 300 value 100 >>>")
		print(self.likelihood[300][100])
		print("")

		for class_num in range(10):
			prior_prob =  (class_count[class_num]+laplace)/(50000+laplace*10)
			if prior_prob != 0:
				prior_prob = np.log(prior_prob)
			self.prior[class_num] = prior_prob

		print("<<< creating prior probability set... >>>")
		print(self.prior)

		print("")
		print("<<< TRAINING COMPLETED >>>")
		print("Training took: "+str(int(time() - train_time))+" seconds")

		self.save_model("prior", "likelihood")
		print("")
		print("<<< SAVING MODELS >>>")

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
		test_time = time()
		print("<<< LOADING MODELS >>>")
		print("")
		self.load_model("prior.npy", "likelihood.npy")
		print("starting test")
		pred_label = np.zeros((len(test_set)))
		total_correct = 0
		null_cnt = 0

		for curr_image in range(len(test_set)):
			actual_label = test_label[curr_image]
			max_prob = -float("inf")
			for curr_class in range(10):
				curr_prob = self.prior[curr_class]
				for pixel_idx in range(len(test_set[curr_image])):
					pixel_color = test_set[curr_image][pixel_idx]
					curr_prob += self.likelihood[pixel_idx,pixel_color,curr_class]
				if curr_prob > max_prob:
					max_prob = curr_prob
					pred_label[curr_image] = curr_class
			if int(pred_label[curr_image]) == actual_label:
				total_correct += 1

		accuracy = total_correct / len(test_set)
		print("Current Test Accuracy at: "+str(accuracy*100)+"% with null cnt: "+str(null_cnt))
		print("")
		print(str(total_correct)+" out of 10,000 images correct")
		print("")
		print(pred_label)
		print("")
		print("Testing took: "+str(int(time() - test_time))+" seconds")
		print("")
		print("Naive Bayes train/test took: "+str(int(time() - self.timer))+" seconds")

		# classification_rate = np.zeros
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
		print("<<< LOADING MODELS >>>")
		print("")
		self.load_model("prior.npy", "likelihood.npy")
		feature_likelihoods = np.zeros((likelihood.shape[0],likelihood.shape[2]))
		for image_type in range(10):
			for color in range(128):
				for pixel in range(784):
					feature_likelihoods[pixel][image_type]+=self.likelihood[pixel][color+128][image_type]
		return feature_likelihoods


###
