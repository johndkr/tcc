from flask import Flask, render_template, request
import sys
from urllib.parse import urlparse
sys.path.append('..\\..\\')

from Microsservices.NewsOrigin import source_checking as Source_Checking
from Microsservices.Linguistic import linguistic as Linguistic
from Microsservices.MainProgram import main as Main
import Microsservices.MainProgram.data.parameters as Parameters
from Microsservices.Linguistic import linguistic as Linguistic

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
		print(processed_url)
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

	return render_template("index_mock.html", link_mode = link_mode, length = length, id_news = newsInfo[0], fake_status = newsInfo[1], keywords = keywords, 
							num_articles = newsInfo[3], sources = sources, authors = authors, titles = titles, descriptions = descriptions,
							url_original = processed_text, fonte = source[0]["source_name"], prob_fake = round(fact_points*100,2), pb = Source_Checking.POLITICAL_BIAS[political_bias], sf = Source_Checking.FACTUALITY[source_factuality])

if __name__ == "__main__":
	app.run(debug=True)