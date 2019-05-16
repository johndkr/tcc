#linguistic
import unittest
from spellchecker import SpellChecker

class LinguisticAnalyses():
  spellchecker = SpellChecker()
        
  def top_n_words(self, n, text):
    return 0

  def wrong_proportion(self, text):
    return self.spellchecker.unknown(text)/(len(text))


######################## TESTS ######################### 

# class TestLiguisticAnalyses(unittest.TestCase):
#     ling_anal = LinguisticAnalyses()

#     def wrong_proporstion_simple_br(self):
#         #Source mock
#         text_sample = 'Joao roubou poa na casa do Jaoo'
#         vec_txt = text_sample.split(' ')
#         #Tests
#         self.assertEqual(self.ling_anal.wrong_proportion(vec_txt), 0.2)

# if __name__ == '__main__':
# 	unittest.main()
