import numpy as np
import os
import sys
import json
import io
import pickle
import heapq
import time
import math
from google import google
from urllib2 import urlopen
from bs4 import BeautifulSoup as bs
from bs4.element import Comment
from urlparse import urlparse
from multiprocessing import Pool, Manager, Process
import threading
import Queue
import requests
from aylienapiclient import textapi

from Classifier import Classifier
from relatedSnippetsExtractor import relatedSnippetsExtractor
from lgExtractor import lgExtractor


#sourcePath = 1
#from where python is called, so this path is really bad
doc2vecPath=u'../data/doc2vec_apnews.bin'
clfModelpath=u'../data/rf100.pkl'
MYWOT_API_ENDPOINT = "http://api.mywot.com/0.4/public_link_json2"
WOT_API_KEY = 'c51c261627d2abfa53f13bde73c033caa7789894'
AYLIEN_APP_ID = '7bcc8a9d'
AYLIEN_APP_KEY = '1f8be31fb1330b2ef6a9ec881de3b1bf'
lgPath = "../data/allFeatures.txt"

badTags = set(['a', 'img', 'style', 'script', '[document]', 'head', 'title', 'link', 'ul', 'ol', 'li', 'dl', 'dt', 'dd', 'time', 'tr'])

# helpers
# load at import. where to put this chunk???
rsExtractor = relatedSnippetsExtractor(.55, doc2vecPath=doc2vecPath)
stanceClf = Classifier('stance', None, None, clfModelpath)
lgExtractor = lgExtractor(lgPath)
aylien_client = textapi.Client(AYLIEN_APP_ID, AYLIEN_APP_KEY)

class topK(object):
	''' items are tuple (score, relatedSnippet, source) '''
	# @param {int} k an integer
	def __init__(self, k):
		self.k = k
		self.items = []
		# self.items = {'score': xx, 'relatedSnippet':yy, 'source':zz}
		heapq.heapify(self.items)

	# @param {int} num an integer
	# A source comes with relatedSnippets and scores
	# add each tuple as item to topK
	''' MORE SB, add has two functionality''' 
	def add(self, scores, relatedSnippets=None, source=None):
		if relatedSnippets is None:
			for score in scores:
				item = (score, None, None)
				if len(self.items) < self.k:
					heapq.heappush(self.items, item)
				elif score > self.items[0][0]:
					heapq.heappop(self.items)
					heapq.heappush(self.items, item)
		else:
			for score, relatedSnippet in zip(scores, relatedSnippets):
				item = (score, relatedSnippet, source)
				if len(self.items) < self.k:
					heapq.heappush(self.items, item)
				elif score > self.items[0][0]:
					heapq.heappop(self.items)
					heapq.heappush(self.items, item)

	# @return {int[]} the top k largest numbers in array
	def topk(self):
		return sorted(self.items, reverse=True)

	def avg(self):
		return sum([item[0] for item in self.items]) / len(self.items)

def searchHelper(item):
	sources.append('{uri.netloc}'.format(uri=urlparse(item)))
	try:
		soup = bs(urlopen(item).read(), 'lxml')
	except:
		return
	texts = soup.findAll(text=True)
	articles.append(filter(self.visible, texts))

class claimReviewer(object):
	"""docstring for ClassName"""
	def __init__(self, claim, cred=None):
		self.claim = claim
		self.cred = cred
		self.articles = []
		self.sources = []
		#self.sourceMatrix = pickle.load(io.open(sourcePath, 'rb'))

	def search(self):
		num_page = 3
		search_results = google.search(self.claim, num_page)
		links = [item.link for item in search_results if (not item.link.startswith('http://www.snopes.com')) and (not item.link.startswith('http://www.snopes.com'))]

		'''
		for link in links:
			# in order to link from an evidence snippet
			self.sources.append(link)
			#self.sources.append('{uri.netloc}'.format(uri=urlparse(link)))
		'''
		
		self.fetch_parallel(links) 
		print len(self.articles)
		'''
		while results.empty() is False:
			article, source = results.get()
			self.articles.append(article)
			self.sources.append(source)
		'''
		#print ('found %i articles' %len(self.articles))

	def review(self, articles=None, sources=None, training=False):
		def f(x):
			x_ = 2**(20*x)/1200
			return 1/(1+math.exp(-x_))
		
		if self.claim is None:
			return
		if articles is None:
			articles = self.articles
			sources = self.sources
		global posTK10
		global negTK10
		posTK10 = topK(10)
		negTK10 = topK(10)
		
		# call reviewHelper with params in parallel
		# this feeds posTK10 and negTK10
		lock = threading.Lock()
		articlesScores = self.gather_results([self.run_item(self.reviewHelper, article, source, lock) for article, source in zip(articles, sources)])

		''' get topK snippets '''
		posTKrelatedSnippets = [item[1] for item in posTK10.items]
		negTKrelatedSnippets = [item[1] for item in negTK10.items]

		'''
		# exampel to modify using item
		posTKrelatedSnippets = [item['relatedSnippet'] for item in posTK10.items]
		negTKrelatedSnippets = [item['relatedSnippet'] for item in negTK10.items]
		'''

		''' get topK sources '''
		posTKUrls = [item[2] for item in posTK10.items]
		negTKUrls = [item[2] for item in negTK10.items]
		# source matrix goes here ???
		posTKSources = ['{uri.netloc}'.format(uri=urlparse(item[2])) for item in posTK10.items]
		negTKSources = ['{uri.netloc}'.format(uri=urlparse(item[2])) for item in negTK10.items]

		''' format result '''
		if training is False:
			weight = 2.3

			print [score[0]*weight for score in articlesScores]
			print [score[1] for score in articlesScores]

			posScore = sum([score[0] for score in articlesScores])
			negScore = sum([score[1] for score in articlesScores])
			score = max(weight*posScore, negScore) / (len(articlesScores))

			result={}
			result['claim'] = self.claim
			if self.cred is not None:
				result['label'] = self.cred
			result['confidence'] = score#f(score)
			if (weight*posScore > negScore):
				result['predict'] = 0
				result['evis'] = posTKrelatedSnippets
				result['url'] = posTKUrls
				result['source'] = posTKSources

			else:
				result['predict'] = 1
				result['evis'] = negTKrelatedSnippets
				result['url'] = negTKUrls
				result['source'] = negTKSources

			return result
		else:
			return

	'''helper function below'''

	def addArticles(self, articlesScore, source):
		# number of articles
		self.articlesScore = articlesScore
		self.source = source

	'''
	# sourceMatrix
	# {source: (#support true, #support false, #refute true, #refute false)}
	def updateSource(self, articlesScore, source, cred):
		if source not in sourceMatrix:
			# smoothing
			sourceMatrix[source] = [1,1,1,1]
		#print (cred)
		#print (articlesScore)
		# support
		if articlesScore[0]*2.4 > articlesScore[1]:
			# true
			if cred == 0:
				sourceMatrix[source][0] += 1
			else:
				sourceMatrix[source][1] += 1
		else:
			if cred == 0:
				sourceMatrix[source][2] += 1
			else:
				sourceMatrix[source][3] += 1
	'''
	def read_url(self, url, queue):
		try:
			'''
			# use AYLEN instead
			data = urlopen(url).read()
			soup = bs(data, 'lxml')
			texts = soup.findAll(text=True)	#5s
			cleaned_texts = filter(self.visible, texts)
			'''
			article = aylien_client.Summarize({'url': url, 'sentences_percentage': 100})['text']
		except:
			print 'e'
			return
		#queue.put((data, url))
		self.articles.append(article)
		self.sources.append(url)

	def fetch_parallel(self, urls_to_load):
		results = Queue.Queue()
		threads = [threading.Thread(target=self.read_url, args = (url,results)) for url in urls_to_load]
		for t in threads:
			t.start()

		for t in threads:
			t.join()

		#

		'''
		while (result.empty() is False):
			print ('heres')
			soup = bs(urlopen(result.get()), 'lxml')
			texts = soup.findAll(text=True)	#5s
			self.articles.append(filter(self.visible, texts))
		'''
		#return results

	

	def visible(self, element):
		if element.parent.name in badTags:
			return False
		elif isinstance(element, Comment):
			return False
		return True

	def run_item(self, f, article, source, lock=None):
		result_info = [threading.Event(), None]
		def runit():
			result_info[1] = f(article, source, lock)
			result_info[0].set()
		thread = threading.Thread(target=runit)
		thread.start()
		#thread.join()
		return result_info

	def gather_results(self, result_infos):
		articlesScores = []
		# book keeping to  
		relatedSnippets = []
		posStanceScores = []
		negStanceScores = []
		for i in xrange(len(result_infos)):
			result_infos[i][0].wait()
			if result_infos[i][1] is None:
				continue
			articlesScore = result_infos[i][1]
			articlesScores.append(articlesScore)
			# updateSource ((posTK10.avg(), negTK10.avg()), source, cred)
			#relatedSnippets.extend(relatedSnippets_)
			#del relatedSnippets_
			#posStanceScores.extend(list(stanceScore_[:,0]))
			#negStanceScores.extend(list(stanceScore_[:,1]))  
		return articlesScores

	

	# core algo
	def reviewHelper(self, article, source, lock=None):
		t1 = time.time()
		_, relatedSnippetsX_, relatedSnippets_, _, overlapScores_ = rsExtractor.extract(self.claim, article)#' '.join(article))
		#print (time.time() - t1)
		# can be many other edge cases
		if relatedSnippets_ is not None:
			# source

			# lg
			lgX = lgExtractor.extract(relatedSnippets_)
			X = relatedSnippetsX_
			#X = np.concatenate((relatedSnippetsX_, lgX), axis=1)
			stanceProb_ = stanceClf.predict_porb(X)
			del relatedSnippetsX_
			# see paper
			# 0 for pos and 1 for neg results 
			stanceScore_ = stanceProb_ * overlapScores_
			
			# does not differentiate articles, i.e. nultiple snippets from the same article can be added to topK and show as the result
			lock.acquire()
			global posTK10
			global negTK10
			try:
				posTK10.add(stanceScore_[:,0], relatedSnippets_, source)
				negTK10.add(stanceScore_[:,1], relatedSnippets_, source)
			finally:
				lock.release()

			# select top 3 snippets to represent article score
			posTK3 = topK(3)
			negTK3 = topK(3)
			print source
			posTK3.add(stanceScore_[:,0], None, None)
			negTK3.add(stanceScore_[:,1], None, None)
			return ((posTK3.avg(), negTK3.avg()))
		else:
			return None
			#articlesScore.append((posTK3.avg(), negTK3.avg()))
			# updateSource ((posTK10.avg(), negTK10.avg()), source, cred)
			# relatedSnippets.extend(relatedSnippets_)
			# del relatedSnippets_
			#posStanceScores.extend(list(stanceScore_[:,0]))
			#negStanceScores.extend(list(stanceScore_[:,1]))  

	
