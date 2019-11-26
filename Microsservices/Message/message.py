#message
import os, sys
sys.path.append('..\\..\\')

from googletrans import Translator
from collections import Counter 
from pyUFbr.baseuf import ufbr

from Microsservices.Message import feeling_evaluator 
from Microsservices.CommonUtil.Log import log_util

import re
import nltk
import json
import unicodedata
import sklearn

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

    def __kill_gremlins(self, text):
        cp1252 = {
            # from http://www.microsoft.com/typography/unicode/1252.htm
            u"\x80": u"\u20AC", # EURO SIGN
            u"\x82": u"\u201A", # SINGLE LOW-9 QUOTATION MARK
            u"\x83": u"\u0192", # LATIN SMALL LETTER F WITH HOOK
            u"\x84": u"\u201E", # DOUBLE LOW-9 QUOTATION MARK
            u"\x85": u"\u2026", # HORIZONTAL ELLIPSIS
            u"\x86": u"\u2020", # DAGGER
            u"\x87": u"\u2021", # DOUBLE DAGGER
            u"\x88": u"\u02C6", # MODIFIER LETTER CIRCUMFLEX ACCENT
            u"\x89": u"\u2030", # PER MILLE SIGN
            u"\x8A": u"\u0160", # LATIN CAPITAL LETTER S WITH CARON
            u"\x8B": u"\u2039", # SINGLE LEFT-POINTING ANGLE QUOTATION MARK
            u"\x8C": u"\u0152", # LATIN CAPITAL LIGATURE OE
            u"\x8E": u"\u017D", # LATIN CAPITAL LETTER Z WITH CARON
            u"\x91": u"\u2018", # LEFT SINGLE QUOTATION MARK
            u"\x92": u"\u2019", # RIGHT SINGLE QUOTATION MARK
            u"\x93": u"\u201C", # LEFT DOUBLE QUOTATION MARK
            u"\x94": u"\u201D", # RIGHT DOUBLE QUOTATION MARK
            u"\x95": u"\u2022", # BULLET
            u"\x96": u"\u2013", # EN DASH
            u"\x97": u"\u2014", # EM DASH
            u"\x98": u"\u02DC", # SMALL TILDE
            u"\x99": u"\u2122", # TRADE MARK SIGN
            u"\x9A": u"\u0161", # LATIN SMALL LETTER S WITH CARON
            u"\x9B": u"\u203A", # SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
            u"\x9C": u"\u0153", # LATIN SMALL LIGATURE OE
            u"\x9E": u"\u017E", # LATIN SMALL LETTER Z WITH CARON
            u"\x9F": u"\u0178", # LATIN CAPITAL LETTER Y WITH DIAERESIS
        }
        # map cp1252 gremlins to real unicode characters
        if re.search(u"[\x80-\x9f]", text):
            def fixup(m):
                s = m.group(0)
                return cp1252.get(s, s)
        
            if isinstance(text, str):
                # make sure we have a unicode string
                text = text
                text = re.sub(u"[\x80-\x9f]", fixup, text)
            return text

    def translate_pt_to_en(self, txt):
        """ translates text to english """
        translator = Translator()
        result = translator.translate(txt, src='pt')
        translator = None
        return str(result.text)

    def get_txt_feeling(self, txt):
        self.log_manager.debbug("Getting text feeling")
        txt = txt.replace('\n\n', ' ').replace('\n', ' ').replace('\t','').replace('\r', ' ')
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

if __name__ == "__main__":
    txt = open('E:\\Documentos Local\\GitHub\\tcc\\Microsservices\\MainProgram\\db\\fake\\' + str(2) + '.txt', encoding='utf-8').read()

    analisator = MessageAnalyses()
    print(analisator.get_txt_feeling(txt))
