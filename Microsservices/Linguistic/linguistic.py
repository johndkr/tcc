#linguistic
import os
import string
import json
from spellchecker import SpellChecker
from collections import Counter 
from Microsservices.CommonUtil.Log import log_util

## consult this before defining which word split will be used: https://machinelearningmastery.com/clean-text-machine-learning-python/

STATE_CITIES_DICTIONARY = "../data/state_city_dictionary"

class LinguisticAnalyses():
  spellchecker = SpellChecker()
  log_manager = log_util.Log_Util(False)

  def __init__(self, log_mega_manager):
    self.spellchecker = SpellChecker()
    self.__states_keys_dictionary = self.__load_states_dic_keys()
    self.log_manager = log_mega_manager

  def __load_states_dic_keys(self):
    ##load states dictionary
    self.log_manager.info('Loading states dictionary file...')
    states_file_loaded = None
    try:
      path = os.path.join(__file__, STATE_CITIES_DICTIONARY)
      with open(path, 'a') as content_file:
        states_file_loaded = content_file.read()
        self.log_manager.info('Found file at: ' + path)
    except Exception as err:
      self.log_manager.err('Ops... something went wrong while loading states dictionaries! -- {}'.format(err.__context__))
      states_file_loaded = {}
    finally:
      return states_file_loaded

  def __text_cleanner(self, text):
    self.log_manager.debbug("cleanning text: {}...".format(text[0:15]))
    ### this method receives a dirty string and removes all its parameters
    ### currently it only strips the ponctuation
    return text.translate(str.maketrans('', '', string.punctuation))
        
  def top_n_words(self, n, text):
    ## https://www.geeksforgeeks.org/find-k-frequent-words-data-set-python/
    # split() returns list of all the words in the string 
    split_it = self.__text_cleanner(text).lower().split()
    
    # Pass the split_it list to instance of Counter class. 
    counter = Counter(split_it) 
      
    # most_common() produces k frequently encountered 
    # input values and their respective counts. 

    return counter.most_common(n)

  def wrong_proportion(self, text):
    split_it = self.__text_cleanner(text).lower().split()
    return len(self.spellchecker.unknown(split_it))/(len(split_it))
  
  def catch_state_mentions(self, text, also_in_lower):
    found =[]

    for key in self.__states_keys_dictionary:
      for city in self.__states_keys_dictionary[key]:
        count = text.count(city.lower())
        if count != 0:
          found.append((key, city, count))
    
    if(also_in_lower):
      for key in self.__states_keys_dictionary:
        for city in self.__states_keys_dictionary[key]:
          count = text.count(city.lower())
          if count != 0:
            found.append((key, city, count))

    return found