#linguistic
import unittest
from spellchecker import SpellChecker

class LinguisticAnalyses():
  spellchecker = SpellChecker()
        
  def top_n_words(self, n, text):

    return 0

  def wrong_proportion(self, text):
    vectext = text.split(' ')
    return len(self.spellchecker.unknown(vectext))/(len(vectext))