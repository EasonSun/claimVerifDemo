# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from src.claimReviewer import claimReviewer
import time
# from project.application.web_search....
#from web_search import google


def search(request):
    # search query, a claim
    query = request.GET.get('term')
    #term = int(term[0])
    #result,url = test(term)
    #return render_to_response('search.html',{'result':result,'url':url})
    #return your cred and related articles,put your .py in google\searchengine file
    #for i in range(len(article)):
    #    article[i] = article[i] + '<br/>credibility:' + overlap[i] 
    query_text = '' 
    claim = ''
    label = 0
    predict = 0
    confidence = 0
    all_labels = '' 
    evis_url_source = []


    if query is not None:
        import time
        t0 = time.time()
        reviewer = claimReviewer(query)
        t1 = time.time()
        reviewer.search()
        t2 = time.time()
        print (t2 - t1)
        result = reviewer.review()
        print (time.time() - t2)
        result['time'] = time.time() - t0
        query_text = result['claim']
        claim = 'Claim: ' + result['claim']
        evis = result['evis']
        predict = result['predict']
        confidence = result['confidence']
        url = result['url']
        source = result['source']
        evis_url_source = zip(evis,url,source)
        time = result['time']
        if 'label' in result.keys():
            label = result['label']
            all_labels = "label: " + ('TRUE' if label==0 else 'FAKE') + " predict: " + ('TRUE' if predict==0 else 'FAKE') + " confidence: %.2f%%" %(confidence*100) + ' using: %.3fs'%time
        else:
           all_labels = "predict: " + ('TRUE' if predict==0 else 'FAKE') + " confidence: %.2f%%" %(confidence*100) + ' using: %.3fs'%time
    '''
    all_labels = "label: 0 predict: 0 confidence: 0.61462561862"
    evis = [u'share of leafy greens sales volume 2005 change in sales volume bagged salads without spinach', u'coli from spinach grown on single california field investigators traced the prepackaged spinach back to natural selection foods and baby spinach five deaths were linked to the outbreak', u'went out in september 2006 at least 205 reports of illnesses and three deaths across twentyfive states were confirmed to have been caused by e all contaminated spinach was sold under the dole brand', u'in recent years there have been e coli outbreaks caused by contaminated signs symptoms and treatment', u'in summer 2010 more than , 900 people were reportedly sickened by salmonella found in eggs produced by which voluntarily recalled about halfbillion eggs nationwide', u'coli outbreak occurred in 2012 thirtythree people became sick and thirteen were hospitalized after eating two people suffered kidney failure', u'isolated from an opened package of baby spinach best if used by august 30 packed by in the refrigerator of an ill new mexico resident matched that of the outbreak strain', u'28563400000 artichoke wheatberry salad 28563700000 southwest soofoo salad 28563800000 southwest soofoo salad', u'as we reported in april there was an e coli outbreak last year linked to bag lettuce this time its allegedly bagged spinach that is contaminated', u'it was distributed throughout colorado kansas and missouri and through retail grocer dole recalls limited number of salads the salads may be contaminated with listeria monocytogenes']
    '''
    context = {
            'term': query_text, #term,
            'claim': claim,
            'all_labels': all_labels, 
            'evis_url_source':evis_url_source
    }
    
    #return render_to_response('search.html',{'term':term,'cred':cred,'article':article})
    return render_to_response('main.html', context)
'''
def home(request):
    term = request.GET.get('term')
    result = stance(term)
    claim = result['claim']
    evis = result['evis']
    predict = result['predict']
    confidence = result['confidence']
    if 'label' in result.keys():
        label = result['label']
        all_labels = "label: " + str(label) + " predict: " + str(predict) + " confidence: " + str(confidence)
    else:
        all_labels = "predict: " + str(predict) + " confidence: " + str(confidence)            
    
    all_labels = "label: 0 predict: 0 confidence: 0.61462561862"
    evis = [u'share of leafy greens sales volume 2005 change in sales volume bagged salads without spinach', u'coli from spinach grown on single california field investigators traced the prepackaged spinach back to natural selection foods and baby spinach five deaths were linked to the outbreak', u'went out in september 2006 at least 205 reports of illnesses and three deaths across twentyfive states were confirmed to have been caused by e all contaminated spinach was sold under the dole brand', u'in recent years there have been e coli outbreaks caused by contaminated signs symptoms and treatment', u'in summer 2010 more than , 900 people were reportedly sickened by salmonella found in eggs produced by which voluntarily recalled about halfbillion eggs nationwide', u'coli outbreak occurred in 2012 thirtythree people became sick and thirteen were hospitalized after eating two people suffered kidney failure', u'isolated from an opened package of baby spinach best if used by august 30 packed by in the refrigerator of an ill new mexico resident matched that of the outbreak strain', u'28563400000 artichoke wheatberry salad 28563700000 southwest soofoo salad 28563800000 southwest soofoo salad', u'as we reported in april there was an e coli outbreak last year linked to bag lettuce this time its allegedly bagged spinach that is contaminated', u'it was distributed throughout colorado kansas and missouri and through retail grocer dole recalls limited number of salads the salads may be contaminated with listeria monocytogenes']
    context = {
            'claim':claim,'all_labels':all_labels,'evis':evis
    }
    
    #return render_to_response('search.html',{'term':term,'cred':cred,'article':article})
    return render_to_response('homepage.html',context)
'''