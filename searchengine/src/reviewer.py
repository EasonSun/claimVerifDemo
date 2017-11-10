from google import google
from urllib2 import urlopen
from bs4 import BeautifulSoup as bs
from bs4.element import Comment
from urlparse import urlparse
import time
import pickle


badTags = set(['a', 'img', 'style', 'script', '[document]', 'head', 'title', 'link', 'ul', 'ol', 'li', 'dl', 'dt', 'dd', 'time', 'tr'])

class Reviewer(object):
    """docstring for Reviewer"""
    def __init__(self, query):
        self.query = query
        self.sources = []
        self.articles = []
        self.sourceMatrix = pickle.load(io.open(sourcePath, 'rb'))
        self.rsExtractor = relatedSnippetsExtractor(overlapThreshold, doc2vecPath=doc2vecPath)
        self.stanceClf = Classifier('stance', logPath, experimentPath)

        self.search()

    def search(self):
        num_page = 3
        search_results = google.search(self.query, num_page)
        articles = []
        sources = []
        for result in search_results:
            self.sources.append('{uri.netloc}'.format(uri=urlparse(result.link)))
            try:
                soup = bs(urlopen(result.link).read(), 'lxml')
            except:
                continue
            texts = soup.findAll(text=True)
            self.articles.append(filter(self.visible, texts))

    def visible(self, element):
        if element.parent.name in badTags:
            return False
        elif isinstance(element, Comment):
            return False
        return True
    
