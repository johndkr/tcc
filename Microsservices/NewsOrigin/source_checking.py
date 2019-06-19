import wikipediaapi as wiki
from googlesearch import search
import json
import tweepy
from urllib.parse import urlparse

CONSUMER_KEY = 'BGlnZtePhg8wAFgjCxzGqGIi8'
CONSUMER_SECRET = 'Ml2xY6MsLjYsrywAZwObXTXKboSt4W75sef01EdzzuXveXTlyO'
ACCESS_TOKEN = '755941172875501568-pJahNX54oxUa6GPXPSEYjMhTDM3wJJt'
ACCESS_TOKEN_SECRET = 'o88gaIlrHqYRvV2REOkd6iO4wp4LPNce1Y6hrB48sadCk'

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
	versions = []
	
	# System classification
	political_bias = POLITICAL_BIAS[3]
	factuality = FACTUALITY[0]

	def update_name(self,new_name):
		self.source_name = new_name

	def update_id(self,new_id):
		self.source_id = new_id

	def update_versions(self,versions):
		self.versions = versions

	def update_political_bias(self,new_political_bias):
		if new_political_bias not in (0,1,2,3,4,5,6):
			new_political_bias = self.political_bias
		else:
			self.political_bias = new_political_bias

	def update_factuality(self,new_factuality):
		if new_factuality not in (0,1,2,3):
			new_factuality = self.factuality
		else:
			self.factuality = new_factuality

	def load_source(self):
		with open('../../Microsservices/NewsOrigin/sources.json') as json_file:
			data = json.load(json_file)
		source = [item for item in data["items"] if item["source_id"] == self.source_id]
		
		self.update_name(source[0]["source_name"])
		self.update_political_bias(source[0]["political_bias"])
		self.update_factuality(source[0]["factuality"])
		self.update_versions(source[0]["versions"])

		return source[0]

	def get_source_id(self, source_name):
		with open('../../Microsservices/NewsOrigin/sources.json') as json_file:
			data = json.load(json_file)
		try:
			source = [item for item in data["items"] if item["source_name"] == source_name]
			self.source_id = source[0]["source_id"]
		except:
			source = []
			print("Fonte não encontrada")

		return self.source_id

	def set_source_id(self,source_id):
		self.source_id = source_id


	def save_source(self):
		with open("sources.json", "r") as json_file:
			data = json.load(json_file)

		tmp = data["items"]
		data["items"][self.source_id] = {
				"source_name": self.source_name,
				"source_id": self.source_id,
				"political_bias": self.political_bias,
				"factuality": self.factuality,
				"versions": self.versions
			}

		with open("sources.json", "w") as json_file:
			json.dump(data, json_file)

	def check_factuality(self):
		#Fact points, the more, the better
		fact_points = 0
		achievable_points = 4 #should change as the number of checks increases

		#Wikipedia
		wikipedia = Wikipedia()
		wikipedia.define_name(self.source_name)
		if wikipedia.has_page():
			fact_points = fact_points + 1
		else:
			pass

		#Twitter
		twitter = Twitter()
		twitter.define_name(self.source_name)
		if twitter.user_has_account():
			fact_points = fact_points + 1
		if twitter.user_is_verified():
			fact_points = fact_points + 1
		if twitter.user_has_location():
			fact_points = fact_points + 1
		#URL checking

		#Factuality test
		if (fact_points/achievable_points) > 0.5:
			self.update_factuality(3)
		else:
			self.update_factuality(0)

		return FACTUALITY[self.factuality]

	def get_stats(self):
		dict_pol = []
		dict_fac = []

		with open('../../Microsservices/NewsOrigin/sources.json') as json_file:
			data = json.load(json_file)

		for item in data["items"]:
			dict_pol.append(item["political_bias"])
			dict_fac.append(item["factuality"])

		political_bias = [{
				'0':dict_pol.count(0),
				'1':dict_pol.count(1),
				'2':dict_pol.count(2),
				'3':dict_pol.count(3),
				'4':dict_pol.count(4),
				'5':dict_pol.count(5),
				'6':dict_pol.count(6)
		}]

		factuality = [{
				'0':dict_fac.count(0),
				'1':dict_fac.count(1),
				'2':dict_fac.count(2),
				'3':dict_fac.count(3)
		}]
		return political_bias, factuality
			



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
		''' Verify if source a Wikipedia page '''
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
	
	''' TWITTER API '''
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	api = tweepy.API(auth)

	base_url = 'https://twitter.com/'
	source_name = ''
	source_id = 0
	has_account = False
	is_verified = False
	creation_date = '1970-01-01'
	has_location = False
	user = ''
	counts = [{
		"followers_count":0,
		"friends_count":0,
		"listed_count":0,
		"favourites_count":0,
		"statuses_count":0
	}]


	def define_name(self,source):
		''' Search and apply official Twitter name of the source '''
		self.source_name = source
		return self.source_name
	
	def get_user(self):
		try:
			self.user = self.api.get_user(self.source_name)
		except:
			self.user = ''
		return self.source_name

	def user_has_account(self):
		''' Verify Twitter account existance '''
		if self.user is not '':
			self.has_account = True
		else:
			self.has_account = False

		return self.has_account

	def user_is_verified(self):
		''' Verify if source has a verified Twitter profile '''
		if self.user_has_account():
			if self.user.verified:
				self.is_verified = True
			else:
				self.is_verified = False
		else:
			pass
		return self.is_verified

	def get_creation_date(self):
		''' Verify Twitter account creation date '''
		if self.user_has_account():
			self.creation_date = self.user.created_at
		else:
			pass
		return self.creation_date

	def user_has_location(self):
		''' Verify if source's location is explicitly provided in their Twitter profile ''' 
		if self.user_has_account():
			if self.user.location is not '':
				self.has_location = True
			else:
				self.has_location = False
		else:
			pass
		return self.has_location

	def url_match(self):
		''' Verify if given url to source's website match with the real in the databases '''
		return 0

	def get_counts(self):
		''' Store statistics about the number of friends, statuses and favorites '''
		if self.user_has_account():
			self.counts = [{
				"followers_count":self.user.followers_count,
				"friends_count":self.user.friends_count,
				"listed_count":self.user.listed_count,
				"favourites_count":self.user.favourites_count,
				"statuses_count":self.user.statuses_count
			}]
		else:
			pass
		return 0

	def check_description(self):
		''' Check description for signs of partisanship, political bias or lack of content '''
		return 0

	def load_all_info(self,source_name):
		self.define_name(source_name)
		self.get_user()
		self.user_has_account()
		self.user_is_verified()
		self.get_creation_date()
		self.user_has_location()
		self.get_counts()

		return 0

class URL():
	
	source_name = ''
	source_id = 0

	def orthographic(self):
		''' Check excessive use of special characters, section length and other type of typical phishing signs in source's URL '''
		return 0
	
	def credibility(self):
		''' Analyze where source is l and if uses htpps protocol '''
		return 0

#Teste
#twitter = Twitter()
#twitter.load_all_info('brunohvlemos')

def extractWebsite(url):
	# from urlparse import urlparse  # Python 2
	parsed_uri = urlparse(url)
	result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
	return result

def querySourceByUrl(url):
	with open('../../Microsservices/NewsOrigin/sources.json') as json_file:
		data = json.load(json_file)
	try:
		print(url)
		source = [item for item in data["items"] if item["versions"][0]["source_url"] == url]
		source_id = source[0]["source_id"]
	except:
		source = []
		print("Fonte não encontrada")
	return source

