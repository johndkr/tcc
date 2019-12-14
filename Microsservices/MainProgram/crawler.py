from newsplease import NewsPlease

def get_news_attributes(news_url):
	article = NewsPlease.from_url(news_url)
	return article