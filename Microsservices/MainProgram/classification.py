import os
import pandas as pd
import numpy as np
from sklearn import datasets, linear_model
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import matplotlib.pyplot as plt
import matplotlib.axis as axis
import matplotlib.dates as mdates
from datetime import date, timedelta, datetime
import seaborn as sn

def get_df(path):
	df = pd.read_excel(path, index_col=None)

	#Treating columns
	labelencoder = LabelEncoder()
	df['fake_or_true'] = labelencoder.fit_transform(df['fake_or_true'])
	df['author'] = labelencoder.fit_transform(df['author'])
	df['link'] = labelencoder.fit_transform(df['link'])
	df['category'] = labelencoder.fit_transform(df['category'])
	df['publication_date'] = labelencoder.fit_transform(df['publication_date'])
	df['nr_links'] = labelencoder.fit_transform(df['nr_links'])

	return df


def plot_cm(df):
	print(df.ravel())
	labels = ["Negative","Positive"]
	fig = plt.figure()
	ax = fig.add_subplot(111)
	cax = ax.matshow(df)
	fig.colorbar(cax)
	ax.set_xticklabels([''] + labels)
	ax.set_yticklabels([''] + labels)
	s = [['TN','FP'], ['FN', 'TP']]
	for i in range(2):
		for j in range(2):
			plt.text(j,i, str(s[i][j])+" = "+str(df[i][j]))
	plt.xlabel('Predicted')
	plt.ylabel('True')
	plt.show()

def show_cm(df):
	ndf = pd.DataFrame(df, index=['True Negative','True Positive'], columns=['Pred Negative','Pred Positive'])
	print(ndf)

def classify():
	#Train and test separation
	df = get_df('db/database.xls')
	X_train, X_test, y_train, y_test = train_test_split(df.loc[:, df.columns != 'fake_or_true'], df['fake_or_true'], test_size=0.30)

	#Classification
	#pred = KNeighborsRegressor(n_neighbors=10)
	#model = pred.fit(X_train, y_train)
	
	#Neural Network
	pred = MLPClassifier(hidden_layer_sizes=(10, 10, 10), max_iter=1000)
	model = pred.fit(X_train, y_train.values.ravel())

	#Prediction of train set
	y_train_pred = pred.predict(X_train)
	formatted_y_train_pred = []
	for item in y_train_pred:
		formatted_y_train_pred.append(int(item))
	acc_score_train = metrics.accuracy_score(y_train, formatted_y_train_pred)
	cm_train = metrics.confusion_matrix(y_train, formatted_y_train_pred)

	#Prediction of test set
	y_test_pred = pred.predict(X_test)
	formatted_y_test_pred = []
	for item in y_test_pred:
		formatted_y_test_pred.append(int(item))
	acc_score_test = metrics.accuracy_score(y_test, formatted_y_test_pred)
	cm_test = metrics.confusion_matrix(y_test, formatted_y_test_pred)

	#Metrics
	print("\n########## ACCURACY SCORE #############")
	print("Accuracy of test set:",acc_score_test)
	print("Accuracy of train set:",acc_score_train)
	print("#######################################\n")

	print("########## CONFUSION MATRIX TEST #############")
	show_cm(cm_test)
	print("###############################################\n")

	print("########## CONFUSION MATRIX TRAIN #############")
	show_cm(cm_train)
	print("###############################################\n")

classify()