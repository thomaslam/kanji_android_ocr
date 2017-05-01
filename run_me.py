from __future__ import division
import struct
import os, time, timeit
from scipy import signal, misc

import numpy as np
import pandas as pd
from sklearn import svm, preprocessing
# from sklearn.neural_network import MLPClassifier
# from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

from util import *
from nn_model import *

X_train = []
y_train = []
X_test = []
y_test = []
figure_num = 1
label_encoder = preprocessing.LabelEncoder()
oh_encoder = preprocessing.OneHotEncoder()
start_time = time.clock()

# # Assuming each label is integer label from 0 to n_labels - 1
# # convert y_labels vector to matrix of one-hot-encoding vectors
# # y_labels of form [[3], [4], [5], ...]
# def one_hot_encode(oh_encoder, y_labels):
# 	return oh_encoder.transform(y_labels).toarray()

### Load CSV files into variables ######
print "\nLoading train data"
train_data_df = pd.read_csv("Data/train_data.csv")
X_train = train_data_df.ix[:, :-1].values
y_train_raw = train_data_df.ix[:, -1].values

label_encoder.fit(y_train_raw) # map raw labels to integer labels from 0 to n_labels-1
y_train = label_encoder.transform(y_train_raw)

print "X_train:", X_train.shape
print "y_train:", y_train.shape

print "\nLoading test data"
test_data_df = pd.read_csv("Data/test_data.csv")
X_test = test_data_df.ix[:, :-1].values
y_test_raw = test_data_df.ix[:, -1].values
y_test = label_encoder.transform(y_test_raw)
print "X_test:", X_test.shape
print "y_test:", y_test.shape

print "\nData prep time: ", time.clock() - start_time
print "========================"
########################################

### Clustering #########################
## Clustering quality
# c_qualities = []
# for c in range(2, 11, 2):
#     kmeans = KMeans(n_clusters=c, random_state=0).fit(X_train)
#     Z = kmeans.labels_
#     c_qualities.append(cluster_quality(Xtr, Z, c))

# print c_qualities
# plot_line_charts(figure_num, "Number of clusters", range(1, 41), (0, 42),
#                 "Cluster quality", c_qualities, (100, 3100),
#                 "../Figures/cluster_line_plot")
# figure_num += 1

## Clustering + Classification
########################################

### Linear SVM #########################
# clf = svm.LinearSVC(random_state=0)
# # pca = PCA(n_components=200)
# # pca.fit(X_train)
# # X_train_reduced = pca.transform(X_train)

# svm_train_time, svm_predict_time, svm_test_acc = train_predict_pipeline(clf, "Linear SVM", 
# 	X_train, y_train, X_test, y_test, num_runs=10)
print "========================"
########################################


### Neural Networks ####################
y_train_2d = [[l] for l in y_train]
y_test_2d = [[l] for l in y_test]
oh_encoder.fit(y_train_2d) # one-hot encoding
y_train_nn = one_hot_encode(oh_encoder, y_train_2d)
y_test_nn = one_hot_encode(oh_encoder, y_test_2d)

n_input = X_train.shape[1]
n_class = 100
n_hidden_list = [256, 256]
arg_list = [n_input, n_class, n_hidden_list]
# clf = multilayer_perceptron_class(n_input, n_class, n_hidden_list, 
# 	training_epochs=100, display_step=10)

# nn_train_time, nn_predict_time, nn_test_acc = train_predict_pipeline(clf, "Multilayer NN",
# 	X_train, y_train_nn, X_test, y_test_nn, num_runs=1, one_hot_encoding=True)

hp_values = [[0.001, 0.01, 0.1], [10, 100, 500]]
hp_names = ["learning_rate", "batch_size"]

print "Performing cross validation..."
print "Hyperparam:"
print "\t", hp_names
print "\t", hp_values
cv_dict = cross_validation(multilayer_perceptron_class, X_train, y_train_nn, 
	arg_list, hp_names, hp_values, num_folds=3, one_hot_encoding=True)
optimal_hp = argmax_dict(cv_dict)
print "Optimal set of hyperparameters:", optimal_hp
print ""

optimal_hp = eval(optimal_hp)
clf = multilayer_perceptron_class(*arg_list, **optimal_hp)
opt_nn_train_time, opt_nn_predict_time, opt_nn_test_acc = train_predict_pipeline(clf, "Optimal Multilayer NN", 
	X_train, y_train_nn, X_test, y_test_nn, num_runs=1, one_hot_encoding=True)
print "========================"
########################################

print "\n\nrun_me.py total time: ", time.clock() - start_time
print "========================\n"