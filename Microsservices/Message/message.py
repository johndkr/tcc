#message
import os, sys
sys.path.append('..\\..\\')

from googletrans import Translator
from collections import Counter 
from pyUFbr.baseuf import ufbr

from Microsservices.Linguistic import feeling_evaluator 
from Microsservices.CommonUtil.Log import log_util

import re
import nltk
import json
import unicodedata

nltk.download('punkt')
from nltk.tokenize import sent_tokenize

STATE_CITIES_DICTIONARY = ".\\data\\state_city_dictionary"

class MessageAnalyses():
    log_manager = log_util.Log_Util(True)

    def __init__(self):
        self.__states_keys_dictionary = self.__load_states_dic_keys()

    def __remove_them_all(self, txt):
        # This method returns a string only containg numbers, letters and space
        nfkd = unicodedata.normalize('NFKD', txt)
        palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

        return re.sub('[^a-zA-Z0-9 \\\]', '', palavraSemAcento)

    def __load_states_dic_keys(self):
        ##load states dictionary
        self.log_manager.info('Loading states dictionary file...')
        states_file_loaded = None
        try:
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), STATE_CITIES_DICTIONARY)
            states_file_loaded = eval(open(path).read())
            self.log_manager.info('Found file at: ' + path)
        except Exception as err:
            self.log_manager.exception(err)
            states_file_loaded = {}
        finally:
            return states_file_loaded

    def translate_pt_to_en(self, txt):
        """ translates text to english """
        translator = Translator()
        result = translator.translate(txt, src='pt')
        translator = None
        return str(result.text)

    def get_txt_feeling(self, txt):
        self.log_manager.debbug("Getting text feeling")

        txt_en = self.translate_pt_to_en(txt)
        feeling = feeling_evaluator.get_text_feeling(txt_en)

        return int(feeling[1][0])

    def top_n_words(self, n, text):
        ## https://www.geeksforgeeks.org/find-k-frequent-words-data-set-python/
        # split() returns list of all the words in the string 
        split_it = self.__remove_them_all(text).lower().split()
        
        # Pass the split_it list to instance of Counter class. 
        counter = Counter(split_it) 
        
        # most_common() produces k frequently encountered 
        # input values and their respective counts. 

        return counter.most_common(n)

    def catch_state_mentions(self, text, also_in_lower):
        self.log_manager.info("Catching states for text {}".format(text[0:10]))
        
        found =[]
        # text = self.__text_cleanner(text).upper()

        for key in self.__states_keys_dictionary:
            for city in self.__states_keys_dictionary[key]:
                count = text.count(city)
                if count != 0:
                    found.append((key, city, count))
        
        if(also_in_lower):
            for key in self.__states_keys_dictionary:
                for city in self.__states_keys_dictionary[key]:
                    count = text.count(city.lower())
                    if count != 0:
                        found.append((key, city, count))

        return found

    def save_cities_learned(self):
        ### updates saved dictionary with the current one loaded on memory
        try:
            path = os.path.join(__file__, STATE_CITIES_DICTIONARY)
            with open(path, 'w') as file:
                file.write(json.dumps(self.__states_keys_dictionary))
        except Exception as err:
            self.log_manager.exception(err)

    def learn_new_cities(self, txt):
        # To learn new cities mentioned we search for it comparing in upper case
        
        text_cleanned = self.__remove_them_all(txt).upper()

        for state in ufbr.list_uf:
            cities_normalized = [self.__remove_them_all(city) for city in ufbr.list_cidades(state)]
            for city in cities_normalized:
                if city in text_cleanned:
                    # check if state is already known
                    if not state in self.__states_keys_dictionary:
                        self.__states_keys_dictionary[state] = []
                        self.__states_keys_dictionary[state].append(city.title())

        self.save_cities_learned()