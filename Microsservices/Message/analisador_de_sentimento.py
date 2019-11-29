import pandas as pd
import os

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

from sklearn.naive_bayes import BernoulliNB

from datetime import datetime

root = "..\\data\\"
path_to_source = os.path.join(__file__, root, "imdb-reviews-pt-br.csv")

class Feeling_Evaluator(): 

    def __init__(self):
        self.df = pd.read_csv(path_to_source).sample(40000, random_state=42)
        self.df.sentiment = self.df['sentiment'].map({'pos': 1, 'neg': 0})
        self.vect = self.__set_vectorizer()
        self.classifier = self.__set_classifier()

    def __set_classifier(self):
        self.vect.fit(self.df.text_pt)
        text_vect = self.vect.transform(self.df.text_pt)

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
    print(eval.get_txt_feeling("Lula é ladrão e roubou milhões de brasileiros!"))
