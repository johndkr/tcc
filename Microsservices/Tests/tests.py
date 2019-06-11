######################## SOURCE TESTS #########################
import unittest
import sys
sys.path.append('..\\..\\')

from Microsservices.CommonUtil.Log import log_util as Log_Util
from Microsservices.NewsOrigin import source_checking as Source_Checking
from Microsservices.Linguistic import linguistic as Linguistic


class TestSourceFactuality(unittest.TestCase):
	
	test_log_util = Log_Util.Log_Util(False)

	mock_source = Source_Checking.Source()
	ling_anal = Linguistic.LinguisticAnalyses(test_log_util)

	def test_source_update(self):

		#Source mock
		self.mock_source.update_name('BBC')
		self.mock_source.update_id(0)
		self.mock_source.update_political_bias(3)
		self.mock_source.update_factuality(0)
		self.mock_source.update_versions({
					"language":"PT-BR",
					"source_url": "https://www.bbc.com/portuguese", 
					"source_twitter_handler": "bbcbrasil", 
					"source_wikipedia_page": "BBC"
				})

		#Tests
		self.assertEqual(self.mock_source.source_name, 'BBC')
		self.assertEqual(self.mock_source.source_id, 0)
		self.assertEqual(self.mock_source.political_bias, 3)
		self.assertEqual(self.mock_source.factuality, 0)
		self.assertEqual(self.mock_source.versions, {
					"language":"PT-BR",
					"source_url": "https://www.bbc.com/portuguese", 
					"source_twitter_handler": "bbcbrasil", 
					"source_wikipedia_page": "BBC"
		})

	def test_wikipedia_has_page(self):

		wikipedia = Source_Checking.Wikipedia()
		wikipedia.define_name(self.mock_source.source_name)
		self.assertTrue(wikipedia.has_page())

	def test_wikipedia_extract_context(self):
		
		wikipedia = Source_Checking.Wikipedia()
		wikipedia.define_name(self.mock_source.source_name)
		self.assertEqual(wikipedia.extract_context(),'BBC')

	def test_source_load_save(self):

		self.mock_source.get_source_id('BBC')
		self.mock_source.load_source()
		# self.mock_source.save_source()
		self.assertEqual(self.mock_source.source_name, 'BBC')
	
	def test_wrong_proporstion_simple_br(self):

		text_sample = 'Joao roubou pao na casa do Jaoo ontem a noite'
		self.assertEqual(self.ling_anal.wrong_proportion(text_sample), 0.4)

	def test_top_n_words(self):
		text_sample = "John is the son of John second. Second son of John second is William second."
		response = [('second', 4), ('john', 3), ('is', 2), ('son', 2)]
		self.assertEqual(self.ling_anal.top_n_words(4, text_sample), response)
	
	def test_get_region(self):
		text_sample = "Os politicos de Sao Paulo sao menos corruptos que os do Rio de Janeiro. O Rio de Janeiro continua lindo"
		response = [('RJ', 'Rio de Janeiro', 2), ('SP', 'Sao Paulo', 1)]
		self.assertEqual(self.ling_anal.catch_state_mentions(text_sample, False), response)

if __name__ == '__main__':
	unittest.main()