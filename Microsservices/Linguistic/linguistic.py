#linguistic
import os, sys
import string
import json

import spacy

from spellchecker import SpellChecker
from unicodedata import normalize
from pyUFbr.baseuf import ufbr
from collections import Counter 
from googletrans import Translator

from Microsservices.Linguistic import feeling_evaluator 
from Microsservices.CommonUtil.Log import log_util


## consult this before defining which word split will be used: https://machinelearningmastery.com/clean-text-machine-learning-python/

STATE_CITIES_DICTIONARY = ".\\data\\state_city_dictionary"

class LinguisticAnalyses():
  spellchecker = SpellChecker()
  log_manager = log_util.Log_Util(True)
  nlp = spacy.load('pt')

  def __init__(self):
    self.spellchecker = SpellChecker()
    self.__states_keys_dictionary = self.__load_states_dic_keys()

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

  def __text_cleanner(self, text):
    self.log_manager.debbug("cleanning text: {}...".format(text[0:15]))
    ### this method receives a dirty string and removes all its parameters
    ### currently it only strips the ponctuation
    return text.translate(str.maketrans('', '', string.punctuation))
  
  def __accent_remover(self, txt):
    ### this method removes all accents from a string
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

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
    text_cleanned = self.__accent_remover(text)
    split_it = self.__text_cleanner(text_cleanned).lower().split()
    return len(self.spellchecker.unknown(split_it))/(len(split_it))
  
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
    ## To learn new cities mentioned we search for it comparing in upper case
    
    text_cleanned = self.__accent_remover(self.__text_cleanner(txt)).upper()

    for state in ufbr.list_uf:
      cities_normalized = [self.__accent_remover(city) for city in ufbr.list_cidades(state)]
      for city in cities_normalized:
        if city in text_cleanned:
            # check if state is already known
            if not state in self.__states_keys_dictionary:
              self.__states_keys_dictionary[state] = []
            self.__states_keys_dictionary[state].append(city.title())

    self.save_cities_learned()

  def get_words_types(self, txt):
    self.log_manager.debbug("Getting words types...")
    
    doc = self.nlp(txt)
    return [(token.orth_, token.pos_) for token in doc]

  def count_words_types(self, txt):
    # this method reveices a text and returns all its words types counted in touples
    # IT IS SENSITIVE to grammar mistakes in portuguese.
    self.log_manager.info("Counting words types")
    types_count = {}
    types_tag_tuples = self.get_words_types(txt)

    for tutuple in types_tag_tuples:
      if tutuple[1] not in types_count:
        types_count[tutuple[1]] = 1
      else:
        types_count[tutuple[1]] += 1

    return types_count

  def get_entities(self, txt):
    # this method gets all entities within a given text.
    # IT IS SENSITIVE to grammar mistakes
    self.log_manager.debbug("Getting text entities...")

    doc = self.nlp(txt)
    return doc.ents

  def count_entities(self, txt):
    # this method receives a text and counts its entities
    # IT IS SENSITIVE to grammar mistakes on the text

    self.log_manager.debbug("Counting entities mentioned on text")

    entities = self.get_entities(txt)
    entities = list(dict.fromkeys([str(ent) for ent in entities]))

    entities_type = [(entitie, txt.upper().count(str(entitie).upper())) for entitie in entities]

    return entities_type

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

  def __chances_based_word_type(self, types):
    verb = types['VERB'] if 'VERB' in types else 0
    noun = types['NOUN'] if 'NOUN' in types else 0
    adv = types['ADV'] if 'ADV' in types else 0

    if (verb == 0) or (noun == 0) or (adv == 0):
      return 1
    else:
      chance = (1/verb)*0.33 + (1/noun)*0.34 + (1/adv)*0.33
    return chance

  def make_linguistic_analyses(self, txt):
    result = {
      "Proportion" : self.wrong_proportion(txt),
      "Locations" : self.catch_state_mentions(txt, True),
      "WordsTypes" : self.count_words_types(txt),
      "Entities" : self.count_entities(txt),
      "Feeling" : self.get_txt_feeling(txt)
    }

    prop_chance = result["Proportion"]/0.3
    
    if prop_chance < 1:
      fake_new_chance = 0.65*prop_chance + 0.35*self.__chances_based_word_type(result["WordsTypes"])
    else:
      fake_new_chance = 1

    result["FakeNewChance"] = fake_new_chance

    return result