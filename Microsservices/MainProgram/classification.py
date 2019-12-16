import os, sys
import json
import pandas as pd
import numpy as np
import platform
if platform.system() == 'Windows':
	sys.path.append('..\\..\\')
else:
	sys.path.append('../../')
from Microsservices.Linguistic import linguistic as Linguistic
from Microsservices.Message import message as Message
from Microsservices.NewsOrigin import source as NewsOrigin
from sklearn import datasets, linear_model
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn import metrics
from sklearn.model_selection import train_test_split, KFold, cross_val_score, cross_val_predict
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import matplotlib.pyplot as plt
import matplotlib.axis as axis
import matplotlib.dates as mdates
from datetime import date, timedelta, datetime
import seaborn as sn
import pickle

def get_df(path):
	df = pd.read_excel(path, index_col=None)

	#Treating columns
	#labelencoder = LabelEncoder()
	#df['fake_or_true'] = labelencoder.fit_transform(df['fake_or_true'])
	#df['author'] = labelencoder.fit_transform(df['author'])
	#df['link'] = labelencoder.fit_transform(df['link'])
	#df['category'] = labelencoder.fit_transform(df['category'])
	#df['publication_date'] = labelencoder.fit_transform(df['publication_date'])
	#df['nr_links'] = labelencoder.fit_transform(df['nr_links'])
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

def class_kfold(pred, x1,y1):
	kfold = KFold(n_splits=10)
	kfold.get_n_splits(x1)
	results_kfold = cross_val_score(pred, x1, y1, cv=kfold)
	y_pred = cross_val_predict(pred, x1, y1, cv=kfold)

	formatted_y_pred = []
	for item in y_pred:
		formatted_y_pred.append(int(item))

	acc_score = metrics.accuracy_score(y1, formatted_y_pred)
	cm = metrics.confusion_matrix(y1, formatted_y_pred)
	#Metrics
	print("\n------------ KFOLD SPLIT ------------")
	print("\n########## ACCURACY SCORE #############")
	print("Accuracy: %.4f%%" % (acc_score*100.0))
	print("\n")

	print("########## CONFUSION MATRIX #############")
	cm_formatted = [[0,0],[0,0]]
	cm_formatted[0][0] = cm[0][0]
	cm_formatted[0][1] = cm[0][1]
	cm_formatted[1][0] = cm[1][0]
	cm_formatted[1][1] = cm[1][1]
	show_cm(cm_formatted)
	print("\n")
	print("------------- END KFOLD SPLIT --------------\n")

	#Acc test, TP, TN, FP, FN
	res_kfold = [acc_score, cm_formatted[0][0],cm_formatted[0][1],cm_formatted[1][0],cm_formatted[1][1]]
	return res_kfold

def class_simple_split(pred, x1,y1):
	X_train, X_test, y_train, y_test = train_test_split(x1, y1, test_size=0.30)
	model = pred.fit(X_train, y_train)

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
	print("\n------------ SIMPLE SPLIT ------------")
	print("\n########## ACCURACY SCORE #############")
	print("Accuracy of test set: %.4f%%" % (acc_score_test*100.0))
	print("Accuracy of train set: %.4f%%" % (acc_score_train*100.0))
	print("\n")

	print("########## CONFUSION MATRIX TEST #############")
	cm_test = cm_test[[0,1],:][:,[0,1]]
	show_cm(cm_test)
	print("\n")

	print("########## CONFUSION MATRIX TRAIN #############")
	cm_train = cm_train[[0,1],:][:,[0,1]]
	show_cm(cm_train)
	print("\n")
	print("------------- END SIMPLE SPLIT --------------\n")

	#Acc test, TP, TN, FP, FN
	res_simple = [acc_score_test, cm_test[0][0],cm_test[0][1],cm_test[1][0],cm_test[1][1]]
	return res_simple

#from sklearn.tree import export_graphviz
#from subprocess import call
#from IPython.display import Image
#from graphviz import Source

def test_tree(x1,y1):
	pred = RandomForestClassifier(n_estimators=10)
	X_train, X_test, y_train, y_test = train_test_split(x1, y1, test_size=0.30)
	model = pred.fit(X_train, y_train)
	# Extract single tree
	estimator = model.estimators_[5]

	graph = Source(export_graphviz(estimator, out_file='tree.dot', 
                feature_names = x1.columns.ravel(),
                class_names = ['index','fake_or_true'],
                rounded = True, proportion = False, 
                precision = 2, filled = True))
	call(['dot', '-Tpng', 'tree.dot', '-o', 'tree.png', '-Gdpi=600'])
	Image(filename = 'tree.png')

def classify():
	#Train and test separation
	df = get_df('db/our_db_v2.xls')

	# KNN
	#pred = KNeighborsRegressor(n_neighbors=77)
	
	#Neural Network
	#pred = MLPClassifier(hidden_layer_sizes=(10, 10, 10), max_iter=1000)

	# Polinomial
	#pred = linear_model.LinearRegression()

	#Lasso
	#pred = linear_model.Lasso()
	i = 1
	nom_pred = ""
	pred = KNeighborsRegressor(n_neighbors=77)
	
	while(i != 0):
		print("Escolha o classificador: ")
		print("1) KNN (n=77)")
		print("2) Neural Network (10 layers, 1000 max iterations)")
		print("3) Lasso")
		print("4) Random Forest (100 estimators)")
		print("5) Naive Bayes")
		i = input()
		if i == "1":
			# KNN
			pred = KNeighborsRegressor(n_neighbors=77)
			nom_pred = "KNN"
		elif i == "2":
		 	#Neural Network
			pred = MLPClassifier(hidden_layer_sizes=(10, 10, 10), max_iter=1000)
			nom_pred = "NEURAL NETWORK"
		elif i == "3":
			#Lasso
			pred = linear_model.Lasso()
			nom_pred = "LASSO"
		elif i == "4":
			#Random Forest Classifier
			pred = RandomForestClassifier(n_estimators=100)
			nom_pred = "RANDOM FOREST"
		elif i == "5":
			#Naive Bayes Classifier
			pred = GaussianNB()
			nom_pred = "NAIVE BAYES"
		elif i == "0":
			break
		else:
			print("Entrada errada")

		print("\n *********************** " + nom_pred + " ***********************")
		class_kfold(pred,df.iloc[:, 3:27],df['fake_or_true'])
		class_simple_split(pred,df.iloc[:, 3:27],df['fake_or_true'])

		#test_tree(df.iloc[:, 2:26],df['fake_or_true'])

def classify_export():
	#Train and test separation
	df = get_df('db/our_db_v2.xls')
	res_vector = []

	pred = KNeighborsRegressor(n_neighbors=33)
	nom_pred = "KNN"
	print("\n *********************** " + nom_pred + " ***********************")
	res_kfold = class_kfold(pred,df.iloc[:, 3:27],df['fake_or_true'])
	res_simple = class_simple_split(pred,df.iloc[:, 3:27],df['fake_or_true'])
	res_kfold.append(nom_pred)
	res_kfold.append("KFold")
	res_simple.append(nom_pred)
	res_simple.append("Simple Split")
	res_vector.append(res_simple)
	res_vector.append(res_kfold)

	pred = GaussianNB()
	nom_pred = "NAIVE BAYES"
	print("\n *********************** " + nom_pred + " ***********************")
	res_kfold = class_kfold(pred,df.iloc[:, 3:27],df['fake_or_true'])
	res_simple = class_simple_split(pred,df.iloc[:, 3:27],df['fake_or_true'])
	res_kfold.append(nom_pred)
	res_kfold.append("KFold")
	res_simple.append(nom_pred)
	res_simple.append("Simple Split")
	res_vector.append(res_simple)
	res_vector.append(res_kfold)

	pred = MLPClassifier(hidden_layer_sizes=(10, 10, 10), max_iter=1000)
	nom_pred = "NEURAL NETWORK"
	print("\n *********************** " + nom_pred + " ***********************")
	res_kfold = class_kfold(pred,df.iloc[:, 3:27],df['fake_or_true'])
	res_simple = class_simple_split(pred,df.iloc[:, 3:27],df['fake_or_true'])
	res_kfold.append(nom_pred)
	res_kfold.append("KFold")
	res_simple.append(nom_pred)
	res_simple.append("Simple Split")
	res_vector.append(res_simple)
	res_vector.append(res_kfold)

	pred = RandomForestClassifier(n_estimators=100)
	nom_pred = "RANDOM FOREST"
	print("\n *********************** " + nom_pred + " ***********************")
	res_kfold = class_kfold(pred,df.iloc[:, 3:27],df['fake_or_true'])
	res_simple = class_simple_split(pred,df.iloc[:, 3:27],df['fake_or_true'])
	res_kfold.append(nom_pred)
	res_kfold.append("KFold")
	res_simple.append(nom_pred)
	res_simple.append("Simple Split")
	res_vector.append(res_simple)
	res_vector.append(res_kfold)

	df = pd.DataFrame(res_vector, columns=['Accuracy','TN','FN','FP','TP','Algorithm','Method'])
	print(df)

	i = 0
	while os.path.exists(str(os.getcwd()) + '/db/results_'+str(i)+'.xls'):
		i += 1
	df.to_excel(str(os.getcwd()) + '/db/results_'+str(i)+'.xls')

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

def make_statistics():
	base = get_df('db/our_db_v2.xls')

	base_fake = base.loc[base['fake_or_true'] == 'Falso']
	results_fake_dict = {
		'feeling': base_fake['feeling'].max(axis=0),
		'nr_links': truncate(base_fake['nr_links'].mean(axis=0), 2),
		'nr_locations': truncate(base_fake['nr_locations'].mean(axis=0), 2),
		'verbos': truncate(base_fake['verbos'].mean(axis=0), 2),
		'substantivos': truncate(base_fake['substantivos'].mean(axis=0), 2),
		'adverbios': truncate(base_fake['adverbios'].mean(axis=0), 2),
		'pronomes': truncate(base_fake['pronomes'].mean(axis=0), 2),
		'artigos': truncate(base_fake['artigos'].mean(axis=0), 2),
		'adjetivo': truncate(base_fake['adjetivo'].mean(axis=0), 2),
		'numerais': truncate(base_fake['numerais'].mean(axis=0), 2),
		'preposicoes': truncate(base_fake['preposicoes'].mean(axis=0), 2),
		'conjuncoes': truncate(base_fake['conjuncoes'].mean(axis=0), 2),
		'pontuacao': truncate(base_fake['pontuacao'].mean(axis=0), 2),
		'interjeicoes': truncate(base_fake['interjeicoes'].mean(axis=0), 2),
		'verbos_modais': truncate(base_fake['verbos_modais'].mean(axis=0), 2),
		'n_palvaras': truncate(base_fake['n_palvaras'].mean(axis=0), 2),
		'prop_palavras_erradas': truncate(base_fake['prop_palavras_erradas'].mean(axis=0), 2),
		'n_camel_case': truncate(base_fake['n_camel_case'].mean(axis=0), 2),
		'n_upper_case': truncate(base_fake['n_upper_case'].mean(axis=0), 2),
		'n_pronome_1': truncate(base_fake['n_pronome_1'].mean(axis=0), 2),
		'n_pronome_1_plural': truncate(base_fake['n_pronome_1_plural'].mean(axis=0), 2),
		'n_pronome_2': truncate(base_fake['n_pronome_2'].mean(axis=0), 2),
		'n_characteres': truncate(base_fake['n_characteres'].mean(axis=0), 2),
		'avg_sentence': truncate(base_fake['avg_sentence'].mean(axis=0), 2),
		'avg_word_length': truncate(base_fake['avg_word_length'].mean(axis=0), 2)
	}

	base_true = base.loc[base['fake_or_true'] == 'Verdadeiro']
	results_true_dict = {
		'feeling': base_true['feeling'].max(axis=0),
		'nr_links': truncate(base_true['nr_links'].mean(axis=0), 2),
		'nr_locations': truncate(base_true['nr_locations'].mean(axis=0), 2),
		'verbos': truncate(base_true['verbos'].mean(axis=0), 2),
		'substantivos': truncate(base_true['substantivos'].mean(axis=0), 2),
		'adverbios': truncate(base_true['adverbios'].mean(axis=0), 2),
		'pronomes': truncate(base_true['pronomes'].mean(axis=0), 2),
		'artigos': truncate(base_true['artigos'].mean(axis=0), 2),
		'adjetivo': truncate(base_true['adjetivo'].mean(axis=0), 2),
		'numerais': truncate(base_true['numerais'].mean(axis=0), 2),
		'preposicoes': truncate(base_true['preposicoes'].mean(axis=0), 2),
		'conjuncoes': truncate(base_true['conjuncoes'].mean(axis=0), 2),
		'pontuacao': truncate(base_true['pontuacao'].mean(axis=0), 2),
		'interjeicoes': truncate(base_true['interjeicoes'].mean(axis=0), 2),
		'verbos_modais': truncate(base_true['verbos_modais'].mean(axis=0), 2),
		'n_palvaras': truncate(base_true['n_palvaras'].mean(axis=0), 2),
		'prop_palavras_erradas': truncate(base_true['prop_palavras_erradas'].mean(axis=0), 2),
		'n_camel_case': truncate(base_true['n_camel_case'].mean(axis=0), 2),
		'n_upper_case': truncate(base_true['n_upper_case'].mean(axis=0), 2),
		'n_pronome_1': truncate(base_true['n_pronome_1'].mean(axis=0), 2),
		'n_pronome_1_plural': truncate(base_true['n_pronome_1_plural'].mean(axis=0), 2),
		'n_pronome_2': truncate(base_true['n_pronome_2'].mean(axis=0), 2),
		'n_characteres': truncate(base_true['n_characteres'].mean(axis=0), 2),
		'avg_sentence': truncate(base_true['avg_sentence'].mean(axis=0), 2),
		'avg_word_length': truncate(base_true['avg_word_length'].mean(axis=0), 2)
	}
	
	return results_true_dict, results_fake_dict


def classify_news(train, text):

	labelencoder = LabelEncoder()
	cols = ['verbos','substantivos','adverbios','pronomes','artigos','adjetivo','numerais','preposicoes','conjuncoes','pontuacao','interjeicoes','verbos_modais','n_palvaras','prop_palavras_erradas','n_camel_case','n_upper_case','n_pronome_1','n_pronome_1_plural','n_pronome_2','n_characteres','avg_sentence','avg_word_length']
	
	# df Linguistica
	ling = Linguistic.LinguisticAnalyses()
	news_data = ling.make_linguistic_analyses(text)
	df = pd.DataFrame.from_dict(list(news_data.items()))
	ndf = pd.DataFrame(columns=cols)
	ndf = ndf.append(pd.Series(df.T.values.tolist()[1], index=cols),ignore_index=True)

	#df Resto
	origin = NewsOrigin.SourceAnalyses()
	nr_links = origin.count_links(text)
	message = Message.MessageAnalyses()
	nr_locations = message.count_location_mentions(text)
	feeling = message.get_txt_feeling(text)
	ndf2 = pd.DataFrame([feeling,nr_links,nr_locations], index=['feeling','nr_links','nr_locations'])
	ndf = ndf2.T.join(ndf)

	if train:
		base = get_df('db/our_db_v2.xls')
		# pred = MLPClassifier(hidden_layer_sizes=(10, 10, 10), max_iter=1000)
		pred = KNeighborsRegressor(n_neighbors=33)
		# pred = RandomForestClassifier(n_estimators=100)
		base['fake_or_true'] = labelencoder.fit_transform(base['fake_or_true'])
		pred.fit(base.iloc[:,3:28], base['fake_or_true'])

	filename = 'modelo_25cols.sav'
	if os.path.exists(filename):
		# load the model from disk
		pred = pickle.load(open(filename, 'rb'))
	else:
		# save the model to disk
		pickle.dump(pred, open(filename, 'wb'))

	prediction = pred.predict(ndf)
	prediction = [int(i) for i in prediction]

	if prediction[0] == 0:
		fake_or_true = 'Falso'
	else:
		fake_or_true = 'Verdadeiro'
	print("Resultado: " + fake_or_true)

	return fake_or_true

#classify_news(False,'O novo governo da Argentina, comandado por Alberto Fernández, decidiu neste sábado (14) aumentar os impostos sobre as exportações agrícolas, uma medida justificada como "urgente" para enfrentar a "grave situação" das finanças públicas" do país, que é um dos maiores produtores e exportadores agrícolas do mundo.O aumento na taxação se junta a outra medida econômica anunciada neste sábado: o aumento no custo para a demissão de trabalhadores.')
#classify_export()
make_statistics()
