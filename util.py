from __future__ import division

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
import timeit, itertools

# Assuming each label is integer label from 0 to n_labels - 1
# convert y_labels vector to matrix of one-hot-encoding vectors
# y_labels of form [[3], [4], [5], ...]
def one_hot_encode(oh_encoder, y_labels):
	return oh_encoder.transform(y_labels).toarray()

# wraps chunks of code that need to be timed into a callable function
def wrapper(fn, *args, **kwargs):
	def wrapped():
		return fn(*args, **kwargs)
	return wrapped

# train given classifer on given training data
def train_clf(clf, train_x, train_y):
	clf.fit(train_x, train_y)

# use given classifier to predict given data
def predict_clf(clf, test_x):
	clf.predict(test_x)

# returns key with largest associated value in a dict
def argmax_dict(dct):
	return max(dct.iterkeys(), key=lambda k: dct[k])

def cluster_lists(X,Y,Z,K):
	cluster_data_lists = []
	cluster_label_lists = []
	for k in range(K):
		cluster_data_list = np.array([X[i] for i in range(X.shape[0]) if Z[i] == k])
		cluster_data_lists.append(cluster_data_list)

		cluster_label_list = [Y[i] for i in range(Y.shape[0]) if Z[i] == k]
		cluster_label_list = set(cluster_label_list)
		cluster_label_lists.append(cluster_label_list)
	return cluster_data_lists, cluster_label_lists

def train_clusters(X, Y, Z, K, clf_class, arg_list):
	cluster_clfs = []
	cluster_data_lists, cluster_label_lists = cluster_lists(X, Y, Z, K)
	for k in range(K):
		data = cluster_data_lists[k]

	return cluster_clfs

def predict_clusters(X, Z, K, cluster_clfs):
	predicts = np.array([])
	for i in range(X.shape[0]):
		clf = cluster_lists[Z[i]]
		predict = clf.predict(X[i])
		predicts = np.vstack(predicts, predict) if predicts.size != 0 else predict
	return predicts
	
# Compute a cluster quality score given a data matrix X (N,D), a vector of 
# cluster indicators Z (N,), and the number of clusters K.
def cluster_quality(X,Z,K):
    cluster_lists = []
    var_sum = 0
    for k in range(K):
        cluster_list = [X[i] for i in range(X.shape[0]) if Z[i] == k]
        cluster_lists.append(cluster_list)
    for l in cluster_lists:
        n = len(l)
        sum_sq = 0
        for i in range(n-1):
            for j in range(i+1, n):
                sum_sq += (np.linalg.norm(l[i] - l[j]))**2
        var = 0 if n == 0 else sum_sq / n
        var_sum += var
    return var_sum

# returns training time, predict time and test accuracy for a given classifier
# on given train and test data
def train_predict_pipeline(clf, clf_name, train_x, train_y, 
	test_x, test_y, num_runs=1, one_hot_encoding=False):
	print "Classifier:", clf_name
	print "Fitting data {:d} time(s)...".format(num_runs)
	training_code = wrapper(train_clf, clf, train_x, train_y)
	training_time = timeit.timeit(training_code, number=num_runs) / num_runs # average 10 runs
	print "Training time: ", training_time

	print "\nPredicting data {:d} time(s)...".format(num_runs)
	predict_code = wrapper(predict_clf, clf, test_x)
	predict_time = timeit.timeit(predict_code, number=num_runs) / num_runs
	print "Predict time: ", predict_time
	print ""

	test_acc = 0.
	if one_hot_encoding == True:
		test_acc = clf.accuracy(test_x, test_y)
	else:
		predicted_test_y = clf.predict(test_x)
		test_acc = accuracy_score(test_y, predicted_test_y)
	print "Test accuracy:", test_acc
	return training_time, predict_time, test_acc

# split learning data into specified number of blocks
# default number of blocks to split into is 5
# returns a list of blocks
def split_learning_data(learning_data, num_blocks=5):
	np.random.seed(0)
	# before splitting, shuffle learning_data
	np.random.shuffle(learning_data)
	num_rows = np.shape(learning_data)[0]
	data_blocks = []
	for i in range(num_blocks):
		block = learning_data[num_rows*i/num_blocks:num_rows*(i+1)/num_blocks, :]
		data_blocks.append(block)
	return data_blocks

# print a dict
def print_dict(dct):
	for k, v in dct.iteritems():
		print "\tKey:", k, " - Score:", v

# perform cross validation using given classifier on given learning data, hyperparameter names and value ranges
# default is 5-fold
# returns a score_dict containing key:value pairs
# where key is a set of hyperparameter values and value is score (average validation set error)
# example hyperparameters input
# hp_names = ['metric', 'n_neighbors']
# hp_val_ranges = [['euclid', 'manhat', 'minkowski'], [1, 3, 5, 10]]
def cross_validation(clf, learning_data_x, learning_data_y, arg_list, hp_names, hp_val_ranges, 
	num_folds=5, one_hot_encoding=False):
	learning_data = np.hstack((learning_data_x, learning_data_y))
	y_col_range = learning_data_y.shape[1]
	data_blocks = split_learning_data(learning_data)

	# get all possible combinations of hyperparameter values
	val_range_combs = itertools.product(*hp_val_ranges)
	val_range_combs = list(val_range_combs)

	# Initialize score_dict
	score_dict = {}
	for comb in val_range_combs:
		key_dict = {}
		for i in range(len(hp_names)):
			key_dict[hp_names[i]] = comb[i]
		score_dict[str(key_dict)] = 0

	for i in range(num_folds):
		# pick one block as val_data
		val_data = data_blocks[i]
		val_y_true = val_data[:, -y_col_range:]
		val_x = val_data[:, :-y_col_range]
		num_val_data = np.shape(val_data)[0]

		# initialize train_data as 1xn zero matrix 
		# where n is number of columns of learning data
		# this sets up appropriate dimension to do vertical concatenation
		train_data = np.zeros((1, np.shape(learning_data)[1]))

		for j in range(num_folds):
			# if current block is not validation set, add it to training data
			if i != j:
				train_data = np.concatenate((train_data, data_blocks[j]))
		# delete first row of 0s from earlier
		train_data = np.delete(train_data, (0), axis=0)
		train_data_x = train_data[:, :-y_col_range]
		train_data_y = train_data[:, -y_col_range:]

		for comb in val_range_combs:
			arg_dict = {}
			for i in range(len(hp_names)):
				arg_dict[hp_names[i]] = comb[i]
			classifier = clf(*arg_list, **arg_dict)
			print "\tParam:"
			print_dict(arg_dict)
			classifier.fit(train_data_x, train_data_y)
			score = 0.
			if one_hot_encoding == True:
				score = classifier.accuracy(val_x, val_y_true)
			else:
				val_y_pred = classifier.predict(val_x)
				# score = np.sum(val_y_true != val_y_pred) / num_val_data
				score = accuracy_score(val_y_true, val_y_pred)
			score_dict[str(arg_dict)] += score
		
	for key, score in score_dict.iteritems():
		score_dict[key] = score / num_folds
	print "\tReturned score_dict:"
	print_dict(score_dict)
	print ""

	return score_dict