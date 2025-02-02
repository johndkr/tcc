from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import confusion_matrix

import numpy as np
import itertools
import matplotlib.pyplot as plt
import pandas as pandas
import os

class Feeling_Evaluator():

    def __init__(self):
        self.training_data, evaluation_data = self.preprocessing_step()
        self.vectorizer = CountVectorizer(binary = 'true')
        self.classifier = self.training_step(self.training_data, self.vectorizer)

    def get_all_data(self):
        root = "..\\data\\"
        path = os.path.join(__file__, root)
        
        data = []
        with open(path + "amazon_labelled.txt", "r") as text_file:
            data += text_file.read().split('\n')
        return data

    def preprocessing_data(self, data):
        processing_data = []
        for single_data in data:
            if len(single_data.split("\t")) == 2 and single_data.split("\t")[1] != "":
                processing_data.append(single_data.split("\t"))
        return processing_data

    def split_data(self, data):
        total = len(data)
        training_ratio = 0.75
        training_data = []
        evaluation_data = []

        for indice in range(0, total):
            if indice < total * training_ratio:
                training_data.append(data[indice])
            else:
                evaluation_data.append(data[indice])

        return training_data, evaluation_data

    def preprocessing_step(self):
        data = self.get_all_data()
        processing_data = self.preprocessing_data(data)

        return self.split_data(processing_data)

    def training_step(self, data, vectorizer):
        training_text = [data[0] for data in data]
        training_result = [data[1] for data in data]

        training_text = vectorizer.fit_transform(training_text)

        return BernoulliNB().fit(training_text, training_result)

    def analyse_text(self, classifier, vectorizer, text):
        return text, classifier.predict(vectorizer.transform([text]))

    def simple_evaluation(self, evaluation_data, classifier, vectorizer):
        evaluation_text     = [evaluation_data[0] for evaluation_data in evaluation_data]
        evaluation_result   = [evaluation_data[1] for evaluation_data in evaluation_data]

        total = len(evaluation_text)
        corrects = 0
        for index in range(0, total):
            analysis_result = self.analyse_text(classifier, vectorizer, evaluation_text[index])
            text, result = analysis_result
            corrects += 1 if result[0] == evaluation_result[index] else 0

        return corrects * 100 / total
        

    def create_confusion_matrix(self, evaluation_data, classifier, vectorizer):
        evaluation_text     = [evaluation_data[0] for evaluation_data in evaluation_data]
        actual_result       = [evaluation_data[1] for evaluation_data in evaluation_data]
        prediction_result   = []
        for text in evaluation_text:
            analysis_result = self.analyse_text(classifier, vectorizer, text)
            prediction_result.append(analysis_result[1][0])
        
        matrix = confusion_matrix(actual_result, prediction_result)
        return matrix

    def test(self):
        training_data, evaluation_data = self.preprocessing_step()
        vectorizer = CountVectorizer(binary = 'true')
        classifier = self.training_step(training_data, vectorizer)
        confusion_matrix_result = self.create_confusion_matrix(evaluation_data, classifier, vectorizer)

        df = pandas.DataFrame(
            confusion_matrix_result, 
            columns=["Negatives", "Positives"],
            index=["Negatives", "Positives"]
        )

        return df

    def get_text_feeling(self, txt):
        return self.analyse_text(self.classifier, self.vectorizer, txt)


