from django.shortcuts import render
import twitter
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Create your views here.
def index(request):
    
    with open("config.json", "r") as f:
        config = json.load(f)
        CONSUMER_KEY = config["ConsumerKey"]
        CONSUMER_SECRET = config["ConsumerSecret"]
        ACCESS_TOKEN_KEY = config["AccessTokenKey"]
        ACCESS_TOKEN_SECRET = config["AccessTokenSecret"]
    
    api = twitter.Api(consumer_key = CONSUMER_KEY,
                  consumer_secret = CONSUMER_SECRET,
                  access_token_key = ACCESS_TOKEN_KEY,
                  access_token_secret = ACCESS_TOKEN_SECRET)
    
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
    