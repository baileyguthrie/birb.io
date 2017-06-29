from django.shortcuts import render
import twitter
from keys import *
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Create your views here.
def index(request):
    
    api = twitter.Api(consumer_key = ConsumerKey,
                  consumer_secret = ConsumerSecret,
                  access_token_key = AccessTokenKey,
                  access_token_secret = AccessTokenSecret)
    
    #if not request.__contains__("search_box"):
    #    return render(request, 'index.html')
    
    try:
        query=request.GET.__getitem__("query")
    except KeyError:
        return render(request, 'index.html')
    
    neg, neu, pos, count = 0, 0, 0, 0
    number_of_searches = 100
    search_results = api.GetSearch(term = query, count=number_of_searches)
    analyzer = SentimentIntensityAnalyzer()
    for s in search_results:
        vs = analyzer.polarity_scores(s.text)
        neg += vs['neg']
        neu += vs['neu']
        pos += vs['pos']
        count += 1

    neg /= count
    neu /= count
    pos /= count
    
    if neg == 0:
        statement = "Maximum positivity!"
        analysis = "There was no detected negativity!"
    elif pos == 0:
        statement = "Maximum negativity..."
        analysis = "There was no detected positivity..."
    elif pos > neg:
        ratio = pos / neg
        statement = "Positive! :)"
        analysis = "The ratio of positivity to negativity is {}".format(ratio)
    elif neg > pos:
        ratio = neg / pos
        statement = "Negative... :("
        analysis = "The ratio of negativity to positivity is {}".format(ratio)
    else:
        statement = "This is a neutral subject!"
        analysis = ""
    
    return render(request, 'index.html', {
        'query': query,
        'statement': statement,
        'analysis': analysis
    })
    