from flask import Flask, render_template, request
import sys
from urllib.parse import urlparse
sys.path.append('..\\..\\')

from Microsservices.NewsOrigin import source_checking as Source_Checking
from Microsservices.Linguistic import linguistic as Linguistic
from Microsservices.MainProgram import main as Main
import Microsservices.MainProgram.data.parameters as Parameters
import Microsservices.MainProgram.data.news_mock as Mock
from Microsservices.Linguistic import linguistic as Linguistic

import tweepy
import time
from random import randint 

CONSUMER_KEY = 'BGlnZtePhg8wAFgjCxzGqGIi8'
CONSUMER_SECRET = 'Ml2xY6MsLjYsrywAZwObXTXKboSt4W75sef01EdzzuXveXTlyO'
ACCESS_TOKEN = '755941172875501568-pJahNX54oxUa6GPXPSEYjMhTDM3wJJt'
ACCESS_TOKEN_SECRET = 'o88gaIlrHqYRvV2REOkd6iO4wp4LPNce1Y6hrB48sadCk'

ling = Linguistic.LinguisticAnalyses()

def is_url(url):
	try:
		result = urlparse(url)
		return all([result.scheme, result.netloc])
	except ValueError:
		return False


app = Flask(__name__)

@app.route("/")
def home():
	return render_template("exemplo.html")

@app.route('/', methods=['POST'])
def my_form_post():
	text = request.form['newsLink']
	processed_text = text

	id_news = 0
	newsInfo = ['','','','','']
	keywords = 0
	articles = 0
	length = 0
	sources = ['']
	authors = ['']
	titles = ['']
	descriptions = ['']
	source = [{"source_name": ""}]
	fact_points = 0
	political_bias = 0
	source_factuality = 0

	link_mode = False
	if is_url(processed_text):
		processed_url = Source_Checking.extractWebsite(processed_text)
		source = Source_Checking.querySourceByUrl(processed_url)
		political_bias = source[0]["political_bias"]
		source_factuality = source[0]["factuality"]

		fact_points = 0.5*Parameters.POLITICAL_BIAS_BASE[str(political_bias)] + 0.5*Parameters.FACTUALITY_BASE[str(source_factuality)]
		newsInfo[1] = fact_points
		sources[0] = processed_url

		link_mode = True
	else:
		id_news = Main.getNews(processed_text)
		newsInfo = Main.getNewsInfo(id_news)
		keywords = ",".join(str(x) for x in newsInfo[2])
		articles = newsInfo[4]
		length = len(articles)
		sources = [item['source']['name'] for item in articles]
		authors = [item['author'] for item in articles]
		titles = [item['title'] for item in articles]
		descriptions = [item['description'] for item in articles]

	return render_template("index.html", link_mode = link_mode, length = length, id_news = newsInfo[0], fake_status = newsInfo[1], keywords = keywords, 
							num_articles = newsInfo[3], sources = sources, authors = authors, titles = titles, descriptions = descriptions,
							url_original = processed_text, fonte = source[0]["source_name"], prob_fake = round(fact_points*100,2), pb = Source_Checking.POLITICAL_BIAS[political_bias], sf = Source_Checking.FACTUALITY[source_factuality])
	
@app.route('/get_linguist_prob')
def linguistic_page():
	result = "Nenhum resultado ainda"
	return render_template("linguistic.html", result = result)

@app.route('/get_linguist_prob', methods=['POST'])
def get_linguist_probability():
    data = request.form['linguisticBox']

    if (len(data)>0):
        result = ling.make_linguistic_analyses(data)
    else:
        result = "Ops... there is no text to be analysed!"

    return render_template("linguistic.html", result = result)

    
@app.route("/mock")
def home_mock():
	return render_template("exemplo_mock.html")

@app.route('/mock', methods=['POST'])
def my_form_post_mock():
	''' TWITTER API '''
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	api = tweepy.API(auth)
	twitter = Source_Checking.Twitter()
	twitter.load_all_info('brunohvlemos')
	user = api.get_user('brunohvlemos')
	locations = []
	user = ''
	try:
		for user in tweepy.Cursor(api.followers, screen_name="brunohvlemos").items():
			try:
				user2 = user.rfind(" ",0,len(user))
				user3 = api.get_user(user2)
				locations.append(user3.location)
			except tweepy.TweepError:
				time.sleep(60 * 15)
			continue
	except:
		print ("Não rolou")

	print(locations)
	text = request.form['newsLink']
	processed_text = text

	id_news = 0
	newsInfo = ['','','','','']
	keywords = 0
	articles = 0
	length = 0
	sources = ['']
	authors = ['']
	titles = ['']
	descriptions = ['']
	source = [{"source_name": ""}]
	fact_points = 0
	political_bias = 0
	source_factuality = 0
	num_cidades = randint(3,52)
	link_mode = False
	ling_result = -1
	multiplier_factor = 1/3
	if is_url(processed_text):
		processed_url = Source_Checking.extractWebsite(processed_text)
		if (processed_url == 'https://twitter.com/' or processed_url == 'https://theintercept.com/'):
			news = [item for item in Mock.noticias_mock["articles"] if item["url"] == processed_text]
			data = news[0]["text"]
			print (data)
			ling_result = ling.make_linguistic_analyses(data)

		source = Source_Checking.querySourceByUrl(processed_url)
		political_bias = source[0]["political_bias"]
		source_factuality = source[0]["factuality"]
		print(ling_result["FakeNewChance"])
		if (ling_result == -1):
			multiplier_factor = 1/2
		fact_points = multiplier_factor*Parameters.POLITICAL_BIAS_BASE[str(political_bias)] + multiplier_factor*Parameters.FACTUALITY_BASE[str(source_factuality)]
		newsInfo[1] = fact_points
		sources[0] = processed_url

		link_mode = True
	else:
		id_news = Main.getNews(processed_text)
		newsInfo = Main.getNewsInfo(id_news)
		keywords = ",".join(str(x) for x in newsInfo[2])
		articles = newsInfo[4]
		length = len(articles)
		sources = [item['source']['name'] for item in articles]
		authors = [item['author'] for item in articles]
		titles = [item['title'] for item in articles]
		descriptions = [item['description'] for item in articles]

	return render_template("index_mock.html", link_mode = link_mode, length = length, id_news = newsInfo[0], fake_status = newsInfo[1], keywords = keywords, 
							num_articles = newsInfo[3], sources = sources, authors = authors, titles = titles, descriptions = descriptions,
							url_original = processed_text, fonte = source[0]["source_name"], prob_fake = round(fact_points*100,2), pb = Source_Checking.POLITICAL_BIAS[political_bias], sf = Source_Checking.FACTUALITY[source_factuality], locations = locations, num_cidades = num_cidades)

if __name__ == "__main__":
	app.run(debug=True)