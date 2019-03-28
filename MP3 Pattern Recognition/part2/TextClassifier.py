# TextClassifier.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Dhruv Agarwal (dhruva2@illinois.edu) on 02/21/2019
import math
import heapq

"""
You should only modify code within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
class TextClassifier(object):
    def __init__(self):
        """Implementation of Naive Bayes for multiclass classification

        :param lambda_mixture - (Extra Credit) This param controls the proportion of contribution of Bigram
        and Unigram model in the mixture model. Hard Code the value you find to be most suitable for your model
        """
        self.lambda_mixture = 0.0

        self.prior = []
        self.likelihood = []
        self.num_words = []

    def fit(self, train_set, train_label):
        """
        :param train_set - List of list of words corresponding with each text
            example: suppose I had two emails 'i like pie' and 'i like cake' in my training set
            Then train_set := [['i','like','pie'], ['i','like','cake']]

        :param train_labels - List of labels corresponding with train_set
            example: Suppose I had two texts, first one was class 0 and second one was class 1.
            Then train_labels := [0,1]
        """
        # TODO: Write your code here
        laplace=0.1
        class_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        prior_prob = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        for example in range(len(train_set)):
            class_count[train_label[example] - 1] += 1
        for i in range(14):
            prob = class_count[i]
            prob += laplace
            prob /= (len(train_label) + laplace*14)
            log_prob = math.log10(prob)
            prior_prob[i] = log_prob
        text_dict = []
        log_dict = []
        for i in range(14):
            text_dict.append({})
            log_dict.append({})
        for i in range(len(train_set)):
            for word in train_set[i]:
                for k in range(14):
                    text_dict[k][word]=0

        for i in range(len(train_set)):
            type = train_label[i] - 1
            for word in train_set[i]:
                text_dict[type][word] += 1

        num_words = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(14):
            for word in text_dict[i].keys():
                num_words[i] += text_dict[i][word]
        for i in range(14):
            k_keys_sorted = heapq.nlargest(20, text_dict[i],key=text_dict[i].get)
            print(k_keys_sorted)

        for i in range(14):
            for word in text_dict[i].keys():
                prob = (text_dict[i][word]+laplace)/(num_words[i] + laplace*len(text_dict[i].keys()))
                log_dict[i][word] = math.log10(prob)
        # print(text_dict[i].keys())

        self.prior = prior_prob.copy()
        self.likelihood = log_dict.copy()
        self.num_words = num_words.copy()

        return

    def predict(self, x_set, dev_label,lambda_mix=0.0):
        """
        :param dev_set: List of list of words corresponding with each text in dev set that we are testing on
              It follows the same format as train_set
        :param dev_label : List of class labels corresponding to each text
        :param lambda_mix : Will be supplied the value you hard code for self.lambda_mixture if you attempt extra credit

        :return:
                accuracy(float): average accuracy value for dev dataset
                result (list) : predicted class for each text
        """
        likelihood = self.likelihood
        prior = self.prior
        num_words = self.num_words
        accuracy = 0.0
        result = []
        index = 0
        for doc in x_set:
            class_prob = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            for type in range(14):
                class_prob[type] += prior[type]
                for word in doc:
                    if word in likelihood[type].keys():
                        class_prob[type] += likelihood[type][word]
                    else:
                        class_prob[type] += math.log10(1 / (num_words[type] + len(likelihood[type].keys())))
            max_idx = 0
            max_prob = 0
            for i in range(14):
                if 10**class_prob[i] >= max_prob:
                    max_prob = 10**class_prob[i]
                    max_idx = i
            result.append(max_idx + 1)
            if result[-1] == dev_label[index]:
                accuracy += 1
            index += 1

        accuracy /= len(x_set)
        return accuracy,result
