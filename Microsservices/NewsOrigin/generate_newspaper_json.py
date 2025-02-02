from googlesearch import search
import json

def get_url():
	file = open('newspapers.txt', 'r', encoding='utf-8')

	pk = 1
	data = []

	for line in file:
		''' SOURCE_NAME '''
		source_name = line.split(' (',1)[0]

		''' SOURCE_URL '''
		source_url = ''
		srch = search("jornal " + source_name, tld="com", num=3, stop=3, pause=3)

		for j in srch: 
			website = j.split('//',1)[1].split('/',1)[0]
			if source_url == '' and website not in ['www.facebook.com','www.twitter.com', 'www.youtube.com']:
				source_url = website
		''' CRIAR ARQUIVO '''
		tmp = [
			{
				"source_name": source_name,
				"source_id": pk,
				"political_bias": 3,
				"factuality": 3,
				"version": [
					{
						"language":"PT-BR",
						"source_url":source_url,
						"source_twitter_handler":'',
						"source_wikipedia_page":''
					}
				]
			}
		]
		data.append(tmp[0])
		pk = pk + 1
		with open('saved.txt', 'w') as outfile:
			json.dump(data, outfile)

def get_twitter_handler():
	test = Source()
	test.set_source_id(1)
	test.load_source()

	srch = search("twitter " + test.source_name, tld="com", num=3, stop=3, pause=3)
	for j in srch: 
		website = j.split('//',1)[1].split('/',1)[0]
		if source_url == '' and website not in ['www.facebook.com','www.youtube.com']:
			source_url = website
	print(source_url)
	
#get_url()
#get_twitter_handler()
