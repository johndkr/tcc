import os, sys
import platform
if platform.system() == 'Windows':
	sys.path.append('..\\..\\')
else:
	sys.path.append('../../')
import string
import json
import re
from Microsservices.CommonUtil.Log import log_util
import tldextract

from lxml import html
import requests

class SourceAnalyses():

	log_manager = log_util.Log_Util(True)

	def count_links(self, text):
		self.log_manager.info("Counting number of links")
		urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
		nr_urls = len(urls)
		# print(nr_urls)
		return nr_urls

	def get_domain(self, url):
		ext = tldextract.extract(url)
		# print(ext.domain)
		return ext.domain

	def define_category(self, category):
		category = category
		return category

	def get_text_from_tweet(self, url):
		page = requests.get(url) # https://twitter.com/pseudobia_/status/1196879870095233025
		tree = html.fromstring(page.content)
		res = tree.xpath('//div[contains(@class, "permalink-tweet-container")]//p[contains(@class, "tweet-text")]//text()')
		print(str(res[0]))
		return str(res[0])
	
#sa = SourceAnalyses()
#sa.get_text_from_tweet('https://twitter.com/pseudobia_/status/1196879870095233025')