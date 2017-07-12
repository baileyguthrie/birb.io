from django.shortcuts import render
from keys import *
import twitter
from functions import *

#from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Create your views here.
def index(request):
    api = twitter.Api(consumer_key = ConsumerKey,
                  consumer_secret = ConsumerSecret,
                  access_token_key = AccessTokenKey,
                  access_token_secret = AccessTokenSecret)
    
    try:
        query=request.GET.__getitem__("query")
    except KeyError:
        return render(request, 'index.html')
    
    user_searched_for = False
    number_of_searches = 200
    
    if str(query)[0] == '@': # search for user
        user_searched_for = True
        try:
            user_timeline = api.GetUserTimeline(screen_name = query, count = number_of_searches)
        except twitter.error.TwitterError as e:
            error = str(e)
            return render(request, 'index.html', { 'error': error })
        user_results = analyze_tweets(user_timeline)
        if 'error' in user_results:
            return render(request, 'index.html', {'error': user_results['error'] })

    try:
        search_results = api.GetSearch(term = query, count = number_of_searches)
    except twitter.error.TwitterError as e:
        error = str(e)
        return render(request, 'index.html', { 'error': error })
    results = analyze_tweets(search_results)
    if 'error' in results:
        return render(request, 'index.html', { 'error': results['error'] })
    
    if user_searched_for:
        return render(request, 'index.html', {
            'query': query,
            'statement': results['statement'],
            'user_statement': user_results['statement'],
            'analysis': results['analysis'],
            'user_analysis': user_results['analysis'],
            'count': results['count'],
            'user_count': user_results['count']
        })
    else:
        return render(request, 'index.html', {
            'query': query,
            'statement': results['statement'],
            'analysis': results['analysis'],
            'count': results['count']
        })
    
def trending(request):
    api = twitter.Api(consumer_key = ConsumerKey,
                  consumer_secret = ConsumerSecret,
                  access_token_key = AccessTokenKey,
                  access_token_secret = AccessTokenSecret)

    number_of_searches = 200
    
    trends = api.GetTrendsCurrent()
    trends[:] = [x for x in trends if isEnglish(x.AsDict()['name'])] # Removes non english trends
    
    for i in range(len(trends)): # Leaves only name, url, and tweet_volume in trends
        trends[i] = trends[i].AsDict()
        trends[i].pop('timestamp', None)
        trends[i].pop('query', None)
        
    for trend in trends:
        try:
            search_results = api.GetSearch(term = trend['name'], count = number_of_searches)
        except twitter.error.TwitterError as e:
            error = str(e)
            return render(request, 'trending.html', { 'error': error })
        
        results = analyze_tweets(search_results)
        if 'error' in results:
            return render(request, 'index.html', {'error': results['error'] })
        trend.update({'statement': results['statement'], 'analysis': results['analysis'], 'count': results['count']})
        
    return render(request, 'trending.html', { 'trends': trends })
    
def compare(request):
    api = twitter.Api(consumer_key = ConsumerKey,
                  consumer_secret = ConsumerSecret,
                  access_token_key = AccessTokenKey,
                  access_token_secret = AccessTokenSecret)
    
    number_of_searches = 200
    
    comparison_results = []     
    try:
        query=request.GET.getlist("query")
    except KeyError:
        return render(request, 'compare.html')
    
    for search_term in query:
        try:
            search_results = api.GetSearch(term = search_term, count = number_of_searches)
        except twitter.error.TwitterError as e:
            error = str(e)
            return render(request, 'compare.html', { 'error': error })
        results = analyze_tweets(search_results)
        if 'error' in results:
            return render(request, 'compare.html', { 'error': results['error'] })
        comparison_results.append({'name': search_term, 'statement': results['statement'], 'analysis': results['analysis'], 'count': results['count']})
    
    return render(request, 'compare.html', {'results': comparison_results})
    
def info(request):
    return render(request, 'info.html')