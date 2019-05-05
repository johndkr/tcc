import unittest
import wikipediaapi as wiki

############## SHOULDNT BE HERE ###################

POLITICAL_BIAS = {  0:'Extreme-left',
					1:'Left',
					2:'Center-left',
					3:'Center',
					4:'Center-right',
					5:'Right',
					6:'Extreme-right'
}

FACTUALITY = {      0:'Low',
					1:'Mixed',
					2:'High',
					3:'Very High'
}

class Source():
	
	# System infos
	source_name = ''
	source_id = 0
	
	# Web infos
	source_url = ''
	source_twitter_handler = ''
	source_wikipedia_page = ''
	
	# System classification
	political_bias = POLITICAL_BIAS[3]
	factuality = FACTUALITY[0]

	def update_name(self,new_name):
		self.source_name = new_name

	def update_id(self,new_id):
		self.source_id = new_id

	def update_url(self,new_url):
		self.source_url = new_url

	def update_twitter_handler(self,new_twitter_handler):
		self.source_twitter_handler = new_twitter_handler

	def update_wikipedia_page(self,new_wikipedia_page):
		self.source_wikipedia_page = new_wikipedia_page

	def update_political_bias(self,new_political_bias):
		self.political_bias = POLITICAL_BIAS[new_political_bias]

	def update_factuality(self,new_factuality):
		self.factuality = FACTUALITY[new_factuality]


######################## SOURCE #########################

class Wikipedia():
	
	#Wikipedia infos
	wiki_pt = wiki.Wikipedia('pt')
	wiki_en = wiki.Wikipedia('en')

	#Source infos
	base_pt_url = 'https://pt.wikipedia.org/wiki/'
	source_name = ''
	source_id = 0
	has_page = False
	page_title = ''
	page_summary = ''
	page_sections = []


	def define_name(self,source):
		''' Search and apply official Wikipedia name of the source '''
		self.source_name = source
		return self.source_name

	def has_page(self):
		''' Verify if source has a Wikipedia page '''
		page = self.wiki_pt.page(self.source_name)
		self.has_page = page.exists()
		return self.has_page

	def extract_context(self):
		''' Check content for signs of partisanship, political bias or lack of content '''
		
		if(self.has_page()):

			page = self.wiki_pt.page(self.source_name)
			
			self.page_title = page.title #Get title
			self.page_summary = page.summary #Get summary
			self.page_sections = page.sections #Get sections			

		return self.page_title

class Twitter():
	
	base_url = 'https://twitter.com/'
	source_name = ''
	source_id = 0
	has_account = False
	is_verified = False
	creation_date = '1970-01-01'
	has_location = False

	def define_name(self,source):
		''' Search and apply official Twitter name of the source '''
		return 0
	
	def has_account(self):
		''' Verify Twitter account existance '''
		return 0

	def is_verified(self):
		''' Verify if source has a verified Twitter profile '''
		return 0

	def creation_date(self):
		''' Verify Twitter account creation date '''
		return 0

	def has_location(self):
		''' Verify if source's location is explicitly provided in their Twitter profile ''' 
		return 0

	def url_match(self):
		''' Verify if given url to source's website match with the real in the databases '''
		return 0

	def counts(self):
		''' Store statistics about the number of friends, statuses and favorites '''
		return 0

	def check_description(self):
		''' Check description for signs of partisanship, political bias or lack of content '''
		return 0

class URL():
	
	source_name = ''
	source_id = 0

	def orthographic(self):
		''' Check excessive use of special characters, section length and other type of typical phishing signs in source's URL '''
		return 0
	
	def credibility(self):
		''' Analyze where source is hosted and if uses htpps protocol '''
		return 0

######################## TESTS #########################

class TestSourceFactuality(unittest.TestCase):
	
	mock_source = Source()
	
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

		wikipedia = Wikipedia()
		wikipedia.define_name(self.mock_source.source_name)
		self.assertTrue(wikipedia.has_page())

	def test_wikipedia_extract_context(self):
		
		wikipedia = Wikipedia()
		wikipedia.define_name(self.mock_source.source_name)
		self.assertEqual(wikipedia.extract_context(),'BBC')

if __name__ == '__main__':
	unittest.main()