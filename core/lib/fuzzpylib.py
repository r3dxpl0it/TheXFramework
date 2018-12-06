'''_____________________________________________________________________
|[] R3DXPL0IT SHELL                                            |ROOT]|!"|
|"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""|"| 
|CODED BY > R3DXPLOIT(JIMMY)                                          | |
|EMAIL > RETURN_ROOT@PROTONMAIL.COM                                   | |
|GITHUB > https://github.com/r3dxpl0it                                | |
|WEB-PAGE > https://r3dxpl0it.Github.io                               |_|
|_____________________________________________________________________|/|
'''
from __future__ import print_function
import os
import sys
import time
import random
import warnings
import argparse
import threading
from math import log
from re import search, findall
from requests import get, post
import platform 
if not int(platform.python_version()[0]) >= 3 : 
	warnings.warn("Python Version not Satisfiable ! | Please Use Python3 ")
	raise SystemExit
try:
	import concurrent.futures
	from urllib.parse import urlparse # for python3
except : 
	raise SystemExit
import json
from core.config import user_agents , intels , badTypes

#end = red = white = green = yellow = run = bad = good = info = que = ''
warnings.filterwarnings('ignore') # Disable SSL related warnings

class Crawler : 
	def __init__ (self , target , crawl_level = 2 , 
			 thread_num = 2 , user_agent = None , moderator = None , additional_seed = list() ,
			 exclude = None , timeout = 10 , verbose = False): 
		self.internal = set()
		self.processed = self.files = set()
		self.exclude = exclude
		self.thread_num = thread_num
		self.timeout = timeout
		self.archive = False
		self.fuzzable = set()
		self.verbose = verbose 
		self.target = self.__url_formatter__(target)
		self.host = urlparse(self.target).netloc 
		self.internal.add(self.target)
		self.seeds = additional_seed
		if user_agent is None : 
			self.user_agent = user_agents
		else : 
			self.user_agent = user_agent
		if moderator is None :
			self.mod = print 
		else : 
			self.mod =  moderator
		self.crawl_level = crawl_level
		self.schema = self.target.split('//')[0]
	@staticmethod 
	def __url_formatter__(buff) : 
			if 'https://www.' in buff : 
				buff = buff.split('https://www.')
				buff = buff[1]
			elif 'https://' in buff : 
				buff = buff.split('https://')
				buff = buff[1]
			elif  'http://www.' in buff : 
				buff = buff.split('http://www.')
				buff = buff[1]
			elif  'http://' in buff : 
				buff = buff.split('http://')
				buff = buff[1]
			elif  'www.' in buff : 
				buff = buff.split('www.')
				buff = buff[1]
			try : 
				get('https://' + buff , verify = True)
				target = 'https://' + buff
			except Exception as e : 
				target = 'http://' + buff
			return target
	def archive_org_extractor(self , host, mode):
		url = '''http://web.archive.org/cdx/search?url=%s&matchType=%s&collapse=urlkey&fl=original&filter=mimetype:text/html&filter=statuscode:200&output=json&from=20180101&to=20181231''' % (host, mode)
		response = get(url).text
		parsed = json.loads(response)[1:]
		urls = []
		for item in parsed:
			urls.append(item[0])
		return urls
	def xmlParser(self ,response):
		return findall(r'<loc>(.*?)</loc>', response) 
	def Digger (self , url , verbose = False ) : 

		if self.archive  : 
			self.mod ('Fetching URLs from archive.org')
			if False:
				archived_urls = self.archive_org_extractor(domain, 'domain')
			else:
				archived_urls = self.archive_org_extractor(self.host, 'host')
			self.mod ('Retrieved %i URLs from archive.org' % (len(archived_urls) - 1))
			for url in archived_urls:
				if verbose : 
						self.mod('Internal page', url)
				self.internal.add(url)
		response = get(url + '/robots.txt', verify=False).text
		if '<body' not in response: 
			matches = findall(r'Allow: (.*)|Disallow: (.*)', response) 
			if matches:
				for match in matches: 
					match = ''.join(match) 
					if '*' not in match: 
						url = self.target + match
						self.internal.add(url)
	   
		response = get(url + '/sitemap.xml', verify=False).text 
		if '<body' not in response: 
			matches = self.xmlParser(response)
			if matches: 
				for match in matches:
					self.internal.add(match) 

	def __flash__ (self , function, links) : 
		thread_count = self.thread_num
		links = list(links)
		threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=thread_count)
		futures = (threadpool.submit(function, link) for link in links)
		for i, _ in enumerate(concurrent.futures.as_completed(futures)):
			if i + 1 == len(links) or (i + 1) % thread_count == 0:
				self.mod('Progress: %i/%i' % (i + 1, len(links)), end='\r')
	def is_link(self , url):
		conclusion = False 
		if url not in self.processed: 
			if url.split('.')[-1].lower() in badTypes:
				self.files.add(url)
			else:
				return True 
		return conclusion 

	def requester(self , url):
		self.processed.add(url) 
		time.sleep(self.timeout) 
		headers = {
		'Host' : self.host, 
		'User-Agent' : random.choice(self.user_agent),
		'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language' : 'en-US,en;q=0.5',
		'Accept-Encoding' : 'gzip',
		'DNT' : '1',
		'Connection' : 'close'}
		response = get(url, headers=headers, cookies = None , verify=False, timeout=self.timeout, stream=True , allow_redirects=False)
		print(response.txt)
		if 'text/html' in response.headers['content-type']:
			if response.status_code != '404':
				return response.text
			else:
				response.close()
				return 'jimmy'
		else:
			response.close()
			return 'jimmy'
	def extractor(self , url):
		response = self.requester(url)
		print(response)
		try : 
			matches = findall(r'<[aA].*href=["\']{0,1}(.*?)["\']', response)
		except :
			matches = []
		print(matches)
		for link in matches:
			if self.verbose : 
				self.mod('[VERBOSE]' , link)
			link = link.split('#')[0] 
			if self.is_link(link): 
				if link[:4] == 'http':
					if self.host in link :
						self.internal.add(link)
				elif link[:2] == '//':
					if link.split('/')[2].startswith(self.host):
						self.internal.add(self.schema + link)
				elif link[:1] == '/':
					self.internal.add(self.target + link)
				else:
					self.internal.add(self.target + '/' + link)
		
	def remove_regex(self , urls, regex):

		if not regex:
			return urls
		if not isinstance(urls, (list, set, tuple)):
			urls = [urls]
		try:
			non_matching_urls = [url for url in urls if not search(regex, url)]
		except TypeError:
			return []
		return non_matching_urls

	def launch(self) :
		try : 
			self.Digger(self.target)
		except ConnectionError : 
			self.mod("Connection Refused")
		except Exception as e : 
			self.mod("An Exception Raised During The process")
			self.mod(e)
		try : 
			for level in range(self.crawl_level):
				links = self.remove_regex(self.internal - self.processed, self.exclude) 
				if not links: 
					break
				try:
					self.__flash__(self.extractor, links)
				except KeyboardInterrupt:
					break
			for url in self.internal:	
				if '=' in url:
					self.fuzzable.add(url)
			datasets = [self.fuzzable]
			dataset_names = ['fuzzable']
			datasets = {'fuzzable': list(self.fuzzable) , 
			'internal' : list(self.internal)
			}
			return datasets
		except Exception as e :
			self.mod("An Exception Raised During The process")
			self.mod(e)
