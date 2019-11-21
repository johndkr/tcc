#linguistic
import os, sys
sys.path.append('..\\..\\')

import string
import json

import spacy
import re

from spellchecker import SpellChecker
from unicodedata import normalize as unicodedata
from collections import Counter 
from googletrans import Translator

import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

from Microsservices.Linguistic import feeling_evaluator 
from Microsservices.CommonUtil.Log import log_util


## consult this before defining which word split will be used: https://machinelearningmastery.com/clean-text-machine-learning-python/

class LinguisticAnalyses():
  spellchecker = SpellChecker()
  log_manager = log_util.Log_Util(True)
  nlp = spacy.load('pt')

  def __init__(self):
    self.spellchecker = SpellChecker()
    self.__load_known_words()
  
  def __accent_remover(self, txt):
    ### this method removes all accents from a string
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

  def __remove_them_all(self, txt):
    # This method returns a string only containg numbers, letters and space
    nfkd = unicodedata.normalize('NFKD', txt)
    palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    return re.sub('[^a-zA-Z0-9 \\\]', '', palavraSemAcento)

  def __load_known_words(self):
    self.spellchecker.word_frequency.load_words(["Lula", "Bolsonaro"])

  def wrong_proportion(self, text):
    text_cleanned = self.__accent_remover(text)
    split_it = self.__remove_them_all(text_cleanned).lower().split()
    return len(self.spellchecker.unknown(split_it))/(len(split_it))
  
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

  def get_defined_word_types(self, txt):
    word_types = self.get_words_types(txt)

    result_json = {
      "verbos": sum('VERB' in type_tuple for type_tuple in word_types),
      "substantivos": sum('NOUN' or 'PROPN' in type_tuple for type_tuple in word_types),
      "adverbios": sum('ADV' in type_tuple for type_tuple in word_types),
      "pronomes": sum('PRON' in type_tuple for type_tuple in word_types),
      "artigos": sum('DET' in type_tuple for type_tuple in word_types),
      "adjetivo": sum('ADJ' in type_tuple for type_tuple in word_types),
      "numerais": sum('NUM' in type_tuple for type_tuple in word_types),
      "preposicoes": sum('ADP' in type_tuple for type_tuple in word_types),
      "conjuncoes": sum('CCONJ' or 'SCONJ' in type_tuple for type_tuple in word_types),
      "interjeicoes": 0
    }

    return result_json
 
  def count_words(self, txt):
    txt_sem_pontuacao = self.__remove_them_all(txt)
    return len(txt_sem_pontuacao.split())

  def get_entities(self, txt):
    # this method gets all entities within a given text.
    # IT IS SENSITIVE to grammar mistakes
    self.log_manager.debbug("Getting text entities...")

    doc = self.nlp(txt)
    return doc.ents

  def get_all_entities_vector(self, txt):
    # this method receives a text and counts its entities
    # IT IS SENSITIVE to grammar mistakes on the text

    self.log_manager.debbug("Counting entities mentioned on text")

    entities = self.get_entities(txt)
    entities = list(dict.fromkeys([str(ent) for ent in entities]))

    entities_type = [(entitie, txt.upper().count(str(entitie).upper())) for entitie in entities]

    return entities_type

  def count_entities(self, txt):
    # this method gets all entities within a given text.
    # IT IS SENSITIVE to grammar mistakes
    self.log_manager.debbug("Counting text entities...")
    return len(self.nlp(txt).ents)

  def count_upper_case_words(self, txt):
    clean_text = self.__remove_them_all(txt)
    return sum(map(str.isupper, clean_text.split()))

  def count_pronome_pessoal_eu_tu_voce(self, txt):
    clean_text = self.__remove_them_all(txt)

    count_pronomes = 0
    count_pronomes += clean_text.lower().split().count("eu")
    count_pronomes += clean_text.lower().split().count("tu")
    count_pronomes += clean_text.lower().split().count("voce")

    return count_pronomes

  def count_pronome_pessoal_nos(self, txt):
    clean_text = self.__remove_them_all(txt)

    count_pronomes = 0
    count_pronomes += clean_text.lower().split().count("nos")

    return count_pronomes

  def count_pronome_pessoal_elxs(self, txt):
    clean_text = self.__remove_them_all(txt)

    count_pronomes = 0
    count_pronomes += clean_text.lower().split().count("ele")
    count_pronomes += clean_text.lower().split().count("eles")
    count_pronomes += clean_text.lower().split().count("ela")
    count_pronomes += clean_text.lower().split().count("elas")

    return count_pronomes

  def count_caracteres(self, txt):
    return len(txt)

  def count_sentence_average_size(self, txt):
    sentences_set = sent_tokenize(txt)
    return sum(len(sentence.split()) for sentence in sentences_set) / len(sentences_set)

  def count_word_average_size(self, txt):
    clean_text = self.__remove_them_all(txt)
    words = clean_text.split()
    return sum(len(word) for word in words) / len(words)

  def __chances_based_word_type(self, types):
    verb = types['VERB'] if 'VERB' in types else 0
    noun = types['NOUN'] if 'NOUN' in types else 0
    adv = types['ADV'] if 'ADV' in types else 0

    if (verb == 0) or (noun == 0) or (adv == 0):
      return 1
    else:
      chance = (1/verb)*0.33 + (1/noun)*0.34 + (1/adv)*0.33
    return chance

  def make_linguistic_analyses_old(self, txt):
    result = {
      "Proportion" : self.wrong_proportion(txt),
      "WordsTypes" : self.count_words_types(txt),
      "Entities" : self.count_entities(txt),
    }

    prop_chance = result["Proportion"]/0.3
    
    if prop_chance < 1:
      fake_new_chance = 0.65*prop_chance + 0.35*self.__chances_based_word_type(result["WordsTypes"])
    else:
      fake_new_chance = 1

    result["FakeNewChance"] = fake_new_chance 

    return result

  def make_linguistic_analyses(self, txt):
    """ this method run all analysis for this module and return them within a json """

    return {}


if __name__ == "__main__":
    txt = "O Lula e o Machao de Assis foi solto ontem"

    analisator = LinguisticAnalyses()
    print(analisator.count_words_types(txt))
    print(analisator.count_entities(txt))
