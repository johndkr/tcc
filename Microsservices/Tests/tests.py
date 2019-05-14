######################## SOURCE TESTS #########################
import unittest
import sys
sys.path.append('../../')

from Microsservices.NewsOrigin import source_checking as Source_Checking
from Microsservices.Linguistic import linguistic as Linguistic


class TestSourceFactuality(unittest.TestCase):
	
	mock_source = Source_Checking.Source()
	
	def test_source_update(self):

		#Source mock
		self.mock_source.update_name('BBC')
		self.mock_source.update_id(0)
		self.mock_source.update_url('https://bbc.co.uk/')
		self.mock_source.update_twitter_handler('BBC')
		self.mock_source.update_wikipedia_page('BBC')
		self.mock_source.update_political_bias(3)
		self.mock_source.update_factuality(0)

		#Tests
		self.assertEqual(self.mock_source.source_name, 'BBC')
		self.assertEqual(self.mock_source.source_id, 0)
		self.assertEqual(self.mock_source.source_url, 'https://bbc.co.uk/')
		self.assertEqual(self.mock_source.source_twitter_handler, 'BBC')
		self.assertEqual(self.mock_source.source_wikipedia_page, 'BBC')
		self.assertEqual(self.mock_source.political_bias, 'Center')
		self.assertEqual(self.mock_source.factuality, 'Low')

	def test_wikipedia_has_page(self):

		wikipedia = Source_Checking.Wikipedia()
		wikipedia.define_name(self.mock_source.source_name)
		self.assertTrue(wikipedia.has_page())

	def test_wikipedia_extract_context(self):
		
		wikipedia = Source_Checking.Wikipedia()
		wikipedia.define_name(self.mock_source.source_name)
		self.assertEqual(wikipedia.extract_context(),'BBC')

class TestLinguisticAnalyses(unittest.TestCase):
	ling_anal = Linguistic.LinguisticAnalyses()

	def wrong_proporstion_simple_br(self):
        #Source mock
		text_sample = 'Joao roubou poa na casa do Jaoo'
		vec_txt = text_sample.split(' ')
		#Tests
		self.assertEqual(self.ling_anal.wrong_proportion(vec_txt), 0.2)

if __name__ == '__main__':
	unittest.main()