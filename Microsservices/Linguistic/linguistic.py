#linguistic
import unittest
import string
from spellchecker import SpellChecker
from collections import Counter 

## consult this before defining which word split will be used: https://machinelearningmastery.com/clean-text-machine-learning-python/

class LinguisticAnalyses():
  spellchecker = SpellChecker()

  def text_cleanner(self, text):
    ### this method receives a dirty string and removes all its parameters
    ### currently it only strips the ponctuation
    return text.translate(str.maketrans('', '', string.punctuation))
        
  def top_n_words(self, n, text):
    ## https://www.geeksforgeeks.org/find-k-frequent-words-data-set-python/
    # split() returns list of all the words in the string 
    split_it = self.text_cleanner(text).lower().split()
    
    # Pass the split_it list to instance of Counter class. 
    counter = Counter(split_it) 
      
    # most_common() produces k frequently encountered 
    # input values and their respective counts. 

    return counter.most_common(n)

  def wrong_proportion(self, text):
    vectext = text.split(' ')
    return len(self.spellchecker.unknown(vectext))/(len(vectext))
  
  def catch_state_mentions(self, text):
    found =[]
    states_keys_dictionary = {
      'AC' : 'Acre',
      'AL' : 'Alagoas',
      'AP' : 'Amapa',
      'AM' : 'Amazonas',
      'BA' : 'Bahia',
      'CE' : 'Ceara',
      'DF' : 'Distrito Federal',
      'ES' : 'Espirito Santo',
      'GO' : 'Goias',
      'MA' : 'Maranhao',
      'MT' : 'Mato Grosso',
      'MS' : 'Mato Grosso do Sul',
      'MG' : 'Minas Gerais',
      'PA' : 'Para',
      'PB' : 'Paraiba',
      'PR' : 'Parana',
      'PE' : 'Pernambuco',
      'PI' : 'Piaui',
      'RJ' : 'Rio de Janeiro',
      'RN' : 'Rio Grande do Norte',
      'RS' : 'Rio Grande do Sul',
      'RO' : 'Rondonia',
      'RR' : 'Roraima',
      'SC' : 'Santa Catarina',
      'SP' : 'Sao Paulo',
      'SE' : 'Sergipe',
      'TO' : 'Tocantins'}

    for key in states_keys_dictionary:
      count = text.count(states_keys_dictionary[key])
      if count != 0:
        found.append((key, count))

    return found