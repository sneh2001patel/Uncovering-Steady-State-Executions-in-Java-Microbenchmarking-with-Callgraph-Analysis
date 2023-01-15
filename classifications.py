import time
import random
import os.path
from os import path

from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC


random.seed(1000)

input_path = "vectors.txt"
label_path = "labels.txt"

training_per = 0.8
testing_per = 1-training_per

# Load in the data
input_data = open(input_path, 'r')
vect = []
d = input_data.readline().strip()
while d:
  d = d.split(" ")
  v = [float(x) for x in d]
  vect.append(v)

  d = input_data.readline().strip()


print("Number of vectors:", len(vect))
print("Number of features:", len(vect[0]))
print()

input_data = open(label_path, 'r')
labels = []

# 0 for warmup 1 for steady state
d = input_data.readline().strip()
while d:
  if "warm up state" in d:
    labels.append(0)
  else:
    labels.append(1)
  d = input_data.readline().strip()

data = []
for x in range(len(vect)):
  data.append([vect[x], labels[x]])

print("Number of warmup instances: %d (%0.3f percent)" %(labels.count(0), labels.count(0)/len(labels)*100))
print("Number of stable instances: %d (%0.3f percent)" %(labels.count(1), labels.count(1)/len(labels)*100))


training = []
training_vect = []
training_labels = []
testing = []
testing_vect = []
testing_labels = []

training_warm = 0
training_steady = 0
testing_warm = 0
testing_steady = 0

# Split up the data
random.shuffle(data)

for x in range(len(data)):
  if len(training)/len(data) < training_per:
    training.append(data[x])
    training_vect.append(data[x][0])
    training_labels.append(data[x][1])
    if data[x][1] == 1:
      training_steady += 1
    else:
      training_warm += 1
  else:
    testing.append(data[x])
    testing_vect.append(data[x][0])
    testing_labels.append(data[x][1])
    if data[x][1] == 1:
      testing_steady += 1
    else:
      testing_warm += 1    

print("Number of training vectors: %d (%0.1f percent)" %(len(training), training_per*100))
print("\tNumber of warmup instances: %d (%0.3f percent)" %(training_warm, training_warm/len(training)*100))
print("\tNumber of stable instances: %d (%0.3f percent)" %(training_steady, training_steady/len(training)*100))
print()
print("Number of testing vectors: %d (%0.1f percent)" %(len(testing), testing_per*100))
print("\tNumber of warmup instances: %d (%0.3f percent)" %(testing_warm, testing_warm/len(testing)*100))
print("\tNumber of stable instances: %d (%0.3f percent)" %(testing_steady, testing_steady/len(testing)*100))

#Classification

# Multi-layer Perceptron (MLP) Classifier
training_start = time.time()
MLP_model = MLPClassifier().fit(training_vect, training_labels)
training_time = time.time() - training_start
testing_start = time.time()
predictions = MLP_model.predict(testing_vect)
testing_time = time.time() - testing_start
print("Multi-layer Perceptron (MLP) Classifier")
print("Training time: %0.5f seconds" %training_time)
print("Prediction time: %0.5f seconds" %testing_time)
print('Accuracy: %.3f' % accuracy_score(testing_labels, predictions))
print('Precision: %.3f' % precision_score(testing_labels, predictions))
print('Recall: %.3f' % recall_score(testing_labels, predictions))
print('F1 Score: %.3f' % f1_score(testing_labels, predictions))
print()

# Random Forest (RF) Classifier  
training_start = time.time()
RT_model = RandomForestClassifier().fit(training_vect, training_labels)
training_time = time.time() - training_start
testing_start = time.time()
predictions = RT_model.predict(testing_vect)
testing_time = time.time() - testing_start
print("Random Forest (RF) Classifier")
print("Training time: %0.5f seconds" %training_time)
print("Prediction time: %0.5f seconds" %testing_time)
print('Accuracy: %.3f' % accuracy_score(testing_labels, predictions))
print('Precision: %.3f' % precision_score(testing_labels, predictions))
print('Recall: %.3f' % recall_score(testing_labels, predictions))
print('F1 Score: %.3f' % f1_score(testing_labels, predictions))
print()

# Decision Tree (DT) Classifier
training_start = time.time()
DT_model = DecisionTreeClassifier().fit(training_vect, training_labels)
training_time = time.time() - training_start
testing_start = time.time()
predictions = DT_model.predict(testing_vect)
testing_time = time.time() - testing_start
print("Decision Tree (DT) Classifier")
print("Training time: %0.5f seconds" %training_time)
print("Prediction time: %0.5f seconds" %testing_time)
print('Accuracy: %.3f' % accuracy_score(testing_labels, predictions))
print('Precision: %.3f' % precision_score(testing_labels, predictions))
print('Recall: %.3f' % recall_score(testing_labels, predictions))
print('F1 Score: %.3f' % f1_score(testing_labels, predictions))
print()

# K-Neighbors (KN) Classifier
training_start = time.time()
KNN_model = KNeighborsClassifier().fit(training_vect, training_labels)
training_time = time.time() - training_start
testing_start = time.time()
predictions = KNN_model.predict(testing_vect)
testing_time = time.time() - testing_start
print("K-Neighbors (KN) Classifier")
print("Training time: %0.5f seconds" %training_time)
print("Prediction time: %0.5f seconds" %testing_time)
print('Accuracy: %.3f' % accuracy_score(testing_labels, predictions))
print('Precision: %.3f' % precision_score(testing_labels, predictions))
print('Recall: %.3f' % recall_score(testing_labels, predictions))
print('F1 Score: %.3f' % f1_score(testing_labels, predictions))
print()

# C-Support Vector Classification (SVC) 
# *From SVM library
training_start = time.time()
SVC_model = SVC().fit(training_vect, training_labels)
training_time = time.time() - training_start
testing_start = time.time()
predictions = SVC_model.predict(testing_vect)
testing_time = time.time() - testing_start
print(" C-Support Vector Classification (SVC) ")
print("Training time: %0.5f seconds" %training_time)
print("Prediction time: %0.5f seconds" %testing_time)
print('Accuracy: %.3f' % accuracy_score(testing_labels, predictions))
print('Precision: %.3f' % precision_score(testing_labels, predictions))
print('Recall: %.3f' % recall_score(testing_labels, predictions))
print('F1 Score: %.3f' % f1_score(testing_labels, predictions))
print()
