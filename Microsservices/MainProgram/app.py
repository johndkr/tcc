from flask import Flask, render_template, request
import os, sys
import platform
from urllib.parse import urlparse

if platform.system() == 'Windows':
	sys.path.append('..\\..\\')
else:
	sys.path.append('../../')

from Microsservices.NewsOrigin import source_checking as Source_Checking
from Microsservices.NewsOrigin import source as Source
from Microsservices.Linguistic import linguistic as Linguistic
from Microsservices.MainProgram import main as Main
from Microsservices.MainProgram import classification as Classification
from Microsservices.MainProgram import crawler as Crawler
import Microsservices.MainProgram.data.parameters as Parameters
import Microsservices.MainProgram.data.news_mock as Mock

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
	processed_text = Source_Checking.extractWebsite(text)

	domain = ''
	source = [{"source_name": ""}]

	link_mode = False
	if is_url(processed_text):
		obj_source = Source.SourceAnalyses()
		domain = obj_source.get_domain(processed_text)
		source = Source_Checking.querySourceByUrl(processed_text)
		if(domain == 'twitter'):
			article_text = obj_source.get_text_from_tweet(text)
		else:
			article = Crawler.get_news_attributes(text)
			article_text = article.text
		fake = Classification.classify_news(False,article_text)
		link_mode = True
	else:
		print("Não é um link")

	return render_template("index.html", link_mode = link_mode, url_original = processed_text, fonte = source[0]['source_name'], 
										fake_true = fake)
	
@app.route('/get_stats')
def get_stats():
	result_true_dict, result_fake_dict = Classification.make_statistics()

	true_feeling = result_true_dict['feeling']
	true_nr_links = result_true_dict['nr_links']
	true_nr_locations = result_true_dict['nr_locations']
	true_verbos = result_true_dict['verbos']
	true_substantivos = result_true_dict['substantivos']
	true_adverbios = result_true_dict['adverbios']
	true_pronomes = result_true_dict['pronomes']
	true_artigos = result_true_dict['artigos']
	true_adjetivo = result_true_dict['adjetivo']
	true_numerais = result_true_dict['numerais']
	true_preposicoes = result_true_dict['preposicoes']
	true_conjuncoes = result_true_dict['conjuncoes']
	true_pontuacao = result_true_dict['pontuacao']
	true_interjeicoes = result_true_dict['interjeicoes']
	true_verbos_modais = result_true_dict['verbos_modais']
	true_n_palvaras = result_true_dict['n_palvaras']
	true_prop_palavras_erradas = result_true_dict['prop_palavras_erradas']
	true_n_camel_case = result_true_dict['n_camel_case']
	true_n_upper_case = result_true_dict['n_upper_case']
	true_n_pronome_1 = result_true_dict['n_pronome_1']
	true_n_pronome_1_plural = result_true_dict['n_pronome_1_plural']
	true_n_pronome_2 = result_true_dict['n_pronome_2']
	true_n_characteres = result_true_dict['n_characteres']
	true_avg_sentence = result_true_dict['avg_sentence']
	true_avg_word_length = result_true_dict['avg_word_length']

	fake_feeling = result_fake_dict['feeling']
	fake_nr_links = result_fake_dict['nr_links']
	fake_nr_locations = result_fake_dict['nr_locations']
	fake_verbos = result_fake_dict['verbos']
	fake_substantivos = result_fake_dict['substantivos']
	fake_adverbios = result_fake_dict['adverbios']
	fake_pronomes = result_fake_dict['pronomes']
	fake_artigos = result_fake_dict['artigos']
	fake_adjetivo = result_fake_dict['adjetivo']
	fake_numerais = result_fake_dict['numerais']
	fake_preposicoes = result_fake_dict['preposicoes']
	fake_conjuncoes = result_fake_dict['conjuncoes']
	fake_pontuacao = result_fake_dict['pontuacao']
	fake_interjeicoes = result_fake_dict['interjeicoes']
	fake_verbos_modais = result_fake_dict['verbos_modais']
	fake_n_palvaras = result_fake_dict['n_palvaras']
	fake_prop_palavras_erradas = result_fake_dict['prop_palavras_erradas']
	fake_n_camel_case = result_fake_dict['n_camel_case']
	fake_n_upper_case = result_fake_dict['n_upper_case']
	fake_n_pronome_1 = result_fake_dict['n_pronome_1']
	fake_n_pronome_1_plural = result_fake_dict['n_pronome_1_plural']
	fake_n_pronome_2 = result_fake_dict['n_pronome_2']
	fake_n_characteres = result_fake_dict['n_characteres']
	fake_avg_sentence = result_fake_dict['avg_sentence']
	fake_avg_word_length = result_fake_dict['avg_word_length']

	return render_template("estatisticas.html", true_feeling  = true_feeling ,true_nr_links  = true_nr_links ,true_nr_locations  = true_nr_locations ,
		true_verbos  = true_verbos ,true_substantivos  = true_substantivos ,true_adverbios  = true_adverbios ,true_pronomes  = true_pronomes ,
		true_artigos  = true_artigos ,true_adjetivo  = true_adjetivo ,true_numerais  = true_numerais ,true_preposicoes  = true_preposicoes ,
		true_conjuncoes  = true_conjuncoes ,true_pontuacao  = true_pontuacao ,true_interjeicoes  = true_interjeicoes ,true_verbos_modais  = true_verbos_modais ,
		true_n_palvaras  = true_n_palvaras ,true_prop_palavras_erradas  = true_prop_palavras_erradas ,true_n_camel_case  = true_n_camel_case ,
		true_n_upper_case  = true_n_upper_case ,true_n_pronome_1  = true_n_pronome_1 ,true_n_pronome_1_plural  = true_n_pronome_1_plural ,
		true_n_pronome_2  = true_n_pronome_2 ,true_n_characteres  = true_n_characteres ,true_avg_sentence  = true_avg_sentence ,
		true_avg_word_length  = true_avg_word_length ,fake_feeling  = fake_feeling ,fake_nr_links  = fake_nr_links ,fake_nr_locations  = fake_nr_locations ,
		fake_verbos  = fake_verbos ,fake_substantivos  = fake_substantivos ,fake_adverbios  = fake_adverbios ,fake_pronomes  = fake_pronomes ,
		fake_artigos  = fake_artigos ,fake_adjetivo  = fake_adjetivo ,fake_numerais  = fake_numerais ,fake_preposicoes  = fake_preposicoes ,
		fake_conjuncoes  = fake_conjuncoes ,fake_pontuacao  = fake_pontuacao ,fake_interjeicoes  = fake_interjeicoes ,fake_verbos_modais  = fake_verbos_modais ,
		fake_n_palvaras  = fake_n_palvaras ,fake_prop_palavras_erradas  = fake_prop_palavras_erradas ,fake_n_camel_case  = fake_n_camel_case ,
		fake_n_upper_case  = fake_n_upper_case ,fake_n_pronome_1  = fake_n_pronome_1 ,fake_n_pronome_1_plural  = fake_n_pronome_1_plural ,
		fake_n_pronome_2  = fake_n_pronome_2 ,fake_n_characteres  = fake_n_characteres ,fake_avg_sentence  = fake_avg_sentence ,
		fake_avg_word_length  = fake_avg_word_length 
	)

@app.route('/get_linguist_prob', methods=['POST'])
def get_linguist_probability():
    data = request.form['linguisticBox']

    if (len(data)>0):
        result = ling.make_linguistic_analyses(data)
    else:
        result = "Ops... there is no text to be analysed!"

    return render_template("linguistic.html", result = result)

if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0', port=80)