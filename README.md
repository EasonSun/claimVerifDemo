RUN

Run in virtual enviroment 
$workon tmp. 
$cd finalversion/google
$python manage.py runserver
then open 127.0.0.1:8000

FUNCTION
The python file remaining to change is searchengine/test1.py
The function remaining to change is test1.py def stance(term)
It would be used in views.py
The input of this function is term(testing claim).
The output of this function is result, a dic type ouput. The attribute of it including label,predict,confidence,claim and evis. An example output would be 

result['label'] = 0 
result['predict'] = 0
result['confidence'] = 0.61462561862
result['claim'] = 'Prepackaged salads and spinach may contain E. coli.'
result['evis'] = [u'share of leafy greens sales volume 2005 change in sales volume bagged salads without spinach', u'coli from spinach grown on single california field investigators traced the prepackaged spinach back to natural selection foods and baby spinach five deaths were linked to the outbreak', u'went out in september 2006 at least 205 reports of illnesses and three deaths across twentyfive states were confirmed to have been caused by e all contaminated spinach was sold under the dole brand', u'in recent years there have been e coli outbreaks caused by contaminated signs symptoms and treatment', u'in summer 2010 more than , 900 people were reportedly sickened by salmonella found in eggs produced by which voluntarily recalled about halfbillion eggs nationwide', u'coli outbreak occurred in 2012 thirtythree people became sick and thirteen were hospitalized after eating two people suffered kidney failure', u'isolated from an opened package of baby spinach best if used by august 30 packed by in the refrigerator of an ill new mexico resident matched that of the outbreak strain', u'28563400000 artichoke wheatberry salad 28563700000 southwest soofoo salad 28563800000 southwest soofoo salad', u'as we reported in april there was an e coli outbreak last year linked to bag lettuce this time its allegedly bagged spinach that is contaminated', u'it was distributed throughout colorado kansas and missouri and through retail grocer dole recalls limited number of salads the salads may be contaminated with listeria monocytogenes']
                                 