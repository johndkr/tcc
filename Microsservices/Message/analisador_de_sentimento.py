import pandas as pd
import os
import platform
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

from sklearn.naive_bayes import BernoulliNB

from datetime import datetime

if platform.system() == 'Windows':
    root = "\\data\\"
else:
    root = "/Message/data/"

path_to_source = os.path.abspath('..') + root + "imdb-reviews-pt-br.csv"

class Feeling_Evaluator(): 

    def __init__(self):
        filename = 'modelo_sentimmento.sav'
        if os.path.exists(filename):
            # load the model from disk
            self.vect = self.__set_vectorizer()
            self.vect.fit(pd.read_csv('text_vect_fit.csv'))
            self.classifier = pickle.load(open(filename, 'rb'))
        else:
            # save the model to disk
            self.df = pd.read_csv(path_to_source).sample(40000, random_state=42)
            self.df.sentiment = self.df['sentiment'].map({'pos': 1, 'neg': 0})
            self.vect = self.__set_vectorizer()
            self.classifier = self.__set_classifier()
            pickle.dump(self.classifier, open(filename, 'wb'))


    def __set_classifier(self):
        self.vect.fit(self.df.text_pt)
        text_vect = self.vect.transform(self.df.text_pt)
        self.df.text_pt.to_csv('text_vect_fit.csv', index=False)
        X_train,X_test,y_train,y_test = train_test_split(
            text_vect, 
            self.df.sentiment,
            test_size = 0.2, 
            random_state = 42
        )

        clf = LogisticRegression(random_state=0, solver='newton-cg')
        clf = clf.fit(X_train, y_train)
        
        return clf

    def __set_vectorizer(self):
        ## model 1 ##
        return CountVectorizer(ngram_range=(1, 1))
        ## model 2 ##
        #return TfidfVectorizer(ngram_range=(1,4), use_idf=True, lowercase=True, min_df=2, max_df=0.95)

    def model_1_test(self):
        start = datetime.now()
        vect = CountVectorizer(ngram_range=(1, 1))

        vect.fit(self.df.text_pt)
        text_vect = vect.transform(self.df.text_pt)

        X_train,X_test,y_train,y_test = train_test_split(
            text_vect, 
            self.df.sentiment,
            test_size = 0.2, 
            random_state = 42
        )

        clf = LogisticRegression(random_state=0, solver='newton-cg')
        clf = clf.fit(X_train, y_train)
        
        y_prediction = clf.predict(X_test)

        f1 = f1_score(y_prediction, y_test, average='weighted')

        print("SCORE MODELO 1 -> {0:.4f}%".format(f1))
        print("TEMPO -> ", str(datetime.now()-start))
    
    def model_2_test(self):
        start = datetime.now()
        vect = TfidfVectorizer(ngram_range=(1,4), use_idf=True, lowercase=True, min_df=2, max_df=0.95)
        vect.fit(self.df.text_pt)
        text_vect = vect.transform(self.df.text_pt)

        X_train,X_test,y_train,y_test = train_test_split(
            text_vect, 
            self.df.sentiment,
            test_size = 0.2, 
            random_state = 42
        )

        clf = LinearSVC(C=10, random_state=0)
        clf.fit(X_train, y_train)

        y_prediction = clf.predict(X_test)
        f1 = f1_score(y_prediction, y_test, average='weighted')
        print("SCORE MODELO 2 -> {0:.4f}%".format(f1))
        print("TEMPO -> ", str(datetime.now()-start))

    def model_3_test(self):
        start = datetime.now()
        vect = CountVectorizer(ngram_range=(1, 1))

        vect.fit(self.df.text_pt)
        text_vect = vect.transform(self.df.text_pt)

        X_train,X_test,y_train,y_test = train_test_split(
            text_vect, 
            self.df.sentiment,
            test_size = 0.2, 
            random_state = 42
        )

        clf = BernoulliNB().fit(X_train, y_train)

        # clf = LogisticRegression(random_state=0, solver='newton-cg')
        # clf = clf.fit(X_train, y_train)
        
        y_prediction = clf.predict(X_test)

        f1 = f1_score(y_prediction, y_test, average='weighted')

        print("SCORE MODELO 3 -> {0:.4f}%".format(f1))
        print("TEMPO -> ", str(datetime.now()-start))

    def get_txt_feeling(self, txt):
        return int(self.classifier.predict(self.vect.transform([txt]))[0])


if __name__ == "__main__":
    eval = Feeling_Evaluator()
    # eval.model_1_test()
    # eval.model_2_test()
    # eval.model_3_test()
    txt1 = "O Lula é um ladrão que roubou meu coração"
    print(txt1, "\n", eval.get_txt_feeling(txt1))
    txt2 = "O Bolsonaro é um canalha e deveria ser impeachado!"
    print(txt2, "\n", eval.get_txt_feeling(txt2))
