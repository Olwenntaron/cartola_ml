#!/usr/bin/python
# encoding: utf-8
from sklearn import *
from sklearn.preprocessing import scale
import numpy as np
import matplotlib.pyplot as plt
import csv


def extract_features(X, features):
    return [[float(i[f]) for f in features] for i in X]


with open('train.csv', 'r')as trainfile, open('test.csv', 'r') as testfile:
    jogadores_train = [i for i in csv.DictReader(trainfile, delimiter=',')]
    jogadores_test  = [i for i in csv.DictReader(testfile, delimiter=',')]

features = ['pontos']
X_train = scale(extract_features(jogadores_train, features))
X_test = scale(extract_features(jogadores_test, features))

y_train = scale([float(i['variacao_pr']) for i in jogadores_train])


clf = 
clf.fit(X_train,y_train)

y_test = clf.predict(X_test)
y_real = scale(np.array([float(i['variacao_pr']) for i in jogadores_test]))
print sum(np.square(y_real - y_test))

#plt.plot(X_train, y_train, 'ro')
#plt.show()
